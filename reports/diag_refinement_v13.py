"""v13 — click-anywhere-outside-the-object dismissal verification."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

URL = "http://localhost:8765/index.html?text=bible_kjv.json"


def open_plate(page):
    page.goto(URL, wait_until="networkidle")
    page.wait_for_function(
        "typeof currentData === 'object' && currentData && currentData.passages",
        timeout=15000,
    )
    page.wait_for_selector(".bcl-enter-btn", timeout=10000)
    page.wait_for_timeout(400)
    page.click(".bcl-enter-btn")
    page.wait_for_timeout(500)
    page.click("#companion-toggle")
    page.wait_for_timeout(400)
    page.wait_for_selector('.cr-margin-witness[data-kind="plate"]', timeout=5000)
    page.click('.cr-margin-witness[data-kind="plate"]')
    page.wait_for_timeout(700)


def is_open(page):
    return page.evaluate(
        "() => document.body.classList.contains('viewer-active')"
    )


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # Get the actual image and plaque positions
        open_plate(page)
        geo = page.evaluate(
            """
          () => {
            const img = document.querySelector('.folio-plate');
            const plaque = document.querySelector('.folio-plate-plaque');
            const wrap = document.querySelector('.folio-plate-wrap');
            return {
              img: img.getBoundingClientRect().toJSON(),
              plaque: plaque.getBoundingClientRect().toJSON(),
              wrap: wrap.getBoundingClientRect().toJSON(),
            };
          }
        """
        )
        print("GEOMETRY:")
        print(f"  img:    L={geo['img']['left']:.0f} R={geo['img']['right']:.0f} "
              f"T={geo['img']['top']:.0f} B={geo['img']['bottom']:.0f}")
        print(f"  plaque: L={geo['plaque']['left']:.0f} R={geo['plaque']['right']:.0f} "
              f"T={geo['plaque']['top']:.0f} B={geo['plaque']['bottom']:.0f}")
        print(f"  wrap:   L={geo['wrap']['left']:.0f} R={geo['wrap']['right']:.0f} "
              f"T={geo['wrap']['top']:.0f} B={geo['wrap']['bottom']:.0f}")

        # The wrap must NOT span the full viewport now
        assert geo["wrap"]["right"] - geo["wrap"]["left"] < 800, (
            f"Wrap still too wide: {geo['wrap']['right'] - geo['wrap']['left']}"
        )

        # ---- ON-OBJECT CLICKS (must stay open) ----
        on_object_points = [
            ("image center", int((geo["img"]["left"] + geo["img"]["right"]) / 2),
             int((geo["img"]["top"] + geo["img"]["bottom"]) / 2)),
            ("plaque center", int((geo["plaque"]["left"] + geo["plaque"]["right"]) / 2),
             int((geo["plaque"]["top"] + geo["plaque"]["bottom"]) / 2)),
        ]
        for label, x, y in on_object_points:
            page.mouse.click(x, y)
            page.wait_for_timeout(200)
            assert is_open(page), f"Click on {label} ({x},{y}) WRONGLY closed viewer"
            print(f"  ✓ {label} ({x},{y}): stays open")

        # ---- DISMISSAL CLICKS (must close) ----
        dismiss_cases = [
            ("far top-left corner", 30, 30),
            ("far top-right corner", 1410, 30),
            ("far bottom-left corner", 30, 870),
            ("far bottom-right corner", 1410, 870),
            ("left of image (dimmed manuscript)", 200, 450),
            ("right of image (dimmed manuscript)", 1290, 450),
            ("above image", 720, 50),
            ("below plaque", 720, 870),
            ("between image and right edge", 1100, 400),
            ("between image and left edge", 280, 400),
        ]
        for label, x, y in dismiss_cases:
            # Reopen
            open_plate(page)
            assert is_open(page), "Failed to reopen for next test"
            page.mouse.click(x, y)
            page.wait_for_timeout(500)
            closed = not is_open(page)
            print(f"  {'✓' if closed else '✗'} click {label} ({x},{y}): "
                  f"{'closed' if closed else 'STILL OPEN'}")
            assert closed, f"Click {label} ({x},{y}) did NOT dismiss viewer"

        # ---- Re-open and confirm no scroll changes ----
        open_plate(page)
        before = page.evaluate(
            """
          () => ({
            doc: document.documentElement.scrollHeight,
            reader: document.getElementById('reader').scrollTop,
            innerH: innerHeight,
          })
        """
        )
        print(f"\nNO-SCROLL CHECK: {before}")
        assert before["doc"] == before["innerH"], (
            f"Document scroll appeared: {before['doc']} vs {before['innerH']}"
        )

        page.screenshot(path="reports/v13_dismiss_zones.png")
        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
