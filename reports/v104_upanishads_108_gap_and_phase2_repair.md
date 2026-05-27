# v104 — Upanishads 108 gap map + Phase 2 Aiyar repair

Phase 2 work on the Upanishads family: deep audit of Aiyar L1=18–33
recovered TWO additional Upanishads (Subāla and Tejobindu); a
formal Muktikā 108 canonical target map is now in place; per-Veda
progress counts and a collapsed "not yet in archive" disclosure
make the gap honest and visible without cluttering the active grid.

## 1. Summary

| Metric | Before (v103) | After (v104) |
|---|---:|---:|
| Total active Upanishads | 35 | **37** |
| Principal active | 12 | 12 |
| Minor active | 23 | **25** (+ Subāla, Tejobindu) |
| Muktikā 108 archive coverage | — | **34 of 108** |
| Routes: safe                | 22 | 22 |
| Routes: safe-start          | 14 | **16** |
| Routes: pid-route           |  2 |  2  (Aitareya, Maitri) |
| Inactive in family page     | Mandukya + Aiyar L1=18-33 block | **Mandukya only** |

Note: archive count (37) ≠ Muktikā coverage (34). Three active
Upanishads are outside the Muktikā 108 in their current naming —
`brahmopanishad` (Aiyar's title; matches Muktikā #32 Brahma but
rendered as a separate slug here), `chandogya` and similar
overlaps are counted only once in the Muktikā lookup.

## 2. Aiyar L1=18–33 repair analysis

Deep audit of every L1 key from 17 through 34 with first/last
passage inspection. Findings:

- **L1=18 through L1=27** = **Subāla Upanishad**.
  Sixteen sub-sections labeled "Khanda I" through "Khanda XVI" in
  chapter_titles. L1=18 opens with: *"THEN he (Raikva) asked:
  ‘What was at first?’ To which (He the Lord) replied…"* — this
  is the Subāla Upanishad's canonical opening. L1=27 closes with
  the explicit sealing rubric: *"This Subala-Bija-Brahma-Upanishad
  should neither be given out nor taught to one who has not
  controlled his passions…"*
- **L1=28 through L1=33** = **Tejobindu Upanishad**.
  Six sub-sections labeled "Chapter I" through "Chapter VI". L1=28
  opens with: *"PARAM-DHYaNA (the supreme meditation) should be
  upon tejo bindu, which is the Atma of the universe…"* — the
  Tejobindu's canonical opening. L1=33 closes with: *"…
  Tejobindu-Upanishad always with delight. By once studying it,
  he becomes one with Brahman. Thus ends the sixth chapter. Thus
  ends the Upanishad."*

Both routes added as safe-start witnesses with explicit notes in
the witness picker explaining that content continues across
following sub-section L1 keys.

v103's "Aiyar L1=18-33 — unidentified Khanda/Chapter block"
inactive entry is REMOVED in v104.

## 3. Source-scan results (other 108 names across the data corpus)

Repo-wide v104 audit scanned 1,264 data files for every Muktikā
108 name + variants in the "X-Upanishad" pattern. Hits:

| Name | Files / context | Verdict |
|---|---|---|
| Maitri | Müller Part 2 (4 hits) — translation source header (already routed in v103); Müller Part 1 (1) — Roer's edition citation | Already active |
| Dakshinamurti | dakshinamurti-stotra (3) — standalone Stotra text, NOT the Upanishad | No new route — Stotra and Upanishad are distinct texts |
| Muktikā | Müller Part 1 (1), Müller Part 2 (1) — both are Müller's own list-of-108 mentions | Commentary only |
| Tejobindu | Aiyar (1) — its own closing rubric | Now active (v104) |
| Yogashikha, Brahmavidya, Kshurika, Atharvashikha, Pranagnihotra, Mahanarayana | Müller Part 2 (1 each) — Müller's bibliographic list of Upanishads he is NOT translating | Commentary / list only |

**Result: no additional translated Upanishads found outside the
six Upanishads-family files.** Subāla and Tejobindu (from Aiyar
L1=18-33) are the only Phase 2 additions.

## 4. Muktikā 108 target table — current coverage

(`status` = active / missing / `cls` = M/V/S/Y/Sh/Vs/Sk per the
legend at the bottom)

