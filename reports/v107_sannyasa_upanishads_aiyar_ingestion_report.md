# v107 — Sannyāsa acquisition audit + Muktikā Upanishad extracted

This pass had two outcomes:

1. **The Sannyāsa Upanishads source v105 recommended turned out to
   be a misattribution.** "K. Narayanasvami Aiyar's Sannyāsa
   Upanishads (1914)" does not exist as a discrete English work.
   The only 1914 Aiyar Upanishads volume IS the *Thirty Minor
   Upanishads* (already in the archive). Available Adyar Library
   Sannyāsa volumes are Sanskrit-only or post-1929 copyrighted.

2. **The deep re-audit recovered the Muktikā Upanishad** hidden
   inside Aiyar's already-ingested Thirty Minor at L1=2-3, listed
   in the source's chapter_titles as plain "Adhyaya I" and
   "Adhyaya II". The Muktikā Upanishad is the eponymous list-of-108
   meta-text — v105 had it as a Tier-2 priority target. Now active.

## 1. Source identification — what does NOT exist

### Original v107 target

| | |
|---|---|
| Target | K. Narayanasvami Aiyar's *Sannyāsa Upanishads* (1914) |
| Actual status | **Does not exist as a discrete English volume.** |

Re-check of v105's source-evaluation: my v105 plan listed an
"Aiyar Sannyāsa Upanishads (1914)" volume that, on rigorous
acquisition audit, was a conflation. Aiyar (K. Narayanasvami
Aiyar) published *one* major Upanishads compilation in 1914 —
*Thirty Minor Upanishads* — which is already in the archive.

### Available alternative Sannyāsa volumes (audit results)

| IA identifier | Year | Editor | Language | Public domain? | Verdict |
|---|---:|---|---|---|---|
| `in.ernet.dli.2015.170085` | 1912 | F. Otto Schrader | Sanskrit + German notes | Yes | Not English; not useful as a reading-room source |
| `dbkg_the-minor-upanisads-by-unknown-volume-1-samnyasa-u` | 1912 | F. Otto Schrader (Adyar Library) | Sanskrit + German notes | Yes (download restricted by IA) | Same content as above |
| `in.ernet.dli.2015.283731` | 1925 | A. Mahadeva Sastri (Adyar) | Sanskrit + Sanskrit commentary | Yes (US PD since 2021) | **Mislabelled in IA**: the OCR shows *The Sakta Upanishads*, not Sannyasa. Sanskrit only. |
| `in.ernet.dli.2015.283732` | 1929 | T.R. Chintamani Dikshit (Adyar) | Sanskrit + Sanskrit commentary by Sri Upanishad-Brahma-Yogin | Yes (US PD since 2025) | Sanskrit only with Sanskrit commentary; not English |
| `samnyasa-upanishads-english-aa-ramanathan-1978` | 1978 | A.A. Ramanathan (Adyar) | English | **No** (1978, still copyrighted) | Skip |
| `108-upanishads-the-order-as-given-in-the-muktika-upanishad` | 2024 | Dr. Prabhakara Rao Marabathina | English | **No** (modern) | Skip |

### Sannyāsa acquisition conclusion

**No clean public-domain English Sannyāsa-class compilation exists
that fits the archive's ingestion pattern.** The pre-1929 English
options (Aiyar 1914 misattribution, Mahadeva Sastri Sakta-not-Sannyāsa)
either don't exist or carry the wrong content; the post-1929
Adyar Library English series (Ramanathan 1978) remains in
copyright; the 2024 Marabathina volume is recent and not PD.

A separate-volume Sannyāsa ingestion would require:
- Either acquiring a not-yet-discovered pre-1929 English
  translation (e.g., older Theosophical Society publications), or
- Translating the Sanskrit-only Schrader / Dikshit volumes
  ourselves (out of scope for this archive's "route, don't merge"
  doctrine), or
- Acquiring rights / licensing the modern Ramanathan volume
  (commercial concern).

## 2. Muktikā Upanishad recovery — what v107 actually adds

### Source

Aiyar's Thirty Minor Upanishads (1914), already in the archive at
`data/upanishads-30-minor-aiyar_aiyar.json`. The Muktikā Upanishad
sits at L1=2-3 of that source — Aiyar's chapter_titles label these
two adhyāyas as plain "Adhyaya I" and "Adhyaya II", with no
"Muktika-Upanishad" prefix. v102's surface audit therefore missed
it; v107's deep textual audit recovered it.

### Identification proof

- **L1=2.1 opens**: *"ADDRESSING with devotion and obedience
  S'ri-Rama — the Lord Hari, at the end of His Samadhi, who being
  Himself changeless is the witness of the thousands of changes
  of Buddhi…"* — Hanuman's invocation that opens the Muktikā.
- **L1=2.5**: *"O Rama, how many are the Vedas and their branches?
  …What are the Upanishads? Please, through Thy grace, tell me
  truly."* — Hanuman's questioning frame.
