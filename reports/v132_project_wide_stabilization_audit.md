# v132 — Project-wide stabilization audit

A documentation/architecture/maintenance pass. **No features added, no
sources ingested, no UI redesigned, no `MUKTIKA_108` or public-count
change, no restricted text touched.** This report maps the whole
Digital Archive / Atlas / Workspace ecosystem so it can be paused and
maintained with confidence.

The constitutional source of truth is
`C:\Users\steve\Documents\Claude Workspace\ARCHITECTURE.md`. Where this
report and that document differ, ARCHITECTURE.md wins until amended; the
discrepancies found here are listed in §11.

## 1. Summary

* **Three institutional layers:** Workspace (the foyer), Atlas (the
  operating system), Digital-Archive (the canonical corpus). Glyphs is a
  self-contained world that Workspace links to.
* **Five GitHub repos** (ARCHITECTURE.md names four — the fifth,
  `Daily-Reader`, is undocumented there; see §11).
* **One local-only repo** (`class notes`, no remote).
* Digital-Archive Reading Room is at build **`v131-upanishads-wrapup`**
  (this report bumps it to `v132-project-wide-stabilization`); the
  Upanishads section is stable and paused. Public Muktikā count **44 /
  108**.
* Main risk: `Digital-Archive/03_web_app` carries **~260 uncommitted
  working-tree entries** (mostly `reports/*.png` diagnostics + `diag_*.py`
  scratch). This is the long-standing drift (ARCHITECTURE.md §11 Q4) and
  is the top cleanup candidate, but is **not** touched in this pass.

## 2. Project map

Root: `C:\Users\steve\Documents\Claude Workspace\`

| Path | Layer / purpose | Git repo? | Public/deployed? | Holds |
|---|---|---|---|---|
| `workspace-hub/` | **Workspace** — public navigation foyer | ✅ `Workspace` | ✅ Pages | source (HTML/CSS/JS world pages) |
| `Atlas/` | **Atlas** — engine, governance, registry | engine = local-only | partial | code, docs, registry, experiments |
| `Atlas/_published/atlas_site/` | Atlas published static site | ✅ `Atlas` | ✅ Pages | generated/curated static site |
| `Digital-Archive/` | **Digital-Archive** — corpus (parent) | ❌ (parent) | no | raw sources, scripts, library |
| `Digital-Archive/03_web_app/` | Reading Room (the repo working tree) | ✅ `Digital-Archive` | ✅ Pages | app (`index.html`), public data, reports |
| `Digital-Archive/04_landing/_deploy/` | Daily-Reader landing/service | ✅ `Daily-Reader` | ✅ (Procfile app) | server app (Flask/Procfile) |
| `glyphs/` | **Glyphs** — one self-contained world | ✅ `Glyphs` | ✅ Pages | static world site |
| `projects/culture/class notes/` | Class notes | ✅ (no remote) | ❌ local-only | notes |
| `projects/` | Local laboratory subprojects | mixed | no | scratch / source-of-truth experiments |
| `_archive/`, `_snapshots/`, `_developer/` | Local-only by underscore convention | n/a | no | archives, backups, dev aids |
| `tools/`, `Launcher/` | Workspace-level utilities + launcher | n/a | no | scripts, launcher |

Inside `Digital-Archive/` (parent, not a repo):

| Subfolder | Purpose | Tier |
|---|---|---|
| `01_library/` | Curated library texts (canonical) | local-only canonical |
| `02_raw_sources/` | Raw OCR/source files (~940 MB, hashed) | local-only canonical |
| `03_web_app/` | The Reading Room repo (public) | **public** |
| `04_landing/` | Daily-Reader app + landing | mixed |
| `05_scripts/` | Ingestion/validation/maintenance tooling | local-only |
| `06_workspace/` | Scratch/working area | local-only ephemeral |

## 3. Repositories & deployments

| Repo | Local working tree | Pages / deploy URL | Purpose | Edit directly? |
|---|---|---|---|---|
| `stevenfrye30/Workspace` | `workspace-hub/` | `stevenfrye30.github.io/Workspace/` | Public dashboard + world pages | Yes — public navigation only |
| `stevenfrye30/Atlas` | `Atlas/_published/atlas_site/` | `stevenfrye30.github.io/Atlas/` | Atlas docs/visualizer site | Cautiously — prefer regenerating |
| `stevenfrye30/Digital-Archive` | `Digital-Archive/03_web_app/` | `stevenfrye30.github.io/Digital-Archive/` | Reading Room corpus app | Yes — but see do-not-touch list |
| `stevenfrye30/Glyphs` | `glyphs/` | `stevenfrye30.github.io/Glyphs/` | Writing-systems world | Yes |
| `stevenfrye30/Daily-Reader` | `Digital-Archive/04_landing/_deploy/` | server app (Procfile) | Daily reading email/print service | Cautiously — it's a running service |
| *(local-only)* `class notes` | `projects/culture/class notes/` | none | Class notes | Local only; no remote |

* **Deploy method (all Pages repos):** push to `main` → GitHub Pages
  serves the repo root. No build step beyond what Pages runs. The change
  is live only after `git commit && git push`.
* **Deploy method (Daily-Reader):** `Procfile` + `requirements.txt`
  indicate a hosted Python (Flask) service; treat as a live service, not
  a static site.
* **Build markers:** only Digital-Archive's `index.html` carries a
  `<meta name="atlas-build">` marker (`vNNN-...`). The others have no
  equivalent versioned marker.

## 4. Digital-Archive audit

* **Public URL:** `https://stevenfrye30.github.io/Digital-Archive/`
* **Local path:** `Digital-Archive/03_web_app/` (repo); parent
  `Digital-Archive/` holds raw sources + scripts.
