# v121 — Restricted-source architecture for Upanishads

After v120 documented the 64 missing Muktikā Upanishads and the
six-volume Adyar Library English Series that would eventually
close them, v121 builds the architecture for honestly representing
those restricted sources in the public GitHub-Pages archive
without ever publishing copyrighted text.

The doctrine has two halves:

1. **Public**: metadata-only placeholder cards that show the
   reader exactly which sources COULD close the missing-64,
   when they become PD-safe, who owns the rights, and what they
   cover.
2. **Local**: a fail-closed-by-default architecture allowing a
   future local build to load lawfully-obtained restricted files,
   while the public Pages deploy NEVER references them.

v121 implements (1) fully and stubs (2). Counts unchanged at
44 / 108 active, 64 missing.

## 1. Summary

| Field | Before v121 | After v121 |
|---|---|---|
| Build marker | `v120-missing-64-acquisition-strategy` | **`v121-restricted-upanishad-placeholders`** |
| `MUKTIKA_108` active | 44 / 108 | 44 / 108 (unchanged) |
| Missing | 64 | 64 (unchanged) |
| `RESTRICTED_SOURCES` const | none | **8 entries** (6 Adyar + Bedekar/Palsule 1980 + Marabathina 2024) |
| `_restrictedSourceTileHTML()` helper | none | **added** — renders distinct muted placeholder cards |
| `isRestrictedLocalModeEnabled()` stub | none | **added** — returns `false` by default (fail-closed) |
| `data/restricted_sources_register.json` | none | **created** — separate metadata-only JSON for tooling that prefers external files |
| CSS for `.restricted-source-tile` / section | none | **added** — dashed border, muted background, no hover lift, no clickable readability |
| Restricted text committed | none | **none** ✓ |
| Public routes to restricted text | none | **none** ✓ |

## 2. Restricted-source policy

### 2.1 What CAN be public
* **Bibliographic metadata only**: title, translator, editor, publication year, publisher, ISBN-like identifier
* **Expected public-domain year** computed from US-copyright term (95 years from publication for URAA-restored works; or earlier if source-country PD on 1996-01-01)
* **Rights-holder attribution** ("Adyar Library and Research Centre, Chennai (likely)" — with explicit confidence level)
* **Coverage summary**: list of Upanishads that would be activated
* **Expected coverage gain** (numeric)
* **Status flag**: `copyrighted-unavailable` / `public-domain-deferred` / `local-restricted-available` / `local-restricted-missing` / `metadata-only` / `future-trigger-ready`

### 2.2 What CANNOT be public
* **Full text** of the source under any circumstances while restricted
* **Substantial excerpts** (≥1 paragraph beyond title or short quotation)
* **OCR / PDF / scan** of copyrighted material
* **Data JSON files** generated from restricted sources
* **Reading-room routes** to restricted content
* **Direct download links** to copyrighted OCR
* **Local file paths** that would reveal a private user's files

### 2.3 Local-mode architecture (fail-closed)
* A user with a lawfully-obtained restricted copy MAY place files at:
  * `03_web_app/data/_restricted/` (gitignored)
  * `02_raw_sources/_restricted/` (gitignored)
  * `01_library/_restricted/` (gitignored)
* The public build NEVER references any path under `_restricted/`.
* `isRestrictedLocalModeEnabled()` returns `false` by default.
* If a future local build flips this to `true` AND a restricted file exists, local routes may activate. If the file is absent, routes must fail closed (no broken-link, no error to public users).
* The public Pages deploy MUST always run with `isRestrictedLocalModeEnabled() === false`.

### 2.4 Future activation rule
A source moves from `copyrighted-unavailable` or
`public-domain-deferred` to `public-domain-active` **only** when:
* Its `expectedPublicDomainYear` has arrived (per US 95-year term), AND
* The user verifies the actual rights state (no copyright restoration or extension has occurred), AND
* A fresh ingestion pass (`v_TRIGGER_YYYY_*.py`) is executed.

The expected-PD-year is necessary but not sufficient. Final
verification is a human decision.

## 3. Metadata register implementation

### 3.1 In-app `RESTRICTED_SOURCES` constant

