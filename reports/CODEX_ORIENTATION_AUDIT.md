# Codex Orientation Audit

*Compiled 2026-05-22, v79. The macro-orientation pass. The
codex's micro-atmosphere reached maturity through v77 (folio
architecture) and v78 (reading choreography); the reader could
feel "this object matters" but not yet "where this object
lives in civilization." This pass builds the first layer of
canonical orientation.*

---

## The macro-orientation problem

A reader opening Genesis 1 felt the leaf's material weight,
the chamber's atmospheric depth, and the witness families'
distinct manuscript-traditions. What they did not feel was
*where in the larger preserved structure* they had arrived.

Genesis 1 read as Genesis 1. Not as the Torah's opening.
Not as the first movement of a massive civilizational corpus.
Not as one chamber among many.

The brief named this: the archive had strong MICRO-atmosphere
but weak MACRO-orientation. The reader could feel "this object
matters" but not "I know where I am in civilization."

---

## The single move

A quiet small-caps italic line beneath the Roman numeral
chapter mark, naming the chapter's canonical position in a
two-segment format: **Macro · Section**.

Examples:

- Genesis 1-11 → `Torah · Primeval History`
- Genesis 12-50 → `Torah · Patriarchal History`
- Exodus 1-18 → `Torah · The Going Out`
- Exodus 19-40 → `Torah · Sinai Covenant`
- Leviticus → `Torah · Priestly Code`
- Numbers → `Torah · Wilderness`
- Deuteronomy → `Torah · Deuteronomy`
- Joshua / Judges / Samuel / Kings / Chronicles / Ezra / Neh
  / Esther / Ruth → `Hebrew Bible · Historical Books`
- Job / Psalms / Proverbs / Ecclesiastes / Song → `Hebrew
  Bible · Wisdom & Hymnody`
- Isaiah / Jeremiah / Lamentations / Ezekiel / Daniel →
  `Hebrew Bible · Latter Prophets`
- Hosea ... Malachi → `Hebrew Bible · The Twelve`
- Matthew / Mark / Luke / John → `New Testament · Gospel`
- Acts → `New Testament · Apostolic Acts`
- Romans / 1-2 Cor / Gal / Eph / Php / Col / 1-2 Thes / 1-2
  Tim / Titus / Philemon → `New Testament · Pauline Letters`
- Hebrews / James / 1-2 Pet / 1-2-3 John / Jude → `New
  Testament · Catholic Letters`
- Revelation → `New Testament · Apocalypse`
- 1-2 Maccabees / 1-2 Esdras → `Deuterocanon · Historical`
- Wisdom / Sirach → `Deuterocanon · Wisdom`
- Tobit / Judith / Greek Esther / Baruch / Song of Three /
  Susanna / Bel & Dragon / Prayer of Manasseh →
  `Deuterocanon · Additions`

---

## Implementation

### Two pieces

1. A single helper function: `_canonicalStratumOf(bookKey, chapterNum)`
   added near the v78 codex-memory helpers. Returns the stratum
   string for any canonical book/chapter pair. Defaults to empty
   string for unknown contexts.

2. A new element in `_buildChapterHeading`: after the Roman
   numeral `<div class="ch-sub">`, append a `<div class="ch-stratum">`
   with the stratum text. Only when the chapter heading is in
   chapter-room mode and stratum is non-empty.

### CSS

```css
.chapter-room-heading .ch-stratum {
  font-family: Georgia, "Palatino Linotype", Palatino, serif;
  font-style: italic;
  font-size: 0.42em;
  font-variant: small-caps;
  letter-spacing: 0.18em;
  color: rgba(110, 75, 35, 0.50);
  margin-top: 22px;
  padding-left: 0.18em;
}
```

- **Italic** — sub-rubric register, distinct from the chapter
  heading's structural type.
- **Small-caps** — civilizational/canonical register, the
  voice used elsewhere in the codex for tradition names.
- **0.42 em** — visibly smaller than the Roman numeral (0.92
  em) and the book name (0.62 em). The stratum is the third
  tier of the heading hierarchy.
- **0.18 em letter-spacing** — matches the existing rubric
  spacing convention; the line breathes.
- **rgba(110, 75, 35, 0.50)** — quiet warm-brown at 50%
  opacity. Reads as stratigraphic context, not as another
  heading.
- **22 px margin-top** — sufficient breath between the Roman
  numeral and the stratum so the heading reads as a single
  three-tier composition, not as two stacked elements.

---

## Heading hierarchy after this pass

