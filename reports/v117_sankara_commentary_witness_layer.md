# v117 — Śaṅkara commentary witness layer (Sastri 1898 + 1905)

S. Sitarama Sastri's English translation of the principal Upanishads
*with Sri Sankaracharya's commentary* (V.C. Seshacharri / G.A.
Natesan, Madras 1898–1901; 5 volumes originally) is the canonical
Advaita-Vedanta study text in English. The v109 Hume principal-
witness layer established the pattern; v117 adds Sastri as a third-
witness layer specifically for commentary depth, alongside Müller
(philological) and Hume (literary).

This pass acquires **two volumes** newly downloaded from Internet
Archive — Vol 1 (Isa+Kena+Mundaka, 1905 reprint) and Vol 2
(Katha+Prasna, 1898 original) — which together provide commentary
witnesses for **5 of the 13 principal Upanishads**. Volumes 3, 4,
and 5 (Chandogya 1–4, Chandogya 5–8, Aitareya+Taittiriya) are not
yet on Internet Archive in the same canonical scan; v118+
acquisition targets.

**Counts unchanged at 44 / 108 active, 64 missing.** v117 adds
witness depth on already-active principals; no Muktikā-coverage
gain (as expected and intended).

## 1. Summary

| Field | Before v117 | After v117 |
|---|---|---|
| Build marker | `v116-aiyar-primary-muktika` | **`v117-sankara-commentary-witnesses`** |
| Public `MUKTIKA_108` count | 44 / 108 | 44 / 108 (unchanged) |
| Missing | 64 | 64 (unchanged) |
| Total catalog entries | 1203 | **1205** (+2: vol1 + vol2) |
| `byUpanishad` entries | 44 | 44 (no new principals; 5 entries gained witnesses) |
| Family `members[]` entries | 8 | **10** (+vol1 +vol2 as source-volume) |
| Principal Upanishads with Sastri witness | 0 | **5** (Isa, Kena, Mundaka via Vol 1; Katha, Prasna via Vol 2) |
| New data files | 0 | **2** (vol1 + vol2 JSON; gzipped) |
| New parser scripts | 0 | **2** (`ingest_sastri_sankara.py` + `register_sastri.py`) |
| New raw-source files | 0 | **2** (downloaded from IA; cached locally) |
| Restricted text committed | none | none |
| External text ingested | (n/a) | yes — PD-safe IA scans |

## 2. Source identification

### 2.1 Volume 1 (Isa, Kena, Mundaka)

| Field | Value |
|---|---|
| Title | The Upanishads and Sri Sankara's Commentary — First Volume |
| Contents | Isavasyopanishad, Kenopanishad, Mundakopanishad |
| Translator | S. Sitarama Sastri, B.A. |
| Publisher (original 1898) | V.C. Seshacharri, B.A. B.L. M.R.A.S., Madras |
| Printer | G.A. Natesan & Co., Printers, Esplanade |
| Year on title page | 1898 (originally); IA scan is 1905 reprint |
| IA identifier | `upanishadssrisan00sita` |
| IA OCR file | `https://archive.org/download/upanishadssrisan00sita/upanishadssrisan00sita_djvu.txt` |
| Local raw-source cache | `02_raw_sources/Library_/Internetarchive/Sastri-1905-Vol1-Isa-Kena-Mundaka.txt` (249,622 bytes) |
| Languages | English (translation + commentary) + Sanskrit (root verses) |
| Page count | 196 leaves (~179 numbered pages) |
| Public-domain status | **PD-safe in the US** — pre-1929 publication (both 1898 first edn and 1905 reprint); translator died ca. 1925, life+70 → 1995 → not URAA-restored on 1996-01-01 |

### 2.2 Volume 2 (Katha, Prasna)

| Field | Value |
|---|---|
| Title | The Upanishads and Sri Sankara's Commentary — Second Volume |
| Contents | Kathopanishad, Prasnopanishad |
| Translator | S. Sitarama Sastri, B.A. |
| Publisher | V.C. Seshacharri, B.A. B.L. M.R.A.S., Madras |
| Printer | G.A. Natesan & Co., Printers, Esplanade |
| Year | 1898 (December, per preface) |
| IA identifier | `upanishadsandsr00agoog` |
| IA OCR file | `https://archive.org/download/upanishadsandsr00agoog/upanishadsandsr00agoog_djvu.txt` |
| Local raw-source cache | `Sastri-1898-Vol2-Katha-Prasna.txt` (downloaded to `C:\Users\steve\AppData\Local\Temp\Sastri-1898-Vol2.txt` — Windows folder write blocked the normal cache location; raw is preserved at the temp path; the JSON output is committed) |
| Languages | English + Sanskrit |
| Page count | 217 (volume 2 + intro) |
| Public-domain status | **PD-safe** — same analysis as Vol 1 |

