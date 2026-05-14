# Citation Permanence

*v1 · 2026-05-14 · stewardship architecture; no implementation yet.*

A scholar in 2126 picks up an essay written in 2026 that cites
`archive:passage:jataka::chalmers-vol1::1.1`. The essay says the
Apannaka opens with a discourse on Truth. The scholar wants to
verify the citation.

This document is about that moment.

The constitutional commitment from `COMMENTARY_CONSTITUTION.md §11`:

> A reference to a primary passage made today must resolve in ten,
> fifty, a hundred years. Identifiers do not get renamed for
> aesthetic reasons. Where they must change, redirection is
> recorded; the old identifier does not disappear.

This document tells the future steward what they must promise to
the future reader.

---

## 1. Citation, in the archive's sense

A **citation** is a reference made by anyone, anywhere, to a stable
identifier in this archive. The identifier may be:

- A primary text:    `archive:text:quran`
- A translation:     `archive:translation:quran::saheeh`
- A volume:          `archive:volume:jataka::vol6`
- A tale:            `archive:tale:jataka::547`
- A chapter:         `archive:chapter:jataka::chalmers-vol1::1`
- A passage:         `archive:passage:quran::saheeh::2.255`
- A range:           `archive:range:quran::saheeh::2.255~2.256`
- A phrase locator:  `archive:passage:quran::saheeh::2.255:phrase=Allah:nth=1`
- An apparatus item: `archive:apparatus:upanishads-muller-part2::muller::27.1`
- A commentary record: `archive:commentary:editorial-2026-05-14-apannaka-page-bracket`
- A revision of a record: `…@2027-03-10`
- An entity:         `archive:entity:bodhisatta`
- A concept:         `archive:concept:no-self`

Each of these identifiers is meant to resolve forever. That is the
commitment this document elaborates.

---

## 2. The three threats to citation permanence

Citations fail over time for three reasons:

1. **Schema evolution.** The schema changes; old fields move; the
   resolver no longer knows where to look.
2. **Content evolution.** The targeted object is renamed, split,
   merged, deprecated, or removed.
3. **Implementation evolution.** The renderer changes; the
   URL scheme changes; the file structure changes.

The archive's defense against each is specific.

---

## 3. Defense against schema evolution

### 3.1 Identifier stability

Identifiers do **not** carry schema-version information. An
identifier valid in v1 is valid in v2. The resolver mediates between
schema versions transparently.

The identifier `archive:passage:quran::saheeh::2.255` does not become
`archive:v2:passage:quran::saheeh::2.255` when the schema bumps to
v2. The version is implicit in the file the identifier resolves
into, not in the identifier itself.

### 3.2 Schema versioning at the file level

Every JSON file in the canonical record set carries a `version`
field at the root. The schema migration discipline
(`COMMENTARY_MIGRATION.md`) governs how this field evolves. The
resolver reads the file's schema version and interprets the file's
contents accordingly.

When a new schema is adopted:

- Old files **remain valid**. They are not auto-rewritten.
- Old files are read by **schema-version-aware** code paths in the
  resolver.
- New files are written in the new schema.
- The migration manifest records when each file last touched any
  schema-relevant field.

A reader's citation does not change because the schema changed. The
resolver does the work.

### 3.3 Schema additivity

The archive's schema evolves **additively** whenever possible. Adding
a field is safe; renaming a field is not. Removing a field is not.
Reordering fields is not.

When a field name must change (a rare event), the old name is
preserved as an alias. The resolver reads either name into the same
internal value. The original-named file remains valid forever.

---

## 4. Defense against content evolution

### 4.1 Identifier reuse is forbidden

An identifier, once issued, is **never reused** for a different
object. If passage `1.1` of a translation is restored such that the
"old 1.1" content is now at `1.2`, the new `1.1` does not refer to
the old content. The old `1.1` identifier either:

- Continues to refer to the old content (preserved at its
  pre-restoration location, with a `superseded_by` alias), or
- Is recorded as **retired**: the identifier exists in the alias
  table marked "retired on [date]; see [restoration]; the content
  that lived here is now at [new identifier] or has been removed."

A reader's citation to the retired identifier still tells the
reader something honest: *the original target existed; here is what
happened to it*. The citation is not silently re-routed to a
different passage and presented as if nothing changed.

### 4.2 The alias table

When a passage id changes during a restoration, the alias table
records the mapping:

```
old identifier                              new identifier                              event                          date
─────────────────────────────────────────   ─────────────────────────────────────────   ──────────────────────────     ──────────
archive:passage:jataka::cowell-rouse-vol6::10.1153   archive:passage:jataka::cowell-rouse-vol6::10.1153   (no change)               2026-05-14
archive:passage:jataka::cowell-rouse-vol6::10.1154   (retired)                                            removed; printer's footer  2026-05-14
```

A citation to a retired identifier resolves to a redirect record,
not to silently-different content. The resolver returns: *"this
identifier was retired on 2026-05-14 by the Vol 6 acquisition
restoration; here is the stewardship log entry."*

