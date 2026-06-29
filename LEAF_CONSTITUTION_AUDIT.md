# Leaf Constitution Audit

*Compiled 2026-05-21. Phases 1-6 of the Leaf Constitution arc.
Companion to `WITNESS_FAMILY_CONSTITUTION.md`,
`GENESIS_HARMONIZATION_AUDIT.md`, `GENESIS_READING_FLOW_AUDIT.md`,
and `ATLAS_EDITORIAL_AUDIT.md`. Observation + specification;
Phase 7 implements; Phase 8 verifies.*

This audit grounds itself in `reports/walk_v72_*.png` and
`reports/walk_v72_metrics.json` — visual evidence captured
against the codex's current state (post-v71). The metrics
table for each family is given below where relevant.

The brief: every witness leaf must become a recognizable
manuscript tradition. Not just a styled variant of a uniform
modal. The reader should feel "this is a sacred-site
inscription" or "this is a linguistic gloss" or "this is an
archival commentary" before they read the title. Each family
remains distinct; the codex remains one volume.

---

## Phase 1 — Leaf Audit

### Current state — what every text-witness leaf shares today

A structural read of the five sampled families' computed
styles shows them sharing the same chrome:

| Property              | Commentary | Linguistic | Architecture | Reception | Doré      |
|-----------------------|-----------:|-----------:|-------------:|----------:|----------:|
| Leaf bg               |  cream     |  cream     |  cream       |  cream    |  transparent |
| Leaf max-width        |  800 px    |  800 px    |  800 px      |  800 px   |  1500 px  |
| Leaf padding          |  56 / 64 px|  56 / 64 px|  56 / 64 px  |  56/64 px |  0        |
| Leaf box-shadow       |  **none**  |  **none**  |  **none**    |  **none** |  none     |
| Leaf border-radius    |  0 px      |  0 px      |  0 px        |  0 px     |  0 px     |
| Provenance present    |  yes       |  yes       |  yes         |  yes      |  no       |
| Provenance margin-btm |  22 px     |  22 px     |  22 px       |  22 px    |  —        |
| Verse "Gen X:Y"       |  identical |  identical |  identical   |  identical|  in plaque|
| Title font-style      |  italic    |  roman     |  italic      |  italic   |  italic   |
| Title font-weight     |  400       |  500       |  500         |  500      |  500      |
| Title font-size       |  fall-thru |  17.28 px  |  17.6 px     |  fall-thru|  16.64 px |
| Title letter-spacing  |  default   |  0.17 px   |  0.26 px     |  default  |  0.42 px  |
| Body max-width        |  640 px    |  560 px    |  480 px      |  700 px   |  —        |
| Colophon present      |  yes       |  yes       |  yes         |  yes      |  no       |
| Distinct child classes|  12        |  12        |  12          |  12       |  8        |

### What the metrics expose

Five observations that the audit treats as load-bearing.

**Obs-1. The chrome is uniform.** Every text-witness leaf has
the same parchment background, same 56/64 px padding, same
provenance-header structure, same verse-ref rendering, same
colophon, same child class count (12). The reader who opens
five different families opens *the same modal frame* five
times; only the body measure and title typography vary.

**Obs-2. Family identity collapses in viewer-active mode for
commentary.** The viewer-active CSS sets every `.folio-leaf-
title` to 1.4 em (22.4 px) at lower specificity. Linguistic
(1.08 em) and architecture (1.10 em) explicitly override
font-size and so retain their family-declared sizes. Commentary
sets only `font-weight: 400` and so inherits the viewer-active
1.4 em — meaning **commentary's title at viewer-active is
visually indistinguishable from a default/reception title** at
the same scale, except for the 400 weight (subtle at 22 px).
The 36 px hairline rule beneath the commentary title remains
the family's only robust differentiator in the full encounter.

