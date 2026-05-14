# READING_ROOM_CONSTITUTIONAL_AUDIT_2026

**Date:** 2026-05-14.
**Scope:** The existing public Reading Room at `03_web_app/index.html`
(177 KB, single file, plain HTML/CSS/JS) and its data shipment under
`03_web_app/data/`.
**Question:** Does the Reading Room still faithfully express the
archive's constitutional commitments?
**Answer:** Mostly, but not yet. Several seams are already correct.
Several others are silently incompatible. None is fatal. None requires
rewriting the Reading Room.

This is an institutional audit, not a redesign sprint. No major
changes are proposed in this document. The recommendations in §10 are
categorized by safety; the dangerous category is the most important to
read.

---

## 1. Method

The audit read the Reading Room's rendering pipeline, URL/link
mechanics, data loading, search index, compare mode, and the export
pipeline that feeds it, against the May 2026 constitutional documents:

- COMMENTARY_CONSTITUTION
- PROVENANCE_LAYERS
- COMMENTARY_ATTACHMENT_MODEL
- INTERPRETIVE_BOUNDARIES
- COMMENTARY_LIFECYCLE
- COMMENTARY_VERSIONING
- CITATION_PERMANENCE
- COMMENTARY_MIGRATION
- COMMENTARY_REPAIR_PROTOCOLS
- AI_STEWARDSHIP_POLICY
- PUBLIC_PRIVATE_BOUNDARIES
- PERMANENCE_PROTOTYPE_2026

There is no STANDARD.md in the archive. The Reading Room's conventions
are encoded directly in `index.html` — CSS variables, register classes,
inline comments. Where this document quotes Reading Room conventions,
they come from the code itself.

The audit makes no changes to the Reading Room. Where prototype
sketches appear, they are illustrative only.

---

## 2. Constitutional compatibility, point by point

The table below records the audit's judgement against each commitment
the constitutional documents place on the public face. The verdict
column uses three values: **YES** (the Reading Room already preserves
this commitment), **PARTIAL** (preserved in spirit but with named
gaps), and **NO** (not preserved at all; no current mechanism).

| Commitment | Verdict | Notes |
|---|---|---|
| Primary text sovereignty | PARTIAL | Passages render byte-equivalent at the data layer (`p.text` passes through `textContent`), but the renderer flattens `\n→ ' '` and rewrites inline `[N]` / `[*N]` markers as anchor elements. The canonical record survives; the rendered surface does not preserve every byte. |
| Bare-canon guarantee | PARTIAL | No UI affordance to suppress overlays. Annotations always render below the passage if present. Inline footnote linkification cannot be turned off. |
| Provenance separation | PARTIAL | The CSS already has three visual registers — `.apparatus-body` (warm tan), `.footnote-body`, `.annotation-note` (blue) — and the code comment at lines 3175–3178 explicitly names this as **constitutional**: "Müller's voice and the archive's voice must remain visually separable." The vocabulary exists. It is hard-coded to one apparatus author (Müller) and to two implicit layers; it does not yet generalize to the seven-layer model. |
| Layer distinction in data | NO | Passage annotations are `{label, id, text}` with no `provenance.layer`, `author`, `date`, or `lifecycle_state`. The renderer cannot distinguish editorial annotation from scholarly annotation from AI annotation because nothing in the record names which it is. |
| Non-destructive overlays | YES | Overlay markers (`[*N]`, annotation markers) do not modify the underlying passage record. The reading view augments; it does not edit. |
| Citation permanence | NO | Permalinks are `?text=<data_file>&p=<pid>` where `data_file` is a mutable filename and `pid` is the raw passage id. Neither is a URN. There is no alias resolution, no URN parsing, no honest "retired" response. `localStorage` uses `data_file` as the bookmark key, so user history breaks silently if any text is renamed. |
| Honest gaps | PARTIAL | Compare mode is honest: "these translations don't share passage IDs — shown side-by-side only." But apparatus markers (`[*N]`) render as anchors even when no apparatus body exists — clicking does nothing, with no diagnostic. (See §4.) |
| Withdrawal visibility | NO | No commentary records are currently loaded into the Reading Room, so there is nothing to withdraw. If they were, the rendering pipeline has no concept of `lifecycle_state`. |
| AI quarantine | NO | The renderer would treat an AI annotation identically to an editorial annotation; no badge, no register, no opt-in. |
| Migration visibility | NO | No `migration_policy` field is read. No `schema_version` awareness. No `@<date>` suffix handling in URLs. |
| Bare-canon access without JavaScript | NO | The reader is a JS-only renderer. With JS disabled, the page is a `<style>` block and an empty `#shell`. This was noted as a known tension in COMMENTARY_PROTOTYPE_2026; it remains. |

