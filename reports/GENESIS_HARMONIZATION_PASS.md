# Genesis Harmonization — Phase 2-5 specification

*Compiled 2026-05-21, following Phase 1 (`GENESIS_HARMONIZATION_AUDIT.md`).
This is the editorial design specification for the small CSS pass
that closes the present harmonization arc. No new metadata, no new
JS, no new HTML. CSS only.*

---

## Phase 2 decision — which family this pass formalizes

**Architecture / sacred-site.**

Per `WITNESS_FAMILY_CONSTITUTION.md` Principle 4, the family
crystallizes at five records. With wave 3 added the count to
eight Genesis records (cosmic-temple 1.7, altar Shechem 12.7,
Bethel-altar-return 13.4, well Beersheba 21.31, mount Moriah
22.2, Machpelah 23.19, wells of Isaac 26.18, Bethel pillar 28.18).

No other unformalized family has yet reached the threshold:
reception-history (2 records), cosmology non-chamber (3), map (2),
manuscript (1), ritual (1), audio (1), cross-reference (1),
reconstruction (1), artifact (1), timeline (1). The constitution
requires deferral until each reaches five.

---

## Phase 3 — opening behavior specification

### What the architecture leaf should communicate at glance

A reader who has opened an altar leaf at Shechem and then opens
a pillar leaf at Bethel should recognize, *before reading the
title*, that these are the same kind of witness — a sacred-site
stone, a place-name held in the manuscript memory.

### How identity is carried

Identity lives in **measure and rhythm**, per the constitution.
No chrome, no badges, no border. Specifically:

- **Body measure: 480 px** — narrower than commentary's 640 and
  linguistic's 560. The stone witness is the most enclosed of
  the three formalized text-witness families. A stone speaks
  briefly and in a small voice.
- **Body font-size: 0.90 em** — between commentary (0.92) and
  linguistic (0.88). The stone is less recessed than the gloss
  (it carries narrative weight, not only philology) but does
  not need the breath of an argument.
- **Body line-height: 1.60** — denser than commentary (1.74)
  and denser than linguistic (1.66). The stone is held; it does
  not breathe between lines. The inscription register.
- **Title font-size: 1.10 em** with letter-spacing 0.015 em —
  smaller than the default 1.18 em, with the faintest
  inscriptional spread between letters. The stone's name is
  spoken quietly.
- **Title margin-bottom: 24 px** — slightly tighter than the
  default 28 px. The body sits closer to its title, as an
  inscription's caption sits close to the carved face.
- **No rule beneath the title.** Distinct from commentary's
  centred hairline. The stone is its own ornament.
- **Title weight: 500 (default) and italic (default).** Not
  changed. The site's name is still in the rubric voice.

### Reading-cadence gradient now established across three families

| Family       | Body width | Body em | Line-height | Title       |
|--------------|-----------:|--------:|------------:|-------------|
| Commentary   |     640 px |   0.92  |        1.74 | italic 400, 1.18 em, centred 36 px hairline rule |
| Linguistic   |     560 px |   0.88  |        1.66 | roman 500, 1.08 em, no rule |
| Architecture |     480 px |   0.90  |        1.60 | italic 500, 1.10 em, letter-spacing 0.015 em, no rule |
| Default      |    ~800 px |   0.86  |        1.70 | italic 500, 1.18 em |

The argument flows; the gloss holds; the stone seals. Each
family's measure narrows inward — toward enclosure — as its
register tightens.

### What does NOT change

- The provenance header at the top of the leaf.
- The verse reference beneath the header.
- The kindred and resonance footers.
- The closing colophon.
- The rail glyph (`⌂`) for architecture witnesses.
- The leaf's outer 800 px width.
- The body opacity (inherited 0.78 from `.folio-body-vertical`
  — matches commentary and linguistic; the constitution forbids
  using opacity as family identifier).

---

## Phase 4 — atmospheric balance check

With architecture formalized, the Akedah cluster at Gen 22 will
visibly carry four distinct manuscript traditions inside one
chapter:

- **akedah-binding (22.9)** — commentary register, 640 px
- **hineni / ram-thicket / yhwh-jireh (22.1, 22.13, 22.14)** —
  linguistic register, 560 px
- **mount-Moriah (22.2)** — architecture register, 480 px
- **three-traditions-reception (22.19)** — default register,
  ~800 px (reception is below the constitutional threshold and
  remains in default chrome by design)

The cluster will now FEEL like a multi-traditioned chapel rather
than six identically-rendered leaves on the rail.

The Genesis-wide rhythm is preserved:

- **Gen 1** remains the museum showpiece (every family represented
  in one or two records; the unformalized families still render
  in default chrome by constitutional rule).
- **Gen 12-21** the patriarchal stippling sharpens visually:
  Shechem (12.7), Bethel-return (13.4), Beersheba (21.31) now
  all open as the same kind of witness.
- **Gen 22** becomes a coherent cluster — three families share
  the chapter cleanly.
- **Gen 23-36** Machpelah, wells of Isaac, Bethel pillar all
  cohere with the earlier sacred sites.

Doré plates, AO chambers, resonance/kindred footers, and the
Gen 1 → Gen 22 atmospheric contrast all remain unchanged.

---

## Phase 5 — implementation footprint

A single CSS block, inserted directly beneath the existing
linguistic-family block in `index.html`, targeting
`.folio-leaf[data-kind="architecture"]`. Approximately twelve
lines. Pure CSS. No JS. No new metadata. No new selectors
beyond `data-kind="architecture"`.

```css
/* ── Architecture / sacred-site family identity ──────────────
   The stone witness — narrowest measure of the three formalized
   text-witness families, denser line-height, slightly smaller
   title with the faintest inscriptional letter-spacing. The
   sacred-site witnesses across Genesis (Shechem, Bethel,
   Beersheba, Moriah, Machpelah, the wells of Isaac, the pillar
   at Bethel) now share a single recognizable leaf register —
   the manuscript inscription, held in small voice. */
.folio-leaf[data-kind="architecture"] .folio-leaf-title {
  font-size: 1.10em;
  letter-spacing: 0.015em;
  margin-bottom: 24px;
}
.folio-leaf[data-kind="architecture"] .folio-body-vertical {
  max-width: 480px;
  margin: 0 auto;
  font-size: 0.90em;
  line-height: 1.60;
}
```

That is the entire Phase-5 footprint.

---

## Phase 6 — verification scope

A diagnostic script will capture:

- One architecture leaf BEFORE the change (default chrome)
- One architecture leaf AFTER the change (family register)
- The Akedah cluster on the rail (showing the six glyphs)
- The Mount Moriah leaf opened (now in architecture register)
- The Bethel-pillar leaf opened (same register, different chapter)
- Two existing-family confirmation shots (one commentary, one
  linguistic) — to verify NO regression in already-formalized
  families
- The Doré "Confusion of Tongues" plate — to verify NO regression
  in the Doré family
- The Gen 1 cosmology chamber — to verify NO regression in AO
  chambers
- The Gen 1 rail vs Gen 22 rail — to verify atmospheric contrast
  preserved

No content changes, no AO count changes, no resonance count
changes, no Doré changes. The verification is conservative by
design.

---

## Posture

This pass is the *smallest possible step* that crosses a
constitutional threshold. One family graduates from default
chrome into formal identity. Ten families remain in default
chrome until each reaches its own five-record threshold.

After this pass, Genesis carries three formalized text-witness
families plus the Doré plates plus the twelve AO chambers plus
the kindred/resonance footers — sixteen distinct visual
traditions inside one civilizational volume. That is the codex
becoming recognizable to itself.
