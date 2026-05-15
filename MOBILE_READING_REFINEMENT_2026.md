# MOBILE_READING_REFINEMENT_2026

A small architectural act of respect toward the text itself.

**Date:** 2026-05-15.
**Scope:** The Reading Room on viewports ≤ 720px.
**Trigger:** Inhabitation surfaced that, on mobile, too much vertical
space sat above the primary text once a passage was opened.
**Result:** On a 390×844 viewport, the chrome above the first passage
shrinks from ~155–192px to ~122–151px. The text now occupies 79–86%
of the viewport on entry, up from ~73–77%. The Reading Room remains
plain HTML, plain CSS, plain DOM. No framework. No SPA. No sticky
toolbar. No floating action button.

This is a repair, not a redesign.

---

## 1. Why this matters

The archive's first constitutional principle is that the primary text
is sovereign (`COMMENTARY_CONSTITUTION.md` §7, `STATE_OF_THE_ARCHIVE_2026.md`
§3.1). On desktop, the Reading Room has honored this for some time:
the text occupies most of the viewport, with chrome sitting calmly
above it.

On mobile, the same chrome — info-bar, translation-bar, nav-bar, the
"About this text" pill, the chapter heading — was claiming roughly a
quarter of the viewport before the first passage even appeared.
Inhabitation revealed that this violated text sovereignty
unintentionally: the primary text was visible but not dominant.

The refinement is narrow. It changes only mobile presentation. The
canonical data is untouched. The desktop reading experience is
unchanged. No new feature, no new dependency, no new pattern.

---

## 2. What changed

Five small changes. All in `03_web_app/index.html`.

### 2.1 Typographic controls behind a quiet disclosure

The font / size / spacing / background / text-color controls were
wrapped in `<details class="display-options"><summary>Display</summary>…</details>`.

- On desktop: the `<details>` element is `display: contents`, so it
  is structurally transparent — the controls flow inline in
  `#controls` as before. The `<summary>` is `display: none`. The
  desktop reading experience is byte-identical.
- On mobile: the `<details>` becomes a real block. The `<summary>`
  appears as a small pill labeled "Display ▾". The typographic
  controls are hidden by default. Tapping the pill reveals them.

A 9-line `matchMedia` bridge synchronizes the `open` attribute with
the breakpoint: open on desktop, closed on mobile. The user can
freely open or close on mobile thereafter.

This pattern — native `<details>` with `display: contents` on the
larger viewport and a real disclosure on the smaller — is the only
"mobile-specific" interaction the refinement introduces. It is a
deliberate use of the platform's own machinery, not a custom
component.

### 2.2 The "About this text" pill became quieter

On mobile, the pill loses its box-shadow, drops to 11px font, 3×10px
padding, font-weight 500. Its info icon shrinks from 18×18px to
14×14px. The pill still functions identically; it simply weighs less
visually.

Net height reduction: ~26px.

### 2.3 The chapter-prev/next bar slimmed

On mobile, `#nav-bar` padding dropped from 6×20px to 3×12px; buttons
to 11px / 3×9px padding. The bar is still a single row of canonical
structure navigation, just narrower.

Net height reduction: ~7px.

### 2.4 Translation switcher slimmed

On mobile, `#translation-bar` padding dropped from 6×20px to 3×12px;
select dropped to 11px font with 2×6px padding. The bar is still
present and functional for multi-translation texts.

Net height reduction: ~8px.

### 2.5 Reader top-padding and chapter heading tightened

`#reader` top padding on mobile: 24px → 12px.
`.chapter-heading` on mobile: font-size 1.3em → 1.15em; padding
24/20 → 12/12.

The chapter heading remains the heading of canonical structure; it
is not collapsed or hidden. It simply takes less vertical weight on
small screens, where every pixel counts.

Net combined reduction: ~17px.

### 2.6 A trailing `@media` block fixes a pre-existing cascade order

While implementing, I found that several mobile rules already in the
file (at the original `@media (max-width: 720px)` block, line ~1280)
were being silently overridden by their desktop counterparts defined
later in the stylesheet (e.g., `#info-bar` at line ~2008,
`#nav-bar` at line ~2038, `#translation-bar` at line ~2004).
Because both rules had equal specificity, the later un-prefixed
desktop rule won.

