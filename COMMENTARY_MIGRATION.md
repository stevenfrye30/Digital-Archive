# Commentary Migration

*v1 · 2026-05-14 · stewardship architecture; no implementation yet.*

The archive's commentary schema will evolve. Ontologies will grow.
Anchor formats may deepen. Renderers will be rewritten. None of
these changes is unwelcome — change is how an archive stays alive —
but each must happen in a way that does not silently rewrite the
past.

This document specifies the **migration discipline** the archive
applies to commentary records. It operates under
`COMMENTARY_CONSTITUTION.md`, `COMMENTARY_VERSIONING.md` (which
governs record-level revision), and `CITATION_PERMANENCE.md` (which
constrains what migration may and may not do to identifiers).

The shortest statement of the discipline:

> **Migration is recorded. Migration is reversible where possible.
> The pre-migration state is preserved. The record's authorship is
> never lost in migration.**

---

## 1. What this document covers

A migration in this archive is a transformation applied to many
commentary records at once — typically because the schema, the
ontology, or the storage format has evolved.

Migration is distinct from:

- **Revision** (`COMMENTARY_VERSIONING.md`). Revision changes one
  record's content. Migration changes a class of records' schema.
- **Restoration** (the `*_RESTORATION_*.md` precedents). Restoration
  affects primary text or apparatus. Migration affects commentary
  layer structure.
- **Repair** (`COMMENTARY_REPAIR_PROTOCOLS.md`). Repair fixes
  broken records. Migration evolves intact ones.

Migration is a third discipline alongside these, with its own
mechanics, its own audit trail, and its own constitutional
constraints.

---

## 2. The migration manifest

Every migration is recorded in a **migration manifest** — a
canonical, append-only file that lives at:

```
01_library/library/migrations/<date>_<short-name>.md
```

The manifest is the canonical record of:

- The date of the migration.
- The steward(s) responsible.
- The schema or ontology version moved from / to.
- The records affected (by id, exhaustively listed).
- The transformation applied (in declarative or imperative form).
- The reversibility status (see §5).
- The reasons for the migration.
- A pre-migration snapshot location.

A migration that is not recorded by a manifest is **not a migration
the archive recognizes**. A change to commentary structure that
bypasses the manifest is a corruption event, not a migration, and
is handled under `COMMENTARY_REPAIR_PROTOCOLS.md`.

### 2.1 Manifest example sketch

A representative manifest header:

```markdown
# Migration 2027-04 — ontology v1 → v2

* **Date**: 2027-04-10
* **Steward**: archive:steward:steve
* **Type**: ontology version bump
* **Reversibility**: reversible (lossless)
* **Pre-migration snapshot**: logs/_archive/2027-04-ontology-v2/
* **Records affected**: 247 (full list below)

## What changed

The category "Folk Literature" is split into "Folk Narrative"
(narrative-focused tales) and "Folk Religion" (ritual / observance-
focused entries). Both categories are added to the v2 vocabulary;
the v1 "Folk Literature" is preserved as an alias.

## Per-record action

For each record carrying `categories: ["Folk Literature"]`:
* …
```

The body of the manifest documents the transformation in enough
detail that a future steward can audit it, reverse it, or apply
the same logic to a new corpus.

---

## 3. Schema-version pinning per record

Every commentary record carries its **schema version** in the
`version` field at the wrapper level (the file wrapper, not the
individual record). When a migration runs, it bumps the version
field for the records it touches.

A record that has **not** been touched by a given migration retains
its old version. The archive then contains records at multiple
schema versions simultaneously. **This is correct, not a problem.**

The renderer reads each record's declared schema version and
interprets the record accordingly. A v1 record continues to be
rendered correctly even after v2 is the current schema. The
constitutional commitment from `COMMENTARY_CONSTITUTION.md §11` is:

> Format portability. The archive's interpretive layer must be
> serializable in formats that long-survive any specific tool.

A v1 file from 2026 must remain readable in 2126 even if the
schema has reached v17 by then. **No migration is required for
correctness**; migration is performed when the steward chooses, not
because the archive's tooling demands it.

---

## 4. Frozen-generation support

