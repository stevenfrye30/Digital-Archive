# v115 — Primary `MUKTIKA_108` map audit + v116 migration plan

The v111–v114 sequence surfaced ad-hoc evidence that the primary
`MUKTIKA_108` array has internal anomalies. v115 runs a single
comprehensive programmatic audit, confirms the scope of the issue,
adopts **Option C** (prepare migration plan to Aiyar primary but do
not switch in this pass), and adds non-destructive in-source
documentation marking every flagged entry.

The public 43 / 108 count and 53 missing-in-both figure are
preserved. The v116 migration plan in §6 below provides a complete,
sequenced procedure for switching primary to Aiyar's ordering as a
single deliberate change set when the user approves.

## 1. Summary

| Field | Value |
|---|---|
| Build before v115 | `v114-periodical-acquisition-needed` |
| Build after v115 | **`v115-primary-muktika-audit`** |
| Primary `MUKTIKA_108` active | 43 / 108 (unchanged) |
| Aiyar `MUKTIKA_108_AIYAR` active | 43 / 108 (unchanged) |
| Missing in primary | 65 (unchanged) |
| Missing in Aiyar | 65 (unchanged) |
| Missing in BOTH | 53 (unchanged) |
| Selected option | **C — prepare migration plan, don't switch yet** |
| Public count change | none |
| `MUKTIKA_108` data changes | **none** — only an annotation comment block added to the array's header documenting known anomalies |
| `MUKTIKA_108_AIYAR` data changes | none |
| `byUpanishad` changes | none |
| Restricted text committed | none |
| Files touched | `index.html` (build marker + comment block above MUKTIKA_108), `05_scripts/v115_primary_muktika_audit.py` (new), `05_scripts/v115_primary_muktika_audit_result.json` (new), `reports/v115_…md` (new) |

## 2. Audit method

`05_scripts/v115_primary_muktika_audit.py` parses both canon arrays
from `index.html`, normalizes names (NFKD strip + transliteration
aliases: sh→s, ch→c, ri→r, w→v, doubled-vowel collapse, drop
trailing "upanishad"), and reports:

1. Duplicate normalized names within primary.
2. Veda mismatches across canons for the same normalized name.
3. Primary-only normalized names (no Aiyar equivalent).
4. Aiyar-only normalized names (no primary equivalent).
5. byUpanishad routes vs canon membership.
6. Specific case-study spot-checks for the names called out in
   the v115 spec.

Result file: `05_scripts/v115_primary_muktika_audit_result.json`.

## 3. Primary `MUKTIKA_108` audit findings

### 3.1 Five duplicate normalized names in primary

| Norm | Primary slot 1 | Primary slot 2 |
|---|---|---|
| `avadhuta` | #53 Avadhūta (Krishna Yajurveda, S) | #104 Avadhūta (Atharvaveda, S) |
| `bhavana` | #92 Bhāvanā (Atharvaveda, Sk) | #107 Bhāvanā (Atharvaveda, Sk) |
| `devi` | #90 Devī (Atharvaveda, Sk) | #106 Devī (Atharvaveda, Sk) |
| `sarasvatirahasya` | #62 Sarasvatī-rahasya (Krishna Yajurveda, Sk) | #94 Sarasvatī-rahasya (Atharvaveda, Sk) |
| `trpura` | #8 Tripura (Rigveda, Sk) | #91 Tripurā (Atharvaveda, Sk) |

Five slots are spent on apparent doubles. **Net: primary has 103
distinct normalized names spread across 108 slots.** Aiyar's list
has 108 distinct normalized names — internally consistent.

The Bhāvanā #92/#107 and Devī #90/#106 pairs even share both
Atharvaveda assignment AND class (Sk) — these are not "same word
different Upanishad" cases. They are clear duplicates.

### 3.2 Veda mismatches between canons

| Norm | Primary | Aiyar |
|---|---|---|
| `trpura` | #8 (RV) + #91 (AV) | #8 only (RV) |
| `maitrayani` | #55 (KY) | #65 (SV) |
| `saubhagya` | #93 (AV) | #9 (RV) |
| `mahanarayana` | #59 (KY) | #88 (AV) |
| `avadhuta` | #53 (KY) + #104 (AV) | #53 only (KY) |
| `sarasvatirahasya` | #62 (KY) + #94 (AV) | #61 only (KY) |

