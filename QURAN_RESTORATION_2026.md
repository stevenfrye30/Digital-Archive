# Qurʾān Restoration — May 2026

A note recording the first editorial restoration pass on the archive's
Qurʾān, performed in the spirit of careful preservation rather than
repair work.

---

## What was thought to be wrong

The Quran was the highest-priority entry in the archive's structural
duplicate-id queue with a reported **158,458 excess passage-id
collisions** under category `missing_book_level`. The figure suggested
the parser had flattened the sura/ayah hierarchy and, since the Quran
is a foundational text and a natural target for a future commentary
layer, the restoration was scheduled as the first such pass.

## What was actually wrong

After careful inspection, the data itself was already at edition
quality.

The canonical `01_library/library/texts/sacred/islam/quran/` directory
holds 20 translations sourced from Tanzil (Saheeh International,
Arberry, Pickthall, Yusuf Ali, Talal Itani, Maududi, the Uthmani
codex, and twelve more). Each translation's `passages_*.json` file is
internally clean: 6,236 ayat keyed as `surah.ayah` with **zero
internal id collisions** and a `path` of `[sura, ayah]` matching the
declared `hierarchy: ["surah", "ayah"]`. Sura counts match the
canonical layout exactly — Sura 1 has 7 ayat, Sura 2 has 286, Sura 36
has 83, Sura 112 has 4, Sura 114 has 6, and so on across all 114
suras.

The 158,458 figure was a **measurement artifact** in
`05_scripts/corpus_audit.py`. The script grouped passages by `text_id`
only, so all 23 published Quran translations (20 Tanzil + 3
auto-ingest variants) were aggregated into one bag of ~180,000
passages and the same ayah ids legitimately appearing once per
translation were counted as collisions. A single ayah keyed `1.1`
appearing across 23 translations contributed 22 to the dup count —
multiplied across 6,236 ayat, the bulk of the 158,458 was nothing more
than parallel translations being read together.

## What was changed

Three small, surgical changes — none of them touching Quran passage
content.

### 1. Metadata of three auto-ingest Quran variants

Three sibling directories carry SacredTexts.com / Project Gutenberg
auto-ingests of historical English translations. Their `text.json`
metadata was inherited from a generic auto-ingest template. The
following fields were corrected:

| Directory | Field | Before | After |
|---|---|---|---|
| `quran-rodwell` | `category` | `"Literature"` | `"Scripture"` |
| `quran-rodwell` | `tags` | `["modern philosophy", "auto-ingest"]` | `["scripture", "islam", "auto-ingest", "non-canonical-ordering"]` |
| `quran-rodwell` | `source_quality` | `"acceptable"` | `"provisional"` |
| `quran-rodwell` | `description` | terse auto-string | a paragraph noting Rodwell's chronological reordering and pointing readers to the Tanzil-sourced sibling |
| `quran-yusuf-ali` | (same four fields) | (same defaults) | corrected; description notes the front-matter chapters and points to the Tanzil-sourced `yusufali` sibling |
| `quran-yusuf-ali-pickthal-shakir` | (same four fields) | (same defaults) | corrected; description notes the bundled-parallel format |

The `hierarchy: ["chapter", "verse"]` was **deliberately preserved**
on all three — Rodwell really did rearrange the suras chronologically,
and the SacredTexts Yusuf Ali file really does have front-matter as
its first chapters. Renaming those structural levels to `surah/ayah`
would have been false. The honest naming is "chapter/verse" with a
description that warns the reader about the non-canonical numbering.

### 2. Surgical fix to `05_scripts/corpus_audit.py`

Two changes to the duplicate-id audit:

- `Passage` records now carry a `data_file` field, identifying the
  specific translation file each passage came from.
- `load_corpus()` deduplicates by `(text_id, data_file)`: when several
  index entries point at the same data file (the three SacredTexts /
  Gutenberg Quran variants all publish to `quran_anonymous.json` under
  the current build pipeline), the file is loaded once.
- `run_dup_id_audit()` audits each translation independently by
  grouping on `(text_id, data_file)`. The per-text-id priority queue
  preserves its existing one-row-per-text shape by keeping the worst
  translation as the representative.

These together make duplicate-id volume a per-translation parser
metric rather than an inadvertent measure of "how many translations
share a text id." Multi-translation works (Quran, Bible, Jataka) no
longer surface false alarms.

### 3. Nothing else

Quran passage text: untouched. Ayah ordering: untouched. Hierarchy
declarations on the canonical Tanzil-sourced `quran/` directory:
untouched. Web reader behaviour: unchanged. Reading Room: untouched.

## What was preserved

- Every byte of every Quran passage in every translation.
- The 6,236-ayat / 114-sura canonical structure across all 20 Tanzil
  translations.
- The Uthmani Arabic script (RTL preserved end-to-end).
- All translation aliases (`yusufali`/`abul-aala-maududi` etc.).
- All raw-source SHA-256 hashes.
- The three auto-ingest variants in their existing internal structure.

## Integrity verification

After the changes:

| Check | Result |
|---|---:|
| Quran passage subsequence proof (23 targets) | **99.99%** (102,516 / 102,522 verified) |
| Quran translations failing 95% threshold | **0** |
| Quran translations at 100% verified | 12 |
| Quran translations skipped (no raw config) | 8 |
| Corpus-wide dup-id total | 184,634 → **12,779** (93% reduction) |
| Quran's contribution to dup-id total | 158,458 → **0** |
| Quran's position on the priority queue | #1 → **off the queue** |

