# Digital Archive — Project Status

*Last refreshed: 2026-05-10*

A single trustworthy view of the project's current state. When numbers
here disagree with anything else in the project, this file is the one
to update — but it only reflects what the validation scripts in
`05_scripts/` actually produced.

---

## Canonical Library

The schema-validated corpus under `01_library/library/` and its
generated reader at `03_web_app/`.

| Measure | Count | Source of truth |
|---|---:|---|
| Distinct texts (web app reader) | **1,091** | `03_web_app/data/index.json` (unique `id`) |
| Translations published (web app reader) | **1,200** | `03_web_app/data/index.json` (entry count) |
| `text.json` files on disk | 1,131 | `01_library/library/texts/**/text.json` |
| Registry `text_count` and array length | 1,131 (agree) | `01_library/library/metadata/registry.json` |
| Distinct ids in registry | 1,086 | same — 13 multi-translation works share ids legitimately |
| Daily-reading whitelist | ~198 | `05_scripts/daily_passage.py` `WHITELIST` |
| Restricted (copyrighted) | 6 | `01_library/_restricted/copyrighted/` |
| Quarantined (integrity wishlist) | 11 | `01_library/_restricted/wishlist/` |

### Validation state (run 2026-05-10)

| Metric | Value | Report |
|---|---:|---|
| Fully clean | 666 (61.0%) | `logs/reports/final_validation.md` |
| Acceptable (minor issues) | 109 | same |
| Needs manual work | 316 (29.0%) | same |
| Texts with residual duplicate IDs | 39 | same |
| Total residual duplicate passages | 12,756 | same |
| Quality flags raised | 551 | same |

### Corpus audit (run 2026-05-10)

| Metric | Value | Report |
|---|---:|---|
| Texts with structural dup-ID issues | 48 | `logs/reports/corpus_audit_report.md` |
| Total excess duplicates (parser) | 184,634 | same |
| Texts missing front matter | 43 | same |
| Short stubs classified | 163,632 | same |
| — keep | 72,683 | same |
| — review | 47,779 | same |
| — drop | 43,170 | same |

### Ingestion warnings (run 2026-05-10)

| Metric | Value | Report |
|---|---:|---|
| Schema warnings | 233 | `logs/ingestion_issues.json` |
| Ingestion errors | 1 | `diogenes-lives::yonge` (empty passages) |

Down from 5,975 → 237 → 233 across Phases 3 and 4. The closed sets in
`validate_metadata.py` now cover `Devotional`, and `KNOWN_PUBLISHERS`
recognises `CCEL`, `Nag Hammadi Library`, `Early Christian Writings`,
and `gnosis.org`. The remaining 233 are content-level gaps — missing
`source.url`, `source_quality`, or `original_*` fields — that need
per-text editorial review rather than schema extension.

### Passage integrity (run 2026-05-10, full corpus)

The passage subsequence proof verifies every reader-facing passage is a
verbatim substring of its raw source after normalization. Combined with
`build_source_hashes.py`, this proves every word the reader sees came
from a named, SHA-256-anchored source.

| Metric | Value | Report |
|---|---:|---|
| Overall pass rate | **99.88%** | `logs/passage_subsequence_proof.md` |
| Passages verified | 2,660,212 / 2,663,500 | same |
| Translations checked | 1,195 | same |
| 100% verified | 706 | same |
| 95–99% verified | 393 | same |
| Below 95% | **0** | same |
| Skipped (no raw source linked) | 96 | same |
| Raw files SHA-256 anchored | 22,651 (~1.02 GB) | `02_raw_sources/manifest.json` |

The reader-facing integrity dashboard at `03_web_app/integrity.html` is
backed by `03_web_app/data/integrity.json` (regenerated 2026-05-10).

The older `text_preservation_proof.py` and its report
`logs/preservation_proof.SUPERSEDED.md` are retained for history only;
do not act on the numbers in that file.

### Raw sources

| Measure | Count |
|---|---:|
| Files in `02_raw_sources/` | 22,661 |
| With SHA-256 in `manifest.json` | (manifest dated 2026-04-19) |

The unparsed remainder is mostly already-acquired Gutenberg/SacredTexts
material that has not been triaged for the library — not all is intended
for ingestion.

---

## Reading Room

The public-facing curated archive at `workspace-hub/archive/`. Authored
locally; deployed via GitHub Pages. Schema for entries is defined in
`workspace-hub/archive/STANDARD.md` (Source Integrity Standard v1,
2026-05-04).

