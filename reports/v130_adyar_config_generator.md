# v130 — Adyar config generator

v128 and v129 hand-wrote local-ingestion configs for the Adyar Saiva
(1935, +13) and Adyar Yoga (1938, +7) families. v130 replaces hand-work
with a **metadata-only generator** that emits the remaining Adyar family
configs straight from the current public data, so every Adyar volume is
ingestion-ready and register-consistent.

This is a metadata/config/tooling pass. **No source was acquired, no
copyrighted text was downloaded or committed, no generated `.local.json`
was committed, public data (except the build marker) and `MUKTIKA_108`
are untouched, and the public count stays 44 / 108.**

## 1. Summary

| Field | Before v130 | After v130 |
|---|---|---|
| Build marker | `v129-adyar-yoga-local-config` | **`v130-adyar-config-generator`** |
| Config generator | none | **`05_scripts/local_only/generate_adyar_configs.py`** |
| Adyar configs | 2 (Saiva, Yoga) | **6** (+ Sāmānya Vedānta, Vaishnava, Shakta, Samnyāsa) |
| Parser / validator | v128/v129 | unchanged (reused) |
| README | v129 | **+ Generate Adyar family configs** |
| Public active count | 44 / 108 | 44 / 108 (unchanged) |
| `MUKTIKA_108` / public data | untouched | untouched |
| Restricted text / `data/_restricted` / `*.local.json` committed | none | **none** ✓ |

### Repo-boundary note
`05_scripts/` is **not** a git repository — only `03_web_app/` is. The
generator, the configs, and the README live in `05_scripts/local_only/`
as canonical local-only tooling and are not part of the public
`03_web_app` commit (same as v124–v129). The committed v130 artifacts in
`03_web_app/` are the build-marker bump and this report.

## 2. Generator

* **Path:** `05_scripts/local_only/generate_adyar_configs.py`
* **Reads:** `03_web_app/index.html` — parses `MUKTIKA_108`
  (n, key, name, veda, cls) and `RESTRICTED_SOURCES` (id, titles, years,
  rights, `coveredNumbers`) with a tolerant, single-quote-aware,
  line-anchored parser (so comments mentioning the array names are
  ignored). No browser or running server needed.
* **Active detection:** a `MUKTIKA_108` entry is publicly **active** iff
  its `key` is non-null. Verified against the live 108 Map: exactly 44
  entries are keyed and exactly 44 are active (no key-but-inactive, no
  active-but-keyless).
* **Writes:** metadata-only configs under `05_scripts/local_only/configs/`
  in the exact v128/v129 shape. Never writes under `data/_restricted/`
  and contains no copyrighted text.
* **CLI:** `--all`, `--source-id <id>`, `--dry-run`, `--overwrite`,
  `--out-dir <dir>`, `--include-existing`, `--report-json <path>`,
  `--index-html <path>`.
* **Dry-run:** prints the planned configs (covered count, numbers, gain,
  PD year) and writes nothing.
* **Overwrite:** by default `--all` only writes families whose config is
  **missing**, so the hand-written Saiva/Yoga configs are protected;
  regenerating them requires `--include-existing --overwrite`.

## 3. Generated configs

| Config path | Source id | Title | Pub | Exp. PD | Rights holder | Covered | Covered Muktikā numbers | Local gain |
|---|---|---|---|---|---|---|---|---|
| `configs/adyar_samanya_vedanta_1941.config.json` | `adyar-samanya-vedanta-upanishads-1941` | Sāmānya Vedānta Upanishads (Adyar Library) | 1941 | 2037 | Adyar Library and Research Centre, Chennai (likely) | 11 | 6, 17, 42, 51, 52, 58, 73, 94, 95, 97, 103 | +11 |
| `configs/adyar_vaishnava_1945.config.json` | `adyar-vaishnava-upanishads-1945` | Vaishnava Upanishads (Adyar Library) | 1945 | 2041 | Adyar Library and Research Centre, Chennai (likely) | 11 | 69, 71, 84, 88, 89, 90, 104, 105, 106, 107, 108 | +11 |
| `configs/adyar_shakta_1950.config.json` | `adyar-shakta-upanishads-1950` | Shakta Upanishads (Adyar Library) | 1950 | 2046 | Adyar Library and Research Centre, Chennai (likely) | 9 | 8, 9, 10, 61, 86, 93, 98, 99, 100 | +9 |
| `configs/adyar_samnyasa_1978.config.json` | `adyar-samnyasa-upanishads-1978` | Samnyāsa Upanishads (Adyar Library) | 1978 | 2074 | Adyar Library and Research Centre, Chennai (per copyright notice; requires verification) | 13 | 5, 13, 15, 21, 24, 27, 28, 53, 64, 70, 72, 75, 92 | +13 |

* All covered entries are currently `future-public-domain` (none
  publicly active), so the public count is unaffected. Total potential
  local gain across the 4 new families is **+44** (which, with Saiva +13
  and Yoga +7, accounts for all 64 future entries).
