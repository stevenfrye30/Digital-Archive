# Commentary Constitution

*v1 · 2026-05-14 · constitutional and architectural; no implementation yet.*

The archive's primary texts are sovereign. Commentary may surround
them, layer onto them, point at them, frame them. Commentary may
never **mutate** them — not by replacement, not by normalization, not
by harmonization, not by summary, not by silent correction.

This document defines the constitutional law under which all
commentary, annotation, apparatus, scholarly note, semantic overlay,
and interpretive surface in the archive operates. It is foundational.
Every implementation choice that follows must agree with it. Where a
later document, schema, or interaction layer disagrees with the
constitution, the constitution wins.

It is **not** a feature specification. It is the rule the features
must obey.

---

## 1. What this document is for

To make four guarantees to a future reader, including a reader a
century from now:

1. **The primary text is the primary text.** Whatever else the
   archive does, a reader can always reach the bare canonical text,
   without any overlay, exactly as it stands today.
2. **Disagreement is preserved, not resolved.** When traditions,
   translators, or scholars disagree, the archive holds the
   disagreement. It does not synthesize one view.
3. **Provenance is permanent.** Every interpretive claim, in any
   layer, carries the name of who said it and where it came from.
4. **Authority layers never collapse.** A reader can always tell
   whether what they are reading is the source, a 12th-century
   commentary, a 21st-century scholar, an editor's note, an AI
   suggestion, or a private annotation.

These are constitutional. They cannot be relaxed by an
implementation decision.

---

## 2. What commentary *is*

A **commentary** in this archive is any addition that:

- references a part of the primary corpus,
- carries its own named provenance, and
- exists in a file or record separate from the primary text it
  references.

A commentary is **about** something. It is not the thing.

A commentary may be:

- a footnote that clarifies a passage,
- a 12th-century gloss on a verse,
- a translator's note that originally appeared in the printed source,
- a modern scholarly observation,
- a cross-reference to another text,
- a tag that identifies a person, place, motif, or concept,
- a semantic-graph attachment,
- a steward's editorial note recording a decision,
- a reader's private annotation,
- an explicitly labelled AI-generated suggestion.

In each case, the commentary's record is **distinct from the primary
text record**. The primary text does not change because a commentary
is added.

---

## 3. What commentary *is not*

A commentary is **not**:

- a **replacement** for primary text. No commentary record may
  overwrite, hide, or substitute a passage.
- a **rewrite** of primary text. The archive does not "improve" or
  modernize the source. Spelling, diacritics, punctuation,
  italicization, and verse numbering follow the source.
- a **summary** that stands in for the primary text. Summaries may
  exist (clearly labelled), but the primary text is always reachable
  beside them.
- a **harmonization** of multiple translations. The archive preserves
  every translation it holds in its own voice; it does not produce a
  "best translation" by averaging.
- an **opinion** rendered as fact. Where an interpretive claim is
  contested, the archive records the contest, not the verdict.
- a **silent correction**. If a primary text has an OCR error, a
  manuscript variant, a known mistranslation, or a contested
  passage, the archive records the issue beside the text, not in it.

---

## 4. What commentary may attach to

Commentary anchors to addressable units of the corpus. The set of
addressable units is enumerated in **`COMMENTARY_ATTACHMENT_MODEL.md`**.
The constitution does not list them here, but it requires that:

- every anchor be **stable**: a commentary that points at
  `quran::saheeh::2.255` must continue to resolve to that passage
  through any future restoration, refactor, or schema change.
- every anchor be **explicit**: no commentary may anchor "to the
  area around verse 5." The targeted unit must be named.
- every anchor be **non-destructive**: anchoring a commentary to a
  passage may not modify the passage's `text`, `id`, `path`, or
  `order` fields.

Citation permanence is a constitutional commitment, on the order of
the integrity proof itself.

---

## 5. Authority levels

The archive distinguishes six layers of authorship. They are listed
in **`PROVENANCE_LAYERS.md`** in detail. The constitution names them
here in order:

1. **Primary text** — the source. Sovereign.
2. **Source apparatus** — material bound to the primary source
   itself (a translator's footnotes, a critical edition's variant
   readings). Carries the primary source's authority, attached to it
   by the publisher.
