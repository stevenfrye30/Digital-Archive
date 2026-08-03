#!/usr/bin/env python3
"""Pre-push guard v2 for the public reader repo (dataflow spec, lane 2).

Every invariant is DERIVED from data/build_manifest.json — the deploy
contract written by the build (05_scripts/build_manifest.py). Nothing
here is remembered or hand-counted:

  1. counts       manifest counts == counts recomputed from index.json
  2. STATUS       STATUS.md's Canonical Library counts == manifest counts
                  (refresh with: python tools/status_from_manifest.py --write)
  3. reasons      every restricted entry carries a restricted_reason
                  from the enum
  4. boundary     no restricted entry ships a tracked data file
                  (.json or .json.gz)
  5. integrity    every manifest data_file exists on disk and its
                  sha256 matches data_hash; no index row lacks a
                  manifest entry and no manifest entry is an orphan

A legitimate corpus change is made pushable by rebuilding the deploy
(which rewrites the manifest) and refreshing STATUS from it — never by
editing this script.

Install with: python tools/install_hooks.py
Run manually: python tools/prepush_guard.py [--fast]   (--fast skips 5's hashing)
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

# Windows consoles may be cp1252; messages carry — glyphs.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
STATUS = REPO / "STATUS.md"
INDEX = REPO / "data" / "_generated" / "index.json"
MANIFEST = REPO / "data" / "build_manifest.json"

REASON_ENUM = {"copyrighted", "uncertain-copyright", "integrity-wishlist",
               "steward-hold"}

STATUS_ROWS = {
    "entries": r"^\|\s*Index entries[^|]*\|\s*\**([\d,]+)\**\s*\|",
    "public": r"^\|\s*—? ?of which public[^|]*\|\s*\**([\d,]+)\**\s*\|",
    "restricted": r"^\|\s*—? ?of which restricted[^|]*\|\s*\**([\d,]+)\**\s*\|",
}


def fail(msg):
    sys.stderr.write("\npre-push guard v2: PUSH BLOCKED\n" + msg + "\n")
    sys.exit(1)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def status_counts():
    if not STATUS.exists():
        fail("STATUS.md not found beside the reader.")
    text = STATUS.read_text(encoding="utf-8")
    out = {}
    for key, pattern in STATUS_ROWS.items():
        m = re.search(pattern, text, re.MULTILINE)
        if not m:
            fail(f"Could not find the '{key}' row in STATUS.md's Canonical "
                 "Library table; update STATUS_ROWS here if it was reworded.")
        out[key] = int(m.group(1).replace(",", ""))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true",
                    help="skip full data_hash verification (counts/boundary only)")
    a = ap.parse_args()

    if not MANIFEST.exists():
        fail("data/build_manifest.json is missing — the deploy has no "
             "contract. Emit it with: python 05_scripts/build_manifest.py "
             "(or run the full build).")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    mtexts = manifest["texts"]

    # 1 — manifest counts vs index reality
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    rows = idx["texts"] if isinstance(idx, dict) and "texts" in idx else idx
    n_restricted = sum(1 for t in rows if t.get("restricted") is True)
    actual = {"entries": len(rows), "public": len(rows) - n_restricted,
              "restricted": n_restricted}
    if manifest["counts"] != actual:
        fail("data/_generated/index.json disagrees with the build manifest.\n"
             f"  manifest : {manifest['counts']}\n"
             f"  index    : {actual}\n"
             "The index changed without a manifest rewrite (or vice versa). "
             "Rebuild, or investigate the drift before pushing.")

    # 2 — STATUS is printed output, and must match
    sc = status_counts()
    if sc != actual:
        fail("STATUS.md's Canonical Library counts are stale.\n"
             f"  STATUS   : {sc}\n"
             f"  manifest : {actual}\n"
             "Refresh with: python tools/status_from_manifest.py --write")

    # 3 + 4 — restricted reasons and the no-body boundary
    tracked = set(subprocess.run(
        ["git", "ls-files", "data/"],
        capture_output=True, text=True, cwd=REPO, check=True,
    ).stdout.splitlines())
    missing_reason, leaks = [], []
    for key, e in mtexts.items():
        if not e.get("restricted"):
            continue
        if e.get("restricted_reason") not in REASON_ENUM:
            missing_reason.append(key)
        df = e.get("data_file")
        if df:
            stem = df[:-3] if df.endswith(".gz") else df
            for cand in (f"data/{stem}", f"data/{stem}.gz"):
                if cand in tracked:
                    leaks.append(cand)
    if missing_reason:
        fail("Restricted entries without a valid restricted_reason:\n  "
             + "\n  ".join(missing_reason[:20]))
    if leaks:
        fail("Restricted entries have TRACKED data files (bodies must "
             "never deploy):\n  " + "\n  ".join(leaks)
             + "\nUntrack them (git rm --cached <file>) and confirm they "
               "are gitignored.")

    # 5 — correspondence + integrity
    idx_dfs = {t["data_file"] for t in rows if t.get("data_file")}
    man_dfs = set()
    for e in mtexts.values():
        df = e.get("data_file")
        if df:
            man_dfs.add(df[:-3] if df.endswith(".gz") else df)
    if idx_dfs - man_dfs:
        fail("Index rows with no manifest entry:\n  "
             + "\n  ".join(sorted(idx_dfs - man_dfs)[:20]))
    if man_dfs - idx_dfs:
        fail("Manifest entries no index row references:\n  "
             + "\n  ".join(sorted(man_dfs - idx_dfs)[:20]))

    hashed = 0
    if not a.fast:
        t0 = time.time()
        bad, gone = [], []
        for key, e in mtexts.items():
            # A split row ships its head under `data_file` and the
            # remainder under `parts`. Both are artifacts this deploy
            # serves, so BOTH are hashed — the invariant is unchanged in
            # meaning (every artifact the manifest declares exists and
            # matches), it simply now sees all of them. Rows without
            # `parts` behave exactly as before.
            declared = [(e.get("data_file"), e.get("data_hash"))]
            for part in (e.get("parts") or []):
                declared.append((part.get("data_file"), part.get("data_hash")))
            for df, want in declared:
                if not df or not want:
                    continue
                p = REPO / "data" / df
                if not p.exists():
                    gone.append(df)
                elif sha256_file(p) != want:
                    bad.append(df)
                hashed += 1
        if gone:
            fail("Manifest data files missing on disk:\n  "
                 + "\n  ".join(gone[:20]))
        if bad:
            fail("Data files whose sha256 no longer matches the manifest "
                 "(edited or corrupted after the build):\n  "
                 + "\n  ".join(bad[:20])
                 + "\nRebuild the deploy so the manifest and the files agree.")
        elapsed = f"{time.time() - t0:.1f}s"
    else:
        elapsed = "skipped (--fast)"

    # 6b. orphan bodies (Task 100, 2026-08-01): a body in data/ that no
    #     index row names is a text the archive retired but whose artifact
    #     was never swept. Fifty of them had accumulated; two were tracked,
    #     so the site served withdrawn Bible bodies at unlisted URLs. The
    #     guard could not see them because checks 1-5 compare the manifest
    #     with the index and never look at the directory itself.
    SITE_ARTIFACTS = {
        "build_manifest.json", "finalized.json", "integrity.json",
        "search_index.json", "source_manifest.json", "index.json",
        "restricted_sources_register.json", "chip_index.json", "read_marks.json",
    }
    # A split row's `rest` artifact is named by the MANIFEST rather than by
    # an index row, so it must be recognised here or it reads as a retired
    # body. Derived from the contract itself — the set of declared parts —
    # never from a filename suffix: a suffix rule would bless any file
    # somebody named `.rest.json.gz`, which is exactly the hole 6b exists
    # to close. A part declared by no row is still an orphan.
    declared_parts = {
        part.get("data_file")
        for e in mtexts.values() for part in (e.get("parts") or [])
        if part.get("data_file")
    }
    orphans = sorted(
        p.name for p in (REPO / "data").glob("*.json.gz")
        if p.name[:-3] not in idx_dfs
        and p.name[:-3] not in SITE_ARTIFACTS
        and p.name not in declared_parts
    )
    if orphans:
        fail("Bodies in data/ that no index row names (retired texts whose "
             "artifacts were never swept — they would deploy unreachable):\n  "
             + "\n  ".join(orphans[:20])
             + "\nRemove them from data/ (the sources stay in 01_library).")

    # 6. reachability (Task 27 closer, 2026-07-29): every public row must be
    #    reachable from a structural surface (map binding or room listing) or
    #    be a recorded decision in tools/reachability_ledger.json. Fails on
    #    silent growth of the reader-only set; shrinkage never fails.
    import check_reachability
    reach = check_reachability.problems()
    if reach:
        fail("Reachability check (6) failed:\n  " + "\n  ".join(reach[:10]))

    print(f"pre-push guard v2: OK — {actual['entries']} = {actual['public']} "
          f"public + {actual['restricted']} restricted; reasons complete; "
          f"boundary clean; {hashed} artifact hashes verified; "
          f"reachability OK ({elapsed}).")


if __name__ == "__main__":
    main()
