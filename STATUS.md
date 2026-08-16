# Digital Archive — Project Status

*Last refreshed: 2026-08-03 — full validation suite re-run, and the
validation metrics below now come from THAT run rather than the 2026-06-07
one they were stuck on. The staleness had a cause, not just neglect: two of
the suite's scripts had stopped loading the corpus at all (see Known Issues).
Numbers here should only ever come from script output; the refresh sequence
is at the foot of this file.*

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
| Index entries (web app reader) | **1,112** | `03_web_app/data/_generated/index.json` (entry count) — 2026-08-07: +5 derived Shakespeare play work records (Much Ado, Troilus, Timon, 2H4, King John; provider `shakespeare-complete-plays`) |
| — of which public | **978** | same (`restricted` ≠ true) — 2026-08-16: −2, the rights-queue exposures withdrawn (ancient-jewish-proverbs, Cohen d. 1957 → PD 2028; buddha-life-herold, Blum d. 1981 → PD 2052) |
| — of which restricted (locked, metadata-only) | **134** | same (`restricted` = true) — incl. nostradamus-roberts (uncertain-copyright, withdrawn 2026-07-28: body does not match its stated Ward 1891 source) |
| Distinct ids | 1,087 | unique `id` — 31 ids legitimately shared across 120 entries (Jātaka ×8, bilingual pairs, multi-volume works). *(Re-derived 2026-08-07; the previous 1,106 figure predated several retirement lanes and was stale.)* |
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
v133 — and its design doctrine lives in `03_web_app/reports/` (it sat
beside this file at the repo root until Task 153, 2026-08-04):
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

- **11 review sheets still ship under `maps/` (77 KB) — by ruling.** Task 138
  moved the 22 files a build stage actually reads. These eleven are the ones
  nothing parses: their job is to be opened and marked up by a person, and the
  ruling says leave those where a maintainer finds them. Recorded with reasons
  in `tools/maps_served_ledger.json`. **Open question nobody has ruled on:**
  they are internal working documents — candidate bindings, rights holds, the
  design side's deliberations — and being tracked they are *served at public
  URLs*. Leaving them in place was ruled; publishing them was never separately
  considered. No scripture body is exposed, so this is not a rights leak.
- **The 12 `map/*.html` reception sections are stale (found in Task 138).**
  Re-running `build_reception_layers.py` rewrites the reception section of
  every map page; everything *outside* those sections is byte-identical, and
  the regeneration is deterministic across runs. So the committed pages were
  generated from an older `index.json` and have drifted since. Not caused by
  the Task 138 move — `ancient` is not in the generator's `SHEETS` map at all
  (its sheet text is `""` before and after), yet it drifted too. The
  regeneration was **reverted, not committed**: it is out of Task 138's scope
  and deserves its own lane, the same shape as Task 136's hall reconciliation.
- **`tools/inventory_chips.py` overwrites its tracked output with an empty
  result** when run without the local server it needs — 3,377 lines to 2, no
  error. Reverted, not committed. Same shape as doctrine §8.1b: an empty
  population should refuse, not write. **Half-closed in Task 148, and only
  half:** the *room-selection* emptiness is fixed — both inventories derived
  their room set from the string `"Task 111 "` appearing in a page, which
  decayed to one room and then (at Task 146) to zero while both still
  reported findings; the set is now derived from what a file is (a room is a
  `map/*.html` that is not a `<meta http-equiv="refresh">` redirect stub) and
  both refuse on empty, proven by running them against an empty `map/`. The
  *no-server* case above is untouched and still open: if Playwright reaches
  no page, the sweep is legitimately empty and gets written.
- **Both inventory artifacts were frozen from 2026-08-02 to 2026-08-04** and
  are only now regenerated on a real 16-room sweep. They were last written at
  `8f508631`, the commit *before* Task 126's shared-block extraction — and
  that same extraction deleted the `"Task 111 "` comments the tools keyed on,
  so the lane that made the artifacts stale also blinded the tool that would
  have caught it. Note when reading them: they count **per-page markup in
  `map/*.html` only**, so anything Task 126 moved into a shared file reads as
  "absent" without having left the archive (`canon note` 16/16 → 0/16,
  `collapse ctl` 4 → 2 per room, `stat line` 15 rooms → 0 all trace to
  `e838922e` alone). The report now says so in its own banner.
