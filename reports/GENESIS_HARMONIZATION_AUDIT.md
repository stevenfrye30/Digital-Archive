# Genesis Harmonization Audit

*Compiled 2026-05-21. Editorial reread of Genesis as it currently
sits in the folio. Companion to `GENESIS_MATURATION_ROADMAP.md`,
`WITNESS_FAMILY_CONSTITUTION.md`, and `ATLAS_EDITORIAL_AUDIT.md`.
This is Phase 1 of the Genesis Harmonization arc — observation
only; no implementation in this document. The diagnoses here feed
phases 2-5.*

The brief for this phase is editorial, not architectural:

> The codex must now be taught how to feel like itself.

Genesis is no longer an expansion frontier; it is the proving
ground on which the witness families learn to behave as
manuscript traditions instead of UI rows. This audit is a slow
read of the book as it currently exists, taking the cadence,
typography, opening behaviour, and silence pacing one chapter at
a time, and naming where the codex feels — and does not yet feel
— inevitable.

---

## I. The Genesis surface as it stands today

After waves one through three, Genesis carries the following
records. Counts include AO originating anchors, AO recurrence
anchors at gen.x.x, and all non-AO witnesses currently surfaced
on the folio rail.

```
Gen 1   ████████████████████  20+ records · the showpiece
Gen 2   ██                     2 AO originating (sabbath, mountain)
Gen 3   █                      1 Doré plate
Gen 4   ██                     genealogy + Doré
Gen 5   █                      AO·003 chamber
Gen 6   █                      genealogy
Gen 7   █                      Doré plate
Gen 8   ·                      silent
Gen 9   ·                      silent
Gen 10  ·                      silent
Gen 11  ███                    two genealogies + Babel Doré
Gen 12  ██                     ◐ lekh-lekha · ○ altar-Shechem
Gen 13  ○                      ○ bethel-altar-return     (wave 3)
Gen 14  ·                      silent (Melchizedek still owed)
Gen 15  ·                      silent (covenant of pieces still owed)
Gen 16  ○                      ○ el-roi-hagar            (wave 3)
Gen 17  █                      AO·006 originating
Gen 18  ◐                      ◐ three-visitors-reception (wave 3)
Gen 19  █                      genealogy
Gen 20  ·                      silent (correct)
Gen 21  █                      genealogy + ○ well-Beersheba
Gen 22  ██████                 the Akedah cluster — 6 records (wave 3)
Gen 23  ○                      ○ machpelah-cave          (wave 3)
Gen 24  ·                      silent (Rebekah still owed)
Gen 25  █                      genealogy
Gen 26  ○                      ○ wells-of-isaac          (wave 3)
Gen 27  ·                      silent (blessing still owed)
Gen 28  ██                     ◐ Jacob's ladder · ○ pillar-Bethel
Gen 29  █                      genealogy
Gen 30  ·                      silent (correct)
Gen 31  ·                      silent (correct)
Gen 32  ◐                      ◐ wrestling-Jabbok        (wave 3)
Gen 33  ·                      silent (correct)
Gen 34  ·                      silent (correct — Dinah)
Gen 35  ·                      silent (Bethel-return still owed)
Gen 36  █                      genealogy (Esau/Edom)
Gen 37  ◐                      ◐ joseph-first-dream      (wave 3)
Gen 38  ·                      silent
Gen 39  ·                      silent (correct)
Gen 40  ·                      silent (butler/baker dreams)
Gen 41  ○                      ○ pharaoh-dreams          (wave 3)
Gen 42  ·                      silent (correct)
Gen 43  ·                      silent (correct)
Gen 44  ·                      silent (correct)
Gen 45  ·                      silent (correct)
Gen 46  ◐                      ◐ going-down-into-Egypt
Gen 47  ·                      silent (correct)
Gen 48  █                      genealogy (Ephraim/Manasseh)
Gen 49  ·                      silent (Shiloh blessing still owed)
Gen 50  ·                      silent (Joseph's bones still owed)
```

**Totals (post-wave-three):** ~62 anchored records across
**~24 chapters touched**, leaving **~26 chapters in undisturbed
silence**. This is very close to the roadmap's target of "presence
at approximately 28-30 chapters."

