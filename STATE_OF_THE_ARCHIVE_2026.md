# STATE_OF_THE_ARCHIVE_2026

**Date:** 2026-05-14.
**Scope:** The Digital Archive at this moment, structurally,
philosophically, and operationally.
**Purpose:** An institutional inventory. What the archive is. What
has been built. What has not. What must not yet be attempted.

This is a stewardship memorandum. It is not a roadmap. It is not a
report to anyone in particular. It is what a future steward will need
to read to understand what the archive had become by May 2026, before
making the next set of decisions.

---

## 1. What the archive is

The Digital Archive is a long-horizon stewardship project: a
byte-faithful canonical store of public-domain sacred and historical
texts, a public reading surface for those texts, and a slowly
accreting constitutional architecture that governs how the archive
may grow, what it may say, and what it must refuse to say.

It now consists of four institutional layers, in order of
foundationality:

1. **The canonical archive** — 1,132 texts in 1,196 translations
   under `01_library/library/texts/`, with their per-translation
   passages, optional apparatus, optional front matter, and stewarded
   metadata. Each text is a directory; each directory's files are
   named by purpose (`text.json`, `passages_<tr_id>.json`,
   `apparatus_<tr_id>.json`).
2. **The stewardship discipline** — the maintenance scripts,
   validation harnesses, integrity proofs, restoration documents, and
   ingestion machinery under `05_scripts/`, `02_raw_sources/`, and
   `logs/`. Read-only with respect to the corpus they audit; modifies
   it only through deliberate, named restoration passes.
3. **The constitutional architecture** — fourteen markdown documents
   at the workspace root and mirrored to `03_web_app/`, written
   between May 9 and May 14 2026, that establish the law under which
   the archive may speak. These documents define what commentary is,
   how provenance must be preserved, how citations must remain
   permanent, how migrations must be visible, and what the archive
   refuses to do.
4. **The Reading Room** — the public face at
   `03_web_app/index.html`, a single 177 KB plain-HTML file that
   renders the canonical archive for human readers and is itself
   subject to the constitutional discipline.

These four layers are not hierarchical in importance. They are
hierarchical in *load-bearing*: the canonical archive carries the
others; the stewardship discipline keeps the canonical archive
trustworthy; the constitutional architecture governs what the
archive's voice may be; the Reading Room is the surface where the
archive becomes public.

---

## 2. Corpus state, in numbers

As of 2026-05-14:

- **Canonical texts:** 1,132
- **Canonical translations:** 1,196
- **Deploy entries (including restricted):** 1,201
- **Total passages in canonical corpus:** ~2.66 million
- **Integrity proof (passage subsequence proof):** 99.88% verified
  (2,660,212 / 2,663,500 passages confirmed as contiguous substrings
  of their raw witnesses after normalization)
  - 706 texts at 100% fidelity
  - 393 texts at 99–100%
  - 67 texts at 95–99%
  - 0 texts below 95%
  - 96 texts with no raw source linked (proof skipped)
- **Front matter:** 155 texts carry structured front matter.
- **Apparatus (canonical):** 1 text. One canonical apparatus file
  exists (`apparatus_muller-part2.json`, 42 entries, 16 page
  boundaries, byte-faithfully recovered from Müller 1879).
- **Apparatus (deploy):** 1 text correctly propagates apparatus to
  the reader; 167 deploys carry orphan `[*N]` markers in passages
  whose canonical apparatus has not yet been extracted (~46,630
  orphan markers in aggregate, with Kojiki, Vishnu Purana, and Thrice
  Greatest Hermes leading the backlog).
- **URN resolver test surface:** 15 test citations, 15/15 pass with
  substantive evidence.
- **Commentary records:** 5 hand-crafted records on a single tale
  (Apannaka-jātaka, Jātaka 1). All other commentary is constitutional
  law without operational instance.

Eight major editorial restoration passes have been completed in 2026:

- Quran structural restoration (April 2026).
- Public reader refresh (early May 2026).
- Stabilization edition checkpoint (May 2026).
- Jātaka narrative restoration pass (May 2026).
- Jātaka Vol 6 acquisition — Cowell six-volume scholarly set
  completed (May 2026).
- Upaniṣads Müller Part 2 apparatus restoration (prior).
- Commentary constitutional architecture (May 14 2026).
- Apparatus propagation repair (May 14 2026).

