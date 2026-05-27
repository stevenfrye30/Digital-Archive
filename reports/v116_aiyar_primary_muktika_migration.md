# v116 — Aiyar primary Muktikā canon migration (executed)

The v112 dual canon-map architecture and the v115 thorough audit
together established the case for switching the public primary
`MUKTIKA_108` from the legacy local list (which v115 confirmed has
5 exact duplicates, 5+ Veda mismatches, a non-standard
"Rudrākṣajābāla", a bad Mahā/Sannyāsa split, and the omitted AV
Vaishnava cluster) to Aiyar's source-derived list (extracted from
the in-archive *Thirty Minor Upanishads* Muktikā text at L1=2,
verses 2.11–2.17).

v116 executes that migration as a single deliberate change set
following the 10-step plan in v115 §6.3. **The legacy primary array
is preserved as `MUKTIKA_108_LEGACY_LOCAL` for audit history; no
readable byUpanishad route is removed.** The Maitreya/Maitreyī
naming question is resolved in favor of "Maitreya" (matching the
Aiyar source's own chapter heading at L1=6). Varāha is natively
included in the new primary (its v111 variant-canon flag removed).

**Net coverage outcome: 43 / 108 → 44 / 108 active.** The +1
increase is explained in §5 below.

## 1. Summary

| Field | Before v116 | After v116 |
|---|---|---|
| Build marker | `v115-primary-muktika-audit` | **`v116-aiyar-primary-muktika`** |
| Public `MUKTIKA_108` array | legacy flawed local list | **Aiyar source-derived list** |
| Public count | 43 / 108 | **44 / 108** ← +1 (Maitreya activation; see §5) |
| Missing | 65 | **64** |
| Legacy array | `MUKTIKA_108` (was) | renamed to `MUKTIKA_108_LEGACY_LOCAL` (data unchanged) |
| Legacy helper | `_muktikaProgressAiyar` (was) | renamed to `_muktikaProgressLegacy` |
| Active route count (byUpanishad) | 44 (43 in legacy + 1 variant Varāha) | 44 (all now in primary, no variant) |
| Varāha status | variant-canon (`inMuktika108: false`) | natively counted in primary KY #59 |
| Maitreya status | active byUpanishad, primary-only entry, missing from Aiyar list | active, primary #66 SV (Aiyar chapter heading naming) |
| Restricted text committed | none | none |

## 2. Migration steps executed

1. **Renamed `const MUKTIKA_108`** (legacy flawed local map) → **`const MUKTIKA_108_LEGACY_LOCAL`**. Data unchanged. Added DEPRECATION NOTICE comment block above.
2. **Renamed `const MUKTIKA_108_AIYAR`** (Aiyar source-derived map) → **`const MUKTIKA_108`** (new public primary). Updated header comment block to document the v116 promotion + the entry #66 rename.
3. **Updated entry #66 SV** in the new primary: was `key:null, name:'Maitreyī'`, now `key:'maitreya', name:'Maitreya'` to match Aiyar's own chapter title at L1=6 and the actual text content. The existing `key='maitreya'` byUpanishad route now counts toward primary.
4. **`_muktikaProgress(fam)` helper**: code body unchanged — it still iterates `MUKTIKA_108`, which is now the Aiyar-derived array. No logic change needed.
5. **`_muktikaProgressAiyar(fam)` helper** renamed to **`_muktikaProgressLegacy(fam)`** and its body updated to iterate `MUKTIKA_108_LEGACY_LOCAL`. Used by reports/historical-comparison code; not used by the UI.
6. **Varāha `byUpanishad` entry**: removed the `inMuktika108: false` flag added in v111. Updated witness note: removed "Variant-canon" language and the v111-report reference; route is otherwise unchanged (still `textId: 'upanishads-30-minor-aiyar', groupKey: '59', routeQuality: 'safe-start'`).
7. **UI byveda-note** updated: replaced the v112 dual-canon-tracking sentence with a single-canon sentence pointing at v116 report.
8. **Build marker** bumped to `v116-aiyar-primary-muktika`.
9. **No new data files, no new parser scripts, no new index.json entries.** All changes are in `index.html`.

## 3. Before/after canon architecture

### Before v116

```js
// flawed legacy local list — was public primary
const MUKTIKA_108 = [/* 108 entries with 5 duplicates, mis-Vedas, etc. */];

// Aiyar source-derived list — tracked alongside for reports
const MUKTIKA_108_AIYAR = [/* 108 source-derived entries */];

function _muktikaProgress(fam)        { /* iterates MUKTIKA_108 */ }
function _muktikaProgressAiyar(fam)   { /* iterates MUKTIKA_108_AIYAR */ }
```

### After v116

```js
// Public primary — Aiyar source-derived
const MUKTIKA_108 = [/* 108 source-derived entries; was MUKTIKA_108_AIYAR */];

// Legacy local list — preserved for audit history
const MUKTIKA_108_LEGACY_LOCAL = [/* 108 entries; was MUKTIKA_108 */];

function _muktikaProgress(fam)        { /* iterates the new MUKTIKA_108 — Aiyar */ }
function _muktikaProgressLegacy(fam)  { /* iterates MUKTIKA_108_LEGACY_LOCAL — legacy */ }
```

The rename is symmetric. The `_muktikaProgress` body did not need
modification (it always iterates `MUKTIKA_108`; the array now points
at different data).

## 4. Count results

### 4.1 Total active / missing

| Metric | Before v116 (legacy primary) | After v116 (Aiyar primary) | Delta |
|---|---:|---:|---:|
| Active | 43 / 108 | **44 / 108** | **+1** |
| Missing | 65 | 64 | −1 |
| Legacy parallel (now `_LEGACY_LOCAL`) active | (was the same 43) | 43 / 108 (unchanged data) | 0 |

### 4.2 Per-Veda totals

| Veda | Before (legacy) | After (Aiyar primary) | Notes |
|---|---|---|---|
| Rigveda | 4 / 10 | 4 / 10 | No change |
| Shukla Yajurveda | 11 / 19 | 11 / 19 | No change |
| Krishna Yajurveda | 19 / 33 | **19 / 32** | Total target −1 (legacy had Mahā-Nārāyaṇa here; Aiyar puts it in AV). Active stays 19 because Varāha joins KY (+1) and Mahā-Nārāyaṇa leaves (−1) — but neither was previously active, so active is net unchanged at 19 |
| Samaveda | 4 / 16 | **5 / 16** | Active +1 — the Maitreya activation at new #66 SV |
| Atharvaveda | 5 / 30 | **5 / 31** | Total target +1 (Mahā-Nārāyaṇa moved in from KY). Active stays 5 because Mahā-Nārāyaṇa isn't active in either canon |
| **Total** | **43 / 108** | **44 / 108** | **+1** |

### 4.3 byUpanishad-route classification

| Route | Pre-v116 status | Post-v116 status |
|---|---|---|
| All 42 routes that were "counted in both" | counted in legacy primary | counted in new primary |
| `maitreya` route | counted in legacy primary only (legacy #66 SV) | counted in new primary (Aiyar #66 SV, renamed to "Maitreya") |
| `varaha` route | active in Aiyar only (variant-canon, `inMuktika108: false`) | counted in new primary (Aiyar #59 KY); variant-canon flag removed |

**All 44 byUpanishad routes are now counted in the public primary.**
No "variant-canon" / "Aiyar-only" / "legacy-only" route categories
remain. The dual-canon Model C of v112 collapses into a single-canon
Model B post-v116.

## 5. Why the count went 43 → 44 (the Maitreya activation)

The legacy primary's #66 SV slot was "Maitreya" with `key='maitreya'`
(active). The Aiyar source-derived list (formerly
`MUKTIKA_108_AIYAR`) had #66 SV as "Maitreyī" with `key:null`
(inactive). The v112 dual-canon report noted this discrepancy:
primary's 42 active included Maitreya; Aiyar's 42 active included
Varāha; neither overlapped on these two slots, and both totals
happened to be 42. After v110+v111+v113 the totals were 43 each
(Dakshinamurti added to both).

v116 had three valid resolutions for the #66 SV slot:

| Option | #66 SV name | key | Active count | Notes |
|---|---|---|---:|---|
| A — Keep Aiyar's literal enumeration | Maitreyī | `null` | 43 | Honest to Aiyar 2.16 verse spelling; but the `maitreya` byUpanishad route stops being counted; risky |
| B — Use Aiyar chapter heading | Maitreya | `'maitreya'` | 44 | Matches Aiyar L1=6 chapter title ("Maitreya-Upanishad of Samaveda") and the actual text content (King Brhadratha + sage Maitreya + Mahadeva dialogue); the `maitreya` route stays counted |
| C — Treat as two separate slots | (extra slot) | mixed | 45 | Add a Maitreyī slot AND a Maitreya slot; would push total past 108 |

**Selected: Option B.** Aiyar's own chapter title in the source
file (`"Maitreya-Upanishad of Samaveda"`) is taken as the more
authoritative signal than the enumeration-verse spelling, because:

1. Chapter headings are typically more carefully copyedited than
   running list-verses.
2. The actual text at L1=6.1 opens with "A KING named Brhadratha,
   thinking this body to be impermanent…" — this is the canonical
   *Maitreya* tradition (sage Maitreya teaches via Brhadratha's
   penance + Sakayanya's instruction in L1=6, then sage Maitreya
   approaches Mahadeva at L1=7.1). The *Maitreyī* tradition (the
   Yajnavalkya-Maitreyī dialogue in Brihadaranyaka IV) is a
   different text and content.
3. Reclassifying as Maitreya activates the existing route without
   removing or adding any new ones — the cleanest non-destructive
   resolution.

The chosen name is documented in the v116 header comment above
the new `MUKTIKA_108` array (point #4 in the migration history
list).

**Net effect: +1 active. This is an honest count fix, not an
inflation.** The Maitreya text has always been active in
byUpanishad (since v107 or earlier) but was previously matched
only to legacy primary's #66 entry. After v116 it matches Aiyar
primary's #66 entry too.

## 6. Maitri / Maitrāyaṇī / Maitreya / Maitreyī — full picture

| In source | Veda | Key | Counted | Notes |
|---|---|---|---|---|
| Müller Part 2 pid='6.348' "Maitrayana-Brahmana-Upanishad" | SV (Aiyar primary) | `maitri` | ✓ (Aiyar #65 SV) | Principal Maitri Upanishad; the longer 7-prapathaka text. Now correctly Veda-classified as SV per Aiyar, was KY in legacy primary. |
| Hume 1921 groupKey='maitri' | SV | `maitri` | ✓ | Hume second-witness route for the same principal Maitri. Auto-aligned. |
| Aiyar L1=6 "Maitreya-Upanishad" | SV | `maitreya` | ✓ (Aiyar primary #66 SV) | The shorter Maitreya tradition; Brhadratha + Sakayanya + sage Maitreya & Mahadeva. Now counted in primary post-v116. |
| Maitreyī Upanishad (Brihadaranyaka IV variant) | — | — | not active | Distinct text from Maitreya; not currently routed. If a future PD English translation surfaces, would be a new byUpanishad entry; would NOT count in current primary's #66 (that slot is now Maitreya). |

The principal Maitri (Yajnavalkya source) remains correctly active
under SV. The Maitreya minor Upanishad is now correctly active
under SV. Maitreyī Upanishad is genuinely missing and unrouted —
documented as an acquisition gap for v117+.

## 7. Legacy anomalies — preserved but no longer public-counted

The legacy primary's known issues (per v115 §3) are still present
in `MUKTIKA_108_LEGACY_LOCAL` for audit history but no longer
drive the public count:

| Anomaly | Legacy slot(s) | Aiyar primary slot |
|---|---|---|
| Avadhūta ×2 | legacy #53 KY + #104 AV | aiyar #53 KY (one slot only) |
| Bhāvanā ×2 | legacy #92 AV + #107 AV | aiyar #100 AV (one slot only) |
| Devī ×2 | legacy #90 AV + #106 AV | aiyar #99 AV (one slot only) |
| Sarasvatī-rahasya ×2 | legacy #62 KY + #94 AV | aiyar #61 KY (one slot only) |
| Tripurā ×2 (×4 with tapinī variants) | legacy #8 RV + #91 AV + #89/#105 tapinī | aiyar #8 RV + #98 tapinī (two slots) |
| Mahā-Nārāyaṇa mis-Veda | legacy #59 KY | aiyar #88 AV (canonical position) |
| Saubhāgya mis-Veda + duplicate | legacy #9 (RV "Saubhāgyalakṣmī") + #93 (AV "Saubhāgya") | aiyar #9 RV (one slot, "Saubhāgya") |
| Maitrāyaṇī mis-Veda | legacy #55 KY | aiyar #65 SV (canonical position) |
| "Mahā" + "Sannyāsa" split | legacy #71 + #72 SV | aiyar #70 SV (one slot, "Mahat-Sannyāsa") |
| Non-standard "Rudrākṣajābāla" | legacy #76 SV | (not present in Aiyar; aiyar has Rudrākṣa #74 + Bhasma-Jābāla #101 as the related canonical pair) |
| Missing AV Vaishnava cluster | (not present in legacy) | aiyar #102–108: Gaṇapati, Mahāvākya, Gopāla-tāpanī, Kṛṣṇa, Hayagrīva, Dattātreya, Garuḍa |

The Aiyar primary is internally consistent (108 distinct
normalized names; matches Aiyar's own enumeration; clean per-Veda
totals 10/19/32/16/31 = 108).

## 8. UI changes

Single sentence change in the family-page `byveda-note` paragraph:

**Before (v112 dual-canon):**
> *The archive tracks two Muktikā lists in parallel: the primary
> 108 (shown in the counts here) and the Aiyar source-derived 108
> (extracted from the in-archive Muktikā Upanishad text); see*
> `reports/v112_muktika_canon_reconciliation.md` *for the variant-
> canon audit.*

**After (v116 Aiyar-primary):**
> *The 108 target now follows Aiyar's Muktikā list as preserved
> in the archive's* Thirty Minor Upanishads *source (Aiyar 1914,
> L1=2 verses 2.11–2.17). A legacy local map is retained in the
> source for audit history; see* `reports/v116_aiyar_primary_muktika_migration.md`*.*

No layout, tile, tab, button, or canon-selector changes. The
per-Veda count badges update automatically (KY badge goes from
"19 / 33" to "19 / 32"; SV from "4 / 16" to "5 / 16"; AV from
"5 / 30" to "5 / 31"; RV unchanged at "4 / 10"; SY unchanged at
"11 / 19").

The total counter (if any visible) goes from "43 / 108" to
**"44 / 108"**.

## 9. Regression verification

| Test | Result |
|---|---|
| `const MUKTIKA_108 = [` resolves to Aiyar list (108 entries, 44 active) | ✓ |
| `const MUKTIKA_108_LEGACY_LOCAL = [` resolves to legacy list (108 entries, 43 active) | ✓ |
| `const MUKTIKA_108_AIYAR` no longer exists | ✓ |
| `_muktikaProgress` function unchanged | ✓ |
| `_muktikaProgressLegacy` exists with new body | ✓ |
| `_muktikaProgressAiyar` no longer exists | ✓ |
| All 44 byUpanishad routes are matched in new primary | ✓ — 0 orphans |
| Varāha byUpanishad entry: `inMuktika108: false` removed | ✓ |
| Maitreya activation: new primary #66 SV has `key:'maitreya'` | ✓ |
| Build marker is `v116-aiyar-primary-muktika` | ✓ |
| Per-Veda totals: 10 + 19 + 32 + 16 + 31 = 108 | ✓ |
| Per-Veda actives: 4 + 11 + 19 + 5 + 5 = 44 | ✓ |
| No restricted text committed | ✓ |
| No source files merged / deleted | ✓ |
| No data files / parser scripts added | ✓ |
| No `index.json` changes | ✓ |
| Hume witnesses (v109) — routes intact | ✓ |
| Dakshinamurti route (v113) — intact | ✓ |
| Pāingala / Maṇḍalabrāhmaṇa / Yogakuṇḍalinī (v110) — intact | ✓ |
| Muktikā (v107) — intact | ✓ |
| Subāla / Tejobindu (v104) — intact | ✓ |
| Varāha route to Aiyar L1=59 — intact | ✓ |
| 13 principals all active — Hume + Müller — intact | ✓ |

## 10. v117 recommendation

With the canon-map now source-backed and internally consistent,
acquisition can resume productively. The new primary's
missing-list (64 entries) is the clean target. Priority paths
ranked by yield-per-effort:

### v117 (recommended): Acquire Sastri & Jha 1898–1901 (5 vols)
Per v114 §4.2 + §6.1, *The Upanishads and Sri Sankara's
Commentary* (S. Sitarama Sastri + Ganganath Jha, Madras 1898–1901)
is the highest-value PD-safe Sankara-commentary English translation
not yet in the archive. Covers principals only — doesn't reduce
the 64 missing — but adds scholarly-grade second/third witnesses
across the 13 principals. Risk: low. Pattern: same as v109 Hume.

### v118: Tattvabhushan 1900–1904 (3 vols)
*The Upanishads, edited with Annotations and English Translation*
by Sitanath Tattvabhushan, Calcutta 1900–1904. Same role —
scholarly principal-Upanishad second witnesses. Risk: low.

### v119: Theosophist back-issue micro-search
If the user can supply specific Internet Archive item identifiers
(IA's JS-rendered search isn't WebFetch-parseable), individual
pre-1929 English translations of minor Upanishads from the
*Theosophist* / *Theosophical Quarterly* / *Indian Antiquary* /
*JRAS* archives could potentially close 1–5 of the 64 missing
entries. Yield: small but missing-targeted.

### v120 / scheduled: 2031 Adyar Saiva trigger
Document the precise Internet Archive identifier for Ayyangar's
1935 *Saiva-Upanishads* (Adyar) and the acquisition pipeline for
automatic ingestion on 2031-01-01 (US-PD entry). Would close 7+
of the 64 missing entries (Akṣamālā, Kālāgnirudra, Rudrahṛdaya,
Pañcabrahma, Atharvaśiras, Atharvaśikhā, Pāśupatabrahma — and
possibly Bṛhad-Jābāla, Śarabha, Bhasma-Jābāla, Gaṇapati if
covered in same volume).

## 11. Non-destructive guarantees

* **No JSON files merged, rewritten, or deleted.**
* **No source files added or modified.**
* **No `byUpanishad` entries added or removed.** Only the Varāha
  entry's variant-canon flag removed; route data unchanged.
* **Legacy primary array data preserved verbatim** as
  `MUKTIKA_108_LEGACY_LOCAL`.
* **No restricted text committed.**
* **No public routes to restricted text.**
* **No UI redesign.** Single-sentence note update in an existing
  paragraph; per-Veda badges and total counter update automatically
  because they bind to the (now Aiyar-derived) `MUKTIKA_108`.
* **No folio / Atlas-Object work.**
* **No new acquisition.** This was a canon-architecture pass only.

## 12. Build marker

`v115-primary-muktika-audit` → **`v116-aiyar-primary-muktika`**

The marker reflects the architectural change: the Aiyar source-
derived list is now the public primary canonical target; the legacy
local list is preserved as audit history.