The chapters still listed as silent in the Maturation Roadmap as
*owed* (not as deliberately quiet) are: Gen 14 (Melchizedek),
Gen 15 (covenant of pieces / Romans 4 anchor), Gen 24 (Rebekah
at the well), Gen 27 (the blessing taken), Gen 35 (Bethel
return), Gen 49 (Shiloh prophecy), Gen 50 (Joseph's bones).

This audit does **not** propose adding those records here. The
present phase is harmonization, not expansion. They are listed
only so the reader understands which silences are intentional
and which are still pending — that distinction is itself part of
the visual rhythm.

---

## II. Witness-family map — the family table at this moment

The family-by-family register of every record-kind currently
carried in Genesis, with the count, the family's maturity status
per `WITNESS_FAMILY_CONSTITUTION.md`, and whether the family has
visual identity in CSS today.

| Family                       | Genesis records | Constitution maturity | CSS identity today |
|------------------------------|----------------:|-----------------------|--------------------|
| AO chambers                  | 6 (originating) + 1 (echo at 22.20 via gen-genealogy) | mature                | bespoke per chamber |
| Doré plates                  | 5               | mature (calibration)  | full bespoke chamber |
| Genealogy chains             | 11              | forming               | minor (0.95em / opacity 0.86) |
| Commentary                   | 11              | formalized this pass  | full family CSS    |
| Linguistic / philological    | 7               | formalized this pass  | full family CSS    |
| Architecture / sacred-site   | 7               | forming → **now at threshold** | none — default leaf chrome |
| Reception-history            | 2               | unformed              | none — default leaf chrome |
| Cosmology                    | 3 (incl. AO·001 chamber) | unformed     | none for non-chamber records |
| Map / itinerary              | 2               | unformed              | none — default leaf chrome |
| Ritual / liturgical          | 1               | unformed              | none — default leaf chrome |
| Manuscript                   | 1               | unformed              | none — default leaf chrome |
| Cross-reference              | 1               | unformed              | none — default leaf chrome |
| Audio (cantillation)         | 1               | unformed              | none — default leaf chrome |
| Reconstruction (P source)    | 1               | unformed              | none — default leaf chrome |
| Artifact (Tannînim)          | 1               | unformed              | none — default leaf chrome |
| Timeline (calendar)          | 1               | unformed              | none — default leaf chrome |
| Translation-tradition (AO)   | 1 (chamber)     | mature (in chamber)   | bespoke (chamber)  |

**The constitutional inflection point this audit identifies:** the
**architecture / sacred-site family has crossed the five-record
threshold** (it now stands at seven Genesis records — Eden's
cosmic-temple parallel at 1.7, altar at Shechem 12.7, Bethel-altar
return 13.4, Machpelah 23.19, wells of Isaac 26.18, Bethel pillar
28.18, well at Beersheba 21.31). Per Constitutional Principle 4
(`WITNESS_FAMILY_CONSTITUTION.md` §VII), "Families crystallize
when they reach five records … the architecture sacred-site
family is right at this threshold; when one more is added, the
family deserves formal CSS treatment."

That moment has arrived.

The architecture family is the single family this audit
recommends Phase 2 formalize, on top of the commentary and
linguistic families already constitutionalized. The other ten
unformed families remain below the threshold and should be
deferred per the constitution.

---

## III. Chapter-by-chapter reread — what the codex looks like as you walk through Genesis

This section reads Genesis as a sustained pass. The aim is to
name where the rhythm holds and where it breaks, not to propose
fixes (that is for phases 2 and 5).

### Gen 1 — Creation (the showpiece chamber)

**Cadence:** dense by design; ~20 records across 31 verses, the
codex's most realized chapter. Two AOs originate here (cosmology
and translation-tradition), plus a constellation of supporting
apparatus: cosmology, linguistic, manuscript, commentary
(Augustine, Philo, Aquinas, Barth), reception-history (rûaḥ,
imago), cross-reference, architecture (cosmic-temple), timeline,
artifact, reconstruction, ritual, audio, plate.

**Atmosphere:** the chamber speaks. Encyclopedic, philosophical,
museum-shaped. The Gen 1 → Gen 2 cliff remains the canon's
sharpest density discontinuity — but this is a known and
intentionally borne tension, addressed not by trimming Gen 1
(which would weaken its calibration role) but by raising the
patriarchal rhythm (which waves 2-3 have begun).

