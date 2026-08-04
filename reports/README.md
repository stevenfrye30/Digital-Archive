# Reports

Snapshot reports from the archive's maintenance tooling. These are
human-readable summaries; the underlying full JSON outputs live in the
working tree and are not published here.

The reports reflect the project's state at the time of the most recent
refresh; they are not regenerated automatically.

| Report | Source | What it answers |
|---|---|---|
| `archive_health.md` | `tools/lint_archive.py` | One-page snapshot. The page to read first. |
| `passage_subsequence_proof.md` | `05_scripts/passage_subsequence_proof.py` | Are the reader's passages still verbatim against their raw sources? |
| `final_validation.md` | `05_scripts/final_validation.py` | Per-text health: clean / acceptable / needs work. |
| `corpus_audit_report.md` | `05_scripts/corpus_audit.py` | Structural problems — duplicate passage ids, missing front matter, short stubs. |
| `archive_link_audit.md` | `tools/validate_archive_links.py` | Reading Room ↔ canonical library link integrity. |
| `shelves_drift.md` | `tools/check_shelves_drift.py` | What entries are not yet on the curated shelves. |

The full refresh sequence is in `../MAINTENANCE.md`.

## Lane audits and design doctrine (moved here 2026-08-04, Task 153)

Twenty audit/report documents that had accumulated at the repo root,
directly beside `index.html`, were moved into this directory: the
`WITNESS_*` / `OBJECT_*` / `LEAF_*` / `FOLIO_*` constitutions and audits,
the `GENESIS_*` roadmap/coverage/harmonization set, the
`CIVILIZATIONAL_*` and `CODEX_`/`COSMOGRAM_` audits,
`ATLAS_EDITORIAL_AUDIT.md`, `READING_CHOREOGRAPHY.md` and
`DUPLICATE_IDS.md`. They are records of completed lanes, not live
tooling output, so they are not in the table above.

`index.html` carries CSS comments of the form `/* … See
OBJECT_FAMILY_CONSTITUTION.md. */` — nine of them. Those name the file
without a path and were deliberately left alone rather than edited: they
still identify the document, and rewriting comments in the deployed
entrance page is more risk than the precision is worth. Look here.

Two root documents were deliberately **not** moved:
`BIBLE_FOLIO_OBJECT_INDEX.md`, which `object_scripts/build_folio_object_index.py`
regenerates at the root and `reports/diag_v63_usability_documentation.py`
asserts is there; and `SENECA_RESTORATION_2026.md`, which is a published
restoration record with a live root URL.

*(That generator lived at `03_web_app/05_scripts/` when this note was
written; Task 154 renamed the directory to `object_scripts/` on
2026-08-04. Bare `05_scripts/` in this repo — including the three rows
in the table above — now unambiguously means the parent working tree's
`05_scripts/`, which is the convention `../STATUS.md` already states.)*
