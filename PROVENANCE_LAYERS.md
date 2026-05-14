# Provenance Layers

*v1 · 2026-05-14 · constitutional and architectural; no implementation yet.*

The archive holds seven layers of authorship. They are listed in
order of their relationship to the primary text — from "the source
itself" to "a reader's private margin note" — but the order is
**not a ranking of value**. The order is descriptive, not
evaluative. Each layer has its own legitimate use; none is silent.

This document defines what each layer holds, how it is identified,
how it is displayed, and what citation rules apply. The
constitutional commitment from `COMMENTARY_CONSTITUTION.md §5`
governs:

> These layers are **never visually or structurally collapsed**.
> A reader looking at a passage with overlays must be able to see, at
> a glance, which voice is speaking.

The implementation of *how* layers are visually distinguished is
the renderer's. The constitution requires only that distinction be
*possible* — that the data model carries every record's layer
explicitly.

---

## 1. The seven layers

| # | Layer | One-line description |
|---:|---|---|
| 1 | **Primary text** | The source. The canon. |
| 2 | **Source apparatus** | Material bound to the source by its publisher (translator footnotes, critical-edition variants). |
| 3 | **Traditional commentary** | Works produced within the textual tradition (tafsīr, ṭīkā, gemara, midrash, patristic exegesis, sūtra commentary). |
| 4 | **Modern scholarship** | Academic studies external to the tradition. |
| 5 | **Archive editorial notes** | The archive's own stewards' notes, recording decisions, observations, restoration history. |
| 6 | **AI-generated interpretation** | Explicitly labelled large-language-model output. |
| 7 | **User/private annotations** | A reader's own notes, by default private. |

