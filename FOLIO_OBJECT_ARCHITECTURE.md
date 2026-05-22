# Folio Object Architecture

*Compiled 2026-05-22, v77. The Manuscript Architecture pass.
Companion to `LEAF_MATERIAL_INDEPENDENCE_AUDIT.md`,
`OBJECT_FAMILY_CONSTITUTION.md`, and the leaf-constitution arc.*

---

## Why the prior atmospheric work didn't separate the leaf

v75 and v76 corrected the leaf's surface (warm halo → dark
attenuation; warm cream → dry vellum). The leaf became
materially distinct in color and shadow logic. But the reader
still perceived the leaf and the reading-room parchment as
the *same manuscript state*:

- Same paper species (both warm cream within a few HSL points)
- Same tonal field (both in the same warm-light family)
- Same spatial rhythm (modal-rapid-deliver headers, even
  paragraph distribution, snug colophon)
- Same codex layer (a centered rectangle stacked over the room)

The opened object continued to read as "a rectangular
continuation of the page" rather than "an extracted archival
leaf brought forward from the chamber." Atmospheric correction
had reached its limit. The remaining work is architectural.

---

## The architectural shift

A leaf is not a modal. A leaf is a *prepared sheet*. Prepared
sheets carry generous archival margins — top entrance silence,
lateral text-block boundaries, bottom closure descent. They
arrive with ceremonial staging and depart with quiet weight.

Modals optimize for content delivery. Leaves optimize for
preservation and presentation. The reader of a modal expects
fast-served information; the reader of a leaf expects to be
admitted into a curated state.

This pass formalizes that distinction by restructuring the
leaf's proportions:

| Region                    | Was      | Now     | Effect                              |
|---------------------------|---------:|--------:|-------------------------------------|
| Leaf top padding          |  56 px   |  88 px  | Ceremonial entrance silence         |
| Leaf bottom padding       |  56 px   | 104 px  | Footer closure descent              |
| Leaf lateral padding      |  64 px   |  64 px  | Unchanged (preserves body widths)   |
| Provenance margin-bottom  |  22 px   |  32 px  | Header → verse/title staging breath |
| Verse-ref margin-bottom   |   6 px   |  14 px  | Citation → title ceremonial pause   |
| Colophon margin-top       |  56 px   |  80 px  | Codex closure descent               |

Total entry region (top-edge → first body line): ≈ 90 px more
silence than v76. Total exit region (last body line → bottom
edge): ≈ 70 px more silence than v76. The leaf is now taller
and more spacious in its compositional gravity.

---

## Scope: text-witness leaves only

The padding change is scoped via:

```css
.folio-leaf:not([class*="-chamber"]):not([data-kind="plate"]) {
  padding: 88px 64px 104px;
}
```

The `:not([class*="-chamber"])` exclusion preserves all twelve
AO chambers (cosmology, sanctuary, lament, etc.) — each
chamber carries its own bespoke compositional architecture and
must not have its outer padding reshaped.

The `:not([data-kind="plate"])` exclusion preserves Doré, whose
explicit `padding: 0` already overrides but is kept defensively.

The provenance, verse, and colophon margin changes are applied
universally because those elements only appear on text-witness
leaves; chambers use their own bespoke headers and footers.

---

## What the reader will feel (without thinking)

A reader summoning a text witness will now experience the
opening as a SEQUENCE rather than a packet:

1. **Ceremonial entrance** — the leaf's top edge holds 88 px
   of preserved silence before the provenance header arrives.
   The reader's eye crosses an archival margin to reach the
   first rubric.
2. **Header staging** — the four-line provenance block sits
   with deeper breath beneath it (32 px) than v76's 22 px.
   The header completes; the reading proper has not yet
   begun.
3. **Citation pause** — the verse-ref carries a 14 px
   ceremonial pause to its title. The citation reads as
   attribution, not breadcrumb.
