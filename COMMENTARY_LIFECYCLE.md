# Commentary Lifecycle

*v1 · 2026-05-14 · stewardship architecture; no implementation yet.*

A commentary record in this archive has a long life. It is drafted,
checked, published, sometimes revised, sometimes superseded,
occasionally withdrawn. Across a working steward's lifetime, that
arc may last decades. Across the archive's intended lifetime, the
records authored today must remain legible to readers a century from
now — including readers who want to see not just the current state
of a commentary record but the **historical strata** of how it
came to its current state.

This document defines the legal lifecycle states a commentary record
may occupy, the transitions between them, and the discipline that
governs each transition. It operates under the constitutional law of
`COMMENTARY_CONSTITUTION.md` and the layer system of
`PROVENANCE_LAYERS.md`.

The most consequential commitment of this document is the simplest:

> **Records are never deleted. Records change state.**

A withdrawn record is still a record. A superseded record is still
a record. A record whose anchor target no longer exists is still a
record. The archive preserves its own editorial history with the
same fidelity it preserves the primary corpus.

---

## 1. The lifecycle states

A commentary record's `lifecycle_state` is one of:

| State | Reader-visible? | One-line meaning |
|---|---|---|
| `drafted` | private | The steward is still composing; not yet published. |
| `provisional` | yes | Published. Steward acknowledges this is not yet steward-verified. |
| `verified` | yes | The steward (or another steward) has reviewed and accepted. |
| `deprecated` | yes (marked) | Older record that a newer one supersedes; still readable, marked. |
| `superseded` | yes (marked) | Deprecated record that explicitly points at its successor. |
| `withdrawn` | yes (marked) | Publicly retracted by the author. Body preserved; reasons recorded. |
| `unresolved` | yes (marked) | Anchor target does not currently resolve. Gap recorded honestly. |
| `orphaned` | yes (marked) | Anchor target removed by an upstream restoration; record preserved. |

Each state has structural meaning, display rules, and rules about
what other states it may transition to.

---

## 2. The transition graph

A state transition is an editorial act. It is dated, attributed, and
recorded in the record's `stewardship_log`. The set of legal
transitions is small:

```
                            ┌─────────────┐
                            │   drafted   │     (private; not in
                            │  (private)  │      canonical record set)
                            └──────┬──────┘
                                   │ publish
                                   ▼
                            ┌─────────────┐
                            │ provisional ├──── withdraw ────────────┐
                            └──────┬──────┘                          │
                                   │ verify                          │
                                   ▼                                 ▼
                            ┌─────────────┐                   ┌────────────┐
                            │  verified   ├── withdraw ─────► │ withdrawn  │
                            └──────┬──────┘                   └────────────┘
                                   │ supersede (by new record)
                                   ▼
                            ┌─────────────┐
                            │ deprecated  │
                            └──────┬──────┘
                                   │ link to successor
                                   ▼
                            ┌─────────────┐
                            │ superseded  │
                            └─────────────┘

  Orthogonal states (apply to provisional/verified/deprecated/superseded):
   - unresolved : anchor stopped resolving
   - orphaned   : anchor target was removed by upstream restoration

  These do not transition the record to a different state; they
  ADD a structural condition that the renderer surfaces.
```

The transitions that **are** legal:

- `drafted` → `provisional` (publish)
- `provisional` → `verified` (steward review accepted)
- `provisional` → `withdrawn` (author retraction)
- `verified` → `withdrawn` (author retraction, even after verification)
- `verified` → `deprecated` (a newer record now stands in its place)
- `deprecated` → `superseded` (the deprecation acquires a named successor)

The transitions that are **forbidden** by constitutional law:

- Any state → deleted. There is no delete state. The record persists.
- `verified` → `provisional` (verification is not un-done; a verified record can be deprecated or withdrawn, but not regressed)
- `withdrawn` → anything (withdrawal is terminal; a retracted claim cannot be silently un-retracted)
- `superseded` → anything (also terminal; the successor chain is the live record)
- Anywhere → `drafted` (a published record cannot be un-published into private state)

A transition that is not in the legal-transition table requires an
amendment to this document, dated and recorded.

---

## 3. State semantics in detail

### 3.1 `drafted`

A work-in-progress record. Lives in the steward's private working
area (`PUBLIC_PRIVATE_BOUNDARIES.md §3`), not in the canonical
record set. The archive does not preserve drafts unless the steward
explicitly archives one (in which case it is a separate Layer-5
editorial note recording the draft's contents, not a "drafted" record
in the canonical set).

