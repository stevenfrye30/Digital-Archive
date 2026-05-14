# Interpretive Boundaries

*v1 · 2026-05-14 · constitutional and architectural; no implementation yet.*

This document records what the archive **refuses to do**, and why.

It is the shortest of the four sibling architectural documents,
because refusals do not need extensive justification — only clarity.
What needs to be refused, and the reason for the refusal, can usually
be stated in a paragraph.

The constitutional law that frames this work is in
`COMMENTARY_CONSTITUTION.md`; the layers that organize what counts as
"interpretation" are in `PROVENANCE_LAYERS.md`. This document
operates under both.

A refusal in this archive is not a limitation. It is a structural
commitment. The archive's identity is partly defined by what it
declines to do.

---

## 1. The shape of a refusal

Every refusal in this document has three parts:

- **What the archive refuses to do.**
- **Why.** Usually: because doing it would compromise a higher
  constitutional commitment.
- **What to do instead**, where there is something to do.

Some refusals have no "instead." That is itself a constitutional
claim: there are some things the archive simply does not do.

---

## 2. Refusals on the primary text

### 2.1 The archive refuses to modify primary text.

Once a passage is in the canonical record set, its `text` field is
immutable except through a deliberate restoration pass — and even
then, the restoration must preserve the original under a snapshot
and document its reasons in the stewardship log.

**Why.** Citation permanence. Trust. The bare-canon guarantee.

**Instead.** Issues with primary text (OCR errors, contested
readings, manuscript variants) are recorded as commentary records
beside the text, not edits in the text.

### 2.2 The archive refuses to modernize language.

A 1611 KJV stays as a 1611 KJV. A 1907 Cowell translation stays as
a 1907 Cowell translation. The archive does not "update" archaic
spellings, replace "thee" with "you," restore diacritics that the
source did not have, or normalize translator idiosyncrasy across
volumes.

**Why.** Every "improvement" to a translation is the
modernizer-not-the-translator's voice. The archive preserves the
translator's voice.

**Instead.** A reader who finds 1611 English difficult can read
another translation. Multiple translations exist precisely for this
reason. The archive holds them all.

### 2.3 The archive refuses to harmonize translations.

When two translations of a single passage disagree, the archive
preserves both. It does not produce a "best translation" by averaging,
selecting, or synthesizing.

**Why.** Translation is interpretation. A harmonized translation is
no one's translation. Future readers deserve to see what each
translator actually wrote, including their disagreements.

**Instead.** A reader interested in comparison reads them
side-by-side. A renderer may help by aligning passage anchors across
translations; the renderer does not produce new text.

### 2.4 The archive refuses to "correct" OCR or scan errors in the primary text.

When a scan reads `MtJGA-PAKKHA-JATAKA` because the M leaked into
the U, the archive records `MtJGA-PAKKHA-JATAKA`. The error is
recorded as found. Where the correction is high-confidence, an
editorial commentary note attached to the passage may say *"OCR
reads MtJGA; canonical Pāli reads MŪGA"* — but the passage itself
is not silently rewritten.

**Why.** A future steward, comparing this archive's record to
another digitization, must be able to see what *this* OCR pass
produced. Silent correction destroys that comparability and that
record of digitization history.

**Instead.** A future "OCR cleanup" pass on a `provisional`-quality
text is a deliberate restoration with its own document, its own
snapshot, and its own published rationale.

### 2.5 The archive refuses to summarize primary text.

A summary is the summarizer's voice. The archive holds primary text,
not summaries of it.

**Why.** A summary, once present, becomes a temptation to read in
place of the text. The archive exists to be read.

**Instead.** Summaries — when they are useful, e.g., for tale-list
navigation — exist as commentary records, explicitly labeled as
summary, attributed to a named author, and toggleable. The bare
canon is always reachable beside them.

---

## 3. Refusals on commentary

### 3.1 The archive refuses to author commentary anonymously.

Every commentary record has a named author. "The archive" is not an
author. "Editor" is not an author. The steward's name (or the
named institution, or the named scholar, or the named model) goes
on every record.

**Why.** Provenance per claim. A reader cannot evaluate a claim
without knowing who made it.

**Instead.** If a steward wishes to publish a note without their
personal name, they may use a named pseudonym, a named institutional
voice, or a named role (e.g., `archive:editor`), but the name is
recorded — and at minimum the date of authorship is.

### 3.2 The archive refuses to rank commentary by authority.

A medieval *tafsīr* and a 21st-century philological note both have
their own provenance; both are recorded; neither is privileged. The
renderer may sort by tradition, date, or layer — but does not assign
a "trustworthiness score."

**Why.** Different readers, different traditions, and different
purposes weight commentaries differently. The archive is not the
arbiter of authority for the world.

**Instead.** Layer assignment (the seven-layer scheme) communicates
*what kind of authority* a record carries — published-with-source vs
traditional vs scholarly vs editorial vs AI vs private — without
ranking within layers.

