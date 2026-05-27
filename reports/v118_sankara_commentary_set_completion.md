# v118 — Śaṅkara commentary witness set complete (Sastri Vols 3+4+5)

v117 acquired Vols 1 + 2 of S. Sitarama Sastri's *The Upanishads
and Sri Sankara's Commentary* (Madras, V.C. Seshacharri / G.A.
Natesan & Co., 1898–1901), covering 5 of 13 principal Upanishads.
v118 completes the set: Vols 3, 4, and 5 are now in the archive,
bringing the Śaṅkara-commentary witness layer to **8 of 13 principal
Upanishads** (Isha, Kena, Mundaka, Katha, Prasna, Chandogya, Aitareya,
Taittiriya).

All five volumes were ultimately found in the **Digital Library of
India** collection on Internet Archive — a single search via the IA
JSON advanced-search API returned all five `in.ernet.dli.2015.NNN`
identifiers in one response, after v117's spot-search via Open
Library had located only Vols 1 + 2 via separate Google-digitised
scans.

**Counts unchanged at 44 / 108 active, 64 missing** — as expected for
a witness-enrichment pass.

## 1. Summary

| Field | Before v118 | After v118 |
|---|---|---|
| Build marker | `v117-sankara-commentary-witnesses` | **`v118-sankara-commentary-set-complete`** |
| Sastri volumes in archive | 2 (Vol 1 + 2) | **5 (Vols 1+2+3+4+5)** ✓ complete set |
| Catalog entries | 1205 | **1208** (+3) |
| Family `members[]` entries | 10 | **13** (+3 source-volume) |
| Principals with Sastri commentary witness | 5 (Isha, Kena, Mundaka, Katha, Prasna) | **8** (+Chandogya, Aitareya, Taittiriya) |
| Chandogya witnesses | 2 (Müller + Hume) | **4** (Müller + Hume + Sastri Vol 3 + Sastri Vol 4) |
| Aitareya witnesses | 2 (Müller Part 1 + Hume) | **3** (+ Sastri Vol 5) |
| Taittiriya witnesses | 2 (Müller + Hume) | **3** (+ Sastri Vol 5) |
| MUKTIKA_108 active | 44 / 108 | 44 / 108 (unchanged) |
| Missing | 64 | 64 (unchanged) |
| New data files | 0 | **3** (vol3 + vol4 + vol5 JSON + gz) |
| New parser/registration scripts | 0 | 2 (`v118_ingest_sastri_vol345.py`, `v118_register_sastri_vol345.py`) |
| Restricted text committed | none | none |
| External text ingested | (n/a) | yes — 3 PD-safe IA-DLI scans |

## 2. Source identification

The v118 IA advanced-search query
(`https://archive.org/advancedsearch.php?q=Aitareya+Taittiriya+Sastri+Sankara&output=json`)
combined with a follow-up query on "Sankaras commentary Upanishad
Sastri OR Jha" returned a clean listing of all five Sastri volumes
via the DLI collection.

| Vol | Year | IA Identifier (DLI) | Contents | Status |
|---:|---:|---|---|---|
| 1 | 1905 (reprint of 1898) | `upanishadssrisan00sita` *(v117 — original Google scan)*; also `in.ernet.dli.2015.106209` | Isa, Kena, Mundaka | v117 ✓ |
| 2 | 1898 | `upanishadsandsr00agoog` *(v117 — Google scan)*; also `in.ernet.dli.2015.106210` | Katha, Prasna | v117 ✓ |
| **3** | **1899** | **`in.ernet.dli.2015.106211`** | **Chandogya parts 1-4** | **v118 ✓** |
| **4** | **1899** | **`in.ernet.dli.2015.106212`** | **Chandogya parts 5-8** | **v118 ✓** |
| **5** | **1901** | **`in.ernet.dli.2015.57841`** + alt scan `AitareyataittiriyaUpanishadsWithShankaraBhashya-English` | **Aitareya, Taittiriya** | **v118 ✓** |

### 2.1 Vol 3 (Chandogya 1-4)

