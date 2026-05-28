# v127 — Local restricted availability indicator (Muktikā 108 Map)

v124 built the fail-closed local loader, v125 the producer, v126 the
validator. v127 surfaces the result **in the Muktikā 108 Map**: when a
lawfully-obtained local copy exists for an otherwise-missing Upanishad,
the map shows a distinct **"Local restricted"** chip — but only in local
mode. On the public GitHub Pages deploy nothing changes.

Contains no copyrighted text. The public Muktikā count stays **44 / 108**.
Local chips open the **metadata dossier** (never the text directly); the
text only loads via the dossier's explicit "Open local restricted copy"
button, which itself appears only in local mode.

## 1. Summary

| Field | Before v127 | After v127 |
|---|---|---|
| Build marker | `v126-local-restricted-validator` | **`v127-local-restricted-availability`** |
| 108-Map status | active / future / needed | + **local restricted** (local only) |
| Public active count | 44 / 108 | 44 / 108 (unchanged) |
| `MUKTIKA_108` array | untouched | untouched |
| Local restricted UI on `github.io` | n/a | **never rendered** ✓ |
| Copyrighted text committed | none | **none** ✓ |
| `data/_restricted` / `*.local.json` committed | none | **none** ✓ |

## 2. What changed in `index.html`

All additions are gated behind the unchanged `isRestrictedLocalModeEnabled()`
guard (hard-blocks `github.io`, requires a local host **and** explicit
opt-in). The guard itself was **not** modified in v127.

* **`_buildMuktika108Map`** — when local mode is on and a valid local
  index is loaded, builds a `localByNum` map from index sources where
  `publicRouteAllowed === false`, `localRouteAllowed === true`,
  `status === 'local-restricted-available'`, and a `localDataPath` is
  present. A `localSource` is attached to a 108 entry **only when that
  entry is not already public-active** — local availability never
  overrides or inflates the public active count. `futureSource` is
  suppressed when a `localSource` exists (so an entry is counted once).
* **`_map108ChipHTML`** — renders a `map108-chip--local` chip (golden
  double border, "Local restricted · PD <year>" badge). Its `onclick`
  is `openRestrictedDossier(...)` — the metadata dossier, never a direct
  text route.
* **`_render108Map`** — separate `localN` tally; summary line gains a
  "**N** local restricted available" segment in local mode only; legend
  and the "Local restricted" status-filter chip appear only in local
  mode and only when `localN > 0`.
* **`_apply108MapView` / `_map108ChipCmp`** — `local` added to the
  status-filter set and sort ranking (between `active` and `future`).
* **108-Map render branch** — in local mode, lazily loads the local
  index once, then re-renders so the map paints availability. No-op on
  public (guard is false → loader returns null).
* **Dossier (`_renderRestrictedDossier`, from v124)** — unchanged
  behaviour: the "Open local restricted copy" button is emitted only
  inside `if (isRestrictedLocalModeEnabled())`. Public mode shows the
  metadata-only note instead.
* **`<meta name="atlas-build">`** bumped to
  `v127-local-restricted-availability`.

## 3. Verification

Tested headless (Chromium / Playwright) against a local HTTP server,
using **temporary fake fixtures** under `data/_restricted/` (gitignored;
contain no real text; deleted before commit). The fixture declared a
local source `adyar-saiva-upanishads-1935` covering Muktikā numbers
81, 82, 83.

### Public mode — `127.0.0.1`, no opt-in (no fixtures needed)

| Check | Result |
|---|---|
| `isRestrictedLocalModeEnabled()` | `false` |
| Counts (active / local / future / needed / total) | **44 / 0 / 64 / 0 / 108** |
| Summary | `44 active · 64 future public-domain source identified · 0 source still needed · 108 total.` |
| Local chip / filter / summary present | **none** |
| JS console errors | **none** |

### `github.io` hard-block — real shipped guard body, fake `location`

| Host + opt-in | `isRestrictedLocalModeEnabled()` |
|---|---|
| `stevenfrye30.github.io` + `?localRestricted=1` | **`false`** (hard-blocked) |
| `localhost` + `?localRestricted=1` | `true` |
| `localhost`, no opt-in | `false` |

### Local mode — `127.0.0.1` + `?localRestricted=1`, fixtures present

| Check | Result |
|---|---|
| `isRestrictedLocalModeEnabled()` | `true` |
| Local index loaded (sources) | yes (1) |
| Local count / numbers | **3** → 81, 82, 83 |
| Summary | `44 public active · 3 local restricted available · 61 future public-domain pending · 0 source still needed · 108 total.` |
| Public **active** count | **still 44** (local carved out of *future*, 64 → 61) |
| Local chip class / filter / summary present | **yes** |
| Local chip `onclick` | `openRestrictedDossier('upanishads','adyar-saiva-upanishads-1935')` |
| Chip routes to direct text (`browseText`/`loadText`/`openLocalRestrictedCopy`) | **no** |
| Dossier shows "Open local restricted copy" | **yes** (`onclick="openLocalRestrictedCopy(...)"`) |
| Dossier leaks passage text | **no** (metadata only) |
| JS console errors | **none** |

### Local host, **no** opt-in, fixtures still on disk

| Check | Result |
|---|---|
| `isRestrictedLocalModeEnabled()` | `false` |
| Local index loaded | **no** (fail-closed) |
| Local count | 0 |
| Local chip / summary present | **none** |

### Public dossier — local-copy button gating

| Check | Result |
|---|---|
| "Open local restricted copy" button | **absent** |
| Public metadata-only note | present |

## 4. Safety boundary

* `isRestrictedLocalModeEnabled()` unchanged: `github.io` hard-blocked;
  requires local host **and** opt-in; fails closed on any error.
* All v127 UI is dead code on the public deploy (guard returns false →
  `localByNum` stays empty → no local chips, no local summary segment,
  no local filter, no "Open local restricted copy" button).
* `MUKTIKA_108` and the public active count (44) are untouched; local
  availability is a separate tally drawn from *future/needed* entries.
* No copyrighted text is committed. `data/_restricted/` and
  `*.local.json` remain gitignored; the fake test fixtures were deleted
  before commit. `05_scripts/check_no_restricted_text.py` passes.

Committed v127 artifacts in `03_web_app/`: the `index.html` changes
(build marker + 108-Map availability logic) and this report.
