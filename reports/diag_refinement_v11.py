"""v11 — reading-room overhaul verification."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

_ = """v11 — reading-room overhaul verification.

Confirms:
  - TOC unchanged (zero scroll, 80 books, columns 7/6/7)
  - Reading-room chapter heading: Genesis larger, ch 1 darker/larger
  - Controls strip has a distinct background tone from reader paper
  - Column switcher shows only "single · wide" (no dual)
  - Wide mode dramatically wider than single
  - Folio side button always visible in reading room, toggles
    body.folio-left and visibly switches placement
"""
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

        # --- Title leaf invariants ---
        leaf = page.evaluate(
            """
          () => ({
            docOverflow: document.documentElement.scrollHeight - innerHeight,
            bookCount: document.querySelectorAll('.bcl-canon-list li').length,
            sectionCols: Array.from(document.querySelectorAll('.bcl-canon-section')).map(s => ({
              canon: s.dataset.canon,
              cols: getComputedStyle(s.querySelector('.bcl-canon-list')).gridTemplateColumns.split(' ').length,
            })),
            ctrlColsDisplay: getComputedStyle(document.getElementById('ctrl-columns')).display,
          })
        """
        )
        print("LEAF:", leaf)
        assert leaf["docOverflow"] == 0
        assert leaf["bookCount"] == 80
        cols = {s["canon"]: s["cols"] for s in leaf["sectionCols"]}
        assert cols == {"old-testament": 7, "apocrypha": 6, "new-testament": 7}
        assert leaf["ctrlColsDisplay"] == "none"

        # Enter the reading room
        page.click(".bcl-enter-btn")
        page.wait_for_timeout(500)

        room = page.evaluate(
            """
          () => {
            const heading = document.querySelector('.chapter-room-heading');
            const title = heading.querySelector('.ch-title');
            const sub = heading.querySelector('.ch-sub');
            const titleCS = getComputedStyle(title);
            const subCS = getComputedStyle(sub);
            const controls = document.getElementById('controls');
            const ctrlCS = getComputedStyle(controls);
            const reader = document.getElementById('reader');
            const readerCS = getComputedStyle(reader);
            const inner = document.getElementById('reader-inner');
            const swap = document.getElementById('companion-swap');
            const swapCS = getComputedStyle(swap);
            const opts = Array.from(document.querySelectorAll('#ctrl-columns .col-opt'))
              .filter(o => getComputedStyle(o).display !== 'none');
            return {
              titleFontPx: parseFloat(titleCS.fontSize),
              subFontPx: parseFloat(subCS.fontSize),
              subOpacity: parseFloat(subCS.opacity),
              subColor: subCS.color,
              controlsBg: ctrlCS.backgroundColor,
              readerBg: readerCS.backgroundColor,
              singleWidth: inner.getBoundingClientRect().width,
              visibleColOpts: opts.map(o => o.dataset.cols),
              swapVisible:
                swap.offsetParent !== null && swapCS.display !== 'none',
              swapText: swap.textContent.trim(),
            };
          }
        """
        )
        print("ROOM (default = single):", room)
        # Heading sizes
        assert room["titleFontPx"] >= 32, (
            f"Genesis title not larger enough: {room['titleFontPx']}px"
        )
        assert room["subFontPx"] >= 14, (
            f"ch 1 not large enough: {room['subFontPx']}px"
        )
        assert room["subOpacity"] >= 0.85, (
            f"ch 1 too faint: opacity {room['subOpacity']}"
        )
        # Controls bg distinct from reader bg
        assert room["controlsBg"] != room["readerBg"], (
            f"Controls bg same as reader: {room['controlsBg']}"
        )
        # Only single and wide visible
        assert room["visibleColOpts"] == ["single", "wide"], (
            f"Column options wrong: {room['visibleColOpts']}"
        )
        # Folio side button is visible
        assert room["swapVisible"], "Folio side button not visible"
        assert "Folio side" in room["swapText"]

        page.screenshot(path="reports/v11_reading_single.png")
        single_w = room["singleWidth"]

        # Switch to wide
        page.evaluate("document.querySelector('#ctrl-columns .col-opt[data-cols=\"wide\"]').click()")
        page.wait_for_timeout(300)
        wide = page.evaluate(
            """
          () => ({
            width: document.getElementById('reader-inner').getBoundingClientRect().width,
            colsClasses: Array.from(document.body.classList).filter(c => c.startsWith('cols-')),
          })
        """
        )
        print(f"\nWIDE: {wide}")
        assert "cols-wide" in wide["colsClasses"]
        assert wide["width"] >= 1380, f"Wide not nearly full screen: {wide['width']}"
        assert wide["width"] - single_w >= 280, (
            f"Wide not dramatically wider than single: {wide['width']} vs {single_w}"
        )
        print(f"width Δ wide - single = {wide['width'] - single_w}px")
        page.screenshot(path="reports/v11_reading_wide.png")

        # Click Folio side — should activate companion mode + folio-left
        page.evaluate("document.querySelector('#ctrl-columns .col-opt[data-cols=\"single\"]').click()")
        page.wait_for_timeout(200)
        page.click("#companion-swap")
        page.wait_for_timeout(400)
        side = page.evaluate(
            """
          () => ({
            classes: Array.from(document.body.classList),
            companionMode: document.body.classList.contains('companion-mode'),
            folioLeft: document.body.classList.contains('folio-left'),
            swapAria: document.getElementById('companion-swap').getAttribute('aria-pressed'),
          })
        """
        )
        print(f"\nAFTER swap click: {side}")
        assert side["companionMode"], "Folio should be activated by swap click"
        assert side["folioLeft"], "folio-left should be set"
        assert side["swapAria"] == "true"
        page.screenshot(path="reports/v11_folio_left.png")

        # Click swap again — should toggle back to right (no folio-left)
        page.click("#companion-swap")
        page.wait_for_timeout(300)
        right = page.evaluate(
            """
          () => ({
            companionMode: document.body.classList.contains('companion-mode'),
            folioLeft: document.body.classList.contains('folio-left'),
          })
        """
        )
        print(f"AFTER second swap click: {right}")
        assert right["companionMode"]
        assert not right["folioLeft"]
        page.screenshot(path="reports/v11_folio_right.png")

        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
