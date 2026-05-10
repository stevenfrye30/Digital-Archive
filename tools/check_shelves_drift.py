#!/usr/bin/env python3
"""
check_shelves_drift.py — Report drift between Reading Room entries on disk
and the curated `shelves.md` deeper-shelves listing.

Read-only. Does not modify shelves.md. The Reading Room is hand-authored;
this script tells the editor what is new or missing so they can decide
how to update the shelves with the same care as the rest of the page.

The script understands two structural realities:

  1. **Multi-chapter works.** Many entries share a `part_of` field
     (e.g. `dhammapada`, `upanishads`, `bhagavad-gita`). When the
     shelves page links *any* chapter of such a work, the whole work
     is considered "covered" — readers reach the rest by sequence
     inside the reader.
  2. **Standalone entries.** Entries with no `part_of` (or whose
     `part_of` is unique to them) appear on the shelves individually.

Usage:
    python 05_scripts/check_shelves_drift.py
    python 05_scripts/check_shelves_drift.py --print-candidate
        (Prints to stdout what a fully-auto-generated shelves.md would
         look like — for comparison only, not for piping into the file.)

Exit code is 0 if no drift, 1 if drift exists.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READING_ROOM = ROOT.parent / "workspace-hub" / "archive"
TEXTS_DIR = READING_ROOM / "texts"
SHELVES_MD = READING_ROOM / "shelves.md"

ENTITY_LINK_RE = re.compile(r"entity\.html\?id=([a-z0-9][a-z0-9-]*)")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)

# Tradition normalization. Some entries carry over-specified tradition
# strings (e.g., "Christian (Western mystical / apophatic)"); the
# shelves use a lighter set of buckets.
TRADITION_BUCKET = {
    "Christian (Western mystical / apophatic)": "Christian",
    "Greek Philosophy": "Greek",
    "Greek Epic":       "Greek",
    "Greek Tragedy":    "Greek",
    "Greek Lyric":      "Greek",
    "Roman Epic":       "Roman",
    "Islam":            "Islamic",
    "Daoist":           "Daoist",
    "Confucian":        "Confucian",
    "Stoic":            "Stoic",
    "Hindu":            "Hindu",
    "Buddhist":         "Buddhist",
    "Jewish":           "Jewish",
    "Egyptian":         "Egyptian",
    "Mesopotamian":     "Mesopotamian",
}

# Display order on the shelves page.
TRADITION_ORDER = [
    "Hindu", "Buddhist", "Jewish", "Christian", "Daoist",
    "Confucian", "Islamic", "Greek", "Roman", "Stoic",
    "Mesopotamian", "Egyptian",
]


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


def load_entries() -> dict[str, dict]:
    out = {}
    for p in sorted(TEXTS_DIR.glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        out[p.stem] = {
            "tradition_raw": fm.get("tradition", ""),
            "tradition":     TRADITION_BUCKET.get(fm.get("tradition", ""),
                                                  fm.get("tradition", "Other")),
            "part_of":       fm.get("part_of", ""),
            "title":         fm.get("title", ""),
            "summary":       fm.get("summary", ""),
        }
    return out


def load_shelf_links() -> set[str]:
    if not SHELVES_MD.exists():
        return set()
    return set(ENTITY_LINK_RE.findall(SHELVES_MD.read_text(encoding="utf-8")))


def covered_works(entries: dict, shelf_links: set[str]) -> set[str]:
    """Return the set of `part_of` values where any chapter is on shelves."""
    parts = {entries[s]["part_of"] for s in shelf_links if s in entries}
    parts.discard("")
    return parts


def check(entries: dict, shelf_links: set[str]) -> dict:
    covered = covered_works(entries, shelf_links)

    new_in_part: dict[str, list[str]] = defaultdict(list)
    new_standalone: dict[str, list[str]] = defaultdict(list)
    obsolete_links: list[str] = []

    for stem, info in entries.items():
        tradition = info["tradition"]
        part_of = info["part_of"]
        if part_of and part_of in covered:
            continue
        if stem in shelf_links:
            continue
        if part_of:
            new_in_part[(tradition, part_of)].append(stem)
        else:
            new_standalone[tradition].append(stem)

    for ref in shelf_links:
        if ref not in entries:
            obsolete_links.append(ref)

    return {
        "covered_works": sorted(covered),
        "new_in_part": dict(new_in_part),
        "new_standalone": dict(new_standalone),
        "obsolete_links": sorted(obsolete_links),
    }


def render_report(result: dict) -> str:
    lines: list[str] = []
    lines.append("# Shelves drift")
    lines.append("")
    lines.append("Read-only check between `workspace-hub/archive/texts/*.md` "
                 "and `shelves.md`.")
    lines.append("")

    new_in_part = result["new_in_part"]
    new_standalone = result["new_standalone"]
    obsolete = result["obsolete_links"]

    new_total = (sum(len(v) for v in new_in_part.values())
                 + sum(len(v) for v in new_standalone.values()))

    lines.append(f"- Multi-chapter works on shelves: {len(result['covered_works'])}")
    lines.append(f"- Entries on disk that the shelves do not yet cover: {new_total}")
    lines.append(f"- Shelf references to missing entries: {len(obsolete)}")
    lines.append("")

    if not new_total and not obsolete:
        lines.append("No drift. The shelves are in step with the texts on disk.")
        lines.append("")
        return "\n".join(lines)

    if obsolete:
        lines.append("## Shelf links pointing at missing entries")
        lines.append("")
        for ref in obsolete:
            lines.append(f"- `{ref}` referenced in shelves.md, no `texts/{ref}.md` exists.")
        lines.append("")

    if new_in_part:
        lines.append("## New chapters of works not yet on the shelves")
        lines.append("")
        lines.append("Each item below is a `part_of` group with at least "
                     "one chapter on disk that is not yet linked. Linking "
                     "any single chapter of the work counts as covering it.")
        lines.append("")
        by_trad: dict[str, list[tuple[str, list[str]]]] = defaultdict(list)
        for (trad, part), stems in new_in_part.items():
            by_trad[trad].append((part, stems))
        for trad in TRADITION_ORDER + sorted(set(by_trad) - set(TRADITION_ORDER)):
            if trad not in by_trad:
                continue
            lines.append(f"### {trad}")
            lines.append("")
            for part, stems in sorted(by_trad[trad]):
                lines.append(f"- `{part}` ({len(stems)} chapter(s) on disk, "
                             "none linked)")
            lines.append("")

    if new_standalone:
        lines.append("## New standalone entries not yet on the shelves")
        lines.append("")
        for trad in TRADITION_ORDER + sorted(set(new_standalone) - set(TRADITION_ORDER)):
            if trad not in new_standalone:
                continue
            lines.append(f"### {trad}")
            lines.append("")
            for stem in sorted(new_standalone[trad]):
                lines.append(f"- `{stem}`")
            lines.append("")

    return "\n".join(lines)


def render_candidate_shelves(entries: dict) -> str:
    """Print what a mechanically-grouped shelves.md would look like.

    The real shelves.md is hand-authored. This is a rough comparator,
    never meant to be piped over the curated file.
    """
    by_trad: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for stem, info in entries.items():
        trad = info["tradition"] or "Other"
        part = info["part_of"] or stem
        by_trad[trad][part].append(stem)

    out = []
    out.append("# (auto-grouped candidate — not for direct use)")
    out.append("")
    out.append("Auto-grouped listing for visual comparison only.")
    out.append("")
    for trad in TRADITION_ORDER + sorted(set(by_trad) - set(TRADITION_ORDER)):
        if trad not in by_trad:
            continue
        out.append(f"## {trad}")
        out.append("")
        for part, stems in sorted(by_trad[trad].items()):
            stems = sorted(stems)
            first = stems[0]
            label = entries[first]["title"] or first
            count_note = f" — {len(stems)} chapter(s)" if len(stems) > 1 else ""
            out.append(f"- [{label}](entity.html?id={first}){count_note}")
        out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="logs/reports/shelves_drift.md",
                    help="Drift report path (relative to Digital-Archive root)")
    ap.add_argument("--print-candidate", action="store_true",
                    help="Print mechanical candidate to stdout (does NOT touch shelves.md)")
    args = ap.parse_args()

    entries = load_entries()
    shelf_links = load_shelf_links()
    result = check(entries, shelf_links)

    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_report(result) + "\n", encoding="utf-8")
    print(f"Drift report saved to {out_path.relative_to(ROOT)}")

    new_total = (sum(len(v) for v in result["new_in_part"].values())
                 + sum(len(v) for v in result["new_standalone"].values()))
    print(f"  {len(entries)} entries · "
          f"{len(result['covered_works'])} works covered · "
          f"{new_total} not yet covered · "
          f"{len(result['obsolete_links'])} broken shelf links")

    if args.print_candidate:
        print()
        print(render_candidate_shelves(entries))

    drift = new_total + len(result["obsolete_links"])
    return 1 if drift > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