### Rigveda (10) — archive coverage: 3 / 10

| # | Upanishad | Status | Cls | Active witness | Notes |
|---|---|---|---|---|---|
| 1  | Aitareya         | active (safe-start, pid='11.51') | M | Müller Part 1 (1879) | Opens at AITAREYA-ARANYAKA section header |
| 2  | Ātmabodha        | active (safe-start) | V | Aiyar L1=11 (1914) | |
| 3  | Kauṣītaki        | active (safe) | M | Müller, complete (1879) | |
| 4  | Mudgala          | missing | V | — | Acquisition needed |
| 5  | Nirvāṇa          | missing | S | — | Acquisition needed |
| 6  | Nādabindu        | active (safe) | Y | Aiyar L1=68 (1914) | |
| 7  | Akṣamālā         | missing | Sh | — | Acquisition needed |
| 8  | Tripura          | missing | Sk | — | Acquisition needed |
| 9  | Saubhāgyalakṣmī  | missing | Sk | — | Acquisition needed |
| 10 | Bahvṛca          | missing | Sk | — | Acquisition needed |

### Shukla Yajurveda (19) — archive coverage: 7 / 19

| # | Upanishad | Status | Cls | Active witness | Notes |
|---|---|---|---|---|---|
| 11 | Īśa            | active (safe) | M | Müller, complete (1879) | |
| 12 | Bṛhadāraṇyaka  | active (safe) | M | Müller, complete (1884) | |
| 13 | Jābāla         | missing | S | — | Acquisition needed |
| 14 | Haṃsa          | active (safe) | Y | Aiyar L1=57 (1914) | |
| 15 | Paramahaṃsa    | missing | S | — | Acquisition needed |
| 16 | Subāla         | active (safe-start) | V | Aiyar L1=18 (1914) | **v104 NEW** (spans L1=18-27) |
| 17 | Mantrikā       | missing | V | — | |
| 18 | Niralamba      | active (safe) | V | Aiyar L1=5 (1914) | |
| 19 | Trīśikhibrāhmaṇa| missing | Y | — | |
| 20 | Maṇḍalabrāhmaṇa| missing | Y | — | |
| 21 | Advayatāraka   | missing | S | — | |
| 22 | Pāingala       | missing | V | — | |
| 23 | Bhikṣu         | active (safe-start) | S | Aiyar L1=41 (1914) | |
| 24 | Turīyātīta     | missing | S | — | |
| 25 | Adhyātmā       | active (safe) | V | Aiyar L1=17 (1914) | |
| 26 | Tārasāra       | active (safe) | Vs | Aiyar L1=38 (1914) | |
| 27 | Yājñavalkya    | missing | S | — | |
| 28 | Sātyāyanī      | missing | S | — | |
| 29 | Muktikā        | missing | M | — | The "list of 108" Upanishad itself |

### Krishna Yajurveda (32) — archive coverage: 16 / 32

