# v58 — Folio Hierarchy Legibility (editorial note)

*A hierarchy-tuning pass. No new systems, no new objects.*

## What was wrong

Tertiary markers were reading as **disabled UI** rather than as
quiet manuscript glosses. Confirmed by computed-style readings on
the live page at `gen.1.1` (ARCHIVE depth):

| State                       | opacity | glyph color α | effective glyph α |
|-----------------------------|--------:|--------------:|------------------:|
| Tertiary resting   (before) | 0.60    | 0.68          | **0.41**          |
| Secondary resting  (before) | 0.78    | 0.82          | 0.64              |
| Tertiary hover     (before) | 0.95    | 1.00          | **0.95**          |

Two compounding problems:

1. **Tertiary resting at 0.41 effective alpha** was below the
   threshold at which a glyph reads as "intentionally light." It
   read as "this control is not available."
2. **The hover ramp from 0.41 → 0.95 was 2.3×** — a violent shift
   that produced the impression of *activating* a disabled
   control rather than *clarifying* a marginal note. The codex
   was implying its own tertiary objects were inert.

The secondary↔tertiary gap was 0.23 in effective glyph alpha — a
gap that pushed tertiary past the perceptual cliff between
"quieter" and "broken." Hierarchy was present but
mis-communicated.

## What changed

Six manuscriptal levers were nudged. No new properties, no
modern colour additions, no glow, no badges.

| State                       | opacity | glyph color α | effective glyph α |
|-----------------------------|--------:|--------------:|------------------:|
| Tertiary resting    (after) | 0.82    | 0.86          | **0.71**          |
| Secondary resting   (after) | 0.88    | 0.94          | 0.83              |
| Tertiary hover      (after) | 1.00    | 1.00          | **1.00**          |

The full lever set:

- **Tertiary resting opacity** 0.60 → 0.82 (no longer reads as
  inactive).
- **Tertiary glyph color α** 0.68 → 0.86 (ink is now legible at
  reading distance, not strained).
- **Tertiary background α** 0.05 → 0.10 (parchment is perceptible
  rather than invisible).
- **Tertiary border α** 0.42 → 0.56 (dotted pattern is now
  discernible; the dotted-vs-dashed distinction reads at a
  glance).
- **Tertiary hover** now adds an *explicit color override*
  rather than only lifting opacity. Hover **clarifies** the gloss
  rather than rescuing it from oblivion.
- **Secondary resting** sharpened in parallel — opacity 0.78 →
  0.88, ink alpha 0.82 → 0.94, border alpha 0.60 → 0.70 — so the
  secondary↔tertiary step remains a felt step in the same
  direction as before, with both tiers more confident.

Dependent rules (visited, echo, originating) were rebased so the
relative deltas remain stable. Specifically `echo+tertiary` rose
from 0.54 to 0.70 (still quieter than originating-tertiary at
0.82), and `visited+tertiary` rose from 0.78 to 0.92 (the slight
recovery of presence after encounter).

## Why this preserves restraint

The codex is now **more legible**, not louder. Effective glyph
alpha gradient:

```
primary:    ≈ 0.96     authoritative canonical encounter
secondary:  ≈ 0.83     substantial supporting witness
tertiary:   ≈ 0.71     quiet scholarly gloss
```

A clean ~0.12 step between each tier — felt as a gradient, not as
a cliff. The hover ramp is now 1.42× rather than 2.3×: gentle
clarification, not rescue. Tertiary remains quieter than
secondary; secondary remains quieter than primary. Hierarchy is
now subconsciously readable within two or three seconds at
peripheral vision, and no tier is mistakable for inactive UI.

The dotted-vs-dashed-vs-solid border distinction continues to
carry the strongest typographic signal of authority. The
opacity / ink / parchment refinements only stop tertiary from
falling off the perceptual cliff into "disabled."

## Screenshots

Captured at `reports/v58_before_*.png` and `reports/v58_after_*.png`:

- `gen1_dense.png` — Genesis 1 cluster at ARCHIVE depth (the
  densest stack in the canon).
- `tertiary_hover.png` — a tertiary marker resting + hovered.
- `mixed_stack.png` — same cluster with two markers temporarily
  promoted to `secondary` to show the mixed-tier rhythm.
- `secondary_hover.png` — a secondary marker resting + hovered.

The before/after pair is the single clearest visual reading of
this refinement.

## Scope and discipline

This pass:

- Did not add any new Atlas Object, chamber, resonance pair, or
  metadata.
- Did not introduce any new CSS property; only adjusted alpha
  and added explicit `color` to two hover rules.
- Did not change JS behaviour.
- Did not touch the depth-filter logic (CORE / STUDY / ARCHIVE).
- Did not modify the `_ATLAS_KIND_GLYPHS` map or any marker
  glyph.

The codex was already architecturally mature. This pass tuned
its typographic register so that the architecture is legible at
a glance.
