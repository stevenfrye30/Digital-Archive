# Archive operations

A quiet handbook for keeping the archive coherent over time.
This is not a developer onboarding document; it records the
operating discipline of a long-running archival project.

When in doubt, prefer slowness, prefer preservation, prefer
explicit decisions over silent automation.

---

## What lives where

The project has two intentional surfaces.

- **Canonical library** — `Digital-Archive/01_library/library/`.
  Every text.json file is a verified ingest of a named source.
  This is the authoritative store. The web reader at
  `03_web_app/` and the daily reading service at `04_landing/`
  are both **generated from** this surface. Do not hand-edit
  files under `03_web_app/data/` — they will be overwritten on
  the next build.
- **Reading Room** — `workspace-hub/archive/`. Hand-authored
  Markdown shelf, deployed via GitHub Pages. The Reading Room is
  **independent** from the canonical library; it soft-links via
  the `library_id` frontmatter field but is not a generated
  mirror. Authoring is canonical here. `Digital-Archive/atlas/`,
  `Digital-Archive/index.md`, and `Digital-Archive/texts/` are
  pre-pivot artifacts retained for history; do not edit them.

Numbers above (and elsewhere in the project) come from script
output. The truth surface for current state is `STATUS.md`.

---

## Refreshing the truth

The single command for "give me the current state of the
archive" is:

```
python 05_scripts/lint_archive.py
```

It produces `logs/reports/archive_health.md`, which links out to
the detailed reports. It is read-only and safe to run any time.

When the underlying numbers themselves are stale (the linter
will quote what is in `logs/`), refresh the inputs in this
order:

```
python 05_scripts/build_registry.py
python 05_scripts/validate_metadata.py
python 05_scripts/passage_subsequence_proof.py --save --min-pass 0
python 05_scripts/build_integrity_report.py
python 05_scripts/export_reader_data.py
python 05_scripts/final_validation.py --out logs/reports/final_validation.md
python 05_scripts/final_validation.py --json --out logs/reports/final_validation.json
python 05_scripts/corpus_audit.py    --out logs/reports/corpus_audit_report.md
python 05_scripts/corpus_audit.py    --json --out logs/reports/corpus_audit_report.json
python 05_scripts/gzip_web_data.py
python 05_scripts/lint_archive.py
python 05_scripts/build_cleanliness_report.py
```

`export_reader_data.py` is the bridge between the canonical library
and the public web reader. It rewrites `03_web_app/data/index.json`,
the per-translation merged files, and `source_manifest.json`. Without
this step, canonical metadata changes (a corrected `category`, a new
`description`, a re-classified `source_quality`) sit silently in the
working tree and are never visible to public readers. The May 2026
public-refresh pass added this step to the ritual after that
divergence was detected.

`export_reader_data.py` runs `validate_metadata` internally before
exporting and aborts on any error. Its pre-flight validation appends
to `logs/ingestion_issues.json`, so if you run both `validate_metadata`
and `export_reader_data` in the same refresh, validation entries
double-count. Either run only one of them or trim the log between
them — `lint_archive.py` reads the log and reports the inflated count
otherwise.

The passage proof is the slow one (~10 minutes for the full corpus).
Everything else completes in seconds.

After a refresh, update `STATUS.md`'s *Last refreshed* date and any
numbers that moved.

---

## Reading Room operations

### Adding a new entry

1. Write the Markdown file under
   `workspace-hub/archive/texts/<id>.md`. Frontmatter must carry
   at least `id`, `title`, `tradition`, `period`, `language`,
   `author`, `library_id`. See `STANDARD.md` for the full
   contract.
2. Run `python Digital-Archive/05_scripts/check_shelves_drift.py`.
   It will report the new entry as not yet covered.
3. Decide whether the entry belongs on the front shelf
   (`index.md`), on the deeper shelves (`shelves.md`), or only
   reachable by deep-link. The default is deep-link.
4. Hand-edit the relevant page — the shelves are hand-authored
   for atmosphere. The drift checker is a reminder, not a
   builder.

### Status field

Each entry's frontmatter may carry `status:` with one of
`shelf | deep-link | draft | legacy`. Absent means `deep-link`.
`entity.html` reads it and renders one quiet italic line under
the H1 for non-shelf entries. The contract is documented in
`workspace-hub/archive/STANDARD.md` §11.

### Verifying links

```
python Digital-Archive/05_scripts/validate_archive_links.py
```

Reports broken `library_id` pointers, broken
`entity.html?id=...` references, and entries that are not
surfaced anywhere. Read-only.

---

## Canonical library operations

### Adding a new text to the canonical library

The canonical-library ingest pipeline lives in `05_scripts/`.
The high-level shape is:

1. Place the raw source under
   `02_raw_sources/<publisher>/<filename>`.
