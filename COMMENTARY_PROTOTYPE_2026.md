# Commentary Prototype — May 2026

A short note recording the May 2026 pressure-test of the commentary
constitutional architecture against a real text. The prototype is
deliberately tiny: one tale (Apannaka-jātaka, #1, Cowell vol 1,
Chalmers 1895), five hand-crafted commentary records across four
layers, one minimal renderer. The point of the work is not features;
it is to find out where the constitution rubs against reality
*before* the implementation is broad enough that the rubs would be
expensive to fix.

This is the prototype's project log. Its tone is honest about what
worked, what was awkward, and what should not scale.

The constitutional documents that frame this work are in:

- `COMMENTARY_CONSTITUTION.md`
- `COMMENTARY_ONTOLOGY.md`
- `COMMENTARY_ATTACHMENT_MODEL.md`
- `PROVENANCE_LAYERS.md`
- `INTERPRETIVE_BOUNDARIES.md`

The illustrative schema is in:

- `COMMENTARY_SCHEMA_SKETCH.md`

---

## 1. What was built

Five hand-crafted commentary records in four sibling files under the
canonical Apannaka directory:

```
01_library/library/texts/sacred/buddhist/jataka-chalmers-vol1/
├── text.json                            (unchanged)
├── passages_chalmers-vol1.json          (unchanged)
├── commentary_editorial.json            (2 prototype records — Layer 5)
├── commentary_scholarship.json          (1 prototype record  — Layer 4)
├── attachments_traditional.json         (1 prototype bridge  — Layer 3)
└── commentary_ai.json                   (1 AI-authored record — Layer 6)
```

One renderer:

```
05_scripts/render_commentary_prototype.py
```

One output:

```
06_workspace/commentary_prototype.html
```

The records cover:

- a passage-level anchor with a `phrase` sub-locator (editorial; the
  `[95.]` page bracket in passage 1.1);
- a multi-anchor record across two adjacent passages (editorial; the
  canonical Jātaka opening formula on 1.1 and 1.2);
- a tale-level anchor + a parallel passage-level anchor (scholarship;
  the doctrinal framing of the Truth-discourse);
- a Layer-3 bridge to a not-yet-acquired traditional commentary
  (`body: null`; the Jātakaṭṭhakathā);
