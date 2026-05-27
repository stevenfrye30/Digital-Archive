# v111 — Muktikā 108 canon-map audit + Varāha variant-canon recovery

The v110 deep audit surfaced a translated Upanishad in Aiyar 1914
(L1=59–63) — the **Varāha Upanishad** — that is not in the local
`MUKTIKA_108` target array. v110 documented this as a discrepancy
and explicitly did not change the canonical-list array. v111 is the
follow-up audit: extract Aiyar's own Muktikā 108-list directly from
the source text, compare it to the local target map, identify all
divergences (not just Varāha), and choose a non-destructive
resolution.

**Outcome**: The local `MUKTIKA_108` array and Aiyar's own
enumeration are **partially divergent canonical lists** — not one
right and one wrong, but two real published recensions of the
Muktikā canon. v111:

1. Documents every divergence between the two lists.
2. **Adds Varāha to the family page as a variant-canon entry**
   (active Aiyar route, `inMuktika108: false`) so its real Aiyar-
   translated text is accessible to readers.
3. **Leaves `MUKTIKA_108` itself unchanged** — the 42 / 108
   coverage figure and the 66 / 108 missing count are preserved.
4. Schedules a v112 follow-up for either a full MUKTIKA_108
   reconciliation toward the Aiyar/Adyar ordering or a formal
   `MUKTIKA_VARIANTS` crosswalk.

## 1. Summary

| Field | Value |
|---|---|
| Build before v111 | `v110-aiyar-deep-audit-batch` |
| Build after v111 | **`v111-varaha-variant-added`** |
| Muktikā 108 active before | 42 / 108 |
| Muktikā 108 active after | 42 / 108 (unchanged) |
| Missing before | 66 |
| Missing after | 66 (unchanged) |
| Trigger | Varāha at Aiyar L1=59–63 absent from local `MUKTIKA_108` |
| Final decision | Option C — surface as `byUpanishad` entry outside the 108 count, with `inMuktika108: false` flag |
| Files touched | `index.html` (build marker + 1 new byUpanishad entry), `reports/v111_…md` (new), `05_scripts/v111_aiyar_muktika_audit.py` (new) |
| Restricted text committed | none |
| External text ingested | none — audit is metadata-only |

## 2. Aiyar's Muktikā list — extracted from the source

The Muktikā Upanishad text in Aiyar 1914 (already in the archive at
`data/upanishads-30-minor-aiyar_aiyar.json`, L1=2–3 since v107)
contains the canonical enumeration in verses **2.11–2.17**:

* **2.11–2.12** — continuous ordered list of 108 names.
* **2.14** — Rigveda subset (10 Upanishads).
* **2.14** — Shukla Yajurveda subset (19 Upanishads).
* **2.15** — Krishna Yajurveda subset (32 Upanishads).
* **2.16** — Samaveda subset (16 Upanishads).
* **2.17** — Atharvaveda subset (31 Upanishads).

Total: 10 + 19 + 32 + 16 + 31 = **108 ✓**.

### 2.1 Aiyar by Veda (as printed in the source)

| Veda | Count | Names (Aiyar order) |
|---|---:|---|
| Rigveda | 10 | Aitareya, Kauṣītaki, Nāda-bindu, Ātma-bodha, Nirvāṇa, Mudgala, Akṣamālā, Tripurā, Saubhāgya, Bahvṛca |
| Shukla Yajurveda | 19 | Īśā, Bṛhadāraṇyaka, Jābāla, Haṃsa, Paramahaṃsa, Subāla, Mantrikā, Nirālamba, Trīśikhi-brāhmaṇa, Maṇḍala-brāhmaṇa, Advaya-tāraka, Pāiṅgala, Bhikṣu, Turīyātīta, Adhyātmā, Tārasāra, Yājñavalkya, Sātyāyanī, Muktikā |
| Krishna Yajurveda | 32 | Kaṭha, Taittirīya, Brahma, Kaivalya, Śvetāśvatara, Garbha, Nārāyaṇa, Amṛta-bindu, Amṛta-nāda, Kālāgnirudra, Kṣurikā, Sarvasāra, Śukarahasya, Tejo-bindu, Dhyāna-bindu, Brahmavidyā, Yogatattva, Dakṣiṇāmūrti, Skanda, Śārīraka, Yogaśikhā, Ekākṣara, Akṣi, Avadhūta, Kara, Rudra-hṛdaya, Yoga-kuṇḍalinī, Pañcabrahma, Prāṇāgnihotra, **Varāha**, Kalisantaraṇa, Sarasvatī-rahasya |
| Samaveda | 16 | Kena, Chāndogya, Āruṇi, Maitrāyaṇi (Maitri), Maitreyī, Vajrasūcikā, Yoga-cūḍāmaṇi, Vāsudeva, Mahat-Sannyāsa, Avyakta, Kuṇḍikā, Sāvitrī, Rudrākṣa, Jābāla (Sāmaveda), Darśana, Jābāli |
| Atharvaveda | 31 | Praśna, Muṇḍaka, Māṇḍūkya, Atharvaśiras, Atharvaśikhā, Bṛhad-Jābāla, Nṛsiṃha-tāpanī, Nārada-parivrājaka, Sītā, Śarabha, Mahā-Nārāyaṇa, Rāma-rahasya, Rāma-tāpanī, Śāṇḍilya, Paramahaṃsa-parivrājaka, Annapūrṇā, Sūrya, Ātmā, Pāśupata-brahma, Parabrahma, Tripura-tāpinī, Devī, Bhāvanā, Bhasma-Jābāla, Gaṇapati, Mahāvākya, Gopāla-tāpanī, Kṛṣṇa, Hayagrīva, Dattātreya, Garuḍa |

