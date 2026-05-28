# v129 — Adyar Yoga 1938 local parser config

v128 made the Saiva Upanishads (Adyar Library, 1935) ready for safe
local-only ingestion via a metadata-only config and config-driven
tooling. v129 does the same for the **Yoga Upanishads (Adyar Library,
1938)** — reusing the v128 `--config` support **unchanged**.

This is a metadata/config/tooling pass. **No source was acquired, no
copyrighted text was downloaded or committed, no generated `.local.json`
was committed, public data and `MUKTIKA_108` are untouched, and the
public count stays 44 / 108.**

## 1. Summary

| Field | Before v129 | After v129 |
|---|---|---|
| Build marker | `v128-adyar-saiva-local-config` | **`v129-adyar-yoga-local-config`** |
| Source config | Adyar Saiva (v128) | **+ `05_scripts/local_only/configs/adyar_yoga_1938.config.json`** |
| Parser harness | v128 `--config` | **unchanged** (reused) |
| Validator | v128 `--config` | **unchanged** (reused) |
| README | v128 | **+ Adyar Yoga 1938 workflow** |
| Public active count | 44 / 108 | 44 / 108 (unchanged) |
| `MUKTIKA_108` / public data | untouched | untouched |
| Restricted text / `data/_restricted` / `*.local.json` committed | none | **none** ✓ |

### Repo-boundary note
`05_scripts/` is **not** a git repository — only `03_web_app/` is. So the
config and the README live in `05_scripts/local_only/` as canonical
local-only tooling and are not part of the public `03_web_app` commit
(same as v124–v128). The committed v129 artifacts in `03_web_app/` are
the build-marker bump and this report.

## 2. Adyar Yoga coverage

Confirmed from `RESTRICTED_SOURCES` + `MUKTIKA_108` in
`03_web_app/index.html` (not a hand-typed list):

| Field | Value |
|---|---|
| id | `adyar-yoga-upanishads-1938` |
| displayTitle | Yoga Upanishads (Adyar Library) |
| translator / editor | T. R. Srinivasa Ayyangar (tr.) *(verify editor against physical copy)* |
| publication year | 1938 |
| expected public-domain year | 2034 |
| rights holder | Adyar Library and Research Centre, Chennai (likely) |
| rights confidence | likely |
| availability status | public-domain-deferred |
| register source family | Adyar Library English Series |
| class | Yoga |
| expected coverage gain | 7 |

**Covered Muktikā entries (all Yoga-class):**

| # | Upanishad | Veda | Archive status |
|---|---|---|---|
| 19 | Trīśikhi-brāhmaṇa | Shukla Yajurveda | future-public-domain |
| 40 | Kṣurikā | Krishna Yajurveda | future-public-domain |
| 45 | Brahmavidyā | Krishna Yajurveda | future-public-domain |
| 50 | Yogaśikhā | Krishna Yajurveda | future-public-domain |
| 54 | Kara | Krishna Yajurveda | future-public-domain |
| 68 | Yoga-cūḍāmaṇi | Samaveda | future-public-domain |
| 76 | Darśana | Samaveda | future-public-domain |

* **Public active vs local/future:** all 7 are currently
  `future-public-domain` — **none** is publicly active. So the public
  count is unaffected (`44 active · 64 future · 0 needed · 108 total`).
* **Already-active Yoga-class (NOT counted as closures):** the archive
  already has 10 active Yoga Upanishads — Nāda-bindu #3, Haṃsa #14,
  Maṇḍala-brāhmaṇa #20, Amṛta-bindu #37, Amṛta-nāda #38, Tejo-bindu #43,
  Dhyāna-bindu #44, Yogatattva #46, Yoga-kuṇḍalinī #56, Śāṇḍilya #91.
  These are correctly excluded from the source's coverage; the Adyar
  volume may hold them as duplicate witnesses but they would not change
  the public count.
* **Expected local availability gain:** up to **7** local restricted
  chips once a lawful local copy is ingested (future pending would drop
  64 → 57 locally; public stays 44).
* **Expected PD year:** 2034 (US copyright term on a 1938 publication).

## 3. Config file

* **Path:** `05_scripts/local_only/configs/adyar_yoga_1938.config.json`
* **Contents:** metadata only — same shape as the v128 Adyar Saiva
  config: `configVersion`, `sourceId`, `displayTitle`, `sourceFamily`
  (`Adyar Yoga`), `tradition`, `category`, `classType` (`Yoga`),
  `translatorOrEditor`, `publicationYear`, `expectedPublicDomainYear`,
  `rightsHolder`, `rightsHolderConfidence`, `availabilityStatus`,
  `localOnly`, route flags, `expectedCoverageGain`, default input/output/
  index paths, `recommendedSplitMode` (`upanishad-heading`),
  `coveredUpanishads[]` (7 entries with `muktikaNumber`, provisional
  ASCII `key`, `displayTitle`, `veda`, `classType`,
  `currentArchiveStatus`, `headingPatterns`), and `notes`.