3. **Traditional commentary** — works produced within the textual
   tradition (tafsīr, ṭīkā, gemara, etc.). Each is itself a primary
   text in this archive, with its own provenance, that happens to
   reference another.
4. **Modern scholarship** — academic studies external to the
   tradition.
5. **Archive editorial notes** — the archive's own stewards
   recording decisions, observations, restoration history.
6. **AI-generated interpretation** — any large-language-model
   output, always labelled, never adopted into another layer.
7. **User/private annotations** — a reader's own notes, by default
   visible only to them.

These layers are **never visually or structurally collapsed**. A
reader looking at a passage with overlays must be able to see, at a
glance, which voice is speaking. Display rules belong to
`PROVENANCE_LAYERS.md` and the renderer; the constitution requires
only that distinction be possible.

---

## 6. The bare-canon guarantee

At any time, a reader of this archive must be able to:

- read **any passage** in its original published form,
- with **no commentary visible**,
- with **no AI-generated overlay**,
- with **no editorial gloss** changing the text,
- with the **exact bytes** that the integrity proof verifies.

This is the bare-canon guarantee. It is the reason the archive
exists. Any feature, any overlay, any commentary system that
threatens this guarantee is non-constitutional and must be redesigned
or removed.

The renderer may default to showing some overlays. The user must be
able to turn them all off. The corpus must remain readable in that
state.

---

## 7. Verbatim discipline (extended from `apparatus_file`)

The existing `apparatus_file` pattern (see `01_library/library/SCHEMA.md`)
already states:

> The apparatus file holds Müller-voiced (or analogous translator-
> voiced) content **verbatim**. The archive imposes no semantic typing:
> there is no `kind`, `category`, or `function` field on apparatus
> records. … The body field is the witness's voice; the surrounding
> structural fields (`id`, `page`, `index`, `anchors`, `source`) are
> the archive's voice.

This discipline extends to commentary. Specifically:

- A commentary record's **body** field — the actual prose or claim —
  is recorded verbatim from its named source whenever such a source
  exists.
- A commentary record's **structural** fields (anchors, layer,
  provenance, timestamp) are the archive's voice. These may be
  edited, re-indexed, or normalized over time.
