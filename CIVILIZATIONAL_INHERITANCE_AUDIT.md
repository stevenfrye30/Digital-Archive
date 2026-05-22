# Civilizational Inheritance Audit

*Compiled 2026-05-22, v81. The first inheritance-layer pass.
Companion to `WITNESS_TEMPORALITY_AUDIT.md` and the
constitutional documents above it.*

After v80's transmission rubrics, each witness declared its
mode of historical passage. But witnesses still felt
*adjacent* rather than *genealogically entangled*. Cosmology
in particular remained the least mature major family —
essay prose about an ancient world-picture rather than a
manuscript cosmogram.

This pass addresses two specific moves. Phase 6 (cosmology
constitution — the brief's explicit highest priority) and
Phase 3 (cross-reference echo register).

---

## Move 1 — Cosmology cosmogram (Phase 6, highest priority)

The user's brief was specific:

> Cosmology remains the least mature major family.
> It still behaves too much like essay prose about
> ancient cosmology.
>
> Begin exploring:
> - conceptual architecture
> - symbolic spatiality
> - world-model composition
> - manuscript cosmogram logic
> - inherited explanatory systems

Two changes:

### A. Editorial restructuring of `gen1-cosmology-ane`

The body was a single paragraph describing the three-tier
cosmos. It has been rewritten as a manuscript-cosmogram-style
descent, one stratum per paragraph:

```
The cosmos presupposed by Genesis 1 is the inherited
Ancient Near Eastern model. The Hebrew text neither argues
for it nor invents it — it receives the picture from the
broader regional imagination (cf. Babylonian Enuma Elish)
and bends it toward Israel's singular God.

The picture descends in clear strata:

Above the firmament — the upper cosmic waters, held back.

The firmament (rāqîaʿ) — a solid sky-vault, hammered out,
separating the waters above from those below.

The earth-disc — a flat plain resting on pillars.

Below the earth — Sheol, the abyss (tehôm), the deep.

The cosmography is older than the text. Genesis 1 inherits
the layered world and rewrites it under a single creating
word.
```

The reader's eye reads down the page through the cosmic
levels. Each stratum is its own paragraph; the em-dash sets
off the layer-name from its content. The body becomes a
written cosmogram.

### B. CSS — spacer pushed to 1.2 em

The cosmology family's paragraph-spacer height moves from
0.75 em to 1.2 em — a ≈ 60 % increase. Each cosmographic
stratum breathes with cosmic distance from the next.

```css
.folio-leaf[data-kind="cosmology"]:not(.cosmology-chamber)
  .folio-body-vertical .folio-body-spacer {
  height: 1.2em;   /* was 0.75em */
}
```

Effective px: 1.2 em × 14.56 px body font ≈ 17.5 px per
inter-stratum spacer. Visibly cosmic; clearly distinct from
commentary's 12.5 px and linguistic's 7 px.

The `light-before-luminaries` record (which was already
nicely-stratified across three interpretive traditions —
Rabbinic, Patristic, Modern critical) inherits the wider
spacer automatically. Its three reading traditions now read
as three separate strata of interpretation rather than a
continuous essay.

The cosmology-chamber (AO·001 firmament) is excluded via
the existing `:not(.cosmology-chamber)` selector. Its
bespoke compositional architecture is untouched.

---

## Move 2 — Cross-reference echo register (Phase 3)

The user's brief:

> Cross-reference objects are currently too informational.
> They should become: echo structures.
> The reader should feel: scripture reverberating through
> scripture. Not: verse links.

The cross-reference record (NT echoes of Genesis 1:1) was
already nicely list-shaped — three NT passages each in its
own block. What was missing was the *visual implication of
echo*.

A single CSS addition:

```css
.folio-leaf[data-kind="cross-reference"] .folio-body-vertical {
  border-left: 1px dotted rgba(120, 80, 40, 0.22);
  padding-left: 18px;
}
```

A faint dotted hairline runs the left edge of the body — the
canonical-resonance axis. Each echoed passage (John 1:1,
Hebrews 11:3, Colossians 1:15-17) hangs off the axis like a
marginal note from a vertical column. The leaf reads as
*resonance* rather than as a flat list.

The dotted style was chosen deliberately — solid would feel
structural; dotted feels *echoing*. The 22 % alpha keeps the
hairline almost subliminal.

---

## What this pass does NOT do

Per the brief, explicitly:

- **No knowledge graphs** — no node/edge UI, no relationship
  visualizations.
- **No relation sidebars** — the inheritance is felt in the
  body's own typography, not in chrome.
- **No "related content" UI** — no recommendation lists, no
  hover-related panels.
- **No ontology exposure** — the family system stays
  invisible to the reader; only its atmospheric
  consequences are felt.
- **No wiki-link systems** — the cross-reference body
  references passages but does not link them as
  clickable jumps.

The codex remains:
- quiet
- ritual
- archival
- civilizational
- inevitable

---

## What this pass leaves for the next

The brief named seven phases. This pass addresses two
(cosmology constitution + cross-reference echo). Five
phases are partially addressed or deferred:

- **Phase 1 (Inheritance Pathways)** — the cosmology
  restructure articulates one inheritance pathway (ANE
  cosmography → Genesis 1's reauthoring); cross-reference
  hairline articulates another (canonical resonance).
  Further pathway work is deferred — Genesis → prophetic
  reinterpretation, Akedah → Abrahamic reception, etc. —
  each would require editorial work on the affected
  records.
- **Phase 2 (Witness Descent)** — implicit via the existing
  family registers (manuscript near-source, commentary
  downstream, ritual living, Doré late-monumental, etc.).
  No new explicit move this pass.
- **Phase 4 (Commentary Genealogy)** — addressed implicitly
  by v80's transmission rubric ("inherited through
  interpretation") and by the existing commentary family
  CSS (640 px column, hairline rule, paragraph rhythm).
  Further work — explicit chains of interpretive
  inheritance — reserved.
- **Phase 5 (Ritual Continuity)** — addressed by v80's
  "carried through generations" rubric and the existing
  ritual family CSS. The distinction between preserved
  text (manuscript) and living transmission (ritual) is
  carried by the contrasting rubrics + spacers + family
  registers.
- **Phase 7 (The Archive as Memory System)** — emergent
  property; each individual pass contributes to the gestalt.
  The codex now layers v77 ceremony + v78 choreography +
  v79 canonical stratum + v80 transmission rubric +
  v81 cosmogram/echo. Together they produce the recursive-
  remembering atmosphere.

---

## What the reader now feels

After v81:

- Opening a cosmology witness, the reader reads down through
  the world: "Above the firmament... The firmament... The
  earth-disc... Below the earth..." The cosmos descends on
  the page in clear strata. The body IS the cosmogram, not
  an essay about one.
- Opening a cross-reference, the reader sees scripture
  echoing through scripture along a dotted vertical axis.
  John 1:1, Hebrews 11:3, Colossians 1:15-17 hang off the
  axis. The reader feels resonance rather than a list of
  links.
- All prior layers continue to work: canonical stratum
  ("Torah · Primeval History"), transmission rubrics
  ("inherited through interpretation"), leaf ceremony,
  reading choreography, codex memory.

The codex begins to feel less like a collection of texts and
more like a civilization recursively transmitting itself
through preserved witnesses — cosmology layered as
cosmogram, cross-reference structured as resonance, each
family carrying its mode of historical passage.
