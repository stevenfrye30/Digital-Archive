# Commentary Versioning

*v1 · 2026-05-14 · stewardship architecture; no implementation yet.*

A commentary record may need to change. The steward may find a
better formulation; a manuscript variant may surface; a fact may
need correction; an attribution may need to be tightened. The
question this document answers is: **how does change happen without
silencing what came before?**

The constitutional answer, simply stated:

> **A commentary record is immutable once published. Change is
> recorded as a new sibling record that names its predecessor.**

This is the *append-only revision* pattern. It is older than
software, and older than printing — it is how the Glossa Ordinaria
accreted, how Talmudic commentary stacked over centuries, how
monastic scriptoria recorded successive readings.

This document operates under `COMMENTARY_CONSTITUTION.md` and the
lifecycle states defined in `COMMENTARY_LIFECYCLE.md`. The most
important precedent is `COMMENTARY_PROTOTYPE_2026.md §6` and §7,
which established the verbatim and idempotency disciplines through
the prototype renderer.

---

## 1. The two questions versioning answers

Every versioning system answers two questions. This archive's
answers are specific:

**1. Where does the new version live?**

In a new record file (or new record within a file), sibling to the
original. Not as an in-place edit of the original. **The original
record is never modified after publication.**

**2. How does a reader find the right version?**

Through an explicit revision lineage: each revision names its
predecessor (`supersedes`), and the renderer follows the chain to
present the most recent version by default, with prior versions
reachable through a "see history" toggle.

These two answers together produce **file-level immutability with
record-level revision history**. Each version is a fully-citable
artifact in its own right.

---

## 2. The append-only sibling pattern

When a record needs revision, the steward authors a **new** record
with:

- A new `id` (typically the original id with a date suffix).
- A `supersedes` field naming the prior record's id.
- The same anchors as the prior record (anchors may be added, but
  removing an anchor is itself an editorial event — see §6).
- The same canonical authorship (the prior author's name carries
  over; the steward's name is added as `revised_by`).
- A new body.
- A fresh `stewardship_log` entry for the revision.

The prior record:

- Transitions to `deprecated` per `COMMENTARY_LIFECYCLE.md §3.4`.
- Acquires a `superseded_by` pointer to the new record.
- Transitions to `superseded` (via the `deprecated → superseded`
  transition).
- Remains in the canonical record set, fully readable and citable.

**Both records exist.** Both are citable. The renderer shows the
successor by default; the predecessor is reachable through a
"history" toggle or by citation lookup.

### 2.1 Identifier format

A revision's id extends the original id with a date suffix. The
prototype's convention:

```
<original-id>@<revision-date>
```

Example progression:

```
editorial-2026-05-14-apannaka-page-bracket
editorial-2026-05-14-apannaka-page-bracket@2027-03-10
editorial-2026-05-14-apannaka-page-bracket@2031-08-22
```

The original id never changes its date suffix (that's the
authorship date). Each revision adds its own date suffix. A reader
in 2126 reading record `…@2027-03-10` sees both *when the record
was first authored* (2026-05-14, from the base id) and *when this
revision was authored* (2027-03-10, from the suffix). The temporal
trajectory is legible from the id alone.

### 2.2 Why date suffix, not version number

The archive rejects sequential version numbers (`-v1`, `-v2`) in
favor of date suffixes. Reasons:

- **Version numbers are arbitrary.** `-v2` does not tell a reader
  when `-v2` was made; the date does.
- **Date suffixes survive missing revisions.** If a record has
  revisions `@2027-03-10` and `@2031-08-22` but no `@2029`
  intermediate, the suffix scheme makes this gap honest. A
  sequential scheme would suggest a missing `-v2`.
- **Dates are universal.** A future scholar reading the archive can
  immediately situate the revision in time without consulting a
  version table.
- **Dates encode collation.** ISO date sort order is the revision
  order; no separate ordering metadata is needed.

The cost is verbosity. A record id with multiple revisions becomes:

```
editorial-2026-05-14-apannaka-page-bracket@2031-08-22
```

That is acceptable for an artifact intended to last centuries.

---

## 3. The revision lineage

Each record carries pointers that make the lineage explicit:

| Field | Direction | Meaning |
|---|---|---|
| `supersedes` | back | Names the prior record this one revises. Set on the revision; null on the original. |
| `superseded_by` | forward | Names the successor (if one exists). Set on the prior record when its successor is published. |

These pointers are **redundant** (one direction would suffice to
reconstruct the chain), but the redundancy is deliberate: bidirectional
pointers allow the renderer to walk the lineage in either direction
without re-scanning the corpus.

If the lineage's redundancy is ever broken (the two pointers
disagree), the archive's repair protocol (`COMMENTARY_REPAIR_PROTOCOLS.md`)
applies.

### 3.1 The chain

A record's chain is the sequence of all versions, in date order:

