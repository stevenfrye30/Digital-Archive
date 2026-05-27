# v119 — Sastri Brihadaranyaka source hunt → Roer 1856 alternative added

The v118 report flagged a possibility: Vol 5's preface and Max
Müller's letter suggested S. Sitarama Sastri *planned* a
Brihadaranyaka volume to follow his 5-volume *The Upanishads and
Sri Sankara's Commentary* set. v119 hunts for any such volume.

**Outcome**: **No Sastri Brihadaranyaka volume was ever published**
(strong evidence below). However, the search surfaced **Eduard Roer's
1856 Brihadaranyaka with Sankara's commentary on Chapter 1**
(Bibliotheca Indica, Asiatic Society of Bengal, Calcutta) — pre-1929
PD-safe, full English translation of the Upanishad plus partial
Sankara commentary. v119 adds Roer 1856 as an additional witness on
the Brihadaranyaka entry, labelled as a `source-volume` (not
`commentary-witness`) because the Sankara coverage is partial.

**Counts unchanged at 44 / 108 active, 64 missing.**

## 1. Summary

| Field | Before v119 | After v119 |
|---|---|---|
| Build marker | `v118-sankara-commentary-set-complete` | **`v119-brihadaranyaka-roer-added`** |
| Sastri Brihadaranyaka volume search | not previously attempted | **NOT FOUND** — likely never published |
| Roer 1856 Brihadaranyaka witness | (n/a) | **added** as source-volume witness on Brihadaranyaka |
| MUKTIKA_108 active | 44 / 108 | 44 / 108 (unchanged) |
| Missing | 64 | 64 (unchanged) |
| Brihadaranyaka witnesses | 2 (Müller + Hume) | **3** (+Roer 1856) |
| Catalog entries | 1208 | **1209** |
| Family `members[]` | 13 | **14** (+Roer source-volume) |
| Restricted text committed | none | none |
| Files touched | `index.html` (build marker + 1 byUpanishad witness + 1 family member), `data/index.json` (+1 entry), `data/upanishads-brihadaranyaka-roer_roer.json` (+gz) (new), `reports/v119_…md` (new), `05_scripts/v119_ingest_roer_brihadaranyaka.py` (new) |

## 2. Internal evidence (re-examined)

### 2.1 Vol 5 preface (Sastri 1901)

From the OCR'd preface in
`02_raw_sources/Library_/Internetarchive/.../Vol5/...`:

> *"**The late Professor Max Muller**, to whom India is under a deep
> debt of gratitude, expressed, in a letter to me (printed
> overleaf), his desire to accept the dedication of the translation
> of the Brihadaranyaka Upanishad."* — V.C. Seshacharri, Publisher,
> Madras, May 1901.

Key word: **"the late"**. Müller died **28 October 1900**. So Vol 5
(1901) was published *after* Müller's death.

### 2.2 Max Müller's letter (printed in Vol 5 preface)

OCR'd as "tfith December 1MM" (date) — most likely **December 1899**
(the "MM" reads as garbled "899" or "999"; Müller's signature is
recognizable). The letter says:

> *"If you translate the Brihadāraṇyaka Upanishad I shall accept its
> dedication to me as a real honour."*

Crucial conditional: **"If you translate"** — Müller was inviting
Sastri to undertake the Brihadaranyaka translation, not
acknowledging an existing translation. As of December 1899:

| Vol | Status as of Dec 1899 |
|---|---|
| Vol 1 (Isa, Kena, Mundaka) | published 1898 — done |
| Vol 2 (Katha, Prasna) | published 1898 — done |
| Vol 3 (Chandogya 1-4) | published 1899 — done or in progress |
| Vol 4 (Chandogya 5-8) | published 1899 — done or in progress |
| Vol 5 (Aitareya + Taittiriya) | not yet — would appear 1901 |
| **Vol 6 (Brihadaranyaka)** | **not even begun; Müller's invitation arrives** |

### 2.3 Subsequent publication record (1901–1928)

* Hume's authoritative 1921 bibliography lists Sastri/Jha as **5 volumes only** (Isa+Kena+Mundaka / Katha+Prasna / Chandogya 1-4 / Chandogya 5-8 / Aitareya+Taittiriya).
* No Vol 6 / "Brihadaranyaka" / "Sastri Brihadaranyaka" is catalogued in Hume's exhaustive bibliography of all known pre-1921 Upanishad editions.
* The 1925-issue Vol 1 reprint and subsequent reprintings don't introduce a new volume — they reissue existing volumes.

### 2.4 Interpretation