Added to `index.html` after the canon helpers. 8 entries:

| id | Year | Expected PD year | Expected gain |
|---|---:|---:|---:|
| `adyar-saiva-upanishads-1935` | 1935 | **2031** | +13 |
| `adyar-yoga-upanishads-1938` | 1938 | **2034** | +7 |
| `adyar-samanya-vedanta-upanishads-1941` | 1941 | **2037** | +11 |
| `adyar-vaishnava-upanishads-1945` | 1945 | **2041** | +11 |
| `adyar-shakta-upanishads-1950` | 1950 | **2046** | +9 |
| `adyar-samnyasa-upanishads-1978` | 1978 | **2074** | +13 |
| `bedekar-palsule-sixty-upanishads-1980` | 1980 | 2076 | wide |
| `marabathina-108-upanishads-2024` | 2024 | 2120 | all 108 |

Each entry carries:
* `id`, `displayTitle`, `sourceFamily`, `tradition`, `category`
* `availabilityStatus` (status flag)
* `translator`, `editor`, `publicationYear`
* `expectedPublicDomainYear`
* `rightsHolder`, `copyrightOwnerConfidence` (`known` / `likely` / `unknown`)
* `expectedCoverageGain` (numeric for closed entries; verbal for wide-coverage)
* `coveredUpanishads` (count)
* `publicRouteAllowed: false` (uniform; enforced by `_restrictedSourceTileHTML` which produces a non-clickable card)

### 3.2 Companion JSON file

`03_web_app/data/restricted_sources_register.json` — same data but in standalone JSON for tooling. Includes per-source `coveredUpanishads[]` array with Muktikā number + Veda + class for each covered text. Self-documenting `_doc` field explains the file's metadata-only nature.

### 3.3 Rights-holder handling

Per the v121 spec ("if unknown, write 'Unknown / requires rights verification.' Do not guess confidently"):

* **Adyar 1935-1978**: `"Adyar Library and Research Centre, Chennai (likely; requires verification)"` — confidence `likely` because the Adyar volumes are co-published under Adyar's institutional name but individual translator estates may also have residual rights. Verification before any 2031+ ingestion is part of the trigger protocol.
* **Bedekar & Palsule 1980**: `"Motilal Banarsidass, Delhi"` — confidence `known` because the standard MB English edition carries that publisher's copyright.
* **Marabathina 2024**: `"Author / publisher (Marabathina, 2024)"` — confidence `known`.

## 4. Placeholder UI

### 4.1 Where placeholders appear

In the **By text view** of any family page whose `tradition` matches a restricted source's `tradition`. For Upanishads (the only family currently with restricted sources), they appear at the **bottom** of the By text view in a new section labelled **"Restricted / Future Public-Domain Sources"**, after the existing role-grouped collections.

### 4.2 Visual distinction

| Feature | Normal text tile | Restricted source placeholder |
|---|---|---|
| Border | solid 1px medium | **1px dashed light-brown** |
| Background | solid cream | **muted translucent cream (30% opacity)** |
| Hover effect | shadow lift + brightening | **no lift, slight background brighten only** |
| Status badge | none / role label | **bold "Copyrighted — unavailable" or "Public-domain deferred" pill** |
| Click action | opens reading room | **none — `cursor: default` and no onclick handler** |
| Title size | 15px medium-weight | 15px medium-weight (matches), but in muted color |
| Reader expectation | clickable text card | informational only |

### 4.3 What readers see on each placeholder

* Status pill (e.g., "Public-domain deferred")
* "Expected public-domain entry: 2031" (or whatever year)
* Title (e.g., "Saiva Upanishads (Adyar Library)")
* Meta line (e.g., "T. R. Srinivasa Ayyangar · ed. G. Srinivasa Murti · 1935")
* Coverage line (e.g., "When activated: 13 of the missing Muktikā 108 closed (13 Upanishads)")
* Rights line (e.g., "Rights holder: Adyar Library and Research Centre, Chennai (likely)")

### 4.4 What readers cannot do
* Click → no action (no `onclick`)
* No reading-room route exists
* No download link rendered
* No excerpt or sample text shown

