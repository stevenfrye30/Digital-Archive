# v123 — Muktikā 108 Map usability polish

v122 introduced the 108 Map. v123 makes it practical: search,
filter chips, alphabetical/active-first/future-year sorting, a
compact density toggle, a legend, improved group-header summaries,
source-family hints on future chips, a single clean exit control,
and a clarified Principal label.

All changes are display-only. No canon data, counts, texts, reading
routes, or copyrighted material were touched. Counts unchanged at
44 / 108 active, 64 missing.

## 1. Summary

| Field | Before v123 | After v123 |
|---|---|---|
| Build marker | `v122-muktika-108-map` | **`v123-muktika-map-usability`** |
| `MUKTIKA_108` active | 44 / 108 | 44 / 108 (unchanged) |
| Missing | 64 | 64 (unchanged) |
| Close controls | 2 (launcher "Close the 108 Map" + internal "Close map ✕") | **1** (launcher relabels to "← Back to Upanishads"; internal control removed) |
| Search box | none | **added** (live, focus-preserving) |
| Filter chips | none | **11** (4 status + 7 class) |
| Sort options | none | **4** (Traditional / Alphabetical / Active first / Future year) |
| Density toggle | none | **Comfortable / Compact** |
| Legend | none | **added** |
| Group-header future-PD summary | none | **added** ("13 future PD 2031", "26 future PD 2031–2074") |
| Future-chip source hint | "Future PD 2031" | **"Future PD 2031 · Adyar Saiva"** (+ hover title) |
| Principal label | "Principal (Mukhya)" | **"Principal / Mukhya-class"** |
| Copyrighted text committed | none | **none** ✓ |
| Public routes to restricted text | none | **none** ✓ |

## 2. Search

* **Location**: inside the map panel, below the summary + legend,
  above the filter chips.
* **Implementation**: focus-preserving. The `oninput` handler calls
  `set108MapSearch(value)` → `_apply108MapView()`, which manipulates
  the already-rendered chip DOM (show/hide/reorder) rather than
  re-rendering the page. The search box never loses focus while
  typing.
* **Fields searched** (per chip `data-search` blob, lowercased):
  Upanishad name, normalized key, Veda, class label, status word
  ("active" / "future public-domain" / "source needed"), future
  source family ("Adyar Saiva" etc.), future source full title, and
  expected public-domain year.
* **Result count**: a live "Showing N of 108" appears next to the
  box (or "108 entries" when no search/filter is active).
* **Clear**: a small "clear" link resets the search.
* **Examples tested** (logic-verified against `data-search` blobs):
  * "Trip" → Tripurā, Tripura-tāpinī
  * "Jabala" → Jābāla, Bṛhad-Jābāla, Bhasma-Jābāla, Jābāli, Jābāla (Sāmaveda)
  * "2031" → the 13 Saiva future entries (their PD year is 2031)
  * "Shaiva" → all Shaiva-class entries
  * "active" → all active entries
  * "Adyar Saiva" → the 13 Shaiva future entries
  * "Mundaka" → Muṇḍaka

## 3. Filters

* **Status row**: All · Active · Future PD · Source needed
* **Class row**: Principal · Vedānta · Sannyāsa · Yoga · Shaiva · Vaishnava · Shakta
* **Behavior**: a single active filter (status OR class) combines
  with the search query (both must match for a chip to show).
  Default = **All**.
* Filter buttons carry `data-filter` and get an `--active` class via
  `_apply108MapView()`.

## 4. Sorting (display-only)

| Option | Behavior |
|---|---|
| **Traditional** (default) | by Muktikā number 1–108 within each current group |
| **Alphabetical** | by name A–Z within each current group (or globally in Traditional Sequence mode) |
| **Active first** | active entries before future before needed, then by Muktikā number |
| **Future year** | active first, then future entries by expected PD year ascending, then name |

Sorting reorders only the visible chip DOM nodes (`grid.appendChild`
in sorted order). **The canon order/data is never changed** — this
is purely a display reordering computed by `_map108ChipCmp()` from
each chip's `data-n` / `data-name` / `data-status` / `data-pdyear`
attributes.

In **Traditional Sequence** mode, the single 1–108 group is
reordered by whichever sort is active (Traditional → 1–108;
Alphabetical → A–Z across all 108; Active first → active block then
future; Future year → active then by PD year).

## 5. Compact mode

A **Display: Comfortable / Compact** toggle in the sort row adds
`map108-panel--compact` to the panel. Compact mode:

* reduces chip padding (12px→6px horizontal, min-height 22px→16px)
* shrinks chip name font (13px→11.5px) and number font (10px→9px)
* shrinks badges (9.5px→8.5px)
* narrows the grid column minimum (220px→160px → more columns)
* tightens group-label vertical spacing

Result: substantially less scrolling while keeping every chip
readable and badges visible. Default remains Comfortable.

## 6. Group-header summaries + legend

### 6.1 Headers

Each group header now shows active count plus a concise future-PD
summary derived from the group's covered future sources:

* Single future year: `Shaiva — 1 / 14 active · 13 future PD 2031`
  (note: in **By Class** view "Shaiva" shows all 14 Shaiva-class
  entries — 1 active Dakṣiṇāmūrti + 13 future)
* Multiple future years in one group (e.g. a Veda group spanning
  several Adyar volumes): `Atharvaveda — 5 / 31 active · 26 future
  PD 2031–2074`

### 6.2 Legend

A small italic legend under the summary:

> **Active** = readable now · **Future PD** = known source, not
> publicly readable yet · **Source needed** = no source identified.
> Click an active entry to choose a witness; click a future entry to
> view metadata only.

## 7. Future-chip source hints

Future chips now show the covering source family inline:
`Future PD 2031 · Adyar Saiva` (compact mode shrinks the font but
keeps the text). Each future chip also has a `title` attribute
("Saiva Upanishads (Adyar Library) — metadata only") for hover.
Clicking still opens the metadata-only dossier — no reading-room
route.

The `_restrictedShortHint()` helper produces "Adyar Saiva", "Adyar
Yoga", etc. from the source's `classLabel` + `sourceFamily`.

## 8. Single exit control

The redundant pair from v122 is resolved:
* The internal "Close map ✕" button was **removed** from the map
  panel head.
* The top launcher button **relabels** to "← Back to Upanishads"
  while the map is open (and back to "View the 108 Map" when closed).

One clear exit, no competing controls.

## 9. Principal label clarified

`_MAP108_CLASS_LABELS.M` changed from "Principal (Mukhya)" to
**"Principal / Mukhya-class"** — signalling that this is the
archive's Muktikā class tag (14 entries) rather than the
"10/11/12/13 principal Upanishads" a reader might expect from other
classifications. Data unchanged; label only.

## 10. Restricted dossier regression

| Test | Result |
|---|---|
| Future map chips still open metadata-only dossiers | ✓ — `openRestrictedDossier` unchanged |
| By-text restricted placeholders still open dossiers | ✓ — `_restrictedSourceTileHTML` clickable path unchanged |
| Dossier "‹ Back" returns to map (if opened from map) or By-text | ✓ — `closeRestrictedDossier` unchanged |
| Dossiers show covered-Upanishad table | ✓ |
| No copyrighted text appears anywhere | ✓ |

## 11. Verification

| Test | Result |
|---|---|
| `MUKTIKA_108` active 44 / 108 | ✓ |
| `MUKTIKA_108_LEGACY_LOCAL` 43 / 108 | ✓ |
| Build marker `v123-muktika-map-usability` | ✓ |
| 8 new/updated functions present | ✓ (set108MapSearch, clear108MapSearch, set108MapFilter, set108MapSort, set108MapCompact, _apply108MapView, _map108ChipCmp, _restrictedShortHint) |
| Internal "Close map ✕" removed | ✓ |
| Launcher relabels to "← Back to Upanishads" | ✓ |
| Principal label updated | ✓ |
| v123 JS block balanced (braces/parens/brackets/backticks) | ✓ |
| **Whole inline-script** balanced (2315/2315 braces, 6018/6018 parens, 878/878 brackets, 782 backticks even) | ✓ |
| Active chips open witness picker | ✓ (showUpanishadDetail reused) |
| Future chips open metadata-only dossiers | ✓ |
| No reading-room route to restricted text | ✓ |
| No copyrighted text committed | ✓ |

(Node was unavailable for a full `--check`; whole-script balance
verification + targeted parse checks were used.)

### Focus-preservation note

The search box uses client-side DOM manipulation
(`_apply108MapView`), not a full re-render, specifically so the
input keeps focus on every keystroke. Mode switching (By Veda / By
Class / By Status / Traditional Sequence) still does a full
re-render — but after re-render, `browseTextFamily` restores the
search value into the new input and re-applies the view, so
search/filter/sort/density persist across mode switches.

## 12. v124 recommendation

Three viable directions:

### v124 (recommended): Local-only restricted loader architecture
Implement the `data/_restricted/` loader path (still default
fail-closed via `isRestrictedLocalModeEnabled()`), so a user with a
lawfully-obtained restricted file (e.g. a personal copy of the Adyar
Saiva volume) can run the app in local mode and route those
Upanishads privately — while the public Pages deploy never sees
them. Requires user confirmation of lawful local files + a test
file.

### v124-alt: 2031 Adyar Saiva trigger script (metadata-only)
Write `05_scripts/v_TRIGGER_2031_adyar_saiva.py` as research-only:
IA-identifier hunt strategy, parser template (mirrors v117/v118
Sastri), and byUpanishad-route template, ready to execute when the
Ayyangar 1935 Saiva volume enters US PD on 2031-01-01. No source
download; no restricted text.

### v124-deferred: Apply the 108 Map to other families
If/when another text family gains a canon list (e.g. a fixed
canon of another tradition), generalise the 108-Map machinery
(`_buildMuktika108Map`, `_render108Map`, `_apply108MapView`) into a
reusable canon-map component.

## 13. Non-destructive guarantees

* No JSON files merged, rewritten, or deleted.
* No `MUKTIKA_108` / `MUKTIKA_108_LEGACY_LOCAL` data changes.
* No `byUpanishad` entries added or removed.
* No catalog / data-file changes.
* No restricted text committed; no public routes to restricted text.
* No reading-room redesign; By Veda / By Text / Traditional order
  family views render identically.
* `RESTRICTED_SOURCES` data unchanged (the `coveredNumbers` arrays
  added in v122 are reused; v123 added no new data).
* Local restricted mode remains disabled (fail-closed).
* No folio / Atlas-Object work.
* All v123 CSS is additive (new selectors only).

## 14. Build marker

`v122-muktika-108-map` → **`v123-muktika-map-usability`**

The marker reflects the usability polish: the Muktikā 108 Map is now
searchable, filterable, sortable, compact-able, legibly summarised,
and has a single clean exit — while preserving the safe
metadata-only structure from v122.