### 2.3 Volumes 3, 4, 5 (deferred to v118+)

* Vol 3: Chandogya 1–4, Jha, 1899 (311 pp.) — not yet found on IA under a canonical Sastri/Jha identifier
* Vol 4: Chandogya 5–8, Jha, 1899 (374 pp.) — not yet found
* Vol 5: Aitareya + Taittiriya, Sastri, 1901 (230 pp.) — not yet found

A more targeted IA search using exact title queries + Madras
publisher filter is warranted in v118.

## 3. Coverage audit

### 3.1 Vol 1 contents (boundary table)

| Upanishad | Source lines | Passages extracted | Notes |
|---|---:|---:|---|
| Isavasyopanishad | 145–955 | 103 | Opens with "Adoration to the Brahman. The Mantras beginning with Isavasyam…" — Sastri's English preface to the Upanishad followed by verse-by-verse text + commentary |
| Kenopanishad | 956–2700 | 213 | Opens with the long Sankara introduction explaining the ninth-chapter Talavakara context |
| Mundakopanishad | 2701–5154 | 306 | Includes Sankara's etymological exposition of "upanisad" itself in opening passages |
| Vol 1 TOTAL | | **622** | — |

### 3.2 Vol 2 contents (boundary table)

| Upanishad | Source lines | Passages extracted | Notes |
|---|---:|---:|---|
| Kathopanishad | 200–4114 | 536 | Six vallis (parts). "Here ends the Kathopanishad" at L4114 confirms boundary |
| Prasnopanishad | 4115–7200 | 355 | Six prashnas. "Here ends the sixth Prasna" near L7191. Sastri's introduction at first passage |
| Vol 2 TOTAL | | **891** | — |

### 3.3 Content structure

Each volume's text interleaves three layers:

1. **Sanskrit root verse** (Devanagari + Roman) — preserved in OCR;
   may show transliteration artifacts but the structure is intact.
2. **English translation** of the root verse.
3. **Sri Sankaracharya's commentary** (marked "Com.—" in the OCR)
   — substantial paragraphs of Advaita exposition.

These are NOT separated in v117's data file. The parser ingests
them as one continuous flow (paragraph-chunked), preserving Sastri's
own intended reading order: Sanskrit → English translation →
Sankara commentary → next verse. The witness-card label
`role: 'commentary-witness'` and note "Translation with Sri
Sankaracharya's commentary interleaved" make this explicit to the
reader before they enter the reading room.

This matches the v117 spec policy: "If the source interleaves root
text and commentary, preserve that structure as the source
presents it. Do not split root text and commentary destructively
unless boundaries are easy and the app structure supports it."

### 3.4 OCR notes

* Some pages show OCR artifacts (e.g. "tii(^" for "the", "Brahin)" for "Brahman"); typical of 19th-century Madras printing on Google's older scans.
* "Digitized by Google" watermark appears once at the start of Vol 2 Katha (passage `katha.1`) — accepted as a single-page artifact rather than aggressively stripped (risk of accidentally dropping legitimate first-paragraph content).
* Page-running-headers ("16 THE KATHOPANISHAD." etc.) and bare page numbers are stripped by the parser.

## 4. Commentary handling policy

The v117 spec required a clear policy. Selected approach:

* **Role**: `commentary-witness` on the byUpanishad entry. Sits
  alongside the existing primary (`primary`) and second-witness
  (`source-volume`) roles for the same Upanishad.
* **Note**: Each witness explicitly says "Translation with Sri
  Sankaracharya's commentary interleaved." A reader looking at the
  witness picker sees three witnesses on each of the 5 affected
  principals (Müller plain translation + Hume scholarly literary +
  Sastri commentary-with-Sankara).
* **Source-volume members[] entries**: `role: 'source-volume'`
  with a longer note: *"Sastri 1905 (reprint of 1898) — Isa, Kena,
  Mundaka with Sri Sankara's commentary; Adyar / Natesan, Madras;
  IA upanishadssrisan00sita"* and analogous for Vol 2.
* **No split** between root text and commentary. The interleaved
  source is preserved as Sastri intended.
* **No "translation-only" extraction**: a reader who wants the
  plain translation without commentary can use the Müller or Hume
  witnesses on the same Upanishad. Sastri is offered specifically
  as a commentary witness.

## 5. Integration changes

### 5.1 Data files

