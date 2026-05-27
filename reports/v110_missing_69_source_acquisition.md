# v110 — Missing-69 source-acquisition pass + Aiyar deep audit batch

The v110 pass attacks the remaining 69-Upanishad Muktikā gap. Two
parallel activities:

1. **Deep audit of in-archive sources** (the v104 → v107 pattern).
2. **Source-family evaluation** of external pre-1929 PD English
   candidates that might cover the Sannyāsa / Yoga / Shaiva /
   Vaishnava / Shakta clusters.

Outcome: **three more Muktikā Upanishads recovered** from Aiyar
1914 via deep audit — Pāingala (#22), Maṇḍalabrāhmaṇa (#20),
Yogakuṇḍalinī (#60). Coverage advances **39 → 42 / 108**.
External-source survey produced no PD-safe ingestible batch source
for the remaining 66; the Adyar Library English Series (1935–1978)
remains the dominant unrealised batch, blocked by URAA-restored US
copyright through 2031–2073 depending on volume.

## 1. Starting state (before v110)

| Metric | Value |
|---|---:|
| Build marker | `v109-hume-principal-witnesses` |
| Active Muktikā 108 | **39 / 108** |
| Missing Muktikā 108 | **69** |
| Principal canon (13) | complete; all 13 carry both Müller (where covered) and Hume second witnesses |
| Active byUpanishad entries | 38 |
| Source files in `data/` | unchanged since v109 |

Hume 1921 was added in v109 as a second-witness layer over the 13
principals; this did not change Muktikā coverage because second
witnesses do not add new entries.

## 2. The missing-69 list (current code state — extracted from MUKTIKA_108)

Class codes: **M** principal · **V** sāmānya Vedānta · **S** sannyāsa
· **Y** yoga · **Sh** shaiva · **Vs** vaishnava · **Sk** shakta.

### Sannyāsa class — 15 missing (S)

| # | Name | Veda |
|---:|---|---|
| 5 | Nirvāṇa | Rigveda |
| 13 | Jābāla | Shukla Yajurveda |
| 15 | Paramahaṃsa | Shukla Yajurveda |
| 21 | Advayatāraka | Shukla Yajurveda |
| 24 | Turīyātīta | Shukla Yajurveda |
| 27 | Yājñavalkya | Shukla Yajurveda |
| 28 | Sātyāyanī | Shukla Yajurveda |
| 53 | Avadhūta | Krishna Yajurveda |
| 54 | Kaṭharudra | Krishna Yajurveda |
| 65 | Āruṇi | Samaveda |
| 67 | Maitreyī | Samaveda |
| 72 | Sannyāsa | Samaveda |
| 74 | Kuṇḍikā | Samaveda |
| 98 | Paramahaṃsa-parivrājaka | Atharvaveda |
|104 | Avadhūta | Atharvaveda |

### Shaiva class — 12 missing (Sh)

| # | Name | Veda |
|---:|---|---|
| 7 | Akṣamālā | Rigveda |
| 39 | Kālāgnirudra | Krishna Yajurveda |
| 47 | Dakṣiṇāmūrti | Krishna Yajurveda |
| 56 | Rudrahṛdaya | Krishna Yajurveda |
| 57 | Pañcabrahma | Krishna Yajurveda |
| 76 | Rudrākṣajābāla | Samaveda |
| 77 | Jābāli | Samaveda |
| 82 | Atharvaśiras | Atharvaveda |
| 83 | Atharvaśikha | Atharvaveda |
| 84 | Bṛhajjābāla | Atharvaveda |
| 88 | Śarabha | Atharvaveda |
|102 | Pāśupatabrahma | Atharvaveda |

### Shakta class — 15 missing (Sk)

| # | Name | Veda |
|---:|---|---|
| 8 | Tripura | Rigveda |
| 9 | Saubhāgyalakṣmī | Rigveda |
| 10 | Bahvṛca | Rigveda |
| 62 | Sarasvatī-rahasya | Krishna Yajurveda |
| 87 | Sītā | Atharvaveda |
| 89 | Tripurātapani | Atharvaveda |
| 90 | Devī | Atharvaveda |
| 91 | Tripurā | Atharvaveda |
| 92 | Bhāvanā | Atharvaveda |
| 93 | Saubhāgya | Atharvaveda |
| 94 | Sarasvatī-rahasya | Atharvaveda |
| 99 | Annapūrṇā | Atharvaveda |
|105 | Tripurā-tāpinī | Atharvaveda |
|106 | Devī | Atharvaveda |
|107 | Bhāvanā | Atharvaveda |

### Sāmānya / Vedānta class — 13 missing (V)

| # | Name | Veda | v110 status |
|---:|---|---|---|
| 4 | Mudgala | Rigveda | still missing |
| 17 | Mantrikā | Shukla Yajurveda | still missing |
| **22** | **Pāingala** | Shukla Yajurveda | **✓ active v110** |
| 42 | Śukarahasya | Krishna Yajurveda | still missing |
| 51 | Ekākṣara | Krishna Yajurveda | still missing |
| 52 | Akṣi | Krishna Yajurveda | still missing |
| 58 | Prāṇāgnihotra | Krishna Yajurveda | still missing |
| 71 | Mahā | Samaveda | still missing |
| 75 | Sāvitrī | Samaveda | still missing |
|100 | Sūrya | Atharvaveda | still missing |
|101 | Ātmā | Atharvaveda | still missing |
|103 | Parabrahma | Atharvaveda | still missing |
|108 | Mahāvākya | Atharvaveda | still missing |

### Vaishnava class — 6 missing (Vs)

| # | Name | Veda |
|---:|---|---|
| 59 | Mahā-Nārāyaṇa | Krishna Yajurveda |
| 70 | Vāsudeva | Samaveda |
| 73 | Avyakta | Samaveda |
| 85 | Nṛsiṃhatāpani | Atharvaveda |
| 95 | Rāmarahasya | Atharvaveda |
| 96 | Rāmatāpaṇi | Atharvaveda |

### Yoga class — 8 missing (Y)

| # | Name | Veda | v110 status |
|---:|---|---|---|
| 19 | Trīśikhibrāhmaṇa | Shukla Yajurveda | still missing |
| **20** | **Maṇḍalabrāhmaṇa** | Shukla Yajurveda | **✓ active v110** |
| 40 | Kṣurikā | Krishna Yajurveda | still missing |
| 45 | Brahmavidyā | Krishna Yajurveda | still missing |
| 50 | Yogaśikhā | Krishna Yajurveda | still missing |
| **60** | **Yogakuṇḍalinī** | Krishna Yajurveda | **✓ active v110** |
| 69 | Yogachūḍāmaṇi | Samaveda | still missing |
| 78 | Darśana | Samaveda | still missing |

## 3. Source-family evaluation

### 3.1 In-archive deep audit — Aiyar 1914 *Thirty Minor Upanishads*

Already covered: 26 minor Upanishads + Subāla, Tejobindu, Muktikā
(via v104, v107 deep audits).

**Aiyar L1 ranges not previously claimed** by `byUpanishad`:

| L1 range | Aiyar chapter title | Content identified |
|---|---|---|
| 1 | "Thirty Minor Upanishads" | front matter |
| 3 | "Adhyaya II" | Muktikā continuation (already routed via L1=2 safe-start) |
| 7–8 | "Adhyaya II", "Adhyaya III" | Maitreya continuation (already routed via L1=6 safe-start) |
| **13–16** | "Adhyaya I"–"Adhyaya IV" | **Pāingala Upanishad** (Yajnavalkya-Paingala dialogue on Kaivalya) |
| 19–27 | "Khanda II"–"Khanda XVI" | Subāla continuation (already routed via L1=18 safe-start) |
| 29–33 | "Chapter II"–"Chapter VI" | Tejobindu continuation (already routed via L1=28 safe-start) |
| 43–50 | "Upades'a II"–"Upades'a IX" | Narada-Parivrajaka continuation (already routed via L1=42 safe-start) |
| 52–54 | "Chapter II", "Chapter III", end | Sandilya continuation (already routed via L1=51 safe-start) |
| 59–63 | "Chapter I"–"Chapter V" | Varaha Upanishad — **NOT in this MUKTIKA_108 array** (see §3.1.1) |
| **64–67** | "Brahmana I"–"Brahmana V" | **Maṇḍalabrāhmaṇa Upanishad** (Yajnavalkya-Aditya dialogue on Atma-tattva + eightfold yoga) |
| **69–71** | "Chapter I"–"Chapter III" | **Yogakuṇḍalinī Upanishad** (chitta / vāsanās / prāṇa-vāyu / khechari / melanamantra) |

**Recovered**: 3 missing Muktikā Upanishads.

#### 3.1.1 Varaha — found but not in the local MUKTIKA_108 array

Aiyar L1=59–63 contains the **Varāha Upanishad** (Rbhu-Varāha
dialogue, opening with the sage Rbhu's twelve-year penance and the
Lord appearing as a boar). The published Muktikā 108 list does
include Varāha (usually at #98, Krishna Yajurveda, sāmānya class),
but the **local `MUKTIKA_108` array in `index.html` does not list it**.
At #98 the local array has Paramahaṃsa-parivrājaka (Atharvaveda,
S-class) instead. This appears to be a divergence between local
canonical-list convention and the most common published version of
the Muktikā list (Adyar Library / Theosophical Society order).

**v110 does NOT modify the local `MUKTIKA_108` array** to insert
Varāha. Modifying canonical-list assignments is outside the v110
scope and would conflict with the principle "do not fake any missing
Upanishad" — the local array represents a particular canonical
choice. A future v111 pass could:

* either add a non-Muktikā `byUpanishad` entry for Varāha (it has
  safe-start text in Aiyar L1=59 → 63) so the family page shows it
  as a recovered minor outside the 108 count, or
* reconcile the local `MUKTIKA_108` with the more common Adyar
  ordering (which would require explicit user direction on which
  canonical version to follow).

For v110, Varāha is documented here as **acquired but not surfaced**.

### 3.2 External pre-1929 PD English candidate sources

#### 3.2.1 Already in archive
- **Müller SBE I + XV (1879 / 1884)** — covers 11 principal Upanishads
- **Hume 1921** — covers all 13 principals (added v109)
- **Aiyar 1914 *Thirty Minor Upanishads*** — covers ~30 minor including 3 newly mapped in v110
- **Charles Johnston** — covers some principals as Theosophical-style retranslations

#### 3.2.2 Surveyed and rejected / deferred

| Source | Year | Author | Lang | PD status | Coverage | Decision |
|---|---:|---|---|---|---|---|
| *Sechzig Upanishads des Veda* | 1897 | Paul Deussen | German | PD | Wide (60 Upanishads incl. several missing-69) | **Defer** — not English. Sanskrit-only / German-only sources cannot become English reading witnesses. |
| *Sixty Upanishads of the Veda* (Eng tr.) | 1980 | Bedekar & Palsule | English | **Copyrighted** | Wide | **Reject** — modern English translation, copyright till 2075. |
| *Sanatana Dharma* | 1903 | A. Besant + B. Das | English | PD | Excerpts of select Upanishads only | **Defer** — fragmentary; not a clean Upanishads volume. |
| *Wisdom of the Upanishats* | 1907 | Annie Besant | English | PD | Synthesis / paraphrase, not direct translation | **Reject** — synthesis text, not source witness. |
| *Saiva Upanishads (Adyar Library Series)* | 1925 | A. Mahadeva Sastri (ed.) | Sanskrit + Sanskrit commentary | PD in US (URAA-restored till 2021; now safe) | Saiva cluster (12 missing) | **Reject as reading witness** — Sanskrit-only with Sanskrit commentary. Only useful as metadata / future Sanskrit-source. Per v109 protocol: Sanskrit-only sources cannot become English reading witnesses. |
| *Sannyāsa Upanishads (Adyar Series, Mahadeva Sastri ed.)* | 1929 | T.R. Chintamani Dikshit | Sanskrit + Sanskrit commentary | PD in US (publication year boundary; just out of copyright) | Sannyāsa cluster (15 missing) | **Reject as reading witness** — Sanskrit-only. |
| *Saiva Upanishads (Adyar Series, English translation)* | 1935 | T.R. Srinivasa Ayyangar (translator), G. Srinivasa Murti (ed.) | English | **Restricted** — 1935 publication + URAA-restored copyright in US through 2031 (95 years from publication) | Saiva cluster (12 missing) | **Restricted** under v109 protocol; defer to ≥2031. |
| *Yoga Upanishads (Adyar Series, English)* | 1938 | T.R. Srinivasa Ayyangar (translator) | English | **Restricted** — URAA-restored till 2034 | Yoga cluster (8 missing minus 3 already covered) | **Restricted**; defer to ≥2034. |
| *Vaishnava Upanishads (Adyar Series, English)* | 1945 | T.R. Srinivasa Ayyangar (translator) | English | **Restricted** — copyright till 2041 (URAA-restored) | Vaishnava cluster (6 missing) | **Restricted**; defer to ≥2041. |
| *Samanya-Vedanta Upanishads (Adyar Series, English)* | 1941 | T.R. Srinivasa Ayyangar (translator) | English | **Restricted** — copyright till 2037 | sāmānya class (12 still missing after v110) | **Restricted**; defer to ≥2037. |
| *Shakta Upanishads (Adyar Series, English)* | 1950 | A.G. Krishna Warrier (translator) | English | **Restricted** — copyright till 2046 | Shakta cluster (15 missing) | **Restricted**; defer to ≥2046. |
| *Samnyāsa Upanishads (Adyar Series, English)* | 1978 | A.A. Ramanathan (translator) | English | **Restricted** — copyright till 2074 | Sannyāsa cluster (15 missing) | **Restricted**; defer to ≥2074 (or rights acquisition). |
| *108 Upanishads — text + commentary* | 2024 | Dr. Prabhakara Rao Marabathina | English | **Restricted** — copyright till 2119 | Full 108 | **Restricted**; defer. |
| sacred-texts.com Upanishad subsections | — | various aggregator | English | mostly PD-aggregator | duplicates of Müller / Hume / Aiyar already in archive | **No new content** — verified no additional pre-1929 English Upanishad volumes surfaced through the aggregator that weren't already covered. |
| Theosophist articles / individual pre-1929 translations | 1879–1928 | W.Q. Judge, A. Besant, B. Das, et al. | English | PD | Scattered individual Upanishads, mostly principals already covered | **Defer** — would require article-by-article acquisition; unlikely to yield batch coverage of any cluster. Possible future v111 micro-acquisitions for specific items (e.g. Atharvaśiras, Nṛsiṃhatāpani) if Theosophist-archived English translation surfaces. |
| Bibliotheca Indica series (Asiatic Society) | 1840–1920+ | various | mostly Sanskrit | PD | Editions of texts, mostly Sanskrit-only with English introductions | **Reject as reading witness** — not source of English translations of the missing-69. |

#### 3.2.3 Pattern observed

The pre-1929 PD English Upanishads landscape is **substantially
exhausted** for the Sannyāsa / Yoga / Shaiva / Vaishnava / Shakta
classes by the in-archive sources (Müller, Hume, Aiyar). The
**Adyar Library English Series (1935–1978)** is the canonical
modern translation of these clusters but is **uniformly
URAA-restricted** in US copyright. The earliest Adyar volumes enter
US PD in 2031 (Saiva), 2034 (Yoga), 2037 (Sāmānya), 2041
(Vaishnava), 2046 (Shakta), 2074 (Samnyāsa).

This pattern is structural, not accidental: the minor Upanishads
were not deemed scholarly priorities in 19th-century European
Indology, and the comprehensive English translation project that
covered them only began in the mid-20th century — exactly the
moment that places the work under continued US copyright.

## 4. Ingestion summary (v110)

| Item | Value |
|---|---|
| New source files created | **0** (route only — existing Aiyar source already on disk) |
| New parser scripts | **0** — used existing `data/upanishads-30-minor-aiyar_aiyar.json` |
| New `byUpanishad` entries | **3** (Pāingala, Maṇḍalabrāhmaṇa, Yogakuṇḍalinī) |
| `MUKTIKA_108` keys changed `null → '<key>'` | **3** (#20, #22, #60) |
| `members[]` additions | **0** — existing Aiyar source already in members list |
| Catalog (`data/index.json`) changes | **0** — existing entry untouched |
| Witness routes added | 3 safe-start routes to Aiyar L1=13, L1=64, L1=69 |
| Note | Each new route includes a per-witness note explaining the Aiyar L1 → Upanishad mapping (matching v104 / v107 documentation discipline) |

### 4.1 Route detail

```js
// v110 additions to TEXT_FAMILIES.upanishads.byUpanishad
{ key: 'paingala', name: 'Pāingala', displayTitle: 'Pāingala Upanishad',
  importance: 'minor', order: 297,
  associatedVeda: 'Shukla Yajurveda', vedaSource: 'curated traditional metadata',
  witnesses: [
    { textId: 'upanishads-30-minor-aiyar', groupKey: '13',
      sourceTitle: 'Thirty Minor Upanishads',
      translator: 'K. Narayanasvami Aiyar', year: '1914',
      role: 'primary', routeQuality: 'safe-start',
      note: '... continues through L1=16.' },
  ] },
{ key: 'mandalabrahmana', name: 'Maṇḍalabrāhmaṇa', displayTitle: 'Maṇḍalabrāhmaṇa Upanishad',
  importance: 'minor', order: 298,
  associatedVeda: 'Shukla Yajurveda', vedaSource: 'curated traditional metadata',
  witnesses: [
    { textId: 'upanishads-30-minor-aiyar', groupKey: '64',
      sourceTitle: 'Thirty Minor Upanishads',
      translator: 'K. Narayanasvami Aiyar', year: '1914',
      role: 'primary', routeQuality: 'safe-start',
      note: '... continues through L1=67.' },
  ] },
{ key: 'yogakundalini', name: 'Yogakuṇḍalinī', displayTitle: 'Yogakuṇḍalinī Upanishad',
  importance: 'minor', order: 299,
  associatedVeda: 'Krishna Yajurveda', vedaSource: 'curated traditional metadata',
  witnesses: [
    { textId: 'upanishads-30-minor-aiyar', groupKey: '69',
      sourceTitle: 'Thirty Minor Upanishads',
      translator: 'K. Narayanasvami Aiyar', year: '1914',
      role: 'primary', routeQuality: 'safe-start',
      note: '... continues through L1=71.' },
  ] },
```

### 4.2 MUKTIKA_108 changes

```js
{ n:20, key:'mandalabrahmana',  name:'Maṇḍalabrāhmaṇa', ... } // was key:null
{ n:22, key:'paingala',         name:'Pāingala',        ... } // was key:null
{ n:60, key:'yogakundalini',    name:'Yogakuṇḍalinī',   ... } // was key:null
```

### 4.3 Coverage changes

| Metric | Before v110 | After v110 |
|---|---:|---:|
| Active Muktikā 108 | 39 / 108 | **42 / 108** |
| Missing Muktikā 108 | 69 | **66** |
| Active byUpanishad entries | 38 | **41** |
| Principal canon | 13 / 13 | 13 / 13 (unchanged) |
| Hume second-witness coverage | 13 principals | 13 principals (unchanged) |
| Shukla Yajurveda Muktikā coverage | 8 / 19 (42%) | 10 / 19 (53%) |
| Krishna Yajurveda Muktikā coverage | 14 / 32 (44%) | 15 / 32 (47%) |

## 5. Deferred / restricted sources — explicit log

The following candidates were evaluated and **not committed** under
the v109 restricted-source protocol:

| Source | Reason | Earliest possible US-PD year |
|---|---|---:|
| Adyar Library Series — Saiva Upanishads (Ayyangar 1935 Eng tr) | URAA-restored | 2031 |
| Adyar Library Series — Yoga Upanishads (Ayyangar 1938 Eng tr) | URAA-restored | 2034 |
| Adyar Library Series — Samanya-Vedanta Upanishads (1941 Eng tr) | URAA-restored | 2037 |
| Adyar Library Series — Vaishnava Upanishads (1945 Eng tr) | URAA-restored | 2041 |
| Adyar Library Series — Shakta Upanishads (Warrier 1950 Eng tr) | URAA-restored | 2046 |
| Adyar Library Series — Samnyāsa Upanishads (Ramanathan 1978 Eng tr) | active US copyright | 2074 |
| Marabathina 2024 — *108 Upanishads* | active US copyright | 2120 |
| Adyar Library Series — Saiva (Mahadeva Sastri 1925 Sanskrit-only) | Sanskrit-only — cannot serve as English reading witness | — |
| Adyar Library Series — Samnyāsa (Chintamani Dikshit 1929 Sanskrit-only) | Sanskrit-only — cannot serve as English reading witness | — |
| Deussen 1897 — *Sechzig Upanishads des Veda* | German-only — cannot serve as English reading witness | — |

**No restricted full text has been committed.** No source files
have been added to `02_raw_sources/_restricted/` in this pass —
none of the above were downloaded.

**No public route created to restricted text.** The Adyar Library
English Series and Marabathina volume have not been added to
`TEXT_FAMILIES.upanishads.members` or `byUpanishad`.

## 6. Next recommended acquisition pass (v111+)

Three plausible follow-on directions, ranked by expected coverage
gain per effort:

### v111 (next pass): Theosophical-Quarterly micro-acquisitions
Hunt the *Theosophist* and *Theosophical Quarterly* archives
(1879–1928, all PD) for individual pre-1929 English translations
of specific missing-66 Upanishads. Likely candidates surfacing in
those journals: Atharvaśiras (Sh #82), Nṛsiṃhatāpani (Vs #85),
Bahvṛca (Sk #10), Atmā (V #101), Sūrya (V #100). Per-Upanishad
acquisition, low yield but compliant. Expected gain: **+1 to +8**.

### v112: Sanskrit-source metadata layer
For the missing-66, ingest Sanskrit-source metadata (chapter
counts, opening verses, named structure, Veda assignments) from
PD Sanskrit-only editions (Adyar Mahadeva Sastri 1925, Chintamani
Dikshit 1929 — both now in US PD). The metadata enriches the
family page's "known but inactive" disclosure without making a
fake reading route. **Coverage gain: 0**, but quality of the
"not yet" cards improves.

### v113 (long horizon — 2031): Adyar Library Series ingestion
First Adyar English volume enters US PD on **2031-01-01** (Saiva
Upanishads, Ayyangar 1935). Stage acquisition automation now so
that on the rollover date the ingestion can proceed without delay.
This is the single highest-yield future event for the missing-66
canopy.

### v114 / extended: Adyar Library digitization access
Adyar Library Bulletin contains shorter English summaries /
extracts of these Upanishads, occasionally pre-1929. Worth a deep
audit; some Bulletin issues may be in IA already.

## 7. Non-destructive guarantees

- **No JSON files merged, rewritten, or deleted.** Aiyar source
  file untouched; v110's three new routes reuse the existing data
  file with new family-index pointers.
- **No synthetic combined text.** No 108-Upanishads composite was
  created.
- **Translator credit preserved.** All three new witness entries
  carry `translator: 'K. Narayanasvami Aiyar', year: '1914'` and
  `sourceTitle: 'Thirty Minor Upanishads'`.
- **Page-type doctrine, three-view family page, witness picker,
  Atlas Object architecture, reading-room flow:** unchanged.
- **No UI redesign.** Same view structure as v109.
- **No folio/Atlas-Object work** in this pass.

## 8. Build marker

`v109-hume-principal-witnesses` → **`v110-aiyar-deep-audit-batch`**

The marker reflects that v110's contribution is a deep-audit batch
recovery from an already-in-archive source — no external acquisition
took place. The remaining 66-Upanishad gap is documented here with
explicit per-source rights status and a staged v111-v113 plan.
