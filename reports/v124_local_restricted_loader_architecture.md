# v124 — Local-only restricted loader architecture

v121 built the metadata-only restricted register; v122/v123 surfaced
it as dossiers and the 108 Map. v124 adds the **local-only restricted
loader**: infrastructure that lets a *private local* build of the
archive read lawfully-obtained restricted/copyrighted source files
from gitignored folders, while the **public GitHub Pages archive
stays metadata-only and copyright-clean**.

Nothing in this pass commits or routes copyrighted text. The loader
is **fail-closed**: disabled by default, hard-blocked on `github.io`,
and only active on a local host with explicit opt-in AND a present
local index AND a present local data file. Counts unchanged at
44 / 108 active, 64 missing.

## 1. Summary

| Field | Before v124 | After v124 |
|---|---|---|
| Build marker | `v124a-muktika-map-overflow-fix` | **`v124-local-restricted-loader`** |
| `isRestrictedLocalModeEnabled()` | stub `return false` | **real fail-closed detector** (host + opt-in, github.io hard-blocked) |
| `loadLocalRestrictedIndex()` | none | **added** (lazy, fail-closed) |
| `openLocalRestrictedCopy()` | none | **added** (local-only contained reader) |
| Committed templates | none | **2** (config + index templates, metadata only) |
| `.gitignore` patterns | v109 `data/_restricted/` | **+`**/_restricted/`, `*.restricted.json`, `*.local.json` family, real config names** |
| Safety script | none | **`05_scripts/check_no_restricted_text.py`** (passing) |
| Dossier copy | metadata note | **public / local-available / local-missing variants** |
| `MUKTIKA_108` / counts | 44 / 108 | 44 / 108 (unchanged) |
| Copyrighted text committed | none | **none** ✓ |
| Public routes to copyrighted text | none | **none** ✓ |

## 2. Public vs local architecture

### Public (GitHub Pages — stevenfrye30.github.io)
* Shows public-domain texts (Müller, Hume, Aiyar, Sastri, Roer, …).
* Shows restricted/future sources as **metadata-only** dossiers +
  108-Map future chips.
* Never includes copyrighted full text, OCR, PDFs, or scans.
* Never routes copyrighted text.
* `isRestrictedLocalModeEnabled()` returns **false** (github.io hard
  block), so no local UI ever appears and no local file is fetched.

### Local (localhost / 127.0.0.1 / ::1 / file://)
* May load restricted files **only** from gitignored `data/_restricted/`.
* Requires explicit opt-in (URL `?localRestricted=1` or localStorage
  flag).
* Fails closed if the flag, local index, or local data file is
  absent → falls back to metadata-only dossier.
* Any restricted text is visibly marked "Local restricted copy" with
  a warning banner and is **never** counted toward the public
  Muktikā 108.

### Fail-closed rule
If local mode is not explicitly enabled, **the app behaves exactly
like the public archive.** If local files are missing, the dossier
shows a metadata-only message — never a broken route.

## 3. Folder structure & .gitignore

### Committed (safe — metadata only)
* `data/restricted_sources_register.json` — public register (v121)
* `data/restricted_templates/restricted_local_config.template.json` — config template
* `data/restricted_templates/restricted_index.local.template.json` — index + local-source-shape template
* `reports/v124_local_restricted_loader_architecture.md` — this doc
* `05_scripts/check_no_restricted_text.py` — safety guard

### Gitignored (local only — never committed)
* `data/_restricted/` and `**/_restricted/` (whole tree)
* `data/_restricted/restricted_local_config.json` (activated config)
* `data/_restricted/restricted_index.local.json` (real local index)
* `data/_restricted/sources/*` (raw restricted OCR/PDF)
* `data/_restricted/generated/*.local.json` (parsed restricted JSON)
* any `*.restricted.json`, `restricted_index.local.json`,
  `restricted_sources.local.json`, `local_restricted_config.json`,
  `restricted_local_config.json`, `*.local.json`

