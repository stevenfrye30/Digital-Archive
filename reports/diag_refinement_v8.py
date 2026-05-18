"""v8 — verify the microscopic-scrollbar fix.

Confirms:
  - document.documentElement.scrollHeight === window.innerHeight
  - #reader uses overflow:hidden on title leaf (no scrollbar possible)
  - The leaf composition has a measured buffer below the content
    so subpixel rounding can never overflow
  - All v7 composition guarantees preserved (no wraps, 80 books,
    column distribution, Enter plate visible)
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
        page.wait_for_selector(".bible-cover-layout", timeout=10000)
        page.wait_for_timeout(400)

        info = page.evaluate(
            """
          () => {
            const reader = document.getElementById('reader');
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
            const readerCS = getComputedStyle(reader);
            const sections = Array.from(document.querySelectorAll('.bcl-canon-section')).map(s => ({
              canon: s.dataset.canon,
              cols: getComputedStyle(s.querySelector('.bcl-canon-list')).gridTemplateColumns.split(' ').length,
            }));
            return {
              vpH: innerHeight,
              docScrollH: document.documentElement.scrollHeight,
              docClientH: document.documentElement.clientHeight,
              bodyScrollH: document.body.scrollHeight,
              readerScrollH: reader.scrollHeight,
              readerClientH: reader.clientHeight,
              readerOverflowY: readerCS.overflowY,
              readerPaddingBottom: readerCS.paddingBottom,
              readerScrollbar:
                window.innerWidth - document.documentElement.clientWidth,
              readerInnerH: document.getElementById('reader-inner').offsetHeight,
              clippingBuffer:
                reader.clientHeight
                - document.getElementById('reader-inner').offsetHeight
                - parseFloat(readerCS.paddingTop)
                - parseFloat(readerCS.paddingBottom),
              titleTop: document.querySelector('.bible-cover-layout .cc-title')?.getBoundingClientRect().top,
              enterBottom: enter ? enter.getBoundingClientRect().bottom : null,
              bookCount: items.length,
              wrapped: wrapped.map(li => li.querySelector('.cc-toc-name').textContent),
              sectionCols: sections,
            };
          }
        """
        )
        print("─── DOC ────────────────────────────────────────────────".replace("─", "-"))
        print(f"  viewport innerHeight:  {info['vpH']}")
        print(f"  doc.scrollHeight:      {info['docScrollH']}")
        print(f"  doc.clientHeight:      {info['docClientH']}")
        print(f"  body.scrollHeight:     {info['bodyScrollH']}")
        print(f"  scrollbar reserved px: {info['readerScrollbar']}")
        print(f"  doc overflow:          {info['docScrollH'] - info['vpH']}px")
        print()
        print("--- READER ----------------------------------------------")
        print(f"  reader.scrollHeight:   {info['readerScrollH']}")
        print(f"  reader.clientHeight:   {info['readerClientH']}")
        print(f"  reader-inner offsetH:  {info['readerInnerH']}")
        print(f"  reader overflow-y:     {info['readerOverflowY']}")
        print(f"  reader padding-bottom: {info['readerPaddingBottom']}")
        print(f"  clipping buffer:       {info['clippingBuffer']}px")
        print()
        print("--- COMPOSITION -----------------------------------------")
        print(f"  title top:             {info['titleTop']:.1f}")
        print(f"  enter plate bottom:    {info['enterBottom']:.1f}")
        print(f"  bottom margin:         {info['vpH'] - info['enterBottom']:.1f}")
        print(f"  bookCount:             {info['bookCount']}")
        print(f"  wrapped:               {info['wrapped']}")
        print(f"  columns:               {info['sectionCols']}")
        print()

        # Hard guarantees
        assert info["docScrollH"] == info["vpH"], (
            f"document scrolls: {info['docScrollH']} != {info['vpH']}"
        )
        assert info["readerOverflowY"] == "hidden", (
            f"reader overflow-y not hidden: {info['readerOverflowY']}"
        )
        assert info["clippingBuffer"] >= 50, (
            f"buffer too thin (vulnerable to subpixel scroll): {info['clippingBuffer']}"
        )
        assert info["enterBottom"] <= info["vpH"] + 1, "Enter cut off"
        assert info["bookCount"] == 80
        assert info["wrapped"] == [], f"Wrapped: {info['wrapped']}"
        cols = {s["canon"]: s["cols"] for s in info["sectionCols"]}
        assert cols == {"old-testament": 7, "apocrypha": 6, "new-testament": 7}

        page.screenshot(path="reports/v8_titleleaf.png")
        print("ALL ASSERTIONS PASSED")
        b.close()


if __name__ == "__main__":
    main()