---

## 3. Constitutional principles

The constitutional architecture is not a style guide. It is a set of
named refusals and named guarantees that together constitute what the
archive promises a reader, a citing scholar, or a future steward.

The principles, synthesized from the constitutional documents:

### 3.1 Primary text sovereignty

The primary text is the byte-faithful canonical record of what a
human translator (or community of translators) produced. It is
preserved verbatim. It is not normalized, edited, or "cleaned" except
through deliberate, named restoration passes whose intent is to
recover lost structure, not to improve the text. The integrity proof
(`passage_subsequence_proof.py`) operationalizes this: every passage
the reader sees must be present, byte-for-byte, in the raw source
that the archive ingested.

### 3.2 The seven provenance layers

Per PROVENANCE_LAYERS.md, the archive recognizes seven distinct
authorship layers and refuses to collapse them: primary text, source
apparatus, traditional commentary, modern scholarship, archive
editorial, AI, and reader-private. Every record must carry
unambiguous evidence of which layer it inhabits. The file-level layer
separation rule says the filename's implied layer and the record's
declared layer must match; mismatch is a load-time error.

### 3.3 Standoff attachment

Per COMMENTARY_ATTACHMENT_MODEL.md, all overlays (apparatus,
commentary, attachment notes) live in sibling files alongside the
passages they reference. They never modify passage records. The
anchor is a structured field — `anchors[{passage_id, anchor_text}]`,
not an inline marker the renderer infers by regex. The
apparatus_muller-part2 file is the exemplar.

### 3.4 Lifecycle, not deletion

Per COMMENTARY_LIFECYCLE.md, a record may occupy one of eight
states: drafted, provisional, verified, deprecated, superseded,
withdrawn, unresolved, orphaned. State transitions are legal, but
no state is "deleted." A withdrawn claim remains visible alongside
its withdrawal metadata. A superseded claim points to its successor.
The archive carries its own history.

### 3.5 Append-only versioning

Per COMMENTARY_VERSIONING.md, revisions to a record are sibling
records with date-suffixed identifiers (`@2027-03-10`). Older
revisions are preserved indefinitely. Diffs are not stored — the
record itself is the unit of history. Bidirectional `supersedes` /
`superseded_by` pointers keep the chain navigable.

### 3.6 Citation permanence

Per CITATION_PERMANENCE.md, citation identity is the URN, not the
URL. URNs follow the form `archive:<kind>:<text>[::trans][::id][:sub]`,
kind-aware. An append-only alias table records when an identifier is
re-keyed or retired. The resolver's contract is: a URN cited in 2026
must still resolve, or honestly refuse, in 2126. The May 2026
operational prototype (`resolve_urn.py`) demonstrates this contract
against a 15-citation test surface.

### 3.7 Migration visibility

Per COMMENTARY_MIGRATION.md, schema migrations are documented in
append-only migration manifests under
`01_library/library/migrations/`. Records may declare
`migration_policy: "frozen"` to opt out of future migrations entirely;
the resolver surfaces this on read. Pre-migration snapshots are
preserved indefinitely. The no-silent-migration rule is absolute.

### 3.8 AI quarantine

Per AI_STEWARDSHIP_POLICY.md, AI-generated material occupies
provenance Layer 6 exclusively, is quarantined by default, and
carries permanent model-identity metadata (model_id, model_date,
prompt context). It is never promoted out of Layer 6 without an
explicit named editorial action. The dual-authorship pattern — the
record's body author is the AI, the record's stewardship author is a
human — is the only legal authoring shape for Layer-6 content.

### 3.9 Honest gaps

Per COMMENTARY_REPAIR_PROTOCOLS.md, every failure mode is named.
Missing data is named. Broken anchors are named. Withdrawn claims
are visible. Apparatus markers that lack bodies surface a visible
diagnostic. The archive never fails silently. As of the May 14 2026
apparatus propagation repair, this is no longer aspirational at the
Reading Room layer.

### 3.10 The refusal index

Per INTERPRETIVE_BOUNDARIES.md and COMMENTARY_CONSTITUTION.md, the
archive maintains an explicit list of things it refuses to do. It does
not arbitrate between traditions. It does not summarize sacred texts
into didactic claims. It does not generate "the meaning of" any
passage. It does not collapse Layer 1 and Layer 6. The refusals are
constitutive of what the archive is.

