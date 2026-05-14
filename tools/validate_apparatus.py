#!/usr/bin/env python3
"""validate_apparatus.py — Apparatus propagation integrity check.

Lightweight, read-only health check for the apparatus pipeline.
Validates the constitutional commitment that the deploy faithfully
represents the canonical archive's apparatus state.

Three classes of finding:

  1. Propagation breach — canonical apparatus exists for a translation
     but the deploy does not carry the apparatus arrays.
  2. Orphan markers — a deploy file carries [*N] markers in passage
     text but no canonical apparatus was ever extracted for that
     translation. (Not a propagation bug; an unrestored gap.)
  3. Anchor inconsistency — canonical apparatus carries an anchor for
     a passage that no longer exists in the passages file, or a
     passage's page boundary is missing.

Writes:

  logs/reports/apparatus_audit.md  (human-readable)
  logs/reports/apparatus_audit.json (machine-readable)

Usage:
    python 05_scripts/validate_apparatus.py
"""
from __future__ import annotations

import gzip
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXTS_DIR = ROOT / "01_library" / "library" / "texts"
DATA_DIR = ROOT / "03_web_app" / "data"
REPORT_MD = ROOT / "logs" / "reports" / "apparatus_audit.md"
REPORT_JSON = ROOT / "logs" / "reports" / "apparatus_audit.json"

MARKER_RE = re.compile(r"\[\*(\d+)\]")