* **Repo:** `stevenfrye30/Digital-Archive`, branch `main`.
* **Build marker:** `v131-upanishads-wrapup` → **`v132-project-wide-stabilization`** (this report).
* **Major sections/traditions:** a large multi-tradition corpus
  (Christian, Hindu, Buddhist, Jewish, classical, esoteric, etc.) — 1000+
  texts, 26+ Bible translations. Surfaced through the Reading Room
  (`index.html`) as text families and per-text readers.
* **Stable areas:** the Upanishads family (108 Map + local-restricted
  pipeline, v121–v131); Christian-texts cleanup + integrity dashboard;
  the multi-translation reader, footnotes, source summaries, integrity
  proof (`integrity.html`).
* **Unfinished / deferred:** Upanishads heading-pattern splitter
  (deferred); actual local ingestion of restricted copies (needs lawful
  copies, local-only); ~169 "missing source.url" metadata warnings; the
  ~260-entry working-tree drift triage.
* **Upanishads status (from v131):** 44/108 active · 64 future · 0 needed.
  All six Adyar families config-ready (Saiva +13, Yoga +7, Sāmānya
  Vedānta +11, Vaishnava +11, Shakta +9, Samnyāsa +13). PD trigger years
  2031/2034/2037/2041/2046/2074. Paused.
* **Restricted/local architecture:** v124 fail-closed loader
  (`github.io` hard-blocked; localhost + opt-in only), v125 parser
  harness, v126 validator, v127 local-availability chips, v128–v130
  Adyar configs + generator. All tooling lives in
  `05_scripts/local_only/` (outside the repo). Nothing restricted is ever
  committed; `data/_restricted/` is gitignored.
* **Data loading model (high level):** public text data ships as
  gzipped JSON under `03_web_app/data/*.json.gz`; the app fetches and
  inflates with `DecompressionStream('gzip')`. `MUKTIKA_108` and
  `RESTRICTED_SOURCES` are inlined JS arrays in `index.html`. Restricted
  local data, when present, loads only from gitignored
  `data/_restricted/` in local mode.
* **Important scripts (`05_scripts/`):** `check_no_restricted_text.py`
  (safety gate), `build_search_index.py`, `gzip_web_data.py`,
  `export_reader_data.py`, `passage_subsequence_proof.py` +
  `build_integrity_report.py` (integrity), and `local_only/`
  (`ingest_restricted_source.py`, `validate_local_restricted.py`,
  `generate_adyar_configs.py`, `configs/`).
* **Important reports:** `reports/v109..v131_*.md` (restricted-source
  protocol → Upanishads wrap-up), plus architecture/cleanup reports.
* **How to run locally:**
  ```
  cd "C:\Users\steve\Documents\Claude Workspace\Digital-Archive\03_web_app"
  python -m http.server 8765
  ```
  then open `http://localhost:8765/`.
* **How to publish:** from `03_web_app/`, `git add <files>` →
  `git commit` → `git push origin main`. Pages serves the repo root.
* **Known risks:** the ~260-entry uncommitted drift (commit-by-accident
  risk — always stage explicit files, never `git add -A`); large gzipped
  data; the inlined-array coupling in `index.html` (edits to
  `MUKTIKA_108` must be deliberate).

## 5. Atlas audit

