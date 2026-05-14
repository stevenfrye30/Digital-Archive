# Public / Private Boundaries

*v1 · 2026-05-14 · stewardship architecture; no implementation yet.*

The archive's commentary infrastructure handles material at five
distinct degrees of publication. They differ by who can see them,
who can edit them, what discipline governs them, and what citation
guarantees they carry.

The constitutional commitment from `PROVENANCE_LAYERS.md` already
established the seven authorship layers. This document is about a
different dimension: not *who authored* the material, but *how
public it is*. The two dimensions are orthogonal — a Layer-5
editorial note can be public; a Layer-4 scholarly draft can be
private; a Layer-7 user annotation is always private.

The shortest statement of the discipline:

> **Each degree of publication has its own home in the file system.
> Material cannot move between degrees by accident. Every transition
> is a recorded editorial act.**

---

## 1. The five degrees

| Degree | Where it lives | Who sees it | Editable how |
|---|---|---|---|
| **Canonical / public** | `01_library/library/.../commentary_*.json` (under version control, mirrored to `03_web_app/`) | Anyone with archive access. | By authoring new records and revisions per `COMMENTARY_VERSIONING.md`. |
| **Public reader cache** | `03_web_app/data/` | Public web readers. | Generated only, not hand-edited. |
| **Working / draft** | `working/` (gitignored), local-only | The steward authoring. | Freely; not citable. |
| **Experimental** | `01_library/library/.../commentary_*.experimental.json` (under version control, marked) | Anyone, with explicit "experimental" labels. | Per the experimental discipline (§6). |
| **Reader-local / private** | The reader's own device | Only the reader. | By the reader. |

Each degree has its own discipline. The boundaries between them are
not technical conveniences but constitutional commitments.

---

## 2. Canonical / public — the archive's authoritative state

The canonical commentary records live in
`01_library/library/texts/<tradition>/<text-dir>/commentary_*.json`,
beside the canonical primary-text and apparatus files.

Properties:

- **Authoritative.** This is what the archive stewards as its
  formal commentary record.
- **Version-controlled.** Every change is in git history.
- **Citable.** Records here have URNs that the resolver guarantees
  forever (per `CITATION_PERMANENCE.md`).
- **Verifiable.** The commentary integrity proof
  (`COMMENTARY_REPAIR_PROTOCOLS.md §15`) covers these records.
- **Lifecycle-governed.** Records transition through
  `COMMENTARY_LIFECYCLE.md` states.
- **Mirrored to the public reader cache** by
  `export_reader_data.py` (or its successor).

This is the **default** degree. A commentary record's normal home
is the canonical record set. Other degrees are exceptions for
specific purposes.

---

## 3. Working / draft — the steward's private workshop

A steward composing a new record typically writes it as a draft
first: the body is still being refined; the anchors are being
checked; the categorization is being considered.

The discipline:

- Drafts live in `working/` at the project root, **gitignored**.
- Drafts are **not citable**. They have no URN. The resolver does
  not see them.
- Drafts may be freely edited, renamed, deleted by the author.
- A draft becomes a real commentary record by being **moved** from
  `working/` to the canonical commentary file, with a proper id,
  stewardship_log, and provenance. The move is the act of
  publication (`drafted → provisional` per
  `COMMENTARY_LIFECYCLE.md §3.1`).

The constitutional commitment that the archive does **not preserve
drafts as drafts**:

A draft that is moved into canonical state acquires the
`stewardship_log[0]` entry recording its creation as a public
record on that date. The earlier draft history is not preserved
in the canonical record. If the steward wishes to preserve the
drafting history (because the drafts themselves were intellectually
substantive), they may author a Layer-5 editorial note recording
the drafting process — but the working files themselves are not
archived.

This is a different discipline from a research notebook. The
archive's preference is that **the canonical record stands for
itself**, and that drafts are scaffolding to be removed when the
building is complete. A steward who wants to publish their
drafting process makes a deliberate, named editorial decision to
do so.

### 3.1 Why `working/` is gitignored

A drafting file ending up in git history is a low-cost mistake but
worth preventing. The `.gitignore` rule for `working/` is part of
the archive's discipline. A steward whose `working/` accidentally
gets staged should `git restore --staged` the change.

