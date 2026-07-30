# Digital Archive — Project Status

*Last refreshed: 2026-07-27 (index counts re-verified against
`data/_generated/index.json`; validation metrics below are from the 2026-06-07
run and are dated where they appear).*

A single trustworthy view of the project's current state. When numbers
here disagree with anything else in the project, this file is the one
to update — but it only reflects what the validation scripts actually
produced.

> **Where this file lives.** Moved from the parent working archive into
> `03_web_app/` on 2026-07-27 so the public README's link to it
> resolves. Paths such as `01_library/` and `05_scripts/` refer to the
> parent `Digital-Archive/` working tree, which is local-only and does
> not publish. The pre-push guard (`tools/prepush_guard.py`) reads the
> Canonical Library counts below as its invariant — refresh them here
> when the corpus legitimately changes.

---

## Canonical Library

The schema-validated corpus under `01_library/library/` and its
generated reader at `03_web_app/`.

| Measure | Count | Source of truth |
|---|---:|---|
| Index entries (web app reader) | **1,195** | `03_web_app/data/_generated/index.json` (entry count) |
| — of which public | **1,095** | same (`restricted` ≠ true) |
| — of which restricted (locked, metadata-only) | **100** | same (`restricted` = true) — incl. nostradamus-roberts (uncertain-copyright, withdrawn 2026-07-28: body does not match its stated Ward 1891 source) |
| Distinct ids | 1,106 | unique `id` — 32 ids legitimately shared across 122 entries (Jātaka ×8, bilingual pairs, multi-volume works) |
| `text.json` files on disk | 1,055 *(2026-07-27)* | `01_library/library/texts/**/text.json` |
| Daily-reading whitelist | ~198 | `05_scripts/daily_passage.py` `WHITELIST` |
| Restricted (copyrighted) source dirs | 81 *(2026-07-27)* | `01_library/_restricted/copyrighted/` |
| Quarantined (integrity wishlist) | 10 *(2026-07-27)* | `01_library/_restricted/wishlist/` |

### Validation / integrity (run 2026-06-07)

| Metric | Value | Source |
|---|---:|---|
| Metadata validation errors | **0** | `05_scripts/validate_metadata.py` |
| Public entries that fail to open | **0** | all public `data_file`s load with content |
| Orphan (un-shelved) public entries | **0** | every tradition maps to a shelf |
| Passage subsequence proof | **99.83%**, 0 FAIL | `logs/passage_subsequence_proof.md` |
| Unproven sources (readable, not yet proof-verified) | 4 | cicero-de-officiis, tibetan-tantra-muses, babylonian-talmud-rodkinson, bible/peshitta |
| Exact-duplicate texts | 0 (+4 intentional Tanakh/Bible-OT parallels) | `05_scripts/find_exact_duplicate_texts.py` |
| Residual duplicate passage-IDs | 196 (upanishads only, deliberate) | `05_scripts/dedupe_passage_ids.py` |
| Restricted-text safety guard | PASS | `05_scripts/check_no_restricted_text.py` |
| Short stubs classified | 163,632 | same |
| — keep | 72,683 | same |
| — review | 47,779 | same |
| — drop | 43,170 | same |

## Text Organization (taxonomy, as of 2026-06-07)

Every public text is shelved into exactly **one of four top-level categories**
by its `tradition` field, via `BUCKET_FOR_TRADITION` in
`03_web_app/index.html` (enforced against `VALID_TRADITIONS` in
`05_scripts/validate_metadata.py`). The `category` field on each text is a
finer-grained *genre* tag (Theology, Mythology, History…), NOT the shelf.

| Shelf | Public texts *(2026-06-07)* | Traditions mapped to it |
|---|---:|---|
| **Religion** | 588 | Christian, Hindu, Buddhist, Jewish, Islam, Confucian, Taoist, Egyptian, Mesoamerican, Mesopotamian, Norse, Celtic, Shinto, Gnostic, Jain, Finnish, Comparative Religion, Sikh, Zoroastrian, Tibetan Buddhist, Bahai, Mandaean, Rastafari, Slavic, Mohist, **Native American**, **Polynesian**, **African** |
| **Philosophy** | 302 | Modern Philosophy, Greek Philosophy, Roman Philosophy, Political Philosophy, Stoic, Legalist, Japanese Philosophy, Chinese Strategy |
| **Literature** | 138 | Greek Literature, Greek, Persian Literature, **Spanish/English/German/French/American/Latin/Sanskrit/Arabic/Japanese Literature** |
| **Esoteric** | 86 | Hermetic, Theosophy, **New Thought**, Witchcraft / Folk Religion |

(Bold traditions were added in the 2026-06-07 correctness pass when the
"Modern Philosophy" catch-drawer and a block of mislabeled folklore were
re-shelved truthfully. Per-shelf counts predate the July 2026 corpus
growth to 1,120 public entries and will be recounted at the next
validation run.)

### Organizing policies
- **One copy per version.** A work + a specific translation appears exactly
  once. 65 exact-duplicate entries were removed in the correctness pass
  (verbose-named re-ingests, Quran/Bible translations stored 2–3×). Verify
  with `05_scripts/find_exact_duplicate_texts.py`.
- **Bible ↔ Tanakh parallel presentations (intentional exception).** The
  Masoretic Text, Westminster Leningrad Codex, JPS, and Leeser each exist
  twice on purpose: once in the Christian **Bible** group (Old Testament path)
  and once as the Jewish **Tanakh** (Jewish-shelf path). These are the *same
  underlying Hebrew text* surfaced through two legitimate browsing traditions,
  not duplicate junk. A future alias/shared-source model could unify the
  bytes; until then both are kept so both paths stay complete.