### 3.11 The bare-canon guarantee

Per COMMENTARY_CONSTITUTION.md §7, a reader must be able to reach
the primary text without traversing any overlay. The passage record
they receive must be byte-equal to the integrity-proof-verified
canonical record. This guarantee is intact at the data layer; at the
rendering layer it is partial (the JavaScript renderer applies
non-destructive presentation transforms; a no-JavaScript reading mode
remains a known tension).

### 3.12 The plain-HTML resilience guarantee

Implicit in the Reading Room's design and made explicit in the May 14
2026 audit: the public face uses no SPA framework, no build pipeline,
no dependency graph. A 2046 browser will still be able to render it.
This is itself a permanence guarantee, treated as a constitutional
posture not to be lightly given up.

---

## 4. Operational infrastructure

What is built, runs, and is used:

### 4.1 Ingestion pipeline

`05_scripts/ingest.py` and many text-specific ingest scripts
(`ingest_batch_*.py`, `ingest_mahabharata.py`, etc.) translate raw
witnesses into the canonical `text.json` + `passages_*.json` shape.
Ingestion preserves source byte-faithfulness as the load-bearing
discipline; it does not auto-extract apparatus, footnotes, or
commentary (those are deliberate, named restoration passes).

### 4.2 Integrity proof

`05_scripts/passage_subsequence_proof.py` verifies that every passage
in every translation is a contiguous substring of its raw witness
(after normalization). Runs in ~minutes against the full corpus.
Current state: 99.88% verified across 2.66 M passages.

### 4.3 Validation harnesses

`validate_metadata.py`, `validate_archive_links.py`, and
`validate_apparatus.py` (added May 14 2026) each audit one axis of
archive integrity. `lint_archive.py` is the calm umbrella check that
runs the others and assembles `logs/reports/archive_health.md`.

### 4.4 Export pipeline

`05_scripts/export_reader_data.py` produces per-translation merged
JSON files for the deploy. As of May 14 2026 it propagates apparatus
arrays and apparatus_meta when canonical apparatus exists.
`05_scripts/gzip_web_data.py` pre-compresses for delivery.
`05_scripts/build_search_index.py` produces the global text-level
search index.

### 4.5 Resolver prototype

`05_scripts/resolve_urn.py` and `05_scripts/verify_permanence.py`
operationalize the URN scheme on a single tale's test surface.
Read-only with respect to canonical content. Demonstrates the
permanence contract; not a production resolver.

### 4.6 Reading Room

`03_web_app/index.html` (177 KB single file) renders the canonical
archive. Includes: text catalog, full-text search (in-text and global
index), translation compare mode, apparatus rendering, annotation
rendering, front-matter rendering, permalink generation,
localStorage-backed reading state, three CSS registers for
provenance.

### 4.7 Restoration documents

Each major editorial restoration is accompanied by a
`*_RESTORATION_*.md` or `*_REPAIR_*.md` document at the workspace
root and mirrored to `03_web_app/`. These are append-only — they
record what was done, what was found to be wrong with prior
assumptions, and what should not scale. Current examples:
QURAN_RESTORATION_2026, JATAKA_RESTORATION_2026,
JATAKA_VOL6_ACQUISITION_2026, COMMENTARY_PROTOTYPE_2026,
PERMANENCE_PROTOTYPE_2026, READING_ROOM_CONSTITUTIONAL_AUDIT_2026,
APPARATUS_PROPAGATION_REPAIR_2026.

### 4.8 Public publication

GitHub Pages serves `03_web_app/` at
`stevenfrye30.github.io/Digital-Archive/`. The deploy repo is
distinct from the canonical workspace, sized to stay under GitHub
Pages's quota by gzipping data and gitignoring the uncompressed
copies.

---

## 5. Stewardship discipline as practiced

The discipline is more important than any single artifact it
produces.

### 5.1 The measurement-artifact lesson

Both the Quran and Jātaka restoration passes opened on the assumption
that the underlying data was damaged. In both cases, the damage was
in the measurement script (`corpus_audit.py`), not the data itself.
The fix was a one-line correction in the auditor; the canonical
records required almost no change. The discipline: when an audit
reports breakage at scale, suspect the audit before suspecting the
data.

### 5.2 The named-restoration discipline