```
┌────────────────────────────────────────┐
│                                        │
│              GENESIS                   │ ← book name (0.62em, small-caps)
│                                        │
│               ───                      │ ← centred 44px hairline
│                                        │
│                I                       │ ← Roman numeral (0.92em)
│                                        │
│      TORAH · PRIMEVAL HISTORY          │ ← stratum (0.42em, small-caps italic)
│                                        │
└────────────────────────────────────────┘
```

Three tiers, increasingly small and increasingly soft. The eye
reads down: book → chapter → corpus position. Each line
narrower in presence than the one above. The composition reads
as a single chapter-plate, not as a stack of titles.

---

## What this pass achieves

For the reader:

- **Canonical context** — opening Genesis 1, the reader sees
  "Torah · Primeval History" and quietly knows: this is the
  opening movement of the Torah, in its primeval section. The
  reading is already positioned.
- **Section transitions felt** — moving from Gen 11 (Primeval)
  to Gen 12 (Patriarchal), the stratum line changes. The
  reader's eye registers the shift without prompting.
- **Macro-position across the canon** — opening any book in
  any corpus surfaces its canonical position. Psalm 23 reads
  as "Hebrew Bible · Wisdom & Hymnody." John 1 as "New
  Testament · Gospel." Revelation 4 as "New Testament ·
  Apocalypse."
- **Long-form readiness** — as the archive grows into other
  corpora, this rubric is already in place. The reader
  moving from Genesis to Exodus to Psalms to Revelation is
  always quietly told where they are.

---

## What this pass does NOT do

The brief explicitly forbade:

- **No breadcrumb UI** — the rubric is not clickable; it is
  not navigation; it provides no path back. Position only.
- **No app-navigation language** — no "current book," no
  "current chapter," no "category." The vocabulary is
  manuscript: Torah, Apocalypse, Twelve, Wisdom.
- **No dashboards** — single line of small-caps italic. No
  tree, no sidebar, no menu.
- **No metadata bars** — the stratum is *content*, set as
  type rather than as UI. It belongs to the heading, not to a
  chrome region.
- **No visible database structure** — book codes, schemas,
  IDs are nowhere visible. The reader sees prose, not data.
- **No educational sidebars** — no explanations, no glosses
  on the stratum names. The names speak for themselves to a
  reader who knows; they orient a reader who is learning
  without lecturing.
- **No wiki navigation** — no hover behavior, no "click for
  more about Torah."
- **No section-name fashioning** that privileges one tradition
  over another. Hebrew Bible terminology for the OT corpus
  ("Torah," "The Twelve," "Latter Prophets") respects the
  Jewish canon's native names; New Testament terminology for
  the Christian corpus respects its native names. Both speak
  in their own tradition's voice.

---

## Future passes (deferred)

The brief named further phases. This pass handles Phase 1
(canonical context) and partial Phase 3 (reading room as
civilizational space). Deferred:

- **Phase 2 (Object Positioning / Witness Era Register)** —
  the witness leaf's provenance line could carry quiet
  temporal positioning ("5th c. CE · patristic" for Augustine;
  "19th c. · French Romantic" for Doré; "ancient core" for
  bĕrēʾšît). Doable but requires editorial care to avoid
  educational labeling. The existing tradition strings already
  imply era; explicit period markers would either help
  orient or feel like footnotes. Deferred for editorial
  consideration.
- **Phase 4 (Long-form orientation)** — movement through
  books / epochs / traditions / interpretive history. The
  v79 stratum rubric is the first step; further orientation
  layers (e.g., a Genesis-wide "where am I in the Torah's
  arc" indicator, a Twelve-wide minor prophets mini-map)
  would require richer per-book metadata.
- **Phase 5 (Non-digital navigation)** — the existing
  prev-next chapter rubric and book selector are already
  manuscriptal. Major navigation redesign deferred — the
  current chrome is acceptable.

---

## Posture

The codex now carries a single quiet line that tells the
reader, on every chapter-plate, where they are in the larger
preserved structure. The reader opens Genesis 1 and silently
receives: "this is the opening of the Torah's primeval
history." The reader opens Revelation 4 and silently receives:
"this is in the apocalyptic register of the New Testament."

The line is small. The line is restrained. The line never
asks for attention. But over a session, the reader builds an
implicit map of the canonical structure — "I have moved
through the Torah's primeval section, into the patriarchal,
toward the Sinai covenant; later I will move into Wisdom &
Hymnody and the Twelve and the Gospel."

Civilizational position, expressed in a single line of
small-caps italic. The archive begins to feel less like a
site containing texts and more like a preserved civilization
arranged into chambers.
