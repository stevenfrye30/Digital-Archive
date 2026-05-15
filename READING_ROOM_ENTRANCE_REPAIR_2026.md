# READING_ROOM_ENTRANCE_REPAIR_2026

Brief repair note. The Reading Room card on the welcome page was
nonfunctional. Clicking it did nothing.

**Date:** 2026-05-15.

---

## What was broken

The Reading Room card was a plain `<div>` with `aria-current="page"`:

```html
<div class="home-path home-path-current" aria-current="page">
  <span class="home-path-label">Reading Room</span>
  <span class="home-path-sub">Read the texts directly.</span>
</div>
```

It had:
- no `href`
- no `onclick`
- no event listener
- no `role="button"`
- no `tabindex`

The card was originally added (May 15 entrance clarification) as a
*visual marker* — "you are here; the four category cards below are
how you enter." `aria-current="page"` signaled this to assistive
tech. But on a real device, the card *looks* tappable: it has the
same warm-tan border, the same padding, the same proportions as the
Atlas card next to it, which *is* a functioning `<a href>`. Readers
tapped Reading Room expecting to enter, and nothing happened.

The Atlas card was unaffected (it remained a functioning link).

---

## What was changed

Three small edits to `03_web_app/index.html`.

### 1. Markup

The `<div>` became a `<button>` with an id:

```html
<button type="button" id="home-path-reading-room"
        class="home-path home-path-current" aria-current="page">
  <span class="home-path-label">Reading Room</span>
  <span class="home-path-sub">Read the texts directly.</span>
</button>
```

Keyboard activation (Enter / Space) works through the native button
semantics. `aria-current="page"` is preserved — this *is* the
current section.

### 2. CSS

Removed `cursor: default` from `.home-path-current` (which was
suppressing the pointer cursor on hover). Added a subtle hover
state (darker tan) so the card visibly responds to interaction.
Added `button.home-path { font: inherit; text-align: left; width:
100%; }` to remove default button chrome so the button shares the
visual register of the Atlas `<a>` card.

### 3. JS

A small IIFE wires the click:

```js
(function wireReadingRoomEntrance() {
  const btn = document.getElementById('home-path-reading-room');
  if (!btn) return;
  const enter = () => {
    // If the reader has a most-recent text (Continue Reading is
    // shown), tapping the card resumes that reading — the most
    // direct meaning of "enter the Reading Room reader environment."
    const continuePanel = document.getElementById('welcome-continue');
    const continueBtn   = document.getElementById('continue-btn');
    const continueVisible = continuePanel &&
      window.getComputedStyle(continuePanel).display !== 'none' &&
      continueBtn;
    if (continueVisible) {
      continueBtn.click();
      return;
    }
    // Otherwise the four category cards below are the entry points;
    // smooth-scrolling them into focus makes that visible.
    const categories = document.getElementById('home-categories');
    if (categories) {
      categories.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };
  btn.addEventListener('click', enter);
})();
```

The handler is conservative — it reuses the existing
`#continue-btn` (the Continue Reading button) and the existing
`#home-categories` container. No new flow, no new state.

---

## Behavior, by case

| Reader | Click Reading Room |
|---|---|
| Returning visitor with a recent text (`da-last` exists) | Resumes the most-recent reading — same action as tapping the Continue Reading button. The welcome hides, the running header / chrome appears, and the previously-read passage scrolls into view. |
| Fresh visitor (no `da-last`) on mobile | The four category cards smooth-scroll into the center of the viewport. The reader sees the entry points clearly. |
| Fresh visitor on desktop | Same scroll-into-view (no-op when the categories are already in view; harmless). |
| Keyboard user | The card receives focus naturally as a `<button>` in tab order. Enter / Space activates it. |

Verified locally at 390×844 and 1280×900 viewports.

---

## What was deliberately not done

- **No redesign.** The card's visual register is unchanged.
- **No new flow.** No new browse mode, no new route, no new state
  surface. The handler delegates to existing affordances.
- **No href change on the Atlas card.** It worked; left alone.
- **No removal of `aria-current="page"`.** The card is still the
  current section semantically; it just now also acts on click.

---

## Files changed

- `03_web_app/index.html` — three small edits as above.

No data files, no scripts, no other surfaces.
