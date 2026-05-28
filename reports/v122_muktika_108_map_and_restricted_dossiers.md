# v122 — Muktikā 108 Map + restricted-source metadata dossiers

v121 created the restricted-source register and placeholder cards.
v122 makes the Upanishads family page feel *complete at the canon
level*: a new "View the 108 Map" button opens a metadata-only
overview of the entire Muktikā 108 — every Upanishad shown as
active / future-public-domain / source-needed — across four view
modes, and the v121 restricted placeholders become clickable
metadata-only dossiers.

All restricted content remains metadata only. No copyrighted text,
excerpts, OCR, scans, download links, or public reading routes were
added. Counts unchanged at 44 / 108 active, 64 missing.

## 1. Summary

| Field | Before v122 | After v122 |
|---|---|---|
| Build marker | `v121-restricted-upanishad-placeholders` | **`v122-muktika-108-map`** |
| `MUKTIKA_108` active | 44 / 108 | 44 / 108 (unchanged) |
| Missing | 64 | 64 (unchanged) |
| "View the 108 Map" button | none | **added** (under intro, above tabs) |
| 108 Map view modes | none | **4** — By Veda / By Class / By Status / Traditional Sequence |
| Restricted placeholder behaviour | static cards | **clickable → metadata-only dossier** |
| Restricted dossier | none | **added** — full per-Upanishad coverage table + rights/PD metadata |
| Placeholder wording | "When activated: 13" | **"Would close: 13 missing Shaiva Muktikā Upanishads"** |
| `RESTRICTED_SOURCES` extended | counts only | **+`coveredNumbers[]` + `classLabel`** on 6 Adyar entries |
| Restricted text committed | none | **none** ✓ |
| Public routes to restricted text | none | **none** ✓ |
| Local restricted loader | disabled (fail-closed) | disabled (unchanged) |

## 2. The 108 Map

### 2.1 Launcher button

Rendered in `browseTextFamily` between the family description and
the existing By Veda / By Text / Traditional order view-switcher,
shown only for families with a Muktikā-108 canon (the Upanishads):

```
The Upanishads
[ View the 108 Map ]        ← new launcher

By Veda | By text | Traditional order
```

Toggling shows the map panel and replaces the normal views (the
launcher stays visible, relabelled "Close the 108 Map"). It does
NOT remove the tabs — closing the map returns to whatever tab was
active.

### 2.2 Default view: By Veda

