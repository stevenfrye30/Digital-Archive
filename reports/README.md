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