| Field | Value |
|---|---|
| Title (printed) | The Chhandogya Upanishad |
| Translator | S. Sitarama Sastri, B.A. |
| Publisher | V.C. Seshacharri (M.R.A.S.); printed by G.A. Natesan & Co., Esplanade, Madras |
| Year | 1899 |
| IA identifier | `in.ernet.dli.2015.106211` |
| IA OCR file | `2015.106211.Upanishads-And-Sri-Sankaras-Commentary-Vol3_djvu.txt` |
| Local raw cache | `C:\Users\steve\AppData\Local\Temp\Sastri-Vol3.txt` (386,561 bytes) — Windows folder write restrictions; raw preserved in JSON output |
| Page count | ~311 (per Hume bibliography) |
| Languages | English (translation + commentary) + Sanskrit (root verses) |
| Public-domain status | **PD-safe in US** — pre-1929 publication |

### 2.2 Vol 4 (Chandogya 5-8)

| Field | Value |
|---|---|
| Title (printed) | The Chhandogya Upanishad |
| Translator | S. Sitarama Sastri, B.A. |
| Publisher | V.C. Seshacharri / G.A. Natesan & Co., Madras |
| Year | 1899 |
| IA identifier | `in.ernet.dli.2015.106212` |
| IA OCR file | `2015.106212.Upanishads-And-Sri-Sankaras-Commentary-Vol4_djvu.txt` |
| Local raw cache | `C:\Users\steve\AppData\Local\Temp\Sastri-Vol4.txt` (453,222 bytes) |
| Page count | ~374 |
| Languages | English + Sanskrit |
| Public-domain status | **PD-safe in US** — pre-1929 |

### 2.3 Vol 5 (Aitareya, Taittiriya)

| Field | Value |
|---|---|
| Title (printed) | The Aitareya and Taittiriya Upanishads and Sri Sankara's Commentary |
| Translator | S. Sitarama Sastri, B.A. |
| Publisher | V.C. Seshacharri, Vakil High Court, Madras; printed at The India Printing Works, Madras |
| Year | 1901 (per Hume bibliography; OCR'd "19$$" on title page is mangled but May 1900 date for Max Müller's letter dedication + Hume bibliography place it at 1901) |
| Dedication | "To Mrs. Annie Besant, P.T.S." (by kind permission); also references a Max Müller letter from December 1900 thanking Sastri for sending him translations |
| IA identifiers | `in.ernet.dli.2015.57841` (DLI scan); also `AitareyataittiriyaUpanishadsWithShankaraBhashya-English` (alt scan) |
| IA OCR file | `2015.57841.Upanishads-And-Sri-Sankaras-Commentary---Vol5_djvu.txt` |
| Local raw cache | `C:\Users\steve\AppData\Local\Temp\Sastri-Vol5-DLI.txt` (289,777 bytes) |
| Page count | ~230 |
| Languages | English + Sanskrit |
| Public-domain status | **PD-safe in US** — pre-1929 |

## 3. Coverage audit

### 3.1 Vol 3 — Chandogya parts 1-4

| Upanishad | textId | groupKey | source line range | Passages | Route quality |
|---|---|---|---:|---:|---|
| Chandogya (parts 1-4) | `upanishads-sankara-sastri-vol3` | `chandogya` | 100–12187 | **1,892** | safe |

### 3.2 Vol 4 — Chandogya parts 5-8

| Upanishad | textId | groupKey | source line range | Passages | Route quality |
|---|---|---|---:|---:|---|
| Chandogya (parts 5-8) | `upanishads-sankara-sastri-vol4` | `chandogya` | 100–13324 | **1,861** | safe |

### 3.3 Vol 5 — Aitareya + Taittiriya

| Upanishad | textId | groupKey | source line range | Passages | Route quality |
|---|---|---|---:|---:|---|
| Aitareya | `upanishads-sankara-sastri-vol5` | `aitareya` | 150–2440 | **241** | safe |
| Taittiriya | `upanishads-sankara-sastri-vol5` | `taittiriya` | 2441–8134 | **655** | safe |

### 3.4 Source content structure

Each volume preserves Sastri's interleaved layout:

1. **Sanskrit root verse** (Devanagari + Roman transliteration)
2. **English translation** of the root verse
3. **Sri Sankaracharya's commentary** (often headed "SRI SANKARA'S
   INTRODUCTION" at section openings) — substantial paragraphs of
   Advaita exposition