**Obs-3. The leaf has no atmospheric edge.** `box-shadow: none`
on every leaf. The leaf is a sharp parchment rectangle laid
directly on the dark backdrop. This is partly what makes the
opened leaf read as "centered modal" rather than "folio
witness surfaced from the codex" — the leaf has no
illumination, no settling, no atmospheric integration with the
chamber it appears in.

**Obs-4. Provenance is identical across families.** The four-
line block (AUTH·KIND / tradition / source-basis / confidence)
appears on every text-witness leaf with the same typography
and same 22 px bottom margin. Family identity is currently
*denied* at the provenance level — the most readable rubric is
also the least family-specific.

**Obs-5. Citation treatment is identical across families.**
"Gen X:Y" renders as 14.4 px italic 0.82 opacity on every
family. This is appropriate for a citation, but it does not
yet vary by family — the linguistic citation could read as
lexicon-shorthand, the architecture citation could read as
site-attribution. Identical treatment is correct restraint
but leaves a small atmospheric opportunity on the table.

### Where the codex still feels software-like

Three concrete seams:

**Seam-1. The leaf reads as a centered card.** Sharp edges,
no atmospheric falloff, identical placement on every opening.
The constitution's chamber should hold the leaf as a folio that
*surfaced* from the codex — currently it presents as
*overlay onto* the codex.

**Seam-2. The provenance header reads as form metadata.** The
4-line scholarly attribution block at the top of every leaf is
correct in content but uniform in delivery. After ten opening
encounters in a session, the block becomes a "modal header
template" rather than a manuscript paragraph.

**Seam-3. Family identity is title-and-measure only.** The
commentary, linguistic, and architecture families differ in
title typography and body measure — but the structural rhythm
inside the leaf is otherwise the same. The reader who opens
five leaves of one family next to five of another family will
feel the difference; the reader who opens one of each in
isolation may not.

---

## Phase 2 — Commentary family constitution

### What commentary should feel like

A preserved interpretive folio leaf. Archival. Accumulated.
Restrained. Quietly authoritative.

The shape of a commentary record in the codex is:
3-5 paragraphs of prose, often citing earlier interpretive
traditions (Augustine, Philo, Aquinas, Barth, the patristic
tradition, the modern reception). The body is *thought*,
running paragraph by paragraph; the title is the
commentator's *position*; the citation is the verse the
commentator is *interpreting*.

### What the family currently has (post-v69)

- Title: italic 400 (lighter than the AO rubric voice).
- 36 px centred hairline rule beneath the title.
- Body: 640 px column, 0.92 em prose, 1.74 line-height.

This is sound. The family already reads as "argument flowing
in a column with a manuscript paragraph break above it."

### What should be added or refined

The Phase-1 audit identifies four small refinements that would
deepen the commentary register without redesigning it:

**Refinement 2-A. Explicit title font-size override.** Set
`.folio-leaf[data-kind="commentary"] .folio-leaf-title`'s
font-size to 1.18 em explicitly (matching the default at rest
state) so that viewer-active's 1.4 em jump no longer takes
effect. Commentary should *not* scale up to 22.4 px on
encounter; the lighter 400 weight reads cleanly at 1.18 em
(~18.88 px) and the family's restraint is preserved in viewer-
active.

**Refinement 2-B. Paragraph rhythm.** Prose paragraphs in
commentary records should have slightly more space between them
than the default. Currently each paragraph is a `<p>` with
default browser spacing. A small CSS rule
`.folio-leaf[data-kind="commentary"] .folio-body-vertical p`
with `margin-top: 1.1em` (vs default ~1em) gives the argument
slightly more breath between thoughts.

**Refinement 2-C. Drop-cap-quiet first paragraph.** A
manuscript folio's opening paragraph often distinguishes
itself. We do NOT add a literal drop-cap (modernist
imitation); we DO let the commentary's first paragraph carry
its first phrase in italic via the `::first-line` pseudo, OR
we add a small extra top-margin to the body's first paragraph
so the prose lands with a faint pause. The simpler move:
`first-paragraph margin-top: 6px` extra.