* **No text:** contains no passages and no copyrighted content.
* **How it is used:** passed via `--config` to the existing harness and
  validator. `key` slugs are provisional; `headingPatterns` are
  forward-looking hints for source-aware splitting (the v125 splitter
  still uses a generic Upanishad-heading regex).

## 4. Parser / validator impact

**No code changes were required.** The v128 `--config` support in
`ingest_restricted_source.py` and `validate_local_restricted.py` is
generic and worked unchanged for the Adyar Yoga config:

* Harness: config dry-run (missing input), fixture-override dry-run,
  generation, and CLI override all behaved correctly.
* Validator: id / `expectedPublicDomainYear` / `sourceFamily` / covered
  Muktikā numbers cross-checked against the Yoga config and matched.
* The v128 Adyar Saiva config still dry-runs correctly (no regression),
  and v125/v126 no-config usage is unaffected.

## 5. README — one-step local workflow

`05_scripts/local_only/README.md` gained an **Adyar Yoga 1938 local
ingestion** section mirroring the Saiva one: place lawful text → config
dry-run → generate + update local index → validate with `--config` →
serve `03_web_app` → open `?localRestricted=1` → 108 Map, plus the
never-commit warnings and the up-to-7 expected local gain.

## 6. Tests (fake fixtures only; all removed before commit)

| Test | Result |
|---|---|
| `--config --dry-run`, default input **missing** | PASS — config summary, covered count **7**, nums `[19,40,45,50,54,68,76]`, "input missing" warning, no files written |
| `--config --input <fake fixture> --split-mode marker --dry-run` | PASS — 4 passages / 3 sections previewed, no files written |
| Fake generation via config + `--update-local-index` | PASS — wrote under `data/_restricted/` (gitignored) |
| Validate source `--config --allow-placeholder` | PASS — coverage matches config (7) |
| Validate index `--check-files --config` | PASS — entry + referenced source cross-checked, coverage matches (7) |
| v128 Adyar Saiva config still dry-runs | PASS — 13 covered, unchanged |
| Fake generated files + index removed | done |

## 7. Safety verification

* `python 05_scripts/check_no_restricted_text.py` → **PASS** (scanned
  ~2006 tracked files in `03_web_app/`; only metadata templates,
  register, and reports tracked).
* No `data/_restricted/` tracked; no `*.local.json` committed; no
  restricted text committed.
* **Safety script review (Part 7):** no change needed — it scans only
  tracked files in `03_web_app/` (so `05_scripts/local_only/configs/` is
  out of scope), already **allows** metadata `*.config.json`, and still
  **blocks** `*.local.json`, `restricted_index.local.json`, the real
  local configs, `*.restricted.json`, and anything under `_restricted/`.

## 8. How to use this locally (with a lawful copy)

```
# 1. place lawful OCR/text
03_web_app/data/_restricted/sources/adyar-yoga-upanishads-1938.txt

# 2. generate local JSON + update the gitignored local index
python 05_scripts/local_only/ingest_restricted_source.py \
  --config 05_scripts/local_only/configs/adyar_yoga_1938.config.json \
  --update-local-index

# 3. validate against the config
python 05_scripts/local_only/validate_local_restricted.py \
  --index 03_web_app/data/_restricted/restricted_index.local.json \
  --config 05_scripts/local_only/configs/adyar_yoga_1938.config.json \
  --check-files --strict --verbose

# 4. serve + open locally
cd 03_web_app && python -m http.server 8765
#   http://localhost:8765/?localRestricted=1
#   Religion → Hindu → The Upanishads → View the 108 Map
```

Public active stays 44; local restricted available rises by up to 7;
future pending drops accordingly; `github.io` stays metadata-only.
Always run the safety script before any commit.

## 9. v130 recommendation

The config pattern is now proven across two Adyar families (Saiva 13,
Yoga 7) with zero tooling changes. Best next step: **build a config
generator** that emits the remaining Adyar family configs from
`RESTRICTED_SOURCES` + `MUKTIKA_108` in one pass —
**Sāmānya Vedānta 1941** (#6, 17, 42, 51, 52, 58, 73, 94, 95, 97, 103;
PD 2037), **Vaishnava 1945** (PD 2041), **Shakta 1950** (PD 2046),
**Samnyāsa 1978** — so all Adyar volumes become ingestion-ready and the
covered-number/metadata is guaranteed consistent with the register.
Strong follow-ups: a **local restricted source progress dashboard**
(per-family expected-gain vs ingested) and source-aware splitting that
consumes `headingPatterns`.
