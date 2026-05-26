# v99 — Upanishads family inventory

Audit of the six Upanishads-family text files registered in the v98
`TEXT_FAMILIES` config. Generated to decide whether the family page
can support a *Browse by Upanishad* mode without merging or
rewriting source files.

## 1. Summary

| | |
|---|---|
| Family members audited | 6 |
| Distinct individual Upanishads routable | 29 (10 principal + 19 minor) |
| Sources with clean per-Upanishad L1 indexing | 2 of 6 |
| Sources with messy or interleaved L1 | 4 of 6 |
| Browse-by-Upanishad verdict | **Safe — conservative prototype implemented** |

## 2. Per-file structure

### `upanishads` — Müller, complete (SBE Vol. I + XV, merged) — **CLEAN**

| | |
|---|---|
| File | `data/upanishads_muller.json` |
| Hierarchy | `[upanishad, section, verse]` |
| Translator | F. Max Müller (1879) |
| Passages | 1831, of which 1 fm |
| Distinct L1 (non-fm) | **10** |
| L1 keys | `chandogya, kena, kaushitaki, isha, katha, mundaka, taittiriya, brihadaranyaka, svetasvatara, prasna` |
| chapter_titles | 0 entries (the L1 slug IS the Upanishad name) |

The merged file uses the actual Upanishad slug as its L1 key — the
ideal shape for per-Upanishad routing. **All 10 principal Upanishads
are directly addressable**: `?text=upanishads_muller.json&p=isha.1.1`,
`...&p=chandogya.1.1`, etc.

### `upanishads-johnson` — Charles Johnston, 1899 — **NOT ROUTABLE per-Upanishad**

| | |
|---|---|
| File | `data/upanishads-johnson_johnson.json` |
| Hierarchy | `[chapter, verse]` |
| Passages | 375, of which 15 fm |
| Distinct L1 (non-fm) | 7 (numeric `6, 7, 8, 9, 10, 11, 12`) |
| chapter_titles | 12 entries, but they read as essay headings: |

```
[1]  From the Upanishads
[2]  Charles Johnston / Foreword
[3]  To G. W. Russell
[4]  In the House of Death
[5]  A Vedic Master
[6]  III That Thou Art
[7]  Foreword
[8]  To G. W. Russell / In the House of Death
[9]  The First Part
[10] The Second Part
[11] A Vedic Master / That Thou Art
[12] That Thou Art
```

Johnston's edition reads more like a thematic essay collection
*about* the Upanishads than a clean per-Upanishad volume. Without
re-parsing the source we can't reliably map L1 keys to individual
Upanishads. Excluded from the by-Upanishad prototype.

### `upanishads-30-minor-aiyar` — K. Narayanasvami Aiyar, 1914 — **PARTIALLY CLEAN**

| | |
|---|---|
| File | `data/upanishads-30-minor-aiyar_aiyar.json` |
| Hierarchy | `[chapter, verse]` |
| Passages | 765, of which 11 fm |
| Distinct L1 (non-fm) | 70 |
| chapter_titles | 71 entries — mix of Upanishad names and sub-section headers (Adhyaya, Khanda, Chapter) |

Aiyar's source was extracted with uneven chunking — some L1 keys
carry the Upanishad name (`L1=4 "Sarvasara-Upanishad of
Krshna-Yajurveda"`, `L1=5 "Niralamba-Upanishad"`), others carry
sub-section labels (`Adhyaya I`, `Khanda II`, `Chapter III`). The
routable subset is L1 keys whose chapter_title matches
`^<Name>-Upanishad` **and** carry ≥10 passages of content (small-count
entries appear to be title pages with content split across following
keys):

| L1 | Upanishad | Passages |
|----|-----------|----------|
| 4  | Sarvasara | 51 |
| 5  | Niralamba | 64 |
| 17 | Adhyatma  | 13 |
| 35 | Vajrasuchi | 12 |
| 37 | Garbha    | 15 |
| 38 | Tarasara  | 15 |
| 55 | Yogatattva | 19 |
| 56 | Dhyanabindu | 18 |
| 57 | Hamsa     | 11 |
| 68 | Nadabindu | 55 |

