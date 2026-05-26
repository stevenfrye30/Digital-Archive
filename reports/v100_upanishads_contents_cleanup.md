# v100 — Upanishads contents cleanup

Cleanup pass on the Upanishads-family specific text contents pages.
Built on top of the v99 family/by-Upanishad system; no source files
were merged, rewritten, or deleted.

## What changed

### Family page (Hindu › The Upanishads)

| Before (v99) | After (v100) |
|---|---|
| Description led with bibliographic framing | Description leads with reader framing: *"Browse the family either by individual Upanishad or by collection / edition. Each route preserves its source witness."* |
| Section order: Browse by collection → Browse by Upanishad | Section order: **Browse by Upanishad → Browse by collection** (reader-facing route first) |
| By-Upanishad cards rendered a stray `·` glyph in the star slot | Glyph removed; the card now reads name + italic "Upanishad" + credit line cleanly |

### Per-record contents pages

A new presentation config — `TEXT_CONTENTS_OVERRIDES` — lets a
record opt into four knobs:

- `hideFrontMatter` — suppress the ✦ Front Matter button when the
  fm passages are editorial boilerplate rather than meaningful
  reader entry
- `titleOverride` — replace the display title without touching the
  source data
- `entries[]` — replace the L1 key list with a curated set of
  cleanly-routable entries (each with its display name)
- `note` — italic prose block above the contents grid, classifying
  the record honestly (source-volume / thematic / legacy)

All overrides are presentation-only; source files are unchanged.

### Per-Upanishads-member changes

| Record | mode | hideFrontMatter | entries[] | titleOverride | Note rendered |
|--------|------|:---:|:---:|---|---|
| `upanishads` (Müller — complete) | clean-upanishad-list | ✓ | – | – | "Müller’s complete merged translation. The contents below are the ten principal Upanishads in source order. Each entry routes to the start of that Upanishad." |
| `upanishads-30-minor-aiyar` (Aiyar — Thirty Minor) | minor-upanishad-list | ✓ | **10** | – | "Aiyar’s collection of thirty lesser Upanishads. The entries below are the Upanishads whose internal sectioning is clean enough for direct routing. Some other Upanishads named in the table of contents have their text split across following sub-section keys — they remain reachable by reading through the collection, but are not yet cleanly indexed individually." |
| `upanishads-muller-part1` (SBE Vol. I) | source-volume | ✓ | – | – | "Source-volume witness — Sacred Books of the East, Vol. I (Müller, 1879). The internal divisions below are the source file’s own sectioning (with editorial chrome). For clean per-Upanishad reading, open *The Upanishads — Müller, complete* from the family page." |
| `upanishads-muller-part2` (SBE Vol. XV) | source-volume | ✓ | – | – | "Source-volume witness — Sacred Books of the East, Vol. XV (Müller, 1884). The internal divisions below are the source file’s own sectioning (with editorial chrome). For clean per-Upanishad reading, open *The Upanishads — Müller, complete* from the family page." |
| `upanishads-johnson` (Johnston) | thematic | – | – | – | "This edition is organised thematically by Charles Johnston, not as a simple Upanishad-by-Upanishad sequence. Section labels reflect the translator’s own structure." |
| `the-upanishads-max-muller-1879` (legacy 1900 reprint) | legacy | ✓ | – | **"The Upanishads — legacy reprint"** | "Legacy duplicate / source-ingestion record (1900 reprint of Müller, 1879/1884). For the clean reader-facing collection, use *The Upanishads — Müller, complete* from the family page. This record is preserved for scholarly continuity." |

## Front Matter buttons hidden

For Upanishads-family records, the fm passages are scaffolding
(SBE preface, translator notes, page boilerplate) rather than
reader-facing text. Hidden on:

- `upanishads` (1 fm passage)
- `upanishads-30-minor-aiyar` (11 fm)
- `upanishads-muller-part1` (294 fm)
- `upanishads-muller-part2` (161 fm)
- `the-upanishads-max-muller-1879` (307 fm)

Kept on `upanishads-johnson` (15 fm) — Johnston's preface, foreword,
and "To G. W. Russell" are arguably reader-facing material distinct
from the translation proper.

The fm passages themselves remain in the data and remain reachable
by direct URL (`?text=...&p=fm.X`).

## Cleanly listed minor Upanishads (Aiyar)

After the override, the Thirty Minor contents page now shows exactly
these 10 entries instead of 70 noisy "Chapter N — Adhyaya I" buttons:

1. Sarvasara Upanishad
2. Niralamba Upanishad
3. Adhyatma Upanishad
4. Vajrasuchi Upanishad
5. Garbha Upanishad
6. Tarasara Upanishad
7. Yogatattva Upanishad
8. Dhyanabindu Upanishad
9. Hamsa Upanishad
10. Nadabindu Upanishad

## Minor Upanishads still uncertain / needing parser repair

These are named in Aiyar's table of contents but their internal
sectioning is uneven (very small passage counts at the title key,
content spread across following Adhyaya / Khanda L1 keys). They
remain reachable by opening the Thirty Minor collection and reading
through, but are not yet per-Upanishad routable:

- Maitreya
- Kaivalya
- Amrtabindu
- Atmabodha
- Skanda
- Brahmopanishad
- S'Ariraka
- Narayana
- Kalisantarana
- Bhikshuka
- Amrtanada
- Upadeśā I–IX (Sariraka-Brahmana-Upanishad?)

A future pass could re-parse the source TXT to recover Upanishad-
boundary metadata; until then the conservative override is the
correct stance.

## What was NOT touched

- No JSON files were merged, rewritten, or deleted.
- No fm passages were removed from the data.
- No translation labels or per-text bibliographic credit was changed.
- The Müller Part 1 / Part 2 records remain fully readable through
  their own contents page; the note simply points readers to the
  cleaner Müller complete for per-Upanishad navigation.
- The legacy 1900 reprint remains accessible; only its display
  title is cosmetically overridden.

## Verification

- Family page: Browse by Upanishad section appears first; no stray
  dot glyphs on cards; source credit visible on every card.
- Müller complete contents: 10 principal Upanishad buttons, in
  source order (Chandogya · Kena · Kaushitaki · Isha · Katha ·
  Mundaka · Taittiriya · Brihadaranyaka · Svetasvatara · Prasna),
  no Front Matter button, with the clean-list note above.
- Aiyar Thirty Minor contents: 10 minor Upanishad buttons only,
  with the "uneven internal sectioning" note above.
- Müller Part 1 / Part 2: contents shown with source-volume note
  pointing back to Müller complete; Front Matter hidden.
- Johnston: contents shown with thematic note.
- Legacy 1900: title now reads "The Upanishads — legacy reprint";
  Front Matter hidden; legacy note rendered.
- Bible / Tao / Gita / Iliad / Odyssey / etc.: contents pages
  unchanged (no overrides registered for them).
- Shelf / category pages: scroll behaviour unchanged.
- Reading room: scroll behaviour unchanged; back-button routing
  to the family page unchanged.