| Measure | Count |
|---|---:|
| `.md` entry files on disk | **205** |
| Entries with YAML frontmatter | 205 |
| Entries with `library_id` link to canonical | 204 |
| Entries linked from the curated front shelf (`index.md`) | 5 |
| Entries listed by tradition on `shelves.md` (deeper index) | all 205 reachable |
| Entries reachable via graph (`node_to_archive.json`) | 8 |
| Entries tagged `status: shelf` in frontmatter | 5 |
| Entries conforming to SIS v1 (`## Primary Text` block) | 10 |

The Reading Room is intentionally curated. The front shelf is small by
design. The deeper shelves at `workspace-hub/archive/shelves.html`
group the remaining entries by tradition; multi-chapter works are
listed once with the link entering at the first chapter.

---

## Project Surfaces

- **Canonical corpus** — `Digital-Archive/01_library/library/`. Schema
  in `SCHEMA.md`. Source of truth for every passage.
- **Web app reader** — `Digital-Archive/03_web_app/`. Browsable local
  reader, generated from the canonical corpus. Started via
  `Digital Archive.bat`.
- **Daily Reader** — `Digital-Archive/04_landing/`. Landing page +
  Render.com cloud server that emails one passage per subscriber per
  day. Pulls from a ~198-text whitelist of audited translations.
- **Reading Room** — `workspace-hub/archive/`. Hand-authored Markdown
  shelf, deployed via GitHub Pages. Independent corpus from the
  canonical library; soft-linked through `library_id` frontmatter.
- **Pre-pivot Atlas** — `Digital-Archive/atlas/`,
  `Digital-Archive/index.md`, `Digital-Archive/texts/`. Frozen.
  Authoring migrated to `workspace-hub/archive/` on the pivot date;
  retained for history.

---

## Known Issues

- Reading Room front shelf still holds 5 entries by design; the other
  200 are now listed by tradition on `shelves.html` (Phase 2). The
  shelves page collapses multi-chapter works into one entry each, so
  the page stays human-scale rather than database-shaped.
- Source Integrity Standard v1 migration is at 10 / 205.
- Schema validator emits 233 content-level warnings (missing
  `source.url`, `source_quality`, `original_*`). These need per-text
  review, not closed-set extension.
- 48 texts have structural duplicate-ID issues; the top 10 (`quran`,
  `jataka`, `ambrose-select-works`, `eusebius-church-history`,
  `expositor-bible`, etc.) account for most of the 184,634 excess
  passage-id duplicates and need parser work or manual restructuring.
  Distinguished from legitimate directory-level shared `id`s in
  `01_library/library/DUPLICATE_IDS.md`.
- `sappho-fragment-31` has no `library_id` — intentional; its body
  text records that the canonical library does not yet hold a Sappho
  text. Documented in `MAINTENANCE.md`.
- The 8-entry `metadata/texts.json` bootstrap fixture has been
  archived to `01_library/_archive/bootstrap-fixtures/` with a README
  explaining its history. The authoritative metadata is
  `registry.json`.
- The 39-entry manual-acquisition wishlist
  (`plans/comprehensive_wishlist.md`) and 10-entry quarantine list
  (`plans/library_wishlist.md`) are unchanged.

---

## Next Priorities

1. Triage the top 10 duplicate-ID texts (parser work, mostly).
2. Decide whether the Source Integrity Standard migration continues
   incrementally or is paused at v1's 10 pilot entries.
3. Reduce the 233 content-level schema warnings as texts come up
   for review.
4. Re-examine `newman-essays` (3 different works share one id) and
   `seneca-minor-dialogues` (duplicated under both `greek-philosophy`
   and `roman-philosophy`) when convenient.

---

## How this file is kept honest

This file is hand-edited but its numbers should come only from script
output. To refresh:

```
python 05_scripts/build_registry.py
python 05_scripts/validate_metadata.py
python 05_scripts/corpus_audit.py     --out logs/reports/corpus_audit_report.md
python 05_scripts/final_validation.py --out logs/reports/final_validation.md
python 05_scripts/passage_subsequence_proof.py --save --min-pass 0
python 05_scripts/build_integrity_report.py
python 05_scripts/gzip_web_data.py
python 05_scripts/lint_archive.py
```

Then update the *Last refreshed* date at the top and any numbers that
moved. Older runs are preserved under `logs/_archive/<date>/`.
