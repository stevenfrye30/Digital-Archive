# v108 — Yoga Upanishads source hunt: acquisition needed

A thorough source hunt for a public-domain English Yoga Upanishads
compilation found no usable candidate. **The only English
compilations (Ayyangar / Adyar Library, 1935 and 1938) are post-1929
and not yet in US public domain;** older sources are Sanskrit-only.
v108 ships as planning-only.

## 1. Summary

| Metric | Value |
|---|---:|
| Muktikā 108 coverage before v108 | 36 / 108 (33%) |
| Muktikā 108 coverage after v108  | **36 / 108 — unchanged** |
| Active witnesses added in v108  | **0** (no clean source) |
| Yoga-class targets identified   | 7 missing |
| Yoga-class targets ingested     | 0 |
| Source candidates evaluated     | 6 |
| Source candidates accepted      | 0 |
| Source candidates deferred (PD-uncertain) | 2 |
| Source candidates rejected (modern copyright) | 2 |
| Source candidates rejected (Sanskrit-only) | 2 |

## 2. Yoga-class target table

Confirmed by extracting MUKTIKA_108 entries with `cls === 'Y'`. Each
already-active entry uses Aiyar's Thirty Minor at the noted L1 key.

| Muktikā # | Upanishad | Veda | Status | Active witness |
|---:|---|---|---|---|
| 6  | Nādabindu      | Rigveda           | **active** | Aiyar L1=68 |
| 14 | Haṃsa          | Shukla Yajurveda  | **active** | Aiyar L1=57 |
| 20 | Maṇḍalabrāhmaṇa| Shukla Yajurveda  | missing    | — |
| 37 | Amṛtabindu     | Krishna Yajurveda | **active** | Aiyar L1=10 |
| 38 | Amṛtanāda      | Krishna Yajurveda | **active** | Aiyar L1=58 |
| 40 | Kṣurikā        | Krishna Yajurveda | missing    | — |
| 43 | Tejobindu      | Krishna Yajurveda | **active** | Aiyar L1=28 (v104) |
| 44 | Dhyānabindu    | Krishna Yajurveda | **active** | Aiyar L1=56 |
| 45 | Brahmavidyā    | Krishna Yajurveda | missing    | — |
| 46 | Yogatattva     | Krishna Yajurveda | **active** | Aiyar L1=55 |
| 50 | Yogaśikhā      | Krishna Yajurveda | missing    | — |
| 60 | Yogakuṇḍalinī  | Krishna Yajurveda | missing    | — |
| 69 | Yogachūḍāmaṇi  | Samaveda          | missing    | — |
| 78 | Darśana        | Samaveda          | missing    | — |
| 97 | Śāṇḍilya       | Atharvaveda       | **active** | Aiyar L1=51 |

**Currently active: 8 of 15 Yoga-class.**
**Targets for v108: 7 missing** (Maṇḍalabrāhmaṇa, Kṣurikā, Brahmavidyā,
Yogaśikhā, Yogakuṇḍalinī, Yogachūḍāmaṇi, Darśana). None of these
appear in Aiyar's Thirty Minor; all 70 L1 keys of that source are
already accounted for after v104 (Subāla/Tejobindu) and v107 (Muktikā).

## 3. Source candidate evaluation

Internet Archive query `"Yoga Upanisads" OR "Yoga Upanishads"`
returned 24 candidates. Detail of each:

### A. T.R. Srinivasa Ayyangar — *The Yoga Upaniṣads* (Adyar Library)

| IA identifier | Year | Language | Verdict |
|---|---:|---|---|
| `in.ernet.dli.2015.283885` | **1935** | English | **Defer (PD-uncertain)** |
| `the-yoga-upanisads` | **1938** | English | **Defer (PD-uncertain)** |
| `TheYogaUpanisadsSanskritEngish1938Text` | 1938 | English (with Sanskrit) | Defer (same edition as above) |
| `yoga-upanisads-engish-tr-srinivasa-ayyangar-1938` | 1938 | English | Defer (same edition) |
| `in.gov.ignca.7881` | 1952 | English | **Reject (post-1977 PD threshold; clearly copyrighted)** |
| `TheYogaUpanishads` | undated | English | Defer (likely a reprint of Ayyangar) |

**Public-domain analysis (US):**

Under the US Copyright Term Extension Act, works published 1929-1977
enter PD 95 years from publication. Therefore:

  · 1929 publications → PD on Jan 1, 2025
  · 1935 publications → PD on Jan 1, 2031
  · 1938 publications → PD on Jan 1, 2034
  · 1952 publications → PD on Jan 1, 2048