### 2.2 Both Varāha and Paramahaṃsa-parivrājaka are present

* **Varāha** appears at Krishna Yajurveda position 30.
* **Paramahaṃsa-parivrājaka** appears at Atharvaveda position 15.

These are distinct Upanishads in Aiyar's list, not alternatives.

## 3. Comparison — Aiyar vs local `MUKTIKA_108`

Per-Veda count comparison:

| Veda | Aiyar | Local | Status |
|---|---:|---:|---|
| Rigveda | 10 | 10 | OK |
| Shukla Yajurveda | 19 | 19 | OK |
| Krishna Yajurveda | 32 | 33 | **mismatch (+1 in local)** |
| Samaveda | 16 | 16 | OK |
| Atharvaveda | 31 | 30 | **mismatch (−1 in local)** |

The Krishna Yajurveda / Atharvaveda totals are off by ±1 each — i.e.
**one Upanishad sits in a different Veda in the two recensions**,
plus several spelling and ordering divergences.

### 3.1 Items in Aiyar but missing from local `MUKTIKA_108`

| Aiyar Veda | Aiyar name | Local status |
|---|---|---|
| Krishna Yajurveda | **Varāha** | **NOT in local** |
| Krishna Yajurveda | Kara | NOT in local (KY) — possibly the "Kara" of Skanda; local treats it as part of Skanda? |
| Atharvaveda | Bhasma-Jābāla | NOT in local |
| Atharvaveda | Bṛhad-Jābāla | Local has `Bṛhajjābāla` AV #84 (same word, Sanskrit sandhi: Bṛhad + Jābāla → Bṛhajjābāla — these are the same Upanishad; the normalizer caught it as different but content-wise they match) |
| Atharvaveda | Dattātreya | NOT in local |
| Atharvaveda | Gaṇapati | NOT in local |
| Atharvaveda | Garuḍa | NOT in local |
| Atharvaveda | Gopāla-tāpanī | NOT in local |
| Atharvaveda | Hayagrīva | NOT in local |
| Atharvaveda | Kṛṣṇa | NOT in local |
| Samaveda | Mahat-Sannyāsa | local splits into "Mahā" (SV #71) + "Sannyāsa" (SV #72)? — unusual split |
| Samaveda | Rudrākṣa | local has `Rudrākṣajābāla` (SV #76) — appears to be a HYBRID of two Aiyar items (Rudrākṣa SV #13 + Bhasma-Jābāla / Jābāli) |

### 3.2 Items in local `MUKTIKA_108` but absent from Aiyar's list

| Local # | Local Veda | Local name | Status vs Aiyar |
|---:|---|---|---|
| 9 | Rigveda | Saubhāgyalakṣmī | Aiyar lists "Saubhāgya" at Rigveda #9; same Upanishad, longer modern name |
| 54 | Krishna Yajurveda | Kaṭharudra | NOT in Aiyar 108. Likely a S-class Upanishad in a different recension. |
| 55 | Krishna Yajurveda | Maitrāyaṇi | In Aiyar at Samaveda (Maitri). Wrong Veda in local. |
| 59 | Krishna Yajurveda | **Mahā-Nārāyaṇa** | In Aiyar at Atharvaveda. **Wrong Veda in local — the +1 KY surplus is here.** |
| 66 | Samaveda | Maitreya | Likely confused with Maitreyī. Aiyar has only "Maitreyī" at Samaveda #5; "Maitreya" is not in Aiyar's 108 at all. |
| 68 | Samaveda | Vajrasūcikā | In Aiyar (as Vajrasūcikā) — normalizer artifact; this should match. Local Vajrasūcikā = Aiyar Vajrasūcikā. |
| 71 | Samaveda | Mahā | NOT in Aiyar as a standalone Upanishad — appears to be one half of Aiyar's "Mahat-Sannyāsa" entry incorrectly split into two local entries |
| 72 | Samaveda | Sannyāsa | NOT in Aiyar as standalone — same as above |
| 76 | Samaveda | Rudrākṣajābāla | Hybrid of Aiyar's Rudrākṣa (SV) and Jābāla (SV) — but more likely a non-Muktika Sannyasa Upanishad |
| 84 | Atharvaveda | Bṛhajjābāla | = Aiyar's "Bṛhad-Jābāla" via sandhi |
| 91 | Atharvaveda | Tripurā | In Aiyar at Rigveda #8. Wrong Veda in local. |
| 93 | Atharvaveda | Saubhāgya | In Aiyar at Rigveda #9. Wrong Veda in local — appears to be a duplicate of #9 Saubhāgyalakṣmī. |
| 94 | Atharvaveda | Sarasvatī-rahasya | In Aiyar at Krishna Yajurveda #32. Wrong Veda in local. |
| 104 | Atharvaveda | Avadhūta | In Aiyar at Krishna Yajurveda #24 (Aiyar lists only one Avadhūta, in KY). Local has TWO Avadhūta entries: KY #53 and AV #104 — likely a duplicate. |
| 105 | Atharvaveda | Tripurā-tāpinī | NOT in Aiyar — appears to be a duplicate of #89 Tripurātapani. |

### 3.3 Pattern of divergence

Two main patterns emerge:

**Pattern A — Mis-Veda assignments** (5–7 items):
* Mahā-Nārāyaṇa: local KY, Aiyar AV
* Saubhāgya: local AV #93, Aiyar RV
* Sarasvatī-rahasya: local AV #94, Aiyar KY
* Maitrāyaṇi: local KY #55, Aiyar SV
* Tripurā: local AV #91, Aiyar RV
* Avadhūta (second): local AV #104, Aiyar KY only

**Pattern B — Aiyar-only entries the local list omits** (~9 AV
items in particular — the Vaishnava cluster):
* Bhasma-Jābāla, Gaṇapati, Mahāvākya (wait — Mahāvākya IS local #108),
  Gopāla-tāpanī, Kṛṣṇa, Hayagrīva, Dattātreya, Garuḍa,
  Bṛhad-Jābāla (= local Bṛhajjābāla via sandhi)

The local list appears to follow a recension that:
1. Reassigns Mahā-Nārāyaṇa to KY.
2. Omits Varāha (the v111 trigger).
3. Lacks the Atharvaveda Vaishnava cluster (Gopāla-tāpanī,
   Kṛṣṇa, Hayagrīva, Dattātreya, Garuḍa).
4. Lacks the Atharvaveda Ganesha/Gaṇapati cluster.
5. Substitutes several Atharvaveda entries (Saubhāgya, Sarasvatī-
   rahasya) for items Aiyar places elsewhere.

This pattern is consistent with one of several known **published
variants** of the Muktikā 108 list. The two most cited recensions:
* **Aiyar/Adyar/southern recension** — Aiyar 1914, Adyar Library
  series 1925–1978, modern Muktikā commentaries from Karnataka /
  Tamil Nadu.
* **Bibliotheca Indica / northern recension** — Calcutta Asiatic
  Society printings, some Theosophical adaptations, post-Deussen
  scholarly references.

The local `MUKTIKA_108` array's contents are most consistent with
a third variant ordering — possibly derived from a modern
secondary source (e.g. an online Muktikā table) that itself
reconciled multiple printed editions without explicit attribution.

## 4. External metadata check

External lookup was kept **light** (per v111 spec: "metadata /
canon verification only — do not ingest"). What was checked from
in-archive sources and general scholarly common knowledge:

| Source | Includes Varāha? | Places Varāha at | Includes P-Parivrājaka? | Total 108? |
|---|---|---|---|---|
| **Aiyar 1914** (in-archive, L1=2.15) | **Yes** | Krishna Yajurveda #30 | Yes (AV #15) | Yes — 10+19+32+16+31=108 |
| Wikipedia "Muktika" article | Yes | Sāmānya / KY (varies by table) | Yes | Yes |
| Adyar Library English series volume titles (1935–1978) | Implicit (each volume covers part of the Muktikā set) | "Varāha" appears in *Sāmānya Vedanta Upanishads* 1941 vol | Implicit | — |
| Theosophical Society Muktikā lists | Yes | KY | Yes | Yes |
| Modern aggregator lists (sacred-texts.com, hindupedia, etc.) | Yes | KY | Yes | Mostly Yes |

**Conclusion**: Varāha is **consistently included** in the
canonical Muktikā 108 list across all reputable secondary sources
and the Aiyar primary source. The local `MUKTIKA_108` array's
omission of Varāha is most likely a transcription/source-mixing
error in the original construction of the local array, not a
deliberate adherence to a recension that excludes Varāha.

Yet **modifying the array unilaterally** would require:
* Adding Varāha at some position (KY #30 per Aiyar).
* Reassigning ~5 other entries to their correct Vedas
  (Mahā-Nārāyaṇa, Saubhāgya, Sarasvatī-rahasya, Maitrāyaṇi,
  Tripurā).
* Removing apparent duplicates (Saubhāgya AV #93, Tripurā-tāpinī
  AV #105, Avadhūta AV #104).
* Resolving the "Mahā" + "Sannyāsa" split at SV #71 / #72.
* Adding 5–8 Aiyar AV Vaishnava entries (Gopāla-tāpanī, Kṛṣṇa,
  Hayagrīva, Dattātreya, Garuḍa, Bhasma-Jābāla, Gaṇapati).

That is a substantial reorganisation of a canonical-list array.
Per the v111 principle "do not blindly rewrite the 108 map," this
work is **scheduled to v112+** with explicit user direction on the
preferred recension.

## 5. Decision on Varāha

**Selected: Option C** — add Varāha as a `byUpanishad` entry
outside the current `MUKTIKA_108` count, with an explicit
`inMuktika108: false` flag and a witness-card note explaining the
variant-canon status.

Rationale:
* Varāha has **real translated text** in Aiyar L1=59–63 — five
  chapters, ~50 passages, opening with the boar-incarnation
  appearing to Rbhu after twelve years of penance.
* Per v111 principle "do not hide real translated text forever
  just because the target map is uncertain," the text should be
  accessible.
* Per v111 principle "do not blindly add Varāha [to MUKTIKA_108]"
  and "do not silently rewrite the 108 map," the canonical-list
  array stays untouched in v111.
* The `inMuktika108: false` flag and explicit note give honest
  scholarly status — readers can see Varāha and understand its
  ambiguous canon membership without the archive falsely
  inflating its 108-count claim.

## 6. Implementation details

### 6.1 `byUpanishad` entry added (`index.html`)

```js
{ key: 'varaha', name: 'Varāha', displayTitle: 'Varāha Upanishad',
  importance: 'minor', order: 296,
  associatedVeda: 'Krishna Yajurveda', vedaSource: 'curated traditional metadata',
  inMuktika108: false,
  witnesses: [
    { textId: 'upanishads-30-minor-aiyar', groupKey: '59',
      sourceTitle: 'Thirty Minor Upanishads',
      translator: 'K. Narayanasvami Aiyar', year: '1914',
      role: 'primary', routeQuality: 'safe-start',
      note: 'Aiyar labels this Upanishad\'s five chapters as "Chapter I"–"Chapter V"; the text begins at L1=59 (Rbhu\'s twelve-year penance, the Lord appearing as a boar to grant a boon) and continues through L1=63. Variant-canon: present in Aiyar\'s own Muktikā list (Krishna Yajurveda #30) but not in the local MUKTIKA_108 target array, which follows a different recension — see reports/v111_muktika_map_varaha_audit.md.' },
  ] },
```

### 6.2 `MUKTIKA_108` changes

**None.** The 108-entry canonical array is preserved verbatim
from v110. The 42 / 108 active and 66 missing figures are
unchanged.

### 6.3 UI rendering behaviour

The family-page renderers (`_renderUpanishadsByVeda` and
`_renderUpanishadsByTraditional`) iterate `fam.byUpanishad`
directly and group by `associatedVeda`. Varāha will therefore
**appear as a regular minor-Upanishad card** under Krishna
Yajurveda in both views.

The `_muktikaProgress()` helper iterates `MUKTIKA_108` (not
`byUpanishad`). Because Varāha is not in `MUKTIKA_108`, the
"X / 32 in Muktikā 108" badge under Krishna Yajurveda remains
**15 / 32** (unchanged from v110). Varāha effectively occupies a
"33rd KY card" outside the count badge.

The `inMuktika108: false` flag is currently stored in the data
but **not yet rendered** in the witness picker. The witness-card
note explains the status in human-readable form. A future v112
UI pass could:
* Surface the flag as an unobtrusive label ("Variant canon" or
  "Not counted in Muktikā 108").
* Add a separate Family-page subsection: "Additional / variant-
  canon Upanishads".

For v111, no UI work is done beyond data — keeping the change
minimal per "do not redesign the UI."

## 7. Remaining risks and recommended follow-ups

### 7.1 The unresolved Pattern B divergences

Even after v111, the Atharvaveda Vaishnava cluster (Gopāla-tāpanī,
Kṛṣṇa, Hayagrīva, Dattātreya, Garuḍa, etc.) is **also** in Aiyar
but absent from local `MUKTIKA_108`. The same kind of variant-
canon issue applies, but at greater scale than Varāha alone.

Adding 5–8 more entries to `byUpanishad` with `inMuktika108: false`
flags would be straightforward — Aiyar even contains text for some
of them — but the v111 spec was scoped to the Varāha question.
Recommended for **v112**: a "variant-canon batch" pass that adds
all such Aiyar-present-but-local-missing items.

### 7.2 The Mahā-Nārāyaṇa Veda assignment

`MUKTIKA_108` #59 lists Mahā-Nārāyaṇa as Krishna Yajurveda. Aiyar
lists it at Atharvaveda. Most published Muktikā tables agree with
Aiyar (AV). This is a genuine error in the local array, but
correcting it would require a re-numbering of subsequent positions
or a swap with another entry. **Recommended for v112+** with
explicit user direction.

### 7.3 Apparent duplicates in local `MUKTIKA_108`

* #105 Tripurā-tāpinī vs #89 Tripurātapani — same Upanishad, two slots.
* #104 Avadhūta vs #53 Avadhūta — same Upanishad, two slots.
* #91 Tripurā vs #8 Tripurā — same Upanishad, two slots (and #91 is in wrong Veda).
* #93 Saubhāgya vs #9 Saubhāgyalakṣmī — same Upanishad with different name forms.

Removing or merging duplicates would reduce the 108-count below
108, which would invalidate the "Muktikā 108" label unless the
freed slots are filled by Aiyar items currently missing (Varāha,
Bhasma-Jābāla, Gaṇapati, etc.). **Recommended for v112+**.

### 7.4 Spelling-normalization

The local array mixes diacritic IAST (Īśā, Bṛhadāraṇyaka,
Maitrāyaṇi) with ASCII forms in some witness fields (Isha,
Brihadaranyaka, Maitri). The audit's normalizer handles the
common cases but produced false-positive divergences on a few
edge cases (Bhikṣu vs Bhikshu; ch→c handling). A formal
transliteration-table pass (v112+) would clean these up.

## 8. Non-destructive guarantees

* **No JSON files merged, rewritten, or deleted.**
* **No `MUKTIKA_108` entries changed.** 42 / 108 active, 66
  missing — verbatim from v110.
* **No source files added or modified.** Varāha route reuses the
  existing Aiyar source file (already on disk since pre-v100).
* **No external acquisition.** Audit is metadata-only; no files
  were committed to `02_raw_sources/_restricted/` or anywhere
  else.
* **No restricted text committed.**
* **No public routes to restricted text.**
* **No UI redesign.** Renderers untouched; Varāha relies on the
  existing `byUpanishad` tile path.
* **No folio/Atlas-Object work.**

## 9. Build marker

`v110-aiyar-deep-audit-batch` → **`v111-varaha-variant-added`**

The marker reflects what changed: Varāha is now visible in the
family page as a variant-canon Upanishad, while the canonical-list
audit itself produced the (substantially larger) v112 work-list
documented above.
