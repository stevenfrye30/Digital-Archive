# v106 — Mandukya Upanishad ingestion (Hume 1921)

Mandukya — the single remaining principal Upanishad gap — is now
active in the archive. Acquired from Robert Ernest Hume's *The
Thirteen Principal Upanishads* (Oxford University Press, 1921),
public domain, sourced via the Internet Archive.

## 1. Source identification

| | |
|---|---|
| Title | The Thirteen Principal Upanishads, Translated from the Sanskrit |
| Translator | Robert Ernest Hume (1877–1948) |
| Publisher | Oxford University Press |
| Year | 1921 |
| Source URL | https://archive.org/details/thirteenprincipa00hume |
| Internet Archive id | `thirteenprincipa00hume` |
| Public-domain status | **Confirmed PD in the US** — published 1921, well past the 95-year cutoff (any US work published before 1929 is in the public domain as of the date of this report). Hume died in 1948; even under life+70 jurisdictions the work would enter PD in 2018. No restrictions for archive use. |
| Local cache | `02_raw_sources/Library_/InternetArchive/Hume-1921-Thirteen-Principal-Upanishads.txt` (the IA djvu OCR text, 35,566 lines / ~1.3 MB) |

## 2. Mandukya audit (boundaries + content)

Hume's Mandukya sits at lines 24075–24226 of the OCR text:

| Marker | OCR line | Content |
|---|---:|---|
| Section opening | 24075 | `MANDUKYA UPANISHAD` |
| Subhead | 24077 | The mystic symbolism of the word ‘Om’ |
| Verse 1 | 24084 | `1. Om ! — This syllable is this whole world. …` |
| Verse 12 | 24221 | `12. The fourth is without an element, with which there can be no dealing, the cessation of development, benign, without a second.` |
| Closing rubric | 24225–6 | `Thus Om is the Self (Atman) indeed. He who knows this, with his self enters the Self — yea, he who knows this!` |
| Next section | ~24249 | `SVETASVATARA UPANISHAD` (verifies Mandukya bound) |

**Karika separation:** Hume's edition of Mandukya is the 12-verse
Upanishad **proper, without Gaudapada's Karika commentary**. (Hume
prints the Karika separately in a different OUP volume; the 1921
*Thirteen Principal Upanishads* contains only the Upanishads.) This
matches v105's caution: "Mandukya Karika is NOT the Mandukya
Upanishad." The archive's Mandukya text is the Upanishad alone.

**Verse count: 12** — matches the canonical Mandukya structure.
The closing rubric is preserved at the end of verse 12.

**OCR cleanliness:** Conservative parse strips footnote bodies
(`^[1-9]\s+(In|Either|A|That|This|…)`) that bled into verses
4, 5, 6, 8, 11 in the raw OCR. Inline footnote-reference digits
(small numerals like "1", "2") remain in the text but are
substantively harmless and recognisable as scholarly apparatus.
A future pass could clean those if reading-room typography becomes
a priority.

## 3. Data integration

### New files

| Path | Bytes | Description |
|---|---:|---|
| `03_web_app/data/upanishads-hume-mandukya_hume.json` | 6,081 | 12 passages, hierarchy `[chapter, verse]`, single L1='1' labelled "Mandukya" |
| `03_web_app/data/upanishads-hume-mandukya_hume.json.gz` | 2,248 | gzipped for Pages |
| `03_web_app/data/index.json` | +1 entry | Catalog registration `id=upanishads-hume-mandukya` |
| `03_web_app/data/index.json.gz` | regenerated | |
| `02_raw_sources/Library_/InternetArchive/Hume-1921-Thirteen-Principal-Upanishads.txt` | 1,291,813 | The full IA OCR text (preserved for future principal second-witness extractions) |
| `05_scripts/ingest_hume_mandukya.py` | — | Idempotent ingestion script |
| `05_scripts/_register_hume_mandukya_in_index.py` | — | Catalog-registration script |

### Catalog (index.json) entry

```json
{
  "id": "upanishads-hume-mandukya",
  "title": "The Mandukya Upanishad (Hume translation)",
  "tradition": "Hindu",
  "collection": "sacred",
  "hierarchy": ["chapter", "verse"],
  "data_file": "upanishads-hume-mandukya_hume.json",
  "source": "internetarchive",
  "author": ["Anonymous"],
  "translator": ["Robert Ernest Hume"],
  "year": 1921,
  "translation_label": "Hume translation",
  "translation_short_label": "Hume 1921",
  "quality": "popular",
  "source_summary": "Translated by Robert Ernest Hume in The Thirteen Principal Upanishads (Oxford University Press, 1921). Sourced from Internet Archive identifier `thirteenprincipa00hume`. Public domain in the United States by date of publication. Karika commentary not included — this excerpt is the twelve-verse Mandukya Upanishad proper.",
  "importance_rank": 8
}
```

### Family index changes

```js
TEXT_FAMILIES.upanishads.members += {
  textId: 'upanishads-hume-mandukya',
  role: 'collection',
  note: 'Hume 1921 — Mandukya only (Hume edition of the 13 principals)'
}
```

