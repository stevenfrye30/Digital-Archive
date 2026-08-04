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
The documents that ship beside this file — every link below resolves —
are:

- **[STATUS.md](STATUS.md)** — current counts, validation state, what's
  canonical, what's legacy. The truth surface; the pre-push guard reads
  its numbers as the deploy invariant.
- **[DUPLICATE_IDS.md](reports/DUPLICATE_IDS.md)** — what counts as a duplicate
  in the corpus, and what does not.
- **[SENECA_RESTORATION_2026.md](SENECA_RESTORATION_2026.md)** — the
  Seneca minor-dialogues re-path: restoration record for the third
  editorial pass.
- **[`reports/`](reports/)** — periodic snapshots from the maintenance
  tooling: integrity proof, validation summary, link audits, and the
  numbered per-build reports (v58 → v133).
- **[`tools/`](tools/)** — the maintenance scripts themselves,
  including the pre-push guard (`prepush_guard.py`) that blocks any
  push where the index disagrees with STATUS.md or a restricted text's
  body is tracked.

### The Genesis codex

Since May 2026 the reader's deepest design work has treated Genesis as
an annotated codex: object families with resonance pairings, witness
families given distinct manuscript identities, the leaf redefined from
modal overlay to prepared sheet, Doré plates behind a museum scrim, a
portrait cosmogram of the five Hebrew cosmic strata. The work is
shipped (build meta v133) and its design doctrine sits beside this
file:

- **[WITNESS_FAMILY_CONSTITUTION.md](reports/WITNESS_FAMILY_CONSTITUTION.md)** —
  how each witness family earns a distinct manuscript identity.
- **[OBJECT_FAMILY_CONSTITUTION.md](reports/OBJECT_FAMILY_CONSTITUTION.md)** —
  the object families and their material rules.
- **[FOLIO_OBJECT_ARCHITECTURE.md](reports/FOLIO_OBJECT_ARCHITECTURE.md)** —
  the leaf as prepared sheet: archival margins, entrance cadence.
- **[READING_CHOREOGRAPHY.md](reports/READING_CHOREOGRAPHY.md)** — movement,
  cadence, orientation, temporality.
- **[GENESIS_MATURATION_ROADMAP.md](reports/GENESIS_MATURATION_ROADMAP.md)**,
  **[GENESIS_EXPANDED_COVERAGE_PLAN.md](reports/GENESIS_EXPANDED_COVERAGE_PLAN.md)**,
  **[GENESIS_HARMONIZATION_PASS.md](reports/GENESIS_HARMONIZATION_PASS.md)** —
  the living plan: waves, coverage, harmonization.
- The audit records (leaf, orientation, temporality, cosmogram,
  civilizational inheritance and geography, reading flow) sit in the
  same folder — each grounded in captured screenshots and a metrics
  JSON. Audit against evidence, specify, implement, verify: that loop
  is the house pattern.

### Internal stewardship records

The rest of the institutional layer — the operating handbook, the
text-cleanliness census, the restoration records (Qurʾān, Jātaka ×2),
the May 2026 stabilization checkpoint, and the constitutional law
governing commentary, provenance layers, citation permanence,
public/private boundaries, and AI stewardship — lives in the archive's
internal working repository, which does not publish. Those documents
were briefly mirrored here; the mirror drifted and was deliberately
removed in July 2026, because a link that can rot is worse than an
honest note. Run artifacts that did ship remain under
[`reports/`](reports/) and [`tools/`](tools/).

For the record, the internal set comprises: MAINTENANCE,
TEXT_CLEANLINESS, STATE_OF_THE_ARCHIVE, STABILIZATION_EDITION,
QURAN_RESTORATION, JATAKA_RESTORATION, JATAKA_VOL6_ACQUISITION; the
doctrine set (CONSTITUTION, COMMENTARY_ARCHITECTURE, PERMANENCE —
consolidated 2026-07 from the twelve commentary-era documents, whose
originals are retained unaltered as records — plus AI_STEWARDSHIP_POLICY
and AUGMENTATION_POSTURE); COMMENTARY_PROTOTYPE,
PERMANENCE_PROTOTYPE; and the reading-surface records
(READING_ROOM_CONSTITUTIONAL_AUDIT, APPARATUS_PROPAGATION_REPAIR,
MOBILE_READING_REFINEMENT, MOBILE_READING_STATE_IMPLEMENTATION,
AUGMENTATION_POSTURE).

The archive is built slowly, read slowly, and maintained without
hurry.