A steward may decide that **some records should not migrate**, even
when a migration runs over the corpus.

Reasons:

- The record is a deliberate historical artifact (the
  COMMENTARY_PROTOTYPE_2026 prototype records, for instance).
- The record's body or anchors are calibrated to v1 semantics, and
  v2 semantics would silently change the meaning.
- The record is part of a frozen restoration document (per
  `COMMENTARY_VERSIONING.md §10`) and may not be transformed.

The discipline:

- The record carries `migration_policy: "frozen"`.
- Migration scripts **must skip** records with this flag.
- The migration manifest **must list** every frozen record it
  encountered, by id, even though it did not transform them.

The frozen records remain at their original schema version forever.
Their continued readability is the archive's responsibility (via
compatibility layers, §6).

---

## 5. Reversibility

A migration is **reversible** if running the reverse transformation
on the post-migration records produces records semantically
indistinguishable from the pre-migration records.

The archive prefers reversible migrations. When a migration is
**inherently lossy** (e.g., consolidating two categories into one
without distinguishing which records came from which), the manifest
**must declare the loss** and explain why the steward chose to
accept it.

The reversibility status is one of:

- **`reversible (lossless)`** — the transformation can be undone
  exactly.
- **`reversible (lossy)`** — the transformation can be undone in
  shape but with documented information loss.
- **`irreversible`** — the transformation cannot be undone. Used
  sparingly. Requires explicit reasoning in the manifest.

A reversible migration's manifest includes the reverse
transformation, so a future steward who wants to undo it can do so
mechanically.

---

## 6. Compatibility layers

When the schema evolves, the renderer must continue to read records
at every version that has ever shipped. This is the **compatibility
layer** discipline.

The contract:

- The renderer ships with a per-version reader for every schema
  version that has ever existed in the canonical record set.
- A renderer that drops support for an old schema version produces
  a **clear failure** — not silent misinterpretation. The
  resolver's behavior is to surface the version mismatch explicitly.
- Old-version files are not auto-rewritten. They are read as they
  stand.

This is a backward-compatibility commitment, not a forward-
compatibility one. The archive **does not** promise that records
created today can be read by tools that predate the schema. The
asymmetry is correct: new tools learn old formats; old tools cannot
learn future ones.

A practical consequence: each released renderer carries its own
version-compatibility table. A renderer from 2030 must read v1
through v2 (and whatever versions existed in 2030). A renderer from
2050 must read v1 through v5 (or whatever). The list grows.

---

## 7. The migration scope question

Migration may be:

- **Global** — applied to every record in the canonical record set
  (e.g., a v1 → v2 schema-wide upgrade).
- **Scoped** — applied to a subset (e.g., all records in a specific
  text directory, or all records of a specific layer).