**Refinement 2-D. Ending cadence.** Currently the body ends
and the colophon follows. We add an `::after` to the
`.folio-body-vertical`'s last paragraph (or to the body
itself) — a small centred italic mark like `‡` or simply
extra bottom margin — to give the argument's close some
weight. A 32 px bottom margin on the body would let the
colophon arrive after a beat.

### Commentary's declared identity, post-Phase-2

```css
.folio-leaf[data-kind="commentary"] .folio-leaf-title {
  font-weight: 400;
  font-size: 1.18em;           /* explicit; resists viewer-active */
}
.folio-leaf[data-kind="commentary"] .folio-body-vertical {
  max-width: 640px;
  font-size: 0.92em;
  line-height: 1.74;
}
.folio-leaf[data-kind="commentary"] .folio-body-vertical p + p {
  margin-top: 1.1em;            /* paragraph rhythm */
}
.folio-leaf[data-kind="commentary"] .folio-body-vertical p:first-child {
  margin-top: 6px;              /* first-paragraph pause */
}
.folio-leaf[data-kind="commentary"] .folio-leaf-body {
  margin-bottom: 32px;           /* ending cadence */
}
```

---

## Phase 3 — Linguistic family constitution

### What linguistic should feel like

A surviving philological note tradition. Compact. Lexical.
Text-centered. Scholarly but restrained.

Less prose-heavy than commentary; more precise; more
textual. Each linguistic record names a single Hebrew or
Greek word and traces its grammar, recurrence, and reading
tradition. The body should feel like a gloss — a marginal
notation that exists *because of* the lexeme.

### What the family currently has (post-v69)

- Title: roman 500, 1.08 em, letter-spacing 0.01 em. The
  transliterated word reads as the lexeme being studied.
- Body: 560 px column, 0.88 em, 1.66 line-height.
- No rule beneath the title.

This is sound. The family already reads as "gloss in a
narrower column with the word foregrounded."

### What should be refined

**Refinement 3-A. Title spacing tightness.** Currently
`margin-bottom: 22px` on the title. A philological gloss's
title sits closer to its body than a commentary's argument
does — the word and its explanation belong together. Reduce
the linguistic title's `margin-bottom` to 16 px so the gloss
text sits nearer to its lexeme.

**Refinement 3-B. Even-tighter paragraph rhythm.** Linguistic
prose should be denser than commentary. Add `p + p { margin-
top: 0.85em; }` — tighter than commentary's 1.1em.

**Refinement 3-C. Lead Hebrew/Greek in body.** Many linguistic
records' bodies already begin with the original word in
Hebrew script. We do NOT add chrome around it. We DO ensure
the first paragraph's lang-attribute is honoured if present
(already works); CSS adds no special treatment beyond the
overall denser register.

**Refinement 3-D. Citation as lexicon-shorthand.** The
"Gen X:Y" citation could read as a smaller lexicon-mark in
linguistic family — italic 0.76em (vs the default 0.85em).
This honours the gloss tradition where citations are
abbreviations in the margin, not headlines.

### Linguistic's declared identity, post-Phase-3

```css
.folio-leaf[data-kind="linguistic"] .folio-leaf-title {
  font-style: normal;
  font-weight: 500;
  font-size: 1.08em;
  letter-spacing: 0.01em;
  margin-bottom: 16px;          /* tighter to the gloss body */
}
.folio-leaf[data-kind="linguistic"] .folio-leaf-verse {
  font-size: 0.76em;            /* lexicon-shorthand citation */
}
.folio-leaf[data-kind="linguistic"] .folio-body-vertical {
  max-width: 560px;
  font-size: 0.88em;
  line-height: 1.66;
}
.folio-leaf[data-kind="linguistic"] .folio-body-vertical p + p {
  margin-top: 0.85em;           /* denser philological rhythm */
}
```

---

## Phase 4 — Architecture / sacred-site family constitution

### What architecture should feel like

