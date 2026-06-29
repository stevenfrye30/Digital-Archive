# Genesis Reading-Flow Audit

*Compiled 2026-05-21. Phase 1 of the Reading-Flow Consolidation
arc. Companion to `GENESIS_HARMONIZATION_AUDIT.md`,
`GENESIS_HARMONIZATION_PASS.md`, `WITNESS_FAMILY_CONSTITUTION.md`,
and `ATLAS_EDITORIAL_AUDIT.md`. This audit is observation, not
implementation; phases 2-5 follow.*

The brief: read Genesis naturally, as a reader. Not as a
developer. Not as an implementer. Find the places where the
codex still feels software-like — the small procedural seams
that the constitution has not yet shaved off — and the places
where the codex now feels inhabitable. Then make extremely small
refinements; no architecture changes.

The reading walk that grounds this audit captured fifteen
chapter rails plus six representative leaf openings plus two
viewer-active spreads — `reports/walk_v70_*.png`. These are
what an actual reader would see at a 1440-wide viewport.

---

## I. The seven reading passes

### 1. Text-only reading

**Procedure.** Open Gen 1 → Gen 50 sequentially with the
companion column collapsed (no rail). Read the scripture as
scripture.

**Observation.** The text-only mode is the codex's quietest
register and reads cleanly. Roman numeral chapter heads, drop
caps on verse one, the small Georgia verse-numbers, the
generous line-height — this is the reading register the codex
was designed around. Nothing here breaks. The text-only reader
sees no codex; only scripture.

### 2. Light folio engagement

**Procedure.** Companion column open at CORE depth (lowest
density). Reader skims chapter to chapter.

**Observation.** At CORE depth most chapters show no rail at
all. The rail only surfaces the AO originating anchors and
plate witnesses. Gen 1, Gen 2 (sabbath + mountain), Gen 3 (Doré),
Gen 5 (lineage chamber), Gen 17 (covenant) — the codex's
canonical centres are visible; everything else is silent. The
CORE register works: a reader hovering at the lowest depth
sees only the gravity centres.

### 3. Dense-object engagement

**Procedure.** Companion at ARCHIVE depth (all records). Reader
opens chambers and leaves freely.

**Observation.** This is where the codex's full apparatus lives.
The AO chambers (cosmology, sanctuary) reward summoning with
vocabulary tables, comparative sections, layered enclosures.
Doré plates dominate the dark chamber. The newly-formalized
text-witness families (commentary, linguistic, architecture)
each open as their own kind of leaf — the gradient is
recognizable now.

**Limit of the reward asymmetry.** Opening an AO chamber yields
~15-20 structured elements (vocabulary, anchorings, comparative,
threshold rubrics, etc.). Opening a non-chamber leaf yields ~4
elements (provenance, verse, title, body). The reward gradient
is steep. This is correct by design — chambers are realized
moments, leaves are quiet witnesses — but it means a reader who
opens *only* non-chamber leaves in succession encounters six
visually-identical templates in a row. The encounter itself
begins to feel modal.

### 4. Sequential chapter navigation

**Procedure.** Move through Gen 1 → 2 → 3 → 4 → ... using
"previous / next" chapter links.

**Observation.** The chapter transitions are graceful in form
— the chapter head (GENESIS · I → GENESIS · II) provides a
consistent visual frame at each step. The previous/next
rubrics at top sit quietly. The codex does not feel like a
"book reader app" here; it feels like turning manuscript leaves.

**One seam.** When moving from a chapter with rail marks (Gen 1)
to a chapter without (Gen 2 at certain depths), the rail column
goes from busy to empty in one click. The transition is sharp.
Not a flaw — the codex is *correctly* reflecting the canon's
shape — but it is felt.

### 5. Long-session fatigue reading

**Procedure.** Forty-five minutes of continuous Genesis reading
with the rail at ARCHIVE depth and occasional summoning.

**Observation.** The eye adapts quickly to the parchment
column and the rail's tertiary recession. The light-fatigue
behaviour is sound. **But:** the leaf-opening cadence becomes
predictable in a quietly tiring way. Every opened leaf appears
in the same modal position, with the same provenance header
structure (TERTIARY · KIND on line 1, source-basis on line 2,
confidence on line 3, hairline separator, "for Gen X:Y" on
line 4, title on line 5). After ten openings the structure is
felt as a template — *the reading rhythm becomes faster than
the encounter rhythm*. This is the cleanest place for a
micro-refinement.

### 6. Random-access opening

**Procedure.** Jump between non-adjacent chapters using the
chapter selector and Atlas Index.

**Observation.** The chapter selector + book pulldown works
quickly. The Atlas Index page (separate from the folio view)
serves random access well. Nothing here that needs attention.