The seven were six in the original constitutional draft; the
"source apparatus" layer (#2) was given its own row in this
document to distinguish it from "traditional commentary" (#3),
because the two travel by different rules even though they look
similar to a casual reader.

---

## 2. Layer 1 — Primary text

### What it is

The text the archive exists to preserve. Currently 1,132 canonical
`text.json` files representing 1,086 distinct works. Each work in
each translation has a `passages_<translation>.json` file. The
passages are the primary record. They are the thing the integrity
proof verifies, the thing the restoration documents commit to
preserving, the thing the bare-canon guarantee protects.

### Identity

A primary record is identified by its `text-id::translation-id::
passage-id` triple. No author is named in the record because the
authorship is recorded elsewhere — in the `text.json`'s
`translation.translator` field and `source` object. The passage
record itself is voice-neutral; the voice is the named translation's.

### Display rules

- **Always shown when toggled on.** The bare-canon guarantee
  requires this layer to be available in every reader, every
  exporter, every print edition.
- **Visually unmarked.** Primary text uses the renderer's body
  text style. Other layers are visually distinct *from* primary
  text, not the other way around.
- **No inline editorial marks.** Page brackets like `[479]` from
  OCR scans are preserved in the source and may be stripped at
  render time only; they are not edited into the canonical record.

### Citation

A primary passage is cited by its anchor:
`archive:passage:<text-id>::<translation-id>::<passage-id>`. The
anchor is permanent. The constitution requires that anchor to
resolve forever; restoration passes that change passage ids must
record aliases.

### Refusals

- The archive does not modify primary records. Restoration passes
  may re-key, but the body is preserved verbatim. See the Jātaka
  Vol 6 acquisition for an example of how OCR drift is preserved
  rather than corrected.
- No layer may overwrite a primary record. Lower-layer additions
  are stand-off, by reference, never inline.

---

## 3. Layer 2 — Source apparatus

### What it is

Material that the primary source published *with* the primary text,
in the same book, by the same publisher: a translator's footnotes
(Müller's notes to the SBE translations); a critical edition's
apparatus criticus (Lobel-Page on Sappho); a translator's
introduction (Cowell's editor's preface to vol 1); page boundary
markers from a printed edition.

These records are not separately authored. They are part of the
named source's publication and inherit its provenance.

### Where it lives

The existing `apparatus_*.json` files under canonical text
directories (see `01_library/library/SCHEMA.md`). One precedent
already exists: `upanishads-muller-part2`'s apparatus.

### Identity

An apparatus record is identified by its `text-id::translation-id::
apparatus-id` triple. The apparatus body is verbatim from the
publication. The surrounding fields (id, page, index, anchors,
source) are the archive's voice.

### Display rules

- **Indented or marginal**, distinguished visually from primary
  text but not strongly. Apparatus is "close" to its primary text;
  the typographic relationship should reflect that.
- **Optionally toggled.** A reader may want to read primary text
  without apparatus, even when the apparatus was published with it.
- **The body is the publisher's, not the archive's.** Verbatim
  preservation rules apply.

### Citation

`archive:apparatus:<text-id>::<translation-id>::<apparatus-id>`.

### Refusals

- The archive does not impose semantic typing on apparatus
  records. (Constitution §8.)
- The archive does not separate "good" apparatus from "bad." All
  published apparatus is preserved.

---

## 4. Layer 3 — Traditional commentary

### What it is

Commentary produced **within** a textual tradition, by authors who
were operating within it. The Jātakaṭṭhakathā on the Pāli Jātaka.
The Tafsīr Ibn Kathīr on the Qur'an. The Sefer ha-Aggadah on the
Talmud. Augustine on the Pauline epistles. The Adi-Sankara bhāṣya
on the Brahma Sutras.

This is the largest acquisition gap the archive currently has.

### Where it lives

Each traditional commentary work is, in the archive, **its own
primary text**. Ibn Kathīr's tafsīr is its own canonical-library
text.json + passages files, with Ibn Kathīr named as the author.
What makes it "commentary" is that its records anchor at the
Qur'an's records — but structurally it is a Layer-1 primary text
in its own right.

A "commentary record" in the formal Layer-3 sense is, then, a
**relationship**: an anchor saying *"this passage of Ibn Kathīr is
commenting on this verse of the Qur'an."* That relationship is the
commentary attachment. The body content stays in the traditional
commentary's own primary record.

### Identity

A Layer-3 commentary attachment is identified by:

- the source commentary's passage anchor (Layer 1, in the
  commentary's own canonical record)
- a target anchor (the passage being commented on, in the
  archive)

A Layer-3 record carries *no body of its own*. The body is in the
source commentary work. The attachment record is the bridge.

### Display rules

- **Side-by-side or interleaved.** Traditional commentary,
  historically, is read alongside its primary text. The Talmud's
  page layout, the Mishneh Torah's marginal commentary blocks, the
  Sanskrit *mūla*-with-*bhāṣya* presentation — these are
  centuries-old solutions.
- **Tradition-attributed.** The renderer must always show *whose*
  traditional commentary this is.
- **Multiple commentaries on the same passage shown together** or
  selectable. The plurality principle (`COMMENTARY_CONSTITUTION.md
  §9`) demands it.

### Citation

The attachment record: `archive:commentary:<attachment-id>`.
The body: `archive:passage:<commentary-text-id>::<trans-id>::<passage-id>`.
A citation can resolve either; they refer to different things
(the relationship vs the prose).

### Refusals

- The archive does not rank traditional commentaries.
- The archive does not omit a commentary tradition because the
  steward disagrees with it.
- The archive does not flatten Sunni and Shia tafsīr into "tafsīr",
  Theravada and Mahayana abhidharma into "Buddhist commentary," or
  rabbinic and patristic exegesis into "religious commentary." Each
  tradition is named.

---

## 5. Layer 4 — Modern scholarship

### What it is

Academic studies, journal articles, monographs, encyclopaedia
entries, and named scholarly observations made **outside** the
tradition. A Cambridge History of Religion chapter on Vessantara.
A philological note on a contested verse. A comparative-religion
essay on parallel motifs.

### Where it lives

Each modern scholarly work is, like traditional commentary, either:

- a full primary text in the archive, when the work is large and
  worth full ingest (a monograph, a critical edition), or
- a commentary record carrying its own body, when the work is
  small enough that ingesting it as a separate primary text would
  be over-structured (a single article, a footnote in a journal).

The decision is per-work and follows the steward's judgment. The
small-record form is more common.

### Identity

A Layer-4 commentary record carries:

- a stable record id
- a body (the scholarly text, verbatim where possible)
- an author (a named scholar or a named institution)
- a source citation (journal, year, page)
- one or more anchors

### Display rules

- **Footnoted or expandable.** Modern scholarship is conventionally
  read as a footnote or an expandable inline note.
- **Author-attributed.** The renderer must show the scholar's name
  and the year.
- **Distinct from traditional commentary.** Whether by typography
  (a different sidebar, a different font weight) or by labeling,
  the reader must be able to tell at a glance that this is modern,
  not traditional. Different reading rules apply.

### Citation

`archive:commentary:<commentary-id>` for the record;
`archive:scholar:<scholar-id>` for the author entity.

### Refusals

- The archive does not curate modern scholarship for ideological
  alignment.
- The archive does not present *consensus* modern scholarship as
  more authoritative than minority modern scholarship; both are
  recorded, both are displayed, the reader weighs them.

---

## 6. Layer 5 — Archive editorial notes

### What it is

The archive's own stewards, recording the archive's own decisions.
A note explaining why one translation was chosen over another; a
note that the OCR of *MtJGA-PAKKHA-JATAKA* preserves the scanner's
misreading; a note that the SacredTexts variants of the Qur'an
were marked `provisional` after a 2026-05 review; a record of which
restoration passes touched which files.

This is the layer that the existing restoration documents
(`QURAN_RESTORATION_2026.md`, `JATAKA_RESTORATION_2026.md`,
`JATAKA_VOL6_ACQUISITION_2026.md`, etc.) live in conceptually. Those
documents are the human-readable narratives; the per-text editorial
records are the machine-readable counterparts.

### Where it lives

In a sibling-to-apparatus layer, with one record per editorial
claim. The narrative documents (the Markdown restoration notes)
remain at the project root for reading; the structured editorial
records anchor at specific texts/passages.

### Identity

A Layer-5 editorial record carries:

- a stable record id
- a body (the steward's prose, verbatim — the steward's voice)
- an author (a named steward, e.g., `archive:steward:steve`)
- a date
- a category (typically `restoration`, `editorial`, `provenance`)
- one or more anchors

### Display rules

- **Marked clearly as archive voice.** No reader should mistake an
  archive editorial note for traditional commentary or modern
  scholarship. The visual style should signal "this is the
  archive's own voice."
- **Toggleable but on by default for stewards.** A casual reader
  may not need to see them; a steward navigating the archive does.
- **Dated.** The date matters: archive editorial decisions in 2026
  may be revised by future stewards.

### Citation

`archive:commentary:<commentary-id>` with provenance layer set to
`archive:editorial`.

### Refusals

- An editorial note does not modify primary text or apparatus
  records.
- An editorial note's claims are not promoted to traditional
  commentary or modern scholarship by passage of time. They remain
  Layer 5 even when republished as institutional documents.
- Stewardship is **named**. Anonymous editorial notes are not
  allowed.

---

## 7. Layer 6 — AI-generated interpretation

### What it is

Output of large language models, generative systems, or any
automated interpretive process. Suggestions for cross-references,
draft glosses, draft translations, motif identifications. Any
content not authored by a human or by a published source.

### Where it lives

In a sibling layer, with one record per AI-generated artifact.
**Always labelled.** Always attributed to a named model and a
date. Always quarantined from the other layers.

### Identity

A Layer-6 record carries:

- a stable record id
- a body (the model's output, verbatim)
- the model identity (e.g., `claude-opus-4-7@2026-05-14`)
- the prompt context, when reproducible
- a date
- a category (where useful)
- one or more anchors
- **a quarantine flag** indicating this is AI-generated

### Display rules

- **Visually quarantined.** A different background tint, a different
  icon, a "machine-generated" banner. The reader must know
  immediately that this is AI output, not human commentary.
- **Off by default.** Even in reader views that show overlays,
  Layer 6 starts collapsed. The reader opts in to see AI output.
- **Never merged.** AI output is never silently rewritten and
  reclassified into another layer. If a human steward decides an AI
  suggestion is correct and wants to endorse it, the steward
  authors a new Layer-5 editorial record citing the AI suggestion;
  the original Layer-6 record stays. Two records, two voices.

### Citation

`archive:commentary:<commentary-id>` with provenance layer set to
`archive:ai`.

### Refusals

This is the most restrictive layer. The archive refuses to:

- Display Layer-6 content unlabeled.
- Promote Layer-6 content to higher layers silently.
- Use Layer-6 to fill gaps in primary text (no AI-completed
  passages, no AI-translated passages, no AI-restored corrupted
  scans).
- Cite Layer-6 records as authoritative.
- Train future models on Layer-6 records without disclosing it.
- Auto-generate Layer-6 content over the entire corpus without
  stewardship review.

The default disposition toward AI output is: **record it, label it,
keep it small, and require explicit human action to elevate it.**

---

## 8. Layer 7 — User / private annotations

### What it is

A reader's own notes on the corpus. A teacher's marginal note on
a passage they assigned. A bookmark. A reading-rhythm tag (e.g.,
"come back to this"). A personal interpretive note never intended
for public display.

### Where it lives

In storage local to the reader, not in the canonical archive.
Either:

- in browser local storage (the simplest case),
- in a synced file on the reader's own device, or
- in a future export format the reader controls.

The canonical archive **does not store** private annotations by
default. They are the reader's; the archive does not collect
them.

### Identity

A Layer-7 record carries:

- a stable record id (local to the reader's storage)
- a body
- a date
- one or more anchors

### Display rules

- **Visible only to the reader.** The renderer surfaces private
  annotations on the reader's own device. The archive's public
  surfaces never display them.
- **Distinct from all other layers.** The reader must be able to
  tell their own notes apart from any layer the archive provides.
- **Exportable.** A reader who wants to take their annotations
  elsewhere must be able to. The format is their property.

### Citation

`local:annotation:<annotation-id>` — not in the `archive:`
namespace. The format signals that the record is outside the
archive's canonical record set.

### Refusals

- The archive does not silently sync private annotations to its
  servers. A reader who wants to back up annotations does so
  consciously.
- The archive does not surface one reader's annotations to another.
- A reader's private annotations are not promoted to Layer 5 by
  the archive's choice; if a reader wants their notes to become
  archive editorial notes, that's a deliberate steward action.

---

## 9. The non-collapse rule, technically

A record's layer is recorded in two places:

1. The **record's own field** (e.g., `provenance.layer: "modern-scholarship"`).
2. The **directory or file structure** that holds it (e.g., editorial
   notes in a separate `editorial_*.json` sibling file to
   `apparatus_*.json`).

Both encodings agree. The directory-or-file encoding is the canonical
one for resolving ambiguity; the field is for record-level
self-description.

The renderer reads the layer and applies the display rules. No
data-level operation may strip the layer field or move a record
into the wrong file. The integrity proof of the commentary layer
includes a check that every record's `provenance.layer` matches the
file it lives in.

---

## 10. Migration and re-layering

Records are not **silently** re-layered. A piece of content that
arrives in one layer stays in that layer unless an editorial act
explicitly moves it.

The acceptable transitions:

- Layer 6 (AI) → Layer 5 (editorial): a steward reviews an AI
  suggestion, decides it is correct, authors a new Layer-5
  record citing the AI source. The original Layer-6 record stays.
- Layer 7 (private) → Layer 5 (editorial): a reader who is a
  steward decides to publish their note. They author a new Layer-5
  record. The Layer-7 record may remain or be deleted by the
  reader; the archive does not retain or remove it.
- Layer 4 (scholarship) → Layer 3 (traditional commentary): a
  scholar's interpretation, by passage of time, becomes a
  tradition's view. **This transition the archive refuses to make
  automatically.** A scholar named in 2026 is a Layer-4 author
  forever in the archive. Future stewards may write Layer-5 notes
  observing that the scholar's reading has been adopted by a
  community, but the layer assignment does not migrate.

The unacceptable transition:

- Layer N → Layer 1 (primary text). **Never.** No commentary is
  ever promoted into the primary record. The constitution forbids
  it.

---

## 11. Citation across layers

A citation may reference a record in any layer. The citation format
includes the layer implicitly via the anchor's target-kind:

- `archive:passage:<…>` → Layer 1
- `archive:apparatus:<…>` → Layer 2
- `archive:commentary:<…>` with `layer: traditional` → Layer 3
- `archive:commentary:<…>` with `layer: scholarship` → Layer 4
- `archive:commentary:<…>` with `layer: editorial` → Layer 5
- `archive:commentary:<…>` with `layer: ai` → Layer 6
- `local:annotation:<…>` → Layer 7 (outside archive namespace)

A scholar in 2080 citing the archive's record of an AI suggestion
on a Jātaka tale is citing a Layer-6 record — and the citation
resolves to *exactly the AI's output as it stood at the time of
recording*, with the model's identity, the date, and the prompt
context preserved. The future scholar can decide what to make of
it; the archive's job is to preserve what was said.

---

## 12. Closing note

The layer system is the archive's commitment to honesty about
authorship. A reader of this archive in 2126 is owed not just the
texts but the **provenance of every claim made about them** —
the names, the dates, the institutional positions, the AI models,
the editorial decisions. The seven-layer system makes that
provenance machine-readable and visually surfaceable.

The archive is not neutral. Every editorial choice is a choice.
What the archive promises is **transparency about its choices**:
to record them, to name them, to keep them distinguishable from
every other layer. That is the function of the layer system.

The implementation, when it comes, must respect every layer. A
reader of the future, looking at a passage with all seven layers
on, should see the primary text in the center and the centuries
of commentary around it, each in its own voice, none speaking over
the canon.