```
record (original)
  ↓ superseded_by
record@revision1
  ↓ superseded_by
record@revision2
  ↓ superseded_by
record@revision3   ← current "head"
```

The chain has a **head**: the most recent revision, which has no
`superseded_by` pointer. The head is what the renderer displays by
default.

The chain has a **root**: the original record, which has no
`supersedes` pointer. The root carries the canonical authorship
date and the canonical record-level provenance.

A reader citing a record cites a **specific point in the chain**.
Citation of the head means "the most recent state"; citation of a
specific revision means "this version, exactly as it was authored."

Both forms are legitimate. The constitution's preference: cite the
specific revision when the citation is being made for a long-lived
artifact (a publication, an essay, a future scholar's reference).
Cite the head when the citation is reader-facing in a context that
should track changes automatically.

---

## 4. What may be revised

A revision may change:

- The `body` (the substantive content).
- The `categories` (per the versioning discipline of
  `COMMENTARY_ONTOLOGY.md §7`, with the version pinning).
- The `reference_text` (the human-readable display string).
- The `anchors` (additions only; see §6 for the asymmetric rule).
- Auxiliary schema-extension fields.

A revision may **not** change:

- The original `id` (the base id is permanent).
- The original `provenance.author` (the original author's name
  stays).
- The original `provenance.date` (the original creation date stays).
- The original `body_language` (a translation to another language
  is a separate concern, see §7).
- The chain's history (revisions do not modify their predecessors).

Each revision's `provenance` records both the original author (who
remains the author of record) and the `revised_by` field naming the
steward who authored the revision.

---

## 5. Body revision conventions

When the body is revised, the new record's body is the **complete
new body**, not a diff. The archive does not store diffs at the
record level. Reasons:

- **Diffs depend on a representation.** A diff format chosen in 2026
  may be unreadable in 2126.
- **Diffs are fragile across schema changes.** A field rename
  invalidates every diff that touched the field.
- **The archive prefers self-contained artifacts.** A revision
  record carries its own complete body; the diff to the predecessor
  can always be computed at read time.

A renderer **may** offer "see what changed" by computing the diff
between the revision's body and its predecessor's body at display
time. The diff is rendered; it is not stored.

### 5.1 The first revision is special

When a record first acquires a revision, the predecessor record (the
original) is the only record that ever had no successor. A reader
who cites the original record before any revision was made cites
the head of a one-record chain. After the first revision, the
original record's `superseded_by` field acquires a value, and
citations to the original now resolve to "deprecated; see
successor."

The citation **still resolves**. The original record is still
readable. But the renderer now displays it with the deprecation
mark, and the reader-facing default view shows the revision.

A citation that explicitly requests the original (by its bare id
without revision date) gets the original record, marked deprecated.
This is the constitutional commitment: **the past is reachable,
even when the present has moved on**.

---

## 6. The anchor-asymmetry rule

A revision may **add** anchors. A revision may **not remove**
anchors that the predecessor had.

The reason is citation permanence. If a record is cited *because of*
its anchor at passage 2.255, removing that anchor in a revision
would silently invalidate the citation. The reader who followed the
citation would arrive at a record that no longer anchors to 2.255 —
and have no way to understand why.

So the rule:

- **Revisions may add anchors.** A second pass may discover that
  the same claim also applies at passage 2.256.
- **Revisions may not remove anchors.** If the steward believes the
  claim no longer applies at passage 2.255, the record is
  **deprecated**, and a **new record** (with the corrected, smaller
  anchor set) is published. Both records remain.

This may feel surprising. The archive prefers the surprise: it is
constitutionally honest, and it preserves what readers cited.

### 6.1 The exception: typo'd anchors

A record published with an anchor to a passage id that **never
existed** is a typo, not a real anchor. Typos may be corrected in
revisions; the predecessor's typo is preserved in its body's
unmodified form, and the revision's `stewardship_log` records:
*"Anchor `passage:foo::bar::999.999` corrected to
`passage:foo::bar::99.99` — the original was a typo with no
resolvable target."*

The discipline: the **typo is preserved** (the predecessor still
shows it), but the **claim** moves forward with the correct anchor.

---

## 7. Translation of a record

A commentary record's body is in a single language. Translation of
the body to another language is a **new record**, not a revision.
Reasons:

- Translation is interpretation. The translator is a named author.
- Translation imposes choices the original author did not make.
- Treating a translation as a "revision" would silently overwrite
  the original-language version in default renders.

The translation record:

- Has its own `id` (typically `<original-id>:<lang-code>`, e.g.,
  `editorial-2026-05-14-apannaka-page-bracket:ru` for a Russian
  translation).
- Has its own `provenance.author` (the translator).
- Carries a `translates` field pointing at the original record.
- Carries the same `anchors` as the original (translations of the
  same claim point at the same targets).
- Lives in the same file or a sibling file.

