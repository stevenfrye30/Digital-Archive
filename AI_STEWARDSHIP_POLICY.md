# AI Stewardship Policy

*v1 · 2026-05-14 · stewardship architecture; no implementation yet.*

The archive holds Layer-6 AI-generated content under strict
quarantine. The constitutional commitments are in
`PROVENANCE_LAYERS.md §7` and `INTERPRETIVE_BOUNDARIES.md §4`. The
prototype (`COMMENTARY_PROTOTYPE_2026.md`) verified that the
quarantine works mechanically: AI records are off by default,
visually distinct, never silently promoted, never used to fill
primary text gaps.

This document formalizes the long-term stewardship policy for AI
content as an archival object. It covers retention, labeling,
identity preservation, prompt provenance, allowed revisions,
deprecation, prohibited behaviors, and how AI-related repair works.

The shortest statement of the policy:

> **AI output is preserved forever, attributed forever, and
> labeled forever. The archive remembers what the machines said.**

The archive does not forget AI's voice; nor does it confuse AI's
voice with any other voice. Both commitments are equally important.

---

## 1. Why this policy exists

The temptation around AI in an archival project is twofold:

- **The temptation to scale.** Generate commentary across the
  corpus quickly, fill all gaps, produce searchable interpretive
  metadata at no per-text cost.
- **The temptation to launder.** Use AI to produce a first draft,
  edit lightly, ship under a human's name; or use AI output as if
  it were unattributed editorial fact.

Both temptations are constitutionally refused. The first by
`INTERPRETIVE_BOUNDARIES.md §4.3` and §4.4. The second by the
requirement (`COMMENTARY_CONSTITUTION.md §5`) that every layer
carry its own provenance, named.

This document is the operational form of those refusals. It is
written from the position that AI is genuinely useful as a
*suggestion*, *prototype*, *first-pass* tool — and genuinely
dangerous if the labeling, retention, and quarantine fail. The
policy aims at both.

---

## 2. Retention

### 2.1 The retention principle

AI records are retained **indefinitely**, like all canonical
commentary records. Layer-6 records are subject to
`COMMENTARY_LIFECYCLE.md` no-deletion principle (§5).

Specifically:

- An AI record once published in the canonical record set persists
  forever, regardless of later judgment about its merit.
- An AI record may be **deprecated** (a successor is preferred),
  **withdrawn** (the original author retracts), or **superseded**
  (a successor record carries the claim better). It is not deleted.
- The model identity, generation date, and prompt context are
  preserved alongside the body.

The reason for indefinite retention is the same as for any other
archival record: a reader in 2126 studying how AI's contributions
to interpretive scholarship evolved must be able to see what AI
actually said in 2026 — including the AI's mistakes, hallucinations,
and confident-but-wrong claims. Erasing those records would make
the AI's contribution appear better than it was. The archive does
not flatter machines.

### 2.2 What is *not* retained

What an AI was asked but did **not** produce a Layer-6 record from
— a draft suggestion the steward read and discarded — is **not
retained**. This is the working-draft discipline of
`PUBLIC_PRIVATE_BOUNDARIES.md §3`: drafts are scaffolding, not
archive material. A steward who solicits ten AI suggestions and
publishes one as a Layer-6 record has, by that act, decided which
one entered the archive. The other nine do not.

This is asymmetric with human authorship: a human's discarded
drafts are also not preserved. The asymmetry is correct.

What **must** be retained when a Layer-6 record is published:

- The body, verbatim.
- The model identity (model ID, model release date).
- The generation date.
- The prompt context (summary or, where reproducibility matters,
  the exact prompt).
- The quarantine flag (always true for Layer-6 records).
- The steward who solicited the AI output and chose to publish it
  (see §3 on dual authorship).

---

## 3. Authorship and identity

### 3.1 The dual-authorship pattern

Per `COMMENTARY_PROTOTYPE_2026.md §7.4`, an AI record has, in
principle, two authors:

- **Body author**: the AI that produced the substantive content.
- **Record author**: the steward who solicited the output, chose
  to publish it, and assembled the record.

The prototype used a single-author pattern (`provenance.author:
archive:ai:<model>`). The policy here adopts the **dual-author
pattern** for production records:

```json
{
  "provenance": {
    "layer": "ai",
    "author": "archive:ai:claude-opus-4-7",          // body author
    "record_author": "archive:steward:steve",       // who published the record
    "date": "2026-05-14",                            // generation date
    "record_date": "2026-05-14",                     // record creation date (often same)
    "source": {
      "model_id": "claude-opus-4-7",
      "model_release_date": "2026-01",
      "prompt_context": "...",
      "prompt_id": "<optional reference to a stored prompt>"
    },
    "quarantine_flag": true
  },
  ...
}
```

The body authorship is the AI's. The record's existence is the
steward's editorial choice. Both names appear forever.

A future reader reading this record can ask either: *"who produced
this content?"* (the model) or *"who decided this content was
worth preserving?"* (the steward). Both questions get clean answers.

### 3.2 Model identity

The model identity is recorded with enough specificity that a
future reader can identify exactly which model produced the
content. Required fields:

| Field | Meaning |
|---|---|
| `model_id` | The model's stable identifier (e.g., `claude-opus-4-7`). |
| `model_release_date` | The date the model was released (or, for fine-tuned variants, the date the variant was released). |
| `model_provider` | The institutional source (Anthropic, OpenAI, an open-weights project, an in-house model). |
| `model_weights_hash` (optional) | Cryptographic hash of the weights when reproducibility at that level matters. |

The model identity is **permanent**. Even if the model is later
deprecated by its provider, even if the model is later shown to
have been trained on contaminated data, even if the model's
behavior is later revealed as untrustworthy — the model identity in
the record does not change. The record records *what model said
what, when*. Later judgments about the model do not retroactively
relabel its prior output.

A future scholar studying "AI commentary trends in archival
projects, 2020s–2060s" depends on this identity preservation.

### 3.3 Prompt provenance

Every AI record carries a **prompt context** describing what the
model was asked. The granularity:

| Prompt-provenance form | Use |
|---|---|
| `prompt_summary` | One-sentence description, the typical form. *"Asked to suggest cross-civilizational parallels for the Apannaka-jataka's two-merchants narrative."* |
| `prompt_text` | The exact prompt, when reproducibility matters and the prompt is short. |
| `prompt_id` | A reference to a stored prompt in the archive's prompt registry, when the prompt is long or shared across multiple records. |
| `conversation_context` | A reference to a stored conversation, when the AI's output depends on multi-turn context. |

A record without prompt provenance fails the AI-label requirement
(`COMMENTARY_REPAIR_PROTOCOLS.md §12`). The minimum is a
`prompt_summary`.

The archive treats prompts as **co-authors** of AI output in an
operational sense: the same model, given different prompts,
produces different outputs. A record preserving only the output
but losing the prompt loses an essential part of the AI's
voice-conditions.

### 3.4 The prompt registry

When a steward generates many AI records using the same or related
prompts, the archive may maintain a **prompt registry**: a file at
`01_library/library/ai_prompts/<date>_<slug>.json` recording the
prompt body once, with each Layer-6 record referencing the prompt
by id.

The prompt registry has its own append-only discipline: prompts are
not modified once a record references them. A new variant of a
prompt gets its own registry entry.

The prompt registry is **part of the canonical record set**,
version-controlled, and persists indefinitely.

---

## 4. Labeling

### 4.1 The permanent label

Every AI record carries the model identity (per §3.2) and the
quarantine flag (`quarantine_flag: true`). The renderer reads
these fields and produces a visible AI label at every rendering
context where the record appears.

The label is **permanent**. There is no field on the record that
turns off the label. A record originating from Layer 6 always
displays as Layer 6.

### 4.2 What the label says

The label communicates, at minimum:

- This record's body was authored by an AI.
- The model that authored it.
- The date the AI generated the content.
- That the record is **quarantined** (off by default in reader
  views).

A reader who sees an AI label is, by that label, informed that the
content is suggestion rather than human claim. The reader weighs
accordingly.

### 4.3 The renderer's visual register

The prototype used:

- Distinct background tint (soft purple).
- "AI · quarantined · off by default" badge.
- Colored left-border distinct from other layers.

These are placeholder conventions; a production renderer chooses
its own typography. The constitutional requirement is that the
visual register is **distinct from every other layer**. A casual
reader cannot mistake Layer 6 content for Layer 4, Layer 5, or
Layer 3 content.