A drafted record has no public anchor. It cannot be cited. It may
freely be edited or discarded by its author.

The transition `drafted → provisional` is the act of **publishing**:
the steward moves the record into the canonical commentary file set,
where it acquires a stable identifier and becomes citable.

### 3.2 `provisional`

A record that is published in the canonical record set but not yet
steward-verified. This is the **default state for newly-published
commentary records**. The provisional state signals: *"the steward
has chosen to publish this, but the claim has not yet been
independently reviewed."*

A provisional record:

- is fully citable;
- displays in readers (with no special marker by default — provisional
  is the default state, and marking it would imply that verified is
  the norm, which would over-promise);
- may be revised by its author, producing a revision lineage per
  `COMMENTARY_VERSIONING.md`;
- may be withdrawn by its author;
- may be promoted to `verified` when a second steward (or, in
  single-steward archives, the same steward after a deliberate
  re-reading) confirms the claim.

The `provisional` → `verified` transition is one of the two paths
out of provisional state. The other is `provisional` → `withdrawn`.

### 3.3 `verified`

A record that has been steward-reviewed. The reviewer is recorded
(`provenance.verifier`), distinct from the original author. In
single-steward archives, this means the same steward returned to
the record at a later date and explicitly re-affirmed it; the
verifier date is later than the author date.

A verified record carries slightly more weight in display: it may
be marked with a small "verified" indicator. But the renderer must
**not** demote provisional records by appearance — verification is
not a quality judgment, it is a process state. A provisional record
is not "worse"; it is "not yet re-read."

Verified records may still be revised (producing a new revision in
provisional state, which must be re-verified to reach verified state
again).

### 3.4 `deprecated`

A record that has been replaced in the steward's view by a different
record (a successor) that the steward considers preferable. The
deprecated record is **still readable**. Both records appear in the
archive. Both are citable.

A deprecated record is visually marked: *"deprecated; see successor."*
The deprecation does **not** rank the deprecated record as wrong; it
records the steward's current preference.

A record may be deprecated for many reasons: a more careful
formulation of the same idea has been written; the steward has
changed their view; new evidence has emerged; the categorization
under a newer ontology fits better elsewhere. Each reason is
recorded in the `stewardship_log` of the deprecation transition.

### 3.5 `superseded`

A deprecated record that has been explicitly linked to its successor.
The transition `deprecated → superseded` is small but important: it
adds a `superseded_by` pointer to the named successor record. The
renderer can now show the successor's claim directly when the
superseded record is referenced.

A record can stay in `deprecated` indefinitely if no single successor
emerges (e.g., a steward decides the original claim should be
split into three more careful claims). In that case, the deprecation
remains in place and the `superseded_by` pointer is never added.

When a successor is named, the transition to `superseded` is
recorded. Both records remain.

### 3.6 `withdrawn`

A record that has been retracted by its author. The retraction is
public, dated, and reason-recorded. The record's body is preserved
verbatim; the **retraction is metadata around the record, not a
modification of it**.

A withdrawn record is visually marked: *"withdrawn; see retraction
note."* The reason for withdrawal is in the `stewardship_log`.

Withdrawal is terminal. A withdrawn claim cannot be silently
un-withdrawn. If the author later believes the original claim was
right after all, they author a **new** record making the claim
again (which enters as provisional), and the old withdrawn record
remains as historical record.

Withdrawal does not erase. It records.

### 3.7 `unresolved`

An orthogonal condition. A record is `unresolved` if any of its
anchors no longer resolves against the current state of the corpus.

This typically happens when:

- The targeted passage's id changed during a restoration (the alias
  table should have caught it; if not, the anchor breaks).
- The targeted text was withdrawn from the canonical library (a rare
  event — the archive prefers archival relocation to removal — but
  possible for restricted/copyrighted material).
- The anchor was always to a hypothetical target (e.g., a
  traditional-commentary bridge to a not-yet-acquired commentary;
  see `COMMENTARY_PROTOTYPE_2026.md §5`).

A record marked `unresolved` is **still preserved**. The unresolved
condition is surfaced to the reader: *"this commentary points at a
target that does not currently resolve."* The condition may be
removed later if the target becomes resolvable (e.g., the
traditional commentary is acquired). The transition into
`unresolved` and out of `unresolved` is recorded.