def find_canonical_apparatus() -> dict:
    """Return {(text_id, translation_id): path} for every canonical apparatus file."""
    found = {}
    for path in TEXTS_DIR.rglob("apparatus_*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        key = (data.get("text_id"), data.get("translation_id"))
        if all(key):
            found[key] = path
    return found


def load_deploy(file_path: Path) -> dict | None:
    try:
        if file_path.suffix == ".gz":
            with gzip.open(file_path, "rt", encoding="utf-8") as f:
                return json.load(f)
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def inspect_deploy(deploy: dict) -> dict:
    """Return marker stats and apparatus-presence flags."""
    passages = deploy.get("passages", []) or []
    marker_count = 0
    marker_passages = 0
    sample_passages = []
    for p in passages:
        text = p.get("text", "") or ""
        ms = MARKER_RE.findall(text)
        if ms:
            marker_count += len(ms)
            marker_passages += 1
            if len(sample_passages) < 3:
                sample_passages.append({"id": p.get("id"), "indices": ms[:5]})
    has_apparatus = bool(deploy.get("apparatus"))
    has_boundaries = bool(deploy.get("apparatus_page_boundaries"))
    return {
        "marker_count": marker_count,
        "marker_passage_count": marker_passages,
        "has_apparatus_array": has_apparatus,
        "has_page_boundaries": has_boundaries,
        "sample_marker_passages": sample_passages,
    }


def find_deploy_for(text_id: str, translation_id: str) -> Path | None:
    candidate = DATA_DIR / f"{text_id}_{translation_id}.json"
    if candidate.exists():
        return candidate
    candidate_gz = DATA_DIR / f"{text_id}_{translation_id}.json.gz"
    if candidate_gz.exists():
        return candidate_gz
    return None


def check_anchor_integrity(canonical: dict, passage_ids: set[str]) -> list[str]:
    """Find anchors in canonical apparatus that no longer resolve."""
    problems = []
    for entry in canonical.get("apparatus", []):
        for a in entry.get("anchors") or []:
            pid = a.get("passage_id")
            if pid and pid not in passage_ids:
                problems.append(
                    f"apparatus id={entry.get('id')} anchor passage_id={pid!r} not in passages file"
                )
    # Check page boundaries reference real passages too.
    for pb in canonical.get("page_boundaries", []):
        for pid in pb.get("passages", []):
            if pid not in passage_ids:
                problems.append(
                    f"page_boundary page={pb.get('page')} references unknown passage_id={pid!r}"
                )
    return problems


def main() -> int:
    canonical = find_canonical_apparatus()

    propagation_breaches = []
    propagation_ok = []
    anchor_problems = []

    for (text_id, tr_id), can_path in sorted(canonical.items()):
        deploy_path = find_deploy_for(text_id, tr_id)
        if deploy_path is None:
            propagation_breaches.append({
                "text_id": text_id,
                "translation_id": tr_id,
                "kind": "missing_deploy_file",
                "canonical_path": str(can_path.relative_to(ROOT)).replace("\\", "/"),
            })
            continue
        deploy = load_deploy(deploy_path) or {}
        stats = inspect_deploy(deploy)
        if not stats["has_apparatus_array"]:
            propagation_breaches.append({
                "text_id": text_id,
                "translation_id": tr_id,
                "kind": "apparatus_dropped",
                "canonical_path": str(can_path.relative_to(ROOT)).replace("\\", "/"),
                "deploy_path": str(deploy_path.relative_to(ROOT)).replace("\\", "/"),
                "deploy_marker_count": stats["marker_count"],
            })
        else:
            propagation_ok.append({
                "text_id": text_id,
                "translation_id": tr_id,
                "deploy_marker_count": stats["marker_count"],
                "deploy_apparatus_entries": len(deploy.get("apparatus", [])),
            })
        # Anchor integrity within the canonical apparatus
        passages_path = can_path.parent / f"passages_{tr_id}.json"
        if passages_path.exists():
            try:
                pd = json.loads(passages_path.read_text(encoding="utf-8"))
                pids = {p["id"] for p in pd.get("passages", []) if "id" in p}
                can_data = json.loads(can_path.read_text(encoding="utf-8"))
                problems = check_anchor_integrity(can_data, pids)
                if problems:
                    anchor_problems.append({
                        "text_id": text_id,
                        "translation_id": tr_id,
                        "problems": problems[:10],
                        "problem_count": len(problems),
                    })
            except Exception:
                pass

    # Orphan-marker scan: deploys with [*N] markers but no canonical apparatus.
    orphan_markers = []
    canonical_keys = set(canonical.keys())
    for deploy_path in sorted(DATA_DIR.glob("*.json")):
        # Skip non-text deploy files
        if deploy_path.name in ("index.json", "integrity.json", "source_manifest.json", "search_index.json"):
            continue
        deploy = load_deploy(deploy_path)
        if not deploy or "passages" not in deploy:
            continue
        text_id = deploy.get("id")
        tr_id = deploy.get("translation", {}).get("id")
        if not (text_id and tr_id):
            continue
        key = (text_id, tr_id)
        if key in canonical_keys:
            continue  # Handled above
        stats = inspect_deploy(deploy)
        if stats["marker_count"] > 0:
            orphan_markers.append({
                "text_id": text_id,
                "translation_id": tr_id,
                "deploy_file": deploy_path.name,
                "marker_count": stats["marker_count"],
                "marker_passage_count": stats["marker_passage_count"],
                "sample": stats["sample_marker_passages"],
            })

    summary = {
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "canonical_apparatus_count": len(canonical),
        "propagation_ok_count": len(propagation_ok),
        "propagation_breach_count": len(propagation_breaches),
        "orphan_marker_text_count": len(orphan_markers),
        "anchor_problem_text_count": len(anchor_problems),
        "propagation_ok": propagation_ok,
        "propagation_breaches": propagation_breaches,
        "orphan_markers": orphan_markers,
        "anchor_problems": anchor_problems,
    }

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(_render_markdown(summary), encoding="utf-8")

    print(f"Wrote {REPORT_JSON.relative_to(ROOT)}")
    print(f"Wrote {REPORT_MD.relative_to(ROOT)}")
    print(
        f"Apparatus status: "
        f"{summary['propagation_ok_count']} ok, "
        f"{summary['propagation_breach_count']} propagation breaches, "
        f"{summary['orphan_marker_text_count']} texts with orphan markers, "
        f"{summary['anchor_problem_text_count']} with anchor integrity problems."
    )
    # Return non-zero only on propagation breaches; orphan markers are
    # a long-term restoration backlog, not a pipeline failure.
    return 1 if summary["propagation_breach_count"] > 0 else 0


def _render_markdown(s: dict) -> str:
    lines: list[str] = []
    lines.append("# Apparatus Propagation Audit")
    lines.append("")
    lines.append(f"Run at: `{s['run_at']}`")
    lines.append("")
    lines.append("This audit verifies that the deploy faithfully represents")
    lines.append("the canonical archive's apparatus state. See")
    lines.append("`APPARATUS_PROPAGATION_REPAIR_2026.md` for the constitutional rationale.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Canonical apparatus files: **{s['canonical_apparatus_count']}**")
    lines.append(f"- Propagated correctly: **{s['propagation_ok_count']}**")
    lines.append(f"- Propagation breaches: **{s['propagation_breach_count']}**")
    lines.append(f"- Deploys with orphan `[*N]` markers (no canonical apparatus): **{s['orphan_marker_text_count']}**")
    lines.append(f"- Canonical apparatus with anchor problems: **{s['anchor_problem_text_count']}**")
    lines.append("")

    if s["propagation_breaches"]:
        lines.append("## Propagation breaches (pipeline bugs)")
        lines.append("")
        lines.append("Canonical apparatus exists; the deploy does not carry it. This is the")
        lines.append("constitutional fail-honestly violation the repair targets.")
        lines.append("")
        for b in s["propagation_breaches"]:
            lines.append(
                f"- `{b['text_id']}::{b['translation_id']}` — {b['kind']} "
                f"(canonical: `{b.get('canonical_path','?')}`)"
            )
        lines.append("")

    if s["propagation_ok"]:
        lines.append("## Propagated correctly")
        lines.append("")
        for o in s["propagation_ok"]:
            lines.append(
                f"- `{o['text_id']}::{o['translation_id']}` — "
                f"{o['deploy_apparatus_entries']} apparatus entries, "
                f"{o['deploy_marker_count']} markers in passages"
            )
        lines.append("")

    if s["anchor_problems"]:
        lines.append("## Canonical anchor integrity problems")
        lines.append("")
        for a in s["anchor_problems"]:
            lines.append(f"- `{a['text_id']}::{a['translation_id']}` — {a['problem_count']} problem(s)")
            for prob in a["problems"][:5]:
                lines.append(f"  - {prob}")
        lines.append("")

    if s["orphan_markers"]:
        lines.append("## Orphan markers (canonical apparatus not yet extracted)")
        lines.append("")
        lines.append("Deploys whose passages carry `[*N]` markers verbatim from the raw witness")
        lines.append("but whose canonical apparatus has not yet been recovered. These are not")
        lines.append("propagation bugs; they are a long-term restoration backlog. The reader")
        lines.append("surfaces an honest-gap diagnostic on click.")
        lines.append("")
        total = sum(o["marker_count"] for o in s["orphan_markers"])
        lines.append(f"Total orphan markers across all deploys: **{total}**.")
        lines.append("")
        lines.append("| Deploy | Markers | Passages |")
        lines.append("|---|---:|---:|")
        for o in sorted(s["orphan_markers"], key=lambda x: -x["marker_count"])[:40]:
            lines.append(
                f"| `{o['deploy_file']}` | {o['marker_count']} | {o['marker_passage_count']} |"
            )
        if len(s["orphan_markers"]) > 40:
            lines.append(f"| _… and {len(s['orphan_markers'])-40} more_ |  |  |")
        lines.append("")

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