A future renderer with stronger typographic discipline (per
`COMMENTARY_PROTOTYPE_2026.md §7.5`) will likely use historical
apparatus conventions: footnote rules, indented blocks, sidebar
columns. The constitutional requirement is the same: AI content is
distinct.

---

## 5. Revision

### 5.1 AI records may be revised

An AI record is subject to the same versioning discipline as any
other record (`COMMENTARY_VERSIONING.md`). A revision happens when:

- The same prompt is re-run against the same model and produces
  improved output (this is a real case; even temperature-zero
  models drift across versions, and prompt refinements often
  produce better results).
- The model itself is updated, and the steward wants to record a
  new output from the newer model.
- The steward decides the original record's body had a defect
  that re-generation fixes.

The revision pattern is the standard one:

- A new record with id suffix `@<revision-date>`.
- `supersedes` pointing at the prior record.
- New `provenance.date` and (potentially) new `model_id` and
  `model_release_date` if a different model produced the revised
  body.
- The prior record transitions to `deprecated` then `superseded`.

Both records persist. A future reader can compare what the same
prompt produced from model A in 2026 vs model B in 2030.

### 5.2 The model-update case

When a new model version is released and the steward wants to
re-generate prior AI records:

- This is **not** done in bulk. Each re-generation is a deliberate
  per-record act.
- The new record's `provenance.author` is the new model.
- The prior record (older model) is preserved as `deprecated` /
  `superseded`.
- The bulk regeneration is **forbidden** by the
  refusal-to-auto-classify discipline
  (`INTERPRETIVE_BOUNDARIES.md §4.3`).

A steward who wants the archive to "have current AI output"
across thousands of texts is asking for something the constitution
refuses. Per-record decisions, recorded for posterity, are the only
discipline.

---

## 6. Deprecation and expiration

### 6.1 AI records do not auto-expire

The archive does **not** automatically deprecate AI records on a
schedule. A 2026 AI record about the Apannaka does not lose
standing because we have entered 2040. The record's status is its
status; time alone does not change it.

### 6.2 Steward-initiated deprecation

A steward may deprecate an AI record at any time, for reasons
including:

- The record's body is wrong (the AI hallucinated).
- The record's body is correct but a better claim exists (a
  Layer-4 scholar or Layer-5 editorial steward has authored a
  more careful version).
- The record's relevance has faded (the parallel it suggested no
  longer seems productive).

Deprecation follows `COMMENTARY_LIFECYCLE.md §3.4`: the record is
marked deprecated, the reason is logged, the record remains
readable.

### 6.3 The withdrawal case

A particularly common AI-record case: the steward, on re-reading,
decides the AI's claim is wrong enough to retract publicly. This is
**withdrawal** (`COMMENTARY_LIFECYCLE.md §3.6`).

A withdrawn AI record is **especially honest** about being
withdrawn:

- The body is preserved (the AI's voice stays on record).
- The withdrawal note explains the steward's reasoning.
- The renderer's display strongly marks the withdrawal — at least
  as prominently as the AI label itself, often more so.

A reader of a withdrawn AI record sees both the original claim and
its retraction together. This is the constitutional commitment that
AI output is preserved alongside the steward's later judgment of it.

---

## 7. Promotion across layers — the asymmetric rule

The single transition the archive forbids is **Layer-6 silently
becoming any other layer**.

What this means in practice:

- A steward who reads an AI suggestion and decides it is correct
  may author a **new Layer-5 editorial record** stating the same
  claim under the steward's name. The new record cites the AI
  record as basis.
- Both records persist. The AI record is not deleted or absorbed.
- The new Layer-5 record carries the steward's name as author;
  the AI's name does not appear as author of the Layer-5 record
  (it appears only as a cited source).
- The AI record's quarantine remains; the Layer-5 record is
  normal-discipline commentary.

This pattern preserves the layer system's integrity. The AI's
contribution to the steward's thinking is recorded; the steward's
own claim is recorded; both stand. A reader can study how AI
suggestions influenced editorial decisions over time.

The opposite direction is **always forbidden**: a human's editorial
record cannot be silently re-attributed to an AI; a scholarly note
cannot be reclassified to Layer 6; a primary text cannot be
demoted to "AI-suggested" if a steward later regrets having
included it.

Layer 6 is a one-way street: AI content goes in, gets cited as
basis for human work, but never absorbs other layers' content.

---

## 8. Prohibited behaviors

The archive refuses the following AI uses on principle. Each is
formal — not subject to feature trade-offs.

### 8.1 No bulk auto-generation

Per `INTERPRETIVE_BOUNDARIES.md §4.3` — no running an AI loop over
the corpus to produce thousands of records. The discipline is
*per-record, named, dated, with prompt provenance*. Bulk is the
violation.

### 8.2 No unlabelled AI

Per `INTERPRETIVE_BOUNDARIES.md §4.1` — no AI output displayed
without the AI label. Per §3.2, the label is permanent.

### 8.3 No AI in primary text

Per `INTERPRETIVE_BOUNDARIES.md §4.2` — no AI-translated passages,
no AI-restored OCR gaps, no AI-imagined manuscript variants in the
primary text. AI may *suggest* — as Layer-6 commentary — that a
restoration would be appropriate; a human steward then performs
the restoration as a normal editorial act, optionally citing the
AI's suggestion as basis.

### 8.4 No silent training-disclosure failure

Per `INTERPRETIVE_BOUNDARIES.md §4.5` — if the archive's content is
used to train a model, the use is disclosed in the archive's
stewardship log. Conversely: if the archive uses an AI whose
training data is unknown or contaminated, that fact is recorded in
the model's identity entry (a `training_disclosure` field).

### 8.5 No "AI native" replacement for human editorial work

The archive does not adopt AI as a substitute for stewardship.
Stewardship is what the human does: choosing what to publish,
choosing what to retract, choosing what to leave silent.
Delegating those choices to an AI would empty out the stewardship
function the archive exists to perform.

This is the constitutional commitment that runs across all the
AI policy: **the archive is human-stewarded, with AI as one of
its tools.** AI does not become the steward.

### 8.6 No identity-loss tolerance

A Layer-6 record that loses its model identity (per
`COMMENTARY_REPAIR_PROTOCOLS.md §12`) is double-quarantined and, if
identity cannot be recovered, withdrawn. The archive does not
present AI output of uncertain origin as if it were anything else.

### 8.7 No proactive expansion

The archive does **not** automatically prompt AI to "look for
parallels", "suggest tags", "find similar passages", or "generate
commentary candidates." Such workflows may exist in a steward's
personal workflow outside the archive, but the resulting
suggestions enter the archive only by deliberate per-record
publication acts.

### 8.8 No "AI says" framing for editorial decisions

A steward's editorial note may **cite** an AI suggestion: *"Layer-6
record X proposes that Apannaka parallels the Choice of Heracles;
I agree, and adopt the parallel in Layer-5 record Y."* This is a
proper citation.

A steward's editorial note may **not** justify itself by AI: *"AI
says this is correct, so I'm publishing it."* This collapses the
human-editorial-judgment commitment that the layer system exists to
preserve.

---

## 9. The "AI-assisted human" question

A steward may use AI tools while doing human editorial work —
asking a language model to help phrase a Layer-5 editorial note,
or to suggest related anchors, or to check internal consistency.

The discipline:

- If the AI's contribution is **substantive** (the AI wrote a draft
  of the record's body, and the steward edited it), the record is
  **Layer 6**, not Layer 5. The body author is the AI; the
  steward's role is record-author and editor.
- If the AI's contribution is **structural** (the AI helped check
  internal consistency, suggested file naming, caught a typo), the
  record is the steward's authorship; the AI's involvement is **not
  recorded on the record**, because it played no substantive role.
- If the AI's contribution is **ambiguous** (the AI suggested a
  framing the steward adopted; the wording is largely the
  steward's, but the conceptual frame is the AI's), the steward
  records this in the stewardship_log: *"Conceptual frame
  suggested by AI consultation; expressed in steward's wording;
  remains Layer-5."* This is an honest hybrid case.

The rule of thumb: **substantive content authorship is the test**.
If the AI wrote the content, it is Layer 6. If the AI helped the
human write, it is Layer 5 with optional acknowledgment.

This rule is conservative because the alternative — allowing AI
contribution to disappear into human authorship — would compromise
the layer discipline. A future reader auditing the archive's
editorial history must be able to see when AI was the actual voice.

---

## 10. The "AI co-authorship" case

A more elaborate case: a human steward and an AI co-author a
record through extended interaction (the model produces drafts,
the steward refines, the model revises, etc.). The result is
clearly hybrid.