### .gitignore additions (v124)
```
**/_restricted/
*.restricted.json
restricted_index.local.json
restricted_sources.local.json
local_restricted_config.json
restricted_local_config.json
```
Templates are NOT ignored: `data/*.json` matches only direct children
of `data/`, so `data/restricted_templates/*.json` ships; the v124
patterns target the *real* files by exact name and never the
`*.template.json` variants. Verified with `git check-ignore`:
templates → not ignored; `data/_restricted/restricted_index.local.json`
and `data/_restricted/generated/foo.local.json` → ignored.

## 4. Local mode activation

### How to enable locally
1. Serve `03_web_app/` from a local host (localhost / 127.0.0.1) or
   open via `file://`.
2. Opt in **either**:
   * append `?localRestricted=1` to the URL, or
   * run `localStorage.setItem('digitalArchive.localRestricted','true')`
     in the console.
   (A URL opt-in is persisted to localStorage for the session.)
3. Copy `data/restricted_templates/restricted_index.local.template.json`
   → `data/_restricted/restricted_index.local.json` and edit it to
   point at your lawfully-obtained local data files.
4. Place each parsed source at the `localDataPath` you specified
   (e.g. `data/_restricted/generated/adyar-saiva-upanishads-1935.local.json`).
5. Reload. Open a restricted dossier → "Open local restricted copy ›".