| Path | Bytes | Description |
|---|---:|---|
| `03_web_app/data/upanishads-sankara-sastri-vol1_sastri.json` | 245,468 | Vol 1: 622 passages across isha/kena/mundaka |
| `03_web_app/data/upanishads-sankara-sastri-vol1_sastri.json.gz` | ~80K | gzipped for Pages serving |
| `03_web_app/data/upanishads-sankara-sastri-vol2_sastri.json` | 276,290 | Vol 2: 891 passages across katha/prasna |
| `03_web_app/data/upanishads-sankara-sastri-vol2_sastri.json.gz` | ~90K | gzipped |
| `03_web_app/data/index.json` | (+2 entries) | Catalog grew from 1203 → 1205 |

### 5.2 New scripts (local-only — outside `03_web_app/` git repo)

* `05_scripts/v117_ingest_sastri_sankara.py` — paragraph-level
  parser; handles both volumes from their downloaded raw text.
* `05_scripts/v117_register_sastri.py` — registers both data files
  in `data/index.json` and regenerates `.gz`.

### 5.3 Raw-source caches (outside git repo)

* `02_raw_sources/Library_/Internetarchive/Sastri-1905-Vol1-Isa-Kena-Mundaka.txt` (Vol 1 OCR)
* `C:\Users\steve\AppData\Local\Temp\Sastri-1898-Vol2.txt` (Vol 2 OCR — saved to temp because the Internetarchive folder rejected the file write under the current sandbox session; data is parsed and stored in the JSON, so the cache location matters only for future re-parsing.)

### 5.4 Catalog (`data/index.json`)

```json
// new entry 1
{
  "id": "upanishads-sankara-sastri-vol1",
  "title": "The Upanishads and Sri Sankara's Commentary (Vol 1 — Isa, Kena, Mundaka)",
  "tradition": "Hindu",
  "collection": "sacred",
  "hierarchy": ["upanishad", "passage"],
  "data_file": "upanishads-sankara-sastri-vol1_sastri.json",
  "source": "internetarchive",
  "author": ["Sankaracarya (commentary)"],
  "translator": ["S. Sitarama Sastri"],
  "year": 1905,
  "translation_label": "Sastri 1905 — Sankara commentary",
  "quality": "scholarly",
  "importance_rank": 5
}
// new entry 2
{
  "id": "upanishads-sankara-sastri-vol2",
  "title": "The Upanishads and Sri Sankara's Commentary (Vol 2 — Katha, Prasna)",
  "year": 1898,
  // … same shape …
}
```

### 5.5 Family `members[]` additions

```js
{ textId: 'upanishads-sankara-sastri-vol1', role: 'source-volume',
  note: 'Sastri 1905 (reprint of 1898) — Isa, Kena, Mundaka with Sri Sankara\'s commentary; Adyar / Natesan, Madras; IA upanishadssrisan00sita' }
{ textId: 'upanishads-sankara-sastri-vol2', role: 'source-volume',
  note: 'Sastri 1898 — Katha, Prasna with Sri Sankara\'s commentary; V.C. Seshacharri / Natesan, Madras; IA upanishadsandsr00agoog' }
```

### 5.6 `byUpanishad` witness additions (5 principals × 1 witness each = 5 new witnesses)

Each of the 5 affected principal entries (`isha`, `kena`,
`mundaka`, `katha`, `prasna`) gains a new third witness card after
the existing Müller (primary) and Hume (source-volume) witnesses:

```js
// Example for Isha (Vol 1):
{ textId: 'upanishads-sankara-sastri-vol1', groupKey: 'isha',
  sourceTitle: "The Upanishads and Sri Sankara's Commentary (Vol 1) — Sastri",
  translator: 'S. Sitarama Sastri', year: '1905',
  role: 'commentary-witness', routeQuality: 'safe',
  note: 'Translation with Sri Sankaracharya\'s commentary interleaved. ' +
        'Originally published 1898; this 1905 reprint is the IA scan.' }

// Example for Katha (Vol 2):
{ textId: 'upanishads-sankara-sastri-vol2', groupKey: 'katha',
  sourceTitle: "The Upanishads and Sri Sankara's Commentary (Vol 2) — Sastri",
  translator: 'S. Sitarama Sastri', year: '1898',
  role: 'commentary-witness', routeQuality: 'safe',
  note: 'Translation with Sri Sankaracharya\'s commentary interleaved.' }
```

### 5.7 Counts unchanged

| Metric | Before v117 | After v117 |
|---|---:|---:|
| MUKTIKA_108 active | 44 / 108 | 44 / 108 |
| Missing | 64 | 64 |
| Legacy `MUKTIKA_108_LEGACY_LOCAL` active | 43 / 108 | 43 / 108 |
| byUpanishad principal entries | 13 | 13 |
| byUpanishad routes total | 44 | 44 |