* File-name ↔ id mapping: `adyar_<family>_<year>.config.json` derived
  from `adyar-<family>-upanishads-<year>`.
* **Faithful to the register:** `availabilityStatus` is copied verbatim,
  so **Samnyāsa 1978 is `copyrighted-unavailable`** (a 1978 work, PD
  2074), while the other three are `public-domain-deferred`. The
  generator did **not** hardcode the example's `public-domain-deferred`.

## 4. Existing config regression

Saiva and Yoga configs were **not** rewritten. Dry-runs confirm no
regression:

* `adyar_saiva_1935.config.json` → 13 covered.
* `adyar_yoga_1938.config.json` → 7 covered.

The generator's output for Saiva/Yoga was compared against the
hand-written files (generated to a temp dir, not overwriting):

* **Load-bearing fields identical** for both — covered numbers,
  `sourceId`, `expectedPublicDomainYear`, `availabilityStatus`,
  `publicRouteAllowed`/`localRouteAllowed`, `expectedCoverageGain`,
  `recommendedSplitMode`, `classType`.
* **Cosmetic-only differences** (not errors, not rewritten): `Saiva`
  config `sourceFamily` is "Adyar Saiva" by hand vs "Adyar Shaiva"
  generated (register `classLabel` is "Shaiva"); `translatorOrEditor`
  wording differs; 4/13 Saiva provisional `key` slugs differ by
  hyphenation (`rudrahrdaya` vs `rudra-hrdaya`). Keys are provisional and
  not used by the loader (which matches on `muktikaNumber`).

## 5. Parser / validator tests

No code changes to the harness or validator — the v128 `--config`
support was reused unchanged:

| Test | Result |
|---|---|
| `generate_adyar_configs.py --all --dry-run` | PASS — 4 candidates planned, no writes |
| `generate_adyar_configs.py --all` | PASS — 4 configs written; Saiva/Yoga skipped (exist) |
| Re-run `--all --dry-run` after generation | candidates 0 (idempotent) |
| JSON parse + counts for all 4 | PASS — 11/11/9/13, numbers + PD years correct, all `future-public-domain` |
| `ingest … --config <each new> --dry-run` (no input) | PASS — config summary, correct covered counts, no writes |
| Fake fixture generation via `adyar_shakta_1950` config | PASS — wrote under `data/_restricted/` (gitignored) |
| `validate … --source --config --allow-placeholder` | PASS — coverage matches config (9) |
| `validate … --index --check-files --config` | PASS — entry + referenced source cross-checked (9) |
| Saiva / Yoga dry-run | PASS — 13 / 7, no regression |
| Fake generated files + index removed | done |

## 6. Safety verification

* `python 05_scripts/check_no_restricted_text.py` → **PASS** (scanned
  ~2007 tracked files in `03_web_app/`).
* No `data/_restricted/` tracked; no `*.local.json` committed; no
  restricted text committed.
* **Safety script review (Part 7):** no change needed. It scans only
  tracked files in `03_web_app/`, so the generator and the
  `05_scripts/local_only/configs/` files are out of scope; its rules
  already **allow** metadata `*.config.json` and the generator script
  while **blocking** `*.local.json`, `restricted_index.local.json`, the
  real local configs, `*.restricted.json`, and anything under
  `_restricted/`.

## 7. How to use this locally (with a lawful copy)

```
# 0. (one-time) generate the Adyar family configs from current public data
python 05_scripts/local_only/generate_adyar_configs.py --all

# 1. place lawful OCR/text at the config's defaultInputPath, e.g.
03_web_app/data/_restricted/sources/adyar-shakta-upanishads-1950.txt

# 2. generate local JSON + update the gitignored local index
python 05_scripts/local_only/ingest_restricted_source.py \
  --config 05_scripts/local_only/configs/adyar_shakta_1950.config.json \
  --update-local-index

# 3. validate against the config
python 05_scripts/local_only/validate_local_restricted.py \
  --index 03_web_app/data/_restricted/restricted_index.local.json \
  --config 05_scripts/local_only/configs/adyar_shakta_1950.config.json \
  --check-files --strict --verbose

# 4. serve + open locally
cd 03_web_app && python -m http.server 8765
#   http://localhost:8765/?localRestricted=1
#   Religion → Hindu → The Upanishads → View the 108 Map
```

Public active stays 44; local restricted available rises by the family's
gain; future pending drops accordingly; `github.io` stays metadata-only.
Always run the safety script before any commit.

## 8. v131 recommendation

The full Adyar set (6 families, +64 potential local entries) is now
config-ready. Best next step: a **source-aware heading-pattern splitter**
that consumes each config's `coveredUpanishads[].headingPatterns` so the
parser segments a real OCR file by Upanishad (instead of the generic
heading regex) and reports covered-vs-found per family. Strong
follow-ups: a **local restricted progress dashboard** (per-family
expected-gain vs ingested), a one-command **"prepare local source"**
wrapper (generate config if missing → ingest → validate), and a **PD
trigger checklist** keyed on each config's `expectedPublicDomainYear`
(2031 → 2076) for when copyrights actually expire.