Per v117 policy, the parser ingests them as a single paragraph
flow without splitting root vs commentary. The witness role
`commentary-witness` and the note "with Sankaracharya's commentary
interleaved" make the structure explicit to the reader before they
enter the reading room.

## 4. Commentary handling — Chandogya split-volume

The user spec explicitly required: *"Do not create two Chandogya
cards. Add either one grouped witness if the app can route across
both volumes cleanly, or two clearly labeled commentary witnesses."*

v118 implementation: **TWO clearly labeled witnesses on the single
existing Chandogya `byUpanishad` entry**. Both witnesses are
type `commentary-witness`; their `note` fields distinguish the
parts:

```js
// Witness 3 on Chandogya (added v118 after v109 Hume):
{ textId: 'upanishads-sankara-sastri-vol3', groupKey: 'chandogya',
  sourceTitle: "The Upanishads and Sri Sankara's Commentary (Vol 3) — Sastri",
  translator: 'S. Sitarama Sastri', year: '1899',
  role: 'commentary-witness', routeQuality: 'safe',
  note: 'Vol 3: Chandogya parts 1-4 with Sankaracharya\'s commentary interleaved. Vol 4 (parts 5-8) is the continuation witness below.' }

// Witness 4 on Chandogya:
{ textId: 'upanishads-sankara-sastri-vol4', groupKey: 'chandogya',
  sourceTitle: "The Upanishads and Sri Sankara's Commentary (Vol 4) — Sastri",
  translator: 'S. Sitarama Sastri', year: '1899',
  role: 'commentary-witness', routeQuality: 'safe',
  note: 'Vol 4: Chandogya parts 5-8 with Sankaracharya\'s commentary interleaved. Continues from Vol 3 (parts 1-4).' }
```

Result: the Chandogya tile shows **4 witnesses** in the picker
(Müller principal + Hume + Sastri Vol 3 parts 1-4 + Sastri Vol 4
parts 5-8). The notes cross-reference each other so a reader who
opens Vol 3 knows where to continue (Vol 4) and vice-versa. No new
Chandogya tile created; no synthetic merging of volumes.

## 5. Integration summary

### 5.1 Data files

| Path | Bytes | Description |
|---|---:|---|
| `03_web_app/data/upanishads-sankara-sastri-vol3_sastri.json` | 487,450 | Vol 3: 1,892 passages under L1=`chandogya` |
| `03_web_app/data/upanishads-sankara-sastri-vol3_sastri.json.gz` | 143,890 | gzipped |
| `03_web_app/data/upanishads-sankara-sastri-vol4_sastri.json` | 551,213 | Vol 4: 1,861 passages under L1=`chandogya` |
| `03_web_app/data/upanishads-sankara-sastri-vol4_sastri.json.gz` | 168,376 | gzipped |
| `03_web_app/data/upanishads-sankara-sastri-vol5_sastri.json` | 333,539 | Vol 5: 241 Aitareya + 655 Taittiriya = 896 passages |
| `03_web_app/data/upanishads-sankara-sastri-vol5_sastri.json.gz` | 101,304 | gzipped |
| `data/index.json` | +3 entries | Catalog 1205 → 1208 |

### 5.2 Parser + registration scripts (local-only, outside repo)

* `05_scripts/v118_ingest_sastri_vol345.py` — extends v117 parser;
  three-volume handling; Chandogya single-L1 per volume; Vol 5
  dual-L1.
* `05_scripts/v118_register_sastri_vol345.py` — catalog registration
  for all 3 new textIds.

### 5.3 Raw-source caches (local-only)

* Vol 3 raw OCR: `C:\Users\steve\AppData\Local\Temp\Sastri-Vol3.txt`
* Vol 4 raw OCR: `C:\Users\steve\AppData\Local\Temp\Sastri-Vol4.txt`
* Vol 5 raw OCR: `C:\Users\steve\AppData\Local\Temp\Sastri-Vol5-DLI.txt`

(Same Windows folder-write restriction as v117 Vol 2; raw text is
preserved within the JSON output. The DLI scans on IA remain the
canonical source.)

### 5.4 Family `members[]` additions