* **Purpose:** the institutional operating system — governance docs,
  schemas, the registry that drives Workspace publication
  (`Atlas/atlas_registry.json`), sync tooling (`Atlas/sync_atlas.py`),
  and engine code (`core/`, `pipeline/`, `query/`). Not the publication
  surface.
* **Local path:** `Atlas/` (engine + governance, local-only) with the
  published static site at `Atlas/_published/atlas_site/`.
* **Repo:** `stevenfrye30/Atlas` (the `_published/atlas_site/` tree).
  Pages: `https://stevenfrye30.github.io/Atlas/`.
* **Relation to Digital-Archive:** one-way, explicit, scripted flows
  only (registry → Workspace; curation → the archive shelf; engine
  exports → world pages). No live import between layers.
* **Stable:** the governance docs, the two-folder split (engine local /
  `_published` repo), the registry + `sync_atlas.py` (moved into `Atlas/`
  2026-05-09).
* **Unfinished / deferred:** whether the local engine code becomes part
  of the published repo, stays local, or is promoted to a separate
  `atlas-engine/` top-level (ARCHITECTURE.md §11 Q1).
* **How Atlas should connect to the archive (eventually):** only through
  named, scripted, reversible one-way flows (registry/sync + curated
  exports) — never a live cross-repo import. A change touching more than
  one repo is a signal the boundary is wrong.
* **This pass:** documentation only; Atlas was not modified.

## 6. Workspace audit

* **Purpose:** the public foyer — the dashboard/launcher grid and curated
  world surfaces (Pantheons, Sound Map, Phonos, Cosmos, the archive
  shelf), with stable links into Atlas, Digital-Archive, and Glyphs.
* **Local path:** `workspace-hub/`. Repo `stevenfrye30/Workspace`,
  Pages `https://stevenfrye30.github.io/Workspace/`.
* **Relation to the others:** the entrance; it links out to the corpus
  (Digital-Archive) and is fed by Atlas's registry/exports. It holds
  independent copies of many `projects/` subprojects (not symlinks).
* **Workspace should be responsible for:** public navigation, world
  pages, dashboards, lightweight reading/exploration.
* **Workspace should NOT be responsible for:** raw corpus data, parser
  or extraction infrastructure, build tooling beyond Pages, unstable
  experimental code, internal/scratch artifacts.
* **This pass:** documentation only; Workspace was not modified (the 3
  uncommitted entries there pre-date this pass).

## 7. Scripts / tooling status

* **Digital-Archive `05_scripts/`** — corpus ingestion, cleanup,
  integrity proofs, search index, gzip, export; plus `local_only/`
  restricted tooling. `check_no_restricted_text.py` is the commit-time
  safety gate.
* **Atlas** — `atlas.py`, `run.py`, `sync_atlas.py`, `core/pipeline/
  query/`, `tools/`. Engine + sync; local-only.
* **Workspace** — minimal build tooling (Pages serves static files);
  receives synced registry/exports.

## 8. Local vs public architecture

* **Public (ships to Pages):** Workspace, the Reading Room
  (`03_web_app/`), Glyphs, Atlas docs/visualizer site. Public data is
  gzipped JSON + inlined arrays; **no restricted text ever ships**.
* **Local-only canonical:** raw sources (`02_raw_sources/`), curated
  library (`01_library/`), Atlas engine + governance drafts, the
  `local_only/` restricted tooling + configs.
* **Local-only ephemeral:** generated indices, caches, diagnostics
  (`reports/diag_*.py`, screenshots), `data/_restricted/` runtime files.
* **Convention:** a leading underscore on a top-level folder = local-only
  (`_archive/`, `_snapshots/`, `_developer/`, `_experiments/`, …).

## 9. Restricted-source safety rules

* Never commit: anything under `data/_restricted/`, any `*.local.json`,
  `restricted_index.local.json`, real local configs
  (`local_restricted_config.json` / `restricted_local_config.json`),
  `*.restricted.json`, or copyrighted OCR/PDF/scans/full text.
* `data/_restricted/` and the patterns above are gitignored; metadata-only
  templates, the register, and `*.config.json` are allowed.
* Always run `python 05_scripts/check_no_restricted_text.py` (must print
  **PASS**) before committing in Digital-Archive.
* Use fake fixtures for tests and delete them before commit.
* Local restricted mode is hard-blocked on `github.io`; it needs
  localhost + explicit opt-in (`?localRestricted=1`).

## 10. Maintenance map (for Steven)

**Common tasks → where to change:**

