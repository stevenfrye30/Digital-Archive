# Witness-Family Constitution

*Compiled 2026-05-20. Editorial design doctrine for the
manuscript identity of each witness family in the codex.
Companion to `ATLAS_EDITORIAL_AUDIT.md` and the Genesis
coverage documents.*

The codex has crossed from individual-object design into
**witness-family** design. The question is no longer *what
should this record look like*, but *what does a family of
witnesses feel like inside the codex over hundreds of
encounters*.

This document audits the witness families currently present in
the archive, defines a stable manuscript identity for each, and
specifies — for the two families that need it most — the first
implementation pass of family identity.

The goal is **differentiated coherence**: distinct families
living inside one codex civilization, none of them flattened
into a generic style, none of them claiming a register that
isn't theirs.

---

## I. The principle

Doré is the only fully mature witness family today. A reader who
has seen one Doré plate recognises the next one immediately —
not because it carries a label, but because the family has a
consistent silhouette in the codex: monumental engraving, dark
viewer scrim, small museum-plaque caption beneath, restrained
typographic provenance. The reader's recognition is *prior to*
the content; the family announces itself before any individual
plate does.

The goal of this constitution is to bring every other witness
family to the same level of recognizable family identity, while
keeping each family's identity *distinct from* the others. The
codex must remain a civilizational volume holding multiple
manuscript traditions — not a uniform template applied to every
record.

What family identity is, restated:

- **Consistent inside a family.** Two commentary witnesses
  should feel like the same kind of writing being practised by
  the same kind of editor.
- **Distinct between families.** A commentary witness and a
  linguistic witness should *not* be confusable at glance.
- **Subordinate to the codex.** No family asserts itself as a
  brand. The differentiation is felt, not announced.

---

## II. Audit — the present witness families

Twelve distinct witness families exist or are emerging in the
codex. The audit ranks each on five maturity dimensions:
**spacing rhythm**, **typography**, **atmospheric density**,
**hierarchy treatment**, and **recurrence behaviour**. Maturity
is rated *mature*, *forming*, or *unformed*.

### 1. Doré plates (mature on all dimensions)

  - **What it is:** 19th-century French biblical illustration,
    five records in Genesis 1-11.
  - **Current behaviour:** Plates render via a bespoke
    `_renderPlate` path. The plate sits in a dark scrim with
    a thin warm mat; beneath, a four-line plaque carries title,
    verse, provenance (artist · year · source), and authority
    line. No paper leaf surrounds the engraving.
  - **What works:** Stable framing. Stable caption rhythm.
    Predictable spacing. The reader immediately recognises a
    Doré encounter.
  - **What's immature:** Nothing. This is the standard.
  - **Constitutional behaviour:** Do not modify. The Doré
    family is the calibration mark for what family maturity
    looks like in the codex.

### 2. AO chambers (mature, family-of-twelve)

  - **What it is:** Twelve Atlas Object classes, each with a
    bespoke chamber render. The cosmology chamber, the
    sanctuary chamber, the lament chamber, the covenant
    chamber, etc.
  - **Current behaviour:** Each chamber dispatches to its own
    function (`_renderCosmologyChamber`, etc.) and carries
    chamber-specific apparatus (vocabulary tables, comparative
    sections, witness slips, layered concentric forms, etc.).
    Shared structural moves: provenance header, AO rubric,
    verse + title, lede, anchorings, kindred, resonance,
    colophon.
  - **What works:** The variety *within* family is the family.
    A reader recognises that they are inside an AO chamber by
    the consistent opening header (provenance + rubric + verse
    + title + lede) and the consistent closing footer (kindred
    + resonance + colophon). The middle of the chamber is
    chamber-specific, which is correct.
  - **What's immature:** None of the chambers; the shared
    cadence works. *Within-class consistency is mature.*
  - **Constitutional behaviour:** Treated as twelve sub-families
    sharing a meta-family identity. Continue to add chambers
    only one at a time (Akedah next). No global redesign.