Drafts may include speculative writing, half-formed thoughts,
private notes-to-self, embarrassing first attempts. None of these
should appear in the public record without the steward's deliberate
publication action.

---

## 4. Experimental — public but explicitly tentative

Between draft and canonical lies a third degree: **experimental**
records. These are records the steward wants to make visible — for
collaborative review, for testing the constitutional architecture
against a new pattern, for soliciting feedback from other stewards
— but does not yet endorse as canonical.

The prototype records from `COMMENTARY_PROTOTYPE_2026.md` are an
example: they exist in the canonical record set
(`01_library/library/.../commentary_*.json`), but every record
carries `provenance.prototype_note` flagging it as experimental.

The discipline:

- Experimental records live in files named with `.experimental`
  in the stem, **next to** canonical commentary files:
  `commentary_<layer>.experimental.json`.
- The experimental file's wrapper declares
  `"experimental": true` at the top level.
- Records inside are flagged with
  `"lifecycle_state": "experimental"` (a state in addition to the
  ones in `COMMENTARY_LIFECYCLE.md §1`; experimental is a
  pre-provisional state that does **not** participate in the normal
  lifecycle transitions).
- The renderer displays experimental records with a clear
  "experimental" marker — distinct from provisional, distinct from
  verified.
- Experimental records **are citable**. The URN scheme works the
  same. But the reader is told, at every display, that the record
  is experimental.

### 4.1 Experimental records and the prototype

The May 2026 commentary prototype records placed in
`01_library/library/texts/sacred/buddhist/jataka-chalmers-vol1/`
should, under this document, be retroactively labeled
**experimental**. Specifically:

- The files should be renamed:
  - `commentary_editorial.json` → `commentary_editorial.experimental.json`
  - `commentary_scholarship.json` → `commentary_scholarship.experimental.json`
  - `attachments_traditional.json` → `attachments_traditional.experimental.json`
  - `commentary_ai.json` → `commentary_ai.experimental.json`
- The wrapper should declare `"experimental": true`.
- Each record's `lifecycle_state` should be set to `"experimental"`.

This retroactive labeling is a **migration** (per
`COMMENTARY_MIGRATION.md`) and is deferred to implementation. The
prototype records' constitutional status — "demonstration content,
not endorsed claims" — is more honestly recorded under the
experimental label than under the prototype_note field added
inline.

When the prototype records are eventually superseded by real
production records, the experimental records remain (per the
no-deletion principle of `COMMENTARY_LIFECYCLE.md §5`), marked
superseded.

### 4.2 The transition from experimental to provisional

An experimental record may be promoted to provisional (the normal
publication state) when the steward decides the record stands as a
real claim, not as a structural demonstration. The transition is
an editorial act recorded in the stewardship_log:

```json
{"date": "...", "action": "promoted-from-experimental",
 "by": "...", "state_after": "provisional",
 "note": "Steward decides this record is now an endorsed claim."}
```

The record's body and anchors carry forward unchanged. The
experimental flag is removed; the file is renamed (per the §4
naming convention). The promotion is itself a migration event.

---

## 5. Public reader cache — generated, not authored

The `03_web_app/data/` directory holds the public web reader's
artifacts: per-translation merged JSON, the index, the integrity
report. These are **generated** by `export_reader_data.py` from the
canonical record set. They are not authored.

The discipline:

- The reader cache is **never hand-edited**. Any change must come
  from re-running the export tool.
- The reader cache is **derivative**. It contains nothing that is
  not in the canonical record set, transformed for the reader's
  convenience.
- Citations to records resolve through the **canonical** record
  set, not through the reader cache. The reader cache may serve
  faster, but it is not authoritative.
- Restoration documents and migration manifests note that the
  reader cache must be refreshed after their work; the cache is
  always behind the canonical record set until refreshed.

This is the discipline that makes the archive resilient to
public-reader changes. A new public reader (a different web UI,
a different export format, a different rendering engine) can be
built from the canonical record set without disturbing the
canonical record set. The reader cache is, structurally, a
**rendering**, not a record.

A future commentary infrastructure will export commentary records
into the reader cache as well — likely as
`03_web_app/data/<text-id>_commentary.json` per translation. The
discipline is the same: generated, not authored; derivative,
never authoritative.