**Family observation inside Gen 1:** because Gen 1 carries one or
two examples of nearly every kind, it is also the place where
the unformalized family openings are *most exposed*. A reader
opening "Cosmic Temple parallels" (architecture) immediately
after "tōhû wā-bōhû" (linguistic) experiences a visible family
change in the second leaf — the linguistic is roman, narrower,
denser — but no corresponding family change in the architecture
leaf, which renders in default chrome. The architecture record's
opening reads as a *commentary record without its commentary
ornament* — slightly orphaned.

This is the most concentrated zone in which family identity
matters, and it is also the place where the un-formalized
families show through most clearly.

**Suggested for stabilization (not this phase):** still hold the
roadmap's recommendation to trim two or three Gen 1 records that
overlap (light-before-luminaries vs the Firmament chamber;
reception-imago-history vs Barth-imago). Defer to the editorial
judgment in §III.A of the Maturation Roadmap; do not act now.

### Gen 2 — Sabbath and Sacred Mountain

**Cadence:** two AO originating chambers, no other apparatus.

**Atmosphere:** quiet. Two chambers seven verses apart (sabbath
at 2.1, mountain at 2.10) means that opening either chamber
returns the reader to the Genesis 2 rail with **no other marks
visible**. The chambers are themselves dense, but the chapter as
a *rail* is sparse — three glyphs total across 25 verses.

**Concern:** Gen 2's atmosphere depends on the two AO chambers
not feeling thin in the rail. Currently they do — because in
isolation, two glyphs on a 25-verse chapter look like the codex
has begun but stopped. The roadmap proposed adding three
tertiaries here (adam-adamah, ezer-kenegdo, edenic-rivers); not
acting now, but noting that the chapter feels *almost-empty*
rather than *deliberately spacious*.

This is the most visible "accidentally silent" chapter in Gen
1-11.

### Gen 3 — The Fall

**Cadence:** one Doré plate (expulsion at 3.24). Nothing else.

**Atmosphere:** the plate's monumental weight does carry the
chapter — the engraving is the canonical image of expulsion. The
chapter doesn't read as accidentally silent; it reads as
"acknowledged by a single image." This is intentionally minimal
and works.

**Note:** the Maturation Roadmap proposed three tertiaries
(nahash, protoevangelium, cherubim-flaming-sword). All three
would deepen the chapter; none are needed for the codex to feel
inhabited here. Defer.

### Gen 4 — Cain and Abel

**Cadence:** Doré plate at 4.8 + genealogy at 4.25. Two marks.

**Atmosphere:** balanced. Plate carries the dramatic moment; the
genealogy carries the chapter's closing register. Works as-is.

### Gen 5 — The Antediluvian Line

**Cadence:** AO·003 originating chamber.

**Atmosphere:** the lineage chamber is one of the five realized
chambers and stands on its own. Single mark, full register. Works.

### Gen 6 — Flood preface

**Cadence:** genealogy at 6.10. Nothing else.

**Atmosphere:** the chapter feels light but coherent — the Sons
of Noah genealogy reads as a transition into the flood
narrative. Sufficient.

### Gen 7 — The Flood

**Cadence:** Doré plate at 7.21.

**Atmosphere:** the deluge plate carries the chapter. The
Maturation Roadmap's proposed Noahide-covenant record (Gen 9)
and Nephilim gloss (Gen 6.4) remain compelling but unbuilt.
Acceptable as-is.

### Gen 8-10 — Post-flood silence (intentional)

**Cadence:** three chapters silent.

**Atmosphere:** the silence reads as intentional. Post-flood
narrative connective tissue; the codex correctly steps back.

### Gen 11 — Table of Nations / Babel

**Cadence:** two genealogies (11.10 Shem-to-Terah, 11.27 Terah's
house) + Babel Doré plate (11.7).

**Atmosphere:** dense but coherent. The chapter is the hinge
between primeval and patriarchal Genesis, and the three marks
read as recapitulation. Works.

### Gen 12 — Abram's call (the patriarchal threshold)

**Cadence:** secondary commentary (lekh-lekha at 12.1) +
tertiary architecture (altar at Shechem 12.7).

