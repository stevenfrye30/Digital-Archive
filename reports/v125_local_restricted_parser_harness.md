# v125 — Local-only restricted parser harness

v124 built the fail-closed local restricted *loader*. v125 supplies
the *producer*: a local-only parser harness that converts a
lawfully-obtained restricted OCR/text file into the
`data/_restricted/generated/<id>.local.json` shape the loader reads —
writing only under the gitignored `data/_restricted/` tree, never
touching the public archive.

No copyrighted text is committed. The public Muktikā count stays
44 / 108, 64 missing. Public dossiers stay metadata-only.

## 1. Summary

| Field | Before v125 | After v125 |
|---|---|---|
| Build marker | `v124-local-restricted-loader` | **`v125-local-restricted-parser-harness`** |
| Parser harness | none | **`05_scripts/local_only/ingest_restricted_source.py`** |
| Local-only README | none | **`05_scripts/local_only/README.md`** |
| Fake test fixture | none | **`05_scripts/local_only/fixtures/fake_restricted_source.txt`** (placeholder text only) |
| Coverage template (committed) | none | **`03_web_app/data/restricted_templates/covered_upanishads.template.json`** |
| Safety script | v124 | unchanged (already covers the cases) — re-run PASS |
| `MUKTIKA_108` / counts | 44 / 108 | 44 / 108 (unchanged) |
| Copyrighted text committed | none | **none** ✓ |
| Generated `.local.json` committed | none | **none** ✓ (gitignored; verified) |

### Repo-boundary note
The deployed git repo is `03_web_app/`. `05_scripts/` lives one level
up (outside the repo), so the harness/README/fixture are inherently
**local-only** — exactly right for local-restricted tooling that
must never ship. The committed v125 artifacts in `03_web_app/` are:
the build-marker bump, the coverage template, and this report. The
harness is documented here by path.

## 2. Parser harness

* **Path**: `05_scripts/local_only/ingest_restricted_source.py`
* **General**, not hardcoded to one source — driven entirely by CLI.