### 7. Object-hopping reading

**Procedure.** Open one leaf at Gen 1.1 → close → open one at
Gen 12.7 → close → open Gen 22.2 → close → ...

**Observation.** This is the pass that most exposes the
leaf-opening repetition. Six leaves opened in succession share:

- Same dark-chamber backdrop
- Same parchment leaf at the same centred position
- Same provenance-header rhythm
- Same "for Gen X:Y" verse-prefix
- Same title-then-body structure
- Same kindred / resonance / colophon footer

The constitution argues — correctly — that this consistency is
the codex's frame, and that family identity should live
*within* the parchment, not in the chrome around it. This audit
agrees. The question is whether the chrome rhythm itself can
be made slightly less repetitive *without* introducing per-
family chrome.

---

## II. What works — keep untouched

1. **The dark-chamber + parchment-leaf framing.** This is the
   codex's signature. It should not change.
2. **The provenance header's existence.** It declares
   authority + kind + tradition + source-basis before content.
   Constitutional. Untouchable.
3. **The chapter head (GENESIS · ROMAN).** The transition rubric
   between chapters. Quiet, dignified, manuscript-shaped.
4. **The silent-rail behaviour at empty chapters.** Gen 8 reads
   as undisturbed scripture; the codex completely steps back.
   Beautiful.
5. **The three-family measure gradient (640 / 560 / 480).** Just
   shipped. Reads coherently in side-by-side openings (Augustine
   commentary vs tohu linguistic vs Shechem architecture — three
   visibly distinct registers).
6. **Resonance + kindred footers.** Italic small-caps "also met
   here", warmer kindred ink, cooler resonance ink. Untouched.
7. **AO chamber dispatch.** Twelve bespoke chambers each their
   own world. Untouched.
8. **Doré plate framing.** Museum chamber. Untouched.

---

## III. Where the codex still feels procedural

Five small observations. Each carries disproportionate
atmospheric weight; none requires architecture change.

### Seam A — "for Gen X:Y" reads as a UI breadcrumb

The verse-reference line ("for Gen 1:1", "for Gen 22:2", etc.)
sits between the provenance header's hairline separator and
the leaf title. It is in italic Georgia at 0.85em with 78%
opacity. It says **for** — a small functional preposition —
followed by a colon-separated citation.

> "for Gen 22:2"

In manuscript typography the citation would more naturally
read as an *attestation*, not a *for-clause*:

> "— Gen 22:2"  or  "Gen 22:2"  or  italicized "Gen 22:2"
> without preface

The current "for" is the only piece of the entire leaf chrome
that reads as a software label rather than as a manuscript
mark. Every other word in the leaf has manuscript weight.

This is the single smallest, cleanest micro-refinement
available. Remove the preface; let the citation stand as
attribution.

### Seam B — Default-chrome leaves render at full ~800px

Three text-witness families now have measured columns
(640 / 560 / 480 px). Every other family — reception-history,
ritual, audio, cosmology non-chamber, manuscript, cross-
reference, reconstruction, artifact, timeline, map — uses the
default `.folio-body-vertical`, which has *no max-width*. These
default-chrome leaves therefore fill the leaf's full ~800px
width.

This creates an inversion that I noticed in the leaf walk:

| Family                | Body width | Authority of records      |
|-----------------------|-----------:|---------------------------|
| Commentary            |     640 px | mostly tertiary           |
| Linguistic            |     560 px | mostly tertiary           |
| Architecture          |     480 px | mostly tertiary           |
| **Reception-history** | **~800 px** | **substantial secondary** |
| Manuscript            |    ~800 px | primary                   |

The Three Visitors leaf at Gen 18.2 (`gen18-three-visitors-
reception`) is the canonical example. It is a SECONDARY
substantial witness with a 400-word body and Rublev's icon as
its visual touchstone. It opens at ~800px — visibly wider than
the tertiary commentary leaves it sits alongside.

**The visual hierarchy reads backwards: the most prepared
witnesses are most constrained; the substantive secondary
sits unbounded.**

This is not a failure of the constitution — the constitution
correctly defers family formalization until five records per
family. But the *default* (un-formalized) body measure was set
when nearly all text witnesses were genealogy chains. With
wave-three additions, the default now collides with the
formalized-family gradient.

**Proposed micro-refinement (Phase 4):** add a default max-width
of ~700 px to `.folio-body-vertical`, so un-formalized leaves
sit visibly above commentary's 640 px in the gradient — still
the widest of the four — but no longer unbounded. The gradient
becomes:

```
default       700 px   (unformalized; widest by ~60 px)
commentary    640 px   (argument)
linguistic    560 px   (gloss)
architecture  480 px   (stone)
```

