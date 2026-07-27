# Civilizational Geography Audit

> *Note (2026-07-27, Task 16): the steward renamed "Atlas Objects" to **Codex Objects** ("Atlas" now belongs solely to the workspace's graph-engine layer). This dated record keeps its original wording.*

*Compiled 2026-05-22, v82. The first depth-gradient pass.
Companion to `CIVILIZATIONAL_INHERITANCE_AUDIT.md` and the
constitutional documents above it.*

After v81's civilizational inheritance (cosmology cosmogram +
cross-reference echo), the codex held witness families in
recursive relation. But every chapter still presented itself
with the same atmospheric weight. Genesis 1, Genesis 8,
Genesis 22, Psalm 23, Isaiah 53, Revelation 21 — all rendered
through an identical chapter-plate. The reader could not
yet feel *where in the codex's geography they were standing*.

This pass introduces the first geographic-depth layer.

---

## The single move

A `data-density` attribute on the chapter heading, set in JS
based on whether the chapter is:

- **silent** — no records anchored to this chapter
- **center** — a canonical center of gravity (hardcoded list)
- **standard** — has records but is not on the center list

The CSS then renders the chapter-plate's atmosphere differently
per register:

### Silent — wilderness register

```css
.chapter-room-heading[data-density="silent"] {
  padding-top: 56px;       /* was 36 */
  padding-bottom: 64px;    /* was 44 */
}
.chapter-room-heading[data-density="silent"] .ch-rule {
  border-top-color: rgba(120, 80, 40, 0.28);  /* was 0.42 */
  width: 36px;                                  /* was 44 */
}
.chapter-room-heading[data-density="silent"] .ch-stratum {
  opacity: 0.6;
}
```

The chapter widens its breath; the rule and stratum fade. The
reader crossing into a silent chapter feels they have entered
*terrain the codex has not colonized*. The page is undisturbed
scripture.

### Center — canonical-gravity register

```css
.chapter-room-heading[data-density="center"] .ch-rule {
  width: 64px;                                  /* was 44 */
  border-top-color: rgba(120, 80, 40, 0.58);  /* was 0.42 */
  margin: 22px auto 20px;                       /* was 20 auto 18 */
}
.chapter-room-heading[data-density="center"] .ch-stratum {
  opacity: 0.65;
}
```

The hairline rule lengthens 45 % (44 → 64 px) and intensifies
(alpha 0.42 → 0.58). The reader crossing into a center feels
*architectural centrality* — the chapter-plate's own rule
declares it a gravitational center.

### Standard — unchanged default

Inhabited chapters that are not centers retain the existing
36/0/44 padding and 44 px hairline. The default reads as
ordinary inhabited terrain.

---

## The canonical-centers list

Hardcoded in JS as `_CANONICAL_CENTERS`:

| Torah | Hebrew Bible | New Testament |
|---|---|---|
| gen.1 (Creation) | psa.13 (Lament) | mat.5 (Sermon on the Mount) |
| gen.22 (Akedah) | psa.22 (Forsaken) | jhn.1 (Word made flesh) |
| exo.3 (Burning Bush) | psa.23 (The Shepherd) | rev.4 (Throne Vision) |
| exo.19 (Sinai) | isa.6 (Throne Vision) | rev.21 (New Creation) |
| exo.20 (Decalogue) | isa.53 (Suffering Servant) | rev.22 (Closing) |
| exo.40 (Glory Filled) | | |
| lev.16 (Day of Atonement) | | |
| deu.6 (Shema) | | |

18 chapters across the canon. Each carries the lengthened
intensified rule. The list is small by design — these are the
chapters the canonical tradition treats as gravitational; the
codex's geography honors them.

The list can grow over time. New centers may emerge as the
codex's coverage deepens (e.g., act.2 Pentecost, rom.8,
1co.13). For now, 18 centers.

---

## What the reader walks through

Reading Genesis sequentially:

```
Gen 1   — CENTER       (creation; the showpiece)
Gen 2   — STANDARD     (sabbath + sacred mountain)
Gen 3   — STANDARD     (Doré expulsion)
Gen 4   — STANDARD     (Cain + Doré)
Gen 5   — STANDARD     (antediluvian chamber)
Gen 6-7 — STANDARD     (Doré deluge + genealogy)
Gen 8   — WILDERNESS   (silent — post-flood breath)
Gen 9   — WILDERNESS   (silent)
Gen 10  — WILDERNESS   (silent)
Gen 11  — STANDARD     (Babel + genealogies)
Gen 12  — STANDARD     (Abram's call)
Gen 13  — STANDARD     (Bethel return altar)
Gen 14  — WILDERNESS   (Melchizedek still owed)
Gen 15  — WILDERNESS   (covenant of pieces still owed)
Gen 16  — STANDARD     (El-roi)
Gen 17  — STANDARD     (Covenant chamber)
Gen 18  — STANDARD     (three visitors reception)
Gen 19  — STANDARD     (Lot's daughters genealogy)
Gen 20  — WILDERNESS   (silent)
Gen 21  — STANDARD     (Beersheba well)
Gen 22  — CENTER       (Akedah; canonical centre)
Gen 23  — STANDARD     (Machpelah)
Gen 24  — WILDERNESS   (Rebekah owed)
Gen 25  — STANDARD     (Jacob & Esau)
Gen 26  — STANDARD     (wells of Isaac)
Gen 27  — WILDERNESS   (blessing still owed)
Gen 28  — STANDARD     (Jacob's ladder)
Gen 29  — STANDARD     (twelve sons)
Gen 30  — WILDERNESS   (silent — household drama)
Gen 31  — WILDERNESS   (silent)
Gen 32  — STANDARD     (Wrestling at Jabbok)
Gen 33  — WILDERNESS   (silent)
Gen 34  — WILDERNESS   (silent — Dinah)
...
Gen 50  — WILDERNESS   (silent — bones owed)
```

