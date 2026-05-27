# v112 — Muktikā canon reconciliation (dual-map architecture)

The v111 audit revealed that the local `MUKTIKA_108` array and
Aiyar's own enumeration in the in-archive Muktikā Upanishad source
are two partially-divergent canonical lists. v111 surfaced Varāha
as a single variant-canon entry; v112 closes the architectural
question by **adopting Model C — dual canon-map architecture**.

A second canonical list, `MUKTIKA_108_AIYAR`, is now tracked
internally alongside the primary `MUKTIKA_108`. The public-facing
"X / 108" badge and gap disclosure on the family page continue to
count against the primary list (preserving the 42 / 108 figure
unchanged from v107). Reports and future passes have access to both
canons.

## 1. Summary

| Field | Value |
|---|---|
| Build before v112 | `v111-varaha-variant-added` |
| Build after v112 | **`v112-dual-muktika-canon-map`** |
| Selected model | **C — dual canon-map** |
| Public Muktikā 108 count before | 42 / 108 (primary) |
| Public Muktikā 108 count after | 42 / 108 (primary, **unchanged**) |
| Aiyar Muktikā 108 count after | 42 / 108 (newly tracked) |
| Missing in primary | 66 |
| Missing in Aiyar | 66 |
| Varāha status | **counted in Aiyar canon (KY #59), not counted in primary canon** — Varāha continues to render as a normal byUpanishad card under Krishna Yajurveda (unchanged from v111) |
| Files touched | `index.html` (+~125 lines: MUKTIKA_108_AIYAR const + helper + UI note + build marker), `reports/v112_…md` (new), `05_scripts/v112_gen_aiyar_const.py` (new generator script) |
| Restricted text committed | none |
| External text ingested | none |

## 2. Why Model C

The user's v112 spec offered three models:

* **Model A** — keep primary as-is, document Aiyar as variant.
* **Model B** — switch primary to Aiyar's source-derived list.
* **Model C** — dual count internally, public UI stays simple.

Per the user's guidance ("If uncertain, implement Model C
internally and keep the public UI simple"), **Model C is the
correct choice for v112**:

1. The primary `MUKTIKA_108` array has multiple independent issues
   (see v111 report §3): mis-Veda assignments, apparent duplicates,
   ~9 missing AV Vaishnava entries, and an unusual Mahā/Sannyāsa
   split at SV #71/#72. A wholesale switch to Aiyar's ordering
   would invalidate every consumer of the primary list (the family
   page count badges, the existing v107/v110 byUpanishad routes
   that reference primary keys, downstream reports).
2. The Aiyar list is itself one legitimate canonical recension
   (Aiyar/Adyar/southern tradition) — adopting it as primary would
   be a deliberate scholarly choice deserving explicit user
   direction, not a silent v112 decision.
3. Both lists are real and worth preserving. Model C does that
   without sacrificing the public count's stability.

Model C means future v113+ acquisition passes can target either
list's missing entries and report progress against both. When the
user is ready to make a primary-canon switch decision, the
infrastructure already exists.

## 3. Aiyar's Muktikā list (extracted from the in-archive source)

Source: `data/upanishads-30-minor-aiyar_aiyar.json`, L1=2 verses
2.11 (full ordered list) and 2.14–2.17 (per-Veda subsets). The
extraction was done by hand in v111 from the actual Aiyar OCR'd
English text and verified to total 108 by Veda counts
(10 + 19 + 32 + 16 + 31 = 108).

The 108 entries are now encoded as `MUKTIKA_108_AIYAR` in
`index.html`, same shape as the primary `MUKTIKA_108` so the
existing `_muktikaProgress` helper logic works (v112 also adds
`_muktikaProgressAiyar` as a parallel helper).

Full list (Aiyar order):

### Rigveda (10)
1. Aitareya · 2. Kauṣītaki · 3. Nāda-bindu · 4. Ātma-bodha ·
5. Nirvāṇa · 6. Mudgala · 7. Akṣamālā · 8. Tripurā ·
9. Saubhāgya · 10. Bahvṛca

### Shukla Yajurveda (19)
11. Īśā · 12. Bṛhadāraṇyaka · 13. Jābāla · 14. Haṃsa ·
15. Paramahaṃsa · 16. Subāla · 17. Mantrikā · 18. Nirālamba ·
19. Trīśikhi-brāhmaṇa · 20. Maṇḍala-brāhmaṇa · 21. Advaya-tāraka ·
22. Pāiṅgala · 23. Bhikṣu · 24. Turīyātīta · 25. Adhyātmā ·
26. Tārasāra · 27. Yājñavalkya · 28. Sātyāyanī · 29. Muktikā

### Krishna Yajurveda (32)
30. Kaṭha · 31. Taittirīya · 32. Brahma · 33. Kaivalya ·
34. Śvetāśvatara · 35. Garbha · 36. Nārāyaṇa · 37. Amṛta-bindu ·
38. Amṛta-nāda · 39. Kālāgnirudra · 40. Kṣurikā · 41. Sarvasāra ·
42. Śukarahasya · 43. Tejo-bindu · 44. Dhyāna-bindu ·
45. Brahmavidyā · 46. Yogatattva · 47. Dakṣiṇāmūrti · 48. Skanda ·
49. Śārīraka · 50. Yogaśikhā · 51. Ekākṣara · 52. Akṣi ·
53. Avadhūta · 54. Kara · 55. Rudra-hṛdaya · 56. Yoga-kuṇḍalinī ·
57. Pañcabrahma · 58. Prāṇāgnihotra · **59. Varāha** ·
60. Kalisantaraṇa · 61. Sarasvatī-rahasya

### Samaveda (16)
62. Kena · 63. Chāndogya · 64. Āruṇi · 65. Maitrāyaṇi ·
66. Maitreyī · 67. Vajrasūcikā · 68. Yoga-cūḍāmaṇi ·
69. Vāsudeva · 70. Mahat-Sannyāsa · 71. Avyakta · 72. Kuṇḍikā ·
73. Sāvitrī · 74. Rudrākṣa · 75. Jābāla (Sāmaveda) ·
76. Darśana · 77. Jābāli

### Atharvaveda (31)
78. Praśna · 79. Muṇḍaka · 80. Māṇḍūkya · 81. Atharvaśiras ·
82. Atharvaśikhā · 83. Bṛhad-Jābāla · 84. Nṛsiṃha-tāpanī ·
85. Nārada-parivrājaka · 86. Sītā · 87. Śarabha ·
88. Mahā-Nārāyaṇa · 89. Rāma-rahasya · 90. Rāma-tāpanī ·
91. Śāṇḍilya · 92. Paramahaṃsa-parivrājaka · 93. Annapūrṇā ·
94. Sūrya · 95. Ātmā · 96. Pāśupata-brahma · 97. Parabrahma ·
98. Tripura-tāpinī · 99. Devī · 100. Bhāvanā ·
101. Bhasma-Jābāla · 102. Gaṇapati · 103. Mahāvākya ·
104. Gopāla-tāpanī · 105. Kṛṣṇa · 106. Hayagrīva ·
107. Dattātreya · 108. Garuḍa

## 4. Primary vs Aiyar — divergence summary

### 4.1 Per-Veda totals

| Veda | Primary | Aiyar | Match? |
|---|---:|---:|---|
| Rigveda | 10 | 10 | OK (composition differs — see below) |
| Shukla Yajurveda | 19 | 19 | OK |
| Krishna Yajurveda | 33 | 32 | mismatch (+1 in primary) |
| Samaveda | 16 | 16 | OK |
| Atharvaveda | 30 | 31 | mismatch (−1 in primary) |
| **Total** | **108** | **108** | both total 108 |

### 4.2 Active-route comparison (the 42 currently-routed Upanishads)

| State | Count | Example |
|---|---:|---|
| In primary 108 AND in Aiyar 108 | 41 | aitareya, kaushitaki, mandalabrahmana, paingala, … |
| In primary 108 only (not in Aiyar) | 1 | `maitreya` (Samaveda #66 primary) — Aiyar has only Maitreyī (SV #66 Aiyar) and Maitrāyaṇi (SV #65 Aiyar) |
| In Aiyar 108 only (not in primary) | 1 | `varaha` (KY #59 Aiyar) — added to byUpanishad in v111 with `inMuktika108: false` |
| Primary active count | **42 / 108** | unchanged |
| Aiyar active count | **42 / 108** | newly visible — same number, different composition |

### 4.3 Cross-canon "found in a different Veda" items

Five entries are present in BOTH canons but assigned to different
Vedas:

| Entry | Primary Veda | Aiyar Veda | Notes |
|---|---|---|---|
| Mahā-Nārāyaṇa | Krishna Yajurveda (#59) | Atharvaveda (#88) | Aiyar / Adyar standard assignment is AV |
| Saubhāgya | Atharvaveda (#93) | Rigveda (#9) | Aiyar lists Saubhāgya only in RV; the AV #93 appears to be a primary-canon error/duplicate |
| Sarasvatī-rahasya | Atharvaveda (#94) | Krishna Yajurveda (#61) | Aiyar / most secondary sources place this in KY |
| Maitrāyaṇi (Maitri) | Krishna Yajurveda (#55) | Samaveda (#65) | Aiyar groups Maitrāyaṇi with the Sāmaveda Upanishads |
| Tripurā | Atharvaveda (#91) | Rigveda (#8) | Aiyar lists Tripurā only in RV |
| Avadhūta (second) | Atharvaveda (#104) | Krishna Yajurveda (#53) only | Aiyar lists only one Avadhūta (in KY); primary's #104 AV entry appears to be a duplicate |

### 4.4 Apparent primary-canon duplicates

The primary `MUKTIKA_108` has several entries that appear to be
double-counts of items also at earlier positions:

| Apparent duplicate | Primary positions | Aiyar treatment |
|---|---|---|
| Saubhāgya / Saubhāgyalakṣmī | #9 RV (as "Saubhāgyalakṣmī") + #93 AV (as "Saubhāgya") | Aiyar has one Saubhāgya only, in RV |
| Tripurā / Tripurā-tāpinī | #8 RV (Tripurā) + #89 AV (Tripurātapani) + #91 AV (Tripurā) + #105 AV (Tripurā-tāpinī) | Aiyar has Tripurā in RV (#8) and Tripura-tāpinī in AV (#98) — not four entries |
| Devī | #90 AV + #106 AV | Aiyar has one Devī only |
| Bhāvanā | #92 AV + #107 AV | Aiyar has one Bhāvanā only |
| Avadhūta | #53 KY + #104 AV | Aiyar has one Avadhūta only |

If duplicates were removed from primary, freed slots could be filled
by Aiyar items the primary list omits (Varāha, Bhasma-Jābāla,
Gaṇapati, Gopāla-tāpanī, Kṛṣṇa, Hayagrīva, Dattātreya, Garuḍa,
Mahāvākya-different-Veda) — but **v112 does not modify
`MUKTIKA_108`** per the principle "do not silently rewrite the
canon."

### 4.5 Items in Aiyar with no English text route yet

Of Aiyar's 108, 66 have `key:null` in `MUKTIKA_108_AIYAR` because
no English-text byUpanishad route exists. These overlap heavily
with the primary's 66 missing entries but are not identical (e.g.,
Varāha is missing in primary but present in Aiyar's active count;
the AV Vaishnava cluster is missing in both).

## 5. Canon architecture implemented

### 5.1 Constants

| Constant | Purpose | Shape |
|---|---|---|
| `MUKTIKA_108` | Primary public-facing canon target. Existing list, unchanged by v112. | `[{n, key, name, veda, cls, variants}, …]` × 108 |
| `MUKTIKA_108_AIYAR` | Aiyar source-derived canon, newly added by v112. | Same shape × 108 |

### 5.2 Helpers

| Helper | Purpose | Used by |
|---|---|---|
| `_muktikaProgress(fam)` | Per-Veda active/target counts against primary | Family page UI (`_renderUpanishadsByVeda`) |
| `_muktikaProgressAiyar(fam)` | Per-Veda active/target counts against Aiyar | Reports + future dual-display paths |

`_muktikaProgressAiyar` follows the same structure as
`_muktikaProgress` but iterates `MUKTIKA_108_AIYAR`. It also
adds a `_total` field on the returned object for convenience.

### 5.3 byUpanishad field changes

`byUpanishad` entry shape is **unchanged in v112**. The
`inMuktika108: false` flag added to Varāha in v111 remains; no
other byUpanishad entries gain new fields. This is intentional:
classifying every byUpanishad entry against both canons can be
done at call time (the helpers do it), so no per-entry duplication
is needed.

## 6. Count results

| Metric | Before v112 | After v112 |
|---|---:|---:|
| Primary MUKTIKA_108 active | 42 / 108 | **42 / 108** (unchanged) |
| Primary missing | 66 | 66 (unchanged) |
| Aiyar MUKTIKA_108_AIYAR active | — (not tracked) | **42 / 108** (newly tracked) |
| Aiyar missing | — | 66 |
| byUpanishad routes | 43 | 43 (no new routes) |
| Hume second witnesses | 13 | 13 (unchanged) |
| v110 deep-audit routes (Pāingala / Maṇḍalabrāhmaṇa / Yogakuṇḍalinī) | active | active (unchanged) |
| Varāha route | active, variant-canon | active, variant-canon (unchanged) |

**The public-facing count did not change.** Per Model C, that is
the desired behavior: dual tracking added without disrupting the
existing display.

## 7. UI changes

Single sentence added to the existing `byveda-note` paragraph on
the Upanishads family page:

> *The archive tracks two Muktikā lists in parallel: the primary
> 108 (shown in the counts here) and the Aiyar source-derived 108
> (extracted from the in-archive Muktikā Upanishad text); see*
> `reports/v112_muktika_canon_reconciliation.md` *for the variant-
> canon audit.*

No layout changes. No new visual elements. No additional buttons
or tabs. Varāha continues to render under Krishna Yajurveda exactly
as it did in v111 (no change to the tile or the witness picker).

## 8. Future recommendations

### v113 (next pass): Resume acquisition with dual-canon reporting

Future acquisition reports should track progress against **both**
canons. A new minor Upanishad found in any source should be checked
against both `MUKTIKA_108` and `MUKTIKA_108_AIYAR`:

* If in primary → counts in primary's 42 / 108 figure
* If in Aiyar but not primary → counts in Aiyar's 42 / 108
* If in both → counts in both
* If in neither → optional add as variant-canon outside both counts
  (the Varāha pattern)

### v114 or later: Primary-canon migration toward Aiyar's ordering

The cleanest long-term resolution is to switch primary to Aiyar's
ordering, since the in-archive Aiyar Muktikā Upanishad text is the
canonical source of the 108 list within the archive's own corpus.
Switching requires:

1. Resolving the apparent duplicates in current primary (Tripurā
   ×4, Saubhāgya ×2, Avadhūta ×2, Devī ×2, Bhāvanā ×2).
2. Reassigning the five mis-Vedaed entries (Mahā-Nārāyaṇa,
   Saubhāgya, Sarasvatī-rahasya, Maitrāyaṇi, Tripurā).
3. Adding the eight Aiyar-only entries (Varāha, Bhasma-Jābāla,
   Gaṇapati, Gopāla-tāpanī, Kṛṣṇa, Hayagrīva, Dattātreya, Garuḍa).
4. Updating any external consumers / documentation that quote
   specific Muktikā numbers.
5. Documenting the canon-switch in a v114 changeset and updating
   build markers / coverage reports accordingly.

This is explicitly out of scope for v112 and requires user
direction to commit to a canonical-list switch.

### v115+: Reconcile other apparent variants

The `cls` (class) assignments in `MUKTIKA_108` vs
`MUKTIKA_108_AIYAR` should be cross-checked. v112 followed the
primary's class assignments where they exist; Aiyar's own
classification can be cross-checked against the Aiyar OCR for
class hints (when the source explicitly classifies an Upanishad).

## 9. Non-destructive guarantees

* **No JSON files merged, rewritten, or deleted.**
* **No `MUKTIKA_108` entries changed.** Primary list verbatim from
  v111.
* **No new external source ingested.**
* **No restricted text committed.**
* **No public routes to restricted text.**
* **No existing routes broken.** Hume witnesses, v110 Aiyar deep-
  audit routes (Pāingala, Maṇḍalabrāhmaṇa, Yogakuṇḍalinī), v111
  Varāha — all unchanged.
* **No UI redesign.** One sentence added to an existing note
  paragraph; no new tiles, sections, tabs, or buttons.
* **No folio / Atlas-Object work.**

## 10. Build marker

`v111-varaha-variant-added` → **`v112-dual-muktika-canon-map`**

The marker reflects the architectural change: a second canon-map
is now first-class in `index.html` and accessible to the renderer,
while the primary public count is preserved verbatim.