This restores the visual hierarchy without claiming a family
identity for the un-formalized leaves. The 700-px default reads
as "leaf-in-progress" rather than "this is the unconstrained
leaf."

### Seam C — Provenance header opens with the same four-line block every time

The provenance header is:

```
TERTIARY · COMMENTARY            ← small-caps, 0.72em
Patriarchal narrative — Hebrew…  ← italic, 0.76em
Gen 22:9; cf. Heb 11:17-19       ← italic, 0.76em
Archive editorial narrative…     ← italic, 0.76em
─────────────────────────────────  ← hairline rule
```

Four lines of small italic before the verse reference and title.
In one leaf, this reads as scholarly rubric — sound. In ten
leaves opened in quick succession (Pass 7 above), the same
four-line shape becomes the rhythm of opening itself. The
reader anticipates the header before it appears.

The header content is constitutional — authority, tradition,
source-basis, confidence all matter. None of them can be
removed. **But** the visual density of the block can be
softened slightly — slightly tighter line-spacing between the
three italic lines, slightly more breath between the block and
the title that follows — so that the header recedes one degree
deeper into the leaf's background and the title carries more
of the leaf's first-glance weight.

**Proposed micro-refinement:** tighten provenance line-height
from current default to ~1.32, and increase the title's
top-margin by ~6 px. The reader's eye lands on the title
sooner; the provenance becomes more clearly a *header* and less
of a *block*.

### Seam D — The Akedah cluster is felt only on the rail

Six records anchored across Gen 22.1, 22.2, 22.9, 22.13, 22.14,
22.19. On the chapter rail the cluster is visible — six glyphs
ranged down the chapter's height. But when the reader opens any
of them individually, the cluster *disappears* from the reading
experience: each opens as a standalone leaf, the rail collapses
into the dark backdrop, and there is no in-leaf indication that
this leaf belongs to a chapter-cluster.

**The cluster is a rail-only phenomenon.** When reading inside
the leaf, the codex forgets that the Akedah is also five other
records away.

This is structurally correct per the wave-three editorial
choice ("six independent witnesses, not a chamber"). And the
audit does NOT propose making it a chamber. **But** there is a
small editorial gesture available: the kindred footer at the
bottom of each Akedah leaf could surface the *other* five
Akedah records as kindred at the same anchor. This would
require record-data, not CSS — and so is out of scope for this
phase.

What CAN happen this phase: when the reader closes an Akedah
leaf and returns to the chapter, the rail should briefly hold
its presence rather than collapse instantly. Currently the
leaf closes and the rail markers re-emerge identical to their
pre-encounter state, as if no encounter occurred. A faint and
extremely brief "warmth" trace on the just-opened marker — say,
a half-second of slightly higher opacity — would teach the
reader that the rail is remembering.

**Status:** noted; potentially in scope for Phase 4 if it can be
done with a single CSS transition on a class the renderer
already toggles. If it requires JS, defer.

### Seam E — Below-the-fold rail marks are invisible on chapter entry

A chapter opens at verse 1. Rail marks at verses 12-30 are
below the visible viewport. Gen 32 is the cleanest example:
the wrestling commentary at v.24 is invisible on first load,
so Gen 32 LOOKS like a silent chapter until the reader scrolls.
The single-most-important witness in the chapter is hidden by
default.

**Proposed micro-refinement:** ensure the rail's overall
extent — a faint vertical line, or even just the company of a
small distant glyph in the lower viewport — is visible even
above the fold. The current rail is per-verse only; there is
no "presence indicator" suggesting the rail has content lower
down.

The cleanest way to do this without adding chrome: a very faint
hairline running the full height of the rail column (perhaps
1px, 8% opacity, parchment-warm) that exists whether or not
the visible verses have markers. This communicates "the rail is
here, and may carry presence below" without claiming any
specific content. It is the same kind of move as the dotted
hairline in Lament chamber, applied at one degree of restraint
further.

**Status:** noted as the second cleanest available micro-
refinement. Implementable as a single `border-left` on the rail
column.

---

## IV. Atmospheric coherence — does Genesis feel inhabitable?

Yes, with the caveats above. The Genesis I walked through
today is:

- **Calibrated.** Gen 1 still the showpiece (rail dense, chamber
  encyclopedic), Gen 22 calmer with its six-record cluster, the
  patriarchal middle quietly stippled with sacred-site marks.
- **Coherent at the family level.** The three formalized
  families now read as distinct manuscript traditions; the
  fourth-and-beyond families read uniformly (default chrome) —
  which is the constitution's correct posture, but Seam B
  surfaces a small visual hierarchy inversion.