### 4.3 Append-only restoration discipline

The restoration documents (`QURAN_RESTORATION_2026.md`,
`JATAKA_RESTORATION_2026.md`, `JATAKA_VOL6_ACQUISITION_2026.md`)
already record what changed in each pass. The alias table is
**generated from these restoration documents**: every restoration
that changes an identifier must record the change in the alias
table, with the restoration's name as evidence.

This is the practical mechanism that makes citation permanence
real. The discipline is: *no identifier change goes undocumented;
the documentation produces the alias.*

### 4.4 Withdrawn / orphaned commentary records

A commentary record that is withdrawn or orphaned remains citable
(per `COMMENTARY_LIFECYCLE.md`). A citation to a withdrawn record
resolves to the record marked withdrawn. A citation to an orphaned
record resolves to the record marked orphaned, with the
restoration that orphaned it named.

The citation **resolves**. It does not silently break.

---

## 5. Defense against implementation evolution

### 5.1 Identifier independence from URL

The archive's identifier scheme is **not** a URL. It is a URN
(uniform resource name). A URN names a resource without saying how
to retrieve it. Retrieval is the resolver's job.

This is deliberate. URLs change as websites, file structures, and
deployment paths change. URNs persist as long as the resolver
exists. The archive's commitment is to the URN; not to any specific
URL form of the URN.

Today, the renderer maps URNs into URLs that look like:

```
archive:passage:quran::saheeh::2.255
  → /reader.html?text=quran&translation=saheeh&passage=2.255
```

But a future renderer may map the same URN into a different URL:

```
archive:passage:quran::saheeh::2.255
  → /tafsir-suite/quran/saheeh/2/255
```

The URN is the same in both eras. The URL changes. **Citations are
URN-based, not URL-based.** A citation in 2026 that quotes a URL
will break when the URL scheme changes; a citation that quotes a
URN will not.

The discipline for citation-making: always include the URN. URLs
may be included for reader convenience but are explicitly secondary.

### 5.2 The resolver as a permanent service

The archive's resolver — the component that takes a URN and
produces a result — must persist across implementation changes. A
specific resolver implementation may be replaced, but the
**function** the resolver performs is permanent.

The resolver's contract:

- Input: a valid URN.
- Output: one of:
  - The targeted object (passage, record, etc.).
  - A redirect to a current identifier (if the URN was retired and
    aliased).
  - An explicit, structured failure (if the URN was retired and
    not aliased, or if the URN is malformed).

The resolver **never** silently substitutes. The resolver **never**
guesses. The resolver **always** produces a deterministic answer
for a given URN and corpus state.

This is the mechanical guarantee that backs the constitutional
commitment.

---

## 6. The migration window

When a restoration changes identifiers, there is a brief window —
between the restoration and the next push — during which the alias
table must be updated. The discipline:

- The restoration pass produces both the new canonical state and
  the alias updates in the same commit.
- The alias table is **part of the canonical record set**, not a
  derived artifact. It is itself preserved forever.
- The resolver reads the alias table at every resolution.

A restoration that changes identifiers without updating the alias
table is incomplete. Its restoration document records the
incompleteness, and the next stewardship pass closes the gap.

---

## 7. Citation forms

The archive recommends three citation forms, in decreasing order of
durability:

### 7.1 Full URN

```
archive:passage:quran::saheeh::2.255
```

The most durable. The URN resolves directly. Schema and
implementation evolve underneath; the URN persists.

### 7.2 URN with human-readable reference

```
Q 2:255 (Saheeh Intl.) [archive:passage:quran::saheeh::2.255]
```

The URN bracketed alongside the conventional citation. A reader can
verify by either; if the conventional citation drifts (e.g., a
future edition changes verse numbering), the URN remains the
canonical pointer.

### 7.3 URN with bare-canon snapshot

For citations made in long-lived publications (books, dissertations,
court documents), the most durable form embeds the actual passage
text as it stood at citation time:

```
Q 2:255 (Saheeh Intl.):
  "Allah - there is no deity except Him, the Ever-Living, the
  Sustainer of [all] existence…"
  [archive:passage:quran::saheeh::2.255; verified 2026-05-14]
```

This pattern is the strongest defense against archive failure
itself. If the archive vanishes, the citation still preserves the
text. If the archive persists, the citation can be verified against
it.

The `verified <date>` notation tells a future reader: *the cited
text was checked against the archive on this date; if the URN now
resolves to different content, the alias chain explains why.*

---

## 8. The 2126 commitment

The archive's commitment to a reader in 2126:

A citation made in 2026, using the URN form, will **resolve in
2126**. The resolution may produce:

- The exact original target, if the target was preserved unchanged.
- A redirect to a current identifier, if the target's id was changed
  (with the alias chain documenting the change).
- A record marked **withdrawn**, **deprecated**, or **orphaned**, if
  the targeted commentary record went through a state transition
  (with full lifecycle history visible).
- An explicit **retirement** notice, if the target was deliberately
  removed (with the responsible restoration documented).

