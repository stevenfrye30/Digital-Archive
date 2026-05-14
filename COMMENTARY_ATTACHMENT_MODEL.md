# Commentary Attachment Model

*v1 · 2026-05-14 · constitutional and architectural; no implementation yet.*

This document specifies **what commentary may attach to** and **how
attachment is expressed**. It is the most technical of the four
sibling architectural documents. The constitution that frames this
work is `COMMENTARY_CONSTITUTION.md`; the categorical vocabulary is
`COMMENTARY_ONTOLOGY.md`; the authority layers are
`PROVENANCE_LAYERS.md`; the things the archive refuses to do are
`INTERPRETIVE_BOUNDARIES.md`.

The constitutional commitment from `COMMENTARY_CONSTITUTION.md §4`
governs this entire document:

> Every anchor must be **stable**, **explicit**, and
> **non-destructive**.

If a proposal in this document violates any of those three, the
proposal is wrong.

---

## 1. The anchor

Every commentary record attaches to one or more **anchors**. An
anchor is a structured reference to an addressable unit of the
corpus.

An anchor is **not** a string of free-form English. It is a
canonical identifier that the archive's resolver can deterministically
look up and that survives schema evolution.

The anchor format proposed here is loosely modelled on the Canonical
Text Services (CTS) URN scheme but adapted to the archive's
existing identifier conventions. The format is **proposed**, not yet
implemented; the constitution requires that whatever format is
ultimately adopted, it satisfy the three properties named in §0.

### Anchor format (proposed)

A canonical anchor is a string of the form:

```
archive:<target-kind>:<target-id>[:<sub-locator>]
```

Where:

- `archive:` is a literal namespace prefix. It exists to make
  anchors distinguishable from URLs, opaque hashes, or filesystem
  paths in any context.
- `<target-kind>` names what kind of object is being referenced
  (see §2 below).
- `<target-id>` is the identifier of the targeted object, in the
  archive's own conventions (see §3 below).
- `<sub-locator>` is optional, specifying a finer-grained location
  within the targeted object (see §4 below).

Examples:

| Anchor | What it means |
|---|---|
| `archive:text:quran` | The Qur'an, as a whole text |
| `archive:translation:quran::saheeh` | The Saheeh International translation of the Qur'an |
| `archive:passage:quran::saheeh::2.255` | Ayat al-Kursi as Saheeh rendered it |
| `archive:passage:quran::saheeh::2.255:phrase=Allah` | The substring "Allah" within Ayat al-Kursi (Saheeh) |
| `archive:passage:jataka::cowell-rouse-vol6::10.1` | The opening passage of Vessantara-jātaka (Cowell vol 6) |
| `archive:tale:jataka::547` | The Vessantara-jātaka as a whole, across translations |
| `archive:entity:bodhisatta` | The conceptual entity "Bodhisatta" |
| `archive:concept:no-self` | The concept tag "no-self" |

The format is human-readable. A reader can read an anchor and know
what it points to. That is intentional: opaque hashes would be
shorter but would compromise stability and the citation-permanence
commitment.

---

## 2. Target kinds

The archive enumerates the kinds of object an anchor may target. The
list below is the working set for v1. A target kind is added by
amendment, not by silent extension.

### Primary text kinds

These target the canonical corpus.

| Kind | What it references | Granularity |
|---|---|---|
| `text` | A canonical work (e.g., the Qur'an, the Jātaka, Plato's Apology) | Whole-work |
| `translation` | A specific translation of a work | Translation-level |
| `volume` | A specific volume of a multi-volume work | Volume-level |
| `tale` | A discrete narrative unit (used for the Jātaka, fable collections, hadith) | Tale-level |
| `chapter` | A chapter in the source's own structure | Chapter-level |
| `passage` | A single reader-facing passage (the smallest schema-recorded unit) | Passage-level |
| `range` | A contiguous span of passages | Passage-range |

### Inter-textual kinds

These reference relations between texts.

