# Package contract & conventions

Every `restricted_toolkits/<id>/` package MUST satisfy this contract.

## Files (exactly these; no others that carry data)
`manifest.json`, `README.md`, `RIGHTS.md`, `SIGNATURES.json`, `acquire.py`, `parse.py`,
`validate.py`, `finalize.py`. No `fixtures/`, `sources/`, `generated/`, `output/`, and no
`*.txt/.epub/.pdf/.usfm/.local.json` — those are gitignored and must never be committed.

## Output paths (enforced by `_shared/io_paths.py`)
- Sources → `data/_restricted/sources/<id>.*` (gitignored)
- Output  → `data/_restricted/generated/<id>.local.json` (gitignored)
- Local index → `data/_restricted/restricted_index.local.json` (gitignored)
- Any attempt to resolve a path outside `data/_restricted/` raises and aborts.

## Script contract
- **acquire.py** — default `--input <user file>`; network fetch ONLY for a `source_option`
  with `allowed:true` (public-domain / clearly-licensed). Never bypasses DRM/paywalls/logins;
  never scrapes against ToS. Writes only under `sources/`.
- **parse.py** — pure, deterministic transform: source → passage schema. No network, no
  embedded text, no hidden fixtures. Same input ⇒ identical output.
- **validate.py** — compare output to `SIGNATURES.json` via `_shared/signatures.compare`.
  Structural diagnostics only (ids/counts/hashes); NEVER prints passage text. Non-zero exit
  on mismatch.
- **finalize.py** — refuses unless validate passed; writes only to the gitignored local tree;
  never touches public `index.json` or `data/*.json(.gz)`.

## Signatures (`SIGNATURES.json`)
Structural fingerprints only — `unit_count`, `first_id`, `last_id`, `book_unit_counts`,
`ordered_ids_sha256`, per-unit `length+tokens`, optional `strict_hashes_sha256`. These are
one-way and non-reconstructive. **No text, excerpts, or readable content of any kind.**

## Rights
`manifest.rights.status` ∈ {public-domain, cc0, open-license, in-copyright}. For in-copyright
texts: `distributable:false`, a clear `RIGHTS.md`, and the lawful-source notice. When rights
are unclear → no toolkit (metadata-only at most, decided separately).

## Forbidden (hard)
No copyrighted text/excerpt/fixture/golden-output/cached-download anywhere here; no DRM/
paywall/login bypass or ToS-violating scraping; no committing output/source/local-index; no
prose in manifests/signatures/logs; no writes to public data; no auto-sync from the private
`05_scripts/local_only/` (promotion is manual + fixture-stripped + reviewed); never relax the
`github.io` local-mode block.
