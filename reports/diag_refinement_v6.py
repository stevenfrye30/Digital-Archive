"""Verify v6 — asymmetric canon columns + tightened manuscript rhythm."""
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
            const sections = Array.from(document.querySelectorAll('.bcl-canon-section'));
            return {
              viewportHeight: innerHeight,
              readerScrollH: reader.scrollHeight,
              readerClientH: reader.clientHeight,
              fitsNoScroll: reader.scrollHeight <= reader.clientHeight + 1,
              enterBottom: enter ? enter.getBoundingClientRect().bottom : null,
              bookCount: items.length,
              wrapped: wrapped.map(li => li.querySelector('.cc-toc-name').textContent),
              sectionColumnCounts: sections.map(s => {
                const list = s.querySelector('.bcl-canon-list');
                const tpl = getComputedStyle(list).gridTemplateColumns;
                return {
                  canon: s.dataset.canon,
                  cols: tpl.split(' ').length,
                  rows: Math.ceil(s.querySelectorAll('li').length / tpl.split(' ').length),
                  items: s.querySelectorAll('li').length,
                  bottom: s.getBoundingClientRect().bottom,
                };
              }),
              labelText: document.querySelector('.bcl-canon-label')?.textContent,
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
        assert info["wrapped"] == [], f"Wrapped: {info['wrapped']}"
        sections = {s["canon"]: s for s in info["sectionColumnCounts"]}
        assert sections["old-testament"]["cols"] == 7, (
            f"OT cols != 7: {sections['old-testament']}"
        )
        assert sections["apocrypha"]["cols"] == 6, (
            f"Apoc cols != 6: {sections['apocrypha']}"
        )
        assert sections["new-testament"]["cols"] == 7, (
            f"NT cols != 7: {sections['new-testament']}"
        )

        # Full leaf
        page.screenshot(path="reports/v6_titleleaf.png")

        # Section close-ups by clipping
        for canon, fname in [
            ("old-testament", "v6_section_ot.png"),
            ("apocrypha", "v6_section_apoc.png"),
            ("new-testament", "v6_section_nt.png"),
        ]:
            sec = page.locator(f'.bcl-canon-section[data-canon="{canon}"]')
            sec.screenshot(path=f"reports/{fname}")

        # Hover one OT entry to capture the rubric + plate hover at once
        page.hover('.bcl-canon-section[data-canon="old-testament"] li:nth-child(1)')
        page.wait_for_timeout(200)
        page.screenshot(path="reports/v6_titleleaf_hover.png")

        b.close()
    print("ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
