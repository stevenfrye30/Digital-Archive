# Reading Choreography

*Compiled 2026-05-22, v78. Codex movement — entry, exit, and
quiet memory. Companion to `FOLIO_OBJECT_ARCHITECTURE.md` and
the prior leaf-constitution arc.*

The prior passes gave the leaf its own material identity. This
pass gives the *movement through* the archive its own pacing.
Moving between witnesses must feel ritual rather than
application-like — a museum's handling cadence, not a
software's transition system.

---

## The cadence gradient — entry per kind

Witnesses arrive at three different cadences depending on what
they are. The reader feels the kind before the content loads.

| Kind | Pre-pause | Settle duration | Translate | Easing |
|---|---:|---:|---:|---|
| Text witness (default) | 0 | 0.72 s | 10 px | cubic-bezier(.22,.61,.36,1) |
| AO chamber (originating) | 0.18 s | 0.92 s | 10 px | ease-out |
| AO chamber (echo) | 0 | 0.92 s | 10 px | ease-out |
| Doré plate | **0.32 s** | **1.2 s** | **20 px + scale 0.985→1** | cubic-bezier(.16,.7,.3,1) |

- **Text witnesses** arrive quietly: 0.72 s settle from a 10 px
  rise. Unchanged from v75.
- **AO chambers** earn slightly more breath: 0.92 s settle.
  Originating chambers retain their pre-pause 0.18 s held
  breath (settled in v69's anchor-gravity work).
- **Doré plates** arrive with cathedral pacing: a 0.32 s held
  breath while the chamber settles dark around them, then a
  1.2 s arrival from a deeper 20 px below, with an almost-
  imperceptible scale-up from 0.985 to 1.0. The plate does not
  appear — it *becomes present*.

The plate-specific keyframe `folio-leaf-plate-arrive` exists
just for this. The scale-shift is faint enough to register as
"settling into being" rather than as a zoom transition.

---

## Plate-chamber isolation

When a Doré plate is open in the viewer, the chamber's radial
gradient deepens slightly:

```css
body.viewer-active:has(.folio-leaf[data-kind="plate"]) #object-viewer {
  background: radial-gradient(
    ellipse 75% 80% at center,
    rgba(20, 14, 8, 0.92) 0%,    /* was 32,24,16,0.86 */
    rgba(14, 10, 6, 0.97) 35%,
    rgba(6, 4, 2, 1) 75%,
    rgba(2, 1, 0, 1) 100%
  );
}
```

The chamber is darker, more enclosed, the engraving more
completely held. This is "stronger isolation behavior" for
plates — Doré's cathedral framing earns deeper darkness when
the plate is summoned. Text-witness chambers retain their
existing warm vignette.

The `:has()` selector fires only when a plate is in the
viewer; text witnesses see no change.

---

## Exit ceremony

The viewer's exit transition extends from 0.6 s to 0.9 s:

```css
#object-viewer {
  transition: opacity 0.9s ease-out, visibility 0s linear 0.9s;
}
```

Opening remains at 0.65 s (the brief said exit feels too
abrupt; entry is fine). The chamber now releases the reader
gradually — the dark chamber fades over almost a full second,
the leaf softens with it, the scripture column returns.

The reader feels "returning to the codex" rather than "closing
a modal."

---

## Codex memory — visited-leaf trace

A subtle "manuscript trace" appears when the reader re-encounters
a record they've seen before. The provenance hairline at the
top of the leaf warms by a tiny amount (alpha 0.22 → 0.36).

This matches the existing rail-marker visited treatment:
the manuscript has been touched; it reads as slightly worn-in.
The change is sub-conscious per encounter. Over a long session
the leaf carries the trace of having been seen.

### Implementation

Two helpers added near `_anchorGravity`:

```js
const _RECORD_SEEN_KEY = 'archive:records-seen:v1';
const _recordSeenMem = new Set();

function _hasRecordBeenSeen(recId) {
  // Check in-memory set first, then localStorage if available.
  // Returns true if the record has been summoned this session
  // or in any prior session on this browser.
}

function _markRecordSeen(recId) {
  // Add to both in-memory and localStorage.
  // Falls back gracefully if localStorage is unavailable.
}
```

In `_renderFolioObjectLeaf`, immediately after the gravity
check:

```js
if (rec && rec.id && _hasRecordBeenSeen(rec.id)) {
  leaf.dataset.visited = 'true';
}
if (rec && rec.id) _markRecordSeen(rec.id);
```

The first call sets `data-visited="true"` if the record has
been seen before; the second records this current visit.
First-time encounters do not show the trace; subsequent
encounters do.

### CSS

```css
.folio-leaf[data-visited="true"] .folio-leaf-provenance {
  border-bottom-color: rgba(120, 75, 30, 0.36);
}
```

A single line. The provenance border becomes slightly warmer.

This is the *opposite* of "visited link" web pattern: no
colored text, no marker dot, no notification. A barely-
perceptible warmth in a single hairline — the manuscript
carries the memory of having been touched.

---

## What is preserved

- The 0.72 s settle for text witnesses (v75).
- The 0.18 s pre-pause for originating chambers (v69).
- All eight formalized family registers.
- All twelve AO chamber renderers.
- All compositional architecture from v77 (88/64/104 padding,
  staging breath, ceremonial pacing).
- The vellum parchment + warm ink (v76).
- The dark-absorption shadow stack (v76).
- The 0.65 s opening transition for the viewer.

---

## What is NOT done in this pass

Per the brief, explicitly:

- **No modern animations** — all transitions are simple linear
  or cubic-bezier eases. No spring, no bounce, no parallax.
- **No app-like transitions** — leaf is not a card that flies
  in; it settles from a 10 px rise (or 20 px for plates).
- **No flashy easing** — the easing curves are restrained
  ease-out variants.
- **No theatrical effects** — no particles, no flares, no
  ornaments.
- **No fake textures** — no parchment grain, no aging filters.
- **No gamification** — no badges, no progress bars, no
  notifications.

Everything remains quiet, scholarly, ritual, museum-like.

---

## What is not yet addressed (deferred)

The brief mentioned six phases. This pass directly addresses:

- Phase 1 (Object Entry Choreography) ✓
- Phase 2 (Object Exit Choreography) ✓
- Phase 4 (Doré Ceremoniality) ✓
- Phase 5 (Object Memory) ✓

Deferred to a future pass:

- **Phase 3 (Inter-Object Continuity)** — currently when the
  reader summons a new leaf while another is open, the DOM
  swap is hard. Cross-fading between leaves would require a
  JS sequencing change (render new leaf at opacity 0,
  fade-out old, remove old, fade-in new). Doable but invasive;
  reserved for a focused pass.
- **Phase 6 (Reading Room Atmosphere)** — the reading room
  itself (the scripture pages with no viewer open) could
  benefit from atmospheric refinement, but the most impactful
  reading-flow work is the entry/exit/memory triad above. The
  reading room is already in good shape after v77's leaf-
  architecture pass.

---

## Posture

After v78, the codex's movement carries a different cadence
for each kind of object:

- Text witnesses appear quickly, like a curator quietly
  setting a leaf on the desk.
- AO chambers take more breath, like opening a bespoke
  studied volume.
- Doré plates arrive with cathedral solemnity, the chamber
  darkening around them as they settle.
- Exits unfold over almost a second — gradual release rather
  than modal collapse.
- Re-encountered records carry the trace of having been seen.

The archive no longer feels like clicking between UI
components. It feels like moving through a preserved
intellectual chamber — a museum's handling rhythm rather than
a software's transition system.

The reader does not consciously notice any single change.
Together the changes shift the codex's experiential register
from *application* to *manuscript ritual*.
