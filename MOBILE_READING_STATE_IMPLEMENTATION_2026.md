# MOBILE_READING_STATE_IMPLEMENTATION_2026

Implementation of the mobile reading-state proposal from
`READING_STATE_PROPOSAL_2026.md`. Approach C: minimal restructuring
and meta-panel expansion.

**Date:** 2026-05-15.
**Result, in one sentence:** On mobile (≤720px), the Reading Room
consolidates the previous seven-band chrome stack into a single
running header — chapter title, prev/next, position+translation
subtitle, and an `ⓘ` retrieval handle — while the receded browsing
affordances (translation switcher, in-text search, Compare,
Contents, Home, Display) relocate via JS into the existing
`#text-meta` panel, which opens inline on demand.

Measured: the first passage now begins at y = 63–94px from the
viewport top (depending on chapter-title length), down from
y = 151–192px after the May-15-morning refinement and y = 155–280px
before any refinement. The text occupies 89–92.5% of a 390×844
viewport on entry.

Desktop is unchanged. Canonical data is untouched. The URL scheme,
the routing, the export pipeline, the apparatus pipeline, and the
permanence resolver are all unmodified.

---

## 1. The diagnosis this addresses

`READING_STATE_PROPOSAL_2026.md` §1 named the problem: on the actual
phone (IMG_1390), the reading view stacked seven chrome bands above
the text — controls (Home/Contents/Display/chapter-selector/search),
info-bar (About pill), translation-bar (switcher + Compare), and
nav-bar (chapter prev/next) — followed by an in-passage chapter
heading that duplicated the nav-bar's chapter label. The text never
dominated the viewport.

The constitutional problem was not that any band was too tall but
that there were too many bands. Desktop can sustain simultaneous
layers. Mobile cannot.

The fix: on mobile, *commit to the reading state*. Browsing
affordances recede into a retrievable panel. The running header
carries only canonical structure (chapter identity + prev/next) and
one path to the panel.

---

## 2. What changed

### 2.1 The consolidated mobile running header

The existing `#nav-bar` was repurposed. On mobile it now displays a
single row containing:

- `◀` (chapter previous, slim chevron)
- The chapter title — centered, Georgia serif, ~15px, with a small
  `▾` indicator when a chapter picker is available. Tapping the
  title opens the native chapter picker (the existing `<select
  id="ctrl-book">`, relocated into `#nav-location` and positioned
  invisibly on top of it).
- A small italic subtitle line beneath the title:
  `<position> · <translation short-label>` —
  e.g. *"1 of 66 · ASV"*, *"5 of 6 · Max Müller"*.
- `▶` (chapter next, slim chevron)
- `ⓘ` (metadata retrieval — opens the inline `#text-meta` panel)

All five tap targets are visible inline. None hides behind a menu.
Total nav-bar height: 55px for short chapter titles, 67–86px for
titles or subtitles that wrap.

The HTML change inside `#nav-bar`:

- `#nav-location` was given an inner `.nav-location-label` span. The
  existing `updateNav()` function now writes the chapter label into
  the inner span, leaving siblings of `.nav-location-label` (like
  the relocated `#ctrl-book-group`) intact. This is the fix for a
  subtle bug discovered during implementation: the prior code used
  `$navLocation.textContent = …`, which wiped any child elements,
  including the chapter selector my relocation logic had moved in.
- The chapter label now has two spans: `.nav-label-chapter` (always
  shown) and `.nav-label-position` (hidden on mobile because the
  subtitle carries the position already).
- New `#nav-subtitle` element (hidden on desktop, populated on
  mobile by `_updateMobileNavSubtitle()`).
- New `#nav-meta-toggle` button (hidden on desktop, visible on
  mobile, wired to the same toggle action as the existing
  `#meta-toggle` pill).

### 2.2 Receded affordances inside the meta panel

Four element groups relocate via JS at the mobile breakpoint:

| Element | Desktop parent | Mobile parent |
|---|---|---|
| `#ctrl-book-group` (chapter picker) | `#controls` | `#nav-location` |
| `#translation-bar` (translation switcher + Compare) | `#panel` | `#text-meta` |
| `#ctrl-search-group` (in-text search) | `#controls` | `#text-meta` |
| `details.display-options` (typography controls) | `#controls` | `#text-meta` |

These are *the same DOM elements*, not duplicates. Event handlers,
form state, and identity are preserved through the move. The
function `setupMobileReadingState()` performs the moves at page
load and re-applies them on any breakpoint change via
`matchMedia('(max-width: 720px)').addEventListener('change', …)`.