## 5. Adyar source roadmap (with explicit per-volume metadata)

### Adyar Saiva 1935 — earliest PD-entry, single largest gain
* **Year**: 1935
* **Expected PD**: 2031-01-01
* **Translator**: T. R. Srinivasa Ayyangar
* **Editor**: G. Srinivasa Murti
* **Rights holder**: Adyar Library and Research Centre, Chennai (likely)
* **Covered (13)**: Akṣamālā, Kālāgnirudra, Rudra-hṛdaya, Pañcabrahma, Rudrākṣa, Jābāli, Atharvaśiras, Atharvaśikhā, Bṛhad-Jābāla, Śarabha, Pāśupata-brahma, Bhasma-Jābāla, Gaṇapati
* **Expected gain**: **+13**

### Adyar Yoga 1938
* **Year**: 1938 — **Expected PD: 2034**
* **Translator**: T. R. Srinivasa Ayyangar
* **Covered (7)**: Trīśikhi-brāhmaṇa, Kṣurikā, Brahmavidyā, Yogaśikhā, Kara, Yoga-cūḍāmaṇi, Darśana
* **Expected gain**: **+7**

### Adyar Sāmānya Vedānta 1941
* **Year**: 1941 — **Expected PD: 2037**
* **Translator**: T. R. Srinivasa Ayyangar
* **Covered (11)**: Mudgala, Mantrikā, Śukarahasya, Ekākṣara, Akṣi, Prāṇāgnihotra, Sāvitrī, Sūrya, Ātmā, Parabrahma, Mahāvākya
* **Expected gain**: **+11**

### Adyar Vaishnava 1945
* **Year**: 1945 — **Expected PD: 2041**
* **Translator**: T. R. Srinivasa Ayyangar (likely; requires verification)
* **Covered (11)**: Vāsudeva, Avyakta, Nṛsiṃha-tāpanī, Mahā-Nārāyaṇa, Rāma-rahasya, Rāma-tāpanī, Gopāla-tāpanī, Kṛṣṇa, Hayagrīva, Dattātreya, Garuḍa
* **Expected gain**: **+11**

### Adyar Shakta 1950
* **Year**: 1950 — **Expected PD: 2046**
* **Translator**: A. G. Krishna Warrier
* **Covered (9)**: Tripurā, Saubhāgya, Bahvṛca, Sarasvatī-rahasya, Sītā, Annapūrṇā, Tripura-tāpinī, Devī, Bhāvanā
* **Expected gain**: **+9**

### Adyar Samnyāsa 1978 — longest horizon
* **Year**: 1978 — **Expected PD: 2074**
* **Translator**: A. A. Ramanathan
* **Covered (13)**: Nirvāṇa, Jābāla, Paramahaṃsa, Advaya-tāraka, Turīyātīta, Yājñavalkya, Sātyāyanī, Avadhūta, Āruṇi, Mahat-Sannyāsa, Kuṇḍikā, Jābāla (Sāmaveda), Paramahaṃsa-parivrājaka
* **Expected gain**: **+13**

**Cumulative**: All six triggers eventually fire → 64 closed → 108 / 108 active. Long-horizon completion plan.

## 6. Local-only architecture

### 6.1 Folder structure (gitignored)

* `03_web_app/data/_restricted/` — restricted JSON data files (parsed locally from restricted source OCR)
* `02_raw_sources/_restricted/` — raw OCR/PDF/scans (already exists per v109 protocol)
* `01_library/_restricted/` — personal copies (already exists per v109 protocol)

### 6.2 `.gitignore` rules

Already covered by v109's `03_web_app/.gitignore` entry `data/_restricted/` and the Digital-Archive root `.gitignore` covering the outer folders. v121 makes no `.gitignore` changes — the v109 protocol is sufficient.

### 6.3 Local mode disabled by default

```js
// v121 — Local restricted-source mode is OFF by default. The public
// build NEVER references restricted text.
function isRestrictedLocalModeEnabled() { return false; }
```