The two PARTIAL verdicts on provenance and primary-text sovereignty are
the most consequential because they describe seams that are *almost*
right. The full NOs on citation permanence and layer distinction in
data are not failures of the Reading Room so much as failures of the
pipeline feeding it.

---

## 3. The apparatus silent-gap

This is the most concrete operational finding, and it is a hidden
breach of the honest-gaps commitment, not a hypothetical one.

The Reading Room's rendering code (`index.html` ~3168–3196) treats `[*N]`
in passage text as an apparatus reference. It builds an anchor element
that, on click, looks up `currentData.apparatus_page_boundaries[]` and
`currentData.apparatus[]` to find the apparatus body.

The canonical archive carries apparatus_*.json — e.g.
`01_library/library/texts/sacred/hindu/upanishads-muller-part2/apparatus_muller-part2.json`
— with the correct structured anchors (`apparatus[].anchors[{passage_id,
anchor_text}]`).

The export pipeline at `05_scripts/export_reader_data.py` does not
propagate apparatus into the per-text deploy JSON. (A `grep apparatus`
of the export script returns one match: a `front_matter` line, and even
that does not match. No apparatus, no boundaries.)

Result: passages in the deploy still carry the `[*N]` markers verbatim
(`[*1]`, `[*2]`, etc. — visible in the deployed Upaniṣads files). The
renderer turns those markers into clickable affordances. Clicks find
no body and silently do nothing.

This is the "renders honestly-by-omission, not honestly-by-design"
pattern named in §8 of this audit. The marker is shown; the body is
absent; the user is given no indication that the body exists somewhere
else in the archive or that it has not yet been published.

Per COMMENTARY_REPAIR_PROTOCOLS.md, an unresolved anchor is a
fail-honestly event. The Reading Room currently fails silently. This
is the single highest-priority constitutional repair.

---

## 4. Architectural mismatches

The following patterns in the current Reading Room implicitly assume
things the constitutional architecture says are not true.

### 4.1 Mutable identifiers as primary keys

`data_file` is treated as the canonical handle in three places: URL
parameters (`?text=<data_file>`), `localStorage` (`da-last`,
`da-recents`, `da-progress`, all keyed by `data_file`), and the global
search index (`m.data_file`). If any translation's data_file is ever
renamed by a future ingest, every external citation to it, every user
bookmark, and every progress record breaks silently.

Constitutional contrast: CITATION_PERMANENCE.md §4 explicitly forbids
this pattern. URNs are the canonical identifier; URL forms are
presentation conveniences. The Reading Room currently has the
relationship inverted.

### 4.2 Simplified authority

Annotations are flat dictionaries `{label, id, text}`. They look like
they were authored by the archive but in fact they were ingested with
the canonical record. There is no field naming the author, the
authoring layer, the date, or the lifecycle state.

Constitutional contrast: PROVENANCE_LAYERS.md says these layers must
never collapse. The current annotation record is itself a small
layer-collapse: archive editorial voice has been merged with whatever
upstream included it in the source pipeline.

### 4.3 Single-layer interpretation

The renderer recognizes two non-canonical voices: apparatus (one
hard-coded author, Müller) and annotation (one undifferentiated
"archive's voice"). The seven-layer model in PROVENANCE_LAYERS.md
expects: primary text / source apparatus / traditional commentary /
modern scholarship / archive editorial / AI / private. The Reading
Room can express two of those distinguishably and conflates the others.