- Where a commentary record represents an archive-original claim
  (e.g., a steward's editorial note), the **body** is the steward's
  voice, recorded with a date and an identity.
- Where a commentary record represents an AI-generated claim, the
  **body** is the AI's text, recorded verbatim, with the model name,
  prompt context, and date.

The archive **records voices**. It does not improve them.

---

## 8. The anti-classification preference

The apparatus pattern's most important institutional commitment is
this:

> The archive imposes no semantic typing. … Functional heterogeneity
> within an apparatus tradition is preserved as ambiguity, not
> resolved by editorial classification.

This is a deep constitutional principle and is *partially* extended
to commentary, with a careful qualification.

**For source-internal apparatus and traditional commentary**, the
preference is to preserve the witness's voice as-is, without
imposing the archive's categorical scheme on it. Müller's footnotes
are not labelled "philological" vs "doctrinal" by the archive,
because Müller did not label them so himself.

**For archive-added commentary and modern scholarship**, the archive
*may* attach categorical metadata, because the category is then
itself a steward's claim with its own provenance, not a re-labeling
of the witness's voice.

The general rule: **classification is part of the archive's voice,
not the witness's.** When an apparatus or commentary record
classifies something, the classification must be attributable to a
named author — the steward, the modern scholar, or the explicit AI
agent — never silently imposed on a source author who did not
classify their own work.

`COMMENTARY_ONTOLOGY.md` describes the categories the archive uses
when classifying. The constitution requires only that every
classification be voice-attributed, never anonymous.

---

## 9. The plurality principle

The Quran has many tafsīr. The Bible has many commentaries. The
Upanishads have a thousand years of ṭīkā tradition. The Jātaka has
the Jātakaṭṭhakathā. A great civilizational text is rarely
mono-commentary.

The archive **expects plurality**. Two commentaries may disagree on
a passage's meaning. Both are recorded. Neither is privileged. The
renderer may show both side-by-side, or one at a time, or filter by
tradition — but never silently choose one as canonical.

A future commentary acquisition that arrives with a position must
not be ranked above existing commentary of equal authority. Authority
is a property of the layer (per §5), not of the position.

This applies symmetrically to translations: if two translations
disagree on a passage's rendering, both stand. The archive does not
choose.

---

## 10. The refusal index

The archive refuses to do certain things on principle. These
refusals are listed in detail in `INTERPRETIVE_BOUNDARIES.md`. The
constitution names six refusals here, as foundational:

1. **No silent correction.** Manuscript errors, OCR drift, archaic
   spelling, contested readings — all stay as found, flagged by
   commentary if needed, never edited in place.
2. **No harmonization.** Disagreeing translations or commentaries
   coexist; the archive does not produce a synthesized version.
3. **No modernization.** The archive does not "update" language to
   contemporary registers. A 1611 KJV is a 1611 KJV.
4. **No unlabelled AI.** Any LLM-generated content is explicitly
   labelled and attributed to a named model and date. AI output is
   never merged into another layer.
5. **No auto-classification of source-internal material.** See §8.
6. **No erasure of minority traditions.** A commentary tradition's
   presence in the archive is not contingent on the steward's
   endorsement of its views.

These refusals are constitutional. They are not subject to feature
trade-offs.

---

## 11. Future-readability commitments

Two long-horizon commitments shape every implementation choice:

- **Citation permanence.** A reference to a primary passage made
  today must resolve in ten, fifty, a hundred years. Identifiers do
  not get renamed for aesthetic reasons. Where they must change,
  redirection is recorded; the old identifier does not disappear.
  See `COMMENTARY_ATTACHMENT_MODEL.md` for anchor format.
- **Format portability.** The archive's interpretive layer must be
  serializable in formats that long-survive any specific tool. JSON
  with named fields, plain UTF-8 text, version-pinned schemas. No
  proprietary binary formats, no platform-locked storage, no
  authentication-required surfaces for the canonical record.

A future steward must be able to ingest the entire interpretive
corpus of this archive into a tool that does not yet exist, without
loss.

---

## 12. Relationship to the existing schema

The constitution does **not** modify the current
`01_library/library/SCHEMA.md` contract. It extends it. Specifically:

- `apparatus_file` continues to operate exactly as documented.
  Apparatus is the most authoritative non-primary layer.
- The interpretive surface designed under this constitution is a
  **new sibling** to the apparatus layer, not a replacement. Schema
  evolution that adds commentary records will be additive: existing
  text.json, passages_*.json, and apparatus_*.json files remain
  valid.
- The Reading Room's STANDARD.md §5 "Commentary rule" already
  establishes that commentary "explains a text. It does not serve as
  primary evidence." That rule is constitutional and is hereby
  reaffirmed for the archive as a whole.

The implementation decisions belong to later phases. The constitution
fixes the floor; the future builds upward from here.

---

## 13. Amendment

This document is amendable. The amendment discipline is the same as
restoration: changes are dated, attributed, recorded in the
stewardship log, and accompanied by an explanation of why the
previous version was insufficient. Existing commentary records
continue to operate under the constitution that was in force when
they were written; migration to a newer constitution is a deliberate
editorial pass, never silent.

The constitution is short on purpose. Most of the real architectural
work belongs to the four sibling documents:

- **`COMMENTARY_ONTOLOGY.md`** — categories of commentary and the
  judgments that shape them.
- **`COMMENTARY_ATTACHMENT_MODEL.md`** — granularity, anchors, and
  what may be referenced.
- **`PROVENANCE_LAYERS.md`** — the six layers, their display rules,
  and their citation rules.
- **`INTERPRETIVE_BOUNDARIES.md`** — what the archive refuses to do,
  in full.

These four documents must be read together. The constitution is
their preamble.

---

## 14. Closing note

The archive is not a content platform. It is not a search engine
for religious quotations. It is not a recommendation system. It is
not a tool for producing the *best* interpretation of any text.

It is a long-term memory structure — for civilizational texts and
for the layers of thought built around them.

A reader in 2126 should be able to open this archive and find:

- the Qur'an as Saheeh translated it in 1997, exact to the byte;
- the Vessantara-jātaka as Cowell and Rouse rendered it in 1907,
  preserved through the OCR noise their print suffered;
- the Mishnah, the Pirke Avot, the Augustine, the Plato, the
  Daodejing — each in their own voice;
- and beside each of these, the layers of interpretation that the
  centuries placed on them, each layer attributed, each layer toggleable,
  none of them speaking over the canon.

That is the archive this constitution serves.