### 3.3 The archive refuses to flatten tradition lines.

Sunni and Shi'a *tafsīr* are not "Islamic commentary." Theravāda and
Mahāyāna *abhidharma* commentaries are not "Buddhist commentary." A
Rashi and a Maimonides are not "rabbinic commentary." Each
tradition has its own provenance, its own internal disputes, its
own register. The archive records each.

**Why.** Flattening tradition lines hides the disagreements that
make commentary meaningful. The plurality principle requires
distinct traditions to be distinctly recorded.

**Instead.** Tradition is recorded in each work's provenance. A
renderer may filter by tradition, but the underlying records carry
the full tradition identity.

### 3.4 The archive refuses to silently re-classify older commentary.

A record tagged `philological` under v1 of the categorical
vocabulary may, under v2, fit better as `lexical`. The re-tagging
is a new editorial act with its own date and provenance. The
original tag is not deleted; the v1 record continues to carry its
v1 tags.

**Why.** Citation permanence. Versioning honesty. A reader citing a
record's classification in 2030 should still find that
classification in 2080.

**Instead.** Tagging revisions are additive. New tags are added with
the version that introduced them; old tags are archived, not
overwritten.

### 3.5 The archive refuses to compose commentary from other commentary without attribution.

If a commentary record's body draws from another commentary's
content — paraphrasing, quoting, synthesizing — the relationship
must be made explicit. Either by quotation (with the source
anchored as `archive:commentary:<id>` in the body), or by a "see
also" anchor in the record's anchor list.

**Why.** Plagiarism is dishonest in any layer. Silent re-statement
of another author's interpretation, as if it were the steward's
own, is silent re-statement.

**Instead.** Cite. The anchor model exists for this.

---

## 4. Refusals on AI and automation

### 4.1 The archive refuses to display AI-generated content unlabeled.

Every record produced by a large language model (or any generative
system) is marked. The label is visible to the reader. The label
identifies the model and the date.

**Why.** Trust. A reader has the right to know whether they are
reading a human's claim or a machine's.

**Instead.** AI suggestions are Layer 6. They are labelled,
quarantined, and toggleable off.

### 4.2 The archive refuses to use AI to fill gaps in primary text.

No AI-generated passages. No AI-restored missing chapters. No
AI-translated translations. No AI-imagined manuscript variants.

**Why.** A gap in the primary text is itself a record — of what was
not preserved, what was lost, what was never written. Filling it
with AI output destroys that record and replaces a gap with a
fiction.

**Instead.** Gaps are recorded as gaps. Editorial notes may
discuss them. AI may suggest hypotheses (as Layer 6 commentary, not
as primary text). The text remains as it is.

### 4.3 The archive refuses to auto-classify the corpus.

The archive will not run an LLM over every passage of every text
and produce tag-clouds, thematic clusters, sentiment scores, or
"key passages." The corpus is not auto-annotated.

**Why.** Every tag is a claim. Auto-classification means many
claims with weak provenance. The archive prefers fewer claims with
strong provenance.

**Instead.** Steward-reviewed, per-passage editorial decisions, made
by named humans. Slow. Inconsistent. Worth it.

### 4.4 The archive refuses to use AI to generate cross-references at scale.

Cross-references between texts are claims about textual
relationships. They are interpretive. They are not safe to
auto-generate.

**Why.** A claim that *"Qur'an 2:255 parallels Psalm 90"* is an
interpretive claim, not a fact. Auto-generating thousands of such
claims would fill the archive with low-confidence claims indexed by
no one's editorial judgment.

**Instead.** Cross-references are made one at a time, by named
authors, with explicit anchors. AI may suggest candidates as Layer
6 records; a steward may review them; reviewed cross-references
become Layer 5 records with the steward's name on them.

### 4.5 The archive refuses to train future models on its content without disclosure.

If the archive's content is used to train a model (the archive's own,
or another), the use is disclosed in the archive's own stewardship
log. A future model trained on this archive's content carries that
provenance.

**Why.** Symmetry with §4.1: the archive labels AI output for its
readers; it labels its content for AI training in the same spirit.

**Instead.** Training disclosure is recorded as a Layer-5 editorial
note. The archive's content is, generally, public-domain primary
text; the disclosure is not about copyright but about provenance
through subsequent models.

---

## 5. Refusals on user-facing behavior

### 5.1 The archive refuses to "recommend" texts.

No "you might also like" panels. No engagement-optimized reading
paths. No algorithmic shelving.

**Why.** A recommendation is an editorial choice with no named
author. It substitutes machine taste for the reader's own. The
archive is built for slow reading, not maximum engagement.

**Instead.** The Reading Room's curated shelf serves the function a
recommendation system would, in a slower and more honest form: a
named human (the steward) chooses what goes on the front shelf,
publishes their reasons, and lets readers walk further at their
own pace.