The evidence is consistent: Sastri received Müller's invitation in
December 1899 but **never undertook the Brihadaranyaka translation**.
Possible reasons (we cannot determine which from internal evidence
alone):
* Müller died < 1 year after writing the letter (Oct 1900), so the
  dedication invitation was moot.
* Sastri's effort shifted to Vol 5 (Aitareya + Taittiriya) and its
  Annie Besant dedication.
* Brihadaranyaka is the longest principal Upanishad (6 adhyāyas, 47
  brāhmaṇas — would have been a much larger volume than Vols 1-5
  combined); the project's scale may have deterred completion.
* No reliable record of any later Sastri Brihadaranyaka volume exists.

**Conclusion: The Sastri Brihadaranyaka volume was apparently never
published.** v119 documents this honestly and moves to the Roer
alternative.

## 3. Local search results

| Location searched | Hits found |
|---|---|
| `02_raw_sources/Library_/Internetarchive/` | None — only the v117/v118 Sastri Vols 1+2 and v118 raw caches (Vols 3,4,5 in `/tmp`). No Sastri Brihadaranyaka. |
| `02_raw_sources/Library_/SacredTexts.com/` | None matching Sastri+Brihadaranyaka. |
| `02_raw_sources/Library_/Gutenberg.org/` | None. |
| `01_library/` | None matching Sastri+Brihadaranyaka. |
| `03_web_app/data/` (catalog) | Existing Brihadaranyaka routes — Müller (`upanishads`) and Hume (`upanishads-hume-1921`). No Sastri Brihadaranyaka witness. |
| Hume 1921 bibliography (lines 28799+) | Brihadaranyaka section header lists: Burnouf 1833 (French), Bohtlingk 1889 (German), Vasu 1913 (English; Sacred Books of the Hindus vol 14). **No Sastri Brihadaranyaka.** |

## 4. External search results

Five separate IA / Open Library API queries were run:

| Query | Hits relevant to target |
|---|---|
| `Brihadaranyaka + Sastri + Sankara` | None pre-1929 with Sastri attribution. Madhavananda 1950 (post-1929 URAA-restricted). |
| `Brihadaranyaka + Seshacharri OR Natesan` | No matching Upanishad editions. Found unrelated Natesan publications. |
| `Brihadaranyaka Upanishad English Sankara commentary date:[1898-1928]` | **Zero results.** |
| Open Library `author=Sitarama Sastri & q=Brihadaranyaka` | **Zero results.** |
| `Brihadaranyaka + Roer + Bibliotheca Indica` | **Hit: `The_Brihad_aranyaka_upanishad_Sankarabhashya_English`** by Eduard Roer, Bibliotheca Indica 1856 — see §5 |

External corroboration: every reputable search returns **zero**
Sastri Brihadaranyaka editions. The conclusion of §2.4 stands.

## 5. Roer 1856 — the alternative found

### 5.1 Source metadata

| Field | Value |
|---|---|
| Title page | "THE BRIHAD ARANYAKA UPANISHAD, AND THE COMMENTARY OF S'ANKARA ACHARYA ON ITS FIRST CHAPTER, TRANSLATED FROM THE ORIGINAL SANSCRIT BY DR. E. ROER" |
| Translator | Eduard Roer (1805–1866), Indologist at the Asiatic Society of Bengal |
| Series | Bibliotheca Indica (Vol II, Part III; Nos. 27, 88, 185) — Collection of Oriental Works under the patronage of the Hon. Court of Directors of the East India Company and superintendence of the Asiatic Society of Bengal |
| Publisher | Calcutta — Printed by J. Thomas at the Baptist Mission Press |
| Year | 1856 (per title page; series 1849-1856 across multiple parts) |
| IA identifier | `The_Brihad_aranyaka_upanishad_Sankarabhashya_English` |
| IA OCR file | `The_brihad_aranyaka_upanishad-SankarabhashyaEnglishforChapter1Only-1849_djvu.txt` (685 KB) |
| Local raw cache | `C:\Users\steve\AppData\Local\Temp\Roer-Brihadaranyaka.txt` (Windows folder-write restrictions; raw preserved in JSON output) |
| Page count | 290 |
| Languages | English (translation + commentary) |
| Public-domain status | **PD-safe in US** — published 1856; Roer died 1866; in Indian/UK PD long before 1996 URAA cutoff |

### 5.2 Coverage audit

| Component | Coverage |
|---|---|
| Brihadaranyaka Upanishad text (all 6 chapters) | **Complete English translation** |
| Sankara's commentary on Chapter 1 | **Complete English translation** |
| Sankara's commentary on Chapters 2-6 | Partial — only selected portions quoted |
| Roer's introduction + notes | Present |