**Atmosphere:** **this is the patriarchal Genesis's first
realized moment**, and it lands. The secondary commentary on
"lekh lekha" carries the gravity; the architecture record at
Shechem inaugurates the wells-altars-pillars rhythm. The
chapter feels named. Two marks, balanced.

**Family observation:** the architecture record at 12.7 (altar
at Shechem) is currently rendering in default leaf chrome — same
title weight as the AO·006 chamber's rubric voice, same body
measure. Side-by-side with the commentary leaf (which is now
formalized), the architecture record looks like an unstyled
commentary. The family identity gap here is *visible at exactly
the verse where the sacred-site rhythm originates*.

### Gen 13 — Bethel altar return

**Cadence:** one architecture record at 13.4 (wave 3).

**Atmosphere:** the chapter reads as a quiet return to known
ground. The single mark feels intentional and is the *second*
architecture record in three chapters, beginning to establish
the rhythm. Works editorially.

**Family observation:** same as Gen 12.7 — the architecture
leaf opens with default chrome, which does not yet teach the
reader that this is the same kind of record as Shechem.

### Gen 14 — Melchizedek (still owed silence)

**Cadence:** silent. Melchizedek not yet present.

**Atmosphere:** the chapter feels accidentally silent given the
canonical weight of Melchizedek (Heb 7). The roadmap names this
as Priority-2 #9; not acting now, but the silence here is the
most noticeable "owed" gap in Gen 12-21.

### Gen 15 — Covenant of pieces (still owed)

**Cadence:** silent.

**Atmosphere:** also feels accidentally silent. The covenant *as
cut* is the AO·006 originating moment but is currently invisible
on the folio rail. Acceptable for this phase; mark for next
expansion.

### Gen 16 — Hagar / El-roi

**Cadence:** one tertiary linguistic record at 16.13 (wave 3).

**Atmosphere:** single quiet marker. Works.

**Family observation:** the El-roi record is linguistic, so it
already opens in the formalized linguistic-family register
(roman title, narrower measure). The chapter's atmosphere is now
correctly shaped by the family typography.

### Gen 17 — Covenant Formula chamber

**Cadence:** AO·006 originating chamber.

**Atmosphere:** chamber stands on its own. Works.

### Gen 18 — Three Visitors at Mamre

**Cadence:** one secondary reception-history record at 18.2
(wave 3).

**Atmosphere:** the chapter is named by a single substantial
witness. Editorial weight correct.

**Family observation:** reception-history has only two records
total in Genesis (this one and rûaḥ-reception at gen.1.2), so
the family is below the constitution's 5-record threshold and
should not yet be formalized. The current default chrome on
this leaf is acceptable for now — but it is also visibly
*the same chrome* as the architecture, ritual, audio, and
manuscript leaves, which means the reader has no way of feeling
"this is a reception register" yet. This is correct per the
constitution (defer until 5 records) but worth noting as a
forward concern.

### Gen 19 — Lot's daughters

**Cadence:** genealogy at 19.37.

**Atmosphere:** single quiet mark. The genealogy carries the
chapter's outcome (Moab and Ammon) without dwelling. Works.

### Gen 20 — Abimelech (intentional silence)

**Cadence:** silent. Works.

### Gen 21 — Isaac, Hagar's exile, Beersheba

**Cadence:** genealogy at 21.3 + tertiary architecture (well at
Beersheba) at 21.31.

**Atmosphere:** two complementary marks — descent + sacred site.
The architecture record fits the wells/altars/pillars rhythm and
deepens it. Works.

### Gen 22 — The Akedah (the second realized presence)

**Cadence:** **six records** across six distinct verses (wave 3):
hineni (22.1, linguistic), mount-Moriah (22.2, architecture),
akedah-binding (22.9, commentary), ram-thicket (22.13, linguistic),
yhwh-jireh (22.14, linguistic), three-traditions-reception (22.19,
reception-history). Plus the existing Nahor genealogy at 22.20.

**Atmosphere — and the central observation of this audit:**

> Gen 22 is now the codex's second realized presence after Gen 1,
> *but its presence is by accumulation, not by chamber*. The six
> Akedah records sit on the rail as six independent witnesses;
> opening any one of them opens a single leaf, not a chamber.