### CLI options
`--input` (required) · `--source-id` (required) · `--display-title`
(required) · `--translator` · `--publication-year` ·
`--expected-pd-year` · `--rights-holder` (default "Unknown /
requires rights verification") · `--source-family` · `--output`
(required) · `--split-mode` · `--covered-upanishads-json` ·
`--notes` · `--update-local-index` · `--overwrite` · `--dry-run`.

### Split modes
| Mode | Behaviour |
|---|---|
| `plain` (default) | one passage per paragraph; single "Source" section |
| `heading` | split on ALL-CAPS headline lines |
| `upanishad-heading` | split on lines ending in "UPANISHAD"/"Upanishad" |
| `marker` | split on `### Name` marker lines |

Each section's paragraphs become passages with id
`<source-id>.NNNN` and fields `l1` (section label), `l2` (running
number), `l3`/`l4` ("0"), `text`. This is a safe first-pass parse,
not perfect structural parsing.

### Output JSON shape
```json
{
  "id": "<source-id>",
  "restricted": true,
  "availabilityStatus": "local-restricted-available",
  "displayTitle": "…",
  "translator": "…",
  "publicationYear": 1935,
  "expectedPublicDomainYear": 2031,
  "rightsHolder": "…",
  "sourceFamily": "…",
  "sourceType": "restricted-local-text",
  "publicRouteAllowed": false,
  "localRouteAllowed": true,
  "generatedBy": "05_scripts/local_only/ingest_restricted_source.py",
  "generatedAt": "2026-05-28T…",
  "notes": "…",
  "coveredUpanishads": [],
  "passages": [ { "id": "<source-id>.0001", "l1": "…", "l2": "1", "l3": "0", "l4": "0", "text": "…" } ]
}
```
(Generated files contain restricted text, so they are gitignored and
never committed. Committed docs/templates show placeholders only.)

### Safety checks (in-script)
* Refuses any `--output` whose path doesn't contain `data/_restricted/`.
* Refuses any `--output` not ending in `.local.json`.
* Refuses an `--input` inside the public `data/` tree but not under
  `data/_restricted/` (prevents treating public data as restricted).
* Requires `--overwrite` to replace an existing output (except in
  `--dry-run`).
* No `--force` escape hatch — fail-safe by design.
* Prints a LOCAL-ONLY warning, then (on write) the output path,
  passage count, index-update status, and a reminder to run the
  safety script. Never runs git commands.

## 3. Local index helper (`--update-local-index`)

When passed, the harness creates/updates
`03_web_app/data/_restricted/restricted_index.local.json` (gitignored,
local only). It refuses to write the index anywhere outside
`data/_restricted/`. It creates `{ "version": 1, "sources": [] }` if
absent, then upserts the source record (id, status, displayTitle,
translator, publicationYear, expectedPublicDomainYear, rightsHolder,
sourceFamily, localDataPath, publicRouteAllowed:false,
localRouteAllowed:true, coveredUpanishads, notes).

It does **not** touch the committed templates or the public
`restricted_sources_register.json`.

## 4. Templates / README / fixture

| File | Committed? | Contents |
|---|---|---|
| `03_web_app/data/restricted_templates/covered_upanishads.template.json` | yes (repo) | metadata-only coverage template |
| `05_scripts/local_only/README.md` | local (outside repo) | usage docs, placeholder examples |
| `05_scripts/local_only/fixtures/fake_restricted_source.txt` | local (outside repo) | obviously-fake placeholder text ("[restricted local text omitted from fixture]") |

No file contains copyrighted text.

## 5. Test / dry run

Ran the harness against the fake fixture in both modes:

* **`--dry-run`** (marker split, `--update-local-index`): reported
  "would write 4 passages across 3 section(s)" with section labels
  Fake Upanishad One/Two/Three; **wrote nothing**.
* **Real write**: produced
  `data/_restricted/generated/fake-restricted-source.local.json`
  (4 passages) and updated the local index — both confirmed
  **gitignored** via `git check-ignore`. Test artifacts then
  removed.
* **Refusal guards** confirmed:
  * `--output …/data/public_leak.json` →
    "REFUSED: output path must be under data/_restricted/"
  * `--output …/data/_restricted/generated/x.json` →
    "REFUSED: output filename must end with .local.json"

## 6. Safety verification

* `python 05_scripts/check_no_restricted_text.py` → **PASS**
  (2001 tracked files; only the public register, the templates, and
  reports are restricted-related — all metadata only).
* `git status` shows no `_restricted/` files even after a real local
  write (they're ignored).
* `git check-ignore` confirms generated output + local index are
  ignored.
* The committed coverage template is allowed (name contains
  "template").

## 7. How to use locally (step-by-step)

1. Place a lawfully-obtained source at
   `03_web_app/data/_restricted/sources/<id>.txt`.
2. Run the harness (see §2) with `--output
   03_web_app/data/_restricted/generated/<id>.local.json
   --update-local-index`.
3. Serve `03_web_app/` locally and open
   `http://localhost:8765/?localRestricted=1`.
4. Open the matching restricted dossier → "Open local restricted
   copy ›". The local reader shows the text with a "Local restricted
   copy" warning banner.
5. Before any commit, run `python 05_scripts/check_no_restricted_text.py`.

## 8. v126 recommendation

* **v126 (recommended): parser validator** — a local-only
  `validate_local_restricted.py` that checks a generated
  `.local.json` against the expected shape (ids unique, passages
  non-empty, no public-route flags true) and confirms the local
  index points at existing files. Improves reliability of the
  local pipeline without touching the public archive.
* **v126-alt: local-only availability indicator** — a separate
  "Local restricted available: X" badge shown only in local mode on
  the 108 Map, never mixed with the public 44 / 108.
* **v126-deferred: 2031 Adyar Saiva trigger** — metadata-only
  research script staged for the 2031 PD entry.

## 9. Non-destructive guarantees

* No copyrighted source acquired or committed.
* No generated `.local.json` committed (gitignored; verified).
* No restricted text in public data.
* No `MUKTIKA_108` / canon / count change (44 / 108).
* No public local-mode enablement; github.io still hard-blocked
  (v124, unchanged).
* No reading-room redesign; no UI change beyond the build marker.
* No folio / Atlas-Object work.
* Harness has no `--force`; refuses unsafe output/index paths.

## 10. Build marker

`v124-local-restricted-loader` → **`v125-local-restricted-parser-harness`**

The marker reflects the new local-only producer tooling: the v124
loader is now usable end-to-end (lawful local OCR → ignored local
JSON → local-only reader) while the public archive stays completely
copyright-clean.