The Genesis terrain begins reading as *geography*: a capital
at chapter 1, breathing silent stretches in the post-flood and
Joseph cycle, a sacred mountain at chapter 22, sparse and
inhabited terrain between.

Reading across the canon: Exodus 19 + 20 + 40 surface as
centers in their book; Leviticus 16 stands as a single center
in an otherwise (currently) silent book; Psalm 13, 22, 23 are
three centers in the Psalter; Isaiah 6 + 53 read as two pillars
of the prophets; the Gospel + Apocalypse close with centers at
John 1, Rev 4, Rev 21, Rev 22.

The reader walking the canon feels its geography form — centers,
inhabited terrain, wilderness, all visible in the chapter-
plate's own register.

---

## What this pass does NOT do

The brief was specific:

- **No maps** — no spatial visualization of the codex.
- **No minimaps** — no overview UI of any kind.
- **No navigation trees** — no expandable hierarchy.
- **No exploration mechanics** — no objectives, no quests.
- **No gamification** — no achievements, no progress, no
  scores.
- **No rarity systems** — no "deep witnesses" hidden by
  difficulty.
- **No hidden collectibles** — nothing the reader has to
  unlock.
- **No game aesthetics** — no fantasy framing, no lore.

Centers are not "boss chapters." Wilderness is not "level
0." The codex is not a game. The geography emerges from the
chapter-plate's own register — type, padding, rule — set
according to the chapter's actual canonical position.

---

## Implementation footprint

CSS-only + a small JS density-computation function. No new
HTML class names. No new metadata fields. No database changes.

### JS

```javascript
const _CANONICAL_CENTERS = new Set([ /* 18 centers */ ]);

function _chapterDensity(bookKey, chapterNum) {
  const key = `${bookKey}.${chapterNum}`;
  if (_CANONICAL_CENTERS.has(key)) return 'center';
  // Scan currentData.genealogy for anchors matching this chapter.
  // If any match → 'standard'; otherwise → 'silent'.
}
```

In `_buildChapterHeading`:
```javascript
heading.dataset.density = _chapterDensity(bk, chNum);
```

### CSS

Three rules: `[data-density="silent"]`, `[data-density="center"]`,
and dark-theme overrides. ~25 lines.

---

## What is preserved

- All eight formalized text-witness families (commentary 640 /
  linguistic 560 / manuscript 500 / architecture 480 small-caps
  / ritual 560 / reception 600 / cross-ref 540 / cosmology 620).
- All twelve AO chambers (cosmology, sanctuary, sabbath,
  lineage, covenant, mountain, wisdom, revelation, lament,
  incarnation, resurrection, translation).
- Doré plates (transparent leaf + plaque + monumental).
- v76 vellum + warm ink + dark-absorption shadow.
- v77 ceremonial leaf padding (88/64/104).
- v78 reading choreography (three-tier entry, exit, codex
  memory).
- v79 canonical stratum rubric.
- v80 transmission rubrics per family.
- v81 cosmology cosmogram + cross-reference resonance hairline.
- 12 Atlas Objects preserved.

The geography pass is purely additive to the chapter-heading
register. No prior pass is touched.

---

## Phase coverage (per brief's seven phases)

- Phase 1 (Density Geography) ✓ — three explicit density
  registers
- Phase 2 (Sacred Centers) ✓ — 18 hardcoded canonical centers
  carry lengthened rule
- Phase 5 (Silence as Geography) ✓ — silent chapters become
  wilderness register
- Partial Phase 4 (Archive Topology) — chapter-level density
  emerges; book-level concentration patterns implicit in the
  density walk above
- Partial Phase 6 (Distance Without Mechanics) — depth is
  felt through register variation, never through lockouts or
  progression
- Partial Phase 7 (Codex as World) — the codex now carries
  geographic register; the reader feels regions

Deferred to a future pass:

- **Phase 3 (Remote Witnesses)** — distinguishing fragile /
  remote / near-source records via per-leaf atmospheric
  treatment. Reserved.

---

## Posture

The codex now layers eight constitutional pillars:

1. **Leaf material** (v76 vellum + warm ink + dark absorption)
2. **Folio architecture** (v77 ceremonial padding + staging)
3. **Reading choreography** (v78 three-tier entry + memory)
4. **Canonical orientation** (v79 stratum rubric)
5. **Witness temporality** (v80 transmission rubric per family)
6. **Civilizational inheritance** (v81 cosmogram + xref echo)
7. **Civilizational geography** (v82 density register)
8. **Witness-family constitution** (v74 + v82 family CSS)

The reader walking through the codex now feels:

- *Where the witness lives* (canonical position)
- *What kind of witness this is* (family)
- *How it arrived through time* (transmission rubric)
- *What kind of terrain the chapter is* (density register)
- *How the chamber opens and closes* (choreography)
- *Whether the codex remembers having seen this* (visited trace)

The archive no longer reads as a uniformly accessible codex.
It reads as a civilization with regions, density, remoteness,
and sacred gravity — felt entirely through type, padding, and
the chapter-plate's own register. No maps, no chrome, no
labels.

A preserved civilization with inhabited regions and sacred
depth.