### 3. Genealogical witnesses (split — chamber mature, chain forming)

  - **What it is:** Two kinds living under one name. The AO·003
    Antediluvian Line is a *realized chamber*. The eleven
    Genesis genealogy chains (cain-seth, shem-to-terah,
    jacob-esau, etc.) are *non-AO commentary records* using
    the generic renderer with `_renderGenealogyVertical` body
    treatment.
  - **What works:** The AO·003 chamber is mature. The
    non-AO chains render the tree-prefix indentation
    consistently via `_renderGenealogyVertical`.
  - **What's immature:** The chains' opened-leaf surrounding
    chrome (provenance header, verse, title) is identical to
    commentary leaves. There is no genealogical *leaf identity*
    distinct from commentary leaves.
  - **Constitutional behaviour:** Long-term — the chains
    should acquire a quiet family register (slightly different
    title weight, or a small ornament marking that the leaf
    contains a descent diagram). **Not in this first
    implementation pass.**

### 4. Commentary witnesses (forming — most numerous, least
    differentiated)

  - **What it is:** Twelve-plus records of theological,
    philosophical, and historical commentary. Augustine, Philo,
    Aquinas, Barth on Genesis 1; the wave-one and wave-two
    secondary commentaries (lekh lekha, Jacob's ladder,
    Melchizedek, covenant of pieces, descent into Egypt).
  - **What works:** The body content varies appropriately by
    record — short or long, narrative or analytical, classical
    or modern.
  - **What's immature:** Every commentary leaf renders
    visually identically. Augustine on Genesis 1:1 and
    Melchizedek at Genesis 14:18 share the same width, the
    same title typography, the same body measure, the same
    leaf chrome. **The reader has no family-level cue that
    they are inside a commentary witness.**
  - **Constitutional behaviour:** **This pass.** Define a
    narrower body measure, a slightly lighter title weight,
    and a thin manuscript rule beneath the title.

### 5. Linguistic / philological witnesses (forming)

  - **What it is:** Hebrew/Greek word-glosses. *bĕrēʾšît*,
    *tōhû wā-bōhû*, *rûaḥ ʾĕlōhîm*, *naʿăśeh ʾāḏām*, and the
    wave-two *chashav* gloss on Genesis 15:6.
  - **What works:** The titles already foreground the original
    word via transliteration. Body content is appropriately
    dense and technical.
  - **What's immature:** Same as commentary — visually
    identical to all other text witnesses. **The original
    language is the philological foreground, but the leaf
    doesn't honour that.**
  - **Constitutional behaviour:** **This pass.** Drop title
    italic so the transliterated word reads as the lexeme
    being commented on; narrow the body measure (a gloss sits
    inside a commentary's column, not beside it); slightly
    smaller title (linguistic notes observe, they do not
    pronounce).

### 6. Architecture / sacred-site witnesses (forming, wave-one
    seeded the family)

  - **What it is:** Records marking sacred sites and structures.
    Cosmic temple parallels (gen.1.7), altar at Shechem
    (gen.12.7), well at Beersheba (gen.21.31), pillar at Bethel
    (gen.28.18), and the secondary cherubim-flaming-sword note
    eventually planned for gen.3.24.
  - **What works:** Wave One established the patriarchal
    rhythm — small `⌂` chips in the rail, brief 2-3 paragraph
    leaves with Hebrew name + recurrence note. A nascent
    family identity is already present.
  - **What's immature:** Identity is not yet visually
    *enforced* — an architecture leaf could expand to look
    like a commentary leaf if its body grew. The "stone with
    an inscription" feel is editorial discipline, not
    typography.
  - **Constitutional behaviour:** Long-term — define a
    "memory-site" identity: very narrow body measure (~480px),
    Hebrew-name lead, recurrence pointer ending. **Not in
    this pass**; the wave-one records already follow this
    pattern editorially, which is enough for now.

### 7. Map / itinerary witnesses (unformed, one record)

  - **What it is:** Manuscript itineraries and cartographic
    placeholders. Constellations of the ANE (gen.1.14),
    patriarchal-journey itinerary (gen.12.5).
  - **What works:** Both records use a text-body approach
    rather than rendered maps; the `✥` rail glyph is
    consistent.
  - **What's immature:** Two records is not yet a family. The
    identity is text-emerging; it will only crystallize when
    five or six map records exist.
  - **Constitutional behaviour:** Defer family definition until
    more map records exist. Continue the text-itinerary
    pattern.