Any change to the canonical archive is accompanied by a restoration
document explaining why, what was changed, what was preserved, and
what was learned. Restoration documents are append-only; they are not
revised after the fact. They make the archive's history readable.

### 5.3 The honest-by-design discipline

Failure modes are designed-in, not omitted. The May 14 2026 apparatus
propagation repair made this concrete at the Reading Room layer: an
unresolvable `[*N]` marker now opens a visible diagnostic that names
two distinct gap shapes (canonical apparatus absent vs. apparatus
present but no entry at this index). Silent failure is treated as a
constitutional violation, not as a graceful degradation.

### 5.4 The verbatim discipline

No content is normalized, summarized, or "improved" without an
explicit named restoration pass. Markers preserved from raw witnesses
remain in passage text even when their referents are missing —
because they are honest evidence of what the raw witness contained.
Stripping them would be a form of silent suppression.

### 5.5 The slow-publication discipline

The archive is built slowly, read slowly, and maintained without
hurry. Publication checkpoints are deliberate, named events. Between
them, work happens locally; the deploy is not updated on every
internal change. Per a stewardship-side memory, iterative refinement
does not auto-commit or auto-push.

---

## 6. The restoration backlog

The archive's largest unfinished work, in scale and in candor:

### 6.1 Apparatus

167 deployed texts carry `[*N]` markers in passage text but have no
canonical apparatus. The total orphan-marker count is approximately
46,630. The leaders by marker count:

- Kojiki (Chamberlain): 2,385
- Pagan Christs (Robertson): 2,005
- The Upaniṣads (Müller 1879, anonymous deploy): 1,582
- Vishnu Purāṇa (Wilson): 1,574
- Thrice Greatest Hermes Vol I (Mead): 1,501
- Lost Books of the Bible (Platt): 1,427
- Mysticism (Underhill): 1,420
- History of Utah (Bancroft): 1,385
- Mishna (Rabbinowicz / Desola-Raphall): 1,332

Each entry represents a multi-day-to-multi-week restoration pass at
the scale of the Quran or Jātaka work. The full backlog is
decades-of-work if pursued exhaustively. The audit at
`logs/reports/apparatus_audit.md` is the navigable map.

### 6.2 Commentary

Commentary infrastructure exists as constitutional law and as five
hand-crafted records on a single tale. The data shape is settled. The
export-pipeline propagation, the renderer-side surfacing, the
lifecycle-state visualization, the alias-aware URL routing, and the
AI quarantine UI are all *designed* but not built. None of this
should be hurried; the constitutional documents specifically warn
against scaling commentary before its operational seams are tested.

### 6.3 Permanence at scale

The URN resolver works against one tale's test surface. Production
resolver behavior at the corpus scale requires an index file (the
canonical-walk approach in the prototype is not viable beyond a few
texts). Schema-version pinning is asserted in the constitution but
not yet operationally tested. Long alias chains have no enforcement
beyond a defensive depth limit.

### 6.4 Reading Room ↔ resolver bridge

The Reading Room's URL form (`?text=&p=`) does not consult the
alias table. Permalinks emitted today are not URN-recoverable
without convention-driven mapping. This is constitutionally important
but operationally not yet a crisis.

### 6.5 Bare-canon access without JavaScript

The Reading Room requires JavaScript. With JS disabled the page is an
empty shell. A no-JS reading path is a known tension recorded in
COMMENTARY_PROTOTYPE_2026.md; the simplest viable shape — server-side
pre-rendered passage HTML at static paths — has not been built.

---

## 7. The Reading Room, currently

The May 14 2026 constitutional audit established the current
position. Summarized:

- Several seams that age into the new constitutional architecture
  surprisingly well: the three-register CSS, the standoff-friendly
  apparatus data shape, the compare-mode honesty, the plain-HTML
  resilience, the front-matter schema.
- Several structural mismatches: mutable identifiers as primary keys,
  hidden provenance on annotations, single-layer interpretation,
  inline-marker assumptions, "current version only" URL semantics.
- One concrete repair landed (May 14 2026): apparatus propagation +
  honest-gap rendering for unresolved markers.
- A short prohibition list (audit §10C) names the changes the
  Reading Room must refuse: SPA migration, framework rewrite, inline
  commentary anchors, silent alias-chain following, treating
  withdrawn records as deleted, shipping apparatus markers without
  bodies.

