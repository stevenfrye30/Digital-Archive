# v131 — Upanishads wrap-up status

Final audit, documentation, and cleanup pass for the Upanishads section.
No new texts, no source acquisition, no ingestion, no UI redesign, no
`MUKTIKA_108` change. The purpose is to leave the section in a clear,
documented, stable state before moving to the broader Digital Archive /
Atlas / Workspace wrap-up.

## 1. Build

| | |
|---|---|
| Build before v131 | `v130-adyar-config-generator` |
| Build after v131 | **`v131-upanishads-wrapup`** |
| Public Muktikā count | **44 / 108** active (unchanged) |
| Future / source-identified | **64** (unchanged) |
| Source still needed | **0** (unchanged) |

## 2. Public status (verified this pass)

Headless audit on `127.0.0.1` with no opt-in:

* Upanishads page loads; no JS console errors.
* 108-Map view modes all render: **By Veda, By Class, By Status,
  Traditional Sequence**.
* Search / filter / sort / compact (density) run without error.
* **Active** chips → `showUpanishadDetail(...)` (witness picker).
* **Future** chips → `openRestrictedDossier(...)` (metadata dossier).
* Future/restricted dossiers are **metadata only** — they show the
  "metadata-only in the public archive" note and **no** "Open local
  restricted copy" button, and leak no passage text.
* No public route opens copyrighted text.
* Counts: **44 active · 0 local · 64 future · 0 needed · 108 total.**

## 3. Local restricted architecture (verified this pass)

The v124–v127 local-only pipeline remains fail-closed:

* `isRestrictedLocalModeEnabled()` guard matrix (real shipped function
  body): `github.io` + opt-in → **false** (hard-block); `localhost` +
  opt-in → true; `localhost` no flag → **false** (behaves like public).
* `localhost` + `?localRestricted=1` with the local index missing →
  **fails closed** (index not loaded, 0 local chips, no error thrown).
* With local index + source fixtures present: 3 local chips appear
  (test fixture covered #81/82/83), chips → `openRestrictedDossier`
  (**not** direct text), dossier shows "Open local restricted copy".
* The local restricted **reader warning banner** + passages appear
  **only after** clicking "Open local restricted copy"
  (`openLocalRestrictedCopy`), never from the chip or the dossier.
* All fake local fixtures were **removed before commit**;
  `data/_restricted/` is untracked and absent.

## 4. Local tooling (verified this pass)

All tooling lives in `05_scripts/local_only/` (local-only; outside the
`03_web_app` git repo by doctrine):

* `ingest_restricted_source.py --help` → OK.
* `validate_local_restricted.py --help` → OK.
* `generate_adyar_configs.py --all --dry-run` → OK.
* All six Adyar configs parse as JSON and parser-dry-run cleanly:

  | Config | Covered | Exp. PD |
  |---|---|---|
  | `adyar_saiva_1935.config.json` | 13 | 2031 |
  | `adyar_yoga_1938.config.json` | 7 | 2034 |
  | `adyar_samanya_vedanta_1941.config.json` | 11 | 2037 |
  | `adyar_vaishnava_1945.config.json` | 11 | 2041 |
  | `adyar_shakta_1950.config.json` | 9 | 2046 |
  | `adyar_samnyasa_1978.config.json` | 13 | 2074 |

* Validator config cross-check confirmed against a fake-fixture build of
  the Saiva config (coverage matched 13; placeholder allowed via
  `--allow-placeholder`); fixtures then removed.

## 5. Source-family roadmap & public-domain triggers

The 64 future/source-identified Upanishads are fully covered by the six
Adyar family configs (13+7+11+11+9+13 = **64**). All covered entries are
currently `future-public-domain` (or `copyrighted-unavailable` for
Samnyāsa 1978) — none is publicly active, so ingestion changes only the
local view, never the public 44/108.

| Source family | Config | Local gain | PD trigger year | Register status |
|---|---|---|---|---|
| Adyar Saiva 1935 | `adyar_saiva_1935` | +13 | **2031** | public-domain-deferred |
| Adyar Yoga 1938 | `adyar_yoga_1938` | +7 | **2034** | public-domain-deferred |
| Adyar Sāmānya Vedānta 1941 | `adyar_samanya_vedanta_1941` | +11 | **2037** | public-domain-deferred |
| Adyar Vaishnava 1945 | `adyar_vaishnava_1945` | +11 | **2041** | public-domain-deferred |
| Adyar Shakta 1950 | `adyar_shakta_1950` | +9 | **2046** | public-domain-deferred |
| Adyar Samnyāsa 1978 | `adyar_samnyasa_1978` | +13 | **2074** | copyrighted-unavailable |

When a family's copyright expires (or a lawful public-domain witness is
secured + rights re-verified), its entries can graduate from
local-restricted to public-active, raising the public count.

## 6. What has been completed

* **v121–v123** — restricted-source register, metadata-only dossiers,
  the Muktikā 108 Map + usability controls.
* **v124** — local-only restricted loader (fail-closed; `github.io`
  hard-blocked).
* **v125** — local-only parser harness.
* **v126** — local-only validator.
* **v127** — local restricted availability indicator in the 108 Map
  (local-only chips, separate tally, never affects the public count).
* **v128 / v129** — Adyar Saiva (+13) and Adyar Yoga (+7) configs.
* **v130** — Adyar config generator + the remaining four family configs
  (Sāmānya Vedānta +11, Vaishnava +11, Shakta +9, Samnyāsa +13).
* **v131** — this audit/stabilization pass: full verification +
  documentation; no behavior change.

All six Adyar source families are **config-ready** for safe, local-only
ingestion the moment a lawful private copy exists.

## 7. What remains deferred

* **Heading-pattern splitter** — source-aware splitting that consumes
  each config's `coveredUpanishads[].headingPatterns` (explicitly
  deferred to a later return-to-Upanishads phase).
* **Actual ingestion** of any restricted source — requires a lawful
  private copy and is local-only by design; nothing to commit.
* **Local restricted progress dashboard**, **"prepare local source"**
  one-command wrapper, **PD-trigger checklist** automation.
* **Editor/translator metadata verification** against the physical
  copies (configs flag this with "verify exact metadata").

## 8. Do not touch unless we return to this section

* `MUKTIKA_108` and the public active count (44 / 108).
* The fail-closed local loader and the `github.io` hard-block.
* The public dossier metadata-only contract (no copyrighted text on the
  public deploy).
* The hand-written Saiva/Yoga configs (generator produces cosmetic-only
  differences; load-bearing fields already match).
* No `data/_restricted/`, `*.local.json`, OCR/PDF/scans, or copyrighted
  full text may ever be committed; always run
  `05_scripts/check_no_restricted_text.py` before any commit.

## 9. Safety verification (this pass)

* `python 05_scripts/check_no_restricted_text.py` → **PASS** (2008
  tracked files in `03_web_app/`).
* No `data/_restricted/` tracked; no `*.local.json` tracked; no
  restricted OCR/PDF/scans committed; no copyrighted full text committed.

## 10. Recommended next phase

The Upanishads section is **stable and paused**. Move to a **project-wide
Digital Archive / Atlas / Workspace stabilization audit**: confirm the
three-layer ecosystem (Workspace foyer / Atlas OS / Digital-Archive
corpus) is internally consistent, the GitHub Pages deploys are healthy,
and each surface has a current status report — mirroring the audit
discipline applied here. Return to the Upanishads only to build the
heading-pattern splitter or to ingest a lawful copy locally.
