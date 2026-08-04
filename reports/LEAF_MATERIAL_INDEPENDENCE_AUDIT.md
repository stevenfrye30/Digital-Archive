# Leaf Material Independence Audit

*Compiled 2026-05-22. Atmospheric/material refinement pass.
Addresses the residual continuity between manuscript surface
and reading-room chamber that v75's shadow + halo pass did not
resolve. Companion to `OBJECT_FAMILY_CONSTITUTION.md` and the
prior leaf-constitution documents.*

---

## Why v75 didn't separate the leaf from the room

The v75 pass added a two-layer shadow stack to `.folio-leaf`:

```css
box-shadow:
  0 8px 36px -10px rgba(20, 14, 8, 0.40),    /* weight beneath */
  0 0 140px 36px  rgba(245, 220, 170, 0.07); /* ambient halo */
```

The change passed the diag (parchment stable across themes,
weight present, halo present) — but visually the manuscript
still belonged to the same atmospheric layer as the chamber.

The reason, when read carefully: **the ambient halo was warm
cream.** It extended warm light *outward from the leaf into
the chamber*. The chamber backdrop is already a warm radial
vignette (`rgb(32, 24, 16)` warm-brown core fading to near-
black at the edges). The leaf's parchment is `#F3E8C8` warm
cream. The leaf's halo was `rgba(245, 220, 170, 0.07)` warm
yellow-cream.

Three warm surfaces in the same hue family, bleeding into one
another. The reader's eye registers a single tonal field —
"warm fog + warm paper" — not two distinct materials.

**The halo was painting warm fog into the chamber.**

---

## What the manuscript and chamber should actually be

Per the brief, the hierarchy:

| Surface | Should feel | Should NOT feel |
|---|---|---|
| Chamber background | atmospheric / infinite / smoky | warm fog continuing onto the leaf |
| Manuscript leaf | dry / stable / archival / tangible | warm tinted continuation of the room |

The fix is not "more glow" or "stronger shadow." The fix is
to make the immediate area around the leaf *quieter and
darker* (chamber attenuates near the manuscript), and to shift
the parchment slightly away from warm yellow toward dry
vellum.

The leaf should read as the ONLY brightly-preserved zone in a
pocket of quietened chamber. Internal luminosity comes from
contrast with surround, not from external glow.

---

## The refinement (three small moves)

### Move A — Replace warm halo with dark absorption

The new shadow stack inverts the prior halo's logic:

```css
box-shadow:
  /* Quiet weight beneath. Dark warm-neutral, narrow spread —
     gives the leaf perceptible physical mass without reading
     as a card shadow. */
  0 6px 28px -8px rgba(0, 0, 0, 0.55),
  /* Chamber attenuation. A dark absorption around the
     manuscript perimeter. The chamber's warm fog quietens
     here; the leaf reads as protected from the surrounding
     atmosphere rather than fused with it. The shadow is
     dark (not warm), so it does NOT paint warm light into
     the chamber. */
  0 0 100px 16px rgba(0, 0, 0, 0.42);
```

Both shadows are now dark, not warm. The chamber backdrop
remains its warm vignette overall, but the immediate area
around the leaf becomes a quieter darker pocket. The leaf is
no longer a warm-cream surface emitting warm light into a
warm-fog chamber — it is a stable parchment surrounded by
absorption.

This is the chamber attenuation the brief named, achieved
through the leaf's own shadow rather than by editing the
chamber gradient.

### Move B — Vellum shift on the parchment

```css
--reader-bg: #ede3cc;   /* was #f3e8c8 */
```

- Old: HSL(46°, 64%, 87%) — warm yellow-cream, saturated.
- New: HSL(40°, 41%, 86%) — dry vellum / bone, less yellow-
  saturated, retains warmth.

The shift is subtle by design:

```
#F3E8C8   →   #EDE3CC
R 243     →   R 237  (−6)
G 232     →   G 227  (−5)
B 200     →   B 204  (+4)
```

The B channel actually *rises* by 4 while R and G drop, which
slightly cools the parchment toward dry vellum without making
it neutral or cool. The warmth remains but the yellow heat
attenuates. Side by side, the eye reads it as a vellum sheet
rather than warm cream paper.

