# Commentary Ontology

*v1 · 2026-05-14 · constitutional and architectural; no implementation yet.*

A commentary in this archive is, formally, **a statement about a part
of the primary corpus, made by a named voice, recorded separately
from the primary text it references.**

This document describes the categories the archive uses to classify
commentary, the limits of that classification, and the cases where
the archive declines to classify at all.

The constitutional law that frames this work is in
`COMMENTARY_CONSTITUTION.md`. The most consequential rule from there
is §8 — *classification is part of the archive's voice, not the
witness's.* This document operates under that rule.

---

## 1. Why ontology is hard for this archive

A naive ontology — a closed list of types like "philological",
"historical", "doctrinal" — would be useful for filtering and
discoverability, but it costs three things the archive values more:

- **Voice fidelity.** A 12th-century commentator did not classify
  his own work. Imposing "philological" on Rashi flattens what Rashi
  was actually doing. He was, often, doing many of those things in
  one sentence.
- **Tradition coherence.** Within a single commentary tradition,
  category lines do not match Western academic ones. The Sanskrit
  *bhāṣya/ṭīkā/ṭippaṇī* distinction is not "long/medium/short
  commentary"; it carries its own technical meaning.
- **The plurality principle.** A single commentary may serve
  multiple functions for different readers. Labeling it once locks
  the reading.

Yet the archive cannot reasonably ban classification altogether:

- Discoverability requires filters.
- Cross-text comparison requires types.
- Print editions need to know whether a note is a footnote or a
  marginal gloss.
- AI overlays need to know what they should and should not generate.

The archive therefore adopts **two-layer classification**: one layer
the archive imposes, another the archive declines. The next sections
define both.

---

## 2. What the archive does NOT classify

The following kinds of commentary are recorded **without categorical
tagging by the archive**:

- **Source-internal apparatus.** Translator footnotes, manuscript
  variants, page boundaries, scholarly editorial marks bound to the
  source publication. These belong to the `apparatus_file` layer
  (see `SCHEMA.md`) and follow its existing anti-classification
  discipline.
- **Traditional commentary as a standalone text.** When the archive
  ingests, say, Ibn Kathīr's *Tafsīr al-Qurʾān al-ʿAẓīm*, that
  becomes its own primary text. Within that work, the archive does
  not impose its own commentary categories on Ibn Kathīr's prose.
  Ibn Kathīr is recorded as a whole text with its own structure; its
  individual paragraphs are not auto-typed.

These two refusals exist for the same reason: in both cases, the
text being recorded is itself a witness with its own voice. The
archive is preserving a voice, not curating an interpretation. Any
type-tag would be the archive speaking over the witness.

When commentary about a traditional commentary is needed — *e.g.,
modern scholarship saying "Ibn Kathīr here is following al-Ṭabarī"*
— that's a different record, in a different layer (modern
scholarship), classified by archive rules.

---

## 3. What the archive DOES classify

The following kinds of commentary **may** carry archive-imposed
classification, because the classifier is the archive itself (or a
named modern author) and the classification is itself a
provenance-tagged claim:

- **Cross-text references** between commentary records and primary
  texts.
- **Modern scholarly notes** added to the archive by stewards or
  ingested from named scholarly works.
- **Archive editorial notes** — restoration history, source-choice
  rationale, OCR-correction decisions.
- **Steward-added concept tags** — entity identification, motif
  tagging.
- **AI-generated suggestions** — explicitly typed by the model that
  produced them.

In each case, the classification is part of the archive's voice and
inherits the archive's provenance discipline: dated, attributed, and
revisable.

---

## 4. Category vocabulary (working list)

The archive's working vocabulary for classifying its own commentary,
ordered from most concrete to most interpretive. This is a **soft
set**, extensible by stewardship decision; new categories require an
amendment to this document.

Each category answers a question a reader is likely to be asking.
The question is the test for whether a category is useful: if it
does not correspond to a real reader need, it is over-taxonomy and
should not be added.

