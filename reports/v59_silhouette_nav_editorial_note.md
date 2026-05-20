# v59 — Silhouette / weight separation + navigation coherence

*A perceptual-clarity refinement pass. No new systems, no new
objects.*

## Why opacity was no longer the right lever

v58 brought tertiary opacity up to a legible band so the
"disabled UI" reading dissolved. But the hierarchy still
collapsed at peripheral vision because **opacity does not change
silhouette mass**. Two markers of equal size, equal glyph,
equal border weight register as the same shape to the eye
regardless of how their alpha differs. The dotted-vs-dashed
border distinction works at reading distance but fails at the
glance distance the rail is read at while the eye is moving
across scripture.

Verified by computed-style readings at `gen.1.1` (ARCHIVE depth)
after v58:

| Measure       | Secondary (before v59) | Tertiary (before v59) |
|---------------|-----------------------:|----------------------:|
| Box           | 28 × 28 px             | 28 × 28 px            |
| Glyph         | 15 px                  | 15 px                 |
| Border weight | 1 px                   | 1 px                  |

The silhouettes were identical. Hierarchy was carried entirely by
ink alpha and border *style*. At rail-skim distance, those
signals dropped below the perception floor.

## What changed — silhouette levers

Six existing properties were rebased so the three tiers carry
materially different silhouette mass, not different alpha.

| Lever          | Primary       | Secondary     | Tertiary      |
|----------------|--------------:|--------------:|--------------:|
| Box            | 28 × 28       | 28 × 28       | **26 × 26**   |
| Glyph          | **16 px**     | 15 px         | **13 px**     |
| Border weight  | **1.5 px**    | **1.5 px**    | 1 px          |
| Border pattern | solid         | dashed        | dotted        |
| Parchment hue  | warm orange   | warm gold     | **cool grey** |
| Parchment α    | 0.30          | 0.18          | 0.08          |

The silhouette step is now read in three independent signals
simultaneously:

1. **Size delta** — tertiary is 26×26, 7% smaller box. The mass
   step is visible at peripheral vision.
2. **Glyph delta** — tertiary glyph is 13px vs 15-16px. The
   typographic mark is distinctly smaller.
3. **Border-weight delta** — primary and secondary share a 1.5px
   confident stroke; tertiary is held at 1px. The two heavier
   tiers feel anchored; the tertiary feels written in pencil.

Plus the existing solid / dashed / dotted distinction (now
reinforced by weight) and the cooler-grey tertiary parchment
(less red, more grey — the "dry paper" register rather than the
"inked parchment" register of secondary and primary).

## Cluster breathing

The dense Genesis 1 rail was also collapsing because the
collision-gap between successive marker clusters was identical
regardless of cluster content. A tertiary-only cluster pressed
hard against an adjacent secondary cluster, and the eye read
them as one row of competing items.

A single JS tunable in `_positionFolioEntries` now distinguishes:

```
COLLISION_GAP        = 14 px   (default, between any two clusters)
TERTIARY_ONLY_GAP    = 24 px   (when the placed cluster is
                                 tier-tertiary across the board)
```

Tertiary-only clusters now sit with extra vertical breath above
them. They read as marginal glosses orbiting the verse, not as
competing items in the row above.

## Navigation coherence

Independent issue, surfaced in the same pass: the "← Bible
Versions" button on the Bible cover was skipping the conceptual
parent. It read its own label correctly but routed to
`browseTradition('Religion', 'Christian')` — two steps up the
hierarchy, dropping the reader into the whole Christian corpus
(109 tiles, only one of which was the Bible).

The Bible-Versions translation picker already existed as
`browseText(cat, trd, 'bible')` — a clean 52-tile grid of every
translation variant — but no route currently reached it from
above. The cover back-button now routes there when the text has
multiple translations, and falls back to the tradition listing
only for single-translation texts.

Verified by the after-state landing:

```
BEFORE:  Home › Religion › Christian       (109 mixed tiles)
AFTER:   Home › Religion › Christian › Bible  (52 translation tiles)
```

Spatial coherence is restored: the codex now walks one step at a
time up its own hierarchy. The reader knows where they are
without thinking.

## How the hierarchy now reads subconsciously

A skim across the rail at peripheral vision now resolves the
three tiers in three independent perceptual signals:

```
PRIMARY       large solid heavy mark    canonical encounter
SECONDARY     large dashed heavy mark   substantial witness
TERTIARY      small dotted light mark   quiet marginal gloss
```

The tertiary marker is no longer "a weaker secondary." It is a
different shape — smaller, lighter, in cooler parchment, written
with a thinner border. The eye groups it with marginalia, not
with the witness layer.

Restraint is preserved. The tertiary layer is still quieter than
secondary. Nothing glows; no new colour is introduced; no badges;
no modern UI affordance. The codex remains manuscriptal.

## Scope and discipline

This pass:

- Did not add any Atlas Object, chamber, resonance pair, or
  metadata.
- Did not introduce any new CSS property — only adjusted
  existing width, height, font-size, border-width, background,
  and one JS tunable for cluster spacing.
- Did not change the depth-filter logic.
- Touched two JS sites: cluster positioning (one numeric branch)
  and the cover back-button routing (one conditional).

The codex was already architecturally mature. v58 fixed the
"disabled UI" reading at hover distance. v59 fixes it at
peripheral vision distance, and restores spatial coherence to
the navigation back-stack.
