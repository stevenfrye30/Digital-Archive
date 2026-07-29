# Buddhist binding supplement — Task 27 lane 2 (2026-07-29)

89 reception rows · 286 chips in 16 zones · NOTHING IS BOUND by this sheet.
Seed context: 18 chips bound (27 dfs) from Task 20 §6 —
all in p-khuddaka / p-abhidhamma / p-paracanon. The four Nikāya zones and the
Vinaya zone are entirely unlit. Scope rows 121 (119 Buddhist + 2 Tibetan
Buddhist), 5 restricted (the Evans-Wentz/Suzuki-era rights holds).

**Map premise (asserted):** bindable chips exist ONLY on the Pāli pillar.
The Chinese pillar (c-sutra…c-hist) and Tibetan pillar (t-kangyur/t-tengyur)
are aggregate-bar territories with chip lists honestly EMPTY, and the map has
no Sanskrit territory at all. ~47 reception rows therefore have no chip to
bind and stay reception (§5) unless the design ever rules structure growth.

If every candidate below confirms, 282 of 286 chips stand lit; the four
left dark are the paracanon ambers (Visuddhimagga · Dīpavaṃsa/Mahāvaṃsa ·
Cūḷavaṃsa · Aṭṭhakathā — chip-named editions not held).

## §1 THE PILLAR FINDING — four Nikāyas + Vinaya held complete;
## TOC assertions RUN AND PASSED

The archive holds the complete SuttaCentral bilingual editions (CC0,
bilara-data) as one df per collection per language. The map's five canon
zones are book-deep (258 chips). This is the hindu principal-Upaniṣad
question at scale — but here the verdict-3 TOC rule is SATISFIED:

| df | hierarchy units | map chips | assertion |
|---|---|---|---|
| `long-discourses-sujato_sujato.json` (+ its `_pli` pair) | 34 contiguous, 0 unmatched ids | 34 | **PASS** |
| `middle-discourses-sujato_sujato.json` (+ its `_pli` pair) | 152 contiguous, 0 unmatched ids | 152 | **PASS** |
| `linked-discourses-sujato_sujato.json` (+ its `_pli` pair) | 56 contiguous, 0 unmatched ids | 56 | **PASS** |
| `numbered-discourses-sujato_sujato.json` (+ its `_pli` pair) | 11 contiguous, 0 unmatched ids | 11 | **PASS** |
| `theravada-vinaya_brahmali.json` (+ `_pli`) | divisions bu-vb · bi-vb · kd 1–22 · pvr | 5 | **PASS** (kd 1–10 = Mahāvagga, kd 11–22 = Cullavagga) |

Chip↔unit mapping is canonical position, CROSS-CHECKED against the `_pli`
dfs' own per-sutta title segments: p-majjhima 152/152 name-matches;
p-digha 33/34 with the single miss being the standard orthographic variant
Pāṭika/Pāthika at position 24. p-anguttara chips are the ordinal book names
(Ekaka…Ekādasaka = nipāta 1…11); p-samyutta maps by explicit saṃyutta
number in the passage ids (sn1…sn56).

**Candidate shape (design rules):** per-chip `contained_in` at scale — the
Zoroastrian/Aiyar shape: every sutta/saṃyutta/book chip binds its two dfs
(Pali + translation) with contained_in "within the Long Discourses, tr.
Sujato (SuttaCentral)" etc., and a deep-route anchor (`dn12`, `sn22`, `an4`,
kd-division) once the reader route grows section targeting — or binds
WITHOUT per-unit routes now (chip lights, reader opens the collection df),
which is exactly how the Aiyar chips were ruled. 258 chips across five
zones; the design also rules whether all five zones ride ONE lane.

Also in p-digha's orbit:
- Dialogues of the Buddha (T.W. Rhys Davids, C.A.F. Rhys Davids, 1899) `dialogues-buddha-rhys-davids_rhys-davids.json` — the Rhys Davids
  Dialogues vol. 1. TOC assertion RUN AND **FAILED**: the df is FLAT
  (hierarchy chapter/verse, page-marker units, no sutta ids) —
  `missing_book_level`, the same class as Müller/Hume in the hindu lane.
  Stays reception; joins the book-aware-restructuring follow-up list.

## §2 Khuddaka — whole-chip binds and joins (bilara editions)

Pali-only dfs bind on the Task 20 precedent (Paṭisambhidāmagga, Apadāna and
all seven abhidhamma chips are already Pali-only lit).