- an AI-generated cross-civilizational parallel record (Apannaka ↔
  Choice of Heracles in Xenophon's *Memorabilia*).

Three of those carry `archive:tale:jataka::1` anchors; four carry
passage anchors; one has a sub-locator. The set was sized to
exercise the schema, not to be comprehensive scholarship.

---

## 2. The bare-canon test — passed

The constitutionally most important test:

> A reader of the archive must be able to read the bare canonical
> text, with no commentary visible, exactly matching the bytes the
> integrity proof verifies. (`COMMENTARY_CONSTITUTION.md §6`)

The renderer's `--bare-canon-byte-equivalence` self-check extracts
the primary text from the rendered HTML, reverses HTML escaping,
and compares it byte-for-byte against the canonical
`passages_chalmers-vol1.json`. **63 of 63 passages match exactly.**
The constitutional commitment is mechanically verifiable.

This is the single result that mattered most. The architecture
works at its foundation.

---

## 3. The layer non-collapse test — passed

Each commentary file declares its layer explicitly in its outer
wrapper, and every record inside declares the same layer in its
`provenance.layer` field. The renderer's `load_commentary` step
checks that both agree, and raises `SystemExit` if either:

- the filename's implied layer disagrees with the wrapper's `layer`,
- or any record's `provenance.layer` disagrees with the file's `layer`.

A deliberate test — relabelling `commentary_ai.json`'s wrapper
`layer` from `"ai"` to `"editorial"` — was caught:

```
layer mismatch: commentary_ai.json declares layer='editorial' but is in the ai file
```

The non-collapse rule from `PROVENANCE_LAYERS.md §9` is enforced at
load time, not just by visual style.

---

## 4. The AI-quarantine test — passed

The AI layer is `default_on=False` in the renderer's `LAYER_DISPLAY`
table. The toggle for the AI layer starts unchecked. The initial
body class includes `layer-off-ai`. AI records are visually marked
with a colored left-border, a soft purple background tint, and an
"AI · quarantined · off by default" badge in the summary.

A reader opening the prototype HTML with default settings sees zero
AI content. They must explicitly tick the AI-layer toggle to reveal
it.

Per `PROVENANCE_LAYERS.md §7`: *AI output is never silently merged
into another layer. The default disposition toward AI output is:
record it, label it, keep it small, and require explicit human
action to elevate it.* The prototype honors this.

---

## 5. The traditional-bridge test — passed

The Layer-3 bridge record (`attachments_traditional.json`) carries
`body: null` and a `body_in_other_record` target pointing at a
hypothetical primary record for the Jātakaṭṭhakathā that does not
exist in the archive. The renderer detects the null body and
renders an honest gap:

> *Traditional commentary expected here. The bridge points at
> `archive:passage:jatakatthakatha::primary-translation::1.0.prologue`,
> which is not currently in the archive. The gap is recorded
> honestly rather than filled.*

When the Jātakaṭṭhakathā is acquired as a primary text in the
future, the bridge target will resolve. Until then, the gap is the
truthful record. The prototype demonstrates that **a gap is a
legitimate display state**, not a bug.

---

## 6. The non-destructive overlay test — passed

The renderer is read-only with respect to the canonical library:

- `passages_chalmers-vol1.json`'s `mtime` is unchanged after the
  renderer runs.
- `text.json`'s `mtime` is unchanged.
- Commentary records are read; never written.
- The output goes only to `06_workspace/commentary_prototype.html`,
  which is workspace material, not canonical material.

The renderer is also idempotent: running it twice produces
byte-identical output. The HTML file has no embedded timestamps, no
random ordering, no run-specific identifiers. This matters for
archival stability — a render done in 2026 and a render done in
2126, given the same inputs, produce the same bytes.

---

## 7. Tensions that surfaced

These are the moments where the prototype rubbed against the
constitution. Each is noted not as a failure but as an architectural
finding worth recording before scale.

### 7.1 Bare-canon mode depends on JavaScript

The renderer expresses bare-canon mode as a JavaScript class
toggle:

```css
body.bare-canon .comment { display: none; }
```

A reader with JavaScript disabled cannot reach bare-canon mode
through the toggle. The default body class shows three of the four
overlays — editorial, scholarship, traditional — and a JS-disabled
reader sees them all.

The constitutional commitment (`COMMENTARY_CONSTITUTION.md §6`)
says *"At any time, a reader of this archive must be able to read
the primary text in its original published form, with no commentary
visible."* In the prototype, that is true only with JavaScript
enabled. **This is a real constitutional tension**, surfaced by
implementation contact.

Recommended for any future renderer: bare-canon mode must be
reachable without JavaScript. Options worth considering:

- Generate a second HTML file — `apannaka.bare.html` — that ships
  no overlays at all and links to the overlay version. The bare
  version is the constitutional default.
- Use a URL query parameter (`?overlays=off`) and have the renderer
  produce two variants of each tale.
- Use CSS-only toggles with `<input type="checkbox">` and
  sibling-selector tricks; less reliable but JS-free.

The prototype illustrates the *shape* of layered reading; a
production renderer must respect the constitutional commitment that
the bare canon is always available, not just when JS is on.

### 7.2 The URN grammar was under-specified

`COMMENTARY_ATTACHMENT_MODEL.md §1` defines the anchor format
abstractly:

```
archive:<target-kind>:<target-id>[:<sub-locator>]
```

In practice, the **number of `::`-separated components inside
`<target-id>` varies by kind**:

- `tale:<text>::<n>` — 2 components
- `passage:<text>::<trans>::<pid>` — 3 components

A single regex cannot parse all kinds correctly without backtracking;
the renderer needs kind-specific patterns. The architectural document
was correct in spirit but under-specified in grammar. **The first
implementation pass hit this and parsed tale anchors as if they
carried a translation component** — caught only by manual inspection
of the rendered tale-level commentary count.

Recommended fix in the architecture document: include a formal
grammar (BNF or equivalent), or at minimum a kind-by-kind component-
count table. The prototype's `ANCHOR_PATTERNS` dict (kind → regex)
is a working reference.

### 7.3 The `prototype_note` field is honest pollution

Every record in this prototype carries an explicit `prototype_note`
field describing it as a prototype demonstration. This is honest —
a future reader of these records knows they are not production
commentary. But the field is **prototype-only**; production records
would not carry it. The schema sketch (`COMMENTARY_SCHEMA_SKETCH.md`)
does not include it.

The asymmetry is: the prototype records are MORE honest than
production records will need to be, because the prototype is itself
a stranger thing than a normal record. **A future implementation
should drop `prototype_note` from production records** — it would be
clutter in a record meant to last centuries.

But before dropping it, the prototype records should be archived
under `logs/_archive/` with their `prototype_note` intact, so the
prototype phase is preserved in stewardship memory even after the
production records replace these.

### 7.4 The AI-record authorship ambiguity

The AI record (`ai-2026-05-14-apannaka-hercules-crossroads-parallel`)
lists `archive:ai:claude-opus-4-7` as both the `provenance.author`
and (through the body) the substantive author of the suggested
parallel. The `stewardship_log[0].by` field is also
`archive:ai:claude-opus-4-7`.

But the record exists at all because a human steward asked the AI
to produce a prototype demonstration. Should the record reflect
that joint authorship? The simplest options:

| Pattern | `provenance.author` | `stewardship_log[0].by` |
|---|---|---|
| **Pure AI** (current) | `archive:ai:claude-opus-4-7` | `archive:ai:claude-opus-4-7` |
| **AI body, steward record** | `archive:ai:claude-opus-4-7` | `archive:steward:steve` |
| **Steward proxy** | `archive:steward:steve(citing AI)` | `archive:steward:steve` |

The current prototype uses the first pattern. The second is
arguably more accurate: the AI authored the *content*, but the
*record-as-record* was created by the steward in the act of
constructing the prototype.

This matters because the constitution requires named authorship for
every record (`INTERPRETIVE_BOUNDARIES.md §3.1`). If a steward
selectively records AI output (rather than batch-generating it),
the steward's selection is itself an editorial act with provenance.
**The recommendation is the second pattern**: distinguish body
authorship from record creation. The schema sketch should reflect
this in a future revision.

### 7.5 Visual layer distinction is UI invention, not archival typography

The prototype's CSS uses colored left-borders and small badges to
distinguish layers visually. It works, but it is **UI invention**,
not the typographic conventions historical printers used for
apparatus and commentary (footnote-with-rule, marginalia, indented
quotation blocks, italic glosses).

The renderer is a prototype; it does not claim to be a model for
the production reading interface. The borders-and-badges approach
is a placeholder. A production renderer should be designed by
someone who has actually looked at historical apparatus layouts
(Talmud-page traditions, *mūla*-with-*bhāṣya* Sanskrit print
conventions, critical-edition footnote stacks). The visual side of
commentary reading is centuries old and deserves better than
generic CSS.

Recorded here only so future stewards know the prototype's CSS is
not the model.

### 7.6 The schema sketch's `body_in_other_record` field is half-built

The Layer-3 bridge record references a target like
`archive:passage:jatakatthakatha::primary-translation::1.0.prologue`
in `body_in_other_record`. This URN follows the passage anchor
grammar but its target text (`jatakatthakatha`) does not yet exist
in the archive. The renderer detects `body=null` and shows the
gap, which is good.

But there is no formal mechanism in the schema sketch for:

- Marking a bridge as **expected to resolve in the future** vs
  **expected to never resolve** (e.g., a bridge to a lost commentary).
- Recording when a bridge **did** resolve (when the Jātakaṭṭhakathā
  is finally acquired, the bridge should "light up" — but the
  schema does not say so today).
- Distinguishing a `body: null` bridge record from a `body: null`
  *error* in a normal record.

These are small future-schema concerns, not constitutional ones.
Worth noting before adoption.

---

## 8. What worked well

Recorded so the patterns can be reused.

- **Stand-off filing.** Commentary in sibling files; the canonical
  passage file is unchanged. The architecture's strongest commitment
  to non-destruction is preserved trivially.
- **Layer-mismatch detection at load time.** The non-collapse rule
  is mechanically enforced, not just visually. A future steward
  cannot accidentally cross-layer-contaminate the file structure
  without the renderer refusing to load.
- **Multi-anchor rendering.** Records with anchors at both
  tale-level and passage-level (record 2, scholarship) appear in
  both places naturally. The schema's multi-anchor design works.
- **Bridge-gap honesty.** A `body: null` Layer-3 record renders as
  an honest gap, not as fabricated content. The constitutional
  commitment to recording gaps rather than filling them holds in
  the rendered surface.
- **Verbatim discipline.** The renderer escapes HTML special
  characters but does no other transformation. The `[95.]` page
  bracket survives in 1.1; canonical bytes are preserved through
  rendering.
- **Idempotent output.** Re-running the renderer produces
  byte-identical HTML. No timestamps, no random orderings, no
  run-specific identifiers. Important for long-term archival
  stability and for git-friendly diffs.
- **AI-quarantine via CSS class.** The AI layer is off by default
  via the initial body class. A reader must take explicit action to
  see AI content. Constitutional commitment to quarantine is
  visually and structurally enforced.

---

## 9. What should change before scaling

Not blocking, but should be addressed when implementation moves from
prototype to production:

1. **Bare-canon mode must work without JavaScript.** See §7.1.
2. **The anchor URN grammar needs a formal BNF specification** in
   `COMMENTARY_ATTACHMENT_MODEL.md`. See §7.2.
3. **`prototype_note` is prototype-only**; production records will
   not carry it. See §7.3.
4. **AI-authorship convention** should distinguish body authorship
   from record creation. See §7.4.
5. **The visual layer system needs a real designer**. The
   prototype's CSS is a placeholder. See §7.5.
6. **Bridge state vocabulary** (`expected`, `resolved`, `lost`) for
   Layer-3 records. See §7.6.
7. **The renderer should produce a structured machine-readable
   index** of which commentary records anchor where, for downstream
   tools (search, citation export). The current renderer only
   produces the HTML.
8. **An end-to-end integrity test that includes commentary** — the
   `passage_subsequence_proof.py` covers primary text; a sibling
   check should verify that commentary anchors all resolve, that no
   record's `provenance.layer` mismatches its file, that no record
   has empty mandatory fields. Closes the validation loop.

---

## 10. What should absolutely NOT scale

These are constitutional refusals (per `INTERPRETIVE_BOUNDARIES.md`)
reinforced by what the prototype made tangible.

1. **Auto-generation of commentary across the corpus.** The five
   prototype records took deliberate steward time. Producing 5,000
   of them with an AI loop would compromise quality, provenance,
   editorial sovereignty, and the layer-discipline that makes
   commentary trustworthy.
2. **Embedding-based "similar passage" overlays at scale.** Not
   constitutionally forbidden — a steward could write a Layer-5
   record citing an embedding similarity — but generating thousands
   of unreviewed AI cross-references is a §4.4 violation.
3. **Auto-classification of source-internal commentary.** When
   traditional commentary is eventually acquired (the
   Jātakaṭṭhakathā, the tafsīr corpus, etc.), the archive does not
   impose category tags on the witness's voice (`COMMENTARY_ONTOLOGY.md
   §2`). The prototype's tagged records are the steward's
   classifications of the *steward's own* records. The same
   discipline must hold at scale.
4. **Treating the prototype renderer as a production-reader.** The
   borders-and-badges CSS, the JS-dependent bare-canon mode, the
   single-file HTML output — all are prototype shortcuts. A
   production reader is a different design problem.
5. **Live commentary editing in the reader.** Layer 7 (private
   annotations) belongs in reader storage, not the canonical
   record set. The renderer does not surface a "comment on this"
   button; if it did, the constitutional separation of
   reader-local notes from archive-canonical commentary would
   blur.

---

## 11. Closing observations

The constitutional architecture survives contact with reality, with
six small caveats noted in §7. None of the caveats are
philosophical; all are implementation refinements. The constitution
as written is structurally sound.

The pressure point that mattered most — the bare-canon guarantee —
passes mechanically. A reader can reach the canonical Apannaka
text exactly as the integrity proof verifies, even with a
prototype renderer that adds commentary overlays around it. The
overlays do not touch the canon. The canon does not depend on the
overlays. The constitutional ordering holds.

The work in §9 is the natural next agenda when the archive returns
to commentary implementation. The work in §10 is the discipline that
must hold for the next century.

The prototype is small, local, and reversible. It was meant to be.
The commentary infrastructure of the archive begins here — with
five records, one tale, one HTML file, and a list of honest
findings about where the law and the practice meet.

---

*Snapshot of the prototype state preserved at the top of the
canonical Apannaka directory and at
`06_workspace/commentary_prototype.html`. The constitutional
documents that govern this work are at the project root with names
beginning `COMMENTARY_`, `PROVENANCE_`, or `INTERPRETIVE_`. The
illustrative JSON schema is at `COMMENTARY_SCHEMA_SKETCH.md`. The
prototype renderer is at `05_scripts/render_commentary_prototype.py`.*