**Ayyangar's 1935 and 1938 editions are NOT in US public domain.**
A 1929-1963 work can be in PD earlier if the copyright was not
renewed in its 28th year, BUT this requires an actual US Copyright
Office renewal-records check. Adyar Library is an Indian publisher;
US renewal status would need to be verified item-by-item against
the *Catalog of Copyright Entries — Renewals* (or via the Stanford
Copyright Renewal Database / CCE search at copyright.gov).

**Without that affirmative non-renewal evidence, the conservative
v108 decision is to defer Ayyangar 1935/1938.**

### B. Pandit A. Mahadeva Sastri — *The Yoga Upanishads* (Adyar Library)

| IA identifier | Year | Language | Verdict |
|---|---:|---|---|
| `in.ernet.dli.2015.448309` | 1920 | **Sanskrit** | Reject — Sanskrit only |
| `in.ernet.dli.2015.345354` | 1920 | **Sanskrit** | Reject — Sanskrit only |
| `the-yoga-upanishads` | 1920 | **Sanskrit** | Reject — Sanskrit only |
| `ksu.1275.yogaupanishads0000pand` | 1920 | **Sanskrit** | Reject — Sanskrit only |
| `wg1249` | 1920 | **Sanskrit** | Reject — Sanskrit only |

**Status:** US public domain (1920 publications well past 95-year
threshold). **Verdict: rejected** because the language code is "san"
(Sanskrit). The archive's reading room expects English translation
text; a Sanskrit-only source does not satisfy the reading-room
contract. Sanskrit text would only be useful as a parallel-text
addition, which is out of v108's scope.

### C. Schrader/Adyar Library Sanskrit + commentary editions

| IA identifier | Year | Language | Verdict |
|---|---:|---|---|
| `oAhs_the-yoga-upanishads-with-sri-upanishad-brahma-yogi` | undated | unknown | Likely Sanskrit + Sanskrit commentary — reject |
| `Xdck_the-yoga-upanishads-with-the-commentary-of-shri-up` | undated | Sanskrit | Reject |
| `tdl.58979-the-yoga-upanishads-with-the-commentary-of-sr` | undated | Tamil | Reject |
| `108UpanishadsWithUpanishadBrahmamCommentary` | undated | Sanskrit | Reject |
| `108_Upanishads_with_Sanskrit_Commentary_of_Upanishad_Br` | undated | English label / Sanskrit content | Reject — same Sanskrit material |

### D. Modern English sources (rejected — copyright)

| IA identifier | Year | Verdict |
|---|---:|---|
| `108-upanishads-the-order-as-given-in-the-muktika-upanishad` | 2024 | Reject (modern, copyrighted) |
| `english-108-upanishads-the-order-as-given-in-the-muktik` | 2024 | Reject (modern, copyrighted) |
| `yogatraditionits0000feue` (Feuerstein) | 2008 | Reject (modern, copyrighted) |
| `49-yoga-its-practice-philosophy-according-to-the-upanis` (Chhawchharia) | undated | Reject (modern, copyrighted) |
| `new-perspectives-on-advaita-vedanta-essays-in-commemora` (Malkovsky) | undated | Reject (modern, copyrighted) |
| `yoga-darshan-vision-of-the-yoga-upanishads-2026-04-01-t` | 2026 | Reject (modern, copyrighted) |

### E. Individual Upanishad translations (older English)

Searches for `"Yogashikha"` / `"Yogakundalini"` / `"Brahmavidya Upanishad"` /
`"Kshurika"` / `"Darshana Upanishad"` AND "English" on Internet Archive
returned only the same Marabathina 2024 modern volumes — no older,
public-domain English standalone translations of these specific
Yoga-class Upanishads appear to exist on IA.

### F. Local repo (final check)

| Path | Yoga-Upanishad content? |
|---|---|
| `02_raw_sources/Library_/Gutenberg.org/An Introduction to Yoga_____Annie Besant.txt` | No — Besant's introduction to yoga philosophy, not Yoga Upanishads |
| `02_raw_sources/Library_/Gutenberg.org/Jnâna Yoga - Part 2_____Swami Vivekananda.txt` | No |
| `02_raw_sources/Library_/Gutenberg.org/The Yoga Sutras of Patanjali_____Charles Johnson.txt` | No — Patanjali, not Yoga Upanishads |
| `02_raw_sources/Library_/Gutenberg.org/The Yoga-Vasishtha Maharamayana of Valmiki - Vol *.txt` | No |
| `01_library/library/texts/sacred/hindu/` | No Yoga-Upanishads directory |
| `03_web_app/data/upanishads-30-minor-aiyar_aiyar.json` | Contains the 8 Yoga-class already active; does NOT contain the 7 missing |

## 4. Public-domain verification

US copyright analysis was the determining factor for v108. Detail:

- **1929 cutoff:** US works published before 1929 are in PD under the
  Copyright Term Extension Act + Sonny Bono Act, life+95 rule.