### 3.8 `orphaned`

A stronger form of `unresolved`. A record is `orphaned` when its
anchor target was **explicitly removed** by an upstream act (e.g.,
the steward removed a passage from the canonical corpus during a
restoration). The orphaned condition records: *"this anchor used to
resolve, and was deliberately broken by an upstream restoration."*

Orphaned is the harshest condition a commentary record can carry.
The constitutional commitment is that **orphaning is rare**, because
the archive prefers archival relocation over removal of canonical
content. When orphaning happens, the upstream restoration's
stewardship log records every commentary record it orphaned, by
record id. The orphaned record's anchor entry is preserved
verbatim, with the orphaning event annotated.

A future restoration may "adopt" an orphaned record by re-resolving
its anchor to a new target, but this is an explicit editorial act,
not an automatic one.

---

## 4. What persists forever

Across every state, the following fields are **immutable** once a
record has left `drafted` state:

| Field | Why |
|---|---|
| `id` | The canonical identifier. Records are cited by id. Renaming would break citations made today. |
| `provenance.author` | Authorship is permanent. Even after withdrawal, the original author is recorded. |
| `provenance.date` | The first-creation date is the historical anchor. |
| `body` (original) | The verbatim body of the original record. Revisions append new bodies; the original stays. |
| `body_language` | The language the body was authored in. |
| `anchors` (original) | The original target(s). Revisions may add anchors; they do not remove original ones. |
| `stewardship_log` | Append-only. Every transition is recorded; nothing is removed. |

What may change:

- `lifecycle_state` (via legal transitions)
- `categories` (per the versioning discipline of
  `COMMENTARY_ONTOLOGY.md §7` — tag revisions are themselves
  recorded, with version pinning)
- `reference_text` (a human-readable display string; renderers may
  re-derive this)
- Auxiliary fields added in later schema versions

The principle: anything load-bearing for citation, attribution, or
historical record is **immutable**. Anything purely cosmetic or
schema-extensible may evolve.

---

## 5. The no-deletion principle

The archive does not delete commentary records.

This includes:

- Drafts that were never published. (These are private; the archive
  does not store them in the first place.)
- Withdrawn records. (They are marked withdrawn; their body is
  preserved.)
- Records the steward later regrets. (Regret is reason for a new
  record, not a deletion.)