### Why GitHub Pages cannot enable it
`isRestrictedLocalModeEnabled()` hard-blocks any host containing
`github.io` (returns false before checking anything else). It also
requires the host to be exactly `localhost` / `127.0.0.1` / `::1` /
`''` (file://). On the public deploy all conditions fail → metadata
only.

### Fallback behavior
* Flag set but no index → console note, dossier shows "no local copy
  was found."
* Index present but data file missing → reader shows "Local
  restricted file not found. Metadata only is available."
* No flag → identical to public behavior.

## 5. Templates committed

### `restricted_local_config.template.json`
`{ enabled:false, mode:'local-only', restrictedIndexPath:…, activation:{…}, notes:[…] }`
— copy to `data/_restricted/restricted_local_config.json`, set
`enabled:true`. No private paths, no text.

### `restricted_index.local.template.json`
`{ version:1, sources:[{ id, status, displayTitle, translator,
publicationYear, expectedPublicDomainYear, rightsHolder,
localDataPath, localRawPath, publicRouteAllowed:false,
localRouteAllowed:true, coveredUpanishads:[…] }], localSourceShape:{…} }`
— includes the expected per-source JSON shape with a placeholder
text field `"[restricted local text omitted from template]"`.

### Expected local source JSON shape
```json
{
  "id": "adyar-saiva-upanishads-1935",
  "restricted": true,
  "availabilityStatus": "local-restricted-available",
  "displayTitle": "Saiva Upanishads (Adyar Library)",
  "translator": "T. R. Srinivasa Ayyangar",
  "publicationYear": 1935,
  "expectedPublicDomainYear": 2031,
  "rightsHolder": "Adyar Library and Research Centre, Chennai (likely)",
  "sourceType": "restricted-local-text",
  "publicRouteAllowed": false,
  "localRouteAllowed": true,
  "hierarchy": ["upanishad", "passage"],
  "passages": [ { "id": "atharvasiras.1", "text": "[local text]" } ]
}
```
Committed templates carry only the placeholder; never real text.

## 6. Dossier behavior

| Mode | Dossier shows |
|---|---|
| Public (default / github.io) | metadata + "This source is metadata-only in the public archive…" |
| Local, index loading | "Local restricted mode enabled — checking for a local copy…" then re-renders |
| Local, local copy present | "Local restricted copy detected…" + **"Open local restricted copy ›"** button |
| Local, no local copy | "Local restricted mode is enabled, but no local copy was found for this source." |

## 7. Restricted reader behavior

`openLocalRestrictedCopy()` renders the fetched local passages into
the family-page scaffold (a contained local reader — NOT the public
reading-room pipeline, to keep restricted text fully isolated from
`indexGroups` / `MUKTIKA_108` / counts). It always shows a prominent
warning banner:

> **Local restricted copy.** This text is loaded only from your
> private local files and is not part of the public GitHub archive.
> It is copyrighted / public-domain deferred (expected public-domain
> year YYYY). Rights holder: …. Not counted in the public Muktikā 108.

No public count change. The text is never persisted, never
re-committed, and only reachable when local mode is truly enabled.

(Full reading-room integration with the restricted text is
deliberately deferred — a contained reader is safer for v124 and
avoids any risk of restricted text leaking into the public
`indexGroups`/catalog. Noted as possible future work.)

## 8. Safety checks

`05_scripts/check_no_restricted_text.py` runs `git ls-files` in
`03_web_app/` and **fails** if any tracked path:
* is under a `_restricted/` directory, or
* is `restricted_index.local.json` / `restricted_sources.local.json` /
  `local_restricted_config.json` / `restricted_local_config.json`, or
* ends with `.restricted.json` or `.local.json`.

It **allows** files whose name contains `template` and the public
`restricted_sources_register.json`.

Run result (this pass): **PASS** — 1998 tracked files scanned; the
only restricted-related tracked files are the public register, the
two templates, and the reports — all metadata only.

## 9. Verification

### Public behavior (unchanged)
| Test | Result |
|---|---|
| 108 Map opens; future chips → metadata dossiers | ✓ |
| By-text restricted placeholders → metadata dossiers | ✓ |
| No "Open local restricted copy" button on public deploy | ✓ (isRestrictedLocalModeEnabled false on github.io) |
| `MUKTIKA_108` 44 / 108, legacy 43 / 108 | ✓ |
| No copyrighted text committed | ✓ (safety script PASS) |

### Fail-closed behavior
| Test | Result |
|---|---|
| Local host, no opt-in → metadata only, no local button | ✓ (optIn false) |
| `?localRestricted=1` but no local index → "checking…" then "no local copy found"; no crash | ✓ (fetch fails → null, fail-closed) |
| github.io host can never enable local mode | ✓ (hard block: `indexOf('github.io') !== -1` → false) |

### Safety
| Test | Result |
|---|---|
| `git check-ignore` on templates → not ignored (committable) | ✓ |
| `git check-ignore` on `data/_restricted/*.local.json` → ignored | ✓ |
| `check_no_restricted_text.py` → PASS | ✓ |
| Whole inline script brace/paren/bracket balanced, backticks even | ✓ |

(Node unavailable for a full `--check`; balance + targeted parse
verification used.)

## 10. v125 recommendation

Three viable directions:

### v125 (recommended): Local-only parser harness for restricted sources
Write a **local-only** parser harness (e.g.
`05_scripts/local_only/ingest_restricted_source.py`, itself placed
under a gitignored path or clearly documented as local-only) that
takes a lawfully-obtained restricted OCR file and produces the
`data/_restricted/generated/<id>.local.json` shape the loader
expects. This makes the v124 architecture actually usable by a user
who has lawful copies, without ever touching the public repo.

### v125-alt: 2031 Adyar Saiva trigger (metadata-only research)
Write `05_scripts/v_TRIGGER_2031_adyar_saiva.py` documenting the IA
identifier hunt + parser template, ready to run when the Ayyangar
1935 Saiva volume enters US PD on 2031-01-01.

### v125-deferred: Optional local-only coverage count
Add a separate, clearly-labelled "Local restricted available: X"
indicator (never mixed with the public 44 / 108) shown only in local
mode. Low priority; the v124 spec preferred keeping the public count
clean and deferring this.

## 11. Non-destructive guarantees

* No copyrighted text, OCR, PDFs, or scans committed.
* No public routes to copyrighted text.
* Local mode disabled by default; hard-blocked on github.io.
* No `MUKTIKA_108` / canon / count changes (44 / 108).
* No reading-room redesign (the local reader is a contained,
  isolated view; the public reading room is untouched).
* No `byUpanishad` / catalog / data-file changes.
* All new CSS additive; all new JS guarded by
  `isRestrictedLocalModeEnabled()`.
* No folio / Atlas-Object work.

## 12. Build marker

`v124a-muktika-map-overflow-fix` → **`v124-local-restricted-loader`**

The marker reflects the safe local-only restricted-loader
infrastructure: the private local archive can read lawfully-obtained
restricted files from gitignored folders, while the public GitHub
archive remains metadata-only and copyright-clean.
