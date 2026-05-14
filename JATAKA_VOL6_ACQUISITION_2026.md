# Jātaka Vol 6 — Acquisition and Integration, May 2026

A short note recording the acquisition of Cowell scholarly Jātaka Vol 6
(the final volume), which closes the canonical six-volume set in the
archive. The archive previously held Vols 1–5; the May 2026 Jātaka
restoration pass concluded that the existing data was already at
edition quality and that Vol 6 was the standing acquisition gap.

This pass closes that gap.

---

## Source provenance

**E. B. Cowell & W. H. D. Rouse, eds., *The Jātaka; or, Stories of
the Buddha's Former Births, Vol. VI* (Cambridge: University Press,
1907).** The final volume of the Cambridge Cowell six-volume scholarly
edition, containing the ten tales of the Mahā-nipāta (jātakas
538–547), culminating in the Vessantara-jātaka.

The volume is in the public domain (US copyright expired; Cowell
1903; Rouse 1950; original publication 1907). Provenance is the
Internet Archive scan of the University of California Los Angeles
library copy, item identifier
[`jatakaorstorieso06cowe`](https://archive.org/details/jatakaorstorieso06cowe).
The raw OCR text was downloaded from
`archive.org/download/jatakaorstorieso06cowe/jatakaorstorieso06cowe_djvu.txt`
on 2026-05-14 and saved verbatim to
`02_raw_sources/Library_/Internetarchive/The Jataka - Vol 6_____EB-Cowell & WHD-Rouse (1907).txt`.

Archive.org's metadata confirms the volume's identity in its own
words: *"vol. VI by E. B. Cowell and W. H. D. Rouse, 1907."*

## Why this source, not SacredTexts.com

Vols 1–5 in the archive came from SacredTexts.com, which had hosted
post-OCR cleaned HTML for those volumes (John Bruno Hare's editorial
work over many years). SacredTexts does not host Vol 6. The Internet
Archive scan is the next-most-accessible canonical source.

The cost is OCR noise. Vol 6's raw text contains characteristic OCR
errors that the SacredTexts cleanup process resolved in vols 1–5 but
that survive here: "MtJGA" for "MUGA" (the tail of the M leaking into
the U), "Jdtaka" for "Jātaka" (the long-ā with macron misread),
"\\1M1" for "NIMI", "Sheio" for "Show", running headers like
`No. 547. 247` repeated at every page boundary, library shelf-marks
on the final pages, and so on. This is real OCR drift from a 1907
print page through a scanner-OCR pipeline — not corruption introduced
by this archive.

The honest classification is therefore `source_quality: provisional`
rather than `clean`. The narrative content is faithful; the surface
text shows scan noise. A future stewardship pass — manual post-OCR
cleanup or substitution of a cleaner source if one appears — can
upgrade this to `clean`. Today's ingest is faithful to the source.

## What was added

One new canonical-library directory:

```
01_library/library/texts/sacred/buddhist/jataka-vol6/
├── text.json
└── passages_cowell-rouse-vol6.json
```

The `text.json` matches the schema and shape of `jataka-vol5/`'s
`text.json` exactly: same `id` (`jataka`, the Cowell series id),
same `hierarchy` (`["chapter", "verse"]`), same `category`
(`Folk Literature`), same `tradition` (`Buddhist`), same `display`
shape. Differences are honest:

- `translator: ["E. B. Cowell", "W. H. D. Rouse"]` (vol 6's actual
  translators)
- `source.publisher: "Internet Archive"` (not SacredTexts)
- `source_quality: "provisional"` (not `clean`, per the OCR-noise
  discussion above)
- `description` records the OCR-quality caveat directly
- `tags` adds `cowell`, `rouse`, `maha-nipata`, `vessantara`

The `chapter_titles` field preserves the canonical Pāli tale names
recovered from the OCR — with the OCR artifacts that survive
preserved as found, e.g. `538. MtJGA-PAKKHA JATAKA`. The decision
not to silently "correct" `MtJGA` to `MUGA` is deliberate: the
archive records the OCR as it was scanned. A future cleanup pass
can choose its corrections with explicit confidence; an ingest pass
making them implicitly would be dishonest about the source.

## What was changed in existing volumes

**Nothing.** Vols 1–5 were not modified. No passage content, no
metadata fields, no parser scripts, no chapter_titles. The Cowell
volumes 1–5 remain exactly as they stood after commit `223231b9`.

## Parser

The Vol 6 ingest script lives at
`05_scripts/ingest_jataka_vol6.py`. It follows the same shape as
`05_scripts/reingest_jataka_and_gospel.py`'s parser used for vols
1–5: walk lines, find tale-start markers, capture title from the
next title-bearing line, build paragraphs from consecutive non-blank
content lines, drop running headers / page markers / footnote
references inline.

Vol 6 required two parser refinements relative to the SacredTexts
pattern:

1. **Trailing-punctuation tolerance.** The OCR renders the period
   after `No. N` as a backslash on at least one tale (jātaka 541
   appears as `No.  541\` rather than `No.  541.`). The tale-marker
   regex was widened to accept `[.\\,]` as the closing punctuation,
   not just `.`.

2. **End-of-tales sentinel.** The volume's back matter (INDEX,
   glossary, library shelf-mark pages) follows the Vessantara-jātaka.
   Without a sentinel, the parser would slurp library checkout cards
   ("xq.xx", "V.6", date stamps from circulation slips) into Vessantara's
   passage tail. The parser stops at the first `INDEX.` line and so
   Vessantara ends cleanly at its canonical samodhāna closing —
   *"When the Master had ended this discourse of Vessantara, with its
   thousand stanzas, he identified the Birth: 'At that time,
   Devadatta was Jūjaka…'"*

## Tales acquired

| Tale | Title (as scanned) | Paragraphs |
|---:|---|---:|
| 538 | MtJGA-PAKKHA JATAKA | 222 |
| 539 | MAHAJANAKA-JATAKA | 211 |
| 540 | SAMA-JATAKA | 183 |
| 541 | NIMI-JATAKA | 270 |
| 542 | THE KHANDAHALA-JATAKA | 198 |
| 543 | BHURIDATTA-JATAKA | 416 |
| 544 | MAHANARADAKASSAPA-JATAKA | 136 |
| 545 | VIDHURAPANDITA-JATAKA | 404 |
| 546 | THE MAHA-UMMAGGA-JATAKA | 703 |
| 547 | VESSANTARA-JATAKA | 1,154 |

Total: 10 tales, 3,897 paragraphs, jātakas 538–547 of the canonical
547. With this acquisition, the archive's Cowell set is complete.

## Integrity verification

Passage subsequence proof was re-run against all eight Jātaka
translations in the canonical library after the ingest:

| Translation | Verified |
|---|---:|
| jataka-chalmers-vol1 | 100 % |
| jataka-vol2 (Rouse) | 100 % |
| jataka-vol3 (Francis & Neil) | 100 % |
| jataka-vol4 (Rouse) | 100 % |
| jataka-vol5 (Francis) | 100 % |
| **jataka-vol6 (Cowell & Rouse) — new** | **99.97 %** (3,711 / 3,712) |
| jataka-tales-vol-1-rhys-davids | 99.97 % (pre-existing) |
| jataka-babbit | 100 % |

Overall pass rate across all eight: **99.99 %**. Zero translations
below the 95 % threshold. Vol 6's one unverified passage is a
trailing footer fragment (`J. VI. ao` — a printer's signature on the
final page) that fails normalization-equivalence with the raw text;
not a corruption, just a passage that should likely have been
filtered. Acceptable for `provisional` quality; a future cleanup
pass can address it.

## Manual editorial check

Sampled across the volume:

- **Tale 538 (Muga-Pakkha) opening** — *"' Sheio no intelligence' etc.
  This story the Master told at Jatavana concerning the great
  renunciation. One day the Brethren seated in the Hall of Truth were
  discussing the praises of the Blessed One's great renunciation."*
  Canonical opening pattern intact; "Sheio" is an OCR error for "Show"
  (the prince Temiya's silence-vow framing) but preserved as found.
- **Tale 541 (Nimi) opening** — *"' Lo these grey hairs' etc. This
  story the Master told while dwelling in Makhadeva's mango park, near
  Mithila, about a smile."* Canonical opening pattern intact.
- **Tale 547 (Vessantara) opening** — *"' Ten boons,' etc. This story
  the Master told while dwelling near Kapilavatthu in the Banyan Grove,
  about a shower of rain."* Canonical opening.
- **Tale 547 closing** — the canonical samodhāna *"When the Master had
  ended this discourse of Vessantara, with its thousand stanzas, he
  identified the Birth: 'At that time, Devadatta was Jūjaka…'"*
  preserved at 10.1152, two passages before the file's hard end.

The Mahā-nipāta narrative cadence is preserved. Verse passages remain
short and distinct from prose. Tale boundaries are clean.

## Provisional notes

These are the OCR-driven imperfections in Vol 6 that future
stewardship may want to address. None of them prevent reading; all
of them are flagged here so a future editor knows what to find.

- **OCR character substitutions** scattered through the prose:
  `MtJGA` ↔ `MUGA`, `Jdtaka` ↔ `Jātaka`, `Sheio` ↔ `Show`,
  `consort` ↔ `oonsort` etc. These are systematic enough that a
  pattern-based pass (with a careful diff review) could clear most
  of them.
- **Footnote markers** appear inline as bare `^` and `-` characters
  where the original page had superscript markers. The parser's
  inline cleanup did not strip them all.
- **Page-bracket markers** like `[1]`, `[479]` are stripped inline,
  but a small number survive in fragmented passages.
- **Italic markers** (the original used italics for Pāli quotations
  and proper names) are gone in OCR.

## What this enables

The Cowell six-volume scholarly Jātaka is now complete in the
archive:

- **Vol 1** — Chalmers (1895), jātakas 1–150 ✓
- **Vol 2** — Rouse (1895), jātakas 151–284 ✓
- **Vol 3** — Francis & Neil (1897), jātakas 285–419 ✓
- **Vol 4** — Rouse (1901), jātakas 420–490 ✓
- **Vol 5** — Francis (1905), jātakas 491–537 ✓
- **Vol 6** — Cowell & Rouse (1907), jātakas 538–547 ✓ **(new)**

(Tale-range numbers are approximate; the Cowell volumes do not divide
the canon by uniform 150-tale boundaries.)

Future work that this completion enables, but does *not* require:

- A unified Cowell index spanning all six volumes (cross-volume tale
  numbering metadata).
- A Vessantara reading edition. Vessantara is the canonical
  culmination of the Buddha's bodhisattva career; with Vol 6 in
  place, a stand-alone print extraction is now possible without an
  external acquisition.
- A Mahā-nipāta thematic anthology. The ten long Mahā-nipāta tales
  (538–547) form a coherent reading collection on the perfection of
  generosity (*dāna-pāramitā*) and the bodhisattva path.
- Commentary infrastructure attached at the tale level, when a
  commentary layer is brought in.

None of these are built. None of them are impeded.

## Remaining limitations

- **Vol 6 is OCR-quality, not SacredTexts-quality.** Honestly tagged
  `source_quality: provisional`.
- **One footer-fragment passage fails integrity** verification (out of
  3,712). Minor.
- **No commentary, no tafsir, no Jātakaṭṭhakathā in the archive yet.**
  Acquisition tasks for the future.
- **Cross-volume tale numbering is still implicit.** A reader citing
  "jātaka 547" must know it lives in Vol 6. A future `tale_offset` per
  volume could resolve absolute citations.
- **No diacritic restoration in tale titles.** "MtJGA-PAKKHA JATAKA"
  stays as scanned. A future cleanup pass can replace OCR'd characters
  with proper Pāli diacritics where confidence is high.

## Closing note

The Cowell scholarly six-volume Jātaka is now closed in the archive.
The acquisition was straightforward: identify the historically
appropriate source (the 1907 Cambridge edition), verify the OCR scan's
provenance (UCLA library copy via Internet Archive), download
verbatim, parse with the same pattern as vols 1–5 (with two small
adjustments for OCR quirks), and integrate without modifying any
existing volume.

The result is honestly imperfect — the OCR shows its origins — but
faithfully complete. The Buddha's birth-stories now read in this
archive from Apannaka (jātaka 1, vol 1) to Vessantara (jātaka 547,
vol 6) without a gap. Future stewardship can refine the OCR. The
acquisition is done.

---

*Pre-acquisition snapshot of the existing Jātaka directories was
preserved at `logs/_archive/2026-05-jataka-restoration/` during the
May 2026 restoration pass. The current full text-by-text condition
report is `TEXT_CLEANLINESS.md`. The companion restoration document
that established the editorial pattern is
`JATAKA_RESTORATION_2026.md`.*