### 4.4 Stable URLs without migration awareness

No URL parameter for `as_of=<date>`, no recognition that a passage may
have been re-keyed, no alias following. The URL is treated as a
straight pointer into current state, not a citation into a moment.

### 4.5 Commentary collapse (latent)

There is no commentary infrastructure to collapse, yet. But the path
of least resistance — extending the `[N]` / `[*N]` inline regex to
include `[c-...]` commentary markers — would collapse the standoff
discipline. The constitution names standoff sibling files as the
canonical attachment model. The renderer's inline-marker convention is
a tempting but constitutionally wrong way to attach commentary.

### 4.6 Hidden provenance

Annotations render with a simple marker and an expandable note. No
visible "added 2026-04-12 by archive steward" line. The user cannot
distinguish a 1924 editorial note from a 2026 stewardship note from a
future AI annotation.

### 4.7 Renderer-centralized truth

The Reading Room infers anchors at render time by regex-splitting the
passage text. The data does not declare its own anchors — the renderer
discovers them. This means the truth about where an anchor points is
implicit in the marker convention. If the convention changes, the data
breaks invisibly.

Constitutional contrast: COMMENTARY_ATTACHMENT_MODEL.md treats anchors
as declared structured fields, not as inferred from formatting.

### 4.8 "Current version only" assumptions

No URL handles a frozen-generation request. No mechanism returns a
schema-v1 record alongside the schema-v3 reader. The Reading Room
implicitly assumes one current state.

---

## 5. What already works, surprisingly well

The Reading Room predates most of the constitutional architecture. It
would be reasonable to expect it to feel obsolete. It does not. Several
decisions made early aged well.

### 5.1 The three-register CSS

`.apparatus-body`, `.footnote-body`, `.annotation-note` are already
visually distinct enough that a reader can see voices change. The code
comment at lines 3175–3178 reads:

> "The apparatus body is rendered with class .apparatus-body (warm tan
> register, distinct from the cooler .footnote-body and the blue
> .annotation-note). The distinction is constitutional: Müller's voice
> and the archive's voice must remain visually separable."

That comment was written before COMMENTARY_CONSTITUTION.md existed.
The Reading Room author recognized a constitutional principle before
the constitution was written down. The CSS register vocabulary is the
single most load-bearing thing the current Reading Room has done
correctly. It generalizes cleanly to seven layers; it just needs more
registers.

### 5.2 The clickable passage reference

Each passage's reference is a clickable element (`copyPassageLink`) that
copies the permalink. This is exactly the right injection point for a
URN-aware future: add a second "Copy URN" affordance and the citation
discipline becomes opt-in for advanced users without disturbing casual
ones.

### 5.3 The front_matter schema

Front matter is already structured: `kind` + `label` + `body`,
rendered in collapsible `<details>` blocks. This is one short step from
carrying provenance metadata. (155 of 1261 texts in the deploy carry
front_matter today.)

### 5.4 Compare mode honesty

When two translations don't share passage IDs, compare mode says so
explicitly: `"these translations don't share passage IDs — shown
side-by-side only"`. It also surfaces partial alignment numerically
(`partial alignment — 47 shared`). This is exactly the institutional
tone the rest of the architecture has been moving toward.

### 5.5 Local-first state hygiene

`da-recents` is capped at 5 entries. `da-progress` is per-file scalar.
`da-last` is a single object. No analytics, no telemetry, no
fingerprinting. This is forward-compatible with the
PUBLIC_PRIVATE_BOUNDARIES.md "reader-local" publication degree.

### 5.6 Render batching

The 200-passage batch + Load More button is appropriate scale
discipline for a text that may have 30,000 verses. The pattern is
useful for commentary, too — a tale with 200 commentary records should
not render all of them on first paint.

### 5.7 No SPA, no framework

The Reading Room is plain HTML, plain CSS, plain DOM, two `fetch` calls
(`getJSON`, a search-index load). It will still work in a 2046 browser
because it does not assume any modern framework, build pipeline, or
package registry. This is itself a permanence guarantee.