The meta panel also gained a new `#meta-mobile-actions` section
containing `← Contents` and `← Home` buttons. These exist in the
HTML always but are `display: none` on desktop (where their function
is already carried by the visible `#controls` Home/Contents buttons).
The `Contents` button is dynamically hidden when `ctrl-contents` is
not currently active (e.g., before a text is loaded).

Each relocated affordance gets a small wrapper-styled section header
on mobile (italic small-caps "BIBLE —", "SEARCH") so the panel
reads as a labeled list rather than a wall of inputs.

### 2.3 In-passage chapter heading suppressed on mobile

`.chapter-heading` is `display: none` on mobile only. The canonical
chapter identity is preserved through the running header. The large
decorative heading inside `#passages` was duplicating the same
content; on a small viewport that duplication was visible chrome,
not visible content.

Desktop retains the heading.

### 2.4 Other chrome bars hidden on mobile

`#controls`, `#info-bar`, and `#translation-bar` are `display: none
!important` on mobile. Their functions live in the running header
(`ⓘ`) and in the relocated affordances inside the meta panel.

### 2.5 Welcome-state regressions repaired

Two real bugs visible in IMG_1391 were fixed in the same change:

- **The translation-bar persisted on the welcome page after a
  reading session.** The `browseHome()` function looked for
  `getElementById('tr-bar')` — an element id that never existed.
  The actual element is `#translation-bar`. The corrected lookup
  now properly hides the bar when returning to the welcome.
- **The recent-reads panel overlapped the home title and category
  cards on mobile.** Root cause: `#home-recent-panel` was a sibling
  of `#welcome-home` inside `#welcome`. With `position: static` on
  mobile (correct rule, present), the panel fell into the normal
  block flow of `#welcome`, but `#welcome-home` is `position:
  absolute inset: 0` — taken out of flow — so the panel appeared at
  top of `#welcome` *overlapping* the absolutely-positioned
  welcome-home below it. Fix: move `#home-recent-panel` (and
  `#welcome-search`) inside `#welcome-home`, so they participate
  in the flex column on mobile. Desktop positioning is unchanged
  because `#welcome-home` is itself the absolute-positioned
  containing block.

A subtle structural bug was introduced during this fix (one closing
`</div>` was lost, which caused `#welcome` to never close and so
all subsequent elements — `#browse`, `#text-cover`, `#passages` —
became nested inside `#welcome`; setting `display: none` on
`#welcome` then silently hid the text during reading). It was caught
during verification and corrected.

---

## 3. Measured effect

Tested at 390×844 viewport (iPhone 12-class) via Playwright. Single
running header band, all four target texts.

| Text | Nav height | First passage y | % of viewport above text |
|---|---:|---:|---:|
| Genesis 1:1 (ASV, 66 books) | 55px | 63px | 7.5% |
| Apannaka 1.1 (Chalmers, 149 tales — chapter title wraps) | 86px | 94px | 11.1% |
| Republic 10.1 (Jowett, 10 books — subtitle wraps) | 67px | 75px | 8.9% |
| Katha Upaniṣad 5.80 (Müller, with apparatus) | 67px | 75px | 8.9% |

Compared to before:

- May-15-morning refinement: y = 122–176px (14–21% of viewport)
- Original state: y = 155–280px (18–33% of viewport, varying based
  on whether the controls bar was visible)
- After this change: y = 63–94px (7.5–11.1% of viewport)

The text now occupies 88.9–92.5% of the viewport on entry. The
single chrome band reads as a running header — the printed-book
posture the proposal aimed for.

Apparatus markers (`[*N]`) still resolve to Müller's footnotes via
the May-14 propagation repair; clicking `[*1]` in Katha 5.80 still
opens the warm-tan apparatus body inline below the passage.

---

## 4. What was preserved

- **Passage text rendering.** Identical at the data layer.
- **Passage numbering / refs.** Untouched.
- **Canonical chapter identity.** Now in the running header rather
  than duplicated in a decorative heading. Still visible, still
  canonical.
- **Chapter sequential navigation.** Prev/next, smaller and
  chevron-only on mobile, full on desktop.
- **Chapter random-access.** The existing `<select id="ctrl-book">`
  was relocated; tapping the chapter title opens the native picker.
- **Translation switcher.** Same `<select>` element, same event
  handler — moved inside `#text-meta` on mobile.
- **Compare mode.** Same button, same handler — accompanies the
  translation switcher in the meta panel.