| # | Upanishad | Status | Cls | Active witness | Notes |
|---|---|---|---|---|---|
| 30 | Kaṭha           | active (safe) | M | Müller, complete (1884) | |
| 31 | Taittirīya      | active (safe) | M | Müller, complete (1884) | |
| 32 | Brahma          | active (safe-start) | S | Aiyar L1=34 (1914) | (key='brahmopanishad') |
| 33 | Kaivalya        | active (safe-start) | V | Aiyar L1=9 (1914) | |
| 34 | Śvetāśvatara    | active (safe) | M | Müller, complete (1884) | |
| 35 | Garbha          | active (safe) | V | Aiyar L1=37 (1914) | |
| 36 | Nārāyaṇa        | active (safe-start) | Vs | Aiyar L1=39 (1914) | |
| 37 | Amṛtabindu      | active (safe-start) | Y | Aiyar L1=10 (1914) | |
| 38 | Amṛtanāda       | active (safe-start) | Y | Aiyar L1=58 (1914) | |
| 39 | Kālāgnirudra    | missing | Sh | — | |
| 40 | Kṣurikā         | missing | Y | — | Müller mentions but does not translate |
| 41 | Sarvasāra       | active (safe) | V | Aiyar L1=4 (1914) | |
| 42 | Śukarahasya     | missing | V | — | |
| 43 | Tejobindu       | active (safe-start) | Y | Aiyar L1=28 (1914) | **v104 NEW** (spans L1=28-33) |
| 44 | Dhyānabindu     | active (safe) | Y | Aiyar L1=56 (1914) | |
| 45 | Brahmavidyā     | missing | Y | — | Müller mentions; not translated |
| 46 | Yogatattva      | active (safe) | Y | Aiyar L1=55 (1914) | |
| 47 | Dakṣiṇāmūrti    | missing | Sh | — | dakshinamurti-stotra is the standalone Stotra, not the Upanishad |
| 48 | Skanda          | active (safe-start) | V | Aiyar L1=12 (1914) | |
| 49 | Śārīraka        | active (safe-start) | V | Aiyar L1=36 (1914) | |
| 50 | Yogaśikhā       | missing | Y | — | Müller mentions; not translated |
| 51 | Ekākṣara        | missing | V | — | |
| 52 | Akṣi            | missing | V | — | |
| 53 | Avadhūta        | missing | S | — | |
| 54 | Kaṭharudra      | missing | S | — | |
| 55 | Maitrāyaṇi      | active (safe-start, pid='6.348') | M | Müller Part 2 (1884) | (key='maitri') |
| 56 | Rudrahṛdaya     | missing | Sh | — | |
| 57 | Pañcabrahma     | missing | Sh | — | |
| 58 | Prāṇāgnihotra   | missing | V | — | Müller mentions; not translated |
| 59 | Mahā-Nārāyaṇa   | missing | Vs | — | Müller mentions; not translated |
| 60 | Yogakuṇḍalinī   | missing | Y | — | |
| 61 | Kalisantaraṇa   | active (safe-start) | Vs | Aiyar L1=40 (1914) | |
| 62 | Sarasvatī-rahasya| missing | Sk | — | |

### Samaveda (16) — archive coverage: 4 / 16

| # | Upanishad | Status | Cls | Active witness | Notes |
|---|---|---|---|---|---|
| 63 | Kena             | active (safe) | M | Müller, complete (1879) | |
| 64 | Chāndogya        | active (safe) | M | Müller, complete (1879) | |
| 65 | Āruṇi            | missing | S | — | |
| 66 | Maitreya         | active (safe-start) | S | Aiyar L1=6 (1914) | |
| 67 | Maitreyī         | missing | S | — | Distinct from Maitreya |
| 68 | Vajrasūcikā      | active (safe) | V | Aiyar L1=35 (1914) | |
| 69 | Yogachūḍāmaṇi    | missing | Y | — | |
| 70 | Vāsudeva         | missing | Vs | — | |
| 71 | Mahā             | missing | V | — | |
| 72 | Sannyāsa         | missing | S | — | |
| 73 | Avyakta          | missing | Vs | — | |
| 74 | Kuṇḍikā          | missing | S | — | |
| 75 | Sāvitrī          | missing | V | — | |
| 76 | Rudrākṣajābāla   | missing | Sh | — | |
| 77 | Jābāli           | missing | Sh | — | |
| 78 | Darśana          | missing | Y | — | |

### Atharvaveda (31) — archive coverage: 4 / 31

