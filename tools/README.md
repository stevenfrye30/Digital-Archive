# Tools

The maintenance scripts that produce the reports under `../reports/`.
They are kept here as part of the archive's institutional record.

These scripts expect the full Digital-Archive working tree as a parent
directory:

```
Digital-Archive/
├── 01_library/library/texts/**/text.json
├── 01_library/library/metadata/registry.json
├── 02_raw_sources/manifest.json
├── 05_scripts/                  ← scripts also live here in the working tree
├── logs/
└── 03_web_app/                  ← this repo's filesystem root
    └── tools/                   ← these copies
```

They will not run from the published repository alone. Running them
requires the canonical library source tree on the local filesystem, the
raw-source archive, and the parent working directory's `05_scripts/`,
`logs/`, and `01_library/` paths to resolve. The published copies here
are a record of what the tooling looks like at the time of the
institutional checkpoint, not an executable bundle.

## What each tool does

- **`lint_archive.py`** — single-command project health check. Calls the
  three validators below and assembles `reports/archive_health.md`.
- **`validate_archive_links.py`** — verifies that every Reading Room
  entry's `library_id` resolves in the canonical registry, and that every
  `entity.html?id=...` reference points at an existing entry.
- **`check_shelves_drift.py`** — reports new entries on disk that the
  Reading Room shelves do not yet cover, and shelf links that point at
  missing entries.
- **`validate_metadata.py`** — schema validator for every `text.json`
  in the canonical library. Holds the closed sets for `tradition`,
  `category`, `source_quality`, and the recognised publishers and URL
  domains. Worth reading as a snapshot of the corpus's working
  vocabulary.
- **`build_cleanliness_report.py`** — joins the validation, audit,
  registry, and integrity reports into the human-readable
  `TEXT_CLEANLINESS.md`. Run after refreshing the underlying reports
  if you want the cleanliness document to reflect the current corpus.
- **`corpus_audit.py`** — the structural duplicate-id, front-matter,
  and short-stub auditor. Reads `03_web_app/data/index.json` and the
  per-translation passage files. As of the May 2026 Quran restoration,
  groups by `(text_id, data_file)` so multi-translation works no
  longer surface false-alarm dup-id totals.
- **`render_commentary_prototype.py`** — the May 2026 commentary-
  prototype renderer. Reads canonical Apannaka-jātaka passages and
  five hand-crafted sibling commentary records, emits a single
  self-contained HTML page testing the constitutional architecture
  (bare-canon byte-equivalence, layer non-collapse, AI quarantine,
  bridge-gap honesty). Local-only artifact. Findings recorded in
  `COMMENTARY_PROTOTYPE_2026.md`.

## Refresh ritual

The full refresh sequence is documented in `../MAINTENANCE.md` under
"Refreshing the truth." The short form is one command:

```
python 05_scripts/lint_archive.py
```

run from the Digital-Archive working tree.