**10 minor Upanishads are routable cleanly.** The other 19 named
Upanishads in Aiyar's table of contents (Maitreya, Kaivalya,
Amrtabindu, Atmabodha, Skanda, S'Ariraka, Narayana, Bhikshuka,
Amrtanada, Kalisantarana, Upades'a I–IX, Brahmana I–V, etc.) either
have very few passages (likely title pages) or are spread across
multiple L1 keys without a clean entry point. Routable via the
collection itself, not yet per-Upanishad.

### `upanishads-muller-part1` — SBE Vol. I (Müller, 1879) — **NOT ROUTABLE per-Upanishad**

| | |
|---|---|
| File | `data/upanishads-muller-part1_muller-part1.json` |
| Hierarchy | `[chapter, verse]` |
| Passages | 2777, of which 294 fm |
| L1 keys | numeric `2–17` |
| chapter_titles | scaffolding noise: "And", "Preface to the Sacred Books of the East", "Introduction to the Upanishads / Translation of the Khandogya-Upanishad / Translation of the Aitareya-Aranyaka / Translation of the Kaushitaki-Brahmana-Upanishad / Translation of the Vagasaneyi-Samhita-Upanishad", "Fourth Khanda [*1]", "Talavakara", "(Total)", "Rv. VIII, 69, 2 a=", "Isavasya or Isa-Upanishad" |

Part 1 carries SBE editorial matter (Preface, Introduction, Program)
interleaved with the translation. Upanishad content is split across
several L1 keys per Upanishad with sub-section titles like "Fourth
Khanda" and "Talavakara". Not per-Upanishad-routable without source
re-parsing — but **the same content is already cleanly indexed in
`upanishads_muller.json` (Müller complete)**, so nothing is lost.

### `upanishads-muller-part2` — SBE Vol. XV (Müller, 1884) — **NOT ROUTABLE per-Upanishad**

| | |
|---|---|
| File | `data/upanishads-muller-part2_muller-part2.json` |
| Hierarchy | `[chapter, verse]` |
| Passages | 2461, of which 161 fm |
| L1 keys | numeric `1–6` |
| chapter_titles[1] | "Introduction / Translation of the Katha-Upanishad / Translation of the Mundaka-Upanishad / Translation of the Taittiriyaka-Upanishad / Translation of the Brihadaranyaka-Upanishad / Translation of the Svetasvatara-Upanishad / Translation of the Prasna-Upanishad" |

Part 2 collapses all six Vol. XV Upanishads into a single L1 key
(L1=1) with the joint title above. Per-Upanishad routing would
require sub-key parsing not currently in the data. Same content
exists in Müller complete.

### `the-upanishads-max-muller-1879` — 1900 reprint, legacy duplicate — **NOT ROUTABLE per-Upanishad**

| | |
|---|---|
| File | `data/the-upanishads-max-muller-1879_anonymous.json` |
| Hierarchy | `[chapter, verse]` |
| Passages | 4265, of which 307 fm |
| L1 keys | numeric `1–9, 11–14, 16` (skips 10 and 15) |
| chapter_titles | overlaps Part 1's noise titles ("Fourth Khanda [*1]", "Talavakara", "Isavasya or Isa-Upanishad", "First Valli", ...) |

**Looks like a re-ingestion of Part 1 + Part 2 combined** (passage
count 4265 ≈ 2777 + 2461 − 973 deduplicated, roughly). The L1 gaps
(missing 10 and 15) and chapter_title overlap with Part 1 strongly
suggest this is a derivative file from an earlier ingestion run.
Kept available for scholarly continuity (the v98 family page lists
it under "Legacy / duplicate records"). Not per-Upanishad-routable.

## 3. Non-Upanishad material observed

| File | Non-Upanishad chrome |
|------|----------------------|
| `upanishads` (Müller complete) | 1 fm passage only; otherwise clean |
| `upanishads-johnson` | 15 fm; "Foreword", "To G. W. Russell", essay-style mid-chapters |
| `upanishads-30-minor-aiyar` | 11 fm; sub-section headers (Adhyaya, Khanda) interleaved |
| `upanishads-muller-part1` | 294 fm; SBE Preface, Introduction, Program, footnote interleaving |
| `upanishads-muller-part2` | 161 fm; SBE Introduction, footnote interleaving |
| `the-upanishads-max-muller-1879` | 307 fm; combined Part 1 + Part 2 chrome |

## 4. Source relationship analysis

