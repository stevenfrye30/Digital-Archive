# v105 — Missing-74 Muktikā Upanishads acquisition plan

Phase 3 is **planning-only**. A deep repo audit (`02_raw_sources/`,
`01_library/`, all of `03_web_app/data/`) found no public-domain
Mandukya source locally, so no new active witnesses are added in
v105. This document is the responsible acquisition roadmap for the
remaining 74 Muktikā Upanishads.

## 1. Summary

| Metric | Value |
|---|---:|
| Muktikā 108 coverage before v105 | 34 / 108 (31%) |
| Muktikā 108 coverage after v105  | 34 / 108 (31%) — unchanged |
| Missing Upanishads | 74 |
| Active witnesses added in v105 | **0** (no local source) |
| Local audit verdict for Mandukya | **No translation text present in archive** |
| Recommended next ingestion (v106) | Mandukya from Hume's Thirteen Principal Upanishads (1921) |

## 2. Local repo audit findings

### Raw sources scanned (`02_raw_sources/Library_/`)

| File | Coverage | Contains Mandukya? |
|---|---|---|
| `openlibrary.org/The Upanishads_____Swami Paramananda.txt` | Vol. 1 only: Isa, Katha, Kena, Mundaka | **No** |
| `openlibrary.org/The Upanishads_____Max Muller.txt` | Müller's Vol. 2 (same as Part 2 already ingested) | **No** |
| `SacredTexts.com/The_Upanishads_____Max Muller (1879).txt` | Source for legacy 1900 reprint, already ingested | **No** |
| `SacredTexts.com/Upanishads (30 minor)_____K-Narayanasvami Aiyar (1914).txt` | Aiyar, already ingested | **No** |
| `SacredTexts.com/Upanishads (from them)_____Charles Johnson (1899).txt` | Johnston, already ingested | **No** |
| `SacredTexts.com/Upanishads - Part 1_____Max Muller (1879).txt` | Müller Part 1, already ingested | **No** |
| `SacredTexts.com/Upanishads - Part 2_____Max Muller (1879).txt` | Müller Part 2, already ingested | **No** |

### `03_web_app/data/` non-Upanishads files with Mandukya hits

| File | Hits | Nature |
|---|---:|---|
| `brahma-knowledge-barnett` | 2 | Bibliographic list mention (id='24.40' is just the word "Mandukya" in the appendix "List of the Chief Upanishads") |
| `dakshinamurti-stotra` | 2 | Commentary mention (the standalone Stotra, not the Dakshinamurti Upanishad) |
| `history-sanskrit-literature-macdonell` | 7 | Literary history description |
| `yoga-vasishtha-...` | 2 | Allusion |
| `thrice-greatest-hermes-...` | 2 | Allusion |

**Verdict: No translation text for the Mandukya Upanishad exists in
the archive.** Every hit is editorial/list/footnote material.

## 3. Missing 74 — full status table

(Format: number · name · variants · Veda · class · priority tier · recommended source)

### Rigveda missing (7)

| # | Name | Veda | Class | Tier | Recommended source |
|---|---|---|---|---|---|
| 4 | Mudgala | Rigveda | V | T5 | Sectarian compilations (Aurobindo / Aiyar broader vols.) |
| 5 | Nirvāṇa | Rigveda | S | T3 | Aiyar Sannyāsa Upanishads vol. or comparable |
| 7 | Akṣamālā | Rigveda | Sh | T4 | Shaiva compilations |
| 8 | Tripura | Rigveda | Sk | T4 | Shakta compilations |
| 9 | Saubhāgyalakṣmī | Rigveda | Sk | T4 | Shakta compilations |
| 10 | Bahvṛca | Rigveda | Sk | T4 | Shakta compilations |

### Shukla Yajurveda missing (12)