The remaining 12,779 corpus-wide duplicate ids are real per-translation
parser problems (mostly the CCEL Christian patristic cluster); they are
unaffected by this restoration and surface honestly now that the
metric reflects the per-translation reality.

## Manual editorial observations

Some details worth recording because they are easy to mistake for
errors but are properties of the Tanzil source.

- **Bismillah in the Uthmani script.** The Uthmani Arabic translation
  prefixes the *Bismillah* (`بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ`) to the
  text of verse 1 of every sura except Sura 9. This matches the
  canonical Mushaf layout in the Uthmanic codex tradition. The English
  translations (saheeh, arberry, pickthall, yusufali) treat the
  *Bismillah* as a separate convention and start verse 1 with the
  sura's first content. Both are correct in their tradition; the
  archive preserves both.
- **Verse-counting traditions.** Tanzil follows the Egyptian standard
  numbering (1924 Cairo edition). Some historical translations use the
  Flügel numbering, which differs in a small number of places. The
  three auto-ingest variants may use either; their `chapter_titles`
  are the most reliable guide to what a given chapter contains.
- **"Surah" / "sura" / "sūra" spelling.** The canonical metadata uses
  `"surah"` in `hierarchy` and `"surah"` in entry counts. Translation
  titles use the spelling chosen by the translator (Saheeh: "Surah",
  Arberry: "sura"). The reader sees both naturally; no normalization
  is desired or appropriate.
- **6,236 vs 6,348 ayat.** The Tanzil distribution counts ayat at
  6,236 (excluding the *Bismillah* of suras 1–8, 10–114, which are not
  separately numbered in the Egyptian standard). Other counting
  traditions reach 6,348 by counting each *Bismillah* as a separate
  ayah. The archive's count of 6,236 reflects the Tanzil source
  faithfully.

## Future commentary readiness

The hierarchy and id scheme are already prepared for tafsir / commentary
insertion:

- **Stable ayah ids.** Every ayah's id is `<sura>.<ayah>` (no zero
  padding; no leading zeros) and these ids are guaranteed unique
  within each translation.
- **Stable deep links.** The web reader already supports
  `?text=quran_<translation>.json&passage=2.255` style anchoring.
  Commentary nodes can attach by referencing `(quran, <translation>,
  <ayah-id>)` or, for translation-independent attachment,
  `(quran, <ayah-id>)`.
- **Cross-references.** Inter-textual references (Quran → Hadith,
  Quran → Tafsir, Quran ↔ Bible) can use the ayah-id as the canonical
  anchor without ambiguity.
- **Apparatus support.** The `01_library/library/SCHEMA.md` `apparatus_file`
  pattern (used by `upanishads-muller-part2`) is the natural shape for
  attaching translator notes and footnotes to a Quran translation
  without modifying the verses themselves. No translation here uses
  it yet; the structure already supports it.

## Future print-quality possibilities

The data structure also supports print rendering without further work:

- **Verse separation.** Each ayah is a discrete passage with a stable
  id. A print engine can render one ayah per indented paragraph with a
  superscript verse number.
- **Sura openings.** Suras can be set in their own page or section with
  the sura title (currently in the translation's chapter_titles, not
  yet in metadata) as a heading. Adding `sura_titles` to text.json's
  metadata layer is a small future addition that would not require
  reingestion.
- **Bilingual layout.** The Uthmani Arabic and any English translation
  can be set facing — Tanzil's stable per-ayah keying makes the
  alignment automatic.
- **Hizb / juz divisions.** Tanzil's source data carries hizb and juz
  metadata that is not currently exposed in the archive. If a print
  edition wants the traditional 30-juz division, the data is
  recoverable from the raw source.

None of these have been built. The structure does not impede them.

## Remaining limitations

- **The three auto-ingest variants remain provisional.** Their
  passage-level data was not re-ingested. Rodwell's chronological
  ordering and Yusuf Ali / SacredTexts' front-matter chapters remain
  as imported. A future per-translation re-ingest could canonicalize
  them, but the Tanzil-sourced `quran/` directory already provides
  edition-quality versions of every text these auto-ingests claimed to
  hold.
- **Three index entries publish to one filename.** The web build
  currently maps the three `quran` directories with translation_id
  `anonymous` to the single output `quran_anonymous.json`, so two of
  the three auto-ingest variants are not separately reachable through
  the public reader. Resolving this is a build-pipeline concern
  upstream of the canonical library and was outside the scope of this
  restoration.
- **Tafsir / commentary.** The archive holds no tafsir at present. The
  structure is ready; the content is not yet acquired.
- **Reading Room.** The Reading Room currently exposes Sura 1 (the
  Fatiha) and Sura 96 (the *Iqra'* opening) under `quran-sura-1` and
  `quran-sura-96`. Both link via `library_id: quran` to the canonical
  `quran` text and `library_chapter: 1` and `96` respectively. Other
  ayat reachable through deep-link only.

## Closing note

The restoration was preservation work, not repair work. The Quran's
data was already in edition-quality shape; the perceived problem was
instrument calibration. The archive now records that finding honestly:
the headline number was an audit metric, not a corpus wound. The
canonical Quran is intact, navigable, and ready to receive a
commentary layer when one is brought in.

---

*Snapshot of pre-restoration state preserved at
`logs/_archive/2026-05-quran-restoration/`. The full text-by-text
condition report covering all 1,091 corpus works is at
`TEXT_CLEANLINESS.md`. The institutional checkpoint that frames this
restoration is `STABILIZATION_EDITION_2026.md`.*
