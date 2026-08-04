# Witness Temporality Audit

*Compiled 2026-05-22, v80. The first temporal-depth pass.
Companion to `CODEX_ORIENTATION_AUDIT.md` and the prior
constitutional documents.*

The codex had become materially independent (v76), compositionally
ceremonious (v77), ritually paced in motion (v78), and canonically
oriented (v79). What it still lacked was *temporal depth*. Every
witness — Augustine, Doré, a Hebrew word-gloss, the ma'ariv
prayer — sat with the same present-tense weight. The reader felt
a preserved civilization arranged into chambers, but every chamber
arrived from the same depth of time.

This pass introduces the first layer of temporal differentiation.

---

## The single move

A small italic small-caps line appended to the provenance block,
declaring each family's *transmission posture*. The phrasing
implies how the witness has come to us through time — by what
mode of preservation, inheritance, or transmission.

```
TERTIARY · COMMENTARY
Christian patristic interpretive tradition
Augustine, Confessions XI / City of God XI
Archive editorial summary of primary text
─────────                                           ← provenance border
INHERITED THROUGH INTERPRETATION                    ← v80 rubric
```

(The rubric renders in italic small-caps at 0.66 em with quiet
warm color and 0.16 em letter-spacing. Sits at the bottom of
the provenance block, before the leaf's verse-ref / title /
body.)

---

## Family rubric table

Each kind carries its own temporal posture phrase, chosen to
imply the witness's mode of historical passage:

| Family             | Rubric                              | Implied transmission                              |
|--------------------|-------------------------------------|---------------------------------------------------|
| Manuscript         | `preserved through transmission`    | Survived ancient text-tradition copying           |
| Commentary         | `inherited through interpretation`  | Intellectual lineage from author to reader        |
| Linguistic         | `witnessed in philology`            | Scholarly lexical attestation                     |
| Architecture       | `held in land-memory`               | Sacred-site permanence through the landscape      |
| Ritual             | `carried through generations`       | Living practice repeated across generations       |
| Reception-history  | `layered across centuries`          | Chronological accumulation of readings            |
| Cross-reference    | `echoing through scripture`         | Canonical resonance between passages              |
| Cosmology          | `read against the world-picture`    | Read in the context of the ANE world-model        |
| Plate (Doré)       | (suppressed)                        | The plaque already carries year/artist/source     |

The rubrics are standalone phrases. They do NOT prefix or
modify the existing tradition string above them. Each is a
self-contained editorial mark declaring the witness's
relationship to time.

---

## Implementation

CSS-only. A single base block + 8 family-specific rules + 1
suppression for plates. No new HTML class names. No JS. No
data changes.

The base rule defines the typographic register:

```css
.folio-leaf-provenance::after {
  display: block;
  font-family: Georgia, serif;
  font-style: italic;
  font-variant: small-caps;
  font-size: 0.66em;
  letter-spacing: 0.16em;
  margin-top: 8px;
  opacity: 0.62;
  color: rgba(95, 70, 40, 0.78);
}
```

Each family rule sets the `content` string:

```css
.folio-leaf[data-kind="manuscript"]
  .folio-leaf-provenance::after {
  content: 'preserved through transmission';
}
.folio-leaf[data-kind="commentary"]
  .folio-leaf-provenance::after {
  content: 'inherited through interpretation';
}
/* ...and so on for the 8 families */

/* Doré is suppressed — the plaque carries its own
   temporality (year · artist · source). */
.folio-leaf[data-kind="plate"]
  .folio-leaf-provenance::after {
  content: none;
}
```

Total addition: ≈ 60 lines of CSS.

---

## Why this works

Each witness now declares its mode of historical passage
without dates, timelines, or museum signage. The reader does
not consciously read the rubric on each leaf; the rubric
accumulates over a session.