Inscriptional. Locational. Sacred-geographic. Land-memory.
Quiet permanence. A surviving site-memory fragment.

Each architecture record names a place — an altar, a well, a
pillar, a cave, a mountain — and traces its founding moment
and its recurrences across the patriarchal narrative. The
record's body is typically 2-3 paragraphs ending in a sealing
line ("The first stone in the patriarchal landscape." /
"Sacred geography by burial." / "The land remembers.").

### What the family currently has (post-v69)

- Title: italic 500, 1.10 em, letter-spacing 0.015 em.
- Body: 480 px column, 0.90 em, 1.60 line-height.
- No rule beneath the title.

This is sound. The family already reads as "stone-inscription
in the narrowest column with letter-spread title."

### What should be refined

**Refinement 4-A. Title small-caps register.** Inscriptions
are historically carved in capitals. We do NOT do all-caps
(too loud) but we DO add `font-variant-caps: small-caps` to
the architecture title so the title carries a quiet
inscriptional voice without becoming a heading. The site's
name in small-caps reads as a place-attribution.

**Refinement 4-B. Sealing-line typography.** The architecture
record's body almost always ends with a one-line "sealing"
statement. We can detect this via `.folio-body-vertical p:
last-child` and give it `text-align: center; font-style:
italic; opacity: 0.78` — the inscription's closing chisel
mark. This is the manuscript-trade equivalent of a date or
mason's mark at the end of an inscription.

**Refinement 4-C. Tighter vertical rhythm.** Inscriptions are
held, not breathy. Architecture's line-height (1.60) is
already tighter than commentary's. Add tighter paragraph
spacing: `p + p { margin-top: 0.9em; }` — between linguistic
(0.85) and commentary (1.1).

**Refinement 4-D. Citation as site-attribution.** The
"Gen 12:7" citation in architecture family could read with
slightly stronger letter-spacing — matching the title's
inscriptional letter-spacing of 0.015 em — so the citation
reads as a stone-engraved attribution rather than as a
breadcrumb.

### Architecture's declared identity, post-Phase-4

```css
.folio-leaf[data-kind="architecture"] .folio-leaf-title {
  font-size: 1.10em;
  letter-spacing: 0.015em;
  margin-bottom: 24px;
  font-variant-caps: small-caps; /* inscriptional voice */
}
.folio-leaf[data-kind="architecture"] .folio-leaf-verse {
  letter-spacing: 0.04em;        /* engraved attribution */
}
.folio-leaf[data-kind="architecture"] .folio-body-vertical {
  max-width: 480px;
  font-size: 0.90em;
  line-height: 1.60;
}
.folio-leaf[data-kind="architecture"] .folio-body-vertical p + p {
  margin-top: 0.9em;
}
.folio-leaf[data-kind="architecture"] .folio-body-vertical p:last-child {
  text-align: center;
  font-style: italic;
  opacity: 0.78;
  margin-top: 1.4em;             /* sealing-line breath */
}
```

---

## Phase 5 — Doré preservation analysis

### Why Doré already works

Doré is the calibration mark. The audit asks not how to change
it but why it succeeds. Five observations.

**Why-1. The plate IS the object.** The Doré chamber has no
paper leaf around the engraving. No 56/64 px padding. No
provenance header. The engraving sits directly on the dark
backdrop, framed only by its thin warm mat. The plate
announces itself as a different *kind* of object before any
typographic detail registers.

**Why-2. Curatorial chrome is restrained to a single plaque
beneath.** Title, verse, provenance (artist · year · source),
authority — all in one compact museum plaque under the
engraving. Four lines maximum. Centered. No header, no
footer.

**Why-3. The dark backdrop becomes part of the family.** Other
families render on cream parchment over the dark backdrop;
Doré has no parchment. The dark is the gallery wall. The
plate's white-on-black contrast carries the family's
identity at a glance — no need for any other family-signal.