The roadmap explicitly chose this — "the Akedah cluster is six
independent witnesses, not a chamber" (`add_patriarchal_wave_three.py`
docstring). That choice was correct: the Akedah's weight is
narrative, dramatic, atmospheric — a chamber-rendered Akedah
would risk colonizing the silence the chapter already carries.

But the choice creates a Phase 1 finding:

> Because the six Akedah records open as six unrelated leaves
> with no shared chrome, the *cluster* is felt only on the rail
> (where six glyphs cluster) and not in the encounter. A reader
> who opens hineni and then opens akedah-binding experiences two
> isolated leaves — one linguistic-family-styled, one
> commentary-family-styled — with nothing in the leaf chrome
> itself indicating they belong to the same chapter's cluster.

This is the most important Phase-2 / Phase-3 concern this audit
surfaces. The recommendation is **not** to build a chamber. It
is to ensure that:

- **the linguistic records (hineni, ram-thicket, yhwh-jireh)
  feel cohesive with each other** — they already do, because
  they share the linguistic family CSS;
- **the architecture record (mount-Moriah) feels cohesive with
  the other sacred-site records across Genesis** — currently it
  does not, because architecture has no family CSS yet;
- **the reception-history record (three-traditions) feels
  cohesive with the other reception records (rûaḥ at gen.1.2)**
  — currently it does not, because reception has no family CSS
  yet, and the family is below threshold;
- **the commentary record (akedah-binding) feels cohesive with
  Augustine, Philo, lekh-lekha, Jacob's-ladder, and
  going-down** — it already does, because commentary has its
  family CSS.

Three of the four Akedah-family observations are about families
that ARE constitutionalized; one is about architecture, the
family at the threshold. Formalizing architecture in Phase 2
would *most directly improve the Akedah cluster's coherence* —
the gain is not "Akedah looks better in isolation" but "Mount
Moriah feels like the same kind of witness as Bethel pillar, the
Shechem altar, and the Machpelah cave."

That is family-tradition recognition, exactly the brief.

### Gen 23 — Machpelah

**Cadence:** one architecture record (wave 3) at 23.19.

**Atmosphere:** the chapter is named by a single quiet sacred-
site mark. Same family observation as Gen 22.2 — formalizing the
architecture family would tighten this leaf's coherence with the
others.

### Gen 24 — Rebekah at the well (still owed silence)

**Cadence:** silent.

**Atmosphere:** the type-scene at the well (which will recur at
Gen 29 Rachel, Exo 2 Zipporah, John 4 Samaritan woman) currently
has no anchor. The chapter feels mildly accidentally silent.
Defer; not for this phase.

### Gen 25 — Jacob and Esau

**Cadence:** genealogy at 25.26.

**Atmosphere:** single mark — the rival twins introduced as
descent. Works.

### Gen 26 — Wells of Isaac

**Cadence:** architecture record at 26.18 (wave 3).

**Atmosphere:** the chapter is held by a single quiet sacred-
site marker — Isaac re-digging his father's wells. The
re-tracing pattern is now articulated. Works editorially.

### Gen 27 — The blessing taken (still owed silence)

**Cadence:** silent.

**Atmosphere:** this is one of Genesis's most contested chapters
(the blessing-irrevocable theology) and is currently invisible.
Defer; mark for next expansion.

### Gen 28 — Jacob's Ladder

**Cadence:** secondary commentary (Jacob's ladder, 28.12) +
tertiary architecture (Bethel pillar, 28.18).

**Atmosphere:** two complementary marks at different registers —
the dream-vision commentary and the sacred-site stone. Strong
chapter. Works.

**Family observation:** the Bethel-pillar architecture record
again opens in default chrome. Formalizing architecture would
tighten this leaf's coherence with the other six.

### Gen 29 — Jacob's twelve sons

**Cadence:** genealogy at 29.32.

**Atmosphere:** the mother-grouped descent register. Single mark.
Works.

### Gen 30-31 — Laban household (intentional silence)

**Cadence:** silent. Works.

### Gen 32 — Wrestling at Jabbok

**Cadence:** one secondary commentary at 32.24 (wave 3).

**Atmosphere:** single substantial witness on the chapter's
hinge moment. Works. (The roadmap proposed three records here —
wrestling, name-change, Peniel; wave 3 chose a single substantial
commentary, which is a sound restraint.)

### Gen 33-34 — Esau reunion / Dinah (intentional silence)

**Cadence:** silent.

**Atmosphere:** correctly held silence. Especially Gen 34, where
the codex's restraint is the better posture.

### Gen 35 — Bethel return (still owed silence)

**Cadence:** silent.

**Atmosphere:** the chapter's structural arc (Jacob's return to
Bethel, completing the outward-and-inward journey) would be
sealed by a single architecture mark. The roadmap names this as
desired. Defer.

