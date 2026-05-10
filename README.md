# Digital Archive

A reading room for public-domain sacred and historical texts.

**[Read here →](https://stevenfrye30.github.io/Digital-Archive/)**

---

A small number of texts have been carefully stewarded — apparatus
restored, transmission noise examined, stewardship history visible
inside the reader. Most of the catalog reflects ingestion-time state
without further editorial work.

A curated short list of stewarded entry points lives at the
[archive shelf](https://stevenfrye30.github.io/Workspace/archive/).

## Sources

Texts are drawn from Project Gutenberg, SacredTexts.com, Suttacentral,
eBible, and the Internet Archive. All are public domain (pre-1929 or
Project Gutenberg verified) or Creative Commons (Suttacentral).
Copyrighted works are excluded from distribution.

## What's inside

- Parallel translations side by side
- Translator index
- Full-text search across the corpus
- Attribution manifest with license per translation
- Permalinks down to the passage level
- Apparatus and stewardship annotations on stewarded texts

## For tinkerers

The reader is a static site — plain HTML + JSON. Data files are shipped
pre-gzipped (`*.json.gz`) and decompressed in the browser via
`DecompressionStream`. Everything else happens client-side.

## Stewardship

The reader is the public face of a longer-running stewardship project.
The institutional layer — what counts as a clean text, how the corpus
is validated, how the curated [archive shelf](https://stevenfrye30.github.io/Workspace/archive/)
relates to this catalog — is recorded in:

- **[STATUS.md](STATUS.md)** — current counts, validation state, what's
  canonical, what's legacy. The truth surface.
- **[MAINTENANCE.md](MAINTENANCE.md)** — operating handbook. How
  refresh works, what should never be edited casually.
- **[DUPLICATE_IDS.md](DUPLICATE_IDS.md)** — what counts as a duplicate
  in the corpus, and what does not.
- **[`reports/`](reports/)** — periodic snapshots from the maintenance
  tooling: integrity proof, validation summary, link audits.
- **[`tools/`](tools/)** — the maintenance scripts themselves. They
  expect the canonical working tree to operate; they are kept here as
  a record of what the project's maintenance discipline looks like.

The archive is built slowly, read slowly, and maintained without
hurry.
