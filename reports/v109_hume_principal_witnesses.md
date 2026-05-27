# v109 — Hume 1921 second-witness layer for the 13 principal Upanishads

Hume's *The Thirteen Principal Upanishads* (OUP 1921, public domain
in the US) is now ingested in full and routed as a second witness on
every principal Upanishad. The v106 Mandukya-only excerpt has been
migrated: Mandukya now routes through the unified Hume source,
alongside the other 12 principals. Müller remains the primary
witness everywhere he covers; readers can now compare two
translations on every principal Upanishad in the archive.

## 1. Boundary audit (12 newly added + 1 verified)

For each of the 13 principals, the audit identified:

| Upanishad | Heading line | Verse-1 line | End line | Notes |
|---|---:|---:|---:|---|
| Brihadaranyaka | 4512 | 4520 | 10703 | First in Hume's order |
| Chandogya | 10704 | 10715 | 16416 | Longest after Brihadaranyaka |
| Taittiriya | 16417 | 16428 | 17710 | Mostly prose; sparse N. markers |
| Aitareya | 17711 | 17721 | 18176 | Hume gives the Upanishad proper, not embedding Aranyaka |
| Kaushitaki | 18177 | 18188 | 20297 | Footnotes label A/B recensions |
| Kena | 20298 | (immediate) | 20674 | Mixed verse + prose; sparse N. markers |
| Katha | 20675 | 20682 | 22219 | Six vallis |
| Isha | 22220 | 22225 | 22475 | 18 verses canonical, 18 passages extracted ✓ |
| Mundaka | 22476 | (immediate) | 23301 | Three mundakas × 2 khandas |
| Prasna | 23302 | 23308 | 24074 | Six prashnas |
| Mandukya | 24075 | 24082 | 24256 | 12 verses ✓ (matches v106) |
| Svetasvatara | 24257 | 24263 | 25584 | Six adhyayas |
| Maitri | 25585 | 25594 | 28544 | Seven prapathakas |

Bibliographic apparatus (preface, introduction, footnotes, index,
bibliography) is preserved in the raw OCR cache but stripped from
the ingested JSON via footnote-body and page-header heuristics.

Boundary correction history within v109:
- Initial detection used "first ALL-CAPS running-header occurrence"
  per Upanishad. This was wrong for several sections because Hume's
  running headers alternate (lowercase on left pages, all-caps on
  right pages) and the first ALL-CAPS occurrence is often the
  second-page header. Re-detection used the centred Upanishad
  title that opens the translation (lowercase styled or first-page
  caps).
- Mandukya's initial boundary bled into Svetasvatara (verses 2–4
  of Svetasvatara appeared as Mandukya passages 14–16). Corrected
  by setting Mandukya end at line 24256, Svetasvatara start at
  24257.
- Chandogya's initial boundary started at line 10829 (a third-page
  running header); corrected to 10704 (chapter-opening heading).

## 2. Parser

`05_scripts/ingest_hume_full.py` — generalised from the v106
`ingest_hume_mandukya.py`. Verse-anchoring strategy: a line that
matches `^N. [A-Z]` (or `^<lowercase-roman>. [A-Z]` for OCR
variants like `i.` in place of `1.`) opens a new passage. Material
before the first verse marker becomes a `preamble` passage carrying
the centred title and section sub-head. Page-running-headers, page
numbers, and footnote bodies are dropped.

Footnote-body detection: a line matching `^[0-9]\s+<English-word>`
(digit + space + capital, no period) is treated as a footnote-body
start; following lines are dropped until a blank line or a clear
new verse marker. Conservative list of English openers tuned from
the v106 Mandukya pass (e.g., *In, A, An, The, That, Or, Compare,
Sankara, Possibly, See, Cf., …*). False positives on legitimate
verses are prevented by the requirement that verses have `^N.`
(digit + period), not `^N ` (digit + space).

## 3. Output

`03_web_app/data/upanishads-hume_hume.json` (789 KB) +
`upanishads-hume_hume.json.gz`. Hierarchy `[upanishad, passage]`.

Passages per Upanishad:

| Upanishad | Passages |
|---|---:|
| Brihadaranyaka | 384 |
| Chandogya | 565 |
| Taittiriya | 13 |
| Aitareya | 29 |
| Kaushitaki | 35 |
| Kena | 8 |
| Katha | 114 |
| Isha | 18 |
| Mundaka | 63 |
| Prasna | 64 |
| Mandukya | 13 |
| Svetasvatara | 108 |
| Maitri | 69 |
| **Total** | **1,483** |

Low counts on Taittiriya/Kena/Aitareya reflect Hume's actual prose
formatting in those Upanishads: many anuvakas and khandas are
rendered as flowing prose without `N.` verse numbers, so the
verse-anchor finds fewer cut points. This is acceptable for a
second-witness use case — the reader lands at the Upanishad's
opening and scrolls through Hume's full text.

## 4. Catalog registration

`data/index.json` — new entry id `upanishads-hume-1921`:

```json
{
  "id": "upanishads-hume-1921",
  "title": "The Thirteen Principal Upanishads (Hume 1921)",
  "tradition": "Hindu",
  "collection": "sacred",
  "hierarchy": ["upanishad", "passage"],
  "data_file": "upanishads-hume_hume.json",
  "source": "internetarchive",
  "translator": ["Robert Ernest Hume"],
  "year": 1921,
  "quality": "scholarly",
  "importance_rank": 6
}
```

