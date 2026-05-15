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
- **[TEXT_CLEANLINESS.md](TEXT_CLEANLINESS.md)** — text-by-text condition:
  which works are clean, which are acceptable, which need work, with
  definitions. Read this before assuming "needs work" means damaged.
- **[MAINTENANCE.md](MAINTENANCE.md)** — operating handbook. How
  refresh works, what should never be edited casually.
- **[DUPLICATE_IDS.md](DUPLICATE_IDS.md)** — what counts as a duplicate
  in the corpus, and what does not.
- **[STABILIZATION_EDITION_2026.md](STABILIZATION_EDITION_2026.md)** —
  the May 2026 institutional checkpoint, recording the moment the
  archive crossed into operational coherence.
- **[QURAN_RESTORATION_2026.md](QURAN_RESTORATION_2026.md)** — the
  first editorial restoration pass: notes on what was thought to be
  wrong with the Qurʾān, what was actually wrong, and what was done.
- **[JATAKA_RESTORATION_2026.md](JATAKA_RESTORATION_2026.md)** — the
  second editorial restoration pass, on the Pāli Jātaka birth-story
  corpus. Like the Qurʾān, mostly preservation work; the existing
  Cowell volumes were already at edition quality.
- **[JATAKA_VOL6_ACQUISITION_2026.md](JATAKA_VOL6_ACQUISITION_2026.md)** —
  acquisition of the missing Cowell Vol 6 (1907) from the Internet
  Archive, closing the canonical six-volume scholarly set. The new
  volume is honestly tagged `source_quality: provisional` because the
  OCR is noisier than the SacredTexts cleanup of vols 1–5.

### Commentary architecture (constitutional, not yet implemented)

In May 2026 the archive began designing the foundational rules under
which commentary, annotation, scholarly apparatus, and interpretive
overlays may eventually attach to the primary corpus. These documents
define the law; no commentary engine is built yet.

- **[COMMENTARY_CONSTITUTION.md](COMMENTARY_CONSTITUTION.md)** —
  foundational law. What commentary is, what it is not, the bare-
  canon guarantee, the refusal index.
- **[COMMENTARY_ONTOLOGY.md](COMMENTARY_ONTOLOGY.md)** — categories
  of commentary, with the careful argument for why the archive
  imposes some classification and refuses other classification.
- **[COMMENTARY_ATTACHMENT_MODEL.md](COMMENTARY_ATTACHMENT_MODEL.md)** —
  how commentary attaches: anchor format, granularity, sub-locators,
  resolution rules.
- **[PROVENANCE_LAYERS.md](PROVENANCE_LAYERS.md)** — the seven
  authorship layers (primary text, source apparatus, traditional
  commentary, modern scholarship, archive editorial notes, AI
  output, private annotations) and why they must never collapse.
- **[INTERPRETIVE_BOUNDARIES.md](INTERPRETIVE_BOUNDARIES.md)** — what
  the archive refuses to do, in detail.
- **[COMMENTARY_SCHEMA_SKETCH.md](COMMENTARY_SCHEMA_SKETCH.md)** —
  illustrative JSON sketches; not adopted yet.
- **[COMMENTARY_PROTOTYPE_2026.md](COMMENTARY_PROTOTYPE_2026.md)** —
  notes from pressure-testing the constitutional architecture against
  a single tale (Apannaka-jātaka). Records what worked, what was
  awkward, and the six implementation tensions surfaced before scale.

### Commentary lifecycle architecture (stewardship discipline, not yet implemented)

After the May 2026 prototype, the archive turned to designing the
long-term lifecycle of commentary as an archival object. These seven
documents specify the discipline that future implementations of the
commentary infrastructure must obey to survive archival time — decades,
centuries — without silently rewriting their own history.

- **[COMMENTARY_LIFECYCLE.md](COMMENTARY_LIFECYCLE.md)** — the eight
  states a commentary record may occupy (drafted, provisional,
  verified, deprecated, superseded, withdrawn, unresolved, orphaned)
  and the legal transitions between them. The no-deletion principle.
- **[COMMENTARY_VERSIONING.md](COMMENTARY_VERSIONING.md)** —
  append-only sibling-record revisions, date-suffix identifiers,
  bidirectional supersession pointers. Why diffs are not stored.
