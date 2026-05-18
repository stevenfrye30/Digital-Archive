"""Verify codex-scale refinement v4 — wider reading measures."""
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
        page.wait_for_selector(".bible-cover-layout", timeout=10000)
        page.wait_for_timeout(400)

        leaf = page.evaluate(
            """
          () => {
            const reader = document.getElementById('reader');
            const layout = document.querySelector('.bible-cover-layout');
            const enter = document.querySelector('.bcl-enter-btn');
            const cite = document.querySelector('.bible-cover-layout .cite-corner');
            return {
              viewportHeight: innerHeight,
              fitsNoScroll: reader.scrollHeight <= reader.clientHeight + 4,
              readerScrollH: reader.scrollHeight,
              readerClientH: reader.clientHeight,
              enterBottom: enter ? enter.getBoundingClientRect().bottom : null,
              layoutWidth: layout.getBoundingClientRect().width,
              citeInCorner: cite
                ? (cite.getBoundingClientRect().right >= layout.getBoundingClientRect().right - 80
                  && cite.getBoundingClientRect().top - layout.getBoundingClientRect().top <= 40)
                : false,
              bookCount: document.querySelectorAll('.bcl-canon-list li').length,
              wrappedNames: Array.from(document.querySelectorAll('.bcl-canon-list li')).filter(li => {
                const name = li.querySelector('.cc-toc-name');
                if (!name) return false;
                const r = name.getBoundingClientRect();
                const cs = getComputedStyle(name);
                const lineH = parseFloat(cs.lineHeight) || (parseFloat(cs.fontSize) * 1.2);
                return r.height > lineH * 1.4;
              }).map(li => li.querySelector('.cc-toc-name').textContent),
            };
          }
        """
        )
        print("LEAF:", leaf)
        assert leaf["fitsNoScroll"], (
            f"reader scrolls: {leaf['readerScrollH']} > {leaf['readerClientH']}"
        )
        assert leaf["enterBottom"] <= leaf["viewportHeight"] + 1
        assert leaf["citeInCorner"]
        assert leaf["bookCount"] == 80
        print("REMAINING WRAPS:", leaf["wrappedNames"])

        page.screenshot(path="reports/v4_titleleaf.png")

        # Enter reading room
        page.click(".bcl-enter-btn")
        page.wait_for_timeout(400)

        def measure_mode(name):
            """Return reader-inner bbox + columnCount for the current mode."""
            return page.evaluate(
                """
              () => {
                const inner = document.getElementById('reader-inner');
                const r = inner.getBoundingClientRect();
                const cs = getComputedStyle(inner);
                return {
                  width: r.width,
                  left: r.left,
                  right: r.right,
                  columnCount: cs.columnCount,
                  bodyClasses: Array.from(document.body.classList)
                    .filter(c => c.startsWith('cols-')),
                };
              }
            """
            )

        # SINGLE
        page.evaluate(
            "document.querySelector('#ctrl-columns .col-opt[data-cols=\"single\"]').click()"
        )
        page.wait_for_timeout(200)
        single = measure_mode("single")
        print("SINGLE:", single)
        assert "cols-single" in single["bodyClasses"]
        assert single["columnCount"] == "1"
        # Target 980-1150px
        assert 980 <= single["width"] <= 1150, (
            f"single width out of range: {single['width']}"
        )
        page.screenshot(path="reports/v4_reading_single.png")

        # DUAL
        page.evaluate(
            "document.querySelector('#ctrl-columns .col-opt[data-cols=\"dual\"]').click()"
        )
        page.wait_for_timeout(200)
        dual = measure_mode("dual")
        print("DUAL:", dual)
        assert "cols-dual" in dual["bodyClasses"]
        assert dual["columnCount"] == "2"
        # Target 1350-1500px, but may be limited by viewport-side padding
        assert 1300 <= dual["width"] <= 1500, (
            f"dual width out of range: {dual['width']}"
        )
        page.screenshot(path="reports/v4_reading_dual.png")

        # WIDE
        page.evaluate(
            "document.querySelector('#ctrl-columns .col-opt[data-cols=\"wide\"]').click()"
        )
        page.wait_for_timeout(200)
        wide = measure_mode("wide")
        print("WIDE:", wide)
        assert "cols-wide" in wide["bodyClasses"]
        assert wide["columnCount"] == "1"
        # Wide should be the widest of the three
        assert wide["width"] > single["width"], (
            f"wide ({wide['width']}) not wider than single ({single['width']})"
        )
        assert wide["width"] >= 1300, f"wide too narrow: {wide['width']}"
        page.screenshot(path="reports/v4_reading_wide.png")

        # Heading position in single
        page.evaluate(
            "document.querySelector('#ctrl-columns .col-opt[data-cols=\"single\"]').click()"
        )
        page.wait_for_timeout(200)
        head = page.evaluate(
            """
          () => {
            const h = document.querySelector('.chapter-room-heading');
            return h ? h.getBoundingClientRect().top : null;
          }
        """
        )
        print("HEADING TOP:", head)
        assert head < 200, f"Heading too far down: {head}"

        b.close()
    print("ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