DecompressionStream and URLSearchParams are the most modern APIs it
uses; both are present in every browser shipped after 2020 and are
trivially polyfillable.

### 5.8 Apparatus shape on the canonical side

The canonical `apparatus_*.json` schema (`apparatus[].anchors[{passage_id,
anchor_text}]`) is already in the right shape for the standoff
commentary model. The export pipeline is the missing piece, not the
data shape.

---

## 6. URL philosophy

### 6.1 What the Reading Room URL is

A presentation-layer convenience pointing at the currently-shipped data
file:

```
https://stevenfrye30.github.io/Digital-Archive/?text=jataka-chalmers-vol1_chalmers.json&p=1.1
```

This URL is fragile under any of: data_file rename, translation re-key,
passage re-id, registry restructure.

### 6.2 What the URN is

A canonical identifier, resolver-anchored:

```
archive:passage:jataka::chalmers-vol1::1.1
```

This URN is permanent under the alias-table discipline of
CITATION_PERMANENCE.md §4.

### 6.3 Relationship

The URL is one presentation of the URN. The URN should be the canonical
identity; the URL is the convenience form for browsers. They should be
inter-derivable but the URN is the authoritative side.

The Reading Room currently has this inverted: the URL is authoritative,
the URN does not exist.

### 6.4 Redirects

A URL redirect that follows a `data_file` rename without an entry in
`aliases.json` would silently launder citation history. That is
constitutionally forbidden.

A URL redirect that *consults* `aliases.json` is safe and is the
correct integration point.

### 6.5 Link rot, today

The longer the Reading Room has been public, the more external
citations to its URL form exist. Each one points at a `(data_file,
pid)` pair. Each is exposed to data_file rename. The risk is real but
bounded: data_file renames have historically been low-frequency, and
the corpus is small enough that an alias table seeded from git history
could repair most existing rot.

### 6.6 Resolver integration, feasibility

A `?urn=...` URL parameter routed through a JS-side bridge that
consults a small alias table is feasible without any structural Reading
Room change. The renderer downstream does not need to know URNs exist:
the URL→loadText path simply gets a "if URN, resolve to (data_file,
pid), then proceed" preamble.

This integration is **additive**, not destructive. It does not require
breaking existing `?text=&p=` URLs.

---

## 7. Commentary-readiness audit

Without implementing commentary, the question is: can the Reading Room
eventually support each of the architecture's commentary features?

| Feature | Reachable? | What's needed |
|---|---|---|
| Layer toggles | YES | Add `data-layer` attribute to register CSS; route toggles by attribute. |
| Provenance display | YES | Generalize the `.apparatus-meta` line ("Müller — page X, footnote N") into a layer-aware byline ("Editorial — archive:steward:steve — 2026-05-14"). |
| Supersession visibility | YES | Renderer reads `lifecycle_state` from commentary records; adds a "superseded — see successor" inline link. |
| Withdrawn record display | YES | Add a `.withdrawn` modifier class. Body remains visible, struck-through or muted. |
| AI quarantine | YES | Add `.layer-ai` register (probably muted gray). Add an opt-in checkbox; default off. |
| Frozen generations | HARDEST | Renderer must gracefully handle records whose fields don't match the current schema. This is forward compatibility, not commentary-specific. |
| Historical citation rendering | YES | URN-aware URL routing with `@<date>` suffix support, handed to the resolver. |
| Commentary attachment visibility | YES | Export pipeline learns to bundle commentary_*.json. Reading Room learns a per-text commentary registry. |

The features that would break the existing design are: extending inline
`[N]` / `[*N]` markers to commentary anchors (would collapse the
standoff discipline; see §4.5); injecting commentary as additional
passages in the passage stream (would collapse layer separation);
treating commentary as a new annotation type without adding the
provenance fields (would replicate §4.2).

The features that are easiest to add cleanly are: standoff commentary
loading (modeled on the existing apparatus pattern), layer-aware
registers (generalization of existing CSS), URN-aware URL routing
(additive).

---

## 8. Typography and visual hierarchy, philosophically

Not aesthetics. Meaning.

