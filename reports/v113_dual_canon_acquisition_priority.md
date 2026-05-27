# v113 — Dual-canon acquisition pass: Dakshinamurti recovered

The v112 dual canon-map architecture made it possible to define a
new acquisition priority: Upanishads **missing from both canons**.
Adding such a text increases coverage in either canon regardless
of which becomes primary later.

v113 builds the missing-in-both intersection (54 entries), does a
deep local audit of non-Aiyar Hindu sources, and recovers
**Dakshinamurti Upanishad** as a single safe new route from an
in-archive 1920 source. External pre-1929 PD English search
produced no new batch sources beyond what was documented in v110.

## 1. Current state

| Field | Before v113 | After v113 |
|---|---:|---:|
| Build marker | `v112-dual-muktika-canon-map` | **`v113-dual-canon-acquisition-batch`** |
| Primary `MUKTIKA_108` active | 42 / 108 | **43 / 108** |
| Aiyar `MUKTIKA_108_AIYAR` active | 42 / 108 | **43 / 108** |
| Missing in primary | 66 | **65** |
| Missing in Aiyar | 66 | **65** |
| Missing in BOTH | 54 | **53** |
| byUpanishad routes | 43 | **44** |
| Varāha variant-canon status | unchanged | unchanged |
| Hume second-witness status | unchanged | unchanged |

## 2. Dual-missing intersection (54 entries, before v113)

Computed by the audit script `05_scripts/v113_dual_missing_intersection.py`
(matches by normalized name across both canon arrays). The 54
entries break down by class as follows (using primary's class
assignments):

| Class | Count | Examples |
|---|---:|---|
| Sannyāsa (S) | 12 | Nirvāṇa, Jābāla, Paramahaṃsa, Advayatāraka, Turīyātīta, Yājñavalkya, Sātyāyanī, Avadhūta, Āruṇi, Maitreyī, Kuṇḍikā, Paramahaṃsa-parivrājaka |
| Shaiva (Sh) | 8 | Akṣamālā, Kālāgnirudra, **Dakṣiṇāmūrti**, Rudrahṛdaya, Pañcabrahma, Atharvaśiras, Atharvaśikhā, Śarabha, Pāśupatabrahma |
| Shakta (Sk) | 9 | Bahvṛca, Sarasvatī-rahasya, Sītā, Annapūrṇā, Tripurā, Devī, Bhāvanā, Tripurā-tāpinī, Saubhāgya |
| Yoga (Y) | 6 | Trīśikhibrāhmaṇa, Kṣurikā, Brahmavidyā, Yogaśikhā, Yogachūḍāmaṇi, Darśana |
| Vaishnava (Vs) | 5 | Nṛsiṃhatāpani, Mahā-Nārāyaṇa, Vāsudeva, Rāmarahasya, Rāmatāpaṇi |
| sāmānya Vedānta (V) | 10 | Mudgala, Mantrikā, Śukarahasya, Ekākṣara, Akṣi, Prāṇāgnihotra, Sūrya, Ātmā, Parabrahma, Mahāvākya |
| Total | **54** | |

(After v113 Dakshinamurti activation: 53 remaining.)

The 54 are the highest-acquisition-priority set because each is
unambiguous: not a recension dispute, just unfound text.

## 3. Non-intersection differences

These 21 differences sit outside the missing-in-both set:

### 3.1 Missing only in primary (7)

Primary lists these but they're either in Aiyar's active list, in
Aiyar at a different Veda, or are primary-canon idiosyncrasies:

| Primary # | Name | Status in Aiyar |
|---:|---|---|
| 9 | Saubhāgyalakṣmī (RV) | longer modern name for Aiyar's "Saubhāgya" (RV #9) |
| 54 | Kaṭharudra (KY) | NOT in Aiyar 108 |
| 71 | Mahā (SV) | possibly one half of Aiyar's Mahat-Sannyāsa split |
| 72 | Sannyāsa (SV) | possibly second half of Aiyar's Mahat-Sannyāsa split |
| 76 | Rudrākṣajābāla (SV) | hybrid of Aiyar's Rudrākṣa + Bhasma-Jābāla? not in Aiyar |
| 84 | Bṛhajjābāla (AV) | = Aiyar's Bṛhad-Jābāla via sandhi (Aiyar #83) — same Upanishad |
| 89 | Tripurātapani (AV) | matches Aiyar's Tripura-tāpinī (AV #98) |