- **In-text search.** Same `<input>` and arrow buttons, relocated.
- **Display controls (font / size / spacing / colors).** Same
  `<details>` disclosure, relocated.
- **Home and Contents navigation.** Original `onclick="browseHome()"`
  and `backToContents()` paths preserved; mobile gets dedicated
  buttons inside the meta panel that call the same functions.
- **Three CSS registers** (apparatus / footnote / annotation).
  Untouched.
- **Honest-gap apparatus diagnostic.** Untouched.
- **Plain-HTML resilience.** No framework. No build pipeline. No
  new dependency. The only JS additions are vanilla matchMedia
  bridges and DOM relocation logic.
- **Desktop reading experience.** Byte-identical (all changes live
  inside `@media (max-width: 720px)` except the `nav-location` HTML
  refactor, which is invisible on desktop because
  `.nav-label-position` shows there and `.nav-location-label`
  carries the text directly).

---

## 5. What was explicitly rejected

By the brief's prohibitions, all upheld:

- No SPA migration. The Reading Room remains plain HTML / plain
  CSS / plain DOM.
- No framework adoption.
- No hamburger menu — every affordance in the running header is
  visible inline; the meta panel opens inline below, not from
  off-canvas.
- No drawer / modal / overlay system.
- No sticky toolbar. The running header is just the top of the
  page; it scrolls with content.
- No floating action button.
- No animation. The meta panel toggles via `style.display`;
  nothing fades, slides, or floats.
- No telemetry, no analytics, no recommendation system, no
  engagement logic.

---

## 6. Compromises and tradeoffs

These are the honest constraints under which the implementation
landed.

### 6.1 The meta panel opens *above* the running header

The `#text-meta` panel's DOM position is between `#info-bar` and
`#translation-bar` in `#panel`. On desktop, where info-bar and
translation-bar are both visible above the nav-bar, the meta panel
opens between them — natural. On mobile, info-bar and
translation-bar are hidden, but the meta panel still sits *above*
the running header in document order. So tapping `ⓘ` expands the
panel above, pushing the running header (and the text below it)
downward.

This works — the panel is fully visible, the running header and
text scroll into view by scrolling down — but the reader does
briefly see the metadata panel rather than the text continuing
right where they were. A future refinement could move the panel
below the running header on mobile via additional DOM
restructuring; the current placement is acceptable as a v1.

### 6.2 The chapter picker is the existing native `<select>`

iOS native `<select>` UI is a wheel picker, which some readers
dislike. Using the native control was chosen for accessibility,
forward compatibility, and zero-JS-state. A future refinement
could replace it with a small inline overlay list of chapters; for
now, the native picker is the most resilient choice.

### 6.3 Long chapter titles wrap

The chapter title in the running header can wrap to two lines
(e.g., "Chapter 1 — APANNAKA-JATAKA"), and the subtitle can also
wrap (e.g., "1 of 149 · Robert Chalmers"). When both wrap, the
running header is taller (~86px instead of 55px). This is
acceptable — the title is canonical content, and the alternative
(truncation) would hide canonical structure. The proposal explicitly
acknowledged this in §10.

### 6.4 Compare mode on a 390px viewport is cramped

The Compare affordance was relocated alongside the translation
switcher. Tapping Compare opens a second translation in a
side-by-side column. At 390px width, side-by-side text is narrow.
This is a pre-existing constraint; the implementation neither
worsens nor improves it. Compare mode plausibly remains a
desktop-primary feature.

### 6.5 Translation switching is two taps on mobile

Tap `ⓘ`, then tap the translation `<select>`. Two taps for an
action a reader performs rarely during a session. The proposal's
§14 framed this as "acceptable for actions a reader takes a handful
of times in a session." It remains so.

### 6.6 Reading-state DOM relocation depends on JS

The mobile reading state requires JS for the relocation to apply.
With JS disabled, the desktop chrome stack would render on mobile —
not catastrophic (the page would still function), but the mobile
reading-state benefits would not appear. This matches the existing
constraint that the Reading Room requires JS overall (a known
tension recorded in `COMMENTARY_PROTOTYPE_2026.md`).

---

## 7. What remains uncertain

- Whether the running header's font sizing is right for actual
  phone reading (Georgia 15px serif title, 10.5px italic subtitle).
  Sitting with the surface for a week or two will refine this.
- Whether the `▾` picker indicator on the chapter title is the
  right discovery affordance, or whether a more explicit "Chapter ▾"
  framing would help first-time readers.
- Whether the meta panel's section headers ("BIBLE —", "SEARCH",
  italic uppercase small text) are too quiet or correctly quiet.
