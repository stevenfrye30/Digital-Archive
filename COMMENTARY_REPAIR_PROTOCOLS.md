# Commentary Repair Protocols

*v1 · 2026-05-14 · stewardship architecture; no implementation yet.*

Things will break. An archive of intended century-long lifespan
must plan for that.

This document defines how the archive's commentary infrastructure
handles breakage: orphaned anchors, broken references, missing
commentary corpora, contradictory metadata, duplicate records,
damaged files, partial ingestion failures. The constitutional
commitment that frames this work, from
`COMMENTARY_CONSTITUTION.md §10`:

> **The archive must fail honestly.**

A broken citation that displays a clear, structured failure is not
a bug. A broken citation that silently returns wrong content is.
The discipline is to make the first the normal case, and to refuse
the second on principle.

This document operates under all four prior commentary documents
and reads particularly closely with `COMMENTARY_LIFECYCLE.md`
(orphaned and unresolved states) and `CITATION_PERMANENCE.md` (the
resolver's behavior on missing targets).

---

## 1. The taxonomy of failures

Breakages in the commentary infrastructure fall into a small
number of named categories. Each has a detection rule, a quarantine
behavior, and a repair workflow.

| Category | What it is | Triage urgency |
|---|---|---|
| **Broken anchor** | A record's anchor cites a target id that does not exist. | Moderate; ongoing repair. |
| **Orphan record** | A record was created targeting an object that was later removed. | Low; lifecycle state already handles it. |
| **Stale alias** | An alias-table entry redirects to a target that no longer exists. | Moderate; cascading risk. |
| **Layer-collapse violation** | A record's `provenance.layer` disagrees with the file it lives in. | High; constitutional violation. |
| **Duplicate id** | Two different records share the same id. | High; citation ambiguity. |
| **Damaged file** | A canonical commentary file fails to parse. | High; data loss risk. |
| **Contradictory metadata** | Internal fields disagree (e.g., `provenance.date` after `stewardship_log[0].date`). | Moderate; honesty failure. |
| **Frozen-record migration** | A migration touched a `migration_policy: "frozen"` record. | High; constitutional violation. |
| **Missing stewardship_log** | A record lacks any log entry. | Moderate; provenance failure. |
| **Missing bridge target** | A Layer-3 bridge points at a not-yet-acquired text. | Routine; the design supports this. |
| **AI label loss** | A Layer-6 record lacks model identity or generation date. | High; quarantine failure. |
| **Schema-version mismatch** | A record's content does not match its declared schema version. | High; migration discipline violation. |

The remainder of this document treats each in detail.

---

## 2. Universal repair principles

Before the case-by-case, four principles apply to every repair:

### 2.1 Quarantine, not delete

A damaged record is **quarantined**, not removed. Quarantine is a
state-like flag that marks the record as "requires repair." The
record remains in the canonical record set. The renderer surfaces
the quarantine state visibly.

Quarantine is not a lifecycle state from `COMMENTARY_LIFECYCLE.md`
— it is a **diagnostic condition** applied alongside the
lifecycle state. A record may be `verified` AND `quarantined:
broken-anchor`. The two coexist.

### 2.2 Record the breakage

Every quarantine event produces a `stewardship_log` entry:

```json
{
  "date": "2027-09-18",
  "action": "quarantined",
  "by": "archive:steward:steve",
  "quarantine_reason": "broken-anchor",
  "details": "Anchor archive:passage:foo::bar::99.9 does not resolve in current corpus."
}
```

The quarantine is itself part of the historical record. When the
record is later repaired, the repair is also logged, but the
original quarantine event stays in the log forever.

### 2.3 Repair is an editorial act

A repair is performed by a named steward at a recorded date with
explicit reasoning. The repair is **not** an automated cleanup
sweep; the archive resists those (per
`INTERPRETIVE_BOUNDARIES.md §4.3`).

A repair may:

- Update a record's anchor to a current target (if the target was
  re-keyed).
- Move a record between files (if the layer encoding was wrong).
- Add a missing `stewardship_log` entry (when constructing history
  from external evidence).
- Author a new record that supersedes a corrupted one.

A repair may **not**:

- Modify a record's `id`, `author`, `original date`, or `body`.
- Remove a quarantine event from a stewardship_log.
- Delete a damaged record.

### 2.4 The archive prefers the honest gap

When a record cannot be repaired (target genuinely lost, body
genuinely damaged beyond recovery), the gap is recorded honestly.
The damaged record is preserved as it stands, quarantined, with
a stewardship log explaining the unrecoverable state. The reader
sees the failure, not a guess at what the record might have meant.