- **Silence-respectful.** Gen 8 / Gen 30 / Gen 47 read as
  undisturbed scripture. The rail completely steps back.
- **Reward-asymmetric, by design.** Chambers reward summoning
  with depth; leaves with brevity. Reading is contemplative
  rather than dashboard-like — the codex does not surface its
  apparatus until requested.

The single residual feeling that remains "software-like": the
*leaf-opening transaction*. Six leaves opened in succession
share the same modal cadence. The constitution allows for
this — identity lives inside the parchment, not in the chrome
around it — but the chrome rhythm can be made slightly less
template-shaped with the small refinements named above.

---

## V. What this audit recommends for Phase 4 implementation

Five micro-refinements, in priority order. Each is small and
reversible.

### 4-1 — Soften the "for Gen X:Y" verse rubric

**Footprint:** one line of JS (the renderer that emits the
verse line) and possibly one CSS adjustment. Drop the "for "
preface; render the citation as standalone italic — either
`Gen 22:2` alone or `— Gen 22:2`.

**Effect:** removes the single most software-like word in the
leaf chrome.

### 4-2 — Add a default body-vertical max-width of ~700 px

**Footprint:** add `max-width: 700px; margin: 0 auto;` to the
existing `.folio-body-vertical` selector.

**Effect:** un-formalized family leaves no longer sit
unbounded. The four-step measure gradient (700 / 640 / 560 /
480) reads from widest-to-narrowest in the constitutional
order. The Three Visitors reception leaf becomes visually
closer to the rest of the codex.

### 4-3 — Soften the provenance header block

**Footprint:** small line-height tightening on the three italic
lines (`.flp-tradition`, `.flp-source`, `.flp-confidence`)
and an ~6 px increase on the title's pre-margin via the leaf
title's effective top-margin in opened-leaf state.

**Effect:** reader's eye reaches the title sooner; provenance
recedes into header-shape rather than reading as a block.

### 4-4 — Add a faint full-height rail-presence hairline

**Footprint:** one `border-left` or `::before` on the rail
column (`#folio` or equivalent) with ~1 px width and ~8 %
opacity in warm parchment tone.

**Effect:** the rail column communicates "I am here" even when
nothing is anchored above the fold. Below-the-fold presence is
implicit.

### 4-5 — Brief warmth on just-summoned rail markers (CONDITIONAL)

**Footprint:** CSS transition on a class the renderer already
toggles when an object is opened. If no such class exists,
defer entirely.

**Effect:** the reader feels the codex remember which marker
was just touched.

Total proposed CSS footprint across all five refinements:
approximately 12 lines of CSS plus ~3 lines of JS for 4-1.
No new metadata, no new renderers, no new HTML class names,
no architecture changes.

---

## VI. What is explicitly OUT of scope for this phase

Per the briefing, none of the following:

- **No new witness records.** Gen 14 Melchizedek, Gen 15
  covenant-of-pieces, Gen 24 Rebekah, Gen 27 blessing, Gen 35
  Bethel-return, Gen 49 Shiloh, Gen 50 Joseph's bones — all
  remain owed-but-deferred per the Maturation Roadmap's
  Priority-2 / Priority-3 lists. Do not add them now.
- **No new AO objects.** Twelve. AO·013-015 still deferred.
- **No new witness-family formalization.** Reception-history
  remains at two records (below threshold). Defer.
- **No new chamber dispatch.** No Akedah chamber. The six
  records remain six independent witnesses.
- **No new dashboard, no navigation overlays, no metadata
  panels, no animation systems.**
- **No expansion into Exodus.** Genesis remains the proving
  ground.

The aim of Phase 4 is editorial tact at the millimetre. Not
redesign. If a refinement requires more than ~5 lines of CSS or
~3 lines of JS, it is the wrong scale for this phase and should
be deferred.

---

## VII. Closing posture

Genesis now reads as inhabitable. The codex's structure, after
v68 wave-three and v69 architecture-family formalization, has
crossed the threshold from "an apparatus laid over scripture"
to "a manuscript in residence." A reader spending an hour with
Genesis encounters silence, chamber, plate, cluster, and the
three-family gradient — each at its own register, each in its
own place.

What remains is millimetre work:

- A word ("for") that does not belong.
- A measure (default ~800 px) that no longer matches the
  family gradient.
- A header block that wants slightly less density when seen
  in succession.
- A rail column that wants a faint indication of vertical
  extent.
- Possibly, a memory in the just-touched marker.

These are the smallest possible refinements that carry
atmospheric weight. They are what Phase 4 will ship.

> *Tiny adjustments carry disproportionate atmospheric weight.*

Phase 1 stands.
