# v101 — Upanishads index architecture (witness picker)

The Upanishads family page now defaults to a reader-facing index:
the user picks an Upanishad first, then picks a witness/edition.
No source files merged, rewritten, or deleted.

## Final index structure

Each Upanishad is described by:

```js
{
  key, name, displayTitle, importance, order,
  witnesses: [
    { textId, groupKey, sourceTitle, translator, year,
      role, routeQuality, note? }
  ]
}
```

- `routeQuality` is `safe` (the source's L1 key is the Upanishad's
  whole content) or `safe-start` (the source's L1 key is the
  Upanishad's title; content continues across following sub-section
  L1 keys until the next named Upanishad).
- Only `safe` and `safe-start` witnesses are rendered as active
  cards. Anything else lives in `byUpanishadInactive` and is
  surfaced as a quiet collapsible disclosure.

## Active Upanishads (21 total)

### Principal Upanishads (10)

| order | Upanishad | Witnesses |
|---:|---|---|
| 10  | Isha           | Müller complete · 1879 (primary, safe) |
| 20  | Kena           | Müller complete · 1879 (primary, safe) |
| 30  | Katha          | Müller complete · 1884 (primary, safe) |
| 40  | Prasna         | Müller complete · 1884 (primary, safe) |
| 50  | Mundaka        | Müller complete · 1884 (primary, safe) |
| 70  | Taittiriya     | Müller complete · 1884 (primary, safe) |
| 90  | Chandogya      | Müller complete · 1879 (primary, safe) |
| 100 | Brihadaranyaka | Müller complete · 1884 (primary, safe) |
| 110 | Svetasvatara   | Müller complete · 1884 (primary, safe) |
| 120 | Kaushitaki     | Müller complete · 1879 (primary, safe) |

(Order positions 60 and 80 are reserved for Mandukya and Aitareya
respectively; both are listed under inactive below.)

### Minor Upanishads (11) — Aiyar, Thirty Minor (1914)

| order | Upanishad | Aiyar L1 | Route quality |
|---:|---|:---:|---|
| 210 | Maitreya       | 6   | safe-start |
| 220 | Sarvasara      | 4   | safe |
| 230 | Niralamba      | 5   | safe |
| 240 | Kaivalya       | 9   | safe-start |
| 250 | Amrtabindu     | 10  | safe-start |
| 260 | Atmabodha      | 11  | safe-start |
| 270 | Skanda         | 12  | safe-start |
| 280 | Adhyatma       | 17  | safe |
| 290 | Brahmopanishad | 34  | safe-start |
| 300 | Vajrasuchi     | 35  | safe |
| 310 | S'Ariraka      | 36  | safe-start |
| 320 | Garbha         | 37  | safe |
| 330 | Tarasara       | 38  | safe |
| 340 | Narayana       | 39  | safe-start |
| 350 | Kalisantarana  | 40  | safe-start |
| 360 | Bhikshuka      | 41  | safe-start |
| 370 | Yogatattva     | 55  | safe |
| 380 | Dhyanabindu    | 56  | safe |
| 390 | Hamsa          | 57  | safe |
| 400 | Amrtanada      | 58  | safe-start |
| 410 | Nadabindu      | 68  | safe |

(That's 21 minor entries — the total active set is 10 principal +
21 minor = **31 Upanishads** the reader can browse and route into.)

## Multiple-witness Upanishads

None yet. Every active Upanishad currently has exactly one safe
witness (Müller complete for principal; Aiyar for minor). The
witness picker is still always shown for visual / source-credit
consistency — the user sees who they're reading and from which
edition before entering the reading room.

When Johnston's edition or the Müller Parts get re-parsed in a
future pass, additional witnesses can be appended to the `witnesses`
array without any UI change.

## Inactive Upanishads (named but not yet routable)

Surfaced as a collapsed `<details>` block beneath the active grid
so the user can see they're not silently omitted.

### Mandukya
**Reason:** Not found as a separately-keyed text in any audited
source file in this archive. (Müller's complete merge does not
surface it; Aiyar's Thirty Minor does not include it.) Acquiring an
edition or re-parsing the source to surface Mandukya is a future
ingestion concern.

### Aitareya
**Reason:** Present in Müller Part 1 (`Aitareya-Aranyaka`,
including the Aitareya Upanishad) but interleaved with
Khandogya / Kaushitaki / Vagasaneyi-Samhita at the same source L1
key. Sub-key routing requires parser repair before an individual
entry-point can be exposed.

### Upadeśā I–IX (Aiyar L1=42–50)
**Reason:** Nine sub-Brahmana "Upadeśā" sections in Aiyar without
a clean `Xxx-Upanishad` boundary; cannot be safely surfaced as
separate Upanishads without parser repair.

## Witness picker

Inline within the family page (same browse / `body.on-shelf-page`
scaffold, so it scrolls and shares breadcrumb chrome):

```
Home › Religion › Hindu › The Upanishads › Kena Upanishad

[← All Upanishads]

Available witnesses for the Kena Upanishad. Each route preserves
its source credit.

┌──────────────────────────────────────────────────────┐
│  PRIMARY READING WITNESS                              │
│  The Upanishads — Müller, complete                    │
│  F. Max Müller · 1879                                 │
└──────────────────────────────────────────────────────┘
```

Click → `openUpanishadAt(textId, groupKey)` → `pendingSection` →
`loadText` → reading room at the right section. Back returns to
the family page via `browseTextFamily(familyId)`.

## Family page section order

1. **Browse by Upanishad** (default; reader-facing)
   - Principal Upanishads grid
   - Minor Upanishads grid
   - Inactive disclosure
2. **Browse by collection** (bibliographic / source)
   - Primary collections, Specialised collections, Volumes and
     parts, Legacy / duplicate records (unchanged from v98/v100)

## Aiyar collection note

Tightened from v100. No longer apologetic; now reads:
*"Aiyar's collection of thirty lesser Upanishads. For the organised
by-Upanishad index across all sources, open The Upanishads family
page (Hindu shelf)."*

## What was NOT touched

- No JSON files were merged, rewritten, or deleted.
- No source-text passages, fm flags, or chapter_titles were modified.
- The Müller Parts, Johnson edition, and legacy 1900 reprint remain
  fully accessible via Browse by collection.
- Every active witness card credits translator + edition + year
  before routing.