---

## 3. Broken anchor

### 3.1 Detection

A record's anchor names a target id (passage, tale, commentary,
entity, etc.). The resolver attempts resolution. If the resolution
returns "no such target" (and the alias table does not redirect),
the anchor is broken.

The detection is performed by the commentary integrity proof (a
deferred check, analog to `passage_subsequence_proof.py` for primary
text). The check is run periodically; broken anchors detected since
the last run are reported.

### 3.2 Likely causes

- A restoration changed the target's id without updating the alias
  table (a stewardship failure — should be rare).
- The target was a typo in the original record (caught late).
- The targeted commentary record was withdrawn / orphaned (the
  resolver still resolves to a marker, so this is **not** a broken
  anchor; it is normal lifecycle behavior).
- The target's file was damaged or moved out of the canonical set.

### 3.3 Quarantine behavior

The record acquires `quarantine_reason: "broken-anchor"` in a new
stewardship_log entry. The record's anchor list is **not modified**
— the broken anchor is preserved as evidence of what was originally
intended.

The renderer displays the record with a clear "anchor does not
resolve" notice, naming the broken anchor URN.

### 3.4 Repair workflow

The steward investigates the breakage. Possible repairs:

1. **The target was re-keyed and the alias table missed it.** Fix:
   add the alias to the alias table. The record's anchor now
   resolves through the alias. The repair entry in the
   stewardship_log records this. **No record modification needed.**

2. **The original anchor was a typo.** Fix: author a revision of
   the record with the corrected anchor (per
   `COMMENTARY_VERSIONING.md`). The original record is preserved
   with its typo'd anchor; the revision carries the correct anchor.

3. **The target was deliberately removed and no alias is
   appropriate.** Fix: transition the record to `orphaned` state
   (per `COMMENTARY_LIFECYCLE.md §3.8`). The orphan condition
   replaces the quarantine. The record continues to display with
   the orphan marker; the steward's stewardship_log entry names
   the upstream restoration responsible.

4. **The cause cannot be determined.** Fix: leave the record
   quarantined. The honest gap is the archive's preferred state
   over a guess.

---

## 4. Stale alias

### 4.1 Detection

An alias-table entry redirects URN A → URN B. If URN B no longer
resolves, the alias is **stale**.

Stale aliases cascade: a citation in 2026 of URN A finds the alias
to B, attempts to resolve B, and discovers B is also broken. The
chain can be long over decades.

### 4.2 Quarantine behavior

The alias-table entry is flagged. The alias-table is itself a
canonical record-set object (per `CITATION_PERMANENCE.md §4.2`); a
stale entry is quarantined in the same way as a stale record.

### 4.3 Repair workflow

The steward investigates whether B was further re-keyed:

- **B was re-keyed to C.** Fix: update the alias entry A → C (NOT
  A → B → C through chained resolution; the archive prefers
  single-hop aliases for resolver efficiency and reader clarity).
  The original A → B entry is preserved in the alias table's own
  history; the active entry is A → C.

- **B was orphaned with no successor.** Fix: alias entry A → "retired";
  the resolver now returns a structured "this URN was retired on
  [date]" for any citation of A.

- **B's location is uncertain.** Fix: quarantine the alias entry
  and document. The gap is recorded.

The alias table follows the same append-only discipline as
stewardship logs: old entries are preserved as historical records
even after they are superseded.

---

## 5. Layer-collapse violation

### 5.1 Detection

A commentary file declares its layer at the wrapper level
(`"layer": "editorial"`). Each record in the file declares its
layer in its `provenance.layer` field. The two must agree.

Detection is at load time (per `COMMENTARY_PROTOTYPE_2026.md §3`,
which already implements this check in the prototype renderer).

### 5.2 Why it is high-urgency

The non-collapse rule (`PROVENANCE_LAYERS.md §9`) is constitutional:
*"Both encodings agree. The directory-or-file encoding is the
canonical one for resolving ambiguity."* A violation is not a minor
inconsistency; it is a structural constitutional breach that may
indicate either:

- A bug in stewardship tooling.
- A copy-paste error during record authoring.
- An attempt to move a record between layers without the proper
  editorial discipline.
- An adversarial modification.

### 5.3 Quarantine behavior

The renderer **refuses to load** the file containing the violation,
per the precedent set by the prototype. The reader sees a load
failure for that file; other files continue to load normally.

This is one of the few places the archive prefers a hard failure
over a degraded reading. Layer integrity is too important to render
through.