```js
TEXT_FAMILIES.upanishads.byUpanishad += {
  key: 'mandukya', name: 'Mandukya',
  displayTitle: 'Mandukya Upanishad',
  importance: 'principal', order: 60,
  associatedVeda: 'Atharvaveda',
  vedaSource: 'curated traditional metadata',
  witnesses: [{
    textId: 'upanishads-hume-mandukya', groupKey: '1',
    sourceTitle: 'The Thirteen Principal Upanishads — Hume',
    translator: 'Robert Ernest Hume', year: '1921',
    role: 'primary', routeQuality: 'safe',
    note: "Hume's edition of the 12-verse Mandukya proper; Gaudapada's Karika commentary is not included."
  }]
}
```

```js
MUKTIKA_108[80] /* #81 Māṇḍūkya */ : key changed from null → 'mandukya'
TEXT_FAMILIES.upanishads.principalMissing : [Mandukya] → []
TEXT_FAMILIES.upanishads.byUpanishadInactive : Mandukya entry removed
```

### Count updates

| Metric | Before v106 | After v106 |
|---|---:|---:|
| Active Upanishads in family index | 37 | **38** |
| Principal active | 12 | **13 / 13** |
| Muktikā 108 coverage | 34 / 108 (31%) | **35 / 108 (32%)** |
| Atharvaveda (Muktikā) | 4 / 31 (13%) | **5 / 31 (16%)** |
| Missing principal | 1 (Mandukya) | **0** |
| Missing Muktikā 108 | 74 | **73** |

## 4. Non-destructive guarantee

- **No JSON files merged, rewritten, or deleted.**
  - The six pre-existing Upanishads source files (Müller complete,
    Müller Part 1, Müller Part 2, Johnston, Aiyar Thirty Minor,
    legacy 1900 reprint) are completely untouched.
- **Hume is preserved as its own witness/source.** The new data
  file is a Mandukya-only excerpt from the 1921 Hume edition,
  clearly labelled as such. The full Hume edition's other 12
  principals (Brihadaranyaka, Chandogya, Aitareya, Taittiriya,
  Kena, Katha, Isha, Mundaka, Prasna, Svetasvatara, Maitri,
  Kaushitaki) are **not** added as active witnesses in v106.
- **Mandukya was not synthesised from commentary.** Verified by
  the audit: Hume's Mandukya is the 12-verse Upanishad text proper.

## 5. Family-page behaviour after v106

- **By Veda view** — Mandukya appears as an active principal card
  in the Atharvaveda group; the Atharvaveda count badge updates
  from `4 / 31 in Muktikā 108` to `5 / 31 in Muktikā 108`. The
  dashed-bar "not yet in archive" missing-status card is **gone**.
- **Traditional order view** — Mandukya appears as the 6th
  principal Upanishad (between Mundaka and Taittiriya per Muktikā
  ordering). The collapsed gap disclosure header updates from
  *"34 active · 74 not yet"* to *"35 active · 73 not yet"*.
- **By text view** — Hume 1921 appears in the **Specialised
  collections** section (role `collection`) with its full
  bibliographic credit. Members list grew from 6 to 7.
- **Witness picker** — clicking Mandukya opens the picker with one
  witness card: *"Primary reading witness — The Thirteen Principal
  Upanishads — Hume — Robert Ernest Hume · 1921 — Hume's edition
  of the 12-verse Mandukya proper; Gaudapada's Karika commentary
  is not included."* Click routes via `pendingSection='1'` to the
  reading room at verse 1.

## 6. Future use of Hume

The full IA OCR is cached locally. Hume's edition is a respected
scholarly translation; future passes (v107+) could:

- Activate Hume's other 12 principals as second-witness routes
  alongside the existing Müller witnesses (gives the witness
  picker its first multi-witness Upanishads — readers could
  compare Müller and Hume on Isha, Kena, etc.).
- Re-parse the cached OCR with better footnote-handling for
  cleaner reading-room text.

**v106 does NOT activate the other Hume principals.** That is
intentionally deferred; v106's scope is exactly Mandukya.

## 7. Closing principal-canon status

```
Conservative principal target (13 Upanishads):
  ✓ Isha
  ✓ Kena
  ✓ Katha
  ✓ Prasna
  ✓ Mundaka
  ✓ Mandukya         ← v106 NEW
  ✓ Taittiriya
  ✓ Aitareya
  ✓ Chandogya
  ✓ Brihadaranyaka
  ✓ Svetasvatara
  ✓ Kaushitaki
  ✓ Maitri (Maitrayaniya)
  ─────────────
  13 / 13 active
```

The principal canon is complete. Remaining 73-Upanishad gap is
documented in `reports/v105_upanishads_missing_74_acquisition_plan.md`;
next acquisition priority shifts to Tier 2 (Muktikā Upanishad,
Mahā-Nārāyaṇa, the Sannyāsa cluster via Aiyar 1914).