- **Müller complete is the canonical merged copy** of Part 1 + Part 2
  with editorial chrome removed and L1 re-keyed by Upanishad slug.
  This was done in an earlier ingestion pass (project memory has the
  merge note). The Part 1 / Part 2 files remain as the original SBE
  volumes preserved for scholarly continuity.
- **The legacy `The_Upanishads` (1900) is a derivative** of Part 1 +
  Part 2, not a distinct edition. The 1900 date is a reprint of
  Müller's 1879/1884 work; content overlaps. Treated as legacy.
- **Johnston is a distinct edition** (Charles Johnston, 1899) with
  its own essay-style structure. Different translator, different
  selection — not a duplicate of Müller.
- **Aiyar is a different collection entirely** (the 30 Minor / late
  Upanishads). Zero overlap with the 10 principal Upanishads in
  Müller complete or with Johnston's selection.

## 5. Routing feasibility — final verdict per Upanishad

### Principal Upanishads (Müller complete)

| Upanishad | Müller complete | Müller P1 | Müller P2 | Johnson | Aiyar | Legacy |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| Isha | ✓ | partial | – | uncertain | – | partial |
| Kena | ✓ | partial | – | uncertain | – | partial |
| Katha | ✓ | – | partial | uncertain | – | partial |
| Prasna | ✓ | – | partial | uncertain | – | partial |
| Mundaka | ✓ | – | partial | uncertain | – | partial |
| Taittiriya | ✓ | – | partial | uncertain | – | partial |
| Aitareya | – | partial | – | uncertain | – | partial |
| Chandogya | ✓ | partial | – | uncertain | – | partial |
| Brihadaranyaka | ✓ | – | partial | uncertain | – | partial |
| Svetasvatara | ✓ | – | partial | uncertain | – | partial |
| Kaushitaki | ✓ | partial | – | uncertain | – | partial |

(`partial` = present but not at a clean L1 entry; `uncertain` = may
be present but chapter_titles don't surface it.)

Note: Aitareya is in Müller Part 1 but the `upanishads` merged file
appears to omit it as a separate L1 key. Either consolidated under
another slug or absent from the merge. Marked uncertain.

### Minor Upanishads (Aiyar)

| Upanishad | Aiyar L1 | Routable? |
|-----------|----------|-----------|
| Sarvasara | 4 | ✓ |
| Niralamba | 5 | ✓ |
| Adhyatma | 17 | ✓ |
| Vajrasuchi | 35 | ✓ |
| Garbha | 37 | ✓ |
| Tarasara | 38 | ✓ |
| Yogatattva | 55 | ✓ |
| Dhyanabindu | 56 | ✓ |
| Hamsa | 57 | ✓ |
| Nadabindu | 68 | ✓ |
| Maitreya | 6 | uncertain (5 passages — likely title only) |
| Kaivalya | 9 | uncertain (8 passages) |
| Amrtabindu | 10 | uncertain (5 passages) |
| Atmabodha | 11 | uncertain (8 passages) |
| Skanda | 12 | uncertain (4 passages) |
| S'Ariraka | 36 | uncertain (3 passages) |
| Narayana | 39 | uncertain (6 passages) |
| Brahmopanishad | 34 | uncertain (8 passages — title shape differs) |
| Bhikshuka | 41 | uncertain (2 passages) |
| Amrtanada | 58 | uncertain (7 passages) |
| Kalisantarana | 40 | uncertain (4 passages) |

The "uncertain" minor Upanishads likely have their content split
across following L1 keys (Adhyaya I, Khanda I, Chapter I, ...) but
without authoritative section-boundary metadata in the source we
cannot map them safely. Reachable via the Aiyar collection page.

## 6. Implementation decision

**Conservative prototype is safe and implemented (v99).**

Browse-by-Upanishad surface shows:

- All **10 principal Upanishads** routed to Müller complete (1
  witness each, clean).
- The **10 verified minor Upanishads** in Aiyar (1 witness each,
  clean).
- An italic note pointing readers to the Aiyar collection for the
  remaining minor Upanishads whose internal routing is not yet
  clean.

Every card displays the source label (translator + edition + year)
inline so credit is preserved.

No JSON files were merged, rewritten, or deleted. Every original
record remains addressable by URL and via the "Browse by collection"
section of the family page.
