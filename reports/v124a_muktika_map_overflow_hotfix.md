# v124a — Muktikā 108 Map horizontal-overflow hotfix

A small layout-only hotfix. The v123 compact map produced a
horizontal scrollbar because long future badges (e.g. "Future PD
2037 · Adyar Sāmānya Vedānta") plus non-shrinking chips pushed the
chip grid wider than the page. v124a removes the horizontal overflow
without touching canon data, counts, search/filter/sort logic,
dossiers, reading-room behaviour, or the copyrighted-text policy.

## 1. Summary

| Field | Before v124a | After v124a |
|---|---|---|
| Build marker | `v123-muktika-map-usability` | **`v124a-muktika-map-overflow-fix`** |
| Horizontal scrollbar on map | yes (esp. compact) | **none** |
| `MUKTIKA_108` active | 44 / 108 | 44 / 108 (unchanged) |
| Missing | 64 | 64 (unchanged) |
| Search / filter / sort / dossier logic | — | unchanged |
| Copyrighted text | none | none |

## 2. Root cause

* Future-chip badges used `white-space: nowrap` with full text
  ("Future PD 2037 · Adyar Sāmānya Vedānta").
* Chips were flex containers without `min-width: 0`, so their
  min-content width (driven by the nowrap badge + name) could exceed
  the grid track.
* The grid used `auto-fill` with `minmax(220/160px, 1fr)`; a chip
  wider than its track expanded the track past the parent, creating
  horizontal overflow.

## 3. Fixes applied (layout only)

### 3.1 Containers cannot overflow
`.map108-panel`, `.map108-groups`, `.map108-chip-grid` all gained:
```css
max-width: 100%;
box-sizing: border-box;
overflow-x: hidden;
```

### 3.2 Responsive columns (auto-fit + safe minmax)
* Comfortable: `repeat(auto-fit, minmax(220px, 1fr))`
* Compact: `repeat(auto-fit, minmax(180px, 1fr))` (was `auto-fill` / 160px)

`auto-fit` collapses empty tracks so the row always fits the parent.

### 3.3 Chips shrink correctly
`.map108-chip` gained `min-width: 0; max-width: 100%; box-sizing:
border-box;` so a chip never forces its track wider than 1fr.

### 3.4 Names truncate safely
`.map108-chip-name` gained `min-width: 0; overflow: hidden;
text-overflow: ellipsis; white-space: nowrap;` — long names ellipsis
inside the chip instead of expanding it.

### 3.5 Badges bounded
`.map108-badge` gained `flex: 0 0 auto; max-width: 60%; overflow:
hidden; text-overflow: ellipsis;` so even a long badge can't dominate
the chip.

### 3.6 Compact badge shortening
Future chips now render TWO badge spans:
```html
<span class="map108-badge-full">Future PD 2037 · Adyar Vedānta</span>
<span class="map108-badge-compact">PD 2037</span>
```
CSS shows the full form in comfortable mode and the short "PD 2037"
form in compact mode (`.map108-panel--compact`). No re-render is
needed when density toggles — the existing CSS-class swap handles it.

The full source hint stays available via the chip `title` (hover):
`Sāmānya Vedānta Upanishads (Adyar Library), 1941 — metadata only`.

### 3.7 Comfortable label shortened
`_restrictedShortHint()` now shortens the longest class label
"Sāmānya Vedānta" → "Vedānta", so the comfortable badge reads
"Future PD 2037 · Adyar Vedānta" rather than the overflow-prone
"… · Adyar Sāmānya Vedānta".

### 3.8 Controls wrap
`.map108-search` changed to `min-width: 0; flex: 1 1 200px;
box-sizing: border-box;` (was `min-width: 230px`) so it shrinks on
narrow widths. `.map108-controls` gained `max-width: 100%`. The
filter rows, sort row, and mode row already used `flex-wrap: wrap`.

## 4. Verification

| Test | Result |
|---|---|
| Map container `overflow-x: hidden` on panel/groups/grid | ✓ |
| Comfortable grid `auto-fit minmax(220px,1fr)` | ✓ |
| Compact grid `auto-fit minmax(180px,1fr)` | ✓ |
| Chip `min-width:0` + name ellipsis | ✓ |
| Future badge full/compact dual spans + CSS swap | ✓ |
| Compact future badge = "PD 2037" | ✓ |
| `_restrictedShortHint` shortens Sāmānya Vedānta → Vedānta | ✓ |
| Search box can shrink (`min-width:0`) | ✓ |
| `MUKTIKA_108` 44/108, legacy 43/108 | ✓ |
| Build marker `v124a-muktika-map-overflow-fix` | ✓ |
| Whole inline script brace/paren/bracket balanced, backticks even | ✓ |
| Active chips still open witness picker (`showUpanishadDetail`) | ✓ (unchanged) |
| Future chips still open metadata-only dossiers (`openRestrictedDossier`) | ✓ (unchanged) |
| No copyrighted text added | ✓ |

Manual check path (per request): Upanishads → View the 108 Map →
filter "Vedānta" → sort "Future year" → toggle Compact → no
horizontal scrollbar; chips readable; active chips → witness picker;
future chips → metadata dossier.

## 5. Non-destructive guarantees

* CSS-only + a minimal badge-markup change in `_map108ChipHTML`.
* No `MUKTIKA_108` / canon / count / data changes.
* No search/filter/sort/dossier logic changes.
* No reading-room or restricted-source-policy changes.
* No copyrighted text; no public routes to restricted text.
* No folio / Atlas-Object work.

## 6. Build marker

`v123-muktika-map-usability` → **`v124a-muktika-map-overflow-fix`**