The discipline:

- The record is **Layer 6**. The AI's substantive contribution
  meets the §9 test.
- The `provenance.author` lists both:
  ```json
  "author": ["archive:ai:claude-opus-4-7", "archive:steward:steve"]
  ```
- The body is the final form; the conversation that produced it
  may be stored in the `conversation_context` reference (per §3.3)
  if reproducibility matters.
- The record carries the AI label.

The reader sees: this is AI-tinged content with human refinement,
not pure AI output and not pure human authorship. The layer
system encodes that honestly.

This is rare in practice but valuable as a category. The May 2026
prototype's AI record was a borderline case: the model proposed the
Choice of Heracles parallel, the steward chose to publish it as a
Layer-6 demonstration. Under the current dual-authorship policy,
the record would carry both authors.

---

## 11. The archival horizon for AI

The constitutional commitment from `CITATION_PERMANENCE.md` —
citations from 2026 must resolve in 2126 — applies to AI records
too. A citation of a Layer-6 record from 2026 must, in 2126,
resolve to:

- The original AI record, with the 2026 model identity preserved.
- The body as the AI produced it in 2026.
- The prompt context as recorded in 2026.
- Whatever lifecycle state the record currently holds (provisional,
  withdrawn, superseded by a 2030 re-generation, etc.).

A future scholar studying "what AI claimed about Buddhist narrative
in the 2020s" can read the archive's Layer-6 records and find
**exactly what AI claimed, with full attribution, and with the
human stewardship that surrounded those claims**.

The archive is, in this respect, a primary source for the history
of AI itself. The integrity of that primary source matters as much
as the integrity of any other primary source the archive holds.

---

## 12. The relationship to `INTERPRETIVE_BOUNDARIES.md §4`

The refusals in `INTERPRETIVE_BOUNDARIES.md §4` are reaffirmed and
extended:

| Boundary doc rule | This document's extension |
|---|---|
| §4.1 No unlabelled AI | + permanent label discipline (§4 of this doc) |
| §4.2 No AI in primary text | + the rare-case rule for AI-suggested restorations (§8.3) |
| §4.3 No auto-classification | + the no-bulk-generation discipline (§8.1) |
| §4.4 No scale cross-references | + per-record discipline for cross-civilizational parallels (the prototype's Heracles record is the model) |
| §4.5 Training disclosure | + the `training_disclosure` field on model identity (§8.4) |

This document's prohibitions are stricter than `INTERPRETIVE_BOUNDARIES.md`,
not weaker. The constitutional floor is established there; the
operational ceiling is established here.

---

## 13. The institutional analog

The institutional analog for the AI-stewardship discipline is the
*editor's note* convention in critical editions, applied with the
honesty of a peer-review record.

A critical edition often carries the editor's notes — "I prefer
reading X over reading Y, against the consensus of the prior
editors" — as a labeled layer distinct from the source text and
from prior scholarship. The editor's name appears beside every
preference; the editor's reasoning is visible; a later editor
who disagrees can author their own notes alongside, without
overwriting the earlier ones.

AI's voice in the archive is structurally similar: a contributing
voice, labeled, preserved, never silently authoritative. The
typographic conventions differ — AI records carry a stronger
visual quarantine — but the institutional logic is the same.

The archive does not invent the discipline; it adopts an old one
for a new author.

---

## 14. Closing note

AI is genuinely useful in this archive: as a tool for proposing
cross-civilizational parallels, suggesting structural anchors,
drafting placeholder content for review, surfacing patterns a
human might miss. The prototype's Choice of Heracles record is a
small case but a real one — the AI's contribution to the
prototype was, in fact, useful.

The discipline above exists so that the usefulness does not erode
the archive's integrity. Every AI record is preserved with its
identity, its date, its prompt, its quarantine. Every AI
contribution is named. Every promotion of AI suggestion to human
editorial work is explicit. The layer never collapses.

A reader of this archive in 2126, looking at Layer-6 records from
the 2020s, sees what AI actually said — including what it got
wrong, what it suggested productively, and what human stewards
chose to do with its suggestions. That is the archive's
contribution to the long history of AI: an honest record of one
small project's engagement with a new kind of authorship.

The archive does not pretend AI was not part of its work. The
archive does not pretend AI was a steward. Both honesties matter
equally.