The resolution **does not produce silently-different content**.
The resolution **does not 404 silently**. The resolution **does
not guess**.

These are the four outcomes the future reader can rely on. Anything
else is a stewardship failure to be documented in the repair
protocols.

---

## 9. Citation across the seven layers

The provenance-layer system of `PROVENANCE_LAYERS.md` interacts
with citation permanence as follows:

| Layer | Citation persists when… | Citation may fail when… |
|---|---|---|
| 1 — Primary text | The text is preserved; the resolver runs. | The text is restricted (then citation resolves to "restricted") or retired with no alias. |
| 2 — Source apparatus | Same as Layer 1. | Same as Layer 1. |
| 3 — Traditional commentary (bridge) | The traditional commentary is acquired as a Layer-1 text. | The bridge target is never acquired; citation resolves to the bridge record's `unresolved` state. |
| 4 — Modern scholarship | The scholarship record persists. | The record is withdrawn (resolves to withdrawn marker). |
| 5 — Archive editorial | The editorial record persists. | Same as Layer 4. |
| 6 — AI-generated | The AI record persists with its model identity. | The record is deprecated; the deprecation chain remains citable. |
| 7 — Private annotation | Outside the archive's citation guarantee. | Reader storage is reader-controlled. |

For Layers 1–6, the archive's citation permanence is a constitutional
commitment. For Layer 7, the commitment lies with the reader's own
storage. The archive does not guarantee resolution of citations into
private annotation storage.

---

## 10. The unresolvable case

Some citations will fail to resolve, eventually, by no one's fault:

- A primary text is removed under legal compulsion (per
  `COMMENTARY_LIFECYCLE.md §5`).
- A commentary record's anchor target was orphaned and never
  re-resolved.
- A bridge to a traditional commentary corpus that the archive will
  never acquire.
- A schema change so dramatic that pre-change records cannot be
  meaningfully migrated.

For each of these, the archive's commitment is to **fail honestly**.
The resolver returns a structured explanation: what the citation
points at, what state that target is in, and why. The reader can
then make their own judgment about how to use the citation.

A failed-but-explained citation is not the same as a broken
citation. The latter has no information; the former has full
historical information.

---

## 11. The archival horizon

A citation made today may need to resolve a century from now.
Realistic horizons:

- **Ten years.** The archive's tools and formats will have evolved
  through several iterations. Schema may be at v2 or v3. The
  resolver may have been rewritten. Citations made today should
  still work transparently.
- **Fifty years.** The archive's stewards may have changed. The
  technical platform may bear no resemblance to today's. Citations
  should still work, possibly through one or two layers of compat
  shims.
- **A century.** The archive's institutional context is unknown.
  The hardware, the software, the legal regimes may all be
  different. Citations should still **mean what they meant**, even
  if some require explicit migration tooling to resolve.

The discipline that makes the century horizon plausible:

- URNs, not URLs.
- Additive schema evolution.
- Alias tables generated from restoration documents.
- Resolver as a permanent service with a stable contract.
- Append-only stewardship of every identifier change.
- Bare-canon snapshots embedded in important citations.

None of these is exotic. All are old archival practices, rendered
in current technology.

---

## 12. Practical guidance for citation-makers

For a steward citing the archive today:

- **Use the URN form** as the canonical identifier.
- **Include the human-readable reference** for convenience.
- **For long-lived publications, embed a snapshot** of the cited
  text with a `verified <date>` annotation.
- **Do not cite URLs as primary identifiers.** URLs are
  implementation; URNs are commitment.
- **Cite a specific revision** when the citation is for a
  long-lived artifact; cite the head when the citation should
  track changes.
- **For commentary records, cite by record id** (with optional
  revision suffix), not by anchor of the underlying primary text.
  The two cite different things.

For a reader following a citation:

- A URN that resolves cleanly is the normal case.
- A URN that resolves with a redirect explains itself via the alias
  chain.
- A URN that resolves with a state marker (withdrawn, deprecated,
  orphaned) explains itself via the stewardship log.
- A URN that fails to resolve is, ideally, a documented failure —
  with the reason explicit, the date recorded, and the
  responsibility named.

---

## 13. Closing note

A citation is a small thing. Across centuries, citations become
the **load-bearing fabric** of a textual tradition. The Talmud's
internal cross-references work because the Talmud's identifiers
have not changed in fifteen centuries. The Loeb Classical Library's
volume-and-page citations work because the Loeb editorial team
maintained identifier permanence across more than a century of
reprints. The PCGS catalog of Greek-coin types works because every
type was given a permanent identifier on first publication.

The archive aspires to that durability. The mechanisms are humble:
URNs, alias tables, schema-versioned files, append-only records,
documented restorations, an honest resolver. The mechanisms are not
new. They are what civilization has used to keep citations alive
for a long time.

A reader in 2126 picking up an essay from 2026 should be able to
follow its citations into this archive and find the texts. The
discipline above is how. The discipline is what makes the archive
worth citing.