| # | Name | Veda | Class | Tier | Recommended source |
|---|---|---|---|---|---|
| 13 | Jābāla | SYV | S | T2 | Aiyar Sannyāsa Upanishads vol. |
| 15 | Paramahaṃsa | SYV | S | T2 | Aiyar Sannyāsa Upanishads vol. |
| 17 | Mantrikā | SYV | V | T3 | Aiyar Yoga Upanishads vol. (likely) |
| 19 | Trīśikhibrāhmaṇa | SYV | Y | T3 | Aiyar Yoga Upanishads vol. |
| 20 | Maṇḍalabrāhmaṇa | SYV | Y | T3 | Aiyar Yoga Upanishads vol. |
| 21 | Advayatāraka | SYV | S | T3 | Aiyar Yoga Upanishads vol. |
| 22 | Pāingala | SYV | V | T3 | Aurobindo collected / sectarian compilations |
| 24 | Turīyātīta | SYV | S | T2 | Aiyar Sannyāsa Upanishads vol. |
| 27 | Yājñavalkya | SYV | S | T2 | Aiyar Sannyāsa Upanishads vol. |
| 28 | Sātyāyanī | SYV | S | T2 | Aiyar Sannyāsa Upanishads vol. |
| 29 | Muktikā | SYV | M | **T2** | Hume / dedicated edition — the eponymous list-of-108 Upanishad itself |
| (16, 25, 26 already active) | | | | | |

### Krishna Yajurveda missing (16)