### Gen 36 — Esau's lines

**Cadence:** genealogy at 36.1.

**Atmosphere:** Esau/Edom chain. Single mark; correct.

### Gen 37 — Joseph's first dream

**Cadence:** one secondary commentary at 37.7 (wave 3).

**Atmosphere:** the Joseph cycle opens with a single substantial
mark on the sheaves dream. Works as the cycle's opening register.

### Gen 38 — Tamar and Judah (silent)

**Cadence:** silent.

**Atmosphere:** Tamar's narrative is theologically dense (the
messianic line through Perez) but the chapter is also delicate.
The codex's restraint here reads as intentional. Acceptable.

### Gen 39 — Joseph in Potiphar's house (intentional silence)

**Cadence:** silent. Works.

### Gen 40 — Butler / baker dreams (silent)

**Cadence:** silent. The Joseph dream-architecture has one
visible anchor at 37.7 and another at 41.25; the intermediate
dreams pass through quietly. Acceptable rhythm.

### Gen 41 — Pharaoh's dreams

**Cadence:** one tertiary commentary at 41.25 (wave 3).

**Atmosphere:** the dream architecture has a second quiet
recurrence here. Works as a pair with 37.7.

### Gen 42-45 — Joseph reveals himself (intentional silence)

**Cadence:** silent. Correct.

### Gen 46 — Descent into Egypt

**Cadence:** one secondary commentary at 46.3.

**Atmosphere:** the codex pivots at the going-down. Single
substantial mark on the inverse-of-exodus moment. Works.

### Gen 47 — Joseph's administration (intentional silence)

**Cadence:** silent. Works.

### Gen 48 — Ephraim and Manasseh

**Cadence:** genealogy at 48.5.

**Atmosphere:** the adoption chain. Single mark; correct.

### Gen 49 — Blessing of the tribes (still owed silence)

**Cadence:** silent.

**Atmosphere:** the Shiloh prophecy (49.10) is the messianic
anchor toward future AO·015 and is currently invisible. The
chapter reads as mildly accidentally silent given its weight.
Defer; mark for next expansion.

### Gen 50 — Joseph's bones (still owed silence)

**Cadence:** silent.

**Atmosphere:** the unfulfilled exodus seed (50.25) — bones
waiting to be carried up. The roadmap proposed a single
tertiary here to seal the book; not yet present. Defer.

---

## IV. Cross-cutting findings

Beyond the chapter-by-chapter reading, four cross-cutting
observations emerge.

### Finding 1 — The architecture family has crossed the constitutional threshold

The single most important Phase-2 observation. Seven
architecture/sacred-site records now exist in Genesis (cosmic
temple at 1.7, altar Shechem 12.7, Bethel-altar return 13.4, well
Beersheba 21.31, mount Moriah 22.2, Machpelah cave 23.19, wells of
Isaac 26.18, Bethel pillar 28.18 — that is in fact eight; the
2026-05-20 generation of `BIBLE_FOLIO_OBJECT_INDEX.md` predates
wave 3 and undercounts).

Per Constitutional Principle 4, the family **deserves formal CSS
treatment**. The roadmap's declared (but un-enforced) identity
was: "very narrow body measure (~480px), Hebrew-name lead,
recurrence pointer ending, 2-3 paragraphs max." This is now ready
to enforce.

**Phase 2 recommendation:** formalize architecture/sacred-site
identity as a CSS-only pass, analogous to the commentary +
linguistic pass. No new renderer, no new metadata. Selector
already exists (`.folio-leaf[data-kind="architecture"]`).

### Finding 2 — The default leaf chrome carries eight other families

Reception-history, cosmology (non-chamber), map, ritual,
manuscript, cross-reference, audio, reconstruction, timeline,
artifact — ten families total (most with one or two records each)
render in the default leaf chrome. This is constitutionally
correct (the constitution defers until five records each) but it
means that in Gen 1, where most of these single-record families
live, a reader sees eight different *kinds* of witness all
visually presented identically.