### 8. Ritual / liturgical witnesses (unformed, one record)

  - **What it is:** Liturgical texts and ritual practices.
    *Ma'ariv ʿarāḇîm* (gen.1.3) is the only current example.
  - **What's immature:** Effectively no family identity exists.
  - **Constitutional behaviour:** Defer. Family definition
    requires more records.

### 9. Reception-history witnesses (unformed, two records)

  - **What it is:** Records tracing a passage's reception
    history across centuries. *rûaḥ ʾĕlōhîm* reception
    (gen.1.2), Imago Dei reception (gen.1.27).
  - **What's immature:** Two records is not yet a family.
  - **Constitutional behaviour:** Defer. The eventual identity
    will probably feature numbered or dated paragraphs — a
    chronological reading register.

### 10. Manuscript-witness records (unformed, one record)

  - **What it is:** Records that present manuscript or textual
    witnesses to a verse. *Manuscript witnesses to Gen 1:1*
    (gen.1.1) is the only current example.
  - **What's immature:** Family identity TBD.
  - **Constitutional behaviour:** Defer. Likely shares family
    register with linguistic witnesses eventually.

### 11. Cross-reference witnesses (unformed, one record)

  - **What it is:** *New Testament echoes of Gen 1:1* (gen.1.1).
  - **What's immature:** Family identity TBD.
  - **Constitutional behaviour:** Defer.

### 12. Resonance / kindred marginalia (mature)

  - **What it is:** The quiet footer lines at the bottom of AO
    chambers — *also met here* (kindred) and *held in resonance*
    (resonance pairings).
  - **What works:** Stable italic small-caps register; warmer
    ink for kindred, cooler for resonance; small glyphs
    matching the linked AO's kind.
  - **Constitutional behaviour:** Mature. Do not modify.

### Audit summary

```
Family                        Maturity     This pass?
─────────────────────────────────────────────────────
Doré plates                   mature        no — calibration mark
AO chambers                   mature        no
Resonance / kindred           mature        no
Architecture (sacred-site)    forming       no — editorial discipline holds
Genealogical chains           forming       no
Commentary                    forming       YES
Linguistic / philological     forming       YES
Map / itinerary               unformed      no — too few records
Ritual / liturgical           unformed      no
Reception-history             unformed      no
Manuscript                    unformed      no
Cross-reference               unformed      no
```

Two families take this pass. The other ten wait for their own
crystallization — some because they are already mature, some
because they have too few records to define a family yet.

---

## III. Family identities — full definitions

For each family, the constitution declares (where the family is
mature enough to declare): **ideal width**, **title behaviour**,
**body measure**, **paragraph rhythm**, **interaction posture**,
**reveal philosophy**, **density ceiling**. Families still
forming carry partial declarations.

### Doré plates

  - **Width:** Wide. The plate fills the viewer's measure
    (~1392px on a 1440 viewport).
  - **Title:** Lives in the museum plaque, not above the
    plate. Roman, small-caps register; modest size.
  - **Body:** None. The engraving *is* the body.
  - **Reveal:** Direct. The plate appears as a finished object.
  - **Interaction:** Click-to-collapse the chamber. No hover
    states on the plate itself.
  - **Density ceiling:** One plate per chapter at most. The
    five Genesis plates are calibrated to the primeval
    section.

### AO chambers

  - **Width:** 800px leaf. Body measures vary by chamber but
    typically constrain to 540-680px.
  - **Title:** Italic, 1.18em, weight 500 — the rubric voice.
  - **Body:** Chamber-specific. Vocabulary tables, comparative
    sections, witness slips, layered forms.
  - **Reveal:** Sequential — provenance header → AO rubric →
    verse + title → lede → sections → anchorings → kindred →
    resonance → colophon.
  - **Interaction:** Click on a resonance item shifts the
    chamber. Hover on resonance items reveals the gloss
    plaque.
  - **Density ceiling:** Up to ~20 records per realized chamber
    (Genesis 1 cosmology stack). New chambers should be
    half that.