4. **Title and body** — these arrive at their family-specific
   rhythms (commentary's hairline rule, linguistic's lexeme,
   architecture's small-caps, etc.).
5. **Body settles into argument/gloss/inscription/etc.** at
   the family's measured cadence.
6. **Footer descent** — when the body ends, the colophon
   drops through 80 px of quiet space; below that, 104 px of
   leaf bottom padding closes the leaf. The reader does not
   exit abruptly.

The opening reads as preserved manuscript pacing, not as
modal-content-delivery.

---

## Compositional region budget (after this pass)

For a representative commentary leaf:

```
┌─────────────────────────────────────────────┐
│                                              │ ← 88 px top padding
│         (preserved entrance silence)         │
│                                              │
├──────────────────────────────────────────────┤
│ TERTIARY · COMMENTARY                        │
│ tradition line                               │ ← 4-line provenance block
│ source basis line                            │
│ confidence line                              │
│ ─────────                                    │ ← provenance border
│                                              │
│         (32 px staging breath)               │
│                                              │
│ Gen 1:1                                      │ ← verse-ref
│                                              │
│         (14 px ceremonial pause)             │
│                                              │
│ Augustine — Confessions XI / City of God XI  │ ← title (1.18 em italic)
│              ───                             │ ← 36 px hairline rule
│                                              │
│ [body paragraphs at 640 px / 0.92 em /       │
│  line-height 1.74, paragraph spacers 0.85em] │
│                                              │
│         (body closes)                        │
│                                              │
│         (80 px colophon descent)             │
│                                              │
│         Genesis 1                            │ ← colophon
│                                              │
│         (104 px footer closure padding)      │
│                                              │
└─────────────────────────────────────────────┘
```

Entry region (top edge → first body line): ≈ 230-270 px
Reading region: variable by content length
Exit region (body close → bottom edge): ≈ 200 px

The proportions read as *archival* rather than *modal*.

---

## What this pass does NOT do

- **No borders.** Not on the leaf, not on the provenance.
- **No card UI.** Padding is internal silence, not card padding.
- **No shadows added.** The v76 dark-absorption stack remains.
- **No new chrome.** No badges, chips, frames, or decorative
  ornaments.
- **No new typography.** Family fonts, weights, sizes
  unchanged.
- **No animation changes.** The 0.72 s leaf-settle remains.
- **No color changes.** Vellum (#ede3cc) + warm ink (#2e2418)
  remain stable.
- **No content edits.** All records render as-is.
- **No max-width change.** Leaf stays at 800 px outer; body
  measures preserved for all families.

The only change is proportional vertical spacing within the
leaf's four key compositional regions.

---

## Doré preservation

Doré's `padding: 0` and `box-shadow: none` are preserved.
Plates render exactly as before:
- The dark museum chamber as frame.
- The engraving directly on the chamber backdrop.
- The compact plaque beneath.
- No ceremonial padding because the plate IS the ceremonial
  moment.

The architectural shift is for *text* witnesses — the
silences only have meaning around words. Doré's silence is
around the engraving.

---

## AO chamber preservation

Twelve chamber renderers carry their own bespoke compositional
architecture (concentric enclosures, layer stacks, return
pairs, descent registers, etc.). The new padding rule
explicitly excludes them via `:not([class*="-chamber"])`. Each
chamber renders exactly as before:

- Cosmology chamber: vocabulary tables + comparative + diagram.
- Sanctuary chamber: five concentric enclosures.
- Lament chamber: dotted axis + cries.
- Resurrection chamber: rupture-then-return pairs.
- ...and the other eight.

The chambers are already their own compositional events.
Their compositional dignity does not need leaf-level
ceremonial padding — it carries its own.

---

## Posture

The leaf is no longer a modal-stacked rectangular continuation
of the reading-room page. It is a preserved manuscript object
with its own compositional pacing: ceremonial entry → header
staging → citation pause → title threshold → body cadence →
codex closure.

The reader who opens a witness now enters *a chamber within
the chamber* — a prepared archival sheet brought forward from
the reading-room field. The transition feels architectural
rather than modal-overlay.

The change is invisible per detail. The change is felt as
inevitability.