- Records that contain embarrassing errors. (Errors are reason for
  a corrected revision, not a deletion of the error's record.)
- Records made by a steward who has since stopped working on the
  archive. (Authorship is permanent; the steward's name stays.)
- AI records that turned out to be wrong. (They are marked
  withdrawn or superseded; the AI's output is preserved.)

The single exception, granted reluctantly, is **legal compulsion**:
if a court order or comparable authority compels removal of a
specific record, the removal is itself recorded. A
`stewardship_log` entry notes: *"record removed under [authority] on
[date]; original body and metadata preserved at [archival location
outside the public archive]."* The record's presence in the public
canonical set ends; the record's *existence* is acknowledged
forever.

This is the archive's strongest commitment to interpretive history.
A future scholar studying how a steward's understanding of the
Apannaka-jātaka evolved over thirty years must be able to read every
draft-published, every revision, every retraction, every successor,
in order. The archive preserves the **process** by which
interpretive claims were made and unmade, not merely the final
state of the claim.

---

## 6. Archival scars

A record that has lived a long life carries archival scars: the
marks of its state transitions. The renderer surfaces these
honestly:

- A `verified` record may carry a quiet "✓ verified by [name] on
  [date]" mark.
- A `deprecated` record carries "see successor: [link]" if
  superseded, or "deprecated by author on [date]" if not yet
  superseded.
- A `withdrawn` record carries "**withdrawn** by author on [date];
  reason: [reason]" — the most visible mark, because withdrawal is
  the strongest editorial act short of legal compulsion.
- An `unresolved` record carries a small note: "anchor does not
  currently resolve; see [restoration document]."
- An `orphaned` record carries a stronger note: "anchor target was
  removed by [restoration name] on [date]; original target was
  [URN]."

The scars are not stigma. They are honesty. A reader of the future
sees the record's full life, not its glossed surface.

---

## 7. Comparative discipline: precedents

The lifecycle discipline above has historical analogs that are
worth naming, so a steward in a later century can see where the
archive's instincts came from.

- **Talmudic stratigraphy.** The Mishnah, Gemara, Rashi, Tosafot,
  and the *acharonim* all coexist on the printed Talmud page.
  Earlier strata are not erased by later ones; each layer occupies
  its own typographic register. The Talmud is read as a stack of
  centuries, not as the latest consensus.
- **Apparatus criticus.** Critical editions (Loeb, Oxford Classical
  Texts, the Cambridge Greek and Latin Classics) preserve manuscript
  variants in apparatus at the foot of every page. A reading that
  another scholar rejected is not erased; it is preserved with its
  source manuscript named.
- **Glossa Ordinaria.** Medieval biblical commentary preserved
  earlier glosses in the margins of newer manuscripts. The
  *interlinear gloss* and the *marginal gloss* both coexisted, both
  attributed (often anonymously by class — *Augustinus*, *Hieronymus*,
  *Beda*), neither replacing the other.
- **Buddhist commentarial strata.** The Pāli tradition layers
  *mūla* (root text) → *bhāṣya* (primary commentary, often
  Buddhaghosa) → *ṭīkā* (subcommentary) → *anuṭīkā*
  (sub-subcommentary). Each layer preserves and depends on the
  earlier; none replaces it.
- **Monastery scriptorium discipline.** A monastery scribe copying
  an earlier manuscript would mark corrections with named
  responsibility (the corrector's hand), not silently edit. The
  *prior* reading was preserved as a known reading even when the
  corrector preferred a different one.

The archive's lifecycle discipline imitates these traditions
without claiming their authority. The shared instinct is: **what
came before is not silenced by what comes next.** Centuries of
textual transmission learned this the hard way. The archive
inherits the lesson.

---

## 8. The stewardship log, in detail

Every commentary record carries a `stewardship_log` field — an
append-only list of state-transition events. The schema (illustrative):

```json
{
  "stewardship_log": [
    {
      "date": "2026-05-14",
      "action": "created",
      "by": "archive:steward:steve",
      "state_after": "provisional",
      "note": "Initial provisional publication."
    },
    {
      "date": "2027-03-10",
      "action": "revised",
      "by": "archive:steward:steve",
      "revision_id": "editorial-2026-05-14-apannaka-page-bracket@2027-03-10",
      "state_after": "provisional",
      "note": "Reformulated to clarify the SacredTexts page-bracket convention."
    },
    {
      "date": "2031-08-22",
      "action": "verified",
      "by": "archive:steward:another-steward",
      "state_after": "verified",
      "note": "Re-read after long interval; claim confirmed."
    },
    {
      "date": "2056-11-04",
      "action": "deprecated",
      "by": "archive:steward:future-steward",
      "state_after": "deprecated",
      "successor_id": "editorial-2056-apannaka-bracket-convention",
      "note": "Replaced by a more careful account of page-bracket transmission."
    }
  ]
}
```

The log is **append-only**. An entry is never removed. An entry's
fields are never modified once written. The integrity of the log
is the integrity of the historical record.

When the archive's future stewards review what happened on
2056-11-04, they read the log entry. The deprecation reason is the
log note. The successor record is named. Nothing is lost.

---

## 9. Display rules summary

The renderer's discipline for displaying lifecycle states is in
the implementation layer (deferred). The constitution requires
only:

- `provisional` and `verified` records display as normal commentary,
  with `verified` optionally carrying a small mark.
- `deprecated` and `superseded` records display with a visible
  deprecation notice; the successor (if any) is linked.
- `withdrawn` records display in full but with the withdrawal
  notice prominent; the reader sees both the original claim and the
  retraction.
- `unresolved` and `orphaned` records display the gap clearly.

A reader filtering for "only verified" content should be able to do
so. The renderer must not, by default, hide deprecated or withdrawn
records — they are part of the historical record. Filtering is
opt-in.

---

## 10. Closing note

The lifecycle described here is conservative on purpose. It
imitates the strata-preserving instincts of monastery scriptoria,
of critical edition apparatus, of the Talmudic page, of the Glossa
Ordinaria — all traditions that learned, over centuries, that
**silent revision is the enemy of textual integrity.**

A commentary record in this archive begins as a provisional act of
authorship, may be verified, may be deprecated, may be superseded,
may be withdrawn. It accumulates archival scars as it lives. None
of these states erases the record; all of them deepen the
historical record around it.

The archive is preserving interpretive history. The lifecycle is
how it does so.