- **Per-record** — applied to one record at a time (e.g., a steward
  manually updating tags on a specific record's revision).

The manifest discipline is the same for all three. A migration of
scope "one record" still produces a manifest, just a small one. The
discipline scales down.

The manifest does **not scale up infinitely**. A migration that
touches 10,000 records produces a manifest with 10,000 record ids
listed. This is correct, and is the archive's preference: full
auditability over compactness.

---

## 8. The pre-migration snapshot

Every migration produces a **pre-migration snapshot** — a
filesystem-level copy of the records as they stood before the
migration ran. The snapshot lives at:

```
logs/_archive/<date>_<short-name>/
```

The snapshot is the archive's **reversibility insurance**. If the
migration's reversibility-claim turns out to be wrong, or if a
later steward determines the migration was misjudged, the snapshot
allows literal restoration of the pre-migration state.

The snapshot is **kept indefinitely**. Snapshots may grow large
over decades; storage of historical archive states is the cost of
permanence. The discipline:

- The snapshot is not modified after the migration completes.
- The snapshot's directory name encodes the migration's date and
  short name, matching the manifest's filename stem.
- The snapshot may be moved (to cheaper storage, to a different
  partition) but never deleted.

The precedent already in place: the May 2026 phase snapshots at
`logs/_archive/2026-04-pre-stabilization/`, `2026-05-quran-restoration/`,
`2026-05-jataka-restoration/`, `2026-05-public-refresh/`, and
`2026-05-quran-restoration/`. These are the model. Migration
snapshots follow the same pattern.

---

## 9. Migration audit trail

After a migration runs, the audit trail consists of:

1. The **manifest** at `01_library/library/migrations/<date>_<short-name>.md`.
2. The **pre-migration snapshot** at `logs/_archive/<date>_<short-name>/`.
3. Per-record **stewardship_log entries** on every affected
   record, with `action: "migrated"`, `migration_id: <manifest-name>`,
   and any record-specific notes.
4. An entry in the archive-wide stewardship index at
   `STATUS.md` (or its successor) recording that the migration
   happened.

A future steward auditing a record's history sees:

- The original record (pre-migration state, accessible via snapshot).
- The migrated record (current state).
- The stewardship_log entry naming the migration.
- The migration manifest explaining the transformation.
- The pre-migration snapshot allowing literal verification.

Nothing is hidden. Nothing is irrecoverable (within reversibility
declarations).

---

## 10. The "no silent migration" rule

The strongest discipline in this document:

> **No silent migration.** A change to a commentary record's
> structure that bypasses the manifest is a corruption event,
> not a migration.

This rule is enforced by an integrity check (deferred to
implementation): a commentary record's `stewardship_log` must
contain an entry corresponding to every detected structural
change since the record's creation. A record whose current
structure does not match its claimed schema version, and whose
log shows no migration event, is **structurally inconsistent**
and is quarantined under `COMMENTARY_REPAIR_PROTOCOLS.md`.

A steward who needs to change a record's structure outside the
migration discipline (e.g., to fix a typo in a field name) must
either:

- Author a manifest, even for a single-record change. The
  discipline scales down.
- Use the revision pattern instead (a new sibling record
  superseding the old). Revision does not require a manifest, but
  is recorded in the record's `stewardship_log`.

Bypassing both is not allowed. The archive has only two legal paths
for record-structure change: migration with manifest, or revision
with stewardship log.

---

## 11. Ontology version migration

The category vocabulary (`COMMENTARY_ONTOLOGY.md §7`) is itself a
schema-like object. When the vocabulary evolves, the migration
discipline applies.

A typical ontology migration manifest header:

```markdown
# Migration 2030-06 — ontology v2 → v3

* **Type**: ontology version bump
* **Vocabulary changes**:
  * `philological` (v2) → split into `lexical` and `grammatical` (v3)
  * `liturgical` (v2) — unchanged
  * (new) `phenomenological` (v3) — added for abhidharma commentary
```

The manifest enumerates which records previously tagged
`philological` are re-tagged as `lexical`, which as `grammatical`,
and which retain `philological` (preserved as a v2 alias). The
re-tagging is the editorial substance of the migration.

A record may be re-tagged across ontology versions; the original
tagging is preserved in the record's `stewardship_log`.

---

## 12. Resolver migration

When the resolver itself changes — a new URN scheme, a richer
sub-locator format, a faster lookup mechanism — the resolver's
contract (per `CITATION_PERMANENCE.md §5.2`) must continue to be
honored.

A resolver migration:

- Does not change identifier formats already in use.
- Adds support for new formats alongside old.
- Records the change in the resolver's own version log.

A renderer that gets a new resolver must continue to resolve URNs
from any prior period. A reader's citation from 2026 must work
through a resolver-replacement in 2040.

The resolver is itself versioned and migrated under the same
discipline as the rest of the commentary infrastructure.

---

## 13. The migration cadence

The archive does not impose a migration cadence. Migrations happen
**when they are warranted**, not on a schedule. Reasons to migrate:

- A new acquisition reveals that an existing schema is insufficient.
- A category vocabulary discrepancy across stewards reaches the
  point of incoherence.
- A renderer's needs change in a way that demands a schema upgrade.
- A new authority layer becomes legitimate (e.g., institutional
  community contributions in a future federated archive).

Reasons **not** to migrate:

- Aesthetic preferences for newer field names.
- Cleanup that has no actual reader-facing benefit.
- Conformity to a fashionable schema convention.
- "Modernization."

A migration imposes cost: manifest authorship, pre-migration
snapshot, per-record stewardship_log entries, compatibility-layer
work in the renderer. The archive prefers to incur this cost only
when a real need is recorded in the manifest.

---

## 14. The migration that should not happen

Some migrations are constitutionally forbidden, even when an
implementation might find them convenient:

- A migration that changes any record's **author**. The author of
  record stays. A migration may add `revised_by` for a
  schema-level revision, but never change `author`.
- A migration that changes any record's **original body**. The
  original body is preserved across schema bumps. A v2 record that
  was migrated from a v1 record carries both the v1 body and any
  v2-formatted overlay; the original is never overwritten.
- A migration that **deletes** records. Even if a category is
  retired, the records that carried it are migrated to a successor
  category — not removed.
- A migration that **silently re-anchors** records. Anchor changes
  per record require either revision (with documented
  recategorization) or alias-table update (with documented
  identifier change). They cannot happen as a side effect of
  schema migration.
- A migration of **AI records** that elevates them to another
  layer. Per `PROVENANCE_LAYERS.md §10`, the Layer-6 → Layer-5
  transition is an editorial act per record, not a migration.

These are not engineering inconveniences. They are the constitutional
floor. A migration that proposes any of them is not a migration; it
is an attempt to bypass the constitution, and is refused.

---

## 15. Worked example: the prototype's `prototype_note` cleanup

`COMMENTARY_PROTOTYPE_2026.md §7.3` identified that the
`prototype_note` field on the May 2026 prototype records is
honest pollution that should be dropped before production.

A future migration to clean this up would proceed:

1. **Manifest authored** at `01_library/library/migrations/2027-XX_prototype-note-cleanup.md`.
2. **Pre-migration snapshot** taken at `logs/_archive/2027-XX_prototype-note-cleanup/`.
3. **Manifest declares**: type = "schema field removal", reversibility = "reversible (lossless)" — the reverse transformation re-adds the `prototype_note` field with the value from the snapshot.
4. **Per-record transformation**: for each of the 5 prototype records, the `prototype_note` field is moved from the record's body into the record's `stewardship_log` (preserved, not deleted), then removed from the record itself.
5. **Affected records listed exhaustively** in the manifest.
6. **Stewardship_log entries** added to each record:
   ```json
   {"date": "2027-XX-XX", "action": "migrated",
    "migration_id": "2027-XX_prototype-note-cleanup",
    "note": "prototype_note field moved to stewardship_log per migration manifest"}
   ```
7. **Compatibility layer**: renderers that look for `prototype_note` at the record level should consult the stewardship_log for migration-relocated values. The reader from 2026 sees the same notes; the field's storage location is the migration's concern.

This example is small but illustrates the discipline. Even a tiny
cleanup goes through the full ceremony, because the ceremony is
what makes future audits possible.

---

## 16. The migration policy on AI records

AI records (Layer 6) have a special migration discipline, drawn
from `AI_STEWARDSHIP_POLICY.md`:

- A migration **may** change the structural fields of AI records
  (anchor format, schema version) the same way it changes other
  records.
- A migration **may not** change the model identity (`provenance.author`)
  of an AI record. The original generating model is permanent.
- A migration **may not** change the body of an AI record. The
  original AI output is the AI's voice; like the apparatus
  discipline (`COMMENTARY_CONSTITUTION.md §7`), it is preserved
  verbatim.
- A migration **may** add structural metadata to an AI record (e.g.,
  a new quarantine field). It cannot remove existing AI-specific
  fields.

A migration that touches AI records must declare this in the
manifest. The AI records' counts before and after must agree.

---

## 17. Closing note

Migration is the discipline that lets the archive's commentary
infrastructure evolve without abandoning what was built earlier.
The mechanics are deliberately old-fashioned: a written manifest,
a snapshot, per-record audit trail, no silent changes.

A migration is small or large; the discipline is the same. A
century of migrations would produce a century of manifests, a
century of snapshots, a long stewardship log. That is correct.
That is what an archive looks like, viewed from far enough away.

The archive is not optimized for the steward's convenience this
year. It is optimized for the audit, by a successor, in a hundred
years. Migration discipline is one of the largest taxes the
archive pays in service of that horizon. It pays the tax willingly.