The brief was explicit:
- Preserve manuscript warmth ✓ (still in the warm family)
- Avoid yellow saturation ✓ (saturation drops 64% → 41%)
- Avoid white or gray ✓ (lightness stays 87%/86%, hue stays in
  40s)

### Move C — Ink stays warm

`--reader-fg: #2e2418` — unchanged from v75. The warm dark
ink continues to read as impressed into the parchment surface.
The reduced parchment saturation does not harm legibility (R:
243→237 against R: 46 is still a large contrast).

---

## Internal luminosity, achieved by subtraction

The brief asked for the manuscript to "appear to emit its own
quiet preserved brightness" and to "favor internal tonal
stability over external glow."

After Move A + Move B:

- The leaf no longer projects warm light outward (warm halo
  removed).
- The chamber around the leaf is quieter (dark absorption).
- The parchment is stable (single color, no graduations).
- The parchment is the only bright surface in its immediate
  pocket of the chamber.

The reader's eye reads this as: the manuscript carries its own
preserved brightness. There is no apparent light source; the
parchment simply *is* preserved. Internal luminosity through
contrast and stability, not through emitted glow.

---

## Edge assertion, achieved by the dark surround

The brief asked for "extremely subtle tonal contrast and
micro-shadowing so the eye perceives a distinct physical
sheet."

The dark absorption shadow at the leaf's perimeter creates
a quiet local tonal drop right at the leaf's edge — the
chamber goes slightly darker the moment it meets the leaf.
The eye registers this as the manuscript's edge without any
visible border line.

The 6px weight-shadow beneath adds a tiny additional edge
definition at the bottom of the leaf (the manuscript settles
on the chamber surface).

Both together provide edge perception without chrome.

---

## Doré preservation

`.folio-leaf[data-kind="plate"] { box-shadow: none; }` is
preserved from the prior pass. Doré plates retain:

- Transparent leaf background (the dark chamber is the frame).
- No halo, no weight-shadow (the engraving is its own gravity).
- The monumental cathedral-chamber treatment.

Doré reads exactly as before — monumental, framed by the dark,
its own world. The refinement passes for text witnesses do not
touch the plate chamber.

---

## What this pass does NOT do

Per the brief, explicitly:

- **No card shadows.** The weight-shadow has negative spread
  (-8px), is narrow, and sits with the leaf rather than under
  it as elevation.
- **No glassmorphism.** No backdrop-filter, no transparency,
  no frosted glass.
- **No modern modal styling.** No backdrop overlay, no
  z-stacking, no animation flourishes.
- **No visible borders.** No outlines, no perimeter lines.
- **No blur effects.** No filter:blur anywhere on the leaf.
- **No saturation increase.** Parchment saturation drops.
- **No reduced chamber darkness globally.** The chamber's
  warm vignette is untouched; only the local area around the
  leaf becomes a darker pocket.

The brief asked for refinement that the reader "should not
consciously think 'the leaf changed.'" The change is
subtle by design: a darker pocket around the leaf, a slightly
drier parchment, and the warm halo gone.

---

## What the reader will feel (without thinking)

After this pass:

- Opening a leaf no longer feels like the chamber continuing
  inward. The immediate area around the leaf grows quieter
  (the chamber attenuates locally) and the parchment reads as
  a separate material.
- The parchment carries its own preserved brightness because
  no warm light is being painted onto the surrounding
  chamber. The leaf is the bright zone; the chamber
  surrounding it is the absorption.
- The vellum shift makes the parchment feel like an archival
  sheet rather than a warm-cream UI panel. The hue change is
  too small to notice consciously; the perception is "dryer,
  older, preserved."
- Doré plates remain monumental — their own cathedral chamber
  is untouched.

The hierarchy is restored:
*Chamber = atmospheric / infinite / smoky.*
*Manuscript = dry / stable / archival / tangible.*

---

## Posture

The constitution holds. The leaf is now materially
independent from the chamber — not because chrome was added
but because warm continuity was removed and a quiet dark
pocket was opened around the manuscript. The codex remains a
codex; the chamber remains a chamber; they no longer share a
single tonal field.

The refinement is committable as a single atmospheric pass.
