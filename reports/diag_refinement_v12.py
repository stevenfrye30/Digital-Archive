"""v12 — folio object encounter verification."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

URL = "http://localhost:8765/index.html?text=bible_kjv.json"


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle")
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_selector(".bcl-enter-btn", timeout=10000)
        page.wait_for_timeout(400)

        # Enter reading room
        page.click(".bcl-enter-btn")
        page.wait_for_timeout(500)

        # Turn folio on
        page.click("#companion-toggle")
        page.wait_for_timeout(400)

        # Wait for a plate witness to appear in the chapter-room margin
        page.wait_for_selector('.cr-margin-witness[data-kind="plate"]', timeout=5000)

        # Capture baseline: reader scrollTop and document height
        before = page.evaluate(
            """
          () => ({
            readerScrollTop: document.getElementById('reader').scrollTop,
            docScrollH: document.documentElement.scrollHeight,
            bodyScrollH: document.body.scrollHeight,
            innerH: innerHeight,
            innerW: innerWidth,
          })
        """
        )
        print("BEFORE OPEN:", before)

        # Open the plate
        page.click('.cr-margin-witness[data-kind="plate"]')
        page.wait_for_selector(".folio-leaf[data-kind='plate'] .folio-plate", state="visible", timeout=5000)
        page.wait_for_timeout(700)  # let animation settle

        opened = page.evaluate(
            """
          () => {
            const img = document.querySelector('.folio-leaf[data-kind="plate"] .folio-plate');
            const rect = img.getBoundingClientRect();
            const viewer = document.getElementById('object-viewer');
            const back = document.querySelector('.folio-leaf-return');
            return {
              viewerActive: document.body.classList.contains('viewer-active'),
              imageWidth: rect.width,
              imageHeight: rect.height,
              imageTop: rect.top,
              imageBottom: rect.bottom,
              imageLeft: rect.left,
              viewportH: innerHeight,
              viewportW: innerWidth,
              docScrollH: document.documentElement.scrollHeight,
              readerScrollTop: document.getElementById('reader').scrollTop,
              viewerOverflow: getComputedStyle(viewer).overflowY,
              bodyOverflow: getComputedStyle(document.body).overflow,
              readerOverflow: getComputedStyle(document.getElementById('reader')).overflowY,
              returnButtonExists: back !== null,
              plaqueExists: !!document.querySelector('.folio-plate-plaque'),
              plaqueRect: (() => {
                const p = document.querySelector('.folio-plate-plaque');
                return p ? p.getBoundingClientRect().toJSON() : null;
              })(),
            };
          }
        """
        )
        print("\nOPENED:", opened)
        # No viewport scroll change
        assert opened["docScrollH"] == before["docScrollH"], (
            f"doc scroll height changed: {before['docScrollH']} -> {opened['docScrollH']}"
        )
        assert opened["readerScrollTop"] == before["readerScrollTop"], (
            f"reader scroll drifted: {before['readerScrollTop']} -> {opened['readerScrollTop']}"
        )
        # Body overflow locked
        assert opened["bodyOverflow"] == "hidden", (
            f"body overflow not locked: {opened['bodyOverflow']}"
        )
        # Viewer overflow hidden
        assert opened["viewerOverflow"] == "hidden", (
            f"viewer overflow not hidden: {opened['viewerOverflow']}"
        )
        # Return button gone
        assert not opened["returnButtonExists"], "Return rubric should be removed"
        # Image is large — at least 60% of viewport height
        assert opened["imageHeight"] >= opened["viewportH"] * 0.6, (
            f"Image too small: {opened['imageHeight']} vs viewport {opened['viewportH']}"
        )
        # Plaque visible below image
        assert opened["plaqueExists"]
        assert opened["plaqueRect"]["bottom"] <= opened["viewportH"] + 1, (
            f"Plaque off-screen: bottom={opened['plaqueRect']['bottom']}, vh={opened['viewportH']}"
        )

        page.screenshot(path="reports/v12_folio_opened.png")

        # Click on the image — should NOT close
        page.click(".folio-plate")
        page.wait_for_timeout(300)
        still_open = page.evaluate("() => document.body.classList.contains('viewer-active')")
        assert still_open, "Click on image incorrectly dismissed viewer"
        print("Click on image: still open ✓")

        # Click inside the plaque — should NOT close (inside the on-object zone)
        page.click(".folio-plate-plaque")
        page.wait_for_timeout(300)
        still_open2 = page.evaluate("() => document.body.classList.contains('viewer-active')")
        assert still_open2, "Click on plaque incorrectly dismissed viewer"
        print("Click on plaque: still open ✓")

        # Click outside the object (in the dark area) — should close
        # Click near a corner, far from the image
        page.mouse.click(50, 50)
        page.wait_for_timeout(700)
        closed = page.evaluate(
            """
          () => ({
            viewerActive: document.body.classList.contains('viewer-active'),
            readerScrollTop: document.getElementById('reader').scrollTop,
            companionMode: document.body.classList.contains('companion-mode'),
            inReading: document.body.classList.contains('in-reading'),
          })
        """
        )
        print(f"AFTER OUTSIDE CLICK: {closed}")
        assert not closed["viewerActive"], "Viewer should be closed"
        assert closed["companionMode"], "Folio should remain on"
        assert closed["inReading"], "Reading state should be preserved"
        assert closed["readerScrollTop"] == before["readerScrollTop"], (
            f"Reader scroll drifted after close: {before['readerScrollTop']} -> {closed['readerScrollTop']}"
        )
        print("Reader scroll preserved exactly ✓")

        page.screenshot(path="reports/v12_after_close.png")

        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