After opening a few records the reader implicitly senses:
- *Augustine arrived through 1500 years of interpretation.*
- *Mount Moriah is held in the landscape itself.*
- *The ma'ariv blessing is alive — every evening.*
- *The Akedah's three-tradition reception is layered.*
- *The manuscript witness exists in fragile transmission.*

The codex no longer flattens these into one "present" register.
Each family carries the *kind of time* it inherits.

---

## What this pass does NOT do

The brief named several constraints. This pass respects all of
them:

- **No timelines** — no chronological bars, axes, or scrolling
  visualizations.
- **No dates everywhere** — the rubric uses *language of
  transmission*, not numbers. (Doré is the only family with
  visible dates, and that's in the existing plaque.)
- **No educational chronology overlays** — no "study guide,"
  no "historical context" panels.
- **No history-app UI** — the rubric is *type set into the
  manuscript surface*, not a chrome element with affordances.
- **No witness-register flattening** — each family carries a
  distinct rubric, not a homogenized one.

The codex remains:
- quiet
- ritual
- archival
- civilizational
- inevitable

---

## Deferred to future passes

The brief named six phases. This pass directly addresses
Phase 1 (Witness Temporality), Phase 3 (Provenance Evolution),
partial Phase 4 (Historical Distance), and partial Phase 6
(Civilizational Continuity — each family's rubric implies a
continuity).

Deferred:

- **Phase 2 (Temporal Cadence)** — temporal depth through
  pacing, density, citation logic. The current pass addresses
  this implicitly via the family-specific spacers (v74, set
  in OBJECT_FAMILY_CONSTITUTION) and the leaf-architecture
  pacing (v77). Further cadence work would require per-family
  rhythm variation; reserved.
- **Phase 5 (Cosmology Deepening)** — world-model gravity for
  cosmology records. The current pass adds the rubric "read
  against the world-picture" to cosmology leaves, but the
  brief named deeper structural work (manuscript cosmograms,
  spatial manuscript composition). This requires record-level
  editorial work, not CSS. Reserved.
- **Witness-internal pacing variation** — distinct paragraph
  cadence per family (e.g., reception-history with
  chronological breaks, manuscript with vertically-tabulated
  variants). Reserved.

---

## What the codex now feels like

After v80:

- Opening a manuscript witness, the reader silently senses
  textual fragility and transmission. "Preserved through
  transmission" sits at the rubric edge.
- Opening Augustine, the reader silently senses intellectual
  inheritance. "Inherited through interpretation" stamps the
  argument.
- Opening Mount Moriah, the reader silently senses
  land-permanence. "Held in land-memory" anchors the
  inscription.
- Opening the ma'ariv blessing, the reader silently senses
  living continuity. "Carried through generations" marks the
  practice.
- Opening the Akedah-three-traditions reception, the reader
  senses centuries of layered reading. "Layered across
  centuries" closes the provenance.
- Opening the NT echoes of Genesis 1:1, the reader senses
  canonical resonance. "Echoing through scripture" announces
  the cross-canonical link.
- Opening the ANE cosmology, the reader senses a world-
  picture context. "Read against the world-picture" frames
  the explanation.
- Opening a Doré plate, the reader sees year + artist +
  source on the plaque (existing); no rubric is added — the
  plaque already carries Doré's late-19th-century gravity.

The reader's accumulated experience over a session is one of
*civilizational stratigraphy*. Different witnesses arrive from
different depths of time. The codex begins to feel temporally
inhabited.

---

## Posture

The constitution holds. The leaf is materially independent
(v76), compositionally ceremonious (v77), ritually paced
(v78), canonically oriented (v79), and now temporally
differentiated (v80).

The archive is no longer merely spatially inhabited. It is
beginning to be temporally inhabited as well — not through
visible chronology but through atmosphere. Each witness
declares its mode of passage through time, quietly, in the
form of a single italic small-caps line.

The reader does not consciously read the rubric. The reader
gradually feels: *some witnesses arrive from farther away;
some from closer; some from the living present; some from
deep transmission.*

Civilizational depth, expressed as type.
