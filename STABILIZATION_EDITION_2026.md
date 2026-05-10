# Stabilization Edition — May 2026

A note recording the moment the archive crossed into operational
coherence.

## State

The Digital Archive at this date holds **1,131 schema-validated
text.json files** representing **1,086 distinct works** and **1,200
published translations**. Every reader-facing passage has been verified
against its named raw source at **99.88 % overall fidelity**, with no
text falling below the 95 % integrity threshold. **22,651 raw source
files** are SHA-256 anchored.

A separate hand-edited Reading Room holds **205 entries**, all
reachable through the deeper shelves, with five on the front shelf and
ten conforming to the Source Integrity Standard v1.

## Confidence

Passage preservation is no longer a working concern. The integrity
proof has been re-run against the full corpus and shipped as part of
the public record. Passages that the reader sees came verbatim from a
named, hash-anchored source — this is mechanically verifiable, not a
claim.

The remaining work is structural and editorial — parser hierarchy
gaps, locator imprecision, schema warnings, slow migration of older
Reading Room entries to the integrity standard. These do not threaten
the corpus; they shape how navigable it feels. They will be addressed
unhurriedly.

## Reading Room maturity

The Reading Room is small by intention and will continue to grow
slowly. It is not a generated mirror of the canonical library but a
hand-authored shelf that soft-links to it. Discoverability is layered:
a curated front shelf for active reading, deeper shelves grouped by
tradition, deep-link entries reachable by URL or by the graph. A
public-facing state page makes the institution's current condition
visible without making the front shelf a dashboard.

## Stewardship discipline

The maintenance discipline that emerged across this stabilization
cycle:

- One command (`python 05_scripts/lint_archive.py`) returns a single
  page of project health.
- Reports refresh on demand from the canonical library, never by
  hand-editing.
- The closed sets in `validate_metadata.py` are extended only when a
  legitimate new use appears in the corpus.
- The Reading Room's atmosphere is preserved over scale. Discoverability
  was added with restraint, not by flattening into a database UI.
- Generated artefacts are not committed casually; the difference between
  canonical content and derived view is preserved in the git history.

## Tensions to live with

Recorded so they are not re-discovered.

- The repository's `.git` lives at `03_web_app/` rather than at the
  Digital-Archive root. Re-rooting would require GitHub Pages
  reconfiguration. The misnomer is acceptable.
- Institutional documents exist in two places: in the working tree and
  in the published repo. They drift unless deliberately synced. The
  refresh ritual should include the sync step.
- The canonical metadata for a work is a `text.json` file; the
  registry is generated. When a translation directory is renamed, the
  Reading Room's `library_id` pointers can silently break. The link
  validator catches this after the fact.
- A small number of structural duplicate-id texts (Qur'an, Jataka, the
  CCEL Christian patristic cluster) carry the bulk of the parser-issue
  volume. They need per-work re-ingest with corrected hierarchy parsers.
- Schema validation produces ~233 content-level warnings (missing
  `source.url`, `source_quality`, `original_*`). These are filled in
  when individual texts are revisited, not in a sweep.
- The Reading Room's Source Integrity Standard v1 migration sits at
  10 / 205 entries. Migration is per-text and unhurried.

## What is next

Slow editorial work. Reading the texts. Bringing individual texts up
to standard when their turn comes. The infrastructure work is done; it
will rarely need to be done again at this scale.

The archive enters its first mature reading season here.

---

*Refreshed reports are at `logs/reports/`. The single-command health
check is `python 05_scripts/lint_archive.py`. The current text-by-text
condition report is `TEXT_CLEANLINESS.md`. The operating handbook is
`MAINTENANCE.md`. The truth surface is `STATUS.md`.*