---

## 6. Reader-local / private — outside the archive

A reader using the archive may keep private annotations on
passages — their own marginalia. These are **outside the canonical
record set entirely**.

The discipline from `PROVENANCE_LAYERS.md §8`:

- The archive does not store private annotations on its servers.
- The renderer surfaces private annotations on the reader's own
  device, from the reader's own storage.
- Private annotations carry `local:annotation:<id>` URNs,
  explicitly outside the `archive:` namespace.
- The archive's citation permanence guarantees **do not apply**
  to private annotations.
- A reader may export their private annotations to take them
  elsewhere; the format is their property.

The constitutional commitment is that **the archive does not see
the reader's notes**. If the public reader implementation needs to
support private annotation, it does so by reading and writing the
reader's local storage; the archive's servers do not receive the
annotations.

A reader who wants their notes to become public — to be archived,
cited by others — takes an explicit action: they author a Layer-5
editorial note in the canonical record set, citing their previous
private annotation as the basis. This is a publication act with
named authorship, not a privacy violation by the renderer.

---

## 7. The transitions between degrees

The legal transitions between degrees:

| From | To | The act |
|---|---|---|
| working draft | canonical | Publication: move from `working/` to canonical file, with full record schema (id, provenance, anchors, stewardship_log). |
| canonical | experimental | Demotion (rare): the steward decides a previously-endorsed record was premature. A new experimental file is created with the record moved into it; the old canonical state is preserved in the migration snapshot. |
| experimental | canonical | Promotion (per §4.2). |
| reader-local | canonical | Author a new canonical record citing the local one as basis. The reader's local note continues to exist locally. |
| canonical | reader-local | **Not a transition.** A reader who exports a public record to their own local storage has a copy of it for their own reference, but the canonical record persists in its place. |

The transitions that are **forbidden**:

- canonical → working. Once a record is canonical, demoting it to a
  private draft state is forbidden. Canonical records are public;
  the public record cannot be hidden by reverting it to draft.
  (Withdrawal is the proper editorial act when a canonical record
  needs to be retracted; see `COMMENTARY_LIFECYCLE.md §3.6`.)
- canonical → reader-local. The archive does not "move" a public
  record into a reader's private storage; the reader copies, not
  moves.
- reader-local → reader-cache. A reader's private annotations do
  not enter the public reader cache. The reader cache only
  reflects the canonical record set.
- reader-local → other-reader-local. The archive does not transmit
  one reader's annotations to another. Annotation sharing, if it
  ever exists, is implemented as an explicit publication step
  (annotation → canonical via author publication).

These forbidden transitions are constitutional, not technical
inconveniences.

---

## 8. The accidental-collapse case

The most dangerous failure mode of the boundary system is
**accidental collapse**: material from one degree silently appearing
in another.

Examples of what must not happen:

- A working draft gets accidentally git-added and pushed; private
  speculation appears in the public record.
- A reader's private annotation gets captured by analytics or
  telemetry and stored on the archive's servers.
- An experimental record's "experimental" flag is dropped during a
  migration; the record appears to be canonical.
- The reader cache is hand-edited; the cache and the canonical
  record set diverge.

For each, the defense is the same: **technical mechanisms enforce
the boundaries; integrity proofs detect violations.**

### 8.1 Working drafts

- `.gitignore` excludes `working/`.
- A pre-commit hook (deferred to implementation) refuses to commit
  files containing the substring `WORKING-DRAFT-DO-NOT-COMMIT` (a
  marker the steward inserts in active drafts).
- The commentary integrity proof scans for records in canonical
  files whose stewardship_log shows no `created` event but whose
  body suggests a draft origin (this is heuristic, not absolute).

### 8.2 Reader privacy

- The public reader does not send analytics, does not phone home,
  does not capture reader behavior.
- The renderer's local-storage usage for annotations is documented
  publicly; readers can audit it.
- The archive's servers do not receive any per-reader data beyond
  unavoidable server logs, which are themselves stewarded under
  archive privacy norms.

### 8.3 Experimental records

- The integrity proof verifies that every record in an
  `*.experimental.json` file carries
  `lifecycle_state: "experimental"`, and that no record in a
  non-`.experimental` file carries it.