| Kind | What it references |
|---|---|
| `parallel` | A pair of passages identified as parallels |
| `quotation` | A passage that quotes another passage |
| `paraphrase` | A passage that paraphrases another |

### Semantic kinds

These reference abstract objects.

| Kind | What it references |
|---|---|
| `entity` | A named person, place, deity, animal, object, lineage |
| `concept` | An abstract concept (no-self, dharma, agape, hesed, dao) |
| `motif` | A narrative motif (the dying god, the silent prince, the rescued bride) |
| `theme` | A thematic cluster broader than a single motif |

### Apparatus kinds

These reference the existing apparatus layer.

| Kind | What it references |
|---|---|
| `apparatus` | A specific apparatus record from `apparatus_file` |
| `variant` | A manuscript variant reading |
| `frontmatter` | A piece of source front-matter (preface, dedication, TOC) |

### Commentary kinds (commentary about commentary)

These reference other commentary records, enabling the commentary-of-
commentary case described in `COMMENTARY_ONTOLOGY.md §8`.

| Kind | What it references |
|---|---|
| `commentary` | A specific commentary record by its own id |
| `commentary-layer` | A whole authority layer, when a comment applies to it (e.g., "all AI-generated tags") |

---

## 3. Target identifiers

The identifier component of an anchor follows the archive's existing
identifier conventions, augmented for granularity.

| Anchor form | Identifier convention |
|---|---|
| `text:<id>` | The `id` field of the canonical text.json (e.g., `quran`, `jataka`) |
| `translation:<text-id>::<translation-id>` | Double-colon separator, both pieces from the existing schema |
| `volume:<text-id>::<volume-label-slug>` | E.g. `jataka::vol6` |
| `tale:<text-id>::<absolute-tale-number>` | Across-volume tale number for multi-volume works (e.g., `jataka::547` = Vessantara, regardless of which volume holds it) |
| `chapter:<text-id>::<translation-id>::<chapter-key>` | Chapter key from the translation's `chapter_titles` |
| `passage:<text-id>::<translation-id>::<passage-id>` | The `id` field of the passage |
| `range:<text-id>::<translation-id>::<start>~<end>` | A contiguous range, inclusive |
| `entity:<entity-id>` | Stable id from the archive's entity registry (to be designed) |
| `concept:<concept-id>` | Stable id from the archive's concept registry (to be designed) |
| `commentary:<commentary-id>` | Stable id of a commentary record |

The `<text-id>::<translation-id>::<id>` pattern reuses the existing
double-colon separator the archive already uses in
`passage_subsequence_proof` reporting (e.g., `quran::saheeh`,
`jataka::cowell-rouse-vol6`). This is deliberate continuity, not
invention.

### A note on `tale` and absolute tale numbers

The `tale:jataka::547` form is **proposed** but depends on a future
`tale_offset` per-volume metadata field, as noted in
`JATAKA_RESTORATION_2026.md` Remaining Limitations. Without that
field, the resolver cannot translate "absolute jātaka 547" to the
right volume's chapter index. Either the offset is added to the
schema (a small, additive change), or the `tale` anchor kind is
deferred until it is. The constitution does not pick; the
architecture allows for both timelines.

---

## 4. Sub-locators

A sub-locator narrows an anchor below the passage level. Sub-
locators are optional; an anchor at the passage level resolves
without one.

The archive needs to support:

- **Pointing at a phrase** within a passage (philological commentary)
- **Pointing at a word** (lexical commentary)
- **Pointing at a verse-line** within a multi-line passage
- **Pointing at a structural sub-element** of a complex passage

### Sub-locator forms

| Form | Use |
|---|---|
| `:phrase=<verbatim-substring>` | The first occurrence of the substring within the passage |
| `:phrase=<verbatim-substring>:nth=<N>` | The Nth occurrence of the substring (1-indexed) |
| `:line=<N>` | The Nth line of the passage (1-indexed; line breaks in source) |
| `:char-range=<start>-<end>` | A character-index range; used only when no other locator fits |

