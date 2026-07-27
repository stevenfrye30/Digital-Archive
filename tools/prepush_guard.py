#!/usr/bin/env python3
"""Pre-push guard for the public reader repo.

Blocks a push when the force-tracked reader index disagrees with the
counts declared in STATUS.md, or when any restricted entry's data file
is tracked by git. START_HERE.md (parent archive) documents this as the
pre-push invariant; STATUS.md is the truth surface the expected numbers
are read from, so a legitimate corpus change is made pushable by
refreshing STATUS.md — never by editing this script.

Install with: python tools/install_hooks.py
Run manually: python tools/prepush_guard.py
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STATUS = REPO / "STATUS.md"
INDEX = REPO / "data" / "index.json"

STATUS_ROWS = {
    "total": r"^\|\s*Index entries[^|]*\|\s*\**([\d,]+)\**\s*\|",
    "public": r"^\|\s*—? ?of which public[^|]*\|\s*\**([\d,]+)\**\s*\|",
    "restricted": r"^\|\s*—? ?of which restricted[^|]*\|\s*\**([\d,]+)\**\s*\|",
}


def fail(msg):
    sys.stderr.write("\npre-push guard: PUSH BLOCKED\n" + msg + "\n")
    sys.exit(1)


def expected_counts():
    if not STATUS.exists():
        fail("STATUS.md not found beside the reader — the guard cannot "
             "verify the index without its truth surface.")
    text = STATUS.read_text(encoding="utf-8")
    counts = {}
    for key, pattern in STATUS_ROWS.items():
        m = re.search(pattern, text, re.MULTILINE)
        if not m:
            fail(f"Could not find the '{key}' row in STATUS.md's Canonical "
                 "Library table. If the table was reworded, update "
                 "STATUS_ROWS in tools/prepush_guard.py to match.")
        counts[key] = int(m.group(1).replace(",", ""))
    return counts


def actual_counts():
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    texts = idx["texts"] if isinstance(idx, dict) and "texts" in idx else idx
    restricted = [t for t in texts if t.get("restricted") is True]
    return {
        "total": len(texts),
        "public": len(texts) - len(restricted),
        "restricted": len(restricted),
    }, restricted


def tracked_restricted_files(restricted):
    out = subprocess.run(
        ["git", "ls-files", "data/"],
        capture_output=True, text=True, cwd=REPO, check=True,
    ).stdout.splitlines()
    tracked = set(out)
    leaks = []
    for t in restricted:
        df = t.get("data_file")
        if not df:
            continue
        for candidate in (f"data/{df}", f"data/{df}.gz"):
            if candidate in tracked:
                leaks.append(candidate)
    return leaks


def main():
    expected = expected_counts()
    actual, restricted = actual_counts()

    if expected != actual:
        fail(
            "data/index.json disagrees with STATUS.md.\n"
            f"  STATUS.md declares : {expected['total']} = "
            f"{expected['public']} public + {expected['restricted']} restricted\n"
            f"  index.json contains: {actual['total']} = "
            f"{actual['public']} public + {actual['restricted']} restricted\n"
            "If the corpus legitimately changed, refresh the Canonical\n"
            "Library counts in STATUS.md (with the export lane's numbers)\n"
            "and try again. If it did not, the index is drifted — stop and\n"
            "investigate before pushing."
        )

    leaks = tracked_restricted_files(restricted)
    if leaks:
        fail(
            "Restricted entries have tracked data files (bodies must never "
            "deploy):\n  " + "\n  ".join(leaks) +
            "\nUntrack them (git rm --cached <file>) and confirm they are "
            "gitignored."
        )

    print(f"pre-push guard: OK — {actual['total']} = {actual['public']} "
          f"public + {actual['restricted']} restricted; "
          "no restricted data files tracked.")


if __name__ == "__main__":
    main()
