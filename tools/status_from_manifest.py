#!/usr/bin/env python3
"""Print (or write) STATUS.md's Canonical Library counts from the build
manifest (dataflow spec, lane 2: counts are derived, never authored).

  python tools/status_from_manifest.py           # print the three rows
  python tools/status_from_manifest.py --write   # rewrite them in STATUS.md

The values come from data/build_manifest.json — the deploy contract —
so a stale STATUS is fixed by rebuilding and re-running this, never by
typing numbers.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Windows consoles may be cp1252; the table rows carry ≠/— glyphs.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
STATUS = REPO / "STATUS.md"
MANIFEST = REPO / "data" / "build_manifest.json"

ROW_PATTERNS = {
    "entries": r"^(\|\s*Index entries[^|]*\|\s*)\**[\d,]+\**(\s*\|)",
    "public": r"^(\|\s*—? ?of which public[^|]*\|\s*)\**[\d,]+\**(\s*\|)",
    "restricted": r"^(\|\s*—? ?of which restricted[^|]*\|\s*)\**[\d,]+\**(\s*\|)",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true",
                    help="rewrite the three count rows in STATUS.md in place")
    a = ap.parse_args()

    if not MANIFEST.exists():
        sys.exit("no data/build_manifest.json — emit it first "
                 "(python 05_scripts/build_manifest.py)")
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    c = m["counts"]

    print(f"from build manifest of {m['generated']}:")
    print(f"| Index entries (web app reader) | **{c['entries']:,}** | "
          "`03_web_app/data/_generated/index.json` (entry count) |")
    print(f"| — of which public | **{c['public']:,}** | same (`restricted` ≠ true) |")
    print(f"| — of which restricted (locked, metadata-only) | **{c['restricted']:,}** | "
          "same (`restricted` = true) |")

    if not a.write:
        return 0

    text = STATUS.read_text(encoding="utf-8")
    changed = 0
    for key, pat in ROW_PATTERNS.items():
        new_text, n = re.subn(
            pat, lambda g: g.group(1) + f"**{c[key]:,}**" + g.group(2),
            text, count=1, flags=re.MULTILINE)
        if n != 1:
            sys.exit(f"could not find the '{key}' row in STATUS.md — "
                     "update ROW_PATTERNS if the table was reworded")
        if new_text != text:
            changed += 1
        text = new_text
    STATUS.write_text(text, encoding="utf-8")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"STATUS.md: {changed} row(s) updated from the manifest "
          f"({stamp}). Update the 'Last refreshed' line if the date moved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
