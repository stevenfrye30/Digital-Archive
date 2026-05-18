"""v20 — verify citation outside-click + Escape, folio visibility."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── BUG 1: citation drawer dismissal ─────────────────────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json",
            wait_until="networkidle",
        )
        page.wait_for_selector(".bible-cover-layout", timeout=10000)
        page.wait_for_timeout(500)

        # Open
        page.click(".cite-corner > summary")
        page.wait_for_timeout(200)
        open_state = page.evaluate("() => document.querySelector('.cite-corner').open")
        assert open_state, "Drawer didn't open on summary click"

        # Click inside the drawer — should stay open
        page.click(".cite-corner .cc-citations")
        page.wait_for_timeout(200)
        still_open = page.evaluate("() => document.querySelector('.cite-corner').open")
        assert still_open, "Drawer wrongly closed on inside click"
        print("Drawer click inside: stays open ✓")

        # Click outside on parchment — should close
        page.mouse.click(400, 500)
        page.wait_for_timeout(200)
        closed = page.evaluate("() => document.querySelector('.cite-corner').open")
        assert not closed, "Drawer didn't close on outside click"
        print("Drawer click outside: closes ✓")

        # Open again via direct DOM manipulation (avoids playwright
        # visibility check edge cases when summary is at the same
        # screen coordinates as the just-closed panel) and test Escape.
        page.evaluate("() => { document.querySelector('.cite-corner').open = true; }")
        page.wait_for_timeout(200)
        assert page.evaluate("() => document.querySelector('.cite-corner').open")
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        closed_by_esc = page.evaluate("() => document.querySelector('.cite-corner').open")
        assert not closed_by_esc, "Drawer didn't close on Escape"
        print("Escape: closes ✓")

        # ── BUG 2: folio visibility ──────────────────────────────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(700)

        # Click Folio side (single-button path)
        page.click("#companion-swap")
        page.wait_for_timeout(500)

        state = page.evaluate(
            """
          () => {
            const folio = document.getElementById('folio');
            const cs = getComputedStyle(folio);
            const passage = document.querySelector('.cr-row > :first-child');
            const fr = folio.getBoundingClientRect();
            const pr = passage.getBoundingClientRect();
            return {
              bodyClasses: Array.from(document.body.classList),
              folio: {
                display: cs.display,
                visibility: cs.visibility,
                opacity: cs.opacity,
                width: cs.width,
                zIndex: cs.zIndex,
                background: cs.backgroundImage,
                rect: fr.toJSON(),
              },
              passage: { rect: pr.toJSON() },
              entryCount: document.querySelectorAll('.cr-folio-entry').length,
              firstEntry: document.querySelector('.cr-folio-entry .cr-folio-title')?.textContent,
              overlapsScripture:
                fr.left < pr.right && fr.right > pr.left &&
                fr.top < pr.bottom && fr.bottom > pr.top,
              // Pixel-strict overlap: actual shared area > 0
              sharedArea: Math.max(0, Math.min(fr.right, pr.right) - Math.max(fr.left, pr.left)) *
                          Math.max(0, Math.min(fr.bottom, pr.bottom) - Math.max(fr.top, pr.top)),
            };
          }
        """
        )
        print(f"\nAfter clicking 'Folio side':")
        print(f"  body classes: {state['bodyClasses']}")
        print(f"  folio.display: {state['folio']['display']}")
        print(f"  folio.width:   {state['folio']['width']}")
        print(f"  folio.rect:    {state['folio']['rect']}")
        print(f"  passage.rect:  {state['passage']['rect']}")
        print(f"  entries:       {state['entryCount']}")
        print(f"  first entry:   {state['firstEntry']}")
        print(f"  shared area:   {state['sharedArea']:.1f} px²")

        assert "companion-mode" in state["bodyClasses"], (
            "Folio side click didn't activate companion-mode"
        )
        assert state["folio"]["display"] == "block"
        assert state["folio"]["visibility"] == "visible"
        assert float(state["folio"]["opacity"]) > 0.5
        assert state["folio"]["rect"]["width"] >= 180
        assert state["entryCount"] >= 1
        assert state["firstEntry"] == "The Creation of Light"
        # Pixel-strict: zero shared area (touching at edge is OK)
        assert state["sharedArea"] == 0, (
            f"Folio overlaps scripture by {state['sharedArea']} px²"
        )

        # Capture folio-LEFT visible state
        page.screenshot(path="reports/v20_folio_left.png")

        # Click swap to go to right
        page.click("#companion-swap")
        page.wait_for_timeout(500)
        page.screenshot(path="reports/v20_folio_right.png")

        # Test scripture invariance: turn off
        ref = state["passage"]["rect"]
        page.click("#companion-toggle")  # turn off
        page.wait_for_timeout(500)
        after_off = page.evaluate(
            "() => document.querySelector('.cr-row > :first-child').getBoundingClientRect().toJSON()"
        )
        print(f"\nScripture invariance:")
        print(f"  reference (folio-left on):  L={ref['left']} R={ref['right']} W={ref['width']}")
        print(f"  after toggle cycle off:     L={after_off['left']} R={after_off['right']} W={after_off['width']}")
        assert abs(ref["left"] - after_off["left"]) <= 0.5
        assert abs(ref["right"] - after_off["right"]) <= 0.5
        page.screenshot(path="reports/v20_folio_off.png")

        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