### 8.1 Does the current visual hierarchy privilege commentary over canon?

No. Canon is large serif Georgia at 1.9 line-height in a 1100px-wide
column. Apparatus is smaller, warm-tan, behind a click. Annotations
are smaller, blue, behind a click. The canon visibly dominates. Good.

### 8.2 Can provenance remain visible without overwhelming the reader?

Yes, in principle. The current `.apparatus-meta` line ("Müller —
page X, footnote N") is small and unobtrusive. A future generalization
("Editorial — 2026-05-14 — provisional") is the same shape. As long
as the byline lives in the small-meta register and is part of the
disclosure-widget content (not the always-visible passage), it does
not overwhelm.

The danger is overdesign: badges, color codes, icons, hover cards.
Restraint here is itself a constitutional posture.

### 8.3 Are layers visually representable?

Yes. The current three-register palette can extend to seven with
minimal additions:

- Primary text — current reader body (no register, just text).
- Source apparatus — current `.apparatus-body` (warm tan).
- Traditional commentary — new register, warmer (e.g. cream).
- Modern scholarship — new register, cooler (e.g. pale slate).
- Archive editorial — current `.annotation-note` (blue).
- AI — new muted register (e.g. gray), opt-in only.
- Private — only visible to the local reader; no public register
  needed.

Each register is one CSS class. Total addition: three to four classes.

### 8.4 Can honest gaps be rendered honestly?

Currently, in compare mode only. Outside compare mode, a missing passage
(e.g. a redacted text) just doesn't appear. There is no "this text
exists in the corpus but is not currently displayable" surface.

A future improvement is a "redacted / restricted / not yet published"
placeholder card in the catalog, with the existing `.gs-sub` styling
generalizing to it.

### 8.5 Can uncertainty remain visible?

Not yet. A provisional commentary record would render identically to a
verified one. The architecture defines the lifecycle states; the
Reading Room would need a small visual vocabulary for them. Italic
text for provisional, normal for verified, strikethrough for withdrawn
is a reasonable starting palette.

---

## 9. Failure behavior

What happens, today, if:

| Scenario | Current behavior | Constitutional expectation |
|---|---|---|
| URN resolves to orphaned record | Falls through to `data_file` lookup, generic error. | Surface lifecycle_state, name the orphan, suggest the related canonical anchor. |
| Commentary withdrawn | (No commentary loaded.) | Render body with withdrawal banner. |
| Multi-generation alias chain | URLs don't go through resolver — no alias following. | Follow chain, show the trail in the diagnostics. |
| Passage exists, commentary doesn't | Passage renders normally. | Correct — commentary absence is the default state. |
| AI commentary exists but quarantined | Would render identically to editorial annotation. | Render only when explicitly enabled; quarantine badge always visible. |
| Frozen generation requested | Not supported. | Honor the @<date> suffix, return the schema-v1 record alongside a "you are viewing a historical generation" banner. |
| Missing data_file in URL | "Could not load text: <error>" — generic. | Consult aliases.json. If not aliased, name what was requested and what's missing. |
| Missing passage id in valid data_file | URL accepted, no scroll, no message. | Inform the reader that the passage does not exist in this generation. |
| Apparatus marker `[*N]` in passage with no apparatus body | Anchor renders; click does nothing. | (See §3.) Highest-priority repair. |
| Renamed text whose old URL is still cited externally | Silently fails. | Consult aliases.json; redirect with visible "this citation was re-keyed on 2026-XX-XX" notice. |

The pattern is consistent: the Reading Room fails by omission, not by
design. It does not lie, but it does not narrate. Constitutional
practice asks for narration: name the failure, name the cause, name
the remediation if any.

---

## 10. Recommendations, in three categories

The categorization matters more than the items.

### A. Safe to do immediately

These are additive changes that do not disturb existing behavior and
do not depend on the constitutional infrastructure being further built
out. They reduce silent failures without committing to new shape.

1. **Repair the apparatus silent-gap (§3).** Either extend
   `export_reader_data.py` to ship the canonical apparatus alongside
   passages, or strip the `[*N]` markers from passages whose deploy
   does not carry apparatus. Current state is honest-by-omission of
   the wrong sort: the markers imply something exists when nothing
   does. Shipping the apparatus is the better repair.

2. **Add a tooltip to `[*N]` markers** that names what they reference
   ("Apparatus footnote — click to expand"). Even before §1 is done,
   this makes the markers' purpose legible.

3. **Add a "Copy URN" affordance** alongside Copy Link. The URN form is
   constructible today from `(text_id, translation_id, passage_id)` —
   all three are already present in the deployed records. Casual
   readers ignore it; citation-disciplined readers gain a permanence
   guarantee.

4. **Reserve a `?as_of=<date>` URL parameter.** Currently it would be
   ignored. Reserving it future-proofs external citations whose
   authors are forward-thinking enough to use it before the resolver
   supports it.

5. **Add a small stewardship-status footer to each text page.** It can
   draw entirely from existing fields (`quality`, `source_summary`,
   `restoration_note` where present). This makes the existing
   stewardship layer visible without requiring new schema.

6. **Document the CSS register system in a STANDARD.md** (or
   READING_ROOM_CONVENTIONS.md). The constitutional comment at
   index.html ~3175–3178 should be promoted to a real document so
   future renderer changes cannot accidentally collapse the registers.

7. **Document this audit's findings in the public README** under the
   stewardship section.

### B. Requires architectural extension

These are not difficult, but they require coordinated work on the
export pipeline, the canonical data schema, or the resolver. They
should happen only after the architecture they depend on is itself
stable enough to expose to readers.

1. **Standoff commentary loading.** Export pipeline learns to bundle
   `commentary_*.json` and `attachments_*.json` alongside passages.
   Reading Room learns a per-text commentary registry and a
   register-aware renderer. This is the largest single new pipeline.

2. **Layer-aware annotation records.** Existing `p.annotations[]` need
   `provenance.{layer, author, date, lifecycle_state}` fields, with
   forward-compatible defaults (missing fields → archive editorial /
   provisional). Migration manifest required per
   COMMENTARY_MIGRATION.md.

3. **URN as canonical permalink identity.** A thin URN-aware bridge in
   the URL handler: if `?urn=...` is present, resolve it through a
   client-side or pre-built alias table and proceed. The existing
   `?text=&p=` form remains supported.

4. **Resolver integration at the URL layer.** Either ship
   `aliases.json` for client-side lookup, or pre-resolve at export
   time and ship redirect pointers. The constitutional answer is
   client-side: the resolver contract is what should travel, not its
   results.

5. **Lifecycle visualization vocabulary.** Italic for provisional,
   strikethrough for withdrawn, "→ successor" inline for superseded.
   Small additions to the existing CSS register palette.

6. **AI quarantine toggle.** A top-of-text checkbox, off by default,
   that controls visibility of Layer 6 commentary. Per
   AI_STEWARDSHIP_POLICY.md, never on by default.

7. **Honest gap surfaces.** A "restricted / redacted / not yet
   published" placeholder card for texts the corpus knows about but
   does not display. Generalization of the existing catalog entry.

### C. Constitutionally dangerous; should be avoided

These are the most important recommendations in this audit. They are
all things the Reading Room could plausibly do, and all of which would
be a regression against the constitutional commitments — sometimes a
subtle one. They are listed not as predictions of error but as
guardrails.

1. **Do not migrate to a SPA framework.** The Reading Room's
   plain-HTML resilience is itself a permanence guarantee. React, Vue,
   Svelte, etc. introduce build pipelines and dependency graphs that
   will not survive twenty years. Plain DOM survives.

2. **Do not combine annotations and commentary into one record
   stream.** They are different layers (PROVENANCE_LAYERS.md). The
   visual register vocabulary already encodes this distinction; the
   data layer should preserve it.

3. **Do not silently follow alias chains in the URL.** A redirected
   citation should arrive at the new URL *with* a visible "this
   citation was re-keyed on 2026-XX-XX" notice. Silent redirects
   launder citation history (CITATION_PERMANENCE.md §6.2).

4. **Do not expose URNs as the default URL form before readers are
   ready.** URNs are for citations and machines. Casual readers should
   see the existing human-friendly URL form. Both should be available;
   only one should be default-visible.

5. **Do not add commentary as inline markers in passage text.**
   Extending the `[N]` / `[*N]` regex convention to include
   `[c-archive:commentary:foo]` markers is a tempting shortcut and a
   constitutional regression. It would collapse the standoff
   discipline (COMMENTARY_ATTACHMENT_MODEL.md). Commentary anchors
   must remain in separate, structured JSON records.

6. **Do not hide withdrawn commentary as "deleted."** Per
   COMMENTARY_LIFECYCLE.md §3.6, withdrawal is visible-not-erased. The
   Reading Room must give withdrawn records a visible state, not
   omit them.

7. **Do not ship apparatus markers in passages without apparatus
   bodies.** This is the current state (§3). Pick a side: either ship
   the bodies or strip the markers. The current state is the worst of
   both worlds — it implies content that does not exist.

8. **Do not rewrite the Reading Room.** This audit confirms that
   compatibility with the new architecture is reachable through
   additive changes. A rewrite would break externally-cited URLs
   without yielding a single new constitutional guarantee. The
   institutional cost would be high; the institutional gain would be
   zero.

9. **Do not run analytics or telemetry on the Reading Room.** The
   "reader-local" publication degree in PUBLIC_PRIVATE_BOUNDARIES.md
   §3 implies the reader's behavior is itself private. Local storage
   is acceptable; remote logging is not. The Reading Room already
   complies; it should continue to.

10. **Do not assume single authority.** The largest design failure
    pattern in archival software is assuming that the archive itself
    is the only voice. The Reading Room already partially refuses this
    (`.apparatus-body`, `.annotation-note` are distinct). Future
    changes must continue to refuse it.

---

## 11. What this audit found, in one paragraph

The Reading Room predates the May 2026 constitutional work and was
designed without explicit awareness of the seven-layer provenance
model, the URN scheme, the lifecycle taxonomy, the alias table, or the
quarantine policy for AI-generated material. Despite this, the Reading
Room's core decisions — the three-register CSS, the front-matter
schema, the standoff-friendly apparatus data shape on the canonical
side, the compare-mode honesty, the plain-HTML resilience — are
already constitutionally compatible. Two real gaps exist: a silent
apparatus mismatch in the deploy pipeline, and a structural reliance
on mutable data-file identifiers as primary keys. Neither is fatal.
Neither requires rewriting the Reading Room. Both can be repaired
additively. The CSS register vocabulary, in particular, was a
constitutional intuition recorded in the code before the constitution
was written, and it generalizes cleanly to the full seven-layer model
with three or four additional classes. The most important
recommendations in this audit are the *prohibitions* — the things the
Reading Room could plausibly do that would collapse the architecture
beneath it.

---

## 12. What this audit does not propose

- A redesign.
- A rewrite.
- A new reader implementation.
- A React/Vue/Svelte migration.
- A styling pass.
- Commentary ingestion.
- A production rollout.
- A new framework, new package, new build pipeline.
- Removal of any existing feature.

This audit proposes the categorization in §10 and the prohibition list
in §10C. Nothing else. Implementation belongs to later phases.

---

## 13. Reading order

A future steward who arrives here cold should read:

1. This document.
2. `PERMANENCE_PROTOTYPE_2026.md`.
3. `COMMENTARY_CONSTITUTION.md`.
4. `PROVENANCE_LAYERS.md`.
5. `03_web_app/index.html`, specifically the rendering-pipeline
   functions (`_renderBatch`, `findApparatusForPassage`,
   `toggleApparatusBody`, `renderTextWithFnRefs`, `passageLinkURL`,
   `loadText`).
6. `01_library/library/texts/sacred/hindu/upanishads-muller-part2/apparatus_muller-part2.json`
   — the exemplar of correctly-shaped canonical apparatus.

That is enough context to understand what the Reading Room is, what
the architecture beneath it has become, and where the two have drifted
out of alignment. The drift is small. The repair is patient.
