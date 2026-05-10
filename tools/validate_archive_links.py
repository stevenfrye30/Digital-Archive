#!/usr/bin/env python3
"""
validate_archive_links.py — Verify links between the Reading Room and the
canonical corpus.

The Reading Room (workspace-hub/archive/) is a hand-authored shelf that
soft-links to the canonical library through two channels:

  1. Each entry's YAML frontmatter may carry `library_id:` — a pointer to
     the canonical text id (registry.json).
  2. The shelf pages (index.md, shelves.md) and the entity router
     (entity.html?id=...) reach individual entries by their filename
     stem in archive/texts/.

This script verifies those pointers without modifying anything. It is
read-only diagnostic tooling, not a build step.

Usage:
    python 05_scripts/validate_archive_links.py
    python 05_scripts/validate_archive_links.py --out logs/reports/archive_link_audit.md

Exit code is 0 on a clean run, 1 if any broken references are found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READING_ROOM = ROOT.parent / "workspace-hub" / "archive"
TEXTS_DIR = READING_ROOM / "texts"
INDEX_MD = READING_ROOM / "index.md"
SHELVES_MD = READING_ROOM / "shelves.md"
REGISTRY = ROOT / "01_library" / "library" / "metadata" / "registry.json"

ENTITY_LINK_RE = re.compile(r"entity\.html\?id=([a-z0-9][a-z0-9-]*)")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def load_canonical_ids() -> set[str]:
    """Distinct text ids from the canonical registry."""
    if not REGISTRY.exists():
        return set()
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {t["id"] for t in reg.get("texts", [])}


def parse_frontmatter(md: str) -> dict:
    m = FRONTMATTER_RE.match(md)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)$", line)
        if mm:
            out[mm.group(1)] = mm.group(2).strip().strip('"').strip("'")
    return out


def collect_reading_room_entries() -> dict[str, dict]:
    """Map entry stem -> {fm, path}."""
    out = {}
    for p in sorted(TEXTS_DIR.glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        out[p.stem] = {"fm": parse_frontmatter(text), "path": p}
    return out


def collect_referenced_ids() -> dict[str, list[Path]]:
    """Every entity.html?id=... target referenced from index.md / shelves.md."""
    refs: dict[str, list[Path]] = {}
    for src in (INDEX_MD, SHELVES_MD):
        if not src.exists():
            continue
        for m in ENTITY_LINK_RE.finditer(src.read_text(encoding="utf-8")):
            refs.setdefault(m.group(1), []).append(src)
    return refs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="logs/reports/archive_link_audit.md",
                    help="Markdown report path (relative to Digital-Archive root)")
    args = ap.parse_args()

    canonical_ids = load_canonical_ids()
    entries = collect_reading_room_entries()
    referenced = collect_referenced_ids()

    # --- Check 1: library_id resolves to a canonical id (or is absent)
    bad_library_id = []
    missing_library_id = []
    for stem, info in entries.items():
        lid = info["fm"].get("library_id", "").strip()
        if not lid:
            missing_library_id.append(stem)
            continue
        if lid not in canonical_ids:
            bad_library_id.append((stem, lid))

    # --- Check 2: every entity.html?id=X reference points at an existing entry
    bad_links = []
    for ref_id, sources in sorted(referenced.items()):
        if ref_id not in entries:
            for s in sources:
                bad_links.append((ref_id, s.relative_to(READING_ROOM).as_posix()))

    # --- Check 3: entries listed on shelves but not on graph mapping
    # (informational, not an error)
    graph_map_path = READING_ROOM.parent / "graph" / "node_to_archive.json"
    graph_targets: set[str] = set()
    if graph_map_path.exists():
        m = json.loads(graph_map_path.read_text(encoding="utf-8"))
        graph_targets = {v for k, v in m.items()
                         if k != "_comment" and isinstance(v, str)}

    # --- Check 4: orphan entries (on disk, not referenced anywhere on a shelf
    # and not in graph map)
    shelf_entries = set(referenced.keys())
    orphans = sorted(set(entries) - shelf_entries - graph_targets)

    # --- Compose report
    lines: list[str] = []
    lines.append("# Archive link audit")
    lines.append("")
    lines.append("Read-only verification of Reading Room ↔ canonical links.")
    lines.append("Run with `python 05_scripts/validate_archive_links.py`.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Reading Room entries on disk: **{len(entries)}**")
    lines.append(f"- Entries with `library_id`: {len(entries) - len(missing_library_id)}")
    lines.append(f"- Entries referenced from `index.md` / `shelves.md`: {len(shelf_entries)}")
    lines.append(f"- Entries reachable from the graph map: {len(graph_targets & set(entries))}")
    lines.append(f"- Canonical ids in registry: {len(canonical_ids)}")
    lines.append("")
    lines.append("## Findings")
    lines.append("")

    def section(title: str, body_lines: list[str], empty_msg: str) -> None:
        lines.append(f"### {title}")
        lines.append("")
        if body_lines:
            lines.extend(body_lines)
        else:
            lines.append(f"*{empty_msg}*")
        lines.append("")

    section(
        f"Broken `library_id` pointers ({len(bad_library_id)})",
        [f"- `{stem}` → `library_id: {lid}` not in canonical registry"
         for stem, lid in sorted(bad_library_id)],
        "All `library_id` values resolve to a canonical text.",
    )

    section(
        f"Broken `entity.html?id=` references ({len(bad_links)})",
        [f"- `{rid}` referenced from `{src}` — no `texts/{rid}.md`"
         for rid, src in sorted(bad_links)],
        "Every shelf reference resolves to an existing entry.",
    )

    section(
        f"Entries without a `library_id` ({len(missing_library_id)})",
        [f"- `{stem}`" for stem in sorted(missing_library_id)],
        "Every entry carries a `library_id` pointer.",
    )

    section(
        f"Deep-archive entries (not on any shelf, not in graph map) "
        f"({len(orphans)})",
        # Soft-cap so the report stays readable; details belong elsewhere.
        ([f"- `{s}`" for s in orphans[:30]]
         + ([f"- *… and {len(orphans) - 30} more*"] if len(orphans) > 30 else [])),
        "Every entry is surfaced on a shelf or in the graph map.",
    )

    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report saved to {out_path.relative_to(ROOT)}")

    # Print a one-line summary to stdout
    errors = len(bad_library_id) + len(bad_links)
    print(f"  {len(entries)} entries · {errors} broken references · "
          f"{len(orphans)} deep-archive entries")

    return 1 if errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