| Category | The question the reader is asking |
|---|---|
| `philological` | What does this word, phrase, or syntactic structure mean in the source language? |
| `lexical` | What is the dictionary meaning of this term? |
| `prosodic` | What is the metre, rhyme, or oral structure? |
| `manuscript` | How does this passage read in other witnesses? Is there a variant? |
| `historical` | When, where, and by whom was this written? What was happening at the time? |
| `geographic` | Where on earth is this place? |
| `chronological` | What date does this passage anchor or refer to? |
| `biographical` | Who is this person? |
| `doctrinal` | What does this passage mean within its own tradition? |
| `liturgical` | How is this passage used in ritual practice? |
| `cross-textual` | What does this passage parallel or echo in other texts? |
| `cross-civilizational` | What is the structurally analogous passage in another civilization's literature? |
| `narrative-motif` | What story-shape (the hero's journey, the rescued bride, the dying god) does this instance belong to? |
| `editorial` | What did the archive's stewards decide here, and why? |
| `restoration` | What changed in this passage during a restoration pass, and what was preserved? |
| `provenance` | Where exactly did this text come from? |
| `translation-comparison` | How does this rendering differ from other translations? |
| `gloss` | An informal, in-flow explanation for a reader, low-stakes. |

A commentary record may carry **zero, one, or several** of these
categories. Records routinely carry several: a note about Vessantara
giving away his children might be `doctrinal` (the dāna-pāramitā
question), `narrative-motif` (the giving-away-the-family motif), and
`cross-textual` (parallels in other Buddhist literature) at once.

A commentary record may also carry **no category at all**, where
classification would be presumptuous or unhelpful. The empty case is
legitimate.

---

## 5. Category vocabulary explicitly NOT adopted

The archive declines to adopt the following category families. Each
declination has a reason.

- **`quality`** — *bad/medium/good* commentary or *authoritative/
  controversial*. The archive does not rank commentary. Plurality
  forbids it.
- **`alignment`** — *Sunni/Shi'a*, *Theravada/Mahayana*,
  *orthodox/heterodox*, *liberal/conservative*. The archive records
  a commentary's tradition through its provenance (who wrote it,
  when, where, in what school), not through a label the archive
  applies. Labeling positions risks the archive choosing sides.
- **`difficulty`** — *introductory/advanced*. Reader-dependent;
  outside the archive's scope.