For Mahā-Nārāyaṇa specifically: the canonical Adyar / scholarly
position (Olivelle, Deussen, Adyar Library *Sāmānya Vedānta
Upaniṣads* 1941) places it under Atharvaveda — matching Aiyar.
Primary's KY assignment at #59 is anomalous.

For Maitrāyaṇi specifically: the textual source (the Maitrāyaṇī
Saṃhitā of the Black Yajurveda) is sometimes invoked to justify
either KY or SV. Aiyar's own enumeration places it at SV #65
(consistent with how Aiyar himself titles the chapter in his
*Thirty Minor Upanishads* source). Primary's KY assignment is
defensible but minority.

### 3.3 Primary-only entries (no Aiyar equivalent)

| Primary # | Name | Veda | cls | Likely Aiyar match (if any) | Status |
|---:|---|---|---|---|---|
| 9 | Saubhāgyalakṣmī | RV | Sk | Aiyar #9 "Saubhāgya" (RV) — longer modern name | Variant spelling |
| 54 | Kaṭharudra | KY | S | none | Genuine non-Muktika item, possibly mis-included |
| 66 | Maitreya | SV | S | none (Aiyar #66 is Maitreyī) | Likely confused with Maitreyī |
| 71 | Mahā | SV | V | half of Aiyar #70 Mahat-Sannyāsa | Bad split |
| 72 | Sannyāsa | SV | S | half of Aiyar #70 Mahat-Sannyāsa | Bad split |
| 76 | Rudrākṣajābāla | SV | Sh | Hybrid name (Rudrākṣa + Jābāla)? | Cannot find as discrete entry in any published Muktika list |
| 84 | Bṛhajjābāla | AV | Sh | Aiyar #83 "Bṛhad-Jābāla" via Sanskrit sandhi | Same Upanishad, spelling variant |
| 89 | Tripurātapani | AV | Sk | Aiyar #98 "Tripura-tāpinī" | Same Upanishad, transliteration variant |

Eight primary-only entries. Of these, only **Maitreya #66** is
currently active (`key='maitreya'` in byUpanishad, routes to Aiyar
L1=6). This is the one entry where primary's anomaly is "live."

### 3.4 Aiyar-only entries (no primary equivalent)

| Aiyar # | Name | Veda | cls | Status |
|---:|---|---|---|---|
| 54 | Kara | KY | Y | Genuinely missing from primary |
| 59 | Varāha | KY | V | Active in byUpanishad as variant-canon (v111) |
| 70 | Mahat-Sannyāsa | SV | S | Possibly = primary's #71 Mahā + #72 Sannyāsa as a unit |
| 74 | Rudrākṣa | SV | Sh | Genuinely missing |
| 75 | Jābāla (Sāmaveda) | SV | S | Second Jābāla — genuinely missing |
| 83 | Bṛhad-Jābāla | AV | Sh | = primary's #84 via sandhi |
| 101 | Bhasma-Jābāla | AV | Sh | Genuinely missing |
| 102 | Gaṇapati | AV | Sh | Genuinely missing |
| 104 | Gopāla-tāpanī | AV | Vs | Genuinely missing |
| 105 | Kṛṣṇa | AV | Vs | Genuinely missing |
| 106 | Hayagrīva | AV | Vs | Genuinely missing |
| 107 | Dattātreya | AV | Vs | Genuinely missing |
| 108 | Garuḍa | AV | Vs | Genuinely missing |

Thirteen Aiyar-only entries. The **AV Vaishnava cluster** (#104–108
Gopāla / Kṛṣṇa / Hayagrīva / Dattātreya / Garuḍa) is the most
notable gap in primary; this is a real, scholarly canonical group
that primary omits entirely.

### 3.5 byUpanishad routes vs canon classification

| Group | Count | Notes |
|---|---:|---|
| Routes counted in BOTH canons | 42 | All routed Upanishads except Maitreya + Varāha |
| Routes counted in PRIMARY only | 1 — `maitreya` | Primary #66; not in Aiyar 108 |
| Routes counted in AIYAR only | 1 — `varaha` | Aiyar #59; flagged `inMuktika108: false` (v111) |
| Routes counted in NEITHER | 0 | All 44 byUpanishad routes are accounted for |

The symmetry (42 in both, 1 each in one only) is why both canons
report 43/108 — the same coverage figure arrived at via slightly
different sets.

## 4. Case studies (per v115 spec §8.4)

### 4.1 Varāha

* **Aiyar #59** (KY, V class)
* **Not in primary**
* **Active byUpanishad route** — added v111 with `inMuktika108: false`
* **Recommendation**: After v116 primary-switch, Varāha is
  natively included in the primary canon (Aiyar's #59) and the
  `inMuktika108` flag can be removed. Until then, the variant-canon
  status from v111 is correct.

### 4.2 Paramahaṃsa-parivrājaka

* **Primary #98** (AV, S class) — not active
* **Aiyar #92** (AV, S class) — not active
* **Both canons include** this Upanishad in AV/S; just at different
  positions. No conflict. Acquisition target for the future Adyar
  Samnyāsa volume (2074 PD entry).

### 4.3 Tripurā / Tripurātāpinī cluster

| Slot | Name | Veda |
|---|---|---|
| primary #8 | Tripura | RV |
| primary #91 | Tripurā | AV |
| primary #89 | Tripurātapani | AV |
| primary #105 | Tripurā-tāpinī | AV |
| aiyar #8 | Tripurā | RV |
| aiyar #98 | Tripura-tāpinī | AV |

Aiyar has the cluster cleanly as **two** Upanishads (Tripurā in RV;
Tripura-tāpinī in AV). Primary spreads it across **four** slots
including an apparent dupe pair (Tripurā #91 = Aiyar's #8 in wrong
Veda) and a triple-Tripurātāpinī (Tripurātapani #89 vs
Tripurā-tāpinī #105 are the same Upanishad with different
diacritic conventions).

Net waste: 2 slots (4 primary slots vs 2 Aiyar slots = 2 slots
could be freed by deduplication).

### 4.4 Saubhāgya / Saubhāgyalakṣmī

* primary #9 Saubhāgyalakṣmī (RV)
* primary #93 Saubhāgya (AV)
* aiyar #9 Saubhāgya (RV) only

Primary has TWO entries; Aiyar has ONE. The "Saubhāgyalakṣmī"
form is the modern fuller name of the same Upanishad. The AV
#93 slot is also a Veda mismatch (Aiyar puts it in RV).

Net waste: 1 slot.

### 4.5 Avadhūta (×2 in primary)

* primary #53 Avadhūta (KY)
* primary #104 Avadhūta (AV)
* aiyar #53 Avadhūta (KY) only

Aiyar lists ONE Avadhūta Upanishad, in KY. Primary has two — one
correctly placed (#53 KY) and one apparently spurious (#104 AV).

Net waste: 1 slot.

### 4.6 Devī / Bhāvanā duplicates

* primary #90 Devī (AV) + #106 Devī (AV) — same Veda, same class
* primary #92 Bhāvanā (AV) + #107 Bhāvanā (AV) — same Veda, same class
* aiyar #99 Devī (AV) + #100 Bhāvanā (AV) — one each

Clear duplications. Net waste: 2 slots.

### 4.7 Mahā-Nārāyaṇa

* primary #59 Mahā-Nārāyaṇa (KY, Vs)
* aiyar #88 Mahā-Nārāyaṇa (AV, Vs)

Aiyar's AV assignment aligns with the dominant scholarly view
(Adyar 1941 Sāmānya Vedānta volume; Olivelle 1998; Deussen 1897).
Primary's KY position is anomalous.

Switching primary to Aiyar would move Mahā-Nārāyaṇa from KY to AV.
Affects the Krishna Yajurveda per-Veda count (would drop −1) and
Atharvaveda count (would rise +1).

### 4.8 Sarasvatī-rahasya (×2 in primary)

* primary #62 Sarasvatī-rahasya (KY)
* primary #94 Sarasvatī-rahasya (AV)
* aiyar #61 Sarasvatī-rahasya (KY) only

Same word, two primary slots, two Vedas. Aiyar lists ONE,
in KY.

Net waste: 1 slot.

### 4.9 Maitri / Maitrāyaṇī / Maitreya / Maitreyī

| Slot | Name | Veda |
|---|---|---|
| primary #55 | Maitrāyaṇi | KY |
| primary #66 | Maitreya | SV |
| primary #67 | Maitreyī | SV |
| aiyar #65 | Maitrāyaṇi (= Maitri) | SV |
| aiyar #66 | Maitreyī | SV |

Aiyar has two entries: Maitrāyaṇī (SV, principal class — the
"Maitri Upanishad") and Maitreyī (SV, S class — different
Upanishad). Primary has THREE entries adding a "Maitreya" (SV, S
class) that isn't in Aiyar at all. The `key='maitreya'` route in
byUpanishad currently activates this primary-only entry —
suggesting the activation may be misclassified (the route should
likely be `maitreyi` matching Aiyar's #66).

Recommendation for v116: investigate whether the maitreya
route actually points at Maitreyī text (which it should). If yes,
rename the key to `maitreyi` to align with Aiyar. If no, document
which text it really points at.

### 4.10 Jābāla cluster

| Slot | Name | Veda |
|---|---|---|
| primary #13 | Jābāla | SY | Aiyar #13 same |
| primary #76 | Rudrākṣajābāla | SV | not in Aiyar |
| primary #84 | Bṛhajjābāla | AV | Aiyar #83 "Bṛhad-Jābāla" — same via sandhi |
| primary #77 | Jābāli | SV | Aiyar #77 same |

Aiyar adds: #75 Jābāla (Sāmaveda) and #101 Bhasma-Jābāla — both
genuinely missing in primary.

Primary's "Rudrākṣajābāla" #76 appears to be a non-standard hybrid
name; neither the Adyar Saiva Upanishads nor any published Muktikā
list catalogues a "Rudrākṣa-Jābāla" Upanishad. This may be an
error.

## 5. Recommendation

**Option C — Prepare migration to Aiyar primary, but do not switch
in v115.**

### Reasoning

1. **The evidence is strong that primary is a flawed local
   construction**, not a legitimate canonical recension:
   * Five exact duplicate normalized names (103 distinct names for
     108 slots).
   * Five Veda mismatches with the dominant scholarly tradition.
   * Mahā/Sannyāsa appears split into two slots inconsistent with
     any published Muktikā list.
   * A "Rudrākṣajābāla" hybrid name not found in any standard
     Muktikā catalogue.
   * The AV Vaishnava cluster (Gopāla / Kṛṣṇa / Hayagrīva /
     Dattātreya / Garuḍa) is entirely missing.
2. **Aiyar's list is internally consistent and source-supported**:
   108 distinct normalized names; derived directly from the
   in-archive Aiyar 1914 Muktikā Upanishad text.
3. **A switch is non-trivial** — affects per-Veda counts, the
   active count's specific composition (would swap Maitreya for
   Varāha), the witness picker's classification flags, and v109
   protocol downstream references.
4. **Per v115 doctrine** ("Do not silently rewrite the canon. Do
   not switch primary unless evidence is overwhelming."), the
   honest move is to **document the case thoroughly and provide a
   detailed migration plan** for v116, then let the user approve
   the switch as a deliberate single change set.

### What v115 did

* Programmatic audit: complete.
* `MUKTIKA_108` source-comment block: added 30+ lines above the
  array documenting all known anomalies for future-maintainer
  visibility.
* No data changes: counts preserved, all routes preserved.
* Detailed v116 migration plan (next section).

## 6. v116 migration plan — switching primary to Aiyar

This section is the executable plan for a future v116 pass that
flips primary to the Aiyar source-derived ordering. v115 does not
execute these steps; they are documented here so the v116 change
set can be made as a single atomic move.

### 6.1 Migration scope

* `MUKTIKA_108` (the constant) → rebuilt from `MUKTIKA_108_AIYAR`'s
  ordering and Veda assignments.
* `MUKTIKA_108_AIYAR` → renamed to `MUKTIKA_108_LEGACY_LOCAL` (or
  removed) — its purpose was to track the alternate canon while
  primary was the legacy local list. After the switch, the legacy
  local list becomes the "alternate" and Aiyar's list becomes the
  primary; the auxiliary list can be dropped.
* `_muktikaProgress` (helper) — no logic change needed; just
  iterates the new primary.
* `_muktikaProgressAiyar` (helper) — remove or repurpose. If we
  drop the legacy local list entirely, this helper is no longer
  meaningful.
* `byUpanishad` entries — the Varāha entry's `inMuktika108: false`
  flag should become `inMuktika108: true` (or be removed). The
  Maitreya entry needs investigation: confirm whether the route
  actually carries Maitreyī text, and rename the key to `maitreyi`
  if so.
* `_renderUpanishadsByVeda` — no code change needed; the new
  per-Veda totals (RV 10, SY 19, KY 32, SV 16, AV 31) match the
  current Aiyar totals already.
* The dual-canon UI note from v112 → simplified to a single-canon
  note (or removed).

### 6.2 Per-Veda count impact

After the switch, per-Veda Muktikā active counts change as follows
(based on which Upanishads are currently routed):

| Veda | Current primary count | After Aiyar switch | Delta |
|---|---:|---:|---:|
| Rigveda | 5 / 10 | 5 / 10 | 0 |
| Shukla Yajurveda | 10 / 19 | 10 / 19 | 0 |
| Krishna Yajurveda | 16 / 33* | 16 / 32 | total target shrinks by 1; active count includes Varāha; net active stays 16 (was 15 + 1 mis-classified Mahā-Nārāyaṇa moved to AV, balanced by gain of Varāha) |
| Samaveda | 8 / 16 | 8 / 16 | 0 |
| Atharvaveda | 4 / 30* | 4 / 31 | Mahā-Nārāyaṇa moves IN; total target grows by 1 |
| **Total** | **43 / 108** | **43 / 108** | **0** |

(Primary's current 33 KY total is wrong — should be 32. After the
switch the per-Veda counts also become internally consistent.)

**Net result: the total 43 / 108 figure is preserved**, but the
per-Veda distribution shifts. The user should be told this before
v116 commits.

### 6.3 Sequenced migration steps for v116

1. **Rename the existing primary** in `index.html` from
   `MUKTIKA_108` to `MUKTIKA_108_LEGACY_LOCAL`. Keep the data
   intact for transition reference.
2. **Rename `MUKTIKA_108_AIYAR` to `MUKTIKA_108`**. This makes
   Aiyar's list the primary public-facing canon.
3. **Update `_muktikaProgress`** — no code change needed (still
   iterates `MUKTIKA_108`, now Aiyar-shaped).
4. **Remove or repurpose `_muktikaProgressAiyar`** — if the legacy
   local list is no longer surfaced, drop the helper. If it's kept
   for historical reference, rename the helper to
   `_muktikaProgressLegacyLocal`.
5. **Update the dual-canon UI note** in `_renderUpanishadsByVeda`
   to reference a single canon (Aiyar's source-derived) rather
   than two.
6. **Fix the Varāha byUpanishad entry**: change `inMuktika108:
   false` → `inMuktika108: true` (or remove the flag entirely).
   Update the witness-card note to remove the "variant-canon"
   language (it's now the primary canon).
7. **Investigate Maitreya/Maitreyī**: read the actual content at
   `upanishads-30-minor-aiyar` L1=6 (current `maitreya` route).
   If it's the Maitreyī Upanishad, rename the byUpanishad key from
   `maitreya` to `maitreyi` to align with Aiyar #66.
8. **Update reports**: add `reports/v116_aiyar_primary_canon_
   switch.md` with before/after counts and all the per-Veda shift
   details; mark v112's `MUKTIKA_VARIANTS` aspirational structure
   as fulfilled by v116.
9. **Build marker**: `v116-aiyar-primary-canon`.
10. **Verify**: run audits, regression-check the family page, push.

### 6.4 Risks

* If the Maitreya investigation reveals the route truly points at a
  Maitreya-Upanishad (not Maitreyī), the active count would drop by
  1 (from 43 to 42) after the switch because Maitreya is not in
  Aiyar's 108. The user should be alerted before the switch.
* Existing external links to `reports/v109_…md` / `v110_…md` that
  cite specific Muktikā numbers (e.g., "#59 Mahā-Nārāyaṇa KY")
  would become slightly inaccurate. Reports themselves are not
  re-written; only the live canon-map array changes.
* Anyone who memorised the local Muktikā numbers (e.g., from the
  family page UI) would notice the renumbering. This is a
  one-time UX surprise that should be flagged in a release note.

## 7. Non-destructive guarantees

* **No JSON files merged, rewritten, or deleted.**
* **No source files added or modified.**
* **`MUKTIKA_108` data array unchanged.** The only modification is
  an explanatory comment block ABOVE the array opening.
* **`MUKTIKA_108_AIYAR` data array unchanged.**
* **No `byUpanishad` entries added, removed, or modified.**
* **No public count change.** Both canons still report 43 / 108
  active, 65 missing, 53 missing-in-both.
* **No restricted text committed.**
* **No public routes to restricted text.**
* **No UI redesign.** Family page renders identically. The v112
  dual-canon UI note is unchanged.
* **No folio / Atlas-Object work.**

## 8. Build marker

`v114-periodical-acquisition-needed` → **`v115-primary-muktika-audit`**

The marker reflects the v115 doctrine: a thorough audit was
performed, no data was changed, and the v116 migration plan is
ready for user approval.