A renderer may display the translation alongside the original; the
constitutional commitment is that the **original is not replaced** by
the translation, and the translation **is not silently elevated** to
the original's authorship.

This is a deliberate echo of the archive's translation discipline
for primary texts: the Pickthall Qur'an does not replace the
Saheeh Qur'an; both are preserved.

---

## 8. Tag (categorization) revisions

The `COMMENTARY_ONTOLOGY.md §7` versioning rule extends here:
**tag changes are themselves recorded.** When a record's
categorization is updated, the update is logged in the
`stewardship_log` with the previous tags, the new tags, and the
reason.

If the categorization change is small (a tag was added or removed
without changing the body), it does **not** require a new record.
The change is logged in place. This is the one exception to the
append-only-record principle, and it is a small one: tags are
metadata about the record, not the record's content.

If the categorization change is **large** — the steward now
considers the record's primary claim to be a different category
entirely — it triggers a real revision: a new record with the new
tags and (probably) a revised body that reflects the recategorization.

The boundary between "small tag adjustment" (logged in place) and
"recategorization" (revision) is editorial judgment. The
`stewardship_log` records the judgment.

---

## 9. Multi-author records

A revision authored by a different steward from the original
records both:

- `provenance.author` — the **original** author (unchanged).
- `provenance.revised_by` — the **current** steward.

If the original author has stopped working on the archive and a new
steward revises the record, the original author's name persists.
The original author is the author of the original; the reviser is
the author of the revision. Both are recorded forever.

Collaborative records — records authored jointly by multiple
stewards — are handled by listing both in `provenance.author` as a
list. The archive does not impose "first author" / "second author"
hierarchy; the list order is the order the stewards chose.

---

## 10. The "frozen" preservation case

A steward may decide that a record should **never be revised**.
Examples: a historical commentary from a specific date that is
worth preserving exactly as it was; a record about a moment in the
archive's own history that would be falsified by later editing.

The discipline:

- The steward sets `revision_policy: "frozen"` on the record.
- The renderer displays a small "frozen" mark.
- Future stewards **may not author a `supersedes` revision** of a
  frozen record. If they have a different view, they author a
  **new, independent record** with its own id (not a revision-by-
  date-suffix), and link to the frozen record by ordinary anchor
  (`archive:commentary:<frozen-id>`).

Frozen state is **rare**. The vast majority of records remain
revisable.

This is the archive's analog of the Talmud's *acharon kaman*
("the latest has stood up") convention: at some point, a tradition
declines to keep revising its earlier strata, and instead lets
them stand as historical record.

---

## 11. What a stewardship_log entry looks like for revision

The append-only stewardship log is the canonical record of the
revision history. For a revision event, the entry is:

```json
{
  "date": "2027-03-10",
  "action": "revised",
  "by": "archive:steward:steve",
  "revision_id": "editorial-2026-05-14-apannaka-page-bracket@2027-03-10",
  "predecessor_id": "editorial-2026-05-14-apannaka-page-bracket",
  "state_after": "provisional",
  "summary_of_change": "Clarified that the [95.] page bracket is from SacredTexts.com's HTML export of the printed Cowell vol I, page 95 — not a passage of the Jataka itself. Original record was correct but could be misread.",
  "note": "Revision triggered by a steward re-reading; no external feedback."
}
```

The `summary_of_change` is the steward's own description of why the
revision was made. It is not auto-generated. It is the historical
record of the editorial intent.

---

## 12. Integration with the integrity proof

The archive's integrity proof for primary text (`passage_subsequence_proof.py`)
verifies that every reader-facing passage is a verbatim substring
of its raw source. The commentary versioning system needs an analog:
a **commentary integrity proof**, deferred to implementation, that
verifies:

- Every record's revisions form a valid chain (no orphan revisions,
  no cycles, no broken pointers).
- Every record's anchors all resolve (per
  `COMMENTARY_REPAIR_PROTOCOLS.md`).
- Every revision's `supersedes` points at a real prior record.
- Every prior record's `superseded_by` points at the right revision.
- Every record's `stewardship_log` has at least a `created` entry.

This is a stewardship contract, not yet implemented. The discipline
is recorded so the implementation, when it comes, knows what to
check.

---

## 13. Closing note

The versioning discipline described here is conservative on purpose.
It rejects in-place edits, sequential version numbers, diff-stored
deltas, and silent revision. It accepts the cost of file
proliferation in exchange for archival permanence.

A commentary record that has lived for thirty years and accumulated
five revisions exists in the archive as six records: the original
and five revisions, each citable, each readable, each part of an
explicit lineage. The reader of the year 2056 looking at the head of
the chain sees the most recent claim; following the lineage, they
read every prior version as it stood.

This is what it means to preserve interpretive history. The
versioning discipline is the mechanism. The mechanism is small and
old and durable, like the lined paper in a monastery's commonplace
book.