```js
{ textId: 'upanishads-sankara-sastri-vol3', role: 'source-volume',
  note: 'Sastri 1899 — Chandogya parts 1-4 with Sri Sankara\'s commentary; …' }
{ textId: 'upanishads-sankara-sastri-vol4', role: 'source-volume',
  note: 'Sastri 1899 — Chandogya parts 5-8 with Sri Sankara\'s commentary; …' }
{ textId: 'upanishads-sankara-sastri-vol5', role: 'source-volume',
  note: 'Sastri 1901 — Aitareya, Taittiriya with Sri Sankara\'s commentary; …' }
```

### 5.5 `byUpanishad` witness additions

| Principal | Witness added | Vol |
|---|---|---|
| Chandogya | `upanishads-sankara-sastri-vol3` (groupKey=chandogya) | 3 |
| Chandogya | `upanishads-sankara-sastri-vol4` (groupKey=chandogya) | 4 |
| Aitareya | `upanishads-sankara-sastri-vol5` (groupKey=aitareya) | 5 |
| Taittiriya | `upanishads-sankara-sastri-vol5` (groupKey=taittiriya) | 5 |

Total: 4 new witness rows added to 3 byUpanishad entries.

### 5.6 Counts unchanged

| Metric | Before v118 | After v118 |
|---|---:|---:|
| Primary `MUKTIKA_108` active | 44 / 108 | 44 / 108 |
| Missing | 64 | 64 |
| Legacy `MUKTIKA_108_LEGACY_LOCAL` active | 43 / 108 | 43 / 108 |
| byUpanishad principal entries | 13 | 13 |
| byUpanishad routes total | 44 | 44 (no new principals; only witness additions) |

v118 is exactly a witness-enrichment pass — no Muktikā-coverage
change.

## 6. Missing Sastri/Jha volumes

**None.** All 5 volumes of *The Upanishads and Sri Sankara's
Commentary* are now in the archive. The set is **complete**.

The 13 principal Upanishads' Sankara-commentary coverage status:

| Principal | Sankara commentary witness? | Source |
|---|:---:|---|
| Isha | ✓ | Sastri Vol 1 |
| Kena | ✓ | Sastri Vol 1 |
| Katha | ✓ | Sastri Vol 2 |
| Prasna | ✓ | Sastri Vol 2 |
| Mundaka | ✓ | Sastri Vol 1 |
| Mandukya | (Sastri set does not include Mandukya as a separate volume) | — |
| Aitareya | ✓ | Sastri Vol 5 |
| Taittiriya | ✓ | Sastri Vol 5 |
| Chandogya | ✓ (parts 1-4) ✓ (parts 5-8) | Sastri Vol 3 + Vol 4 |
| Brihadaranyaka | — (Sastri set does not include Brihadaranyaka; per the Max Müller letter in Vol 5 preface, Sastri planned to dedicate a Brihadaranyaka translation to Müller but it was either never published or published separately) | — |
| Svetasvatara | — | — |
| Kaushitaki | — | — |
| Maitri | — | — |

**8 of 13 principals** are covered. The remaining 5 (Mandukya,
Brihadaranyaka, Svetasvatara, Kaushitaki, Maitri) are NOT in
Sastri's 5-volume set; they require a different Sankara-commentary
translation source for any future enrichment pass.

## 7. Regression verification

| Test | Result |
|---|---|
| App loads | (verify on Pages) |
| Family page renders | (verify) |
| `MUKTIKA_108` active = 44 / 108 | ✓ |
| Missing = 64 | ✓ |
| Legacy `MUKTIKA_108_LEGACY_LOCAL` = 43 / 108 | ✓ |
| v117 Sastri witnesses on Isha, Kena, Mundaka, Katha, Prasna intact | ✓ — Vol 1 + Vol 2 witnesses unchanged |
| New Sastri witnesses on Chandogya (×2), Aitareya, Taittiriya present | ✓ |
| Müller principal witnesses (v0/v100) intact | ✓ — all 13 principals' Müller routes unchanged |
| Hume principal witnesses (v109) intact | ✓ |
| Aiyar minor routes intact (Paingala, Mandalabrahmana, Yogakundalini, Varaha, Dakshinamurti, Subala, Tejobindu, Muktika, etc.) | ✓ |
| Maitreya (v116) intact | ✓ — `key='maitreya'` still routes to Aiyar L1=6 |
| Sastri data files exist | ✓ — vol3 488K, vol4 551K, vol5 334K (+ gz) |
| Catalog 1208 total | ✓ |
| No restricted text committed | ✓ — all 3 are pre-1929 PD-safe DLI scans |
| No duplicate principal cards | ✓ — Sastri witnesses appended to existing entries |
| Chandogya split represented as 2 labeled witnesses on 1 tile | ✓ |