A future local build can override this (e.g., in a separate
`local-config.js` that's gitignored) to enable local routes. The
public Pages deploy must always run with the default `false`.

### 6.4 Future local build plan

(Sketched — not implemented in v121):

1. User obtains a lawfully-acquired restricted file (e.g., personal copy of Adyar Saiva).
2. User places OCR at `02_raw_sources/_restricted/Adyar-Saiva-1935.txt`.
3. User runs a local-only parser (e.g., `05_scripts/ingest_adyar_saiva_local.py`) that outputs to `03_web_app/data/_restricted/upanishads-saiva-adyar_ayyangar.json`.
4. User flips `isRestrictedLocalModeEnabled` to `true` in a gitignored `local-config.js`.
5. The local app build loads the restricted file and routes the 13 Shaiva Upanishads.
6. **The public Pages deploy never sees any of this.**

## 7. Copyright safety verification

Before commit, verified:

| Check | Result |
|---|---|
| No restricted full text in `index.html` | ✓ — only metadata in `RESTRICTED_SOURCES` |
| No restricted full text in `data/restricted_sources_register.json` | ✓ — only metadata + Upanishad coverage lists |
| No OCR / PDF / scans from copyrighted sources staged | ✓ — no new raw-source files committed |
| No data JSON generated from restricted sources staged | ✓ — no new `data/upanishads-*.json` files (only the register) |
| No public routes to restricted full text | ✓ — `_restrictedSourceTileHTML()` renders no `onclick` and no `href` to any text route |
| Placeholders distinct from normal texts | ✓ — dashed border, muted bg, status pill, no hover lift |
| `RESTRICTED_SOURCES` all have `publicRouteAllowed: false` | ✓ |
| Each restricted entry has `expectedPublicDomainYear` | ✓ |
| Each entry has `rightsHolder` (with confidence) | ✓ |
| Restricted entry without confident rights-holder ID is marked accordingly | ✓ — "(likely; requires verification)" suffix used consistently |

## 8. v122 recommendation

Three viable v122 directions:

### v122 (recommended): Implement metadata-only detail page
* On click of a restricted-source placeholder, open a metadata-only
  modal/page showing the full per-Upanishad coverage list (currently
  in the JSON register but not surfaced in the placeholder card).
* Reader sees: full coverage table, complete rights analysis, PD-year
  reasoning, future-trigger script reference.
* Still NO text — all metadata.
* Small UI addition (~30 lines).

### v122-alt: Build the 2031 Adyar Saiva trigger script (metadata-only)
* Write `05_scripts/v_TRIGGER_2031_adyar_saiva.py` as a metadata-only
  research file: documents the IA-search strategy for finding the
  exact Ayyangar 1935 *Saiva-Upanishads* identifier, the parser
  approach (mirrors v117/v118 Sastri), and the byUpanishad-route
  template ready to run on 2031-01-01.
* No source download. No restricted text committed. Pure pipeline
  preparation.

### v122-deferred: Local restricted-loader implementation
* Implement the `data/_restricted/` loader path so that a user can
  drop in a lawfully-obtained restricted file and the local app
  routes it.
* Requires user-supplied test data (lawful local copies).
* Not implementable without user direction on specific files.

## 9. Non-destructive guarantees

* **No JSON files merged, rewritten, or deleted.**
* **No source files added or modified** (other than `restricted_sources_register.json` which contains zero copyrighted text).
* **No `MUKTIKA_108` changes.** Canon array unchanged from v116.
* **No `byUpanishad` entries added or removed.**
* **No catalog entries changed.**
* **No restricted text committed.**
* **No public routes to restricted text.**
* **No UI redesign of existing surfaces.** A new restricted-source section is added to the By-text view only; existing By Veda / Traditional order views are unchanged. The new section's CSS is additive (new selectors, no overrides of existing styles).
* **No folio / Atlas-Object work.**
* **No external acquisition.** v121 is architecture-only.

## 10. Build marker

`v120-missing-64-acquisition-strategy` → **`v121-restricted-upanishad-placeholders`**

The marker reflects the architectural contribution: a metadata-only
restricted-source register is now first-class in the app and
rendered as distinct placeholder cards in the By-text view of the
Upanishads family page. Public count, canon, and routes are all
unchanged. The doctrine and local-mode stub are in place for any
future v122+ work.