- **`maps/trad2map.json` churned on every build until Task 138.** Its key order
  came from iterating Python **sets**, so randomized string hashing reordered
  it each run — three consecutive builds produced three different sha256s. It
  is now emitted sorted. Pre-existing and unrelated to the file moves, but it
  silently defeated the byte-identical proof discipline the deploy rests on.
  Worth a sweep for the same shape in other generators.

- Archive-shelf front shelf still holds 5 entries by design; the other
  200 are now listed by tradition on `shelves.html` (Phase 2). The
  shelves page collapses multi-chapter works into one entry each, so
  the page stays human-scale rather than database-shaped.
- Source Integrity Standard v1 migration is at **77 / 269** Reading Room
  entries (was 10 / 205).
- Schema validation is at **0 errors, 220 warnings** across 1,055 texts
  (missing `source.url`, `source_quality`, `original_*`) — was 233. These
  need per-text review, not closed-set extension. Note
  `logs/ingestion_issues.json` holds 6,424 entries, but it is a CUMULATIVE
  history across every run, not a current state; `archive_health.md` used to
  present it as "schema warnings / schema errors" and now labels it honestly.
  Its single logged error is an *ingestion* error, not a schema one — see
  Diogenes Laertius below.
- **Duplicate IDs: RESOLVED.** The 2026-08-03 suite reports **0 texts, 0
  excess duplicates** across 3,293,485 passages in 1,076 texts, and
  `final_validation` agrees (0 texts with residual dups). The former claim —
  40 texts and 12,779 excess ids, led by the CCEL patristic cluster — is
  retired. The cleanup lanes since June closed it. The Quran's once-reported
  158,458 collisions were a measurement artifact resolved by the May 2026
  restoration (`records/QURAN_RESTORATION_2026.md`). Legitimate
  directory-level shared `id`s remain distinguished in
  `01_library/library/DUPLICATE_IDS.md`.
- **The validators were measuring nothing (found 2026-08-03).** Both
  `corpus_audit.py` and `final_validation.py` crashed on the six restricted
  rows that carry `data_file: null` by design, and both looked for
  `data/<name>.json` when the deploy layer leaves `data/<name>.json.gz` —
  1,177 gzipped bodies against 4 plain ones. So every body was skipped and
  the audit reported "0 texts, 0 excess dups, 0 missing front matter" from a
  corpus of zero, which reads as a clean bill of health. Both now fall back
  to the gzip and both REFUSE an empty population (doctrine §8.1b). This is
  the likeliest reason the corpus metrics sat unchanged from 2026-06-07.
- **162 texts are missing front matter**, and 104,854 short stubs are
  triaged 51,337 keep / 36,283 review / 17,234 drop
  (`logs/reports/corpus_audit_report.md`).
- **Heading leakage is now the top structural fault**, not duplicates:
  `ramayana-griffith` (498), `book-of-dead-renouf` (430),
  `anf01-early-fathers` (395), `proclus-theology-plato` (371),
  `uttaradhyayana-sutra` (276). 265 of 1,076 texts are "needs work" on this
  measure; 715 (66.4%) are fully clean.
- **Passage-fidelity proof reads 90.50%** (2,328,378 / 2,572,799), 641 texts
  at 100%. **Treat the headline as understated.** Eleven texts report exactly
  0.0% — every non-English Bible witness (Russian Synodal, Arabic Van Dyck,
  Louis Segond, Chinese Union, Reina-Valera, Luther, Nestle Greek, both
  Peshitta NTs) plus Targum Onkelos, and `sbl-nt` at 38.8%. A whole text
  matching zero of 31,141 passages is an instrument reading, not a corpus
  reading (doctrine §8.1f): the normalizer is almost certainly ASCII-centric.
  Those 11 account for 216,868 of the 244,421 unverified passages — 88.7%. If
  the normalizer is the fault, true fidelity is ≈98.9%. **Not fixed: this
  needs a real encoding investigation, not a guess.**
- **One ingestion error outstanding:** "The Lives and Opinions of Eminent
  Philosophers" (Diogenes Laertius) — *Parser produced 0 passages*.
- `sappho-fragment-31` has no `library_id` — intentional; its body
  text records that the canonical library does not yet hold a Sappho
  text. Documented in `MAINTENANCE.md`.
- The 8-entry `metadata/texts.json` bootstrap fixture has been
  archived to `01_library/_retired/bootstrap-fixtures/` with a README
  explaining its history. The authoritative metadata is
  `registry.json`.
- The 39-entry manual-acquisition wishlist
  (`plans/comprehensive_wishlist.md`) and 10-entry quarantine list
  (`plans/library_wishlist.md`) are unchanged.

