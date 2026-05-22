"""v78 — Reading Choreography verification.

Verifies the four-move pass per READING_CHOREOGRAPHY.md:

  Move 1 (Entry):
    · AO chambers: animation-duration 0.92s (was 0.72s)
    · Doré plates: custom folio-leaf-plate-arrive animation,
      1.2s duration, 0.32s delay, translateY 20px + scale 0.985

  Move 2 (Exit):
    · #object-viewer transition-duration 0.6s → 0.9s

  Move 3 (Plate-chamber isolation):
    · :has() selector deepens chamber when plate is open

  Move 4 (Codex memory):
    · _hasRecordBeenSeen / _markRecordSeen helpers
    · Leaf gets data-visited="true" on re-encounter
    · Provenance hairline warms via CSS

No regressions: text-witness leaves still 0.72s settle,
formalized families preserved, AO inventory == 12, Doré
preserved (now ceremonial-entry, was sudden).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


def open_leaf(page, pid, rec_id, *, reset_seen=False):
    page.goto(
        f"http://localhost:8765/index.html?text=bible_kjv.json&p={pid}",
        wait_until="networkidle",
    )
    page.wait_for_function(
        "typeof currentData === 'object' && currentData && currentData.passages",
        timeout=15000,
    )
    page.wait_for_timeout(700)
    page.evaluate("() => localStorage.removeItem('atlas:encounters:v1')")
    if reset_seen:
        page.evaluate(
            "() => localStorage.removeItem('archive:records-seen:v1')"
        )
    page.evaluate("document.getElementById('companion-toggle').click()")
    page.wait_for_timeout(500)
    page.evaluate("_setFolioDepth('archive')")
    page.wait_for_timeout(400)
    page.evaluate(f"(() => _openFolioObject('{rec_id}'))()")
    page.wait_for_timeout(1500)


def leaf_animation(page):
    return page.evaluate(
        """
        (() => {
          const leaf = document.querySelector('.folio-leaf');
          if (!leaf) return null;
          const s = getComputedStyle(leaf);
          return {
            kind: leaf.dataset.kind,
            classes: leaf.className,
            visited: leaf.dataset.visited || null,
            animationName: s.animationName,
            animationDuration: s.animationDuration,
            animationDelay: s.animationDelay,
            animationTimingFunction: s.animationTimingFunction,
          };
        })()
        """
    )


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 1100})
        page = ctx.new_page()

        # ── Move 1 — Entry cadence per kind ────────────────────────
        print("=== Move 1 — Entry cadence per kind ===")

        # Text witness — 0.72s
        open_leaf(page, "gen.1.1", "gen1-commentary-augustine",
                  reset_seen=True)
        m = leaf_animation(page)
        print(f"  commentary (text witness): duration={m['animationDuration']} "
              f"name={m['animationName']}")
        assert m["animationDuration"] == "0.72s", m["animationDuration"]
        assert "folio-leaf-settle" in m["animationName"]

        # AO chamber — 0.92s
        open_leaf(page, "gen.1.6", "gen1-cosmology-firmament")
        m = leaf_animation(page)
        print(f"  cosmology chamber:         duration={m['animationDuration']} "
              f"name={m['animationName']}")
        assert m["animationDuration"] == "0.92s", m["animationDuration"]

        # Another chamber
        open_leaf(page, "exo.40.34", "exo40-sanctuary-glory")
        m = leaf_animation(page)
        print(f"  sanctuary chamber:         duration={m['animationDuration']}")
        assert m["animationDuration"] == "0.92s"

        # Doré plate — 1.2s with 0.32s delay
        open_leaf(page, "gen.1.3", "dore-creation-of-light")
        m = leaf_animation(page)
        print(f"  Doré plate:                duration={m['animationDuration']} "
              f"delay={m['animationDelay']} name={m['animationName']}")
        assert m["animationDuration"] == "1.2s", m["animationDuration"]
        assert m["animationDelay"] == "0.32s", m["animationDelay"]
        assert "folio-leaf-plate-arrive" in m["animationName"]
        print("  OK — three-tier entry gradient: 0.72s text / 0.92s chamber / "
              "1.2s plate (after 0.32s held breath).\n")

        # ── Move 2 — Exit ceremony ─────────────────────────────────
        print("=== Move 2 — Exit ceremony (extended chamber release) ===")
        # Read viewer transition at NON-active state (the exit transition)
        page.evaluate("document.body.classList.remove('viewer-active')")
        page.wait_for_timeout(100)
        exit_transition = page.evaluate(
            """
            (() => {
              const v = document.getElementById('object-viewer');
              return v ? getComputedStyle(v).transitionDuration : null;
            })()
            """
        )
        # Restore viewer-active for subsequent tests
        page.evaluate("document.body.classList.add('viewer-active')")
        page.wait_for_timeout(100)
        print(f"  #object-viewer (exit) transitionDuration: {exit_transition}")
        # The transition is "opacity 0.9s ease-out, visibility 0s linear 0.9s"
        # so transitionDuration returns "0.9s, 0s"
        assert "0.9s" in exit_transition, exit_transition
        print("  OK — exit fade extended to 0.9s (was 0.6s).\n")

        # ── Move 3 — Plate chamber isolation (:has selector) ───────
        print("=== Move 3 — Plate-chamber isolation ===")
        open_leaf(page, "gen.1.3", "dore-creation-of-light")
        plate_chamber_bg = page.evaluate(
            "(()=>getComputedStyle(document.getElementById('object-viewer')).background)()"
        )
        print(f"  plate chamber bg (first 90 chars): {plate_chamber_bg[:90]}...")
        # The deeper chamber uses rgba(20, 14, 8, 0.92) as its
        # center stop. The text-witness chamber uses rgba(32, 24, 16, 0.86).
        assert "rgba(20, 14, 8, 0.92)" in plate_chamber_bg or \
               "rgb(20, 14, 8)" in plate_chamber_bg, plate_chamber_bg
        # Text-witness chamber should NOT have this deeper background.
        open_leaf(page, "gen.1.1", "gen1-commentary-augustine")
        text_chamber_bg = page.evaluate(
            "(()=>getComputedStyle(document.getElementById('object-viewer')).background)()"
        )
        print(f"  text chamber bg (first 90 chars):  {text_chamber_bg[:90]}...")
        assert "rgba(32, 24, 16, 0.86)" in text_chamber_bg or \
               "rgb(32, 24, 16)" in text_chamber_bg, text_chamber_bg
        print("  OK — plate chamber deepens via :has() selector; text "
              "chamber unchanged.\n")

        # ── Move 4 — Codex memory: visited-leaf trace ──────────────
        print("=== Move 4 — Codex memory (visited-leaf trace) ===")
        # Reset seen set, open commentary fresh
        open_leaf(page, "gen.1.1", "gen1-commentary-augustine",
                  reset_seen=True)
        m = leaf_animation(page)
        print(f"  1st encounter:  visited={m['visited']}")
        assert m["visited"] is None, m["visited"]
        # Re-open same record — should now be visited
        page.evaluate("(() => _openFolioObject('gen1-commentary-augustine'))()")
        page.wait_for_timeout(1500)
        m = leaf_animation(page)
        print(f"  2nd encounter:  visited={m['visited']}")
        assert m["visited"] == "true", m["visited"]
        # Provenance border-bottom-color should be the visited warm
        border = page.evaluate(
            """
            (()=>{
              const p = document.querySelector('.folio-leaf-provenance');
              return p ? getComputedStyle(p).borderBottomColor : null;
            })()
            """
        )
        print(f"  visited provenance border: {border}")
        # The visited rule sets rgba(120, 75, 30, 0.36)
        assert "rgb(120, 75, 30)" in border or "120, 75, 30" in border, border
        # Reset and verify localStorage tracks across page loads
        seen_list = page.evaluate(
            "(()=>JSON.parse(localStorage.getItem('archive:records-seen:v1') || '[]'))()"
        )
        print(f"  records-seen storage: {seen_list}")
        assert "gen1-commentary-augustine" in seen_list
        print("  OK — codex memory: leaf gains data-visited after re-encounter;"
              " provenance hairline warms; localStorage persists.\n")

        # ── No regression: text witness still 0.72s ────────────────
        print("=== Text-witness entry preserved (0.72s) ===")
        open_leaf(page, "gen.22.2", "gen22-mount-moriah", reset_seen=True)
        m = leaf_animation(page)
        print(f"  architecture (Moriah): duration={m['animationDuration']}")
        assert m["animationDuration"] == "0.72s"
        open_leaf(page, "gen.1.2", "gen1-linguistic-tohu")
        m = leaf_animation(page)
        print(f"  linguistic (tohu):     duration={m['animationDuration']}")
        assert m["animationDuration"] == "0.72s"
        print("  OK — text witnesses preserve 0.72s settle.\n")

        # ── No regression: family identities ───────────────────────
        print("=== Family identities preserved ===")
        for label, pid, rec_id, exp in [
            ("commentary", "gen.1.1", "gen1-commentary-augustine", "640px"),
            ("linguistic", "gen.1.2", "gen1-linguistic-tohu",     "560px"),
            ("manuscript", "gen.1.1", "gen1-manuscript-opening",  "500px"),
            ("architecture","gen.22.2","gen22-mount-moriah",      "480px"),
            ("ritual",     "gen.1.3", "gen1-ritual-maariv-aravim","560px"),
            ("cross-ref",  "gen.1.1", "gen1-xref-nt-creation",    "540px"),
            ("cosmology",  "gen.1.1", "gen1-cosmology-ane",       "620px"),
            ("reception",  "gen.18.2","gen18-three-visitors-reception", "600px"),
        ]:
            open_leaf(page, pid, rec_id, reset_seen=True)
            bm = page.evaluate(
                "(()=>{const b=document.querySelector('.folio-body-vertical');return b?getComputedStyle(b).maxWidth:null;})()"
            )
            print(f"  {label:<14}: bodyMaxWidth={bm}")
            assert bm == exp, (label, bm, exp)
        print("  OK — all 8 families preserved.\n")

        # ── AO count ───────────────────────────────────────────────
        ao_count = page.evaluate(
            """(() => {
                const ids = new Set();
                const recs = (currentData && currentData.genealogy) || [];
                for (const r of recs) {
                    if (r && r.atlas_object && r.atlas_object.id) ids.add(r.atlas_object.id);
                }
                return ids.size;
            })()"""
        )
        print(f"=== AO inventory: {ao_count} ===")
        assert ao_count == 12
        print("  OK — 12 Atlas Objects preserved.\n")

        # ── Captures: plate ceremonial entry mid-animation ─────────
        print("=== Per-family screenshots after v78 choreography ===")
        for pid, rec_id, label in [
            ("gen.1.1",  "gen1-commentary-augustine",       "commentary"),
            ("gen.1.6",  "gen1-cosmology-firmament",        "ao_cosmology"),
            ("exo.40.34","exo40-sanctuary-glory",           "ao_sanctuary"),
            ("gen.1.3",  "dore-creation-of-light",          "dore"),
            ("gen.22.2", "gen22-mount-moriah",              "architecture"),
            ("gen.1.1",  "gen1-manuscript-opening",         "manuscript"),
            ("gen.18.2", "gen18-three-visitors-reception",  "reception"),
        ]:
            open_leaf(page, pid, rec_id, reset_seen=True)
            page.screenshot(path=f"reports/v78_after_{label}.png")
            print(f"  captured {label}")

        b.close()
    print("\nALL CHECKS PASSED — Reading Choreography operational.")


if __name__ == "__main__":
    main()