- **`length`** — handled structurally (a record's body has a length),
  not classifiably.
- **`emotion`** — the archive does not annotate primary text with
  affective tags.
- **`relevance`** — relative to what? The archive does not predict
  reader needs.

If a steward needs one of these for a specific local purpose, it
belongs in a *private* annotation layer, not the public commentary
schema.

---

## 6. Granularity and multiplicity

A commentary record's classification is independent of its
attachment granularity. A `philological` comment may attach to a
single word; a `doctrinal` comment may attach to a whole tale; a
`cross-civilizational` comment may attach to a chapter. The
attachment level is described in `COMMENTARY_ATTACHMENT_MODEL.md`;
classification is independent.

A record carrying multiple categories is the **normal case**, not
the exceptional case. Forcing a single primary category would over-
flatten. The reader-facing renderer may, for display purposes,
select one of the categories as the primary "type" (alphabetical
priority is the default rule), but the underlying record is
multi-typed.

---

## 7. Categorical sets are versioned

The category vocabulary is part of the archive's voice. The
vocabulary in §4 is **v1**. Future versions may add categories,
deprecate categories, or refine definitions. Each version is dated
and reversible. A commentary record carries the vocabulary version
it was tagged under, so that a renderer interpreting an old record
can still understand the tags.

A commentary record's classification, like its body, is **never
silently re-classified**. If a steward decides a v1 record's
`philological` tag is really `lexical` under v2, that re-tagging is
a new editorial act, dated and recorded.

---

## 8. The commentary-of-commentary case

When a commentary record describes another commentary record (e.g.,
*"Rashi here departs from his usual exegetical practice"*), the
inner commentary is its own primary text. The outer record uses
`anchor.target = "commentary:<id>"` rather than
`anchor.target = "passage:<id>"`. Both records exist; neither
modifies the other.

Classification of the outer record follows the same rules: stewards'
categories on stewards' work, not on the inner commentary's voice.

This may stack: archive notes on modern scholarship on traditional
commentary on a primary text. Each layer is its own record. The
archive's job is to preserve the stack, not to flatten it.

---

## 9. Reading-by-category

For a renderer, the categorical metadata is a filter tool. A reader
may say:

- *"show me only the philological notes on this passage"*
- *"show me only the cross-civilizational notes"*
- *"show me everything from this scholar"*
- *"show me everything without categorical tags"*

The last case is important: untagged commentary is not less valuable
than tagged commentary. It is, often, more careful, because the
steward declined to over-classify. The renderer must support
*reading the untagged set*, not only the tagged subset.

Default reader view shows **everything**. Filtering is opt-in.

---

## 10. Special cases

A small number of cases require constitutional handling.

### 10.1 Translation-comparison commentary

A `translation-comparison` record sits between two translations.
Its anchor is dual: one passage in each translation. Display-wise,
this is a "compare" overlay. Provenance-wise, it is normal
commentary. Its body says, in archive voice or scholar voice,
*"Pickthall has 'God', Yusuf Ali has 'Allah'; both render Arabic
'Allāh' but reflect different conventions of the period."*

### 10.2 Restoration notes

A `restoration` category record is, specifically, an archive
editorial note recording a decision made during a restoration pass
(e.g., the Qur'an restoration, the Jātaka Vol 6 acquisition). These
records have a fixed provenance — `archive:steward` — and are dated
by the restoration date.

A `restoration` record exists **independently** of the restoration
document itself (e.g., `QURAN_RESTORATION_2026.md`). The Markdown
restoration document is the human-readable narrative; the
`restoration` commentary records are the machine-readable per-text
anchors of decisions that document describes. Both exist; the
Markdown is the editorial voice, the records are its index.

### 10.3 Manuscript-variant commentary

A `manuscript` category record records a variant reading in another
witness. Its body is the verbatim variant text from that witness.
Its anchor is the passage(s) in the archive's reference text where
the variant applies. Its provenance is the named witness manuscript.

This is **adjacent to** but **distinct from** the existing
`apparatus_file` mechanism. Apparatus is variant readings *as
preserved by the printed witness's own apparatus*. A `manuscript`
commentary record is an external claim about a variant reading,
made by the archive or a modern scholar after consulting another
manuscript. The first is part of the printed source; the second is
a new claim about it.

---

## 11. Categories not yet thought of

The vocabulary in §4 is a working list, **not** a complete one. The
archive expects to add categories as commentary corpora are
acquired:

- Acquiring a *tafsīr* tradition may suggest `eschatological`,
  `legal`, `mystical` as Islamic-tradition-specific categories.
- Acquiring a Buddhist *abhidharma* commentary may suggest
  `taxonomic`, `phenomenological`.
- Acquiring patristic exegesis may suggest `allegorical`,
  `typological`, `tropological`, `anagogical` (the medieval
  fourfold).

Each addition follows the §7 versioning discipline. The archive
errs on the side of fewer-but-clearer categories. When in doubt,
**a steward should record the commentary without categorical tags
rather than invent a category for it.**

The empty case is constitutional. Over-classification is not.

---

## 12. Closing note

The ontology described here is not a taxonomy of *what commentary
fundamentally is*. It is a taxonomy of *what the archive needs to
ask of commentary in order to make it findable, comparable, and
honest*.

The archive resists the urge to be a clean ontology. It is more
honest as a slightly-messy archive of voices than as a clean
philosophical taxonomy of one steward's view.

The vocabulary will grow slowly. Adoption will be careful. The
absence of a category is a possible answer.