- **1929-1963 renewal:** US-published works in this window enter PD if
  not renewed at year 28; foreign-published works generally remain
  copyrighted unless they were public domain in their source country
  on 1 January 1996 (the URAA date).
- **India and the URAA:** Works published in India that were not in
  PD in India on 1996-01-01 had their US copyright restored under
  URAA. Indian PD rule is life+60 of the author.
- **Adyar Library 1935/1938 specifically:** T.R. Srinivasa Ayyangar
  (1879–1949 according to common records). Life+60 = 2009. **Therefore
  works by Ayyangar are PD in India as of 2010 forward, but were NOT
  PD in India on 1 January 1996, so URAA restored their US copyright
  for 95 years from publication.**

**Final verdict for Ayyangar 1935 and 1938: US copyright restored
under URAA; not in US PD until 2031 and 2034 respectively.** This
defers ingestion until either:

  · those dates pass (2031 / 2034), or
  · an explicit non-renewal / PD-determination from the US Copyright
    Office is documented, or
  · the archive's host jurisdiction's PD rules change.

## 5. Remaining Yoga-class gaps

The 7 missing Yoga-class Upanishads remain inactive:

| Muktikā # | Upanishad | Source for future acquisition |
|---:|---|---|
| 20 | Maṇḍalabrāhmaṇa | Ayyangar 1935/1938 (after PD), Mahadeva Sastri Sanskrit + translation work |
| 40 | Kṣurikā          | Ayyangar 1935/1938 (after PD) |
| 45 | Brahmavidyā      | Ayyangar 1935/1938 (after PD) |
| 50 | Yogaśikhā        | Ayyangar 1935/1938 (after PD) |
| 60 | Yogakuṇḍalinī    | Ayyangar 1935/1938 (after PD) |
| 69 | Yogachūḍāmaṇi    | Ayyangar 1935/1938 (after PD) |
| 78 | Darśana          | Ayyangar 1935/1938 (after PD) |

## 6. Revised acquisition plan (post-v108)

The v105 plan's v108 entry ("Aiyar Yoga Upanishads 1938 → ~10 yoga,
post-PD-verify") is **not safe to act on without explicit non-renewal
evidence.** v108 confirms the deferral.

Updated acquisition sequence:

| Pass | Source | Notes |
|---|---|---|
| v109 | **Sectarian compilations — Shaiva / Vaishnava / Shakta** | Same PD-verification caveats apply. Most likely sources: Adyar Library English series (1925 Sakta, 1953 Saiva, others), all post-1929. Likely defer. |
| v110 | **Hume 1921 second-witness extraction** for principal Upanishads (Brihadaranyaka, Chandogya, Aitareya, etc.) using the already-cached `Hume-1921-Thirteen-Principal-Upanishads.txt` | NOT new Muktikā 108 entries (those are already active via Müller); would only enrich the witness picker. Lower 108-coverage value but no copyright issues. |
| 2031 | Auto-PD: Ayyangar 1935 Yoga Upanishads → ingest the 7 missing Yoga-class | Wait |
| 2034 | Auto-PD: Ayyangar 1938 Yoga Upanishads (if 1938 is the canonical edition) | Wait |
| Anytime | Any pre-1929 individual Upanishad translation that surfaces | Opportunistic |
| Anytime | Verified non-renewal of a specific 1929-1963 Yoga Upanishads work via US Copyright Office records | Conservative path forward |

## 7. Rights cautions documented

For future passes:

  · **Adyar Library (Theosophical Society, India) Upanishads series**
    — many editions in the 1920s-1950s. Pre-1929 (e.g., 1920 Sastri
    Sanskrit) is PD but rarely contains English. Post-1929 (1935
    Ayyangar English, 1953 Saiva, etc.) is URAA-restored and NOT
    in US PD until 95 years from publication.
  · **Theosophical Society publications (Madras / Adyar / Wheaton)**
    — same analysis: pre-1929 PD, post-1929 deferred.
  · **Ramakrishna Mission / Nikhilananda translations** — post-1949,
    still copyrighted.
  · **Modern self-published or Marabathina 2024 editions** — definitively
    copyrighted; cannot be used.

## 8. App state preserved

- No JSON files added, modified, merged, or deleted.
- No new active witnesses.
- No UI changes.
- The Muktikā 108 disclosure still shows "36 active · 72 not yet".
- All other archive flows untouched.

## 9. Build marker

`v107-muktika-extracted-sannyasa-acquisition-needed`
→ **`v108-yoga-acquisition-needed`**

The marker honestly reflects the pass's outcome: a thorough source
hunt that did not yield a safely-ingestible source. The Yoga
Upanishads remain a known gap; the path forward is documented above.
