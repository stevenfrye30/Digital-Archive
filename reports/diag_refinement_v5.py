"""Verify v5 — manuscript-plate canon entries, no wraps, no scroll."""
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

        info = page.evaluate(
            """
          () => {
            const reader = document.getElementById('reader');
            const layout = document.querySelector('.bible-cover-layout');
            const enter = document.querySelector('.bcl-enter-btn');
            const items = Array.from(document.querySelectorAll('.bcl-canon-list li'));
            const wrapped = items.filter(li => {
              const name = li.querySelector('.cc-toc-name');
              if (!name) return false;
              const cs = getComputedStyle(name);
              const lineH = parseFloat(cs.lineHeight) || (parseFloat(cs.fontSize) * 1.2);
              return name.getBoundingClientRect().height > lineH * 1.4
                  || name.scrollWidth > name.clientWidth + 1;
            });
            return {
              viewportHeight: innerHeight,
              readerScrollH: reader.scrollHeight,
              readerClientH: reader.clientHeight,
              fitsNoScroll: reader.scrollHeight <= reader.clientHeight + 1,
              enterBottom: enter ? enter.getBoundingClientRect().bottom : null,
              bookCount: items.length,
              wrapped: wrapped.map(li => ({
                name: li.querySelector('.cc-toc-name').textContent,
                height: li.querySelector('.cc-toc-name').getBoundingClientRect().height,
                scrollWidth: li.querySelector('.cc-toc-name').scrollWidth,
                clientWidth: li.querySelector('.cc-toc-name').clientWidth,
              })),
              firstItemBg: items[0] ? getComputedStyle(items[0]).backgroundColor : null,
              apocItemBg: items[40] ? getComputedStyle(items[40]).backgroundColor : null,
              ntItemBg: items[60] ? getComputedStyle(items[60]).backgroundColor : null,
            };
          }
        """
        )
        print("LEAF:", info)
        assert info["fitsNoScroll"], (
            f"reader scrolls: {info['readerScrollH']} > {info['readerClientH']}"
        )
        assert info["enterBottom"] <= info["viewportHeight"] + 1, (
            f"Enter below fold: {info['enterBottom']}"
        )
        assert info["bookCount"] == 80
        assert info["wrapped"] == [], f"Wrapped or overflowing names: {info['wrapped']}"
        # Each canon section should have a distinct background tint.
        assert (
            info["firstItemBg"] != "rgba(0, 0, 0, 0)"
        ), "OT items missing plate background"
        assert (
            info["firstItemBg"] != info["apocItemBg"]
        ), "Apocrypha tint not distinct from OT"
        assert (
            info["firstItemBg"] != info["ntItemBg"]
        ), "NT tint not distinct from OT"

        page.screenshot(path="reports/v5_titleleaf.png")

        # Hover an OT book
        page.hover('.bcl-canon-section[data-canon="old-testament"] li:nth-child(1)')
        page.wait_for_timeout(250)
        page.screenshot(path="reports/v5_hover_ot.png")

        # Hover the Enter button
        page.hover(".bcl-enter-btn")
        page.wait_for_timeout(250)
        page.screenshot(path="reports/v5_hover_enter.png")

        # Hover an NT book
        page.hover('.bcl-canon-section[data-canon="new-testament"] li:nth-child(1)')
        page.wait_for_timeout(250)
        page.screenshot(path="reports/v5_hover_nt.png")

        # Hover an Apocrypha book
        page.hover('.bcl-canon-section[data-canon="apocrypha"] li:nth-child(4)')
        page.wait_for_timeout(250)
        page.screenshot(path="reports/v5_hover_apoc.png")

        # Enter the room
        page.evaluate("document.querySelector('.bcl-enter-btn').click()")
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v5_reading_room.png")

        b.close()
    print("ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