NEW LIGHTS (5 chips):
- **Itivuttaka** ← `itivuttaka-sujato_pli.json` + `itivuttaka-sujato_sujato.json`
- **Theragāthā** ← `theragatha-sujato_pli.json` + `theragatha-sujato_sujato.json`
- **Niddesa** ← `mahaniddesa-pali_pli.json` + `culaniddesa-pali_pli.json` — Mahā- / Cūḷa- labels; Pali only
- **Vimānavatthu · Petavatthu** ← `vimanavatthu-pali_pli.json` + `petavatthu-kovilo_pli.json` — per-book labels; Pali only
- **+ Nettippakaraṇa · Peṭakopadesa  AND  Nettippakaraṇa · Peṭakopadesa (paracanon)** ← `nettippakarana-pali_pli.json` + `petakopadesa-pali_pli.json` — per-book labels; Pali only; DUAL-CHIP per the Milindapañha precedent

JOINS to bound chips (new routes, no new lights):
- Dhammapada ← `dhammapada-sujato_pli.json` + `dhammapada-sujato_sujato.json`
- Udāna ← `udana-sujato_pli.json` + `udana-sujato_sujato.json`
- Sutta Nipāta ← `sutta-nipata-sujato_pli.json` + `sutta-nipata-sujato_sujato.json`
- Therīgāthā ← `therigatha-sujato_pli.json` + `therigatha-sujato_sujato.json`
- Jātaka ← `jataka-sujato_pli.json` + `jataka-sujato_sujato.json` — canonical VERSES only — honesty label
- Buddhavaṃsa · Cariyāpiṭaka ← `cariyapitaka-sujato_pli.json` + `cariyapitaka-sujato_sujato.json` + `buddhavamsa-pali_pli.json` — per-book labels

## §3 English edition joins — content checks ride the verdicts

- The Dhammapada (SBE X, Müller) (F. Max Müller, 1881) `dhammapada-sbe_muller.json` → Dhammapada — SBE X part 1 — TWIN CHECK vs the bound `dhammapada_muller.json` and the double volume
- The Dhammapada & Sutta-Nipāta (Müller) (Max Müller, V. Fausböll, 1881) `dhammapada-muller_muller.json` → Dhammapada + Sutta Nipāta — SBE X BOTH parts in one df — containment/twin question with the two above
- The Sutta-Nipāta (SBE X, Fausböll) (V. Fausböll, 1881) `sutta-nipata-sbe_fausboll.json` → Sutta Nipāta — clean SBE X Fausböll; the BOUND route is a `-no_anonymous` stub — SWAP candidate
- The Buddha's Way of Virtue (W.D.C. Wagiswara, K.J. Saunders, 1912) `buddha-way-virtue-wagiswara_wagiswara-saunders.json` → Dhammapada — a Dhammapada verse rendering — join with label

The Sutta Nipāta situation needs a named ruling: the chip's ONLY current
route is `the-sutta-nipata-v-fausboll-1881-no_anonymous.json` (year-1900
stub, translator field "V-Fausboll 1881 (NO)") while the clean SBE X
Fausböll sits in reception. If the twin check confirms, the clean df should
take the route and the stub retire (the hindu Rāmāyaṇa-swap shape). The
bound Udāna route `the-udana-gm-strong-1902-no_anonymous.json` has the same
stub signature but NO clean twin held — attribution-suspect hold pattern.

## §4 R5 / dedup-queue suspects (design confirms; checks post-verdict)

- `gleaings-in-buddha-fields-lafcadio-hearn-1897_anonymous.json` — twin of `gleanings-buddha-fields-hearn_hearn.json` (title typo, year-1900 stub)
- `buddhas-life-a-ferdinand-herold-t_anonymous.json` — twin of `buddha-life-herold_blum.json` (translator field carries the whole imprint)
- `saddharma-pundarika-buddhism_anonymous.json` — twin of `lotus-sutra-kern_kern.json` (both Kern 1884)
- `buddhas-life-olcott_olcott.json` — EXTRACT suspect — Olcott 1881, likely the life section of his own Buddhist Catechism
- `the-buddhavam-sa-and-the-cariya-pit-aka-richard-morris-no_anonymous.json`
  — CROSS-SCOPE find: shelved under **Greek Literature**; twin suspect of
  the BOUND `buddhavamsa-cariyapitaka_morris.json`. Twin check + retirement
  + (if it somehow survives) shelf correction — a named record either way.

## §5 No-chip families — stay reception honestly (47 rows)