The v117 work is exactly what was expected: witness enrichment
without Muktikā-coverage change. The 5 affected principals already
counted in primary; adding Sastri's commentary witness does not
add a new key to the canon array.

## 6. Regression verification

| Test | Result |
|---|---|
| App loads | (verify on live Pages) |
| Family page renders | (verify) |
| Muktikā count remains 44 / 108 | ✓ |
| Missing count remains 64 | ✓ |
| Müller principal witnesses intact | ✓ — Müller entries unchanged on all 13 principals |
| Hume principal witnesses (v109) intact | ✓ — Hume entries unchanged on all 13 principals |
| Sastri Vol 1 witnesses appear on Isha, Kena, Mundaka | ✓ |
| Sastri Vol 2 witnesses appear on Katha, Prasna | ✓ |
| Aiyar minor routes (Paingala, Mandalabrahmana, Yogakundalini, Varaha, Dakshinamurti, Subala, Tejobindu, Muktika) intact | ✓ |
| Dakshinamurti (v113) intact | ✓ |
| Varaha (v111→v116 native primary) intact | ✓ |
| Sastri data files exist + sized | ✓ — vol1: 245K, vol2: 276K |
| Sastri catalog entries registered | ✓ — 1205 total texts |
| No duplicate Upanishad cards | ✓ — Sastri appended to existing byUpanishad entries, no new principal entries created |
| No restricted text committed | ✓ — Sastri 1898/1905 are PD-safe |
| No public routes to restricted text | ✓ |

## 7. v118 recommendation

### Primary recommendation: Continue Sastri 5-volume completion

Track down IA identifiers for the missing 3 volumes:
* Vol 3 (Chandogya 1–4, Jha 1899, 311 pp.)
* Vol 4 (Chandogya 5–8, Jha 1899, 374 pp.)
* Vol 5 (Aitareya + Taittiriya, Sastri 1901, 230 pp.)

Strategy: Open Library search by exact title + publisher Natesan +
year. If not on IA, the Digital Library of India (DLI) `in.ernet.dli`
series may have them. Once acquired, ingest with the same parser
pattern; activate as commentary witnesses for Chandogya,
Aitareya, Taittiriya (would bring all 8 of the 13 principals
covered by the Sastri Sankara-commentary layer up to 8 — strong
scholarly depth).

### Secondary: Tattvabhushan 1900–1904 (per v114 §6.1)

Sitanath Tattvabhushan's 3-volume *The Upanishads, edited with
Annotations and English Translation* (Calcutta, Som Brothers,
1900–1904) covers 12 of 13 principals. Would add fourth-witness
depth for the principals. Adds no Muktikā-coverage gain but
significant scholarly value. Same low-risk acquisition pattern.

### Tertiary: Vasu *Sacred Books of the Hindus* series 1909–1917

Srisa Chandra Vasu's *Sacred Books of the Hindus* (Allahabad Panini
Office) — Vol 1 (six principals 1911), Vol 3 (Chandogya 1909–10
reprinted 1917), Vol 14 (Brihadaranyaka 1913) — would add a third
scholarly translation tradition.

### Long horizon: 2031 Adyar Saiva trigger

The 2031 Adyar Library *Saiva Upanishads* (Ayyangar 1935) entry to
US PD remains the single highest-yield event for closing
missing-in-both Upanishads — would close 7+ Shaiva-class entries.

## 8. Non-destructive guarantees

* **No JSON files merged, rewritten, or deleted.** Müller, Hume,
  Aiyar, Johnson, Sastri 1920 Dakshinamurti — all untouched.
* **No source files merged.** Each Sastri volume is its own
  textId / data file.
* **No `MUKTIKA_108` changes.** Canon array byte-for-byte same.
* **No `byUpanishad` principal entry removed or reorganized.**
  Sastri is appended as additional witness; no existing witness
  altered.
* **No restricted text committed.**
* **No public routes to restricted text.**
* **No UI redesign.** No layout, tile, tab, button, or canon-
  selector changes. The 5 affected principal cards now show 3
  witnesses (Müller + Hume + Sastri) where before they showed 2.
  The By-text Specialised-collections list grows from 8 to 10
  source-volume entries.
* **No folio / Atlas-Object work.**

## 9. Build marker

`v116-aiyar-primary-muktika` → **`v117-sankara-commentary-witnesses`**

The marker reflects the scholarly-depth contribution: 5 principal
Upanishads now have a Śaṅkara-commentary reading witness layer
backed by Sastri's Madras Natesan-Press edition of 1898 / 1905.