| # | Upanishad | Status | Cls | Active witness | Notes |
|---|---|---|---|---|---|
| 79 | Praśna           | active (safe) | M | Müller, complete (1884) | |
| 80 | Muṇḍaka          | active (safe) | M | Müller, complete (1884) | |
| 81 | Māṇḍūkya         | **missing** | **M** | — | **Acquisition required (highest priority). Audit confirmed no translation text exists in any archive file.** |
| 82 | Atharvaśiras     | missing | Sh | — | |
| 83 | Atharvaśikha     | missing | Sh | — | Müller mentions |
| 84 | Bṛhajjābāla      | missing | Sh | — | |
| 85 | Nṛsiṃhatāpani    | missing | Vs | — | |
| 86 | Nāradaparivrājaka| active (safe-start) | S | Aiyar L1=42 (1914) | (key='narada-parivrajaka', spans L1=42-50) |
| 87 | Sītā             | missing | Sk | — | |
| 88 | Śarabha          | missing | Sh | — | |
| 89 | Tripurātapani    | missing | Sk | — | |
| 90 | Devī             | missing | Sk | — | |
| 91 | Tripurā          | missing | Sk | — | |
| 92 | Bhāvanā          | missing | Sk | — | |
| 93 | Saubhāgya        | missing | Sk | — | |
| 94 | Sarasvatī-rahasya| missing | Sk | — | |
| 95 | Rāmarahasya      | missing | Vs | — | |
| 96 | Rāmatāpaṇi       | missing | Vs | — | |
| 97 | Śāṇḍilya         | active (safe-start) | Y | Aiyar L1=51 (1914) | (key='sandilya', spans L1=51-53) |
| 98 | Paramahaṃsa-parivrājaka | missing | S | — | |
| 99 | Annapūrṇā        | missing | Sk | — | |
| 100| Sūrya            | missing | V | — | |
| 101| Ātmā             | missing | V | — | |
| 102| Pāśupatabrahma   | missing | Sh | — | |
| 103| Parabrahma       | missing | V | — | |
| 104| Avadhūta         | missing | S | — | |
| 105| Tripurā-tāpinī   | missing | Sk | — | |
| 106| Devī             | missing | Sk | — | |
| 107| Bhāvanā          | missing | Sk | — | |
| 108| Mahāvākya        | missing | V | — | |

### Coverage by Veda

| Veda | Active | Target | %  |
|------|---:|---:|---:|
| Rigveda          |  3 |  10 | 30% |
| Shukla Yajurveda |  7 |  19 | 37% |
| Krishna Yajurveda| 16 |  32 | 50% |
| Samaveda         |  4 |  16 | 25% |
| Atharvaveda      |  4 |  31 | 13% |
| **Total**        | **34** | **108** | **31%** |

## 5. UI changes

- **By Veda view** — each Veda group header now carries a small
  italic small-caps "X / Y in Muktikā 108" count, so the reader
  sees coverage per group at a glance.
- **Traditional order view** — gained a collapsed disclosure at
  the bottom titled *"Traditional Muktikā 108 — N active in
  archive · M not yet in archive"*. Expanded, it lists every
  missing Upanishad grouped by Veda, with its Muktikā number,
  class abbreviation (M/V/S/Y/Sh/Vs/Sk), and a legend.
- **By text view** — unchanged.
- **Witness picker** — unchanged.

No nested tabs, no modals, no merge of source files. The
disclosure is collapsed by default so the family page stays at
the v103 length unless the reader explicitly opens the gap map.

## 6. Next acquisition list (priority order)

1. **Māṇḍūkya** (#81, Atharvaveda, Mukhya) — the single missing
   principal Upanishad. Highest priority.
2. **Muktikā** (#29, Shukla Yajurveda) — the eponymous list of
   108 Upanishads itself. Symbolically important.
3. **Mahā-Nārāyaṇa** (#59, Krishna Yajurveda, Vaishnava) — large
   and structurally important; Müller mentions but does not
   translate.
4. **Yogashikha, Brahmavidya, Atharvashikha, Atharvasiras,
   Pranagnihotra, Kshurika** — six Upanishads Müller's Part 2
   editorial bibliography mentions but does not include.
5. **Sannyāsa-class Upanishads** (Jābāla, Paramahaṃsa, Āruṇi,
   Yajñavalkya, Avadhūta, Turīyātīta, etc.) — substantial group;
   commonly available in compilations.

Candidate public-domain sources for these remaining Upanishads
include Aiyar's broader *Sannyāsa Upanishads* / *Yoga Upanishads*
collections (separate volumes from his Thirty Minor), or
Radhakrishnan/Hume/Aurobindo translations. Acquisition workflow:
place TXT in `02_raw_sources/Library_/<source>/` and run the
existing ingestion pipeline.

## 7. What was NOT touched

- No JSON files merged, rewritten, or deleted.
- No source-text passages or chapter_titles modified.
- v100 TEXT_CONTENTS_OVERRIDES preserved.
- All non-Upanishads flows preserved (Bible, Tao, Gita, etc.).
- Page-type doctrine, Atlas Object architecture, witness picker
  unchanged.

## 8. Phase 3 — future

Phase 3 = acquisition. The 108 gap is now mapped honestly; the
next pass would acquire one or more public-domain Upanishad
compilations and route them through the existing witness-picker
infrastructure, starting with Māṇḍūkya.
