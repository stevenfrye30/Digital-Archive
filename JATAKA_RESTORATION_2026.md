# Jātaka Restoration — May 2026

A note recording the second editorial restoration pass on the archive's
narrative tradition: the Pāli Jātaka, the corpus of birth-stories
of the Buddha. Like the Qur'an restoration that preceded it, this pass
turned out to be more about confirming an already-quiet state than
about repair.

---

## What was thought to be wrong

The Jātaka was the next entry on the structural duplicate-id queue
after the Qur'an, with **8,895 excess passage-id collisions** under
category `missing_book_level`. The audit suggested the volumes had
collapsed and the parser had flattened the multi-volume hierarchy.
The Jātaka is also a natural candidate for editorial care — it is
oral storytelling literature, future Reading Room material, and a
plausible target for a print edition — so a substantive parser
restoration was scheduled.

## What was actually wrong

The data itself was already at edition quality.

The canonical library holds **seven Jātaka directories**, each with
its own self-contained translation:

| Directory | Translator | Year | Tales | Passages |
|---|---|---:|---:|---:|
| `jataka-chalmers-vol1` | Robert Chalmers | 1895 | 149 | 3,123 |
| `jataka-vol2` | W. H. D. Rouse | 1895 | 134 | 4,224 |
| `jataka-vol3` | H. T. Francis & R. A. Neil | 1897 | 135 | 2,967 |
| `jataka-vol4` | W. H. D. Rouse | 1901 | 71 | 3,033 |
| `jataka-vol5` | H. T. Francis | 1905 | 27 | 2,981 |
| `jataka-tales-vol-1-rhys-davids` | T. W. Rhys Davids | 1880 | 30 | 3,948 |
| `jataka-babbit` | Ellen C. Babbit | 1912 | 22 | 398 |

The first five directories are the scholarly **Cowell edition**,
spanning Volumes 1 through 5 of what was originally a six-volume set
(Volume 6 is not yet in the archive). Each volume's `passages_*.json`
keys passages as `chapter.passage` where each "chapter" is a complete
Jātaka tale; the `chapter_titles` field in `text.json` carries the
canonical Pāli tale names (APANNAKA-JĀTAKA, VANNUPATHA-JĀTAKA,
SERIVANIJA-JĀTAKA, …). **Zero internal id collisions** in any
single translation. **99.99 % overall passage-integrity rate** across
all seven; six at 100 %, one at 99.97 % (Rhys Davids, one passage off
— pre-existing, not from this pass).