| Task | Where | Then |
|---|---|---|
| Public navigation / a world page | `workspace-hub/` | commit + push Workspace |
| Reading Room behavior | `Digital-Archive/03_web_app/index.html` | safety check, commit + push |
| Add/curate corpus text | `Digital-Archive/01_library/` + scripts | regenerate data, gzip, export |
| Atlas governance/registry | `Atlas/` | `sync_atlas.py` to push to hub |
| A writing-systems change | `glyphs/` | commit + push Glyphs |

**Before committing (Digital-Archive):**
```
cd "C:\Users\steve\Documents\Claude Workspace\Digital-Archive\03_web_app"
git status
git diff
python ..\05_scripts\check_no_restricted_text.py     # must say PASS
git add index.html reports\<your-report>.md          # explicit files only
git commit -m "vNNN — <summary>"
git push origin main
```

**Run the Reading Room locally:**
```
cd "C:\Users\steve\Documents\Claude Workspace\Digital-Archive\03_web_app"
python -m http.server 8765
# open http://localhost:8765/
```

**Recover if something breaks:**
* Unstaged mistake: `git checkout -- <file>` (discards working change).
* Staged mistake: `git restore --staged <file>`.
* Bad commit not pushed: `git reset --soft HEAD~1` (keeps changes).
* Already pushed: make a new corrective commit (do **not** force-push
  shared `main`).
* Verify the live site after pushing (Pages can take a minute).

**Avoid committing restricted/private material:**
* Stage explicit files (`git add index.html reports/...`), never
  `git add -A` / `git add .`.
* Run `check_no_restricted_text.py` first.
* Confirm `git status` shows no `data/_restricted/` or `*.local.json`.

## 11. Do-not-touch-casually list

* `MUKTIKA_108` (inlined canon in `03_web_app/index.html`) and the public
  count (44/108).
* `data/restricted_sources_register.json` (the metadata register).
* `data/_restricted/` and any generated `*.local.json`.
* Public data JSON (`data/*.json.gz`) — regenerate via scripts, don't
  hand-edit.
* Build/deployment settings and GitHub Pages config for every repo.
* Parser/ingestion scripts lacking tests (change behind a fixture).
* Any generated Atlas output and the Atlas published site (prefer
  regenerating over hand-editing).
* Any local-only restricted files (`05_scripts/local_only/` real data).
* **Never `git add -A`** in `03_web_app/` (the ~260-entry drift makes
  accidental mass-commits easy).

## 12. Discrepancies & open issues (found this pass)

* **R1 — fifth repo undocumented.** `stevenfrye30/Daily-Reader`
  (`Digital-Archive/04_landing/_deploy/`) is a live Procfile service not
  named in ARCHITECTURE.md (which says "four GitHub repositories"). It
  should be added to the architecture doc, or its status clarified.
* **R2 — `03_web_app` drift.** ~260 uncommitted entries (mostly
  `reports/*.png` + `diag_*.py`). ARCHITECTURE.md §11 Q4. Needs triage:
  gitignore the diagnostics, or archive them.
* **R3 — `START_HERE.md` vs `README.md`.** Both exist at root (also a new
  `STRUCTURE.md`). ARCHITECTURE.md §7.1/§11 Q5 says pick one.
* **R4 — `class notes`** local-only repo with no remote (§11 Q3):
  publish, archive, or keep local — undecided.
* **R5 — Atlas engine occupancy** (§11 Q1): local engine vs published
  repo split unresolved.

None of these were changed in this pass — they are recorded for a future
consolidation phase.

## 13. Deferred work

* Upanishads heading-pattern splitter; local ingestion of lawful copies;
  local-restricted progress dashboard; PD-trigger checklist.
* `03_web_app` drift triage; the five open governance questions
  (ARCHITECTURE.md §11); Daily-Reader documentation.

## 14. Recommended next phase

**A Steven developer handbook + learning roadmap (v133).** With the map
in place, the next step is a hands-on handbook: how each repo works, the
exact edit→verify→commit→push loop per surface, how to read the Reading
Room code, how to run the scripts safely, and a staged learning path
(start with a tiny Workspace edit → a Reading Room report → a script run)
so Steven can begin maintaining the ecosystem independently. Pair it with
resolving R1–R5 as a short consolidation checklist.

## Audit confirmations

* Changed in this pass: **documentation only** — this report + the
  Digital-Archive build-marker bump. No app behavior, no `MUKTIKA_108`,
  no public count, no restricted material.
* Public Muktikā count: **44 / 108** (unchanged).
* `check_no_restricted_text.py`: **PASS**; no `data/_restricted`,
  `*.local.json`, or copyrighted text committed.