- A migration that touches experimental files is flagged for
  steward review; experimental status is not a routine attribute.

### 8.4 Reader-cache divergence

- The reader cache is regenerated from canonical state. A
  divergence is a `gzip_web_data.py` failure or a stale build —
  not a legitimate editorial state.
- The cache files carry a `generated` timestamp; the canonical
  state carries a `last-modified` notion through git. The two
  should agree within a sensible window after each refresh; a
  long divergence is a maintenance failure surfaced by
  `STATUS.md` (the precedent already in place; see the May 2026
  public-refresh restoration document for an example of detecting
  and repairing this).

---

## 9. The audit question: who saw what, when

A possible future concern: a reader in 2126 wants to know which
records were public when. The archive's discipline supports this:

- Git history records every change to canonical files.
- Migration manifests record schema and structural changes.
- Restoration documents record content changes.
- Stewardship logs record per-record lifecycle changes.

Together these enable a reconstruction of *what the public record
looked like at any given prior date*. The reconstruction is not
trivial — it requires walking git history and consulting the
manifests — but it is mechanically possible.

The archive does **not** promise instant point-in-time queries
("show me the canonical record set as of 2027-04-01"). The
mechanism exists; the convenience is implementation-deferred.

Experimental records, working drafts, and reader-local annotations
are **not** included in the historical reconstruction. Working
drafts are gitignored; reader annotations are reader-controlled;
experimental records have their own visible state markers.

---

## 10. The institutional analog

The five degrees described here have institutional analogs in
older scholarly traditions:

- **Working draft** = a scholar's notebooks, never published, often
  destroyed at career's end. Some archives preserve notebooks;
  most do not, and the scholar's intention shapes that decision.
- **Experimental** = a working paper, a preprint, a colloquium
  draft. Visible but explicitly tentative. The convention of
  preprint servers (arXiv, SSRN) is in this register.
- **Canonical** = a peer-reviewed publication, the definitive
  archival form of a scholar's claim.
- **Reader-cache** = the published journal issue or printed book.
  Derivative of the canonical record but the actual artifact most
  readers encounter.
- **Reader-local** = the reader's own marginalia in their copy of
  the book. Private to the reader; potentially valuable to a
  later historian but generally not shared.

The archive's boundary discipline rediscovers these distinctions.
The names are new; the discipline is centuries old.

---

## 11. The federation question

A future archive may federate with other archives — taking in
their commentary, exposing its own commentary to theirs. The
boundary system must be ready.

The principle:

- Each archive maintains its own canonical record set with its own
  citation namespace.
- Citations across archives use the source archive's URN, never
  silently re-keyed.
- Records ingested from another archive are recorded as such (the
  source archive named in provenance); they retain their source
  attribution.

A federated record is, structurally, a Layer-3 traditional-commentary
bridge to another archive's canonical record set. The bridge
discipline (`COMMENTARY_ATTACHMENT_MODEL.md §11` and
`COMMENTARY_PROTOTYPE_2026.md §5`) generalizes naturally.

The constitutional refusal: **no archive may silently absorb
another archive's records into its own canonical record set.** The
two record sets remain distinct; the federation is the
relationship between them. This is how the Talmud, the Glossa
Ordinaria, the Pāli tradition all managed multi-source corpora
historically. The instinct is preserved here.

Federation is a future concern. The boundary discipline today is
sufficient if it is treated with care; future federation will
extend it, not replace it.

---

## 12. Closing note

The boundary discipline is the part of the commentary architecture
most likely to be tested by everyday stewardship. Most working
days will involve drafts that get refined into canonical records,
experimental work that gets promoted or retired, public renderings
that get refreshed.

The constitutional commitments — that boundaries are honored, that
transitions are recorded, that accidents are detected — exist so
that the archive's everyday work does not gradually erode the
distinctions between what is authored, what is published, what is
experimental, and what is private.

A reader of the canonical record set in 2126 should be able to
trust that what they are reading was deliberately published as a
canonical claim. A reader of the experimental file in 2126 should
be able to see that the work was tentative when authored. A
steward whose working drafts from 2026 never reached the canonical
record set should not find them surfacing in the archive in 2126.

These are small commitments. Together they preserve the integrity
of authorship itself.