The map opens in **By Veda** mode (matching the Muktikā structure
and the archive's existing By Veda logic). Five sections in Veda
order (Rigveda, Sāmaveda, Śukla Yajurveda, Kṛṣṇa Yajurveda,
Atharvaveda), each with an active-count label and **all** canon
entries in that Veda (active + missing + future), not just active
ones.

### 2.3 View modes

| Mode | Grouping |
|---|---|
| **By Veda** (default) | 5 Veda sections, each `X / Y active` |
| **By Class** | 7 class sections: Principal, Sāmānya Vedānta, Sannyāsa, Yoga, Shaiva, Vaishnava, Shakta (+ Unclassified) |
| **By Status** | 3 sections: Active in archive / Future public-domain source identified / Source still needed |
| **Traditional Sequence** | all 108 in Muktikā order 1–108 |

### 2.4 Chip states

Each of the 108 entries renders as a compact chip (not a large
reading card):

| State | Visual | Click action |
|---|---|---|
| **Active** | green-tinted, solid border, "Active" badge (or "Active · N" for multi-witness) | opens the witness picker (`showUpanishadDetail`) |
| **Future public-domain** | dashed border, muted, "Future PD 2031" badge (year from the covering Adyar source) | opens the metadata-only dossier for that source |
| **Source needed** | dashed border, more muted, "Source needed" badge | no action (none currently — all 64 missing map to an Adyar source) |

Map summary line at the top shows: `44 active · 64 future
public-domain source identified · 0 source still needed · 108
total`. (All 64 missing are covered by the six Adyar volumes, so the
"source needed" bucket is currently empty — an honest reflection of
v120's finding that the Adyar series covers 100% of the gap.)

## 3. Restricted metadata dossiers

### 3.1 How they open

* From the **By text view**: the v121 "Restricted / Future
  Public-Domain Sources" placeholder cards are now clickable
  (`rs-clickable` class + `openRestrictedDossier(...)`), with a
  "View metadata dossier ›" affordance.
* From the **108 Map**: clicking any future-PD chip opens the
  dossier for the Adyar source covering that Upanishad.

Both set module-scope `_activeDossierId`; `browseTextFamily`
renders the dossier branch (which returns early, before the normal
views). "‹ Back" clears `_activeDossierId`; if the map was open when
the dossier launched, the next render returns to the map, otherwise
to the By-text view.

### 3.2 What the dossier shows (metadata only)

* Source title + family
* Status ("Public-domain deferred" / "Copyrighted — unavailable")
* Translator / editor (+ original author for Bedekar/Palsule)
* Publication year
* Expected public-domain year
* Rights holder + rights-holder confidence (known / likely / unknown)
* Expected coverage gain
* **Covered Upanishads table**: # · name · Veda · class · current
  archive status (Active / Missing) — derived live from
  `coveredNumbers` against `MUKTIKA_108`
* A standing notice: *"No copyrighted text is included in the
  public archive. This dossier is metadata only. The source will
  become readable here only after its copyright expires (expected
  YYYY) and a rights re-verification is performed."*

### 3.3 What the dossier does NOT show

* No full text, no excerpts, no OCR, no scans
* No download links to copyrighted material
* No private local file paths
* No reading-room route

## 4. Data model

### 4.1 `_buildMuktika108Map(fam)`

Derives the enriched 108-entry model at render time from three
sources of truth:

1. **`MUKTIKA_108`** (the public Aiyar-primary canon) — provides
   n / name / veda / cls / key for all 108.
2. **`fam.byUpanishad`** — provides active status + witness data.
   An entry is `active` iff its `key` is non-null AND has ≥1
   safe/safe-start witness.
3. **`RESTRICTED_SOURCES[].coveredNumbers`** — maps each missing
   Muktikā number to the restricted source that would activate it
   (`futureSource`).

Returns per entry: `{ n, name, veda, cls, key, active, witnessCount,
primaryWitness, futureSource }`.

### 4.2 `coveredNumbers` extension

v122 added a `coveredNumbers: [...]` array + `classLabel` to each of
the 6 Adyar `RESTRICTED_SOURCES` entries (the per-Muktikā-number
coverage was previously only in the standalone JSON register). The
six arrays partition the 64 missing numbers exactly:

| Source | coveredNumbers | count |
|---|---|---:|
| Saiva 1935 | 7,39,55,57,74,77,81,82,83,87,96,101,102 | 13 |
| Yoga 1938 | 19,40,45,50,54,68,76 | 7 |
| Sāmānya 1941 | 6,17,42,51,52,58,73,94,95,97,103 | 11 |
| Vaishnava 1945 | 69,71,84,88,89,90,104,105,106,107,108 | 11 |
| Shakta 1950 | 8,9,10,61,86,93,98,99,100 | 9 |
| Samnyāsa 1978 | 5,13,15,21,24,27,28,53,64,70,72,75,92 | 13 |
| **Total** | (64 unique) | **64** |

Verified: 64 unique numbers = exactly the 64 missing entries.

## 5. UI changes

| Element | Change |
|---|---|
| "View the 108 Map" launcher | New button under intro, above tabs |
| 108 Map panel | New metadata-only panel with 4 mode tabs + chip grid |
| Map chips | New compact-chip CSS (`.map108-chip*`) with status badges |
| Restricted placeholder cards | Now clickable (`rs-clickable`) + "View metadata dossier ›" affordance |
| Placeholder coverage wording | "When activated: 13" → **"Would close: 13 missing Shaiva Muktikā Upanishads"** |
| Restricted dossier panel | New metadata-only panel (`.dossier-*` CSS) |

All CSS is additive (new selectors). No existing styles overridden.
The By Veda / By Text / Traditional order views and the reading room
are untouched.

## 6. Copyright safety

| Check | Result |
|---|---|
| No copyrighted full text added | ✓ — `RESTRICTED_SOURCES` and the register are metadata only |
| No OCR / PDF / scans from restricted sources | ✓ |
| No public reading routes to restricted sources | ✓ — future chips + placeholders route only to metadata dossiers |
| Restricted dossiers metadata-only | ✓ — coverage table shows name/Veda/class/status, never text |
| Local restricted loader still fail-closed | ✓ — `isRestrictedLocalModeEnabled()` returns `false`, unchanged |
| Standing "no copyrighted text" notice in every dossier | ✓ |
| Muktikā count unchanged | ✓ — 44 / 108 |
| Missing unchanged | ✓ — 64 |

git-diff review confirms the only committed files are `index.html`
(UI + data-const), the v122 report, and (already-tracked)
`restricted_sources_register.json` is untouched this pass. No new
data files, no raw sources, no `_restricted/` content.

## 7. Verification

| Test | Expected |
|---|---|
| `MUKTIKA_108` parses, 44/108 active | ✓ |
| `MUKTIKA_108_LEGACY_LOCAL` 43/108 | ✓ |
| Build marker `v122-muktika-108-map` | ✓ |
| 8 map/dossier functions present | ✓ (toggle108Map, set108MapMode, openRestrictedDossier, closeRestrictedDossier, _buildMuktika108Map, _render108Map, _renderRestrictedDossier, _map108ChipHTML) |
| 6 `coveredNumbers` arrays, 64 unique numbers | ✓ |
| Added JS block brace/paren/bracket/backtick balanced | ✓ |
| Active map chips → `showUpanishadDetail` (witness picker) | ✓ (existing route reused) |
| Future map chips → `openRestrictedDossier` (no reading room) | ✓ |
| Restricted placeholders → dossier | ✓ |

(Node was unavailable in this session for a full `--check`; balance
verification + targeted parse checks were used instead.)

## 8. v123 recommendation

Three viable directions:

### v123 (recommended): 108 Map search / filter
Add a small text filter box to the 108 Map ("filter by name…") and
optional status filter chips, so a reader can quickly find a
specific Upanishad or see (e.g.) just the Atharvaveda future-PD
entries. Small, self-contained UI addition; high reader value now
that all 108 are visible.

### v123-alt: Local-only restricted loader architecture
Implement the `data/_restricted/` loader path (still default
fail-closed) so a user with lawfully-obtained restricted files can
run the app in local mode and route those Upanishads privately.
Requires user-supplied test data and explicit confirmation of
lawful local files.

### v123-deferred: 2031 Adyar Saiva trigger script (metadata-only)
Write `05_scripts/v_TRIGGER_2031_adyar_saiva.py` as research-only
(IA-identifier hunt + parser template + byUpanishad-route template)
ready to execute when the Ayyangar 1935 Saiva volume enters US PD
on 2031-01-01.

## 9. Non-destructive guarantees

* No JSON files merged, rewritten, or deleted.
* No `MUKTIKA_108` / `MUKTIKA_108_LEGACY_LOCAL` data changes.
* No `byUpanishad` entries added or removed.
* No catalog changes.
* No restricted text committed; no public routes to restricted text.
* No reading-room redesign; no existing-view changes (By Veda / By
  Text / Traditional order render identically when the map is closed).
* No folio / Atlas-Object work.
* Local restricted mode remains disabled (fail-closed).

## 10. Build marker

`v121-restricted-upanishad-placeholders` → **`v122-muktika-108-map`**

The marker reflects the canon-level navigation addition: readers
can now see the entire Muktikā 108 at a glance and drill into
metadata-only dossiers for the future public-domain sources, with
all copyrighted text kept out of the public archive.