### Commentary witnesses (this pass)

  - **Width:** 800px leaf, but body measure narrows to **640px,
    centred**. The commentary reads as a deliberate paragraph
    column inside the leaf rather than as edge-to-edge text.
  - **Title:** Italic, **weight 400** (down from 500). A
    commentary title is observational, not declarative.
  - **Body:** Slightly larger font-size and longer line-height
    than the default body — a manuscript argument needs reading
    room. **font-size 0.92em, line-height 1.74.**
  - **Ornament:** A thin **36px hairline rule below the title,
    centred** — the manuscript paragraph break that signals
    "the commentary begins here." Same vocabulary as the
    chapter-plate rule from v61.
  - **Reveal:** Provenance header → verse → title → rule → body
    → kindred → resonance → colophon.
  - **Density ceiling:** Body 3-5 paragraphs for secondary, 2-3
    for tertiary. No reception-history chains, vocabulary
    tables, or multi-author stacks (those belong to the AO
    chambers).

### Linguistic / philological witnesses (this pass)

  - **Width:** 800px leaf, body measure narrows to **560px,
    centred** — narrower than commentary. A gloss is more
    enclosed than an argument.
  - **Title:** **Roman (not italic)**, weight 500, slightly
    smaller (1.08em vs 1.18em). The transliterated word in the
    title reads as the lexeme being commented on, not as an
    editorial title.
  - **Body:** Slightly smaller and tighter than commentary —
    philological notes are denser. **font-size 0.88em,
    line-height 1.66.**
  - **Ornament:** No rule below the title. The smaller roman
    title and narrower measure carry the identity.
  - **Reveal:** Provenance header → verse → title → body →
    kindred → resonance → colophon.
  - **Density ceiling:** Body 2-3 paragraphs. Linguistic notes
    name a word, give its register and morphology, point at
    one or two recurrences, and stop.

### Architecture / sacred-site witnesses (declared, not enforced
this pass)

  - **Width:** 800px leaf, body measure ~480px (narrower than
    linguistic). The "stone with an inscription" target.
  - **Title:** Italic, weight 500. The site's English name +
    em-dash + short description.
  - **Body:** **Two to three paragraphs**, opening with the
    Hebrew name + transliteration, naming the patriarchal
    event, ending with a recurrence pointer.
  - **Reveal:** Standard.
  - **Density ceiling:** Three paragraphs maximum. *Editorial
    discipline holds the form for now; if architecture
    records start sprawling, return and enforce the measure.*

### Map / itinerary witnesses (provisional)

  - **Width:** 800px leaf, body measure ~620px.
  - **Title:** Italic, weight 500.
  - **Body:** Itinerary chain followed by 2-3 paragraphs of
    geographic commentary. *Manuscript cartography, not UI
    cartography.*
  - **Density ceiling:** No actual rendered map. The body's
    arrow-chain itinerary is the map.

### Resonance / kindred marginalia

  - **Already mature. Do not modify.**
  - Italic small-caps "also met here" or "held in resonance"
    lead, followed by small kind-glyph + sub-title for each
    related object. Warmer ink for kindred, cooler for
    resonance.

---

## IV. What this pass implements

Two families: **commentary** and **linguistic / philological**.

The implementation is **pure CSS** targeting the existing
`data-kind` attribute on the leaf element. No JS changes. No
renderer changes. No new metadata fields. No new chamber
classes. The renderer continues to dispatch via `kind` exactly
as it does today; the CSS adds family-specific identity to the
common rendering output.

The full set of changes:

```css
/* ── Commentary family identity ───────────────────────────── */
.folio-leaf[data-kind="commentary"] .folio-leaf-title {
  font-weight: 400;
}
.folio-leaf[data-kind="commentary"] .folio-leaf-title::after {
  content: '';
  display: block;
  width: 36px;
  height: 1px;
  background: rgba(120, 80, 40, 0.22);
  margin: 14px auto 0;
}
.folio-leaf[data-kind="commentary"] .folio-body-vertical {
  max-width: 640px;
  margin: 0 auto;
  font-size: 0.92em;
  line-height: 1.74;
}

/* ── Linguistic / philological family identity ────────────── */
.folio-leaf[data-kind="linguistic"] .folio-leaf-title {
  font-style: normal;
  font-weight: 500;
  font-size: 1.08em;
  letter-spacing: 0.01em;
  margin-bottom: 22px;
}
.folio-leaf[data-kind="linguistic"] .folio-body-vertical {
  max-width: 560px;
  margin: 0 auto;
  font-size: 0.88em;
  line-height: 1.66;
}
```

That is the entire footprint of this pass.

---

## V. Recognizability — what should now feel different

A reader who has opened five commentary witnesses and five
linguistic witnesses should, by the sixth of each, recognise
the family before reading the title.

For commentary leaves: a slightly lighter title, a small
centred rule, a narrower paragraph column, slightly larger
prose — the manuscript-argument register.

For linguistic leaves: a roman title (often with a Hebrew
transliteration that now reads as the lexeme being studied),
a narrower body, slightly tighter line-spacing — the
philological-gloss register.

Both families remain inside the same 800px leaf, the same
provenance header, the same closing colophon. Their identity
is **internal to the leaf**, not chromatic or chromed. The
codex remains coherent.

---

## VI. What is NOT done in this pass

To be precise:

- The Doré plate family is unchanged.
- The AO chamber dispatch is unchanged.
- The kindred/resonance footer is unchanged.
- The Atlas Index page is unchanged.
- The chapter-plate, top traverse, folio rail are unchanged.
- The seven other families with one or two records each are
  unchanged. Their families do not yet exist; constitutional
  definition for them waits for sufficient records to define.
- No new metadata. No new JS function. No new HTML class names
  beyond the existing `data-kind` selector. No new files
  outside the constitutional document and the diagnostic.

The footprint is small *by design*. This is the maturation of
two families, not the redesign of a codex.

---

## VII. Constitutional principles (what governs future passes)

1. **Family identity is added via the existing `data-kind`
   selector.** No new metadata fields are introduced to support
   family typography. The kind already exists; the CSS reads
   from it.

2. **Identity is internal to the leaf.** A family's identity
   should never require new chrome around the leaf, new viewer
   states, or new interaction surfaces. Identity lives in
   title weight, body measure, and reveal cadence.

3. **No family carries colour as primary identifier.** The
   codex's colour palette is unified parchment + ink. A family
   may carry a subtle ink temperature shift, but never a
   coloured chip, badge, or border.

4. **Families crystallize when they reach five records.**
   Earlier than that, the editorial pattern is in flux; the
   constitution should not lock it in. The architecture
   sacred-site family is right at this threshold (4 records:
   altar, well, pillar, cosmic-temple); when one more is added,
   the family deserves formal CSS treatment.

5. **Mature families do not move.** Doré, AO chambers, and
   resonance/kindred are calibration marks. The next time a
   family wants to imitate one of them, that desire is a
   warning sign — distinct families inside one civilization,
   not one family wearing many costumes.

6. **The codex's volume is bounded by the leaf, the chamber,
   and the plate.** Three architectural types; everything else
   is family identity inside one of them.

---

## VIII. Closing posture

The codex began as a collection of records and is becoming a
manuscript with multiple traditions in residence. This document
formalises the transition: from "individual witnesses" to
"witness families," each with its own rhythm but all inside one
civilizational volume.

What this pass adds, simply:

- A constitutional record of where each family currently sits.
- A definition of mature identity for two families — commentary
  and linguistic — and partial definitions for the rest.
- A small CSS implementation of those two identities, using the
  existing `data-kind` attribute, no new infrastructure.
- The principle that family identity is read from the kind,
  expressed in typography and measure, and never asserted as
  brand chrome.

The next time a witness-family pass is undertaken, this
document is the editorial baseline. Future families
(architecture, genealogy, map, ritual, reception, manuscript,
cross-reference) will receive their own definitions when their
record counts warrant it, and not before.

The codex remains a codex. The families it holds become more
recognisable. The civilization deepens by becoming more
internally legible — not by adding more surface.