The 8,895 figure was a **measurement artifact** in `corpus_audit.py`,
the same kind already documented for the Qur'an. The audit grouped
passages by `text_id` only; all seven directories share `id: jataka`,
so the same `chapter.passage` ids legitimately appearing once per
translation were summed across the bag and counted as collisions.
Phase 8's surgical fix to `corpus_audit.py` (group by `(text_id,
data_file)`, dedup by published file, audit each translation
independently) had already removed the Jātaka from the priority
queue before this restoration began. Verified: it is currently absent
from the queue.

## What was changed

A single small editorial correction, parallel to the Qur'an
auto-ingest variants pass.

### Rhys Davids metadata correction

`jataka-tales-vol-1-rhys-davids/text.json` was an auto-ingest of the
Project Gutenberg edition of T. W. Rhys Davids' 1880 *Buddhist Birth
Stories*. It had inherited a generic auto-ingest template:

| Field | Before | After |
|---|---|---|
| `category` | `Literature` | `Folk Literature` |
| `tags` | `["buddhist", "auto-ingest"]` | `["jataka", "buddhist", "folktale", "rhys-davids", "auto-ingest"]` |
| `source_quality` | `acceptable` | `provisional` |
| `description` | `Jataka tales - Vol 1 (auto-ingested from Project Gutenberg).` | A paragraph noting the front-matter chapters and pointing readers to the Cowell scholarly edition. |

The first ~30 chapters in the file are front-matter (title page,
dedications, preface, "Translator's Introduction. Page", contents
listings, etc.) rather than tales, so `provisional` is the honest
classification. Tales begin further in. The Cowell scholarly edition
is preferred for any citation.

### Nothing else

No passage content modified. No hierarchy declarations changed. No
chapter_titles touched. No tale orderings altered. The Cowell
volumes — Chalmers, Rouse vols 2 & 4, Francis-Neil vol 3, Francis
vol 5 — are untouched because they are already in edition-quality
shape: schema-valid, no internal collisions, proper Pāli tale names
in `chapter_titles`, narrative cadence preserved at the passage
level. Babbit's metadata was already accurate (`category: Folk
Literature`, proper tags, `source_quality: clean`) and was not
touched.

## What was preserved

- Every byte of every Jātaka passage in every translation.
- The 547-tale narrative ordering, as represented in our seven
  available volumes (516 tales in the Cowell five plus the Rhys
  Davids and Babbit overlapping selections).
- The verse/prose rhythm: gathas survive as discrete short
  passages; prose framework as longer paragraph passages. Sampled
  across the Apannaka-jātaka (vol 1, tale 1), the Sigala-jātaka
  (vol 2, tale 1), and the Kimchanda-jātaka (vol 5, tale 1) — all
  read with their canonical opening formula ("This discourse
  regarding Truth was delivered by the Blessed One…"), their
  embedded gathas, and their tale-end markers intact.
- Each translator's identity and idiom, distinct across the five
  Cowell volumes plus Rhys Davids and Babbit.
- The canonical Pāli tale names in each Cowell volume's
  `chapter_titles`.
- Per-volume narrative cadence — long form in Vol 5 (the
  Mahā-nipāta range), shorter form in Vol 1 (the Eka-nipāta).

## Integrity verification

After the changes:

| Check | Result |
|---|---:|
| Jātaka passage subsequence proof (7 targets) | **99.99 %** (18,484 / 18,485) |
| Translations failing 95 % | **0** |
| Translations at 100 % | 6 |
| Translations at 99 %+ | 7 |
| Internal duplicate-id count, any single translation | **0** |
| Position on the corpus_audit priority queue | not in queue |

## Manual editorial observations

Findings from reading samples across the volumes — the kind of
observations a steward would record so they are not re-discovered:

- **Frame structure is intact.** Each tale opens with the
  paccuppanna-vatthu (story of the present, with the Buddha
  speaking at Jetavana or another monastery), proceeds to the
  atīta-vatthu (story of the past), interleaves the gātha (canonical
  Pāli verse, in English translation), and resolves with the
  samodhāna (identification of past actors with present ones). The
  Cowell parser preserved this structure as a sequence of passages
  within each chapter. Chapter boundaries align with tale boundaries.
- **Verse vs prose.** The gāthās appear as standalone short
  passages — typically a single quatrain — visually distinguishable
  from the surrounding prose by length and cadence. Example, from
  Sigala-jātaka (vol 2, tale 1, passage 1.15): *"Who rashly
  undertakes an enterprise, / Not counting all the issue may arise,
  / Like one who burns his mouth in eating food / Falls victim to
  the plans he did devise."* The line breaks in the source HTML are
  reflected in the parsed passages.
- **Embedded narratives.** Some longer tales contain stories within
  stories (the Bodhisatta tells a tale within the past-life tale).
  These are not given their own chapter level — they remain inside
  the parent tale's passage sequence — which is faithful to the
  Cowell edition's typographic decisions.
- **Tale-end markers.** Each chapter's last passage carries a
  bracketed marker like `[j002]`, `[j153]`. These are SacredTexts.com
  internal anchors used in their HTML to link to "next tale." They
  are preserved as raw text; harmless and useful as canonical-tale
  identifiers if anyone wants to cross-reference the SacredTexts
  online edition.
- **Volume boundary footers.** A few volume-final passages carry a
  SacredTexts source footer ("…at sacred-texts.com"). Cosmetic; not
  corrupting.
- **Volumes 2 and 5 do not align cleanly with the canonical
  150-tale-per-book division.** Vol 2 has 134 chapters; Vol 5 has 27.
  This reflects the Cowell volumes' actual page-count division
  rather than the Pāli-canonical nipāta division. Each "chapter" is
  still a tale; only the volume membership of each tale is
  Cowell's editorial choice, not the corpus's natural shape.

## Future commentary readiness

Already supported, no further work needed:

- **Tale-level commentary anchors.** Each tale is one chapter (`l1`)
  in its volume's `passages_*.json`. The pair `(translation, l1)`
  uniquely identifies a tale; commentary can attach there cleanly.
- **Verse-level anchors.** Each gāthā passage has its own id; tafsir-
  style commentary at verse level is supported.
- **Cross-tale references.** A tale's title (in `chapter_titles`)
  maps to the canonical Pāli name; canonical references like
  "Sigāla-jātaka" can resolve to either of multiple jātakas of that
  name and any future commentary layer can disambiguate by volume.
- **Frame-element anchors.** Future commentary could distinguish
  paccuppanna-vatthu vs atīta-vatthu vs gātha vs samodhāna at the
  passage level if the steward chose to tag them. The current
  structure does not enforce that distinction, but neither does it
  prevent adding it later as `passage.frame_element` metadata.
- **Bodhisatta continuity.** The Cowell tales identify the Bodhisatta
  in their samodhāna passages; cross-tale tracking of the
  Bodhisatta's incarnations is a future commentary layer the
  structure already supports.
- **Nikāya parallels and folktale relationships.** Citation-by-tale
  is enough; no structural changes needed.

## Future print-quality possibilities

The Jātaka is a particularly natural fit for print editions —
collections of short, complete narratives — and the data structure
supports several print directions without further work:

- **Per-tale rendering.** A print engine can render each tale as a
  discrete chapter starting with its `chapter_titles` heading. Verse
  passages set as indented quatrains; prose as flowing paragraphs.
- **Themed anthologies.** Tales by topic (kings, animals, kindness,
  cleverness) — selectable by tale title plus future tagging.
- **Bedside-reading editions.** A short tale a day. The Daily Reader
  whitelist already includes selected Jātakas; a print version is
  the same content reformatted.
- **Scholarly editions.** The Cowell volumes were originally typeset
  with the gāthās in italics or smaller font. Future print rendering
  could re-establish that distinction by detecting verse-shaped
  passages.
- **Children's editions.** Babbit's selection is structured for this
  use today; a print extraction would not require any data changes.

None of this is built. None of it is impeded by the current structure.

## Remaining limitations

- **Volume 6 is not in the archive.** Cowell's six-volume edition
  ends with Vol 6 (jātakas 538–547, including the long Vessantara-
  jātaka and the Mahā-Sutasoma-jātaka in their full form). Adding it
  is a separate acquisition task. The archive currently covers ~516
  of the 547 canonical tales.
- **The Rhys Davids variant retains its front-matter chapters.**
  The first ~30 "chapters" are not tales but title pages and
  prefaces. A re-ingest with corrected boundaries would be ideal but
  is beyond this restoration's scope. The Cowell volumes provide the
  canonical content readers should cite from.
- **Babbit's chapter numbering has gaps** (`1, 2, 3, 5, 6, 7, 9, 10,
  11, 12, 14, 16, 17, 18, 19, 21, 23, 25, 26, 28, 30, 32`) — the
  parser identified 22 chapter-shaped sections but the children's
  edition's actual chapter numbering reaches 32. Cosmetic; not
  corrupting.
- **Cross-volume tale numbering is implicit.** A reader citing
  "Jātaka #316" must know that this lives in Vol 3. A future
  enhancement could add `display.tale_offset` metadata per volume
  (e.g., Vol 2 starts at tale 151) so absolute citations resolve
  automatically. Not added in this pass because the volume
  boundaries don't divide the canon cleanly into 150-tale portions
  and asserting an offset would require external verification of
  each volume's tale range.
- **Frame elements are not separately tagged.** Paccuppanna-vatthu,
  atīta-vatthu, gāthā, and samodhāna live in the same flat passage
  sequence. A future commentary layer could surface them
  distinctly.
- **No tafsir / commentary yet.** The structure is ready; the
  commentary content has not been acquired. The Jātaka's traditional
  commentaries (the Jātakaṭṭhakathā) and modern scholarly works
  would attach naturally at the tale level.

## Closing note

Like the Qur'an restoration before it, this turned out to be
preservation work rather than repair work. The Jātaka's data was
already in edition-quality shape; the perceived problem was an audit
metric that has since been corrected. The single small change — a
metadata correction to one auto-ingest variant — is the kind of slow
editorial care this archive is built around: not a sweeping pass,
but one honest paragraph of description added where one was missing.

The narrative tradition is intact. Six volumes of scholarly Pāli
translation, plus a 19th-century English selection and a children's
retelling, all carrying the Buddha's birth-stories with their oral
cadence preserved. The archive is ready to receive a commentary
layer when one is brought in. It is ready to support print editions.
And it is ready to be read.

---

*Snapshot of pre-restoration state preserved at
`logs/_archive/2026-05-jataka-restoration/`. The full text-by-text
condition report covering all 1,091 corpus works is at
`TEXT_CLEANLINESS.md`. The institutional checkpoint that frames this
restoration is `STABILIZATION_EDITION_2026.md`. The first restoration
pass that established this pattern is `QURAN_RESTORATION_2026.md`.*