- **Restricted entries** (91 in the index) are locked, metadata-only
  placeholders (`restricted: true`) for works not yet clear for
  worldwide public-domain publication. The named record for the
  June→July growth from 19 to 91 is the L6 rights-blocked tier of
  `plans/EXPANSION_2026-07_master_plan.md` (finalization + rights
  model). Backing on disk: 81 source dirs under
  `01_library/_restricted/copyrighted/`, plus the local-only Upaniṣad
  pipeline volumes staged outside the repo. Their data files are
  gitignored + untracked so the body is **never deployed**; the
  pre-push guard verifies this on every push.

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

## Reader design state — the Genesis codex

Since May 2026 the reader's deepest design work has treated Genesis as
an annotated codex: twelve object families with resonance pairings,
witness families given distinct manuscript identities, the leaf
redefined from modal overlay to prepared sheet, five Doré plates staged
behind a museum scrim, and a portrait cosmogram of the five Hebrew
cosmic strata. This work is **shipped** — the reader's build meta reads
v133 — and its design doctrine lives beside this file in `03_web_app/`:
`WITNESS_FAMILY_CONSTITUTION.md`, `OBJECT_FAMILY_CONSTITUTION.md`,
`FOLIO_OBJECT_ARCHITECTURE.md`, `READING_CHOREOGRAPHY.md`, the
`GENESIS_*` roadmap/coverage/harmonization set, and the audit records
(leaf, orientation, temporality, cosmogram, civilizational). Its build
loop — audit against captured screenshots and a metrics JSON, specify,
implement, verify — is the house pattern for reader design work.

---

## Archive shelf (`workspace-hub/archive/`)

The hand-authored curated shelf, deployed via GitHub Pages — what
ARCHITECTURE.md calls the *archive shelf* (older revisions of this file
called it the Reading Room; that name belongs to the generated reader
at `03_web_app/`). Authored locally; schema for entries is defined in
`workspace-hub/archive/STANDARD.md` (Source Integrity Standard v1,
2026-05-04).

| Measure | Count *(2026-06-07)* |
|---|---:|
| `.md` entry files on disk | **205** |
| Entries with YAML frontmatter | 205 |
| Entries with `library_id` link to canonical | 204 |
| Entries linked from the curated front shelf (`index.md`) | 5 |
| Entries listed by tradition on `shelves.md` (deeper index) | all 205 reachable |
| Entries reachable via graph (`node_to_archive.json`) | 8 |
| Entries tagged `status: shelf` in frontmatter | 5 |
| Entries conforming to SIS v1 (`## Primary Text` block) | 10 |

The archive shelf is intentionally curated. The front shelf is small by
design. The deeper shelves at `workspace-hub/archive/shelves.html`
group the remaining entries by tradition; multi-chapter works are
listed once with the link entering at the first chapter.

---

## Project Surfaces

- **Canonical corpus** — `Digital-Archive/01_library/library/`. Schema
  in `SCHEMA.md`. Source of truth for every passage.
- **Web app reader (the Reading Room)** — `Digital-Archive/03_web_app/`.
  Browsable reader, generated from the canonical corpus by
  `05_scripts/export_reader_data.py`. Started via
  `Digital Archive.bat`. The exact regeneration timestamp is recorded
  inside `03_web_app/data/source_manifest.json` (the `generated` field);
  if that timestamp is older than `Last refreshed` above, the public
  reader is stale and the refresh ritual in `MAINTENANCE.md` should
  be re-run.
- **Daily Reader** — `Digital-Archive/_archive/04_landing/` (frozen
  surface since Task 11 lane A, 2026-07-27). Landing page +
  Render.com cloud server that emails one passage per subscriber per
  day. Pulls from a ~198-text whitelist of audited translations.
- **Archive shelf** — `workspace-hub/archive/`. Hand-authored Markdown
  shelf, deployed via GitHub Pages. Independent corpus from the
  canonical library; soft-linked through `library_id` frontmatter.
- **Pre-pivot Atlas** — `Digital-Archive/_archive/atlas/`,
  `Digital-Archive/_archive/texts/`. Frozen. Authoring migrated to
  `workspace-hub/archive/` on the pivot date; retained for history
  (the root `index.md` tombstone was deleted 2026-07-27).

---

## Known Issues

- Archive-shelf front shelf still holds 5 entries by design; the other
  200 are now listed by tradition on `shelves.html` (Phase 2). The
  shelves page collapses multi-chapter works into one entry each, so
  the page stays human-scale rather than database-shaped.
- Source Integrity Standard v1 migration is at 10 / 205.
- Schema validator emits 233 content-level warnings (missing
  `source.url`, `source_quality`, `original_*`). These need per-text
  review, not closed-set extension.
- 40 texts have structural duplicate-ID issues; the top 10
  (`ambrose-select-works`, `eusebius-church-history`,
  `augustine-confessions-enchiridion-ccel`, `jerome-letters-works`,
  `athanasius-select-works`, etc. — the CCEL Christian patristic
  cluster) account for most of the 12,779 excess passage-id duplicates
  and need parser work or manual restructuring. The Quran's previously
  reported 158,458 collisions turned out to be a measurement artifact
  in `corpus_audit.py` and were resolved by the May 2026 restoration
  (`records/QURAN_RESTORATION_2026.md`); the audit now groups per translation
  so multi-translation works do not surface false alarms.
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
5. Re-run the full validation suite so the 2026-06-07-dated metrics
   above catch up with the July 2026 corpus growth.

---

## How this file is kept honest

This file is hand-edited but its numbers should come only from script
output. To refresh (from the parent `Digital-Archive/` working tree):

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
moved. Older runs are preserved under `logs/_archive/<date>/`. The
pre-push guard reads the Canonical Library counts, so a push after an
export lane will be blocked until they are refreshed here.