The refinement adds a small `@media (max-width: 720px)` block at the
end of the stylesheet — after every desktop element definition —
that reaffirms the mobile chrome rules. This is a cascade-order
correction, not a new pattern; it makes the file's mobile intent
actually apply.

---

## 3. What was preserved

By design and explicit decision:

- **Passage text rendering.** Untouched.
- **Passage numbering and reference labels.** Untouched.
- **Chapter heading as canonical structure.** Smaller in weight but
  still present, still visually distinct.
- **Translation switcher.** Still visible on multi-translation
  texts. The reader can still switch translations and enter compare
  mode without expanding any disclosure.
- **Chapter prev/next navigation.** Still visible; canonical
  structure navigation is sovereign.
- **The three CSS registers (apparatus, footnote, annotation).**
  Untouched. Provenance separation is preserved at full fidelity.
- **The honest-gap apparatus diagnostic.** Untouched. Clicking an
  unresolvable `[*N]` still opens the warm-tan dashed-border
  diagnostic from `APPARATUS_PROPAGATION_REPAIR_2026.md`.
- **The desktop reading experience.** Byte-identical CSS-wise (via
  `display: contents`).
- **localStorage state.** Untouched. No new keys, no new schema.
- **Plain HTML resilience.** No framework. No build pipeline. No new
  dependency.

---

## 4. What was rejected

By explicit decision, the following were considered and not done.

- **A hamburger menu.** Forbidden by the brief; would have hidden
  too much behind a single off-canvas affordance.
- **A slide-out drawer.** Forbidden by the brief; introduces an
  app-paradigm interaction.
- **A sticky / floating toolbar that hides on scroll.** Forbidden
  by the brief; introduces motion under the reader's attention.
- **A "reader mode" toggle that swaps in a maximally minimal
  layout.** Would have been a parallel surface, not a refinement.
- **Hiding the translation-bar inside the meta panel.** Considered;
  rejected because translation switching is meaningful structural
  movement, not metadata.
- **Hiding the chapter-prev/next nav-bar.** Considered; rejected
  because it is canonical structure navigation, not chrome.
- **Removing the typographic controls entirely on mobile.**
  Considered; rejected because some readers genuinely benefit from
  font-size and spacing controls on small screens. The disclosure
  preserves access without enforcing presence.
- **Animating the disclosure expansion.** The brief asks for "no
  animation or extremely subtle animation." The disclosure uses the
  browser's native `<details>` toggling with no transition.
- **Adding any new JavaScript pattern, framework, or library.**
  The bridge is 9 lines of vanilla matchMedia plus a feature-detect
  fallback for older browsers.

---

## 5. Measured effect

Tested at 390×844 viewport (iPhone 12/13/14), with the local static
server. Four texts inhabited; chrome height above first passage
measured directly from the rendered DOM via Playwright.

| Text | Before | After | Δ | After % of viewport |
|---|---:|---:|---:|---:|
| Genesis 1:1 (Bible ASV — multi-translation) | 192px | 151px | −41px | 18% |
| Apannaka 1.1 (Jātaka Vol 1 — multi-translation, two-line heading) | — | 176px | — | 21% |
| Republic 10.1 (Plato — single translation) | — | 122px | — | 14% |
| Katha Upaniṣad 5.80 (with apparatus) | 155px | 122px | −33px | 14% |

Above-text chrome reduced ~20–22% on the two before/after cases.
Apannaka measured higher because its chapter heading wraps to two
lines ("Chapter 1 — APANNAKA-JATAKA") — that is canonical content
length, not chrome.

Where measured, screenshots in
`03_web_app/reports/mobile_inhabitation/*.png` (also at
`logs/reports/mobile_inhabitation/` mirror) confirm that the text
visibly dominates the viewport on entry. The chrome at the top is a
quiet band; below it the passages rise into the reader's primary
attention.

---

## 6. Atmosphere

The brief asked for the surface to feel "more like a quiet pocket
reading chamber, a text-forward manuscript space, a contemplative
surface where the interface recedes naturally."

Reading the four test passages on a mobile viewport, with the
refinement applied:

- **Genesis.** The Hebrew Bible's opening verses begin near the top
  of the viewport. The "Bible — ASV" translation pill is small. The
  chapter heading "Genesis" is dignified but quiet. The text is the
  obvious primary object.