**Phase 1 finding, no Phase-2 action:** the constitution's
"defer-until-five" rule is correct and should be honoured. But
this audit notes that **Gen 1 is the most exposed surface** for
the cost of that rule, because the one-record-per-family
distribution is densest here. As future records accrue in
Exodus and beyond, the families that currently live only in Gen 1
will gain second and third records, and the threshold will be
crossed. Until then, the default chrome is the right placeholder.

### Finding 3 — Tertiary readability is acceptable but recessed

The `.folio-body-vertical` default of `0.86em / line-height 1.7 /
opacity 0.78` was set when the family was almost entirely
genealogy chains. With wave-three additions, the architecture,
reception, linguistic, and commentary witnesses now render
through the same wrapper. The commentary and linguistic family
CSS already restores presence (0.92em and 0.88em respectively).

But architecture, reception-history, and the unformalized
families still inherit the recessed default — which made sense for
**genealogy chains** (tree-prefix lines that should sit quietly)
but reads as **slightly washed-out** for prose witnesses.

**Phase 2 recommendation:** when formalizing architecture, give
it its own body measure rather than inheriting the genealogy
recession. Roughly: 480px measure, 0.9em, line-height 1.7,
opacity 1.0 (no recession — the stone wants presence, not
fade). This matches the constitution's declared identity for the
family.

### Finding 4 — Opening rhythm is consistent in structure but inconsistent in feel

The opening sequence for every non-chamber text witness is:
provenance header → verse → title → body → kindred → resonance →
colophon. Structurally identical across all families. This is
**correct** — the constitution says identity lives in
typography and measure, not in chrome rearrangement.

But because the title is currently the family-bearing element
(commentary lighter, linguistic roman, plate-museum-plaque,
everything else identical default), the family signal is read
in the *title alone*, not in the title-plus-cadence-plus-measure
ensemble the constitution envisions.