## 8. Future recommendations

### v119: Tattvabhushan 1900–1904

Sitanath Tattvabhushan's 3-volume *The Upanishads, edited with
Annotations and English Translation* (Calcutta, Som Brothers,
1900–1904) covers 12 of the 13 principals. Would add fourth-witness
depth and a Bengali-tradition translation alongside Sastri's
Madras-tradition Sankara commentary. PD-safe. Same low-risk pattern.

### v120: Vasu *Sacred Books of the Hindus* series

S.C. Vasu's Allahabad Panini Office series (1909–1917):
* Vol 1 *Six Upanishads* (Isa+Kena+Katha+Prasna+Mundaka+Manduka, 1911)
* Vol 3 *Chandogya* (1909-10)
* Vol 14 *Brihadaranyaka* (1913)

Would add Madhva-commentary tradition (Vasu drew on Madhvacharya's
Dvaita reading, complementing Sastri's Advaita Sankara reading).
PD-safe.

### v121: Return to missing-64 acquisition

The witness-enrichment passes (v109 Hume, v117+v118 Sastri) have
now substantially deepened the principal layer. The 64 missing
minors remain the structural gap. v121+ should pivot back to
missing-64 work:
* Theosophist back-issue micro-search if user can supply IA item
  identifiers
* DLI advanced-search for older Adyar Bulletin English translations
* Schedule 2031 Adyar Saiva Upanishads PD-entry trigger

### v122 / scheduled: 2031 Adyar Saiva trigger

The single highest-value future event for missing-64 reduction.
Document the Ayyangar 1935 *Saiva-Upanishads* (Adyar) IA identifier
+ acquisition pipeline for automated ingestion on 2031-01-01.

### Note on Brihadaranyaka commentary

Per Vol 5's preface, Sastri planned to dedicate his Brihadaranyaka
translation to Max Müller (Müller's December 1900 letter accepts
the dedication: *"If you translate the Brihadaranyaka Upanishad I
shall accept its dedication to me as a real honour"*). However:
* Müller died in October 1900 — predating the letter? OR the letter
  is actually from late 1899; OCR'd "1MM" as the year is ambiguous.
* No published Sastri Brihadaranyaka volume is catalogued in Hume's
  1921 bibliography.

A targeted v123+ search may surface a separately-published Sastri
Brihadaranyaka volume that would complete the Sankara-commentary
coverage to 9 of 13 principals. Until then, the 5-volume set is
considered complete.

## 9. Non-destructive guarantees

* **No JSON files merged, rewritten, or deleted.** All prior Sastri
  Vol 1+2 data + every Müller/Hume/Aiyar/Johnson source untouched.
* **No source files merged.** Each Sastri volume is its own textId
  + data file.
* **No `MUKTIKA_108` changes.** Canon array byte-for-byte same as v116.
* **No `byUpanishad` principal entry removed or reorganized.** New
  Sastri witnesses appended after existing Müller + Hume witnesses.
  Order preserved.
* **No restricted text committed.** All 3 new sources are pre-1929
  PD-safe DLI scans.
* **No public routes to restricted text.**
* **No UI redesign.** No layout, tile, tab, button, or canon-
  selector changes. The Chandogya tile now shows 4 witnesses in
  the picker; the Aitareya and Taittiriya tiles show 3 each. Other
  tiles unchanged.
* **No folio / Atlas-Object work.**

## 10. Build marker

`v117-sankara-commentary-witnesses` → **`v118-sankara-commentary-set-complete`**

The marker reflects the completion: all 5 volumes of Sastri's
*The Upanishads and Sri Sankara's Commentary* are now in the
archive; 8 of 13 principal Upanishads carry a Śaṅkara-commentary
witness layer.
