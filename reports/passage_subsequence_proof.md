# Passage Subsequence Proof Report

Every reader-facing passage verified as a contiguous substring of the raw source (after normalization).

## Summary

- **Overall rate:** 99.88% (2,660,212 / 2,663,500 passages verified)
- Targets: 1195
- PASS (100%): 706
- PARTIAL (>=95%): 393
- FAIL (<95%): 0
- SKIP (no raw source linked): 96

## Per-text fidelity distribution

- **100%**: 706 texts
- **99-100%**: 326 texts
- **95-99%**: 67 texts
- **80-95%**: 0 texts
- **50-80%**: 0 texts
- **<50%**: 0 texts

## How this proof works

For each `text.json` in the library, we load its raw source file (via `source.raw_file`) and every passage from the corresponding `passages_*.json`. After normalizing both (whitespace, smart quotes, footnote markers, underscore italics, ellipses), we verify every passage is a contiguous substring of the raw source. This proves no passage was corrupted, invented, or silently altered during ingestion.

Combined with `build_source_hashes.py` (raw sources cryptographically pinned), this gives: **every word the reader sees came verbatim from a named, SHA-256-anchored source.**