**Sanskrit kāvya & Sanskrit-canon works (no Sanskrit territory on the map)** (12):
- The Buddha-Karita of Aśvaghoṣa, Book I (E. B. Cowell, 1894) `buddhacarita-cowell_e-b-cowell.json`
- The Buddha-Karita of Aśvaghoṣa, Book II (E. B. Cowell, 1894) `buddhacarita-cowell-book-2_e-b-cowell.json`
- The Buddha-Karita of Aśvaghoṣa, Book III (E. B. Cowell, 1894) `buddhacarita-cowell-book-3_e-b-cowell.json`
- The Buddha-Karita of Aśvaghoṣa, Book IV (E. B. Cowell, 1894) `buddhacarita-cowell-book-4_e-b-cowell.json`
- The Buddha-Karita of Aśvaghoṣa, Book V (E. B. Cowell, 1894) `buddhacarita-cowell-book-5_e-b-cowell.json`
- The Buddha-Karita of Aśvaghoṣa, Book VI (E. B. Cowell, 1894) `buddhacarita-cowell-book-6_e-b-cowell.json`
- The Buddha-Karita of Aśvaghoṣa, Book VII (E. B. Cowell, 1894) `buddhacarita-cowell-book-7_e-b-cowell.json`
- The Buddha-Karita of Aśvaghoṣa, Book VIII (E. B. Cowell, 1894) `buddhacarita-cowell-book-8_e-b-cowell.json`
- The Jātakamālā: Garland of Birth-Stories (J.S. Speyer, 1895) `garland-birth-stories-speyer_speyer.json`
- The Saddharma-Puṇḍarīka (H. Kern, 1884) `lotus-sutra-kern_kern.json`
- The Diamond Sutra (William Gemmell (after Kumarajiva), 1912) `diamond-sutra_kumarajiva.json`
- 金剛般若波羅蜜經 (Diamond Sutra) (Kumarajiva, 1900) `diamond-sutra-kumarajiva_anonymous.json`

**Sanskrit/Tibetan-preserved EARLY-DISCOURSE PARALLELS (SuttaCentral)** (9):
- The Discourse giving the Analysis of the Topics (Bhikkhu Ānandajoti) `arthaviniscaya-anandajoti_anandajoti.json`
- The Discourse on the Fourfold Assembly (Bhikkhu Sujato) `catusparisat-sutra-sujato_sujato.json`
- Origination (Bhikkhu Sujato) `dipa-sutra-sujato_sujato.json`
- The City (Bhikkhu Sujato) `nagara-sutra-sujato_sujato.json`
- The Discourse to Śroṇa (Bhikkhu Sujato) `srona-sutra-sujato_sujato.json`
- The Tree (Bhikkhu Sujato) `vrksa-sutra-sujato_sujato.json`
- Discourse to Kātyāyana (Jayarava) `katyayana-jayarava_jayarava.json`
- The Discourse giving the Explanation and Analysis of Conditional Origination from the Beginning (P. L. Vaidya) `pratityasamutpada-vaidya_vaidya.json`
- Upāyikā Fragments (Sāmaṇerī Dhammadinnā) `upayika-dhammadinna_dhammadinna.json`

**Chinese-canon Vinaya (c-vin has no chips)** (2):
- Dharmaguptaka Monks' Code of Discipline (Samuel Beal, 1871) `dharmaguptaka-beal_beal.json`
- Ordination (Dharmaguptaka Vinaya Khandaka) (Tripiṭaka Buddhayaśas of Kaśmīra, Zhu Fonian) `ordination-dharmaguptaka_buddhayasas.json`

**Tibetan holdings (t-kangyur / t-tengyur have no chips)** (3):
- Code of Discipline for Monks (Tibetan Mūlasarvāstivāda) (Tibetan Mūlasarvāstivāda tradition) `patimokkha-tibetan_patimokkha.json`
- She-rab Dong-bu (The Prajñādaṇḍa) (W.L. Campbell, 1919) `sherab-dongbu-campbell_campbell.json`
- Tibetan Folk Tales (A.L. Shelton, 1925) `tibetan-folk-tales_shelton.json`

**Japanese Pure Land / Shin cluster (no chips)** (4):
- Buddhist Psalms (S. Yamabe, L. Adams Beck, 1921) `buddhist-psalms_yamabe-beck.json`
- Principal Teachings of the True Sect of Pure Land (Shugaku Yamabe, L. Adams Beck (ed.), 1915) `pure-land-yamabe-sasaki_yamabe-sasaki.json`
- Shinran and His Work (Arthur Lloyd, 1910) `shinran-lloyd_lloyd.json`
- The Creed of Half Japan (Arthur Lloyd, 1911) `lloyd-creed-half-japan_lloyd.json`