This is a smaller observation. The Phase-2 work on architecture
will extend the family-bearing surface to title + rule + measure
+ body cadence (analogous to what commentary already does), and
the reader will begin to recognize family before reading the
title — which is the actual constitutional target ("the family
announces itself before any individual record does").

---

## V. Atmospheric balance — Genesis as one continuous experience

The Maturation Roadmap's vision (§VI) imagines a reader moving
through Genesis and experiencing the atmosphere shift twice:
encyclopedic-dense in Gen 1, primeval-quiet through Gen 2-11,
patriarchal-stippled with sacred-sites through Gen 12-21,
slowing into the Akedah at Gen 22, recurring patriarchal rhythm
through Gen 23-36, then Joseph-cycle sparse-but-deliberate
through Gen 37-50, closing on Joseph's bones.

**As of wave 3, this arc is mostly in place** — with three
caveats:

1. **Gen 22 is realized at the rail but not at the leaf.** The
   six-record Akedah cluster is visible as a cluster on the rail
   and would benefit (Phase 2) from architecture-family
   formalization to tighten its cohesion when individual leaves
   are opened. The reading roadmap's idea of a "chapel-shaped"
   second realized presence is essentially there in record
   density; what remains is family identity at the leaf level.

2. **Gen 12-21 patriarchal-stippling reads correctly.** The
   sacred-site rhythm (Shechem 12.7, Bethel 13.4, Beersheba
   21.31) is now legible on the rail across multiple chapters.
   The single weak point is that opening each architecture leaf
   does not yet reinforce the family — Phase 2 closes this.

3. **Gen 50 is silent where the roadmap wanted a sealing mark
   (Joseph's bones).** Without it, the book ends in unannounced
   silence rather than the deliberate sealing the roadmap
   imagined. This is not a Phase-1 fix; mark for the next
   expansion.

The Gen 1 → Gen 22 atmospheric contrast that the audit was
asked to evaluate now reads correctly: Gen 1 is a museum, Gen 22
is a chapel-as-cluster, the patriarchal chapters between them
breathe with sacred-site rhythm. **The chapel does feel holier
and sparser than the museum.** This is the right shape.

---

## VI. Phase-2 / Phase-3 input — what this audit hands forward

Concretely, the next phases inherit:

### For Phase 2 (witness-family formalization)

- **Architecture / sacred-site is the one new family to
  formalize.** Eight records in Genesis, above threshold, with a
  clear identity declared in the constitution but un-enforced.
  CSS-only pass on `.folio-leaf[data-kind="architecture"]`.
- **All other unformalized families remain below threshold and
  should be deferred** per Constitutional Principle 4.
- **Commentary and linguistic remain as-is** — they were
  formalized in the prior pass and the audit confirms they work.
- **Genealogy chains do not yet need formalization** — the
  minor existing CSS (recession to 0.86 opacity) is correct for
  tree-prefix descent text, and the AO·003 chamber carries the
  family's mature realization. Defer.

### For Phase 3 (object opening standardization)

- **Each family's opening should communicate its kind before the
  reader reads the title.** Commentary already achieves this via
  lighter title + centred hairline rule + narrower paragraph
  measure. Linguistic achieves it via roman title + narrower
  measure + tighter prose. Architecture should achieve it via
  even-narrower measure + Hebrew-name lead in the body + restored
  presence (not the recessed default).
- **No new chrome.** No badges, no chips, no kind labels above
  the leaf. The constitution forbids it; this audit reaffirms.
- **No new HTML or renderers.** All identity is on the existing
  `data-kind` selector.

### For Phase 4 (atmospheric balance)

- The arc is already in place. The phase-4 audit will mostly
  verify rather than redesign.
- The two open concerns named in §V (Gen 22 leaf-level cohesion,
  Gen 50 unsealed close) are the only structural items —
  cohesion is addressed in Phase 2, and the Gen 50 record is
  out of scope for this phase entirely.

### For Phase 5 (refinement-only implementation)

The refinements that follow from this audit are deliberately
small:

1. **Architecture family CSS.** Title weight + body measure +
   first-paragraph Hebrew-name register (if achievable via
   selector; otherwise editorial-only). Tertiary-of-the-tertiary
   register: the stone should feel like a stone, not a
   commentary.
2. **Body measure correction for architecture.** Stop inheriting
   the recessed `.folio-body-vertical` default; restore opacity
   to 1.0 and use a 480-540px measure.
3. **No other CSS changes.** Phase 5 is about extending the
   constitution's two-family pattern to one additional family,
   not about touching anything that already works.

### For Phase 6 (verification)

- **AO count must not change.** Twelve.
- **Resonance pair count must not change.** Eight.
- **Doré must not change.** Five.
- **Commentary + linguistic + AO chamber families must not
  regress.** Phase 5 touches only architecture selector.
- **Screenshots must show:** Mount Moriah leaf · Bethel pillar
  leaf · altar at Shechem leaf · Machpelah cave leaf · Beersheba
  well leaf — to verify the family now feels like one tradition.
  Plus the standard Gen 1 vs Gen 22 atmospheric pair and one
  commentary + one linguistic example to confirm no regression.

---

## VII. Closing posture

Genesis has reached its coverage target. What the codex needs
now is not more, but coherence — the manuscript-tradition feel
the witness-family constitution names.

This phase of harmonization is the smallest possible step that
crosses a constitutional threshold: one family — architecture —
graduates from default chrome into formal identity, while
ten other still-unripe families wait their turn. Commentary and
linguistic have already done so. After Phase 2-5, the rail of
Genesis will carry three distinct, recognizable witness
traditions plus the calibration marks (AO chambers, Doré
plates, resonance/kindred). That is the minimum number at which
the reader can begin to *feel* the codex as multi-traditioned —
and it is also the maximum number that respects the
constitution's "five-records-or-defer" rule.

The Genesis Harmonization arc, in summary:

- **Phase 1 (this document):** name what the codex now looks like.
- **Phase 2:** formalize architecture's family identity (CSS only).
- **Phase 3:** verify the new opening teaches the reader the
  kind it belongs to.
- **Phase 4:** confirm the Genesis-wide atmosphere still
  breathes correctly.
- **Phase 5:** ship the small CSS pass; touch nothing else.
- **Phase 6:** diag + screenshots to verify no regressions.

The goal is not novelty. The goal is that Genesis, encountered
again from the beginning after the work is done, will feel
*more itself* — and that the architecture leaves, when the
reader opens them, will recognizably belong to the same
manuscript tradition as one another.

That is what this phase is for.
