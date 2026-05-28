# v128 — Adyar Saiva 1935 local parser config

v124–v127 built the local-only restricted pipeline (loader → parser
harness → validator → 108-Map availability indicator). v128 makes one
specific source family — the **Saiva Upanishads (Adyar Library, 1935)** —
ready for safe, repeatable, source-aware local ingestion via a
metadata-only config and config-driven tooling.

This is a metadata/config/tooling pass. **No source was acquired, no
copyrighted text was downloaded or committed, no generated `.local.json`
was committed, public data and `MUKTIKA_108` are untouched, and the
public count stays 44 / 108.**

## 1. Summary

| Field | Before v128 | After v128 |
|---|---|---|
| Build marker | `v127-local-restricted-availability` | **`v128-adyar-saiva-local-config`** |
| Source config | none | **`05_scripts/local_only/configs/adyar_saiva_1935.config.json`** |
| Parser harness | v125 (CLI only) | **+ `--config` (CLI overrides; config dry-run)** |
| Validator | v126 | **+ `--config` coverage cross-check** |
| README | v125/v126 | **+ config-driven + Adyar Saiva workflow** |
| Public active count | 44 / 108 | 44 / 108 (unchanged) |
| `MUKTIKA_108` / public data | untouched | untouched |
| Restricted text / `data/_restricted` / `*.local.json` committed | none | **none** ✓ |

### Repo-boundary note
`05_scripts/` is **not** a git repository — only `03_web_app/` is. So
(as with the v124 loader docs, the v125 harness, and the v126 validator)
the config, the harness/validator changes, and the README all live in
`05_scripts/local_only/` as canonical **local-only tooling** and are not
part of the public `03_web_app` commit. The committed v128 artifacts in
`03_web_app/` are the build-marker bump and this report.

## 2. Adyar Saiva coverage

Confirmed from `RESTRICTED_SOURCES` + `MUKTIKA_108` in
`03_web_app/index.html` (not from a hand-typed list):

| Field | Value |
|---|---|
| id | `adyar-saiva-upanishads-1935` |
| displayTitle | Saiva Upanishads (Adyar Library) |
| translator / editor | T. R. Srinivasa Ayyangar (tr.); ed. G. Srinivasa Murti *(verify against physical copy)* |
| publication year | 1935 |
| expected public-domain year | 2031 |
| rights holder | Adyar Library and Research Centre, Chennai (likely) |
| rights confidence | likely |
| availability status | public-domain-deferred |
| register source family | Adyar Library English Series |
| class | Shaiva |
| expected coverage gain | 13 |

**Covered Muktikā entries (all Shaiva):**

| # | Upanishad | Veda | Archive status |
|---|---|---|---|
| 7 | Akṣamālā | Rigveda | future-public-domain |
| 39 | Kālāgnirudra | Krishna Yajurveda | future-public-domain |
| 55 | Rudra-hṛdaya | Krishna Yajurveda | future-public-domain |
| 57 | Pañcabrahma | Krishna Yajurveda | future-public-domain |
| 74 | Rudrākṣa | Samaveda | future-public-domain |
| 77 | Jābāli | Samaveda | future-public-domain |
| 81 | Atharvaśiras | Atharvaveda | future-public-domain |
| 82 | Atharvaśikhā | Atharvaveda | future-public-domain |
| 83 | Bṛhad-Jābāla | Atharvaveda | future-public-domain |
| 87 | Śarabha | Atharvaveda | future-public-domain |
| 96 | Pāśupata-brahma | Atharvaveda | future-public-domain |
| 101 | Bhasma-Jābāla | Atharvaveda | future-public-domain |
| 102 | Gaṇapati | Atharvaveda | future-public-domain |

* **Public active vs local/future:** all 13 are currently
  `future-public-domain` — **none** is publicly active. So the public
  count is unaffected (`44 active · 64 future · 0 needed · 108 total`).
* **Expected local availability gain:** up to **13** local restricted
  chips once a lawful local copy is ingested (future pending would drop
  64 → 51 locally; public stays 44).
* **Dakṣiṇāmūrti** is already active and is **not** part of this
  source's public-closure coverage (correctly excluded). The Adyar
  volume may contain it as a duplicate witness, but it would not change
  the public count.
* **Expected PD year:** 2031 (US copyright term on a 1935 publication).

## 3. Config file

* **Path:** `05_scripts/local_only/configs/adyar_saiva_1935.config.json`
* **Contents:** metadata only — `configVersion`, `sourceId`,
  `displayTitle`, `sourceFamily`, `tradition`, `category`, `classType`,
  `translatorOrEditor`, `publicationYear`, `expectedPublicDomainYear`,
  `rightsHolder`, `rightsHolderConfidence`, `availabilityStatus`,
  `localOnly`, route flags, `expectedCoverageGain`, `defaultInputPath`,
  `defaultOutputPath`, `defaultIndexPath`, `recommendedSplitMode`
  (`upanishad-heading`), `coveredUpanishads[]` (13 entries with
  `muktikaNumber`, provisional ASCII `key`, `displayTitle`, `veda`,
  `classType`, `currentArchiveStatus`, `headingPatterns`), and `notes`.
* **No text:** contains no passages and no copyrighted content.
* **How it is used:** passed via `--config` to the harness and the
  validator. The harness reads it for defaults; the validator
  cross-checks generated output against it. `key` slugs are provisional
  (MUKTIKA_108 assigns no archive key to these future entries yet);
  `headingPatterns` are forward-looking hints for source-aware splitting
  (the v125 splitter still uses a generic Upanishad-heading regex).