- **[CITATION_PERMANENCE.md](CITATION_PERMANENCE.md)** — the URN
  scheme, alias tables, schema-version pinning, the resolver's
  contract, the 2126-resolves-2026 commitment.
- **[COMMENTARY_MIGRATION.md](COMMENTARY_MIGRATION.md)** — the
  migration manifest discipline, frozen-generation support,
  reversibility classes, the no-silent-migration rule.
- **[COMMENTARY_REPAIR_PROTOCOLS.md](COMMENTARY_REPAIR_PROTOCOLS.md)** —
  the taxonomy of failures (broken anchor, layer-collapse, duplicate
  id, damaged file, contradictory metadata, ...) and how each is
  detected, quarantined, and repaired. The fail-honestly discipline.
- **[PUBLIC_PRIVATE_BOUNDARIES.md](PUBLIC_PRIVATE_BOUNDARIES.md)** —
  the five degrees of publication (canonical / public-cache /
  working / experimental / reader-local) and the rules governing
  transitions between them.
- **[AI_STEWARDSHIP_POLICY.md](AI_STEWARDSHIP_POLICY.md)** — the
  formal long-term policy for Layer-6 AI-generated content:
  retention, labeling, identity preservation, prompt provenance,
  the dual-authorship pattern, and the prohibited behaviors.

### Operational permanence (first prototype)

- **[PERMANENCE_PROTOTYPE_2026.md](PERMANENCE_PROTOTYPE_2026.md)** — the
  May 2026 URN resolver prototype: what was built, what worked, where
  the architecture is fragile, what should not scale. The first
  operational counterpart to the constitutional permanence commitments.
  Run artifacts live at [`reports/permanence_audit.md`](reports/permanence_audit.md)
  and [`reports/permanence_audit.json`](reports/permanence_audit.json);
  the scripts at [`tools/resolve_urn.py`](tools/resolve_urn.py) and
  [`tools/verify_permanence.py`](tools/verify_permanence.py).

### Reading Room constitutional audit

- **[READING_ROOM_CONSTITUTIONAL_AUDIT_2026.md](READING_ROOM_CONSTITUTIONAL_AUDIT_2026.md)** —
  May 2026 audit of the existing Reading Room against the May 2026
  commentary, lifecycle, and permanence architecture. Determines
  what is already compatible, what is silently incompatible, and the
  short list of constitutionally dangerous things the Reading Room
  should refuse to do. Not a redesign proposal.
- **[APPARATUS_PROPAGATION_REPAIR_2026.md](APPARATUS_PROPAGATION_REPAIR_2026.md)** —
  Narrow constitutional repair flowing from the audit: apparatus
  bodies now propagate from canonical to deploy when they exist;
  unresolved markers now fail honestly with a visible diagnostic
  instead of silent inaction. Audit at
  [`reports/apparatus_audit.md`](reports/apparatus_audit.md);
  validator at [`tools/validate_apparatus.py`](tools/validate_apparatus.py).
- **[MOBILE_READING_REFINEMENT_2026.md](MOBILE_READING_REFINEMENT_2026.md)** —
  Narrow mobile reading-surface refinement following inhabitation:
  typographic controls move behind a native `<details>` disclosure on
  small screens; chrome above the first passage tightens. The text
  occupies 79–86% of the viewport on entry, up from ~73–77%. Plain
  HTML retained; no framework introduced. Re-verification at
  [`tools/test_mobile_inhabitation.py`](tools/test_mobile_inhabitation.py).

### Institutional state

- **[STATE_OF_THE_ARCHIVE_2026.md](STATE_OF_THE_ARCHIVE_2026.md)** —
  May 2026 institutional snapshot. What the archive is, structurally
  and philosophically; the corpus state in real numbers; the twelve
  constitutional principles synthesized; what is stable, experimental,
  and prohibited; known unresolved tensions; lessons learned.
  Successor stewards begin here.

- **[`reports/`](reports/)** — periodic snapshots from the maintenance
  tooling: integrity proof, validation summary, link audits.
- **[`tools/`](tools/)** — the maintenance scripts themselves. They
  expect the canonical working tree to operate; they are kept here as
  a record of what the project's maintenance discipline looks like.

The archive is built slowly, read slowly, and maintained without
hurry.