### 5.4 Repair workflow

The steward investigates. Possible repairs:

1. **The record is in the wrong file.** Fix: move the record to
   the file matching its `provenance.layer`. The move is logged
   in stewardship_log: `action: "relocated-for-layer-correction"`.
2. **The record's `provenance.layer` is wrong.** Fix: this should
   be very rare. If the record genuinely belongs to a different
   layer than originally tagged, the proper repair is to author a
   new record in the correct layer that supersedes the
   miscategorized one; the original record's `provenance.layer`
   is preserved as historical record (because constitutionally,
   the original cannot be modified).

The second repair is unusual but real: a steward who, in retrospect,
realizes a Layer-5 editorial note should really have been a Layer-4
scholarship attribution (because the steward was unconsciously
channeling someone else's view) makes a new Layer-4 record citing
the prior Layer-5 record's content. Both stand.

---

## 6. Duplicate id

### 6.1 Detection

The commentary integrity proof scans for duplicate record ids
across all commentary files. Two records with the same id is a
citation-ambiguity violation: a citation to that id cannot
deterministically resolve.

### 6.2 Quarantine behavior

Both records are flagged. The resolver's default response to a
citation of the duplicate id is "ambiguous identifier; see
[both candidates]." This is **deterministically a failure**, per
the resolver's contract (`CITATION_PERMANENCE.md §5.2`).

### 6.3 Repair workflow

The steward determines which record was the original. Typically the
record with the earlier `provenance.date` is the original; the
later one is a duplicate that should have had a different id.

Repair:

1. The later record's id is changed by appending a discriminator
   (typically `-2`, `-3`, or a date suffix). This is a rare case
   where an id changes; it is permitted **only** because the id
   was created in error and was never legitimately citable.
2. The id-change is recorded in the alias table: the old (collision)
   id maps to "ambiguous; see [both records]" — a permanent
   record that the collision happened.
3. Both records continue to exist with their distinct ids.

If both records were authored on the same date and the collision is
genuinely accidental (e.g., a steward forgot a record existed and
re-authored a similar one), the second record is preserved as a
revision-sibling — but **not** as a revision of the first
(because the second steward did not intend a revision; they
intended an independent record).

---

## 7. Damaged commentary file

### 7.1 Detection

A canonical commentary file fails to parse as valid JSON. The
renderer reports the parse error; the resolver cannot resolve any
URN that targets a record in the damaged file.

### 7.2 Causes

- Disk corruption.
- Mid-write process interruption (resolved by atomic-write
  discipline at the storage layer).
- Editorial error: a steward broke the JSON by hand-editing.
- Schema-migration tooling produced invalid output.

### 7.3 Quarantine behavior

The renderer skips the damaged file with a clear error log. URNs
targeting records in the file return a structured "file damaged;
see repair log" response from the resolver.

### 7.4 Repair workflow

1. **The pre-migration snapshot or git history holds an intact
   copy.** Fix: restore from the snapshot. The corruption event is
   logged at the archive level; per-record stewardship_logs are
   updated if necessary.
2. **No intact copy exists.** This is the rare disaster case. The
   damaged file is preserved as evidence (renamed to
   `commentary_<layer>.DAMAGED.json`), and a new file is
   constructed by manually parsing what can be recovered. Records
   whose bodies are unrecoverable are preserved in
   `lifecycle_state: "withdrawn"` with the stewardship_log
   recording: "body unrecoverable from damaged file; preserved as
   evidence at .DAMAGED.json."

The archive does not pretend a recovery is clean when it is not.
A damaged file is permanent evidence of the breakage; the
repair record is permanent evidence of the recovery.

---

## 8. Contradictory metadata

### 8.1 Detection

The commentary integrity proof checks internal consistencies:

- A record's `provenance.date` must be ≤ all `stewardship_log[i].date`
  values.
- A record's `lifecycle_state` must match the state implied by its
  latest stewardship_log entry's `state_after`.
- A record's `supersedes` target must itself have a `superseded_by`
  pointing back.
- A record's `provenance.layer` must match its file's `layer`
  (covered in §5).
- A revision record's id must follow the `<base-id>@<date>` pattern.

Violations are contradictions.

### 8.2 Quarantine behavior

The record carries `quarantine_reason: "contradictory-metadata"`
with the specific contradiction recorded. The renderer displays
the record with the contradiction note.

### 8.3 Repair workflow

Each contradiction has its own repair. Generally:

- The repair updates the inconsistent field to match the canonical
  source of truth.
- The canonical source of truth, when in doubt, is the **earliest
  recorded value**. The archive prefers what was first claimed,
  not what was most recently claimed.
- The discrepancy is recorded in stewardship_log: `action:
  "metadata-corrected"`, naming the field, the prior and new
  values, and the reasoning.

Contradictions caused by automated tooling failure (rather than
human stewardship) are flagged for tooling review in the
manifest as well as the record.

---

## 9. Frozen-record violation

### 9.1 Detection

A migration changed the structural fields of a record marked
`migration_policy: "frozen"`. Detected by comparing pre- and
post-migration snapshots of frozen records.

### 9.2 High urgency

This is a constitutional violation, per
`COMMENTARY_MIGRATION.md §4`. A frozen record is deliberately
preserved at its declared schema version; modifying it bypasses
the steward's explicit preservation decision.

### 9.3 Repair workflow

1. **Restore the frozen record's pre-migration state** from the
   snapshot.
2. **Audit the migration manifest** to determine why the frozen
   flag was ignored. Likely causes: tooling bug, manifest oversight,
   or the steward made a deliberate decision to override the freeze
   that was not properly recorded.
3. **If the override was deliberate**, the proper recording is a
   manifest amendment that explicitly names the previously-frozen
   record and the reason for unfreezing. This is itself a
   high-significance event.
4. **If the override was accidental**, the migration is
   partially reverted (only for the frozen records), and the
   tooling is fixed.

The archive treats this case with the gravity due a
constitutional breach.

---

## 10. Missing stewardship_log

### 10.1 Detection

A record exists with no `stewardship_log[0].action: "created"` entry.

### 10.2 Likely causes

- Manual record authorship that omitted the log.
- Tooling that produced records without log entries.
- A record imported from an external source where the log was not
  reconstructed.

### 10.3 Repair workflow

1. **Reconstruct the log entry from available evidence.** The
   record's `provenance.date` and `provenance.author` are usually
   enough to author a retrospective `created` entry. The entry is
   marked: `note: "log entry reconstructed [date]; original log
   missing from record-as-found."`
2. **If no evidence exists for the creation event**, the steward
   authors a "first-recorded" entry on the date the gap was
   discovered: `action: "first-recorded"`, `note: "record was
   found without a creation log; reconstructed minimal log here."`

The reconstruction is itself a stewardship act, recorded
faithfully.

---

## 11. Missing bridge target

### 11.1 The "normal" case

A Layer-3 bridge record (`COMMENTARY_PROTOTYPE_2026.md §5`)
intentionally points at a target that does not yet exist (the
not-yet-acquired traditional commentary).

This is **not a breakage**. The record is marked `unresolved` per
`COMMENTARY_LIFECYCLE.md §3.7`, and the renderer displays the gap
honestly.

### 11.2 When it becomes a repair

A bridge record is in repair territory when:

- The target was expected to be acquired but the acquisition
  effort was abandoned. The bridge should be re-marked from
  `unresolved` to a stewardship_log note explaining the
  abandonment.
- The acquisition succeeded but the bridge's target URN no longer
  matches the acquired text's structure. The bridge needs a
  revision pointing at the actual ingested URN.

### 11.3 Repair workflow

Authorship of a revision (per `COMMENTARY_VERSIONING.md`) with
the corrected target. Both records preserved.

---

## 12. AI label loss

### 12.1 Detection

A Layer-6 record is missing one or more of:

- `provenance.author` set to a model identity (`archive:ai:<model>`)
- `provenance.source.model_id`
- `provenance.source.model_date`
- `provenance.source.prompt_context` (or an explicit "not
  recorded" marker)
- `quarantine_flag: true`

### 12.2 Why high urgency

Per `INTERPRETIVE_BOUNDARIES.md §4.1` and `AI_STEWARDSHIP_POLICY.md`,
AI records must carry full identity at all times. A record missing
identity has lost its quarantine; a reader cannot tell it is AI
output.

### 12.3 Quarantine behavior

The record is double-quarantined: both `quarantine_reason:
"ai-label-loss"` and a renderer-side override that forces the
record to display with explicit "**AI ORIGIN UNCERTAIN**" warning,
even if the layer encoding still places it in Layer 6.

### 12.4 Repair workflow

1. **Reconstruct identity from evidence.** If the model identity
   can be recovered from git history, generation logs, or the
   author's records, restore the fields.
2. **If identity cannot be reconstructed**, the record is
   transitioned to `lifecycle_state: "withdrawn"` with the
   stewardship_log explaining: *"AI provenance lost; record
   preserved as historical artifact, withdrawn from active use."*
   The body remains; the record is no longer eligible for any
   reader-facing surfacing other than a withdrawal notice.

The archive refuses to surface unattributed AI content under any
circumstances. The withdrawal is the archive's defense of its
own quarantine discipline.

---

## 13. Schema-version mismatch

### 13.1 Detection

A record's structure does not match the schema implied by its
declared version. For example: a record declares
`schema_version: 1` but contains fields introduced in v2.

### 13.2 Likely causes

- A migration touched the record without updating its declared
  version.
- A manual edit added new-version fields to an old-version record
  without going through migration discipline.
- Tooling bug.

### 13.3 Quarantine and repair

The record is quarantined. The repair determines what happened:

- **A migration should have updated the version.** Fix: update the
  declared version, log the correction, audit the migration
  manifest for similar misses.
- **A manual edit was made outside discipline.** Fix: either
  formalize the edit as a one-record migration (with manifest and
  snapshot, per `COMMENTARY_MIGRATION.md §10`), or revert the edit
  and author the change properly as a revision.

This case is the archive's primary defense against "silent
migration" (the rule in `COMMENTARY_MIGRATION.md §10`).

---

## 14. The repair manifest

For repairs that affect more than a small number of records (e.g.,
fixing a class of broken anchors), the steward authors a **repair
manifest** alongside the standard stewardship_log entries on each
affected record. The manifest lives at:

```
01_library/library/repairs/<date>_<short-name>.md
```

Its format parallels the migration manifest
(`COMMENTARY_MIGRATION.md §2.1`), with sections:

- Date and steward.
- Type of repair (broken-anchor sweep, layer correction, etc.).
- Records affected.
- Detection that surfaced the issue (the integrity proof's report).
- The repair applied.
- Reversibility status.
- Pre-repair snapshot location.

Repairs and migrations are siblings: both are deliberate,
documented, reversible-where-possible editorial acts. The
distinction is intent: a migration evolves the schema; a repair
restores correctness.

---

## 15. The integrity proof, for commentary

The deferred commentary integrity proof
(`COMMENTARY_VERSIONING.md §12`) is the primary detection mechanism
for the failure categories above. Its checks include:

1. Every record's `provenance.layer` matches its file's `layer`.
2. Every anchor resolves through the resolver (or is marked
   `unresolved`/`orphaned`).
3. Every revision's `supersedes` points at an existing record
   that has a matching `superseded_by` pointer.
4. Every record has at least one stewardship_log entry.
5. Every duplicate id case is in the alias table.
6. Every AI record has full model identity.
7. Every record's `schema_version` matches its structural shape.
8. Every frozen record's structure is byte-identical to its
   last-known frozen snapshot.

A failing check produces a quarantine event; the steward responds
per the relevant section above.

The proof is **read-only** with respect to the canonical record
set. It does not perform repairs. Repairs are deliberate steward
acts. This separation is the same as the existing
`passage_subsequence_proof.py` for primary text: the proof
detects; the steward repairs.

---

## 16. The catastrophic case

In the worst case — disk failure that destroys part of the
canonical record set, with no recoverable snapshot — the archive's
honesty discipline still applies:

1. **What can be recovered, is**. From git history, from
   institutional backups, from old runtime caches, from the public
   reader's exported data.
2. **What cannot be recovered, is recorded as lost**. A canonical
   "loss event" document at `logs/_archive/<date>_loss/` enumerates
   every record id that was in the canonical set before the loss
   and is not in the canonical set after.
3. **The reader is told**. The renderer's status page lists known
   lost records by id. A citation to a lost record resolves to a
   "lost on [date]; see [loss document]" response.

The archive does not pretend it never had records it lost. The
loss is part of its history, recorded with the same discipline as
any other event. A reader in 2126 reading the loss document
understands what happened; the archive's credibility survives the
loss because the loss was acknowledged.

---

## 17. Closing note

Repair is the discipline of facing reality. Records break. Files
corrupt. Tooling fails. Stewards make mistakes. The constitutional
commitment is not that the archive will never fail; it is that the
archive will fail **honestly**, and that every failure will be
preserved as part of the archive's institutional memory.

A repair-protocol document is, viewed properly, an act of
preparation. The archive is preparing for the moments — across
decades, perhaps centuries — when something will need fixing. By
the time those moments arrive, the protocols are already in place.
The steward of 2086 who finds a broken anchor knows what to do, not
because they invented a process, but because the process was
recorded in 2026 with the future in view.

That is what an archival institution is.