- **Apannaka-jātaka.** The Pāli birth-story opens at the top. The
  bracketed `[95.]` page marker (preserved verbatim from Chalmers
  1895) is visible in the body, where it belongs as part of the
  canonical text. No clutter.
- **Republic 10.1.** Single translation, so no translation-bar.
  Chrome reduces to two slim bands plus the chapter heading. The
  text claims 86% of the viewport. Sustained scrolling feels calmer
  than before.
- **Katha Upaniṣad 5.80.** Apparatus markers `[*1]` and `[*2]`
  appear in the passage body as small superscript markers. The text
  dominates. Clicking the apparatus marker resolves to Müller's
  footnote (the May 14 propagation repair is in effect). Two voices
  in the room; the canon's voice is louder.

The interface does not disappear. It recedes. That is the correct
distinction.

---

## 7. What this is not

- This is not a reader rewrite. The Reading Room remains
  `index.html`, a single plain-HTML file.
- This is not a mobile-app paradigm. There is no off-canvas, no
  drawer, no FAB, no sticky bar, no tab system.
- This is not a generalized responsive redesign. The desktop
  rendering is unchanged at every breakpoint above 720px.
- This is not an optimization pass. No telemetry was added. No
  performance metric was instrumented. The single end-user-visible
  goal was: read the text, with less chrome above it.

---

## 8. Constitutional compatibility, re-tested

| Commitment | Result |
|---|---|
| Primary text sovereignty | Strengthened: text now occupies 79–86% of mobile viewport on entry, up from ~73–77%. |
| Bare-canon access | Unchanged. The passage record is rendered as before. |
| Provenance separation | Unchanged. Three CSS registers preserved. |
| Honest-gap rendering | Unchanged. Apparatus diagnostic still resolves on click. |
| Plain-HTML resilience | Unchanged. No framework added. No build pipeline. The added JS is 9 lines of vanilla matchMedia. |
| No telemetry, no analytics | Unchanged. None added. |
| No reader-engagement patterns | Unchanged. No streaks, no progress quotas, no recommendation surfaces. |

---

## 9. Files changed

- `03_web_app/index.html`:
  - HTML: `<details class="display-options">` wrapper around the five
    typographic ctrl-groups (~30-line restructure, no new elements
    beyond the wrapper).
  - CSS: ~30 lines added to the existing mobile `@media` block;
    ~40-line trailing `@media (max-width: 720px)` block; ~35-line
    `details.display-options` rule.
  - JS: 9-line `matchMedia` bridge to sync `open` to breakpoint.

- New: `03_web_app/tools/test_mobile_inhabitation.py` — Playwright
  script that measures chrome above the first passage at a 390×844
  viewport across the four test texts. Produces screenshots and a
  metrics JSON. Read-only; not in any production path.

- New: `MOBILE_READING_REFINEMENT_2026.md` (this document) at the
  workspace root.

- Generated: `03_web_app/reports/mobile_inhabitation/` —
  per-passage portrait screenshots and `metrics.json`.

No data files changed. No canonical archive touched.

---

## 10. Did the atmosphere improve

Yes, in the specific and measurable sense intended.

The reading surface is now more *text-forward*. On entry, the first
passage is closer to the viewport top. Sustained scrolling feels
calmer because each passage rises into the reader's attention sooner
after the previous one. The "About this text" pill is no longer the
loudest object on the page; it is a small affordance that recedes.

The Reading Room still feels archival rather than appified. There
are no animations, no sticky bars, no floating affordances, no
modern-SaaS rhythms. The discipline is restraint; the discipline
held.

The refinement was small. The constitutional cost of doing it was
zero. The constitutional benefit was the recovery of a guarantee the
mobile surface had been silently violating.

---

## 11. Reading order, if you arrive cold

1. This document.
2. `READING_ROOM_CONSTITUTIONAL_AUDIT_2026.md` §4.2 — the original
   "single-layer interpretation" mismatch this work also touches.
3. The diff to `03_web_app/index.html` — easier to read than
   summarize.
4. `03_web_app/reports/mobile_inhabitation/metrics.json` and the
   four `.png` files — the actual visible result.

If you arrive cold a year from now and the metrics look different,
re-run `python 03_web_app/tools/test_mobile_inhabitation.py` from
the workspace root (with the local server on :8765). The script
exists for re-verification, not for ongoing CI.
