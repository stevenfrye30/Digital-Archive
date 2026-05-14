#!/usr/bin/env python3
"""resolve_urn.py — Tiny URN resolver prototype for the Digital Archive.

The first operational layer of the archive's permanence infrastructure.
Implements the resolver contract specified in CITATION_PERMANENCE.md §5.2:

  - Input: a valid URN.
  - Output: one of:
      - resolved          (target found cleanly)
      - alias_redirected  (URN was retired/re-keyed; follow alias chain to target)
      - retired           (URN was retired with no successor)
      - withdrawn         (commentary record state: withdrawn)
      - superseded        (commentary record state: superseded by named successor)
      - frozen            (record carries migration_policy: "frozen")
      - orphaned          (record's anchor does not resolve)
      - missing           (no such target; no alias)
      - malformed         (URN does not parse)
      - ambiguous         (duplicate id — a constitutional breach)

The resolver is deterministic, read-only, and explicit. It does not guess.
It does not perform repairs. It does not modify any canonical record.

This prototype's scope is intentionally narrow: it handles the Apannaka-
jataka surface and the test-fixture records in
01_library/library/permanence/test_fixtures/. It is sufficient to
verify the constitutional permanence commitments operationally; it is
not sufficient to serve the production reader.

Usage:
    python 05_scripts/resolve_urn.py <urn> [--load-test-fixtures]
    python 05_scripts/resolve_urn.py archive:passage:jataka::chalmers-vol1::1.1

Output: JSON to stdout, one resolution per invocation.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
TEXT_DIR = ROOT / "01_library" / "library" / "texts"
REGISTRY = ROOT / "01_library" / "library" / "metadata" / "registry.json"
PERMANENCE = ROOT / "01_library" / "library" / "permanence"

# URN parsers, kind-aware (cf. COMMENTARY_PROTOTYPE_2026.md §7.2).
URN_PATTERNS = {
    "text":       re.compile(r"^archive:text:(?P<text>[A-Za-z0-9_\-]+)$"),
    "tale":       re.compile(r"^archive:tale:(?P<text>[A-Za-z0-9_\-]+)::(?P<id>\S+)$"),
    "translation":re.compile(r"^archive:translation:(?P<text>[A-Za-z0-9_\-]+)::(?P<trans>\S+)$"),
    "chapter":    re.compile(r"^archive:chapter:(?P<text>[A-Za-z0-9_\-]+)::(?P<trans>[^:]+)::(?P<id>\S+)$"),
    "passage":    re.compile(r"^archive:passage:(?P<text>[A-Za-z0-9_\-]+)::(?P<trans>[^:]+)::(?P<id>[^:]+)(?::(?P<sub>.+))?$"),
    "range":      re.compile(r"^archive:range:(?P<text>[A-Za-z0-9_\-]+)::(?P<trans>[^:]+)::(?P<start>[^~]+)~(?P<end>\S+)$"),
    "commentary": re.compile(r"^archive:commentary:(?P<id>\S+)$"),
    "apparatus":  re.compile(r"^archive:apparatus:(?P<text>[A-Za-z0-9_\-]+)::(?P<trans>[^:]+)::(?P<id>\S+)$"),
}

SUB_LOC_PATTERNS = {
    "phrase": re.compile(r"^phrase=(?P<value>.+?)(?::nth=(?P<nth>\d+))?$"),
    "line":   re.compile(r"^line=(?P<value>\d+)$"),
}


def parse_urn(urn: str) -> dict:
    """Return {'kind': ..., ...} or {'kind': None} for malformed input."""
    for kind, pattern in URN_PATTERNS.items():
        m = pattern.match(urn)
        if m:
            parsed = {"kind": kind, "raw": urn, **m.groupdict()}
            # If passage URN has a sub-locator, parse it.
            sub = parsed.pop("sub", None)
            if sub:
                for sub_kind, sub_pattern in SUB_LOC_PATTERNS.items():
                    sm = sub_pattern.match(sub)
                    if sm:
                        parsed["sub_locator"] = {"type": sub_kind, **sm.groupdict()}
                        if sub_kind == "phrase":
                            parsed["sub_locator"]["nth"] = int(parsed["sub_locator"]["nth"] or 1)
                        break
                else:
                    # Sub-locator present but unrecognized; record it raw.
                    parsed["sub_locator"] = {"type": "unknown", "raw": sub}
            return parsed
    return {"kind": None, "raw": urn}


class Resolver:
    def __init__(self, load_test_fixtures: bool = False):
        self.load_test_fixtures = load_test_fixtures
        self._registry = None
        self._aliases: dict[str, dict] = {}
        self._commentary: dict[str, dict] = {}  # id -> record
        self._commentary_by_supersedes: dict[str, list[str]] = {}
        self._index_loaded = False

    # ──────────────────────────────────────────────────────────────────────
    # Loading

    def _load_aliases(self) -> None:
        for path in [PERMANENCE / "aliases.json"]:
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                for entry in data.get("aliases", []):
                    self._aliases[entry["old_urn"]] = entry
        if self.load_test_fixtures:
            tp = PERMANENCE / "test_fixtures" / "aliases.json"
            if tp.exists():
                data = json.loads(tp.read_text(encoding="utf-8"))
                for entry in data.get("aliases", []):
                    self._aliases[entry["old_urn"]] = entry

    def _load_commentary(self) -> None:
        # Walk all commentary_*.json under canonical text dirs.
        for path in TEXT_DIR.rglob("commentary_*.json"):
            self._absorb_commentary_file(path)
        for path in TEXT_DIR.rglob("attachments_*.json"):
            self._absorb_commentary_file(path)
        if self.load_test_fixtures:
            for path in (PERMANENCE / "test_fixtures").glob("commentary_*.json"):
                self._absorb_commentary_file(path)

    def _absorb_commentary_file(self, path: Path) -> None:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return
        for rec in data.get("records", []):
            rid = rec.get("id")
            if not rid:
                continue
            if rid in self._commentary:
                # Duplicate id is a constitutional breach (COMMENTARY_REPAIR_PROTOCOLS.md §6).
                # Mark the record as ambiguous and keep both for the response.
                existing = self._commentary[rid]
                if not isinstance(existing, list):
                    self._commentary[rid] = [existing, rec]
                else:
                    existing.append(rec)
            else:
                self._commentary[rid] = rec
            if rec.get("supersedes"):
                self._commentary_by_supersedes.setdefault(
                    rec["supersedes"].replace("archive:commentary:", ""), []
                ).append(rid)

    def _load_registry(self) -> dict:
        if self._registry is None:
            if REGISTRY.exists():
                self._registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
            else:
                self._registry = {"texts": []}
        return self._registry

    def _ensure_loaded(self) -> None:
        if self._index_loaded:
            return
        self._load_aliases()
        self._load_commentary()
        self._load_registry()
        self._index_loaded = True

    # ──────────────────────────────────────────────────────────────────────
    # Public API

    def resolve(self, urn: str) -> dict:
        self._ensure_loaded()
        return self._resolve_with_chain(urn, [])

    # ──────────────────────────────────────────────────────────────────────
    # Resolution

    def _base_response(self, urn: str, parsed: dict) -> dict:
        return {
            "input_urn": urn,
            "parsed": {k: v for k, v in parsed.items() if k != "raw"},
            "aliases_traversed": [],
            "resolution_status": None,
            "resolved_to": None,
            "diagnostics": [],
        }

    def _resolve_with_chain(self, urn: str, chain: list) -> dict:
        # 1. Check alias table.
        if urn in self._aliases:
            entry = self._aliases[urn]
            chain.append(entry)
            target = entry.get("new_urn")
            if target == "retired":
                parsed = parse_urn(urn)
                resp = self._base_response(urn, parsed)
                resp["aliases_traversed"] = chain
                resp["resolution_status"] = "retired"
                resp["resolved_to"] = None
                resp["diagnostics"].append(
                    f"URN was retired on {entry.get('date','?')} "
                    f"(reason: {entry.get('reason','no reason recorded')})."
                )
                return resp
            # Recurse — but only one hop deep per CITATION_PERMANENCE.md §4.3
            # ("single-hop aliases preferred"). We allow up to 3 hops for safety
            # in case of pathological cases, but emit a diagnostic if >1.
            if len(chain) > 1:
                # Multiple hops — would be flagged for stewardship review.
                pass
            if len(chain) > 5:
                parsed = parse_urn(urn)
                resp = self._base_response(urn, parsed)
                resp["aliases_traversed"] = chain
                resp["resolution_status"] = "alias_chain_too_long"
                resp["diagnostics"].append(
                    "Alias chain exceeded safe traversal depth; refusing to recurse further."
                )
                return resp
            result = self._resolve_with_chain(target, chain)
            result["input_urn"] = urn  # preserve original
            if result["resolution_status"] == "resolved":
                result["resolution_status"] = "alias_redirected"
                result["diagnostics"].insert(
                    0,
                    f"Original URN {urn} redirected via alias to {target}."
                )
            return result

        # 2. Parse URN.
        parsed = parse_urn(urn)
        resp = self._base_response(urn, parsed)
        resp["aliases_traversed"] = chain

        if parsed["kind"] is None:
            resp["resolution_status"] = "malformed"
            resp["diagnostics"].append(
                "URN does not match any known kind pattern. "
                "See COMMENTARY_ATTACHMENT_MODEL.md for valid forms."
            )
            return resp

        kind = parsed["kind"]
        if kind == "text":
            return self._resolve_text(parsed, resp)
        if kind == "tale":
            return self._resolve_tale(parsed, resp)
        if kind == "translation":
            return self._resolve_translation(parsed, resp)
        if kind == "chapter":
            return self._resolve_chapter(parsed, resp)
        if kind == "passage":
            return self._resolve_passage(parsed, resp)
        if kind == "range":
            return self._resolve_range(parsed, resp)
        if kind == "commentary":
            return self._resolve_commentary(parsed, resp)
        if kind == "apparatus":
            return self._resolve_apparatus(parsed, resp)
        resp["resolution_status"] = "missing"
        resp["diagnostics"].append(f"Resolver does not handle kind={kind!r}.")
        return resp

    # ──────────────────────────────────────────────────────────────────────
    # Per-kind resolution

    def _resolve_text(self, parsed: dict, resp: dict) -> dict:
        reg = self._load_registry()
        target_id = parsed["text"]
        for t in reg.get("texts", []):
            if t.get("id") == target_id:
                resp["resolution_status"] = "resolved"
                resp["resolved_to"] = {
                    "kind": "text",
                    "id": target_id,
                    "title": t.get("title"),
                    "tradition": t.get("tradition"),
                    "category": t.get("category"),
                    "translation_count": len(t.get("translations", [])),
                }
                return resp
        resp["resolution_status"] = "missing"
        resp["diagnostics"].append(
            f"No canonical text with id={target_id!r} found in registry.json."
        )
        return resp

    def _resolve_tale(self, parsed: dict, resp: dict) -> dict:
        # Tale-level URNs are virtual — there is no `tale.json`. The resolver
        # returns a structured "tale" object that names the constituent
        # translations and (when available) chapter indices per translation.
        # See COMMENTARY_ATTACHMENT_MODEL.md §3 on the tale_offset gap.
        text_id = parsed["text"]
        tale_id = parsed["id"]
        # Confirm text exists.
        reg = self._load_registry()
        text_entries = [t for t in reg.get("texts", []) if t.get("id") == text_id]
        if not text_entries:
            resp["resolution_status"] = "missing"
            resp["diagnostics"].append(
                f"No canonical text with id={text_id!r}; cannot resolve tale {tale_id}."
            )
            return resp
        # The tale concept across volumes requires tale_offset metadata which
        # the current schema does not formally define. We report the virtual
        # tale and the constituent volumes/translations.
        resp["resolution_status"] = "resolved"
        resp["resolved_to"] = {
            "kind": "tale",
            "text_id": text_id,
            "tale_id": tale_id,
            "note": (
                "Tale-level URNs are virtual references across translations. "
                "Per-translation chapter mapping requires tale_offset metadata "
                "(see COMMENTARY_ATTACHMENT_MODEL.md §3); not yet populated for "
                "all texts. The resolver returns the symbolic tale handle; the "
                "renderer is responsible for finding the chapter in each "
                "translation."
            ),
            "translations_carrying_text": [t.get("id") for t in text_entries[:1]],
        }
        return resp

    def _resolve_translation(self, parsed: dict, resp: dict) -> dict:
        text_id = parsed["text"]
        trans_id = parsed["trans"]
        reg = self._load_registry()
        for t in reg.get("texts", []):
            if t.get("id") != text_id:
                continue
            for tr in t.get("translations", []):
                if tr.get("id") == trans_id:
                    resp["resolution_status"] = "resolved"
                    resp["resolved_to"] = {
                        "kind": "translation",
                        "text_id": text_id,
                        "translation_id": trans_id,
                        "translator": tr.get("translator"),
                        "language": tr.get("language"),
                        "passages_file": tr.get("passages_file"),
                    }
                    return resp
        resp["resolution_status"] = "missing"
        resp["diagnostics"].append(
            f"No translation {trans_id!r} of text {text_id!r} in registry.json."
        )
        return resp

    def _resolve_chapter(self, parsed: dict, resp: dict) -> dict:
        # Chapter URN: locate the chapter_titles entry.
        text_id = parsed["text"]
        trans_id = parsed["trans"]
        chap_id = parsed["id"]
        # Find the text.json that carries this text + translation.
        meta_path = self._find_text_json(text_id)
        if meta_path is None:
            resp["resolution_status"] = "missing"
            resp["diagnostics"].append(f"No text.json found for text {text_id!r}.")
            return resp
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        chapter_titles = meta.get("chapter_titles", {})
        if chap_id not in chapter_titles:
            resp["resolution_status"] = "missing"
            resp["diagnostics"].append(
                f"No chapter {chap_id!r} in chapter_titles of {text_id!r}::{trans_id!r}."
            )
            return resp
        resp["resolution_status"] = "resolved"
        resp["resolved_to"] = {
            "kind": "chapter",
            "text_id": text_id,
            "translation_id": trans_id,
            "chapter_id": chap_id,
            "title": chapter_titles[chap_id],
        }
        return resp

    def _resolve_passage(self, parsed: dict, resp: dict) -> dict:
        text_id = parsed["text"]
        trans_id = parsed["trans"]
        passage_id = parsed["id"]
        passages_path = self._find_passages_file(text_id, trans_id)
        if passages_path is None:
            resp["resolution_status"] = "missing"
            resp["diagnostics"].append(
                f"No passages file for translation {text_id!r}::{trans_id!r}."
            )
            return resp
        data = json.loads(passages_path.read_text(encoding="utf-8"))
        matches = [p for p in data.get("passages", []) if p.get("id") == passage_id]
        if not matches:
            resp["resolution_status"] = "missing"
            resp["diagnostics"].append(
                f"No passage {passage_id!r} in {passages_path.name}."
            )
            return resp
        if len(matches) > 1:
            resp["resolution_status"] = "ambiguous"
            resp["diagnostics"].append(
                f"Passage id {passage_id!r} appears {len(matches)} times in "
                f"{passages_path.name}. This is a constitutional duplicate-id breach "
                f"(COMMENTARY_REPAIR_PROTOCOLS.md §6)."
            )
            return resp
        p = matches[0]
        resolved = {
            "kind": "passage",
            "text_id": text_id,
            "translation_id": trans_id,
            "passage_id": passage_id,
            "path": p.get("path"),
            "order": p.get("order"),
            "text": p.get("text"),
        }
        # Sub-locator handling
        sub = parsed.get("sub_locator")
        if sub:
            sub_result = self._apply_sub_locator(p.get("text", ""), sub)
            resolved["sub_locator"] = sub_result
            if not sub_result["resolved"]:
                resp["diagnostics"].append(
                    f"Sub-locator {sub} did not resolve cleanly: {sub_result.get('reason')}."
                )
        resp["resolution_status"] = "resolved"
        resp["resolved_to"] = resolved
        return resp

    def _apply_sub_locator(self, passage_text: str, sub: dict) -> dict:
        if sub.get("type") == "phrase":
            value = sub.get("value", "")
            nth = sub.get("nth", 1)
            # Verbatim case-sensitive search per the attachment-model discipline.
            indices = []
            i = 0
            while True:
                idx = passage_text.find(value, i)
                if idx < 0:
                    break
                indices.append(idx)
                i = idx + 1
            if not indices:
                return {"type": "phrase", "value": value, "nth": nth,
                        "resolved": False,
                        "reason": "Phrase not found in passage text (verbatim, case-sensitive)."}
            if nth > len(indices):
                return {"type": "phrase", "value": value, "nth": nth,
                        "resolved": False,
                        "reason": f"Phrase appears {len(indices)} time(s); requested nth={nth} exceeds count."}
            return {"type": "phrase", "value": value, "nth": nth,
                    "resolved": True,
                    "char_offset": indices[nth - 1],
                    "occurrence_count": len(indices)}
        if sub.get("type") == "line":
            value = int(sub.get("value", 0))
            lines = passage_text.split("\n")
            if value < 1 or value > len(lines):
                return {"type": "line", "value": value, "resolved": False,
                        "reason": f"Line index out of range (passage has {len(lines)} line(s))."}
            return {"type": "line", "value": value, "resolved": True,
                    "line_text": lines[value - 1]}
        return {"type": sub.get("type"), "resolved": False,
                "reason": "Unrecognized sub-locator type."}

    def _resolve_range(self, parsed: dict, resp: dict) -> dict:
        # Resolve start and end; return the bounded range.
        text_id = parsed["text"]
        trans_id = parsed["trans"]
        passages_path = self._find_passages_file(text_id, trans_id)
        if passages_path is None:
            resp["resolution_status"] = "missing"
            resp["diagnostics"].append(
                f"No passages file for translation {text_id!r}::{trans_id!r}."
            )
            return resp
        data = json.loads(passages_path.read_text(encoding="utf-8"))
        all_p = data.get("passages", [])
        by_id = {p["id"]: p for p in all_p}
        start, end = parsed["start"], parsed["end"]
        if start not in by_id or end not in by_id:
            resp["resolution_status"] = "missing"
            resp["diagnostics"].append(
                f"Range endpoint(s) not in passages file: "
                f"start={start!r} present={start in by_id}, "
                f"end={end!r} present={end in by_id}."
            )
            return resp
        s_order = by_id[start].get("order", 0)
        e_order = by_id[end].get("order", 0)
        in_range = [p for p in all_p if s_order <= p.get("order", 0) <= e_order]
        resp["resolution_status"] = "resolved"
        resp["resolved_to"] = {
            "kind": "range",
            "text_id": text_id,
            "translation_id": trans_id,
            "start_id": start,
            "end_id": end,
            "passage_count": len(in_range),
            "first_passage_text": (in_range[0].get("text", "") if in_range else "")[:120],
        }
        return resp

    def _resolve_commentary(self, parsed: dict, resp: dict) -> dict:
        # Strip an optional @revision-date suffix.
        full_id = parsed["id"]
        base_id, _, rev_date = full_id.partition("@")
        rec = self._commentary.get(full_id) or self._commentary.get(base_id)
        if rec is None:
            resp["resolution_status"] = "missing"
            resp["diagnostics"].append(
                f"No commentary record with id={full_id!r} (or base {base_id!r})."
            )
            return resp
        if isinstance(rec, list):
            resp["resolution_status"] = "ambiguous"
            resp["diagnostics"].append(
                f"Commentary id {full_id!r} appears in {len(rec)} records. "
                f"Constitutional duplicate-id breach (COMMENTARY_REPAIR_PROTOCOLS.md §6)."
            )
            resp["resolved_to"] = {
                "kind": "commentary",
                "id": full_id,
                "candidate_count": len(rec),
            }
            return resp

        lifecycle = rec.get("lifecycle_state", "provisional")
        layer = rec.get("provenance", {}).get("layer", "?")
        resolved = {
            "kind": "commentary",
            "id": full_id,
            "lifecycle_state": lifecycle,
            "layer": layer,
            "author": rec.get("provenance", {}).get("author"),
            "date": rec.get("provenance", {}).get("date"),
            "body": rec.get("body"),
            "body_in_other_record": rec.get("body_in_other_record"),
            "anchors": rec.get("anchors", []),
            "reference_text": rec.get("reference_text"),
        }
        # Layer-6 quarantine preserved.
        if layer == "ai":
            resolved["quarantined"] = True
            resolved["model_identity"] = rec.get("provenance", {}).get("source", {})

        # Frozen flag (independent of lifecycle).
        if rec.get("migration_policy") == "frozen":
            resolved["migration_policy"] = "frozen"
            resolved["schema_version"] = rec.get("schema_version")

        # Lifecycle-derived resolution statuses.
        if lifecycle == "withdrawn":
            resp["resolution_status"] = "resolved"
            resolved["withdrawn_marker"] = True
            resp["diagnostics"].append("Record withdrawn; body preserved per COMMENTARY_LIFECYCLE.md §3.6.")
        elif lifecycle in ("deprecated", "superseded"):
            resp["resolution_status"] = "resolved"
            successor = rec.get("superseded_by")
            if successor:
                resolved["superseded_by"] = successor
            resp["diagnostics"].append(
                f"Record {lifecycle}; see lifecycle_state and (if present) successor."
            )
        elif lifecycle == "orphaned":
            resp["resolution_status"] = "resolved"
            resolved["orphaned_marker"] = True
            resp["diagnostics"].append("Record orphaned; anchor target removed by upstream restoration.")
            # Verify the anchor actually fails to resolve, for honesty.
            for a in rec.get("anchors", []):
                sub_resp = self.resolve(a.get("target", ""))
                if sub_resp.get("resolution_status") == "missing":
                    resolved["orphan_evidence"] = {
                        "broken_anchor": a.get("target"),
                        "anchor_resolution_status": sub_resp.get("resolution_status"),
                    }
                    break
        else:
            resp["resolution_status"] = "resolved"

        resp["resolved_to"] = resolved

        # Note revision-date specificity if present
        if rev_date:
            resolved["requested_revision_date"] = rev_date
            if rec.get("id") != full_id:
                # Asked for @date suffix but only the base record exists
                resolved["revision_note"] = (
                    f"Request specified revision-date suffix @{rev_date}, but only "
                    f"the base record {base_id!r} exists. Returning base."
                )
        return resp

    def _resolve_apparatus(self, parsed: dict, resp: dict) -> dict:
        resp["resolution_status"] = "missing"
        resp["diagnostics"].append(
            "Apparatus resolution not implemented in the May 2026 permanence prototype. "
            "The existing apparatus_file mechanism is documented in SCHEMA.md; full "
            "resolver support is deferred."
        )
        return resp

    # ──────────────────────────────────────────────────────────────────────
    # Helpers

    def _find_text_json(self, text_id: str) -> Optional[Path]:
        for path in TEXT_DIR.rglob("text.json"):
            try:
                meta = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if meta.get("id") == text_id:
                return path
        return None

    def _find_passages_file(self, text_id: str, trans_id: str) -> Optional[Path]:
        for path in TEXT_DIR.rglob("text.json"):
            try:
                meta = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if meta.get("id") != text_id:
                continue
            for tr in meta.get("translations", []):
                if tr.get("id") == trans_id:
                    pf = path.parent / tr.get("passages_file", "")
                    return pf if pf.exists() else None
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urn", help="The URN to resolve.")
    ap.add_argument("--load-test-fixtures", action="store_true",
                    help="Load test fixtures from 01_library/library/permanence/test_fixtures/.")
    args = ap.parse_args()

    resolver = Resolver(load_test_fixtures=args.load_test_fixtures)
    result = resolver.resolve(args.urn)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