The character-index form is the **last-resort** locator. Phrase-
based locators survive minor passage reformatting (e.g., whitespace
normalization). Character ranges do not. The archive prefers phrase-
based anchors and avoids character ranges when an alternative is
available.

A phrase locator carries **risk**: if the same substring appears
multiple times in the passage, the renderer must disambiguate. The
`nth=<N>` qualifier handles that case. If a steward cannot
unambiguously identify which occurrence is meant, the anchor is
ill-formed; refusal-to-anchor is better than ambiguous anchoring.

### Verbatim substring discipline

A `:phrase=<text>` sub-locator's `<text>` is **verbatim**. The
archive does not normalize, lowercase, or strip diacritics from the
phrase when resolving. A phrase locator that fails to find its
target is an explicit error condition; the renderer must report the
failure, not silently best-guess.

This is the same discipline as the apparatus pattern: bodies are
verbatim, surrounding structure is the archive's voice.

---

## 5. Multi-anchor records

A commentary record **may** carry more than one anchor when its
claim genuinely targets more than one location. Examples:

- A `parallel` record between Qur'an 2:255 and Bible Psalm 121 has
  two anchors, both at the passage level. Neither is "primary."
- A `translation-comparison` record about the rendering of "Allāh"
  across Pickthall, Yusuf Ali, and Saheeh has three anchors, one
  per translation, all at the same passage level.
- A `narrative-motif` record on the motif of "the dying-and-rising
  god" might anchor at multiple tales across traditions.

Multi-anchor records are first-class. The renderer must display them
in a way that surfaces the multiplicity rather than picking one
target as the "primary" one.

A single-anchor record is the more common case. The constitution does
not privilege either.

---

## 6. Granularity choice — when which level

Stewards face a choice on every commentary record: at what level to
anchor. The archive offers guidance, not law.

| If the comment is about… | Anchor at… |
|---|---|
| The work as a whole | `text` |
| A specific translation's overall character | `translation` |
| A multi-volume work's volume division | `volume` |
| One discrete narrative | `tale` (for Jātaka, hadith collections) or `chapter` |
| One reader-facing passage | `passage` |
| A specific phrase or word inside a passage | `passage` + `:phrase=` sub-locator |
| A pair of locations across texts | multi-anchor `parallel` |
| An abstract concept that appears in many places | `concept` |
| A specific person who appears in many places | `entity` |

The **default heuristic** is: anchor at the smallest unit that fully
contains what the comment is about. A philological note about one
word anchors at the phrase level. A note about how a tale's whole
narrative arc plays out anchors at the tale level. Anchoring too
broadly hides the comment from readers who care about its specific
target. Anchoring too narrowly can split a single point of
observation into many redundant records.

---

## 7. Anchor resolution

The resolver — implementation-deferred — must obey these rules:

1. **Determinism.** Given a corpus state and an anchor, the resolver
   produces exactly one resolution or one explicit failure. No
   probabilistic best-guess.
2. **Stability across additive changes.** Adding a new commentary
   record, a new translation, or a new text does not break existing
   anchors.
3. **Explicit failure on missing target.** If an anchor's target
   does not exist (e.g., a passage id that was never created), the
   resolver returns a structured failure, not a fallback.
4. **Read-only over primary.** The resolver may not modify any
   primary record while resolving, period.
5. **Verbatim sub-locator matching.** Phrase locators match the
   passage text exactly. The archive does not "fuzzy-match."

When the corpus changes destructively (a passage is restored, a
translation is re-ingested), the anchors that pointed at the
affected passages are **explicitly migrated** by the restoration
pass, with the old anchors recorded in the restoration document.
Existing commentary records are not silently re-pointed.

This is the citation-permanence commitment in practice. If a
passage's id must change, the previous id is recorded as an alias.
The old anchor still resolves; it resolves to the same content as
before, via the alias table.

---