### 3.2 Missing only in Aiyar (12)

Aiyar lists these but the primary canon does not include them
under any spelling:

| Aiyar # | Name | Class | Veda |
|---:|---|---|---|
| 54 | Kara | Y | KY (no English translation found anywhere) |
| 70 | Mahat-Sannyāsa | S | SV (apparent ancestor of primary's Mahā + Sannyāsa split) |
| 74 | Rudrākṣa | Sh | SV |
| 75 | Jābāla (Sāmaveda) | S | SV (second Jābāla, distinct from #13) |
| 83 | Bṛhad-Jābāla | Sh | AV (= primary's Bṛhajjābāla #84 via sandhi) |
| 101 | Bhasma-Jābāla | Sh | AV |
| 102 | Gaṇapati | Sh | AV |
| 104 | Gopāla-tāpanī | Vs | AV |
| 105 | Kṛṣṇa | Vs | AV |
| 106 | Hayagrīva | Vs | AV |
| 107 | Dattātreya | Vs | AV |
| 108 | Garuḍa | Vs | AV |

The Atharvaveda Vaishnava cluster (#102–108) is Aiyar-only as a
*group*; primary canon's AV section ends with Mahāvākya #108
without these Vaishnava-class entries.

### 3.3 Active only in primary (1)

| Primary # | Name | Veda |
|---:|---|---|
| 66 | Maitreya | SV (key='maitreya' in byUpanishad, routes to Aiyar L1=6) |

Aiyar's #66 SV is "Maitreyī" (with diacritic) — different
Upanishad. The Maitreya/Maitreyī distinction in primary is a
recension-difference issue.

### 3.4 Active only in Aiyar (1)

| Aiyar # | Name | Veda |
|---:|---|---|
| 59 | Varāha | KY (key='varaha' in byUpanishad — v111 variant-canon addition) |

## 4. Local deep audit results

### 4.1 Sources audited (Hindu, non-Aiyar)

| Source | hierarchy | Hidden Upanishads found |
|---|---|---|
| `upanishads` (Müller complete merged) | `[chapter, verse]`, 1831 passages | None — uses principal-Upanishad L1 keys directly (chandogya/brihadaranyaka/etc.) already routed |
| `upanishads-muller-part1` (SBE I) | 17 L1 chapters with editorial/preface chrome | None — principal Upanishads only, no minors |
| `upanishads-muller-part2` (SBE XV) | 6 L1 chapters | None — Katha, Mundaka, Maitrayana-Brahmana (= Maitri); already routed |
| `upanishads-johnson` (Charles Johnston 1899) | 12 L1 chapters — "In the House of Death", "A Vedic Master", "That Thou Art" | None — Theosophical retranslations of Katha, Kena, Chandogya (already routed) |
| `the-upanishads-max-muller-1879` (legacy reprint) | duplicate of Müller content | None new |
| `vedanta-sutras-sankara` (Sankara's Brahma-Sutra Bhasya, Thibaut tr.) | commentary not Upanishad | Upanishads QUOTED extensively but no full-text routes — per principle, commentary mentions don't count |
| `vedanta-sutras-ramanuja` (Ramanuja's BSB) | commentary not Upanishad | same — quotations only |
| **`dakshinamurti-stotra`** (Sastri 1920) | 16 L1 chapters | **★ Dakshinamurti Upanishad at L1=16 (full English text)** |

### 4.2 The Dakshinamurti finding

Alladi Mahadeva Sastri's *Dakshinamurti Stotra (with the Vedanta
Doctrine of Sankaracharya as Expounded by Suresvaracharya in His
Manasollasa and Pranava Vartika)* was published by the Theosophical
Society Press at Adyar in 1920. The volume's main subject is
Sankaracharya's hymn (Stotra) and Suresvaracharya's commentary.
But **Section III** of the volume — printed as L1=16 in the
archive's `dakshinamurti-stotra` source — is the **full English
translation of the Dakshinamurti Upanishad itself**, opening with
the canonical Krishna Yajurveda shanti mantra:

> *"May (Brahman) protect us both! May He give us both to enjoy!
> Efficiency may we both attain! Effective may our study prove!
> Hate may we not (each other) at all! Peace! Peace!! Peace!!!
> Amen!"*

followed by the Markandeya-Sanaka dialogue about Dakshinamukha
Siva ("In the Brahmavarta, at the foot of a mighty bhandira fig
tree, there assembled Sanaka and other mighty sages for a great
sacrifice…").

This Upanishad is:
* Missing in primary `MUKTIKA_108` #47 (Krishna Yajurveda, Shaiva
  class)
* Missing in Aiyar `MUKTIKA_108_AIYAR` #47 (same)
* Not present in Aiyar's *Thirty Minor* source.

Activating it improves coverage in **both** canons simultaneously.

### 4.3 Sastri 1920 PD status

* **First publication**: 1920, Theosophical Society Press, Adyar
  (India).
* **US public-domain status**: PD by date of publication (pre-1929
  → US PD regardless of URAA).
* **Translator**: Alladi Mahadeva Sastri (ca. 1857–1925), Sanskrit
  scholar at the Mysore Oriental Library. Died ~1925; life+70 → 1995
  (Indian PD in 1985 under earlier life+60). On 1996-01-01 (URAA
  cutoff) the work was already in PD in India — so URAA did NOT
  restore US copyright.
* **Conclusion**: Sastri 1920 is **safely PD in the US** for
  archive publication. No restricted-source protocol applies.

### 4.4 What does NOT exist in the archive

* No Theosophical Quarterly back-issue caches.
* No Annie Besant Sanatana Dharma volumes.
* No Vivekananda complete works (Karma-Yoga 1921 is the only
  Vivekananda text and is in raw-source cache only, not ingested).
* No Swami Paramananda translations (Paramananda translated
  several short Upanishads 1909–1916; the archive does not
  currently cache his volumes).
* No Sitaram Sastri Aitareya/Taittiriya volumes (1898–1899,
  already covered by Müller/Hume).
* No older Adyar Bulletin issues.

Acquisition of any of the above would be **v114+** work and
requires verifying PD status per the v109 protocol.

## 5. Source-family evaluation (external — no ingestion)

| Source | Year | Translator | PD status | Texts covered | Decision |
|---|---:|---|---|---|---|
| **Sastri 1920** *Dakshinamurti Stotra* | 1920 | A. Mahadeva Sastri | **PD-safe** | Dakshinamurti Upanishad (+ Stotra and Pranava-Vartika commentaries, not Upanishads) | **INGEST** (route already added) |
| Adyar Library Saiva Upanishads | 1935 | T.R. Srinivasa Ayyangar | URAA-restricted till 2031 | Akṣamālā, Kālāgnirudra, Rudrahṛdaya, Pañcabrahma, Atharvaśiras, Atharvaśikhā, Bṛhad-Jābāla, Śarabha, Pāśupata-brahma, Bhasma-Jābāla, Gaṇapati, Jābāli + others | DEFER → 2031 |
| Adyar Library Vaishnava Upanishads | 1945 | T.R. Srinivasa Ayyangar | URAA-restricted till 2041 | Nṛsiṃhatāpani, Vāsudeva, Avyakta, Mahā-Nārāyaṇa, Rāmarahasya, Rāmatāpaṇi, Gopāla-tāpanī, Kṛṣṇa, Hayagrīva, Dattātreya, Garuḍa | DEFER → 2041 |
| Adyar Library Shakta Upanishads | 1950 | A.G. Krishna Warrier | URAA-restricted till 2046 | Bahvṛca, Sarasvatī-rahasya, Sītā, Annapūrṇā, Tripurā, Devī, Bhāvanā, Tripurā-tāpinī, Saubhāgya | DEFER → 2046 |
| Adyar Library Samanya-Vedanta Upanishads | 1941 | T.R. Srinivasa Ayyangar | URAA-restricted till 2037 | Mudgala, Mantrikā, Śukarahasya, Ekākṣara, Akṣi, Prāṇāgnihotra, Sūrya, Ātmā, Parabrahma, Mahāvākya + others | DEFER → 2037 |
| Adyar Library Yoga Upanishads | 1938 | T.R. Srinivasa Ayyangar | URAA-restricted till 2034 | Trīśikhibrāhmaṇa, Kṣurikā, Brahmavidyā, Yogaśikhā, Yogachūḍāmaṇi, Darśana | DEFER → 2034 |
| Adyar Library Samnyāsa Upanishads | 1978 | A.A. Ramanathan | Active US copyright till 2074 | Nirvāṇa, Jābāla, Paramahaṃsa, Advayatāraka, Turīyātīta, Yājñavalkya, Sātyāyanī, Avadhūta, Āruṇi, Maitreyī, Kuṇḍikā, Paramahaṃsa-parivrājaka + others | DEFER → 2074 |
| Marabathina 2024 *108 Upanishads* | 2024 | Marabathina | Active copyright till 2120 | All 108 | DEFER → 2120 |
| Deussen *Sechzig Upanishads des Veda* | 1897 | Paul Deussen | PD but German-only | 60 Upanishads (many missing-in-both) | REJECT (German, not English reading witness) |
| Adyar Sanskrit-only volumes (Mahadeva Sastri 1925, Chintamani Dikshit 1929) | 1925-1929 | Adyar | PD but Sanskrit-only | Shaiva and Sannyasa clusters | REJECT (Sanskrit-only, not English witnesses) |
| Theosophist back-issues (1879-1928) | various | Judge, Besant, Chatterji, etc. | PD | scattered individual minor translations | Possible v114+ micro-search, not in v113 scope |

## 6. Ingestion summary

### 6.1 New byUpanishad route

```js
{ key: 'dakshinamurti', name: 'Dakṣiṇāmūrti', displayTitle: 'Dakṣiṇāmūrti Upanishad',
  importance: 'minor', order: 293,
  associatedVeda: 'Krishna Yajurveda', vedaSource: 'curated traditional metadata',
  witnesses: [
    { textId: 'dakshinamurti-stotra', groupKey: '16',
      sourceTitle: 'Dakshinamurti Stotra (with Vedanta Doctrine of Sankaracharya)',
      translator: 'Alladi Mahadeva Sastri', year: '1920',
      role: 'primary', routeQuality: 'safe-start',
      note: '...' },
  ] },
```

### 6.2 Canon-map updates (both canons)

```js
// MUKTIKA_108 (primary)
{ n:47, key:'dakshinamurti', name:'Dakṣiṇāmūrti', veda:'Krishna Yajurveda', cls:'Sh', ... }
// was: key:null

// MUKTIKA_108_AIYAR
{ n: 47, key:'dakshinamurti', name:'Dakṣiṇāmūrti', veda:'Krishna Yajurveda', cls:'Sh' }
// was: key:null
```

### 6.3 members[] addition

Added `dakshinamurti-stotra` to `TEXT_FAMILIES.upanishads.members` as
a `source-volume` role (since the volume is primarily a Stotra
commentary; only one of its 16 sections is the Upanishad itself).

### 6.4 No new files

* No new data file (existing `data/dakshinamurti-stotra_sastri.json`
  reused)
* No new parser script (the source was already ingested into the
  archive in an earlier non-Upanishad pass)
* No new entry in `data/index.json` (existing
  `dakshinamurti-stotra` entry reused)
* No new gzip needed

### 6.5 Count results

| Metric | Before | After |
|---|---:|---:|
| Primary active | 42 / 108 | **43 / 108** |
| Primary missing | 66 | 65 |
| Aiyar active | 42 / 108 | **43 / 108** |
| Aiyar missing | 66 | 65 |
| Missing in BOTH | 54 | **53** |

The primary and Aiyar counts both advance by 1 (Dakshinamurti is
at #47 in both canon arrays). Net family-page change: the Krishna
Yajurveda count badge will go from 15 / 32 to 16 / 32.

## 7. Deferred / restricted sources

**No restricted full text was committed in v113.** The Adyar
Library English Series volumes (1935–1978) and the Marabathina
2024 volume remain documented but unaccessed. No `_restricted/`
files were created.

The Adyar Library Saiva Upanishads (1935, Ayyangar tr.) is the
highest-value future acquisition for the Shaiva cluster (which
still has 7 missing-in-both entries: Akṣamālā, Kālāgnirudra,
Rudrahṛdaya, Pañcabrahma, Atharvaśiras, Atharvaśikhā, Pāśupatabrahma,
Śarabha), but enters US PD only in 2031.

## 8. Next recommendation (v114+)

### v114: Theosophist back-issue micro-acquisition

The most likely productive pre-PD source for additional missing-
in-both Upanishads is the *Theosophist* journal (1879-onwards,
all pre-1929 issues are PD). Individual translations of small
Upanishads occasionally appeared in *Theosophical Quarterly* and
related Theosophist publications:

* Charles Johnston published translations of some Vedanta-class
  Upanishads in *Theosophical Quarterly* 1906-1914 — already
  partially reflected in the archive's `upanishads-johnson` source
  but possibly with more material in original journal back-issues.
* J.C. Chatterji translated minor Upanishads in the *Indian
  Antiquary* and similar journals.
* William Quan Judge published *Theosophist* articles 1880-1896
  that included some Upanishad translations.

A v114 acquisition pass would:
1. Survey Internet Archive's *Theosophist* / *Theosophical
   Quarterly* / *Indian Antiquary* digitized back-issues.
2. Index any English Upanishad translations against the missing-
   in-both list.
3. Ingest individual short Upanishads as discrete one-text data
   files (similar to v113's Dakshinamurti pattern).

Realistic expectation: +1 to +5 entries — modest, but per the
v113 principle "prioritize missing-in-both texts," each is a clean
dual-canon win.

### v115+: Swami Paramananda volumes

Swami Paramananda (Vedanta Society of America) published several
short Upanishad translations 1909–1916:
* *The Mundaka Upanishad* (1911)
* *The Maitrayana Brahmana Upanishad* (1912)
* *Self-Knowledge: Atma-Bodha* (1911) — possibly contains the
  Ātma-bodha Upanishad text
* *The Vedanta in Practice* (1915)

These are PD-safe. Most overlap with already-routed principals, but
the Atma-bodha Upanishad (RV #4 active in both canons) might gain
a second witness; and any minor-Upanishad text Paramananda
translated could become a new route.

### v116+: Adyar Library 1935 Saiva → 2031 trigger

Schedule an automatic 2031-01-01 acquisition trigger for the
Ayyangar 1935 Saiva Upanishads volume. That alone would close
seven missing-in-both entries (the entire Shaiva cluster minus
Dakshinamurti, now done).

## 9. Non-destructive guarantees

* **No JSON files merged, rewritten, or deleted.**
* **No new external source ingested.** Sastri 1920 was already in
  the archive from an earlier non-Upanishad pass.
* **No restricted text committed.**
* **No public routes to restricted text.**
* **No UI redesign.** Added one byUpanishad entry, updated one
  member entry, flipped two `key:null → key:'dakshinamurti'`
  values. No layout, view, or witness-picker code changed.
* **No folio / Atlas-Object work.**
* **Canon model unchanged.** Model C (dual canon-map) from v112
  preserved; both maps' totals stay at 108.

## 10. Build marker

`v112-dual-muktika-canon-map` → **`v113-dual-canon-acquisition-batch`**

The marker reflects the first acquisition pass under the dual-canon
architecture: one Upanishad missing in both canons recovered from an
in-archive PD source, with no canon-model changes.
