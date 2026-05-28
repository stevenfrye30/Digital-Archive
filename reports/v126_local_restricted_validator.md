# v126 — Local-only restricted validator

v125 built the producer (parser harness). v126 adds the **checker**:
a local-only validator that verifies generated restricted JSON files
and the local restricted index *before* they are used by the v124
loader — shape validation, path safety, id-uniqueness, index↔source
cross-checks, and fixture-placeholder detection.

Contains no copyrighted text and never prints passage text. Public
Muktikā count stays 44 / 108, 64 missing. Public dossiers stay
metadata-only.

## 1. Summary

| Field | Before v126 | After v126 |
|---|---|---|
| Build marker | `v125-local-restricted-parser-harness` | **`v126-local-restricted-validator`** |
| Validator | none | **`05_scripts/local_only/validate_local_restricted.py`** |
| README validator section | none | **added** |
| `MUKTIKA_108` / counts | 44 / 108 | 44 / 108 (unchanged) |
| Copyrighted text committed | none | **none** ✓ |
| Generated `.local.json` committed | none | **none** ✓ |

### Repo-boundary note
`05_scripts/` is outside the deployed `03_web_app/` repo, so the
validator + README are inherently local-only (correct for
local-restricted tooling). Committed v126 artifacts in `03_web_app/`:
the build-marker bump and this report.

## 2. Validator script

* **Path**: `05_scripts/local_only/validate_local_restricted.py`
* **Modes**: `--source <file>` (one generated local source),
  `--index <file>` (the local index), or both. `--check-files`
  (with `--index`) validates every referenced source. `--verbose`,
  `--strict`, `--allow-placeholder`.
* **Exit codes**: `0` pass, `1` one or more FAILs, `2` usage error.
* **Safe output**: prints only ids, counts, and PASS/WARN/FAIL
  lines — **never passage text**.

## 3. Source JSON checks

**Required (FAIL if wrong/missing):** `id` (non-empty string),
`restricted === true`, `availabilityStatus ===
'local-restricted-available'`, `displayTitle` (non-empty),
`sourceType === 'restricted-local-text'`, `publicRouteAllowed ===
false`, `localRouteAllowed === true`, `passages` (non-empty array).

**Passage checks (FAIL):** each passage has a string `id` and a
non-empty `text`; passage ids unique.

**Recommended (WARN; FAIL under `--strict`):** `translator`,
`publicationYear`, `expectedPublicDomainYear`, `rightsHolder`,
`sourceFamily`, `generatedBy`, `generatedAt`, `notes`,
`coveredUpanishads`.

**Placeholder detection:** passages whose text contains a fixture
marker (`[restricted local text omitted from template]`,
`[restricted local text omitted from fixture]`, `this is not a real
source`, `fake upanishad`) → FAIL, unless `--allow-placeholder`
(then WARN).

## 4. Index checks

**Required (FAIL):** `version`; `sources` array; each entry: `id`
(unique non-empty), `status === 'local-restricted-available'`,
`displayTitle`, `localDataPath` (non-empty), `publicRouteAllowed ===
false`, `localRouteAllowed === true`.

**Recommended (WARN; FAIL under `--strict`):** `translator`,
`publicationYear`, `expectedPublicDomainYear`, `rightsHolder`,
`sourceFamily`, `coveredUpanishads`, `notes`.

**With `--check-files`:** each `localDataPath` must end
`.local.json`, resolve under `data/_restricted/`, and exist; the
referenced source is fully validated; and the source file's `id`
is cross-checked against the index entry's `id`.

## 5. Safety checks

* `--source` / `--index` / each `localDataPath` must contain
  `data/_restricted/` and resolve **under** `03_web_app/data/_restricted/`.
* `..` path segments are rejected.
* Public-data paths (e.g. `data/index.json`) are rejected.
* FAIL if `publicRouteAllowed` is true, `restricted` is not true,
  `localRouteAllowed` is not true, or `sourceType` is wrong.

## 6. Strict mode

`--strict` promotes all recommended fields to required, and
additionally requires `publicationYear` + `expectedPublicDomainYear`
to be integers, `rightsHolder` non-empty, and `coveredUpanishads`
non-empty.

## 7. Test results (fake fixture)

Regenerated the v125 fake output + index, then:

| Test | Command | Result |
|---|---|---|
| 1. Source, no allow-placeholder | `--source …fake….local.json` | **FAIL** (exit 1) — "4 passage(s) contain placeholder/fake text" |
| 2. Source, allow-placeholder | `--source … --allow-placeholder --verbose` | **PASS** (exit 0) — 4 passages, unique ids, route flags correct, "placeholder passages: 4 (allowed)" |
| 3. Index, check-files, allow-placeholder | `--index … --check-files --allow-placeholder` | **PASS** (exit 0) — referenced source + index both pass |
| 4. Path safety | `--source 03_web_app/data/index.json` | **FAIL** (exit 1) — "source path must be under data/_restricted/" |

Fake generated output + local index then **removed**.

## 8. Safety verification

* `python 05_scripts/check_no_restricted_text.py` → **PASS** (only
  public register + templates + reports are restricted-related, all
  metadata-only).
* No `data/_restricted/` files tracked; no generated `.local.json`
  committed (verified via git status after fake removal).

## 9. How to use locally

```
# after running the v125 harness:
python 05_scripts/local_only/validate_local_restricted.py \
  --index 03_web_app/data/_restricted/restricted_index.local.json \
  --check-files --verbose
# (add --strict for required-field enforcement;
#  add --allow-placeholder only for the fake fixture)
```
Then, before any commit: `python 05_scripts/check_no_restricted_text.py`.

## 10. v127 recommendation

* **v127 (recommended): local-only availability indicator** — a
  separate, clearly-labelled "Local restricted available: X" badge
  shown only in local mode on the 108 Map, never mixed with the
  public 44 / 108.
* **v127-alt: source-specific Adyar Saiva local parser config** — a
  committed (metadata-only) config that pre-fills the harness flags
  for the Adyar Saiva volume, so a lawful local copy can be ingested
  in one step.
* **v127-deferred: 2031 Adyar Saiva trigger** — metadata-only
  research script staged for the 2031 PD entry.

## 11. Non-destructive guarantees

* No restricted source acquired or committed.
* No generated `.local.json` committed (verified).
* No public data / `MUKTIKA_108` / count change (44 / 108).
* No public local-mode enablement; github.io hard-block unchanged.
* No UI change beyond the build marker; no reading-room redesign.
* No folio / Atlas-Object work.
* Validator never prints passage text; refuses unsafe paths.

## 12. Build marker

`v125-local-restricted-parser-harness` → **`v126-local-restricted-validator`**

The local restricted pipeline is now end-to-end safe: produce
(v125) → validate (v126) → load locally (v124), with the public
archive remaining copyright-clean throughout.