## 8. Inverse navigation

Commentary attachment is one-directional: a commentary record names
its anchors, but a primary passage does not list the commentary
records that point at it.

The renderer builds the inverse index dynamically by scanning
commentary records. This means:

- Adding a commentary record does not modify any primary file.
- Removing a commentary record does not require touching primary
  files.
- Two stewards writing commentary on the same passage do not edit
  the same file.

This is a constitutional consequence of `COMMENTARY_CONSTITUTION.md
§4`'s non-destructive requirement, expressed in storage terms.

The inverse index is the renderer's responsibility. It is rebuilt
from the canonical record set on demand; it is not a stored
authoritative artifact. If the inverse index disagrees with the
canonical record set, the canonical record set wins.

---

## 9. Anchor opacity

A reader looking at a commentary record's anchor sees a structured
identifier, not free-form prose. A reader looking at the rendered
commentary attached to a passage sees a footnote or marginal note,
not the anchor itself.

This is deliberate. Anchors are machine-readable; the surface
presentation is human-readable. The archive does not expose the
anchor format to the reader except by deliberate request (a
"show citation" toggle), because anchors are not the point —
*resolving* them is.

A commentary record may carry a human-readable reference text in
addition to its structured anchor (e.g., `"reference_text": "Q 2:255
(Saheeh Intl.)"`). The reference text is for display only; the
anchor is for resolution. Both belong on the record.

---

## 10. Forbidden anchor forms

The following are **not** valid anchors, even though they may look
plausible:

- **Free-text descriptive references** like *"the passage about
  Vessantara giving away his children"*. The archive does not
  resolve descriptions; it resolves identifiers.
- **Page-number references** that are not bound to a specific
  translation's pagination. *"Page 247 of the Pāli Text Society
  edition"* is fine in the body of a commentary record, but the
  *anchor* must be a passage id, not a page number.
- **Translator-agnostic passage references** when the comment is
  translation-specific. *"Qur'an 2:255 in 'the Qur'an'"* is
  insufficient if the comment is about wording; the anchor must
  name the translation.
- **Fuzzy ranges** like *"verses 5-ish"*. Ranges are inclusive and
  exact.
- **Conditional anchors** like *"if this verse is by Paul, then…"*.
  The condition belongs in the commentary body; the anchor must be
  unconditional.

The constitution requires explicit, stable, non-destructive
anchors. Any anchor form that compromises any of those three is
forbidden.

---

## 11. The Reading Room and entity.html

The Reading Room (`workspace-hub/archive/`) currently links into the
canonical library by a thin convention:

```
entity.html?id=<text-id>
```

The Reading Room's `library_id` frontmatter field plays the role of
a text-level anchor today. This is a *de facto* commentary
attachment: each Reading Room entry is, structurally, a commentary
record (with its own provenance, body, and target) anchored at the
`text` level.

When the formal commentary architecture is implemented, the Reading
Room's existing pattern can be expressed in the new model:

```
anchor: archive:text:<library_id>
```

with the Reading Room's `library_chapter` becoming a chapter or
passage anchor where appropriate. Migration is incremental, per
Reading Room entry, and follows the same restraint the SIS v1
migration follows.

Until the commentary architecture is implemented, the existing
`library_id` + `library_chapter` convention is the de facto anchor.
This document specifies the formal model; the implementation does
not yet exist.

---

## 12. Closing note

Attachment is the load-bearing part of commentary architecture. A
commentary record is, structurally, *its body* plus *its
provenance* plus *its anchor(s)*. The body and provenance are
relatively simple; the anchor is what makes commentary a *layer*
rather than a *blog about a corpus*.

The model described here is intentionally close to existing patterns
in the archive — passage ids, the `apparatus_file` mechanism, the
double-colon translation separator. It does not invent vocabulary
where the archive already has working vocabulary. It does not allow
anchors that the constitution forbids.

The implementation, when it comes, will live alongside the existing
apparatus layer, sharing its discipline.