**Why-4. Title sits BENEATH the engraving, not above.** The
plate-name does not introduce the image; it labels the image.
This is the museum-plaque cadence, not the article-headline
cadence. The reader sees the engraving first, then reads what
it is.

**Why-5. No animation, no transition. The plate is just
present.** The leaf-settle animation that other families use
(0.5s down-fade-in) does not call attention to the plate's
arrival. The reader who summons a plate encounters it as
something *already there*, lifted into focus.

### What other families can learn from Doré

Doré's principles can be stated as five constitutional
moves; each other family applies them at its own register.

1. **The kind announces itself before any detail.** Plate's
   dark backdrop is its kind-signal. For text witnesses, the
   chrome (provenance header, measure, title typography) must
   together carry the kind-signal at a glance.
2. **Curatorial chrome is held in ONE place, not stacked.**
   Plate has one plaque; text witnesses currently have a
   provenance header AND a verse-ref AND a colophon — three
   stations of curatorial metadata. The audit does not propose
   removing any of them; it does propose that they should
   feel like *one rhythm*, not three separate UI cards.
3. **The object is encountered, not navigated.** Plate has no
   navigation affordance — no "next plate" link, no breadcrumb.
   Text witnesses also avoid this correctly (no in-leaf
   navigation). Preserve.
4. **Authority is whispered, not announced.** Plate's
   authority class is a tiny small-caps line in the plaque
   ("TERTIARY · PLATE"). Text witnesses do the same in their
   provenance ("TERTIARY · COMMENTARY"). Preserve.
5. **The leaf carries weight, not ornament.** Plate has no
   border, no shadow, no decorative flourish. The engraving's
   own visual gravity is enough. Text witnesses likewise
   avoid ornament — but the *atmospheric* element that
   replaces the engraving's gravity in text witnesses is the
   parchment-on-dark contrast. Phase 6 addresses this.

Doré does not change. It is the standard.

---

## Phase 6 — Modal → leaf transition

### The residual modal energy

Five sampled text-witness leaves all share:

- Identical centered placement on the dark backdrop.
- Identical 0.5s downward-fade-in settle animation.
- Identical sharp parchment edges with no atmospheric falloff.
- `box-shadow: none` — no weight, no depth, no integration.

The leaf reads as a *card laid over* the chamber rather than
as a *folio surfaced from* the chamber. The reader's eye
registers "popup" before it registers "manuscript."

### What manuscript folio feel requires

Three constitutional moves, none of which require new
chrome, animation, or layout.

**Move 6-A. Ambient parchment illumination.** Add a faint
warm outer halo to the leaf — a very large, very soft,
slightly warm box-shadow that reads as candlelight bouncing
off the parchment back into the dark space. This is the
opposite of a "card shadow" (sharp, near, gray); it is
manuscriptal ambient light (broad, distant, warm).

Concrete value: `box-shadow: 0 0 120px 24px rgba(245, 220,
170, 0.04);` — a 120 px blur, 24 px spread, very low alpha,
warm tone. Almost invisible per se; perceived as the leaf
"belonging in the room."

**Move 6-B. Soft top-edge fade.** The top edge of the leaf
currently cuts sharply against the dark backdrop. A 12-16 px
gradient fade at the top (a `::before` element or a CSS
gradient mask) would soften the boundary slightly — as if
the parchment's top has been touched by candlelight and the
dark surrounds it gradually. NOT a faux torn-edge effect;
just a gentle dissolve.

This is risky to implement because masking can interact
oddly with the leaf's child elements. **Defer to Phase 7
implementation; if the masking causes any rendering bug,
abandon and stick with Move 6-A only.**

**Move 6-C. The leaf-settle animation eases longer.** The
current `folio-leaf-settle` is 0.5s ease-out. A slightly
longer settle (0.7s) with a gentler curve would let the leaf
*emerge* rather than *appear*. The transform-Y of 8 px is
adequate; the timing is the change.

### What this is NOT

Explicitly forbidden by the brief and reaffirmed here:

