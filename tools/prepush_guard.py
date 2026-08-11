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

    # 6b-maps. stray build inputs in a SERVED directory (Task 137,
    #     2026-08-03). seed_bindings.json — a pure build input, generated by
    #     map_draft_seeds.py and read by build_map_bindings.py — was tracked
    #     under maps/, so 1,131 KB of scaffolding shipped to Pages at a public
    #     URL for as long as the map program has existed. Nothing fetched it;
    #     nothing complained. The data/ half of 6b could not see it, because it
    #     only ever looked at data/.
    #
    #     The served set is DERIVED, never enumerated (8.1e): read the pages and
    #     take the maps/ filenames they actually fetch. A file becomes
    #     legitimate the moment code asks for it, so this never needs editing
    #     when a room gains an artifact. Matching is on the FULL BASENAME, not a
    #     suffix — the same reasoning the data/ half gives above for refusing to
    #     bless anything ending `.rest.json.gz`.
    served_names = set()
    for src in [REPO / "index.html", *sorted((REPO / "map").glob("*.html")),
                *sorted((REPO / "map").glob("*.js")),
                *sorted((REPO / "hall").glob("*.html"))]:
        if src.exists():
            served_names |= set(re.findall(
                # The room artifacts are fetched as `maps/' + SLUG + '/bindings
                # .json'` — the directory is BUILT AT RUNTIME, so the pattern
                # has to tolerate a concatenation expression between the two
                # slashes. A first cut that assumed a literal path derived a
                # served set with no bindings.json in it and duly reported the
                # sixteen most-fetched files in the archive as strays.
                r"maps/(?:[A-Za-z0-9_.\-/'\"+ ]*/)?([A-Za-z0-9_.-]+\.json)",
                src.read_text(encoding="utf-8", errors="replace")))
    if not served_names:
        fail("6b-maps derived an EMPTY served set — the scan found no maps/ "
             "fetches at all. A guard that blesses everything because it looked "
             "at nothing is the failure mode 8.1b names; refusing instead.")

    ledger_path = REPO / "tools" / "maps_served_ledger.json"
    recorded = set()
    if ledger_path.exists():
        recorded = set(json.loads(ledger_path.read_text(encoding="utf-8"))
                       .get("recorded", {}))
    tracked_maps = subprocess.run(
        ["git", "ls-files", "maps/"], cwd=REPO,
        capture_output=True, text=True,
                             encoding="utf-8", errors="replace").stdout.split()
    map_strays = sorted(
        p for p in tracked_maps
        if p.rsplit("/", 1)[-1] not in served_names and p not in recorded
    )
    if map_strays:
        kb = sum((REPO / p).stat().st_size for p in map_strays) / 1024
        fail("Tracked files under maps/ that no page fetches (%.0f KB of build "
             "input that would ship to Pages at a public URL):\n  " % kb
             + "\n  ".join(map_strays[:20])
             + "\nMove them out of the published tree (05_scripts/configs/ is "
               "where seed_bindings.json went in Task 137), or record each one "
               "with its reason in tools/maps_served_ledger.json.")

    # 6. reachability (Task 27 closer, 2026-07-29): every public row must be
    #    reachable from a structural surface (map binding or room listing) or
    #    be a recorded decision in tools/reachability_ledger.json. Fails on
    #    silent growth of the reader-only set; shrinkage never fails.
    import check_reachability
    reach = check_reachability.problems()
    if reach:
        fail("Reachability check (6) failed:\n  " + "\n  ".join(reach[:10]))

    # 7. private/public lane separation (Task 156). The fail-closed separation
    #    guard lives in the parent tree, and until now its ONLY caller was
    #    05_scripts/check_restricted_invariants.py — which had been dying on a
    #    moved index path since July, so the check had not run on a push in
    #    months and nothing said so. A guard nobody calls is not a guard.
    #    It belongs here, on the path every push actually takes.
    sep_state = "SKIPPED (no parent tree)"
    sep_script = REPO.parent / "05_scripts" / "check_public_private_separation.py"
    if sep_script.exists():
        sep = subprocess.run([sys.executable, str(sep_script)],
                             capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        if sep.returncode != 0:
            tail = (sep.stdout or sep.stderr or "").strip().splitlines()
            fail("Private/public separation (7) FAILED — a local-only record or "
                 "body would ship:\n  " + "\n  ".join(tail[-6:]))
        sep_state = (sep.stdout or "").strip().splitlines()[-1] if sep.stdout else "OK"
    elif (REPO.parent / "_private_library").exists():
        # The private lane exists but its guard does not: refuse rather than
        # report a separation nobody verified.
        fail("Private/public separation (7) could not run: _private_library/ "
             "is present but 05_scripts/check_public_private_separation.py is "
             "missing. Refusing to push an unverified boundary.")

    # 8. the finalization ledger is DERIVED, not asserted (2026-08-08). The
    #    ledger drifted from its reports for months because it was
    #    transcribed by hand: 68 entries against 147 reports, 86 of which no
    #    entry cited. It is now generated from a fenced `finalization` block
    #    in each report, and this check refuses on a malformed block OR on a
    #    STALE ledger — a file that quietly says something the reports do not
    #    is exactly the failure the convention was written to end. Reports
    #    without a block are reported as unmigrated, not as failures; the
    #    backlog is expected to shrink, not to block a deploy.
    fin_state = "SKIPPED (no parent tree)"
    fin_script = REPO.parent / "05_scripts" / "generate_finalization_ledger.py"
    if fin_script.exists():
        fin = subprocess.run([sys.executable, str(fin_script)],
                             capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        if fin.returncode != 0:
            # The reason is the REFUSED line, which arrives on stderr; stdout
            # is the (non-empty) progress report. Taking `stdout or stderr`
            # would therefore print the summary and hide the cause.
            lines = ((fin.stderr or "") + "\n" + (fin.stdout or "")).splitlines()
            why = [l.strip() for l in lines if "REFUSED" in l] \
                or [l.strip() for l in lines if l.strip()][-4:]
            fail("Finalization ledger (8) FAILED — a report's finalization "
                 "block is malformed, or the ledger no longer matches what "
                 "the reports say:\n  " + "\n  ".join(why[:4]))
        line = [l for l in (fin.stdout or "").splitlines()
                if "UNMIGRATED" in l]
        fin_state = line[0].strip() if line else "OK"
        # A legacy ledger row that contradicts the deploy is not a
        # bookkeeping nit: bible_peshitta.json was recorded `removed`
        # after a rights rejection and a later full export put it back
        # in the public deploy, where it stayed for seven weeks because
        # nothing compared the two. The count rides in the guard's own
        # summary line so it cannot be silent again.
        contra = [l for l in (fin.stdout or "").splitlines()
                  if "LEGACY ROWS CONTRADICTING THE DEPLOY" in l]
        if contra and not contra[0].strip().endswith(": 0"):
            fin_state += f"; {contra[0].split(':')[-1].strip()} " \
                         f"LEGACY ROW(S) CONTRADICT THE DEPLOY"

    # 9. WITHDRAWAL IS DISCOVERABLE FROM THE DEPLOY (2026-08-08). Three
    #    mechanisms had grown up for one concept and only one was visible
    #    here: four records had left the archive by relocation alone, with
    #    nothing the deploy could see to say they had ever existed. A text
    #    that can be withdrawn invisibly is the Peshitta defect in other
    #    clothes, so the export now emits data/_generated/withdrawn.json
    #    and this refuses if it is missing, empty, or fails to name a
    #    record that is sitting under 01_library/_retired/.
    wd_state = "n/a"
    wpath = REPO / "data" / "_generated" / "withdrawn.json"
    if not wpath.exists():
        fail("Withdrawal manifest (9) MISSING — data/_generated/withdrawn.json "
             "is not built; run 05_scripts/build_public.py")
    wd = json.loads(wpath.read_text(encoding="utf-8"))
    listed = set(wd.get("withdrawn") or {})
    if not listed:
        fail("Withdrawal manifest (9) is EMPTY — this population has never "
             "legitimately been zero; refusing rather than blessing it")
    parked = set()
    retdir = REPO.parent / "01_library" / "_retired"
    for tj in retdir.rglob("text.json") if retdir.exists() else []:
        if "bootstrap-fixtures" in tj.parts:
            continue
        meta = json.loads(tj.read_text(encoding="utf-8"))
        for tr in meta.get("translations", []):
            if tr.get("id"):
                parked.add(f"{meta.get('id')}_{tr['id']}.json")
    unrecorded = sorted(parked - listed)
    if unrecorded:
        fail("Withdrawal manifest (9) FAILED — record(s) under "
             "01_library/_retired/ appear in no authority the deploy can "
             "see:\n  " + "\n  ".join(unrecorded))
    # 10. Creator death dates on gated records. REPORTED, never blocking:
    #     on the day this convention lands the honest number is small, and
    #     refusing a push over it would be theatre. But it must not be
    #     silent — every "PD by age" claim without dates rests on the
    #     publication year, and the 1948 Enchiridion was indexed 1900.
    cd_state = "n/a"
    cd_script = REPO.parent / "05_scripts" / "audit_creator_dates.py"
    if cd_script.exists():
        cd = subprocess.run([sys.executable, str(cd_script), "--brief"],
                            capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        if cd.returncode == 0 and cd.stdout.strip():
            cd_state = cd.stdout.strip().splitlines()[-1]

    # 11. Provenance, resolved through the derived-record convention.
    #     BLOCKING, unlike 10, and for a reason: check 10 reports a gap in
    #     evidence nobody has gathered yet, but this one fires only when the
    #     convention itself has broken — a derived record whose parent volume
    #     left the index, or whose parent cannot say where IT came from. In
    #     that state 35 public records silently lose their only source pin,
    #     and an audit reading text.json alone will report them as
    #     unprovenanced and propose them for removal. That happened once.
    pv_state = "provenance: resolver absent"
    pv_script = REPO.parent / "05_scripts" / "provenance_resolver.py"
    if pv_script.exists():
        pv = subprocess.run([sys.executable, "-X", "utf8", str(pv_script), "--brief"],
                            capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        if pv.returncode != 0:
            fail("Provenance (11) FAILED — the derived-record convention is "
                 "broken:\n" + (pv.stdout + pv.stderr).strip())
        pv_state = pv.stdout.strip().splitlines()[-1] if pv.stdout.strip() else pv_state

    # 12. citation permanence (2026-08-10). The archive promises that a
    #     citation keeps resolving. verify_permanence.py checks that promise
    #     against the live corpus — and it was wired into NOTHING: not this
    #     guard, not build_public, not rebuild_all. Its last committed run was
    #     2026-05-14, so when a June cleanup removed the passage a test
    #     citation pointed at, the failure sat unseen for three months.
    #     A promise nothing verifies is not a promise. 0.7s, so there is no
    #     argument for running it anywhere but here.
    #     --check because a guard that rewrites the tree it gates would leave
    #     uncommitted report files behind on every push.
    pm_state = "permanence unchecked"
    pm_script = REPO.parent / "05_scripts" / "verify_permanence.py"
    if pm_script.exists():
        pm = subprocess.run([sys.executable, "-X", "utf8", str(pm_script), "--check"],
                            capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        out = (pm.stdout + pm.stderr).strip()
        if pm.returncode != 0:
            fail("Citation permanence (12) FAILED — a URN the archive promises "
                 "will keep resolving does not:\n" + out)
        last = [ln for ln in pm.stdout.strip().splitlines() if ln.startswith("Result:")]
        pm_state = "permanence " + (last[-1].replace("Result: ", "") if last else "ok")

    wd_state = (f"{wd['counts']['total']} withdrawn "
                f"({wd['counts']['retired']} retired + "
                f"{wd['counts']['restricted']} restricted), "
                f"{len(parked)} relocated all recorded")

    print(f"pre-push guard v2: OK — {actual['entries']} = {actual['public']} "
          f"public + {actual['restricted']} restricted; reasons complete; "
          f"boundary clean; {hashed} artifact hashes verified; "
          f"reachability OK; separation: {sep_state}; "
          f"withdrawal: {wd_state}; {pv_state}; {cd_state}; "
          f"{pm_state}; "
          f"finalization ledger derived [{fin_state}] ({elapsed}).")


if __name__ == "__main__":
    main()