## 4. Parser harness changes (`ingest_restricted_source.py`)

* **`--config <file>`** — loads metadata defaults from the config.
* **CLI override** — any explicit CLI flag wins over the config value,
  which in turn wins over the built-in default.
* **Input** — `--input` is optional when the config provides
  `defaultInputPath`. Output still must be under `data/_restricted/` and
  end `.local.json`; public-data paths are still refused.
* **Config dry-run** — `--config --dry-run` needs **no** real input
  file. It prints source id, display title, expected input/output/index
  paths, split mode, covered count, and covered Muktikā numbers, and
  warns if the input is missing (acceptable for a config dry-run).
* **Missing input (real run)** — fails clearly:
  `Input file not found. Place a lawful local copy at …`.
* **No regression** — the full v125 CLI (no `--config`) works exactly as
  before; `coveredUpanishads` may come inline from config or from
  `--covered-upanishads-json`.

## 5. Validator changes (`validate_local_restricted.py`)

Added `--config <file>` cross-check (in addition to all v126 checks):

* Source **id** must match `config.sourceId` → **FAIL** on mismatch.
* **expectedPublicDomainYear** must match config → **FAIL** on mismatch,
  **WARN** if missing.
* **sourceFamily** must match config → **FAIL** on mismatch, **WARN** if
  missing.
* **Covered Muktikā numbers** (`coveredNumbers` or
  `coveredUpanishads[].muktikaNumber`) compared to config → **WARN** if
  missing or differing (lists the missing/extra numbers).
* With `--index`, the matching entry is cross-checked; if the config's
  `sourceId` is absent from the index it **WARN**s (expected pre-ingest).
* Needs **no** source file for the cross-check (works index-only); still
  never prints passage text. Public route flags checked as before.

## 6. README — one-step local workflow

`05_scripts/local_only/README.md` gained a **Config-driven runs (v128)**
section and an **Adyar Saiva 1935 local ingestion** section: place lawful
text → config dry-run → generate + update local index → validate with
`--config` → serve `03_web_app` → open `?localRestricted=1` → 108 Map,
plus the never-commit warnings.

## 7. Tests (fake fixtures only; all removed before commit)

| Test | Result |
|---|---|
| `--config --dry-run`, default input **missing** | PASS — prints config summary + "input missing" warning, no files written |
| `--config --input <fake fixture> --dry-run` | PASS — 4 passages / 3 sections previewed, no files written |
| CLI override (`--display-title` over config) | PASS — CLI value wins |
| v125 regression (no `--config`, full CLI, dry-run) | PASS — unchanged behaviour |
| No args | clear "missing required value(s)" error |
| Non-dry-run, input missing | clear "Input file not found…" error |
| Fake generation via config + `--update-local-index` | PASS — wrote under `data/_restricted/` (gitignored) |
| Validate source `--config --allow-placeholder` | PASS — coverage matches config (13) |
| Validate index `--check-files --config` | PASS — entry + referenced source cross-checked |
| Negative: matching source vs **wrong** config | FAIL on id / PD-year / family + coverage WARN (cross-check works) |
| v126 regression (validate without `--config`) | PASS |
| Fake generated files + index removed | done |

## 8. Safety verification

* `python 05_scripts/check_no_restricted_text.py` → **PASS** (scanned
  ~2005 tracked files in `03_web_app/`; only metadata templates,
  register, and reports tracked).
* No `data/_restricted/` tracked; no `*.local.json` committed; no
  restricted text committed.
* **Safety script review (Part 8):** no change needed. It scans only
  tracked files in `03_web_app/` (so `05_scripts/local_only/configs/` is
  inherently out of scope), and its rules already **allow** metadata
  `*.config.json` while **blocking** `*.local.json`,
  `restricted_index.local.json`, the real local configs
  (`local_restricted_config.json` / `restricted_local_config.json`),
  `*.restricted.json`, and anything under `_restricted/`.

## 9. How to use this locally (with a lawful copy)

```
# 1. place lawful OCR/text
03_web_app/data/_restricted/sources/adyar-saiva-upanishads-1935.txt

# 2. generate local JSON + update the gitignored local index
python 05_scripts/local_only/ingest_restricted_source.py \
  --config 05_scripts/local_only/configs/adyar_saiva_1935.config.json \
  --update-local-index

# 3. validate against the config
python 05_scripts/local_only/validate_local_restricted.py \
  --index 03_web_app/data/_restricted/restricted_index.local.json \
  --config 05_scripts/local_only/configs/adyar_saiva_1935.config.json \
  --check-files --strict --verbose

# 4. serve + open locally
cd 03_web_app && python -m http.server 8765
#   http://localhost:8765/?localRestricted=1
#   Religion → Hindu → The Upanishads → View the 108 Map
```

Public active stays 44; local restricted available rises by up to 13;
future pending drops accordingly; `github.io` stays metadata-only.
Always run the safety script before any commit.

## 10. v129 recommendation

Next best step: **add the Adyar Yoga 1938 config**
(`adyar_yoga_1938.config.json`, covers Muktikā #19, 40, 45, 50, 54, 68,
76 — 7 Yoga Upanishads, expected PD year 2034) using the exact v128
config shape, so a second Adyar family is ingestion-ready. Strong
follow-ups: a **local restricted source progress dashboard** (per-family
expected-gain vs ingested), source-aware splitting that consumes
`headingPatterns`, and a local-only route validator. The repeatable
config pattern established here should template the remaining Adyar
volumes (Sāmānya Vedānta 1941, Vaishnava 1945, Shakta 1950).