- No glassmorphism (frosted glass, backdrop-blur).
- No floating card aesthetics (multi-layer shadows, depth
  stacking, "lifted-from-surface" effects).
- No app-window framing (title-bar, close-X corner, etc.).
- No fake antiquity (parchment textures, fake torn edges,
  ink stains, fake aging filters).
- No depth or 3D effects.

The atmosphere remains: civilizational, quiet, material,
manuscriptal.

### Move 6 declared identity

```css
/* Move 6-A — ambient parchment illumination.
   A very large, very low-alpha, warm outer glow. The leaf
   reads as illuminated parchment rather than as a card on
   a dark surface. Almost subliminal; perceived as
   atmosphere, not as a shadow. */
.folio-leaf {
  box-shadow: 0 0 120px 24px rgba(245, 220, 170, 0.04);
}
.folio-leaf[data-kind="plate"] {
  /* Doré plates retain their own museum-chamber framing —
     no halo around the engraving. */
  box-shadow: none;
}

/* Move 6-C — longer settle.
   0.5s → 0.72s with a gentler ease. The leaf emerges
   rather than appearing. */
@keyframes folio-leaf-settle {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
.folio-leaf {
  animation: folio-leaf-settle 0.72s cubic-bezier(0.22, 0.61, 0.36, 1);
}
```

Move 6-B (soft top-edge fade) deferred to a future pass if
the simpler Move 6-A + 6-C combination does not sufficiently
soften the modal feeling.

---

## Phase 7 implementation footprint

A single CSS block per family plus the leaf-emergence
refinements. Total additions: ~35 lines of CSS. No JS. No new
metadata. No new HTML class names. No new selectors beyond
the existing `data-kind` attribute and the existing
`.folio-leaf` class.

Five constitutional moves ship:

1. **Commentary** — explicit title font-size + paragraph
   rhythm + ending cadence (Refinements 2-A through 2-D).
2. **Linguistic** — title margin tightening + paragraph
   density + lexicon-shorthand citation (Refinements 3-A
   through 3-D).
3. **Architecture** — small-caps title + sealing-line
   typography + engraved-attribution citation + tighter
   paragraph rhythm (Refinements 4-A through 4-D).
4. **Doré** — UNCHANGED. The standard remains.
5. **Leaf emergence** — ambient parchment glow + longer
   settle (Moves 6-A + 6-C).

Each family's distinct register deepens. The leaf no longer
reads as a modal popup. The codex carries four distinct
manuscript traditions plus the calibration plate, all inside
one civilizational volume.

---

## Phase 8 verification scope

The verification diag will:

1. Walk all five families and confirm computed-style metrics
   match the constitutional declarations above.
2. Confirm commentary title now reads 1.18 em in viewer-
   active (not 1.4 em).
3. Confirm architecture title font-variant is `small-caps`.
4. Confirm the leaf carries the ambient warm halo
   (`box-shadow` non-empty) and Doré remains shadow-less.
5. Confirm the leaf-settle animation duration is 720 ms.
6. No AO count change, no resonance count change, no Doré
   render change.
7. Screenshots: one of each family at viewer-active + chapter
   atmosphere captures (Gen 1, Gen 8, Gen 22) for no-
   regression.

---

## Posture

After this pass, each family will carry a recognizable
manuscript-tradition voice:

- **Commentary** — archival argument in a measured column,
  with rhythmic paragraph breath and a centred hairline mark.
- **Linguistic** — philological gloss in a tighter column,
  with the original word foregrounded and lexicon-style
  citation.
- **Architecture** — site-inscription in a small-caps voice,
  with paragraph density and a centred italic sealing line.
- **Doré** — monumental engraved plate, untouched.
- **All text leaves** — emerging from the codex with ambient
  parchment illumination, settling slowly.

The reader who walks Genesis after this pass will increasingly
recognize each family before reading content. The codex begins
to hold four (and eventually more) manuscript traditions as
its own residents.

The pass is small in CSS but large in atmosphere. The
constitution holds.