| # | Name | Veda | Class | Tier | Recommended source |
|---|---|---|---|---|---|
| 39 | Kālāgnirudra | KYV | Sh | T4 | Shaiva compilations |
| 40 | Kṣurikā | KYV | Y | T3 | Aiyar Yoga Upanishads vol. |
| 42 | Śukarahasya | KYV | V | T4 | Sectarian compilations |
| 45 | Brahmavidyā | KYV | Y | T3 | Aiyar Yoga Upanishads vol. (Müller mentions, doesn't translate) |
| 47 | Dakṣiṇāmūrti | KYV | Sh | T4 | Shaiva compilations |
| 50 | Yogaśikhā | KYV | Y | T3 | Aiyar Yoga Upanishads vol. (Müller mentions) |
| 51 | Ekākṣara | KYV | V | T4 | Sectarian compilations |
| 52 | Akṣi | KYV | V | T4 | Sectarian compilations |
| 53 | Avadhūta | KYV | S | T2 | Aiyar Sannyāsa Upanishads vol. |
| 54 | Kaṭharudra | KYV | S | T4 | Shaiva / Sannyāsa compilations |
| 56 | Rudrahṛdaya | KYV | Sh | T4 | Shaiva compilations |
| 57 | Pañcabrahma | KYV | Sh | T4 | Shaiva compilations |
| 58 | Prāṇāgnihotra | KYV | V | T3 | Aiyar Yoga Upanishads vol. (Müller mentions) |
| 59 | Mahā-Nārāyaṇa | KYV | Vs | **T2** | Could be in extended SBE volumes or Vaishnava compilations; Müller mentions but does not include |
| 60 | Yogakuṇḍalinī | KYV | Y | T3 | Aiyar Yoga Upanishads vol. |
| 62 | Sarasvatī-rahasya | KYV | Sk | T4 | Shakta compilations |

### Samaveda missing (12)

| # | Name | Veda | Class | Tier | Recommended source |
|---|---|---|---|---|---|
| 65 | Āruṇi | SV | S | T2 | Aiyar Sannyāsa Upanishads vol. |
| 67 | Maitreyī | SV | S | T2 | Aiyar Sannyāsa Upanishads vol. |
| 69 | Yogachūḍāmaṇi | SV | Y | T3 | Aiyar Yoga Upanishads vol. |
| 70 | Vāsudeva | SV | Vs | T4 | Vaishnava compilations |
| 71 | Mahā | SV | V | T4 | Sectarian compilations |
| 72 | Sannyāsa | SV | S | T2 | Aiyar Sannyāsa Upanishads vol. |
| 73 | Avyakta | SV | Vs | T4 | Vaishnava compilations |
| 74 | Kuṇḍikā | SV | S | T2 | Aiyar Sannyāsa Upanishads vol. |
| 75 | Sāvitrī | SV | V | T4 | Sectarian compilations |
| 76 | Rudrākṣajābāla | SV | Sh | T4 | Shaiva compilations |
| 77 | Jābāli | SV | Sh | T4 | Shaiva compilations |
| 78 | Darśana | SV | Y | T3 | Aiyar Yoga Upanishads vol. |

### Atharvaveda missing (27)

| # | Name | Veda | Class | Tier | Recommended source |
|---|---|---|---|---|---|
| **81** | **Māṇḍūkya** | AV | **M** | **T1** | **Hume's Thirteen Principal Upanishads (1921) — top priority** |
| 82 | Atharvaśiras | AV | Sh | T4 | Shaiva compilations (Müller mentions) |
| 83 | Atharvaśikha | AV | Sh | T4 | Shaiva compilations (Müller mentions) |
| 84 | Bṛhajjābāla | AV | Sh | T4 | Shaiva compilations |
| 85 | Nṛsiṃhatāpani | AV | Vs | T2 | Vaishnava compilations (Müller mentions extensively) |
| 87 | Sītā | AV | Sk | T4 | Shakta compilations |
| 88 | Śarabha | AV | Sh | T4 | Shaiva compilations |
| 89 | Tripurātapani | AV | Sk | T4 | Shakta compilations |
| 90 | Devī | AV | Sk | T4 | Shakta compilations |
| 91 | Tripurā (AV) | AV | Sk | T4 | Shakta compilations |
| 92 | Bhāvanā | AV | Sk | T4 | Shakta compilations |
| 93 | Saubhāgya | AV | Sk | T4 | Shakta compilations |
| 94 | Sarasvatī-rahasya | AV | Sk | T4 | Shakta compilations |
| 95 | Rāmarahasya | AV | Vs | T4 | Vaishnava compilations |
| 96 | Rāmatāpaṇi | AV | Vs | T4 | Vaishnava compilations |
| 98 | Paramahaṃsa-parivrājaka | AV | S | T2 | Aiyar Sannyāsa Upanishads vol. |
| 99 | Annapūrṇā | AV | Sk | T4 | Shakta compilations |
| 100 | Sūrya | AV | V | T4 | Sectarian compilations |
| 101 | Ātmā | AV | V | T4 | Sectarian compilations |
| 102 | Pāśupatabrahma | AV | Sh | T4 | Shaiva compilations |
| 103 | Parabrahma | AV | V | T4 | Sectarian compilations |
| 104 | Avadhūta (AV) | AV | S | T4 | Sannyāsa / Aiyar Sannyāsa Upanishads vol. |
| 105 | Tripurā-tāpinī | AV | Sk | T4 | Shakta compilations |
| 106 | Devī (AV) | AV | Sk | T4 | Shakta compilations |
| 107 | Bhāvanā (AV) | AV | Sk | T4 | Shakta compilations |
| 108 | Mahāvākya | AV | V | T4 | Sectarian compilations |

## 4. Priority tiers

- **Tier 1 — complete principal canon (1 entry)**: Mandukya. The
  final missing Mukhya Upanishad. Acquisition closes the v103
  principal-completion target.
- **Tier 2 — high-value structural items (~13 entries)**:
  Muktikā (#29), Mahā-Nārāyaṇa (#59), Nṛsiṃhatāpani (#85), plus
  the canonical sannyāsa-class group (Jābāla, Paramahaṃsa, Āruṇi,
  Yajñavalkya, Avadhūta, Turīyātīta, Kuṇḍikā, Sannyāsa, Maitreyī,
  Sātyāyanī, Paramahaṃsa-parivrājaka). Most accessible through
  one source: Aiyar's *Sannyāsa Upanishads* (1914) volume.
- **Tier 3 — yoga cluster (~10 entries)**: Yogaśikhā,
  Yogakuṇḍalinī, Yogachūḍāmaṇi, Brahmavidyā, Kṣurikā,
  Trīśikhibrāhmaṇa, Maṇḍalabrāhmaṇa, Advayatāraka, Prāṇāgnihotra,
  Darśana, Nirvāṇa. One source: Aiyar's *Yoga Upanishads* (1938)
  volume — but copyright status post-1923 needs verification.
- **Tier 4 — sectarian clusters (~40 entries)**: Shaiva,
  Vaishnava, Shakta Upanishads. Lower-priority; require
  specialized compilations.
- **Tier 5 — unstable / lower-priority (~10 entries)**:
  Mudgala, Mantrikā, Pāingala, etc. — texts that appear mainly
  in lists.

## 5. Source family evaluation

### Hume — *The Thirteen Principal Upanishads* (1921, Oxford)

| | |
|---|---|
| Public domain | **Yes** (1921; >95 years; clearly PD in US) |
| In repo | No |
| Coverage | 13 principal Upanishads including **Mandukya** |
| Translation quality | Scholarly, well-edited; Sanskrit-aware |
| Parser difficulty | Medium — uses standard Upanishad numbering; should structure cleanly |
| Duplicates existing | Yes for 11 of 13 principals (Müller already has them); would be a second witness for those |
| Fills | **Mandukya** — the critical gap; potentially a richer principal witness for the others |
| Recommendation | **Primary source for v106** |

### Aiyar — *Sannyāsa Upanishads* (1914)

| | |
|---|---|
| Public domain | **Yes** (1914) |
| In repo | No |
| Coverage | Sannyāsa-class Upanishads (Jābāla, Paramahaṃsa, Kuṇḍikā, Āruṇi, Yajñavalkya, Avadhūta, Turīyātīta, Sannyāsa, Maitreyī, Paramahaṃsa-parivrājaka, Sātyāyanī, Nirvāṇa, Brahma, and more) |
| Translation quality | Same series + translator as the already-active *Thirty Minor* — known shape, known parser fit |
| Parser difficulty | Low — same Aiyar/SacredTexts ingestion pattern works |
| Duplicates existing | Brahmopanishad already active via Thirty Minor L1=34; would be a second witness |
| Fills | ~12 of the missing Tier-2 sannyāsa cluster in one ingestion |
| Recommendation | **Best Tier-2 single-source ingestion** |

### Aiyar — *Yoga Upanishads* (1938)

| | |
|---|---|
| Public domain | **Uncertain** — US PD cutoff is 1929 for life+95; needs verification of the specific 1938 publication |
| In repo | No |
| Coverage | Yoga-class Upanishads (Yogaśikhā, Yogakuṇḍalinī, Brahmavidyā, Kṣurikā, Trīśikhibrāhmaṇa, Maṇḍalabrāhmaṇa, Advayatāraka, Prāṇāgnihotra, Darśana, Yogachūḍāmaṇi, etc.) |
| Translation quality | Same Aiyar series |
| Parser difficulty | Low — Aiyar pattern |
| Recommendation | **Tier-3 ingestion AFTER copyright verification** — do not assume PD |

### Sacred Books of the East (Müller-edited Hindu volumes)

| | |
|---|---|
| Public domain | Yes |
| In repo | Already ingested as Müller Part 1 + Part 2 |
| Coverage | The 11 Müller principals + Maitri + Aitareya + commentary apparatus |
| Fills | **Already exhausted.** Müller explicitly omitted Mandukya. |
| Recommendation | No further extraction available from SBE alone |

### Aurobindo — *Upanishads* and related volumes (pub. ~1909-1920s)

| | |
|---|---|
| Public domain | Yes (most pre-1929) |
| In repo | No |
| Coverage | Isha, Kena, Katha, Mundaka, Mandukya (Aurobindo translated Mandukya), Taittiriya, Aitareya, Prashna, plus selected interpretations |
| Translation quality | Spiritual/interpretive rather than philological — distinct register; valuable as second witness |
| Parser difficulty | Medium — Aurobindo's structure varies by volume |
| Fills | **Includes Mandukya** — alternative to Hume |
| Recommendation | Secondary source; could fill Mandukya AND add interpretive witnesses for already-active principals |

### Nikhilananda — *Upanishads* (1949-1959)

| | |
|---|---|
| Public domain | **Uncertain** — post-1929; needs case-by-case verification |
| In repo | No |
| Coverage | All principal + Mandukya with Gaudapada Karika |
| Recommendation | Do not ingest without explicit PD verification |

### Source coverage matrix (compact)

| Tier | Best single source | Adds | Missing-74 reduction |
|---|---|---|---|
| T1 | Hume's 13 Principal Upanishads | Mandukya (+ optional 2nd witnesses for 11 principals) | 1 |
| T2 | Aiyar Sannyāsa Upanishads (1914) | Jābāla, Paramahaṃsa, Kuṇḍikā, Āruṇi, Yajñavalkya, Avadhūta, Turīyātīta, Sannyāsa, Maitreyī, Paramahaṃsa-parivrājaka, Sātyāyanī, Nirvāṇa | ~12 |
| T3 | Aiyar Yoga Upanishads (1938, PD-uncertain) | Yogaśikhā, Yogakuṇḍalinī, Brahmavidyā, Kṣurikā, Trīśikhibrāhmaṇa, Maṇḍalabrāhmaṇa, Advayatāraka, Prāṇāgnihotra, Darśana, Yogachūḍāmaṇi | ~10 |
| T4 | Multiple sectarian compilations | Shaiva / Vaishnava / Shakta clusters | ~40 |
| T5 | Mixed compilations | Hard-to-source residue | ~10 |

## 6. Recommended acquisition sequence

| Pass | Source | Adds | Cumulative coverage |
|---|---|---|---:|
| **v106** | Hume's Thirteen Principal Upanishads (1921) | Mandukya (+ optional second witnesses for 11 principals) | 35 / 108 (32%) |
| **v107** | Aiyar's Sannyāsa Upanishads (1914) | ~12 sannyāsa-class Upanishads | ~47 / 108 (44%) |
| v108 | Aiyar's Yoga Upanishads (1938, *after PD verification*) | ~10 yoga-class Upanishads | ~57 / 108 (53%) |
| v109+ | Sectarian compilations (Shaiva/Vaishnava/Shakta) | T4 cluster | ~95 / 108 (88%) |
| v110+ | Specialised / unstable | T5 residue | toward 108 |

## 7. Warnings

- **Mandukya Karika is NOT the Mandukya Upanishad.** Acquisition
  must include the 12 verses of the Upanishad proper, not only
  Gaudapada's Karika commentary. Hume's edition includes both
  but parses them as separate units.
- **Aiyar Yoga Upanishads (1938) copyright is uncertain.** Verify
  US PD status (life of author + 70 / 95 from publication) before
  ingestion.
- **Nikhilananda translations (post-1949)** are likely still
  in copyright. Skip unless explicit PD evidence emerges.
- **Don't double-count** Upanishads listed under multiple Vedas
  in different traditional sources — e.g. Mahā-Nārāyaṇa appears
  under both KYV and AV in some lists; use one canonical position
  (KYV / #59) per Muktikā.
- **Don't conflate the standalone Stotra with the Upanishad.**
  `dakshinamurti-stotra` is a hymn, not the Dakshinamurti
  Upanishad — those are distinct texts.
- **List/footnote mentions never count as text.** A name appearing
  in Müller Part 2's bibliography is documentation that the
  Upanishad exists, not that Müller translated it.

## 8. What v105 did NOT do

- No new JSON files added.
- No new active witnesses.
- No UI changes.
- No source-text passages modified.
- The 108 gap map (v104) is unchanged; the disclosure still shows
  74 not yet in archive.
- Mandukya status card (v103) preserved.

## 9. App state preserved

- Page-type doctrine (shelf scrolls, contents leaf static,
  reading room scrolls): unchanged
- Three Upanishads-family views (By Veda / By text / Traditional):
  unchanged
- Witness picker + Muktikā count badges + 108 gap disclosure:
  unchanged
- Atlas Object / Folio / companion mode: untouched
- Bible, Tao, Gita, Iliad, Odyssey, other family flows: untouched

The build marker advances to `v105-upanishads-missing-74-plan` to
record that this pass is a planning report only.