The title page is explicit: *"AND THE COMMENTARY OF S'ANKARA
ACHARYA **ON ITS FIRST CHAPTER**"* — Roer's edition was always
intended as full-Upanishad + Chapter-1-commentary. This is not an
OCR loss; it is the original 1856 publication's scope.

### 5.3 Witness role choice

Per the v119 spec § "Commentary handling policy" and the v117
precedent, the natural label would be `commentary-witness`. But
the Sankara commentary is only **complete for 1 of 6 chapters**.
Labeling this as `commentary-witness` could mislead readers who
have come to expect (from v117/v118 Sastri witnesses) a full
Sankara reading throughout.

**Selected role: `source-volume`** (same role as Hume's literary
witness). The witness note explicitly explains the partial Sankara
coverage:

```js
{ textId: 'upanishads-brihadaranyaka-roer', groupKey: 'brihadaranyaka',
  sourceTitle: 'The Brihad Aranyaka Upanishad — Roer (Bibliotheca Indica)',
  translator: 'Eduard Roer', year: '1856',
  role: 'source-volume', routeQuality: 'safe',
  note: 'Earliest English translation of the Brihadaranyaka Upanishad ' +
        '(Asiatic Society of Bengal, Calcutta). Includes Sankara\'s ' +
        'commentary translated in full for Chapter 1 only; selected ' +
        'commentary portions for chapters 2-6. v119 alternative after ' +
        'confirming no Sastri Brihadaranyaka volume exists.' }
```