The Reading Room is not obsolete. It is partially compatible with
the architecture beneath it. The audit's central finding stands: a
rewrite would break externally-cited URLs without yielding a single
new constitutional guarantee.

---

## 8. Known unresolved tensions

Tensions are not failures. They are seams where the architecture
acknowledges incompleteness.

1. **Constitutional law outpacing operational implementation.**
   Fourteen constitutional documents; five operational records. The
   discipline of "build the law before the engine" is intentional,
   but the resulting gap is large.
2. **The orphan-marker landscape.** ~46,630 markers visible in the
   public reader pointing at apparatus that does not yet exist
   canonically. The honest-gap rendering names this. The backlog is
   real.
3. **The reading-room/resolver bridge gap.** Permalinks remain
   URL-shaped; URNs remain machine-shaped. The relationship between
   them is convention rather than law.
4. **Bare-canon access without JavaScript.** Aspirational, unbuilt.
5. **Single-author institutional continuity.** The archive is largely
   the work of one steward. The constitutional architecture is
   designed to be readable by successors, but successor recruitment
   is not in scope.
6. **Layer-7 reader-private storage.** PUBLIC_PRIVATE_BOUNDARIES.md
   names "reader-local" as a publication degree; localStorage already
   serves this role for reading state, but a designed reader-private
   annotation layer has not been built.
7. **Restoration prioritization criteria.** No principled framework
   for ordering the 167-text apparatus backlog. The audit lists by
   marker count; that is not the same as importance.

---

## 9. What is stable, experimental, and prohibited

Stable:
- Ingestion pipeline.
- Integrity proof methodology.
- Reading Room rendering (with the May 14 repair).
- Validation harnesses (`lint_archive`, `validate_metadata`,
  `validate_apparatus`).
- Editorial restoration discipline.
- Apparatus propagation pipeline.
- Plain-HTML deploy posture.
- Local-first reading state (no telemetry, no remote logging).

Experimental:
- URN resolver (single-tale scope).
- Commentary records (five records, single tale).
- Honest-gap rendering vocabulary (apparatus only).
- Public/private publication-degree enforcement (constitutional only).

Constitutional only (designed, not built):
- Commentary lifecycle states in the reader.
- Append-only revision visualization.
- Migration manifest enforcement.
- AI quarantine UI.
- Frozen-generation handling.
- Schema-version pinning.

Prohibited (in the constitutional sense — these are refusals, not
unmet to-dos):
- Reader rewrite as an SPA.
- Mass commentary ingestion before the operational seams are tested.
- Auto-generation of apparatus, footnotes, or commentary by AI.
- Silent suppression of unresolved markers.
- Synthesis or fabrication of missing apparatus bodies.
- Layer-6 promotion to canonical without explicit named editorial
  action.
- Telemetry, analytics, or remote logging of reader behavior.
- Hidden alias-chain following at the URL layer.
- Treating withdrawn records as deleted.

---

## 10. Architectural strengths

Worth naming because they are load-bearing.

- **Standoff data discipline.** Apparatus, attachments, and
  commentary live in sibling files. Passage records are unchanged
  across all overlay layers. This is the single most important
  architectural posture; nearly every constitutional guarantee
  depends on it.
- **Verbatim ingestion with named restoration.** Source bytes are
  preserved; corrections require named, dated, documented
  restoration passes. The corpus's history is readable.
- **Plain-HTML reader.** No framework, no build pipeline. Survives
  decades of browser drift trivially.
- **Three-register CSS as constitutional intuition.** The visual
  vocabulary for provenance separation predates the constitutional
  documents that justify it.
- **Append-only documents.** Restoration documents, migration
  manifests, lifecycle documents — all preserve their history rather
  than overwriting it.
- **Integrity proof at 99.88%.** The corpus actually is what the
  archive says it is, to a measurable degree.
- **Local-first reading state.** No analytics, no fingerprinting.
- **Constitutional documents that are readable in one sitting.**
  Each is short enough to be re-read. The full constitutional corpus
  is roughly 30,000 words.

---

## 11. Institutional risks

Worth naming because they are real.

- **Bus factor of one.** The archive has one active steward. The
  constitutional documents are designed to support successor
  stewardship, but successor recruitment, training, or transition
  protocols have not been built.
