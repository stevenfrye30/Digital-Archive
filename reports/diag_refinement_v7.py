"""Verify v7 — final spatial tuning, tactile plate relief."""
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
            const title = document.querySelector('.bible-cover-layout .cc-title');
            const items = Array.from(document.querySelectorAll('.bcl-canon-list li'));
            const wrapped = items.filter(li => {
              const name = li.querySelector('.cc-toc-name');
              if (!name) return false;
              const cs = getComputedStyle(name);
              const lineH = parseFloat(cs.lineHeight) || (parseFloat(cs.fontSize) * 1.2);
              return name.getBoundingClientRect().height > lineH * 1.4
                  || name.scrollWidth > name.clientWidth + 1;
            });
            const plate = items[0];
            const plateCS = plate ? getComputedStyle(plate) : null;
            return {
              viewportHeight: innerHeight,
              viewportWidth: innerWidth,
              docScrollH: document.documentElement.scrollHeight,
              docClientH: document.documentElement.clientHeight,
              readerScrollH: reader.scrollHeight,
              readerClientH: reader.clientHeight,
              fitsNoScrollReader: reader.scrollHeight <= reader.clientHeight + 1,
              fitsNoScrollDoc: document.documentElement.scrollHeight <= innerHeight + 1,
              titleTop: title ? title.getBoundingClientRect().top : null,
              enterBottom: enter ? enter.getBoundingClientRect().bottom : null,
              bookCount: items.length,
              wrapped: wrapped.map(li => li.querySelector('.cc-toc-name').textContent),
              sectionCols: Array.from(document.querySelectorAll('.bcl-canon-section')).map(s => ({
                canon: s.dataset.canon,
                cols: getComputedStyle(s.querySelector('.bcl-canon-list')).gridTemplateColumns.split(' ').length,
              })),
              plateBoxShadow: plateCS ? plateCS.boxShadow : null,
              firstSectionTop: document.querySelector('.bcl-canon-section')
                ? document.querySelector('.bcl-canon-section').getBoundingClientRect().top
                : null,
              ntSectionBottom: document.querySelector('.bcl-canon-section[data-canon="new-testament"]')
                ? document.querySelector('.bcl-canon-section[data-canon="new-testament"]').getBoundingClientRect().bottom
                : null,
            };
          }
        """
        )
        print("LEAF:", info)
        assert info["fitsNoScrollReader"], (
            f"reader scrolls: {info['readerScrollH']} > {info['readerClientH']}"
        )
        assert info["fitsNoScrollDoc"], (
            f"document scrolls: {info['docScrollH']} > {info['viewportHeight']}"
        )
        assert info["enterBottom"] <= info["viewportHeight"] + 1, (
            f"Enter below fold: {info['enterBottom']}"
        )
        assert info["bookCount"] == 80
        assert info["wrapped"] == [], f"Wrapped: {info['wrapped']}"
        cols = {s["canon"]: s["cols"] for s in info["sectionCols"]}
        assert cols == {"old-testament": 7, "apocrypha": 6, "new-testament": 7}, (
            f"Column layout drifted: {cols}"
        )
        # Confirm plate has tactile box-shadow (inset highlights)
        assert info["plateBoxShadow"] and "inset" in info["plateBoxShadow"], (
            f"Plate missing inset relief: {info['plateBoxShadow']}"
        )

        page.screenshot(path="reports/v7_titleleaf.png")

        page.hover('.bcl-canon-section[data-canon="old-testament"] li:nth-child(1)')
        page.wait_for_timeout(200)
        page.screenshot(path="reports/v7_hover_ot.png")

        page.hover(".bcl-enter-btn")
        page.wait_for_timeout(200)
        page.screenshot(path="reports/v7_hover_enter.png")

        # Spacing report
        print("\nSPACING METRICS")
        print(f"  Title top:           {info['titleTop']:.0f}px")
        print(f"  First canon top:     {info['firstSectionTop']:.0f}px")
        print(f"  NT section bottom:   {info['ntSectionBottom']:.0f}px")
        print(f"  Enter plate bottom:  {info['enterBottom']:.0f}px")
        print(f"  Bottom margin:       {info['viewportHeight'] - info['enterBottom']:.0f}px")

        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