- Whether the panel's above-running-header opening is acceptable in
  practice or whether the §6.1 refinement should be pursued.
- Whether flat-hierarchy texts (Crito: 103 sequential passages, no
  chapter structure) should display a different running-header shape
  — currently they show "103 passages" as the label, which is
  meaningful but not as natural as a chapter title.
- Whether the chapter random-access affordance (tap title to open
  picker) should be enabled on flat-hierarchy texts where there are
  no chapters to pick.

These are not blockers. They are the kind of question that sustained
inhabitation will answer.

---

## 8. Atmosphere assessment

The brief asked: did the atmosphere improve?

Yes, in the specific sense intended.

The mobile Reading Room now feels like a reading surface. The
running header reads as a chapter heading — chapter title centered,
serif, with small navigation chevrons and a quiet `ⓘ`. The reader
is not greeted by seven rows of chrome but by one. The text begins
within 63–94px of the viewport top. There is no app-toolbar feel,
no floating affordance, no menu drawer. The pacing is calm.

Open the `ⓘ` panel and the affordances are there — translation
switcher, search, Contents, Home, Display — labeled, restrained,
inline. Close the panel and the reading surface returns. The
distinction between *browsing the archive* and *reading inside it*
is now visible to the reader, on a phone, without saying so.

The literary register holds. The archival register holds. Plain
HTML still wins.

---

## 9. Files changed

- `03_web_app/index.html`:
  - HTML: `#nav-bar` gains `#nav-subtitle`, `#nav-meta-toggle`,
    and an inner `.nav-location-label` span; `#text-meta` gains
    `#meta-mobile-actions` with Contents/Home buttons;
    `#home-recent-panel` and `#welcome-search` move inside
    `#welcome-home`.
  - CSS: a substantial new `@media (max-width: 720px)` block at the
    end of the stylesheet (hides receded bars, restyles the running
    header, styles the relocated affordances inside the meta panel,
    styles the Home/Contents buttons); a `@media (min-width: 721px)`
    block wraps the mobile-only-element hides so they don't
    override the mobile rules.
  - JS: a `setupMobileReadingState()` IIFE performs the relocation
    moves with idempotent breakpoint application; `updateNav()`
    writes to the inner label span and dispatches a
    `reading-state:should-refresh` event; `_updateMobileNavSubtitle()`
    composes the subtitle line; `browseHome()` correctly hides
    `#translation-bar` (the prior code looked for `tr-bar`, which
    never existed); the in-passage `.chapter-heading` is still
    created in `enterReading()` (CSS suppresses it on mobile).

- New: `03_web_app/reports/mobile_inhabitation/reading-state-*.png`
  — screenshots of the four target texts in reading state plus
  meta-open and welcome-with-recents states.

- New: `MOBILE_READING_STATE_IMPLEMENTATION_2026.md` (this
  document).

No canonical data changed. No new deploy data files. No new tools
(the existing `tools/test_mobile_inhabitation.py` continues to
serve re-verification).

---

## 10. Re-verification

```
# Static server on :8765
python -X utf8 -m http.server 8765 -d 03_web_app

# Re-run mobile inhabitation
python -X utf8 03_web_app/tools/test_mobile_inhabitation.py
```

Expected: four screenshots, single-row running header per text,
text begins at y = 63–94px depending on chapter-title length.

---

## 11. What this implementation is not

- It is not a Reading Room rewrite.
- It is not a separate "mobile reader."
- It is not a feature.
- It is not appification.
- It does not introduce a "reader mode" toggle. The reading state
  is what the page naturally *is* on a small viewport once a text
  is open — not a mode the reader selects.
- It does not change the URL, the routing, the data shape, the
  apparatus pipeline, the resolver contract, or any constitutional
  document.

---

## 12. Reading order for future stewards

1. This document.
2. `READING_STATE_PROPOSAL_2026.md` for the architectural rationale.
3. The diff to `03_web_app/index.html` — search for `@media
   (max-width: 720px)` near the end of the stylesheet, and for the
   IIFE `setupMobileReadingState`. The full mobile change lives in
   those two places.
4. `03_web_app/reports/mobile_inhabitation/reading-state-*.png` —
   the actual visible result.
5. If you arrive a year from now and the chrome has crept back, the
   thing to check is whether new affordances added to `#controls`
   or `#info-bar` have been correspondingly relocated for mobile.
   The pattern from §2.2 generalizes.

The text remains the point. The disposition of furniture in the
room around it is now, on mobile, a single quiet shelf above it.