- **Restoration backlog mass.** 167 texts with orphan markers, each
  representing a real restoration pass. If the archive grows the
  corpus faster than it restores existing texts, the orphan-marker
  ratio rises. The current state is honest about this but does not
  bound it.
- **Constitutional-to-operational drift.** The constitution is more
  thoroughly designed than implemented. The drift is itself a
  hazard: a steward returning to the project after a long absence
  may read the constitution and assume more is built than is.
- **GitHub dependency.** The deploy lives on GitHub Pages. The
  canonical archive lives in a local working tree backed by Git. A
  GitHub-side outage or policy change is a real, externally-imposed
  failure mode. Mitigation has not been formalized.
- **The temptation to scale before stabilizing.** Every major
  successful restoration pass invites more. The constitutional
  documents say to refuse this; future stewards will need to keep
  refusing.

---

## 12. Lessons learned

In order of weight:

1. **Measurement artifacts look like data damage.** Twice. Audits
   should be doubted before data is.
2. **Constitutional law before operational engine.** Quick
   implementation followed by retrofitted discipline produces
   architecture that the discipline cannot govern. The reverse —
   write the law, then build the engine that obeys it — is slower
   and survives longer.
3. **The CSS three-register pattern in the Reading Room was a
   constitutional intuition recorded before the constitution.**
   Pay attention to such intuitions; they are evidence of correct
   design under pre-articulate pressure.
4. **Append-only is non-negotiable.** Diffs lose context.
   Sibling-record revisions preserve the readable history.
5. **Pipeline drift between canonical schema additions and consumers
   is the most ordinary failure mode.** Every new canonical file
   shape must be paired, at the same commit, with the export-side
   learner that propagates it.
6. **Silent failure is not honest failure.** The honest-gap
   rendering pattern (May 14 2026) generalizes: every renderer
   affordance that expects a resolvable target must have a fallback
   that names the failure mode visibly.
7. **The deploy is not the archive.** The archive is in
   `01_library/`. The deploy is a presentation of it. Treating them
   as the same surface led, twice, to deploys that lied by omission
   about the canonical state. Validation tools (`validate_apparatus`,
   `validate_archive_links`) operationalize the distinction.
8. **Restoration documents pay for themselves.** Months later, the
   reasoning behind a restoration pass is only legible because it
   was written down at the time. The discipline costs a few hours
   per restoration and saves multi-day rediscovery.

---

## 13. Cautious future directions

Listed not as commitments but as candidates the constitutional
documents have made possible.

- **Apparatus restoration of one or two more high-priority texts**
  (e.g., Upaniṣads Müller Part 1; Kojiki) to validate that the
  May 14 propagation pipeline generalizes beyond Müller Part 2.
- **Commentary ingestion path** — extending `export_reader_data.py`
  to discover and propagate `commentary_*.json` files, modeled on the
  apparatus block. Should not happen before commentary records exist
  for at least one full text.
- **Resolver index** — generating a per-text URN index at export
  time, allowing the resolver to operate without walking the tree.
- **Reader URN routing** — adding `?urn=...` URL handling alongside
  the existing `?text=&p=` form, with alias-table consultation.
  Additive; non-destructive.
- **Reader-private annotation layer** — a JS-side annotation surface
  backed by localStorage, exposed only to the reader who created it,
  with explicit reader-controlled export. Implements
  PUBLIC_PRIVATE_BOUNDARIES.md §3.5.
- **Migration manifest tooling** — the manifest format is
  constitutional but tooling for producing and validating manifests
  is not yet built.
- **Bare-canon no-JS reading path** — server-side static rendering
  of canonical passage HTML at predictable paths. Constitutionally
  important; operationally unbuilt.

None of these is urgent. All are constitutionally permitted. The
discipline is to refuse to do them faster than the institution can
absorb them.

---

## 14. What this document is not

This document is not a roadmap. It is not a marketing surface. It is
not a justification for any further work. It is an institutional
snapshot — a thing the next steward (whoever they are, whenever they
arrive) can read to know what the archive was on the day this was
written.

If the archive looks different in ten years, this document remains
useful as a baseline for what changed and why. If the archive looks
the same in ten years, that is a separate finding — and one that
should be examined carefully, because some kinds of stability are
themselves a slow form of decline.

The archive is built slowly, read slowly, and maintained without
hurry. As of 2026-05-14, it is approximately what it claims to be.