`data/index.json.gz` regenerated. Catalog grew from 1202 → 1203
texts.

## 5. Family-index changes (`TEXT_FAMILIES.upanishads`)

### `members[]`

Replaced the v106 `upanishads-hume-mandukya` entry with the new
unified `upanishads-hume-1921`:

```js
- { textId: 'upanishads-hume-mandukya', role: 'collection',
-   note: 'Hume 1921 — Mandukya only (Hume edition of the 13 principals)' }
+ { textId: 'upanishads-hume-1921', role: 'collection',
+   note: 'Hume 1921 — The Thirteen Principal Upanishads (Oxford University Press), all 13 principals' }
```

### `byUpanishad[]`

- **Mandukya**: witness migrated from
  `upanishads-hume-mandukya` (groupKey '1') to
  `upanishads-hume-1921` (groupKey 'mandukya'). Route quality stays
  `safe`. Note about Karika omission preserved.
- **Isha, Kena, Katha, Prasna, Mundaka, Taittiriya, Chandogya,
  Brihadaranyaka, Svetasvatara, Kaushitaki**: each gets a NEW
  second witness `{ textId: 'upanishads-hume-1921', groupKey:
  '<slug>', role: 'source-volume', routeQuality: 'safe' }`
  appended after the existing Müller primary witness.
- **Aitareya**: second witness added — points to
  `upanishads-hume-1921` at groupKey 'aitareya'. The note explains
  this is "Hume's direct translation of the Aitareya Upanishad
  proper (without the embedding Aranyaka)" — a meaningful
  comparison case against the existing Müller Part 1 witness which
  routes into the AITAREYA-ARANYAKA section.
- **Maitri**: second witness added — points to
  `upanishads-hume-1921` at groupKey 'maitri', alongside the
  existing Müller Part 2 pid-route.

All 13 principal Upanishads now carry a Hume witness.

## 6. Files not deleted

The v106 Mandukya-only excerpt is **kept on disk**:

- `03_web_app/data/upanishads-hume-mandukya_hume.json` (preserved)
- `03_web_app/data/upanishads-hume-mandukya_hume.json.gz` (preserved)
- `03_web_app/data/index.json` still carries the
  `upanishads-hume-mandukya` catalog entry from v106 (preserved)
- `05_scripts/ingest_hume_mandukya.py` (preserved)
- `05_scripts/_register_hume_mandukya_in_index.py` (preserved)

The family `byUpanishad` config no longer points at the v106 file,
but the file remains as a historical record of the v106 ingestion.
The witness picker for Mandukya now shows the new full-Hume
witness; the old standalone Mandukya source is no longer surfaced
through the By-text view (per the user's spec).

## 7. Non-destructive guarantees preserved

- **No JSON files merged, rewritten, or deleted.** The five pre-v109
  Upanishads source files (Müller complete, Müller Part 1, Müller
  Part 2, Johnston, Aiyar Thirty Minor) are completely untouched.
  The v106 Mandukya-only file is also untouched.
- **No synthetic combined text.** The new `upanishads-hume-1921`
  source is exclusively from Hume's 1921 edition — no inter-
  translator synthesis.
- **Translator/editor/source/year credit preserved on every
  witness card.** The new Hume entries carry
  `translator: 'Robert Ernest Hume'` and `year: '1921'`.
- **Route quality is `safe` for every new Hume witness.** No fake
  or uncertain routes added. The `principalMissing` list remains
  empty.
- **Page-type doctrine, three-view family page, witness picker,
  Atlas Object architecture, reading-room flow:** unchanged.
- **No UI redesign.** Same view structure as v108.
- **No folio/Atlas-Object work** in this pass.

## 8. Muktikā coverage unchanged

The 36/108 Muktikā coverage figure does NOT increase. Second
witnesses do not add new entries to the Muktikā 108 — they enrich
existing entries with additional translations.

```
Muktikā 108 coverage: 36 / 108 (33%)   ← unchanged from v107
Principal active:    13 / 13            ← unchanged from v106
```

## 9. Family-page behaviour after v109

- **By Veda view**: no card changes; counts unchanged.
- **Traditional order view**: no card changes; counts unchanged.
- **By text view**: Hume entry in the **Specialised collections**
  section now reads "The Thirteen Principal Upanishads (Hume 1921)
  — all 13 principals" rather than v106's "Mandukya only".
- **Witness picker**: every principal Upanishad now shows TWO
  witnesses (Müller + Hume), or in the cases of Aitareya and
  Maitri, Müller-via-pid-route + Hume. Mandukya shows only one
  witness (Hume), because no Müller Mandukya exists.

## 10. Coordination with the restricted-source protocol

Hume 1921 is the canonical example of a PD-safe source: published
in the US before 1929 → public domain regardless of URAA. The
parallel v109 deliverable `reports/v109_restricted_source_protocol.md`
documents how restricted (copyrighted / PD-uncertain) sources are
handled OUT-OF-GIT, so the path Hume takes (public cache → public
data → public witness route) is reserved for genuinely PD-safe
material.

## 11. Build marker

`v108-yoga-acquisition-needed` → **`v109-hume-principal-witnesses`**

The marker name reflects the headline win: Hume now provides a
second witness on every principal Upanishad in the archive. The
sannyāsa-cluster, yoga-cluster, Mahā-Nārāyaṇa, and sectarian
acquisition needs remain open — see v107 and v108 reports for the
deferred plan.