- **L1=2.13**: *"The twice-born — after learning the 108 Upanishads,
  together with the Śānti as prescribed both before and after from
  the mouth of a Guru well versed in the observances of Vedic
  knowledge and study — become Jīvanmuktas till the destruction
  of the body."* — the canonical "108 Upanishads" passage.
- **L1=2.14–2.17**: Sri Rama's enumeration of every Upanishad in
  the 108 canon, grouped by Veda. This is the source-text behind
  the MUKTIKA_108 config the v104 pass built — recovered from its
  own underlying text.
- **L1=3**: continuation — Hanuman's questions on jīvanmukti and
  videhamukti; the Vasanā doctrine; the destruction of citta.

### Route quality

- Safe-start at `groupKey='2'` (33 non-fm passages across L1=2 and
  L1=3).
- Witness card carries a note explaining the spread:
  "Aiyar labels this Upanishad's two adhyāyas as 'Adhyaya I' /
  'Adhyaya II'; the text begins at L1=2 (Hanuman's opening
  question to Sri Rama) and continues through L1=3, including the
  canonical enumeration of the 108 Upanishads at verses 2.14–2.17."

### Family-index changes

```js
TEXT_FAMILIES.upanishads.byUpanishad += {
  key: 'muktika', name: 'Muktikā',
  displayTitle: 'Muktikā Upanishad',
  importance: 'principal',          // Mukhya per Muktikā classification
  order: 130,                       // after Kaushitaki in the principal sequence
  associatedVeda: 'Shukla Yajurveda',
  vedaSource: 'curated traditional metadata',
  witnesses: [{
    textId: 'upanishads-30-minor-aiyar', groupKey: '2',
    sourceTitle: 'Thirty Minor Upanishads',
    translator: 'K. Narayanasvami Aiyar', year: '1914',
    role: 'primary', routeQuality: 'safe-start',
    note: '...'
  }]
}
```

```js
MUKTIKA_108[28] /* #29 Muktikā */ : key changed from null → 'muktika'
```

## 3. Coverage changes

| Metric | Before v107 | After v107 |
|---|---:|---:|
| Active Upanishads in family index | 38 | **39** |
| Principal active | 13 / 13 | 13 / 13 + Muktikā (Mukhya) |
| Muktikā 108 coverage | 35 / 108 (32%) | **36 / 108 (33%)** |
| Shukla Yajurveda (Muktikā) | 7 / 19 (37%) | **8 / 19 (42%)** |
| Missing Muktikā 108 | 73 | **72** |

## 4. Uncertain / not-added material

- **Sannyāsa-class cluster** (Jābāla, Paramahaṃsa, Āruṇi, Sannyāsa,
  Kuṇḍikā, Yājñavalkya, Sātyāyanī, Nirvāṇa, Avadhūta, Kaṭharudra,
  Paramahaṃsa-parivrājaka, Turīyātīta, Maitreyī): **still missing**.
  No clean public-domain English compilation available. Best path
  forward is per-Upanishad acquisition from compilations that
  happen to include one or two sannyāsa-class texts each, or
  awaiting an Older-than-1929 English Sannyāsa anthology surfacing.

- **Mahā-Nārāyaṇa, Nṛsiṃhatāpani**: deferred — no clean source
  found in this pass.

## 5. Next acquisition recommendations (revised)

The v105 acquisition plan needs the following revision based on
this audit:

| Phase | Old plan (v105) | Revised plan (v107) |
|---|---|---|
| v107 | "Aiyar Sannyāsa Upanishads 1914" → ~12 sannyāsa | NOT POSSIBLE (misattribution). Replaced by Muktikā extraction from in-archive Aiyar source. |
| v108 | "Aiyar Yoga Upanishads 1938" → ~10 yoga (post-PD-verify) | T.R. Srinivasa Ayyangar's Adyar *Yoga Upanishads* (1938 / 1952 reprint) exists; copyright status needs verification (life+95: 2034 for 1938; life+70 of Ayyangar's death). Defer. |
| v109+ | Sectarian compilations (Shaiva / Vaishnava / Shakta) | Same; Adyar Library English series likely covers these (post-1929; copyright concerns). |
| Future | T5 residue | Same. |
| **Practical next pass** | — | **Re-audit existing Hindu data corpus** for other hidden Upanishads (Aiyar's L1 ranges, the Yoga-Vasishtha files, other compilations). v107 already proved deep audit pays off — v104 found Subāla/Tejobindu, v107 found Muktikā. |

## 6. App state preserved

- No JSON files merged, rewritten, or deleted.
- Aiyar source file (`upanishads-30-minor-aiyar_aiyar.json`)
  untouched; v107's Muktikā route reuses the existing data file
  with a new family-index pointer.
- Hume 1921 cache preserved for future second-witness use.
- Page-type doctrine, three-view family page, Atlas Object
  architecture, all other archive flows: unchanged.

## 7. Build marker

`v106-mandukya-hume-witness` → `v107-muktika-extracted-sannyasa-acquisition-needed`

The composite marker name honestly reflects both outcomes:
* Muktikā was extracted (a real win).
* Sannyāsa-class acquisition remains needed; the v105 plan
  recommendation has been corrected.