---

## What's actually urgent

**0. The backup pack — the Tasks 137–138 regression is CLOSED; the standing
habit is not.** Tasks 137 and 138 moved 23 build inputs (1,208 KB) out of
the served tree and into `05_scripts/configs/`. That was the right move:
they were shipping to Pages at public URLs for no reason. But the parent
repo **has no remote**, and `03_web_app` does — so until then those files
were being backed up *by accident*, as a side effect of the mistake.
Correcting the mistake removed their only offsite copy.

These are not regenerable from the archive: `seed_bindings.json` carries
the design side's confirmed verdicts, and the 16 `structure.json` files
are the hand-reviewed zone/chip skeletons every room's bindings derive
from. Losing this machine loses them.

The 2026-08-03 pack below closed that specific hole — the 23 files are in
it and verified. What has NOT changed is the underlying exposure: **every
parent-repo commit is one machine away from gone until the next pack**, and
packs are steward-only by design (the passphrase never touches this
machine). So this stays at the top of the list, no longer as an emergency
but as the one item that has to be re-run rather than finished.

**Scope fixed 2026-08-03.** `05_scripts/configs` is now in
`backup_canonical.py`'s `INCLUDE_ROOTS`, so all 23 files (the 22 moved plus
`seed_bindings.json`) are in the pack manifest — verified by listing
`collect_files()`, not assumed. Note `collect_files()` is a plain `rglob`
and never consults `.gitignore`, so the gitignored `configs/maps/**` and
`configs/sheets/**` are covered by naming the directory there; they remain
untracked by git, which is a separate question nobody has ruled on. Two
`--pack` runs on 2026-08-03 wrote unopenable archives (a passphrase
whitespace defect, since fixed and proven) and were deleted.

**RUN AND VERIFIED 2026-08-03 21:29 local.** From `logs/backups.log`, which
is the source of truth for this row — not this file:

```
20260804T012922Z PACK   files=30240 bytes=5,748,862,457
                        fp=sha256:f81ac816…  archive_sha=c6a116b06d19
                        -> D:\Archive Backups\digital-archive-backup_20260804T012922Z.tar.gz.enc
20260804T015146Z VERIFY result=OK bad=0 missing=0 fp=ok
```

The `files=` count rising 30,120 → 30,240 is the 23 moved config files
entering the pack, which is the regression above closing. Two verified July
28 packs are also intact.

**This row was stale for one day and said the opposite.** It read "run
pending" after the run had happened and verified, and that wording was
repeated back to the steward as fact more than once. Timestamps in
`backups.log` are UTC (`Z`); local is UTC−4, so `20260804T012922Z` is the
evening of **August 3** local — the off-by-one is easy to make and is why
the log line is quoted verbatim here rather than paraphrased.

**What the verified pack does NOT contain.** It predates the morning of
2026-08-04 by about four hours, so Tasks 146, 147 and 148 are outside it:
parent commits `8ed83b7`, `b664165`, `3c5a7e6` (including Task 148's 16
resynced `map_sources/` files, ~1.19 MB) and hindu's gitignored
`configs/maps/hindu/structure.json` gloss edit. The parent repo has no
remote, so for those files the pack is the only offsite copy that will ever
exist. **Next action, steward-only: another `--pack` + `--verify` once the
external drive is connected.**

## Next Priorities

*Re-baselined 2026-08-03 from a full suite run. The duplicate-ID triage that
led this list for two months is done — it reports zero.*

1. **Investigate the passage-fidelity normalizer.** Eleven texts read
   exactly 0.0%, all non-English or non-Latin script. They are 88.7% of all
   unverified passages. Either the archive has a real corruption confined to
   every non-English witness at once, or the normalizer cannot read them —
   and the second is far likelier. This is the single largest number on the
   board and probably not a corpus problem at all.
2. Reduce the 220 content-level schema warnings as texts come up for review.
3. Decide whether the Source Integrity Standard migration continues
   incrementally or pauses at 77 / 269.
4. Front matter: 162 texts missing; and work the 36,283 "review" stubs.
5. Fix the Diogenes Laertius ingestion error (parser produced 0 passages).
6. Re-examine `newman-essays` (3 different works share one id) and
   `seneca-minor-dialogues` (duplicated under both `greek-philosophy`
   and `roman-philosophy`) when convenient.

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
moved. Older runs are preserved under `logs/_before_snapshots/<date>/`. The
pre-push guard reads the Canonical Library counts, so a push after an
export lane will be blocked until they are refreshed here.