2. Run `python 05_scripts/build_source_hashes.py` to anchor the
   raw file in `manifest.json`.
3. Run an `ingest_*.py` script appropriate to the source. The
   scripts produce a new `01_library/library/texts/<tradition>/<id>/`
   directory containing `text.json` and `passages_*.json`.
4. Re-run the refresh sequence above so all generated artifacts
   pick up the new text.

The 39-entry manual-acquisition wishlist is at
`plans/comprehensive_wishlist.md`. The 10-entry quarantine list
of texts removed for integrity issues is at
`plans/library_wishlist.md`. Both are reference, not enforcement.

### Restricted-library texts

`01_library/_restricted/` holds texts that are not exported to
the public surfaces. `_restricted/copyrighted/` is for texts
under copyright (Dead Sea Scrolls, etc.); these may appear in
the local web reader but are excluded from the registry.
`_restricted/wishlist/` is quarantine for texts removed because
their integrity fell below the 95 % subsequence-pass threshold.
Restoration is documented in `plans/library_wishlist.md`.

### Intentional outliers

Some validator findings are acceptable and should not be "fixed."

- **`sappho-fragment-31` has no `library_id`.** The Reading Room
  entry's body explains, in plain prose, that "Fragment 31 is not
  currently held in the Archive library." The pointer is genuinely
  absent because the canonical does not yet contain a Sappho text.
  When one is acquired, add the pointer; until then, the absence is
  the truth. The link validator will continue to count this as 1.
- **5 web-app entries do not appear in `registry.json`.** They live
  under `01_library/_restricted/copyrighted/`
  (`dead-sea-scrolls-{garcia-martinez,vermes}`,
  `gospel-ramakrishna-nikhilananda`, `hesse-siddhartha`,
  `think-grow-rich-hill`). The registry intentionally excludes them
  because they are under copyright; the local web app exposes them
  for personal reading.

### What the registry counts mean

`registry.json` is generated by `build_registry.py`. It walks
every `text.json` in the canonical library and records one
entry per file.

- `text_count` and the `texts` array length both equal the
  number of `text.json` files. They should always agree.
- The number of **distinct ids** is smaller, because some
  canonical works (`bible`, `quran`, `jataka`, ...) have parallel
  translation directories that share an `id`. Each directory has
  its own `text.json`; they are legitimately separate entries
  and not duplicates.
- The web app exposes ~5 ids that are not in the registry —
  these live under `_restricted/copyrighted/` and are deliberately
  excluded from the public registry.

---

## Things that should never be edited casually

- **Files under `03_web_app/data/`.** These are regenerated by
  the build pipeline. Edits will be lost.
- **Files under `Digital-Archive/atlas/`,
  `Digital-Archive/index.md`, `Digital-Archive/texts/`.**
  Pre-pivot, frozen, retained for history.
- **Reports under `logs/_archive/`.** Historical snapshots.
- **`logs/preservation_proof.SUPERSEDED.md` and
  `.SUPERSEDED.json`.** Misleading older preservation report
  retained for history. The current integrity anchor is
  `logs/passage_subsequence_proof.md`.
- **Passage content in `passages_*.json`.** Verified verbatim
  against raw sources. Re-ingest if the source changes; do not
  hand-edit.
- **Raw sources in `02_raw_sources/`.** Hash-anchored. Hand-
  editing breaks the integrity proof.

---

## Known long-running issues

These are tracked here so they do not get re-discovered each
session.

- **Top-10 duplicate-ID texts** (`quran`, `jataka`,
  `ambrose-select-works`, `eusebius-church-history`, etc.).
  Parser-level structural problems with passage-id collisions inside a
  single text. Distinct from directory-level shared `id` (which is
  often legitimate); the difference is documented in
  `01_library/library/DUPLICATE_IDS.md`. Visible in
  `logs/reports/corpus_audit_report.md`.
- **Source Integrity Standard v1 migration.** 10 / 205 Reading
  Room entries follow the stricter primary/commentary separation
  (`workspace-hub/archive/STANDARD.md` §1). Migration is
  unhurried.
- **Schema validation produces ~237 warnings** (mostly missing
  `source.url`, missing `source_quality`, missing `original_*`).
  These are content-level gaps, not structural problems.
- **`logs/preservation_proof.SUPERSEDED.md`.** Older 0.8 % pass
  rate is from a stricter golden-corpus check that no longer
  reflects the current discipline. Current integrity is 99.88 %.

---

## Two-surface contract, in one paragraph

The canonical library is the long memory. The Reading Room is
the doorway. The library is comprehensive, schema-validated,
and machine-built; the Reading Room is small, hand-edited, and
human-shaped. They are deliberately separate. A new entry on the
Reading Room does not require a canonical entry; a new canonical
text does not auto-appear in the Reading Room. They share a
project, not a build pipeline.