**Historical / travel / art records** (2):
- A Record of Buddhistic Kingdoms (James Legge, 1886) `faxian-record_legge.json`
- The Thousand Buddhas (Aurel Stein, 1921) `thousand-buddhas-stein_stein.json`

**Lives, legends & literary renderings** (6):
- The Light of Asia (Edwin Arnold, 1879) `light-of-asia_arnold.json`
- The Life or Legend of Gaudama, the Buddha of the Burmese, Vol 1 (Paul Bigandet, 1880) `gaudama-burmese-vol1_bigandet.json`
- The Life or Legend of Gaudama, the Buddha of the Burmese, Vol 2 (Paul Bigandet, 1880) `gaudama-burmese-vol2_bigandet.json`
- The Life of Buddha (Paul Blum, 1922) `buddha-life-herold_blum.json`
- The Gospel of Buddha (Paul Carus, 1894) `gospel-of-buddha_carus.json`
- Eastern Stories and Legends (Marie L. Shedlock, 1920) `eastern-stories_shedlock.json`

**Works-about (R1)** (9):
- The Essence of Buddhism (Edwin Arnold, 1892) `arnold-essence-buddhism_arnold.json`
- The Buddhist Catechism (Henry Steel Olcott, 1881) `buddhist-catechism_olcott.json`
- Chinese Buddhism (Joseph Edkins, 1880) `chinese-buddhism-edkins_edkins.json`
- The Creed of Buddha (Edmond Holmes, 1919) `creed-of-buddha_holmes.json`
- Outlines of Mahayana Buddhism (Daisetz Teitaro Suzuki, 1907) `outlines-mahayana-suzuki_suzuki.json`
- Essays in Zen Buddhism (First Series) (Daisetz Teitaro Suzuki, 1927) `suzuki-essays-zen_suzuki.json`
- Zen Buddhism and Its Relation to Art (D.T. Suzuki, 1907) `zen-buddhism-art-suzuki_suzuki-art.json`
- Zen for Americans (Daisetz Teitaro Suzuki, 1906) `zen-for-americans-suzuki_suzuki.json`
- Gleanings in Buddha-Fields (Lafcadio Hearn, 1897) `gleanings-buddha-fields-hearn_hearn.json`

Notes: `diamond-sutra-kumarajiva_anonymous.json` is the CHINESE text of the
Diamond Sutra (金剛般若波羅蜜經) — an original-language witness alongside
Gemmell, not a twin; year-1900 default flagged. The Buddhacarita family is
the SBE 49 Cowell translation split book-wise (I–VIII held). The parallels
family are Sanskrit/Tibetan-preserved counterparts of Pāli discourses —
binding them onto Pāli sutta chips would need a per-chip "parallel" label
precedent the program hasn't set; the design rules whether to set it now
or leave the family reception.

## §6 Cross-scope sweep (asserted)

- The Morris Greek-shelf stub above is the sweep's one action item.
- `monier-williams-buddhism_williams.json` (Comparative Religion) is a
  work-about, correctly shelved — no action.
- The eastasian map holds NO Buddhist chips (asserted) — no cross-map
  Hermetica-shape option exists for the Chinese-canon holdings.

## §7 Ambers & honest reports

- Task 20's eight `possible` chips are exactly covered: five Vinaya chips +
  Itivuttaka + Theragāthā are §1/§2 candidates; **Dīpavaṃsa · Mahāvaṃsa**
  stays possible-not-held → amber (with Visuddhimagga, Cūḷavaṃsa,
  Aṭṭhakathā — the four dark paracanon chips).
- RIGHTS QUERY (design confirms, no binding impact — none of these rows
  bind): the four public D.T. Suzuki rows (d. 1966) sit against the
  worldwide-PD bar the Waley cluster is held under; flagged for the rights
  lane, not this one.
- Bilingual pairs: 13 in reception + Khuddakapāṭha + Milindapañha already
  bound = the 15 the readiness audit counted.

Totals: reception 89 · §1 containment 10 dfs (+1 flat-FAIL) · §2 whole-chip
23 dfs (5 new lights + 6 joins) · §3 edition joins 4 · §4 R5/suspects 4
(+1 cross-scope) · §5 no-chip 47 · chips lightable 282/286.