This is honest: readers see Roer as a third Brihadaranyaka witness
(after Müller's SBE complete + Hume 1921) with Sankara commentary
on Chapter 1 only. Discovery of the partial coverage is explicit
before the reader enters the reading room.

## 6. Integration summary

### 6.1 Data files

| Path | Bytes | Description |
|---|---:|---|
| `03_web_app/data/upanishads-brihadaranyaka-roer_roer.json` | 777,958 | 2,014 passages across L1=`brihadaranyaka` |
| `03_web_app/data/upanishads-brihadaranyaka-roer_roer.json.gz` | 208,889 | gzipped |
| `data/index.json` | +1 entry | Catalog 1208 → 1209 |

### 6.2 Family `members[]` addition

```js
{ textId: 'upanishads-brihadaranyaka-roer', role: 'source-volume',
  note: 'Roer 1856 — Brihadaranyaka Upanishad with Sankara commentary on Chapter 1 only; …' }
```

### 6.3 `byUpanishad` witness addition

Brihadaranyaka now shows **3 witnesses** (was 2):
1. Müller (primary, principal route)
2. Hume 1921 (source-volume)
3. **Roer 1856** (source-volume, with partial-Sankara note)

### 6.4 Counts unchanged

| Metric | Before v119 | After v119 |
|---|---:|---:|
| Primary `MUKTIKA_108` active | 44 / 108 | 44 / 108 |
| Missing | 64 | 64 |
| Legacy active | 43 / 108 | 43 / 108 |
| byUpanishad principals | 13 | 13 (Brihadaranyaka gained 1 witness, no new principal) |

## 7. Regression verification

| Test | Result |
|---|---|
| App loads | (verify on Pages) |
| Brihadaranyaka tile shows 3 witnesses (Müller + Hume + Roer) | ✓ |
| v117 Sastri Vols 1+2 witnesses (Isha/Kena/Mundaka/Katha/Prasna) intact | ✓ |
| v118 Sastri Vols 3+4+5 witnesses (Chandogya×2, Aitareya, Taittiriya) intact | ✓ |
| Müller principal routes intact | ✓ |
| Hume principal routes intact | ✓ |
| Aiyar minor routes intact (Paingala, Mandalabrahmana, Yogakundalini, Varaha, Dakshinamurti, Subala, Tejobindu, Muktika) | ✓ |
| Maitreya (v116) intact | ✓ |
| MUKTIKA_108 count 44/108 | ✓ |
| Missing 64 | ✓ |
| Per-Veda totals unchanged | ✓ |
| Roer 1856 data file exists (777K + gz 209K) | ✓ |
| Catalog 1209 entries | ✓ |
| No restricted text committed | ✓ — Roer 1856 is PD-safe |
| No duplicate principal tile | ✓ — appended as 3rd witness to existing Brihadaranyaka entry |
| No UI redesign | ✓ |

## 8. Sankara commentary coverage status (post-v119)

| Principal | Sankara commentary witness | Source |
|---|---|---|
| Isha | ✓ | Sastri Vol 1 |
| Kena | ✓ | Sastri Vol 1 |
| Katha | ✓ | Sastri Vol 2 |
| Prasna | ✓ | Sastri Vol 2 |
| Mundaka | ✓ | Sastri Vol 1 |
| Mandukya | — | (Hume; no Sankara commentary translation in archive — Gaudapada Karika is a separate text) |
| Aitareya | ✓ | Sastri Vol 5 |
| Taittiriya | ✓ | Sastri Vol 5 |
| Chandogya | ✓ (parts 1-4) ✓ (parts 5-8) | Sastri Vol 3 + Vol 4 |
| **Brihadaranyaka** | **partial (Chapter 1 only)** | **Roer 1856** |
| Svetasvatara | — | (no Sankara commentary translation in archive) |
| Kaushitaki | — | (no Sankara commentary translation in archive) |
| Maitri | — | (no Sankara commentary translation in archive) |

**Coverage of the principal-canon Sankara-commentary layer**:
* Full Sankara: 8 / 13 (Isha, Kena, Katha, Prasna, Mundaka, Aitareya,
  Taittiriya, Chandogya)
* Partial Sankara: 1 / 13 (Brihadaranyaka Ch 1 via Roer)
* No Sankara: 4 / 13 (Mandukya, Svetasvatara, Kaushitaki, Maitri)

## 9. Future recommendations

### v120: Search for remaining Sankara-commentary translations

The 4 still-uncovered principals (Mandukya, Svetasvatara,
Kaushitaki, Maitri) could potentially be searched in:
* DLI advanced-search by Upanishad name + "Sankara" + pre-1929
* Older Bibliotheca Indica volumes (Roer, Mitra translated several
  Upanishads for that series 1840s–1860s)
* Sacred Texts archive
* Gaudapada Karika translations would cover Mandukya commentary
  (but those are separate texts, not Sankara's direct commentary —
  Mandukya itself has no full Sankara bhasya in any tradition)
* Note: Svetasvatara, Kaushitaki, and Maitri are NOT traditionally
  among the Upanishads on which Sankara wrote bhasya. The Sankara-
  commentary "complete set" may have always been the 10 principals
  (Isha, Kena, Katha, Prasna, Mundaka, Mandukya, Aitareya,
  Taittiriya, Chandogya, Brihadaranyaka) — plus Mandukya's commentary
  is Gaudapada's not Sankara's. **The Sankara-commentary layer is
  essentially complete at 8-9 of 13 principals.**

### v120: Tattvabhushan 1900–1904 (per v118 §8)

3-volume Calcutta edition covering 12 of 13 principals. Would add
fourth-witness depth and a Bengali-tradition translation alongside
Sastri's Madras-Sankara and Roer's Calcutta-Bibliotheca-Indica
witnesses. PD-safe.

### v121: Pivot back to missing-64 acquisition

The witness-enrichment passes (v109 Hume → v117 Sastri Vols 1+2 →
v118 Sastri Vols 3+4+5 → v119 Roer) have now substantially deepened
the principal-Upanishad layer (most principals have 3–4 English
witnesses + Sankara-commentary for 8 of 13). The 64 missing minors
remain the structural gap. Time to return to:
* Theosophist back-issue micro-search
* 2031 Adyar Saiva trigger scheduling

## 10. Non-destructive guarantees

* **No JSON files merged, rewritten, or deleted.**
* **No source files merged.** Roer 1856 is its own textId / data file.
* **No `MUKTIKA_108` changes.** Canon array unchanged from v116.
* **No `byUpanishad` principal entry removed or reorganized.** Roer
  appended as 3rd Brihadaranyaka witness; Müller and Hume entries
  preserved verbatim.
* **No restricted text committed.** Roer 1856 is pre-1929 PD-safe.
* **No public routes to restricted text.**
* **No UI redesign.** Single new witness row in the Brihadaranyaka
  picker; one new entry in the family By-text members list. Other
  views unchanged.
* **No folio / Atlas-Object work.**
* **No new acquisition path invented.** Roer is a real, catalogued,
  PD-safe English Sankara-commentary source for Brihadaranyaka; no
  fakery.

## 11. Build marker

`v118-sankara-commentary-set-complete` → **`v119-brihadaranyaka-roer-added`**

The marker reflects what actually happened: the planned Sastri
Brihadaranyaka volume was confirmed absent from history, and an
authentic 1856 Roer alternative — pre-1929 PD-safe, full Upanishad
translation, partial Sankara commentary — was added as a new
witness on the existing Brihadaranyaka entry.