### 5.2 The archive refuses to personalize text in ways that hide what is shown to other readers.

What a reader sees on a passage is, by default, the same content
other readers see. The reader may toggle layers, filter by tradition,
collapse overlays — but the underlying record set is the same.

**Why.** Personalization that silently filters content is opaque
filtering. A reader who does not know that other readers see a
different version of the corpus cannot reason about it.

**Instead.** Filtering controls are visible. The reader knows what
they have toggled off. The reader can return to "show everything"
in one click.

### 5.3 The archive refuses to A/B-test on readers.

No experiments. No randomized layout changes. No analytics-driven
feature roll-outs.

**Why.** A/B testing assumes the reader is the subject of an
experiment. The archive does not experiment on its readers.

**Instead.** Changes are made deliberately, documented in
stewardship logs, and explained to anyone reading the project's
restoration documents.

### 5.4 The archive refuses to display ads, accept sponsorships, or commercialize attention.

The archive's surfaces are unsponsored. No promoted texts, no
"sponsored commentary," no commerce embedded in reading.

**Why.** The archive is not a content platform.

**Instead.** Sustainability of the project is a separate, slow
question, addressed by the steward outside the reading surfaces.

---

## 6. Refusals on time

### 6.1 The archive refuses to break old citations.

A citation to a passage made in 2026 must resolve in 2126. If the
passage's id must change in the future, the old id is retained as
an alias. If the file format changes, a migration tool reads the
old format. If the schema evolves, the old schema is documented.

**Why.** Citation permanence is foundational. An archive that
breaks its own citations is not an archive.

**Instead.** Schema evolution is additive. Re-keying is documented
and aliased. Migration is a published act, not a silent one.

### 6.2 The archive refuses to delete editorial history.

A restoration that changes a passage records what the passage said
before and after. A re-classification records the old classification
and the new. A retracted editorial note is *marked retracted*, not
removed.

**Why.** The archive's stewardship history is itself a record. An
archive that erases its own decisions is unreviewable.

**Instead.** Append-only stewardship logs. Retractions are
annotations on records, not removals.

### 6.3 The archive refuses to outsource long-term storage to platforms it does not control.

The canonical record set lives in files the steward controls. A
cloud platform may serve as a publishing surface (e.g., GitHub
Pages today), but the canonical record set is not dependent on any
single platform.

**Why.** A century-scale archive cannot depend on a platform that
has not existed for a century.

**Instead.** The canonical record set is plain text files (JSON,
Markdown, UTF-8) in a version-controlled repository, exportable
without loss to any reasonable future storage. The publication
surface can change; the canon survives.

---

## 7. Refusals on scope

### 7.1 The archive refuses to be a search engine for religious quotations.

Search exists in the renderer for navigability. But the archive
does not optimize itself for "find a verse for any occasion." A
verse pulled out of context, presented as a snippet for a sermon
or a meme, is the kind of use the archive is not designed for and
does not invite.

**Why.** Civilizational texts deserve to be read in the structure
their tradition holds them in.

**Instead.** Reading paths that move through chapters, tales,
sections — not search results that pluck verses.

### 7.2 The archive refuses to be a teaching curriculum.

The archive does not assert "you should read X next" or "the
canonical reading list for understanding Y is …". Reading lists
are pedagogical choices; the archive holds texts, not pedagogies.

**Why.** Different traditions, different teachers, different readers
will all assemble different reading lists from the same archive.
The archive's neutrality on assemblage is part of its
preservation function.

**Instead.** A teacher building a reading list may publish their
list — as commentary, as an external document, as a Reading Room
shelf they curate — but the archive itself does not generate one.

### 7.3 The archive refuses to be the final word on any text it holds.

The archive holds *this* version of *this* translation, with *this*
provenance, and as much commentary as has been recorded. It does
not claim to hold the definitive version of any text, the
authoritative interpretation of any passage, or the complete
commentary on any work.

**Why.** No archive can be the final word. The honest disposition
is humility.

**Instead.** Where the archive's holdings are partial, the
partiality is acknowledged. The wishlist documents what is
missing. The restoration documents say what was preserved and what
was not.

---

## 8. Closing note

These refusals are constitutional. They are not subject to
feature-prioritization decisions. They are not relaxed when a
specific use case would benefit from relaxing them. They are not
made conditional on "if the technology improves."

A future steward who finds one of these refusals inconvenient is
welcome to propose an amendment to the constitution — but until
the amendment is accepted, dated, and recorded in the stewardship
log, the refusal holds.

The archive's identity is partly composed of these. To remove them
would be to make a different archive. The constitution is the
floor; these refusals are part of the floor.

A reader in 2126 should be able to verify that none of these
refusals have been silently violated in the intervening century.
That is the standard the archive is built to.
