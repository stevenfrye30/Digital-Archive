"""v35 — layout refinement.

Verifies:
  1. Scripture text body sits with left breathing room when folio
     is visible (companion-mode + folio-right). Folio markers still
     align to verses.
  2. Bible contents/title page typography is fixed regardless of
     --reader-size and --reader-leading.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── 1a. Title leaf — capture baseline typography ───────
        page.goto("http://localhost:8765/index.html?text=bible_kjv.json",
                  wait_until="networkidle")
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        cover_base = page.evaluate(
            """
          () => {
            const layout = document.querySelector('.bible-cover-layout');
            const title = document.querySelector('.cc-title');
            const tocItem = document.querySelector('.bcl-canon-list li');
            return {
              readerSize: getComputedStyle(document.documentElement)
                            .getPropertyValue('--reader-size').trim(),
              layoutFontSize: getComputedStyle(layout).fontSize,
              layoutLineHeight: getComputedStyle(layout).lineHeight,
              layoutFontFamily: getComputedStyle(layout).fontFamily,
              titleFontSize: getComputedStyle(title).fontSize,
              tocItemFontSize: tocItem ? getComputedStyle(tocItem).fontSize : null,
              layoutWidth: layout.getBoundingClientRect().width,
              titleRect: title.getBoundingClientRect().toJSON(),
            };
          }
        """
        )
        print(f"BASELINE cover — reader-size={cover_base['readerSize']}")
        print(f"  layout font: {cover_base['layoutFontFamily']}")
        print(f"  layout font-size: {cover_base['layoutFontSize']}")
        print(f"  layout line-height: {cover_base['layoutLineHeight']}")
        print(f"  title font-size: {cover_base['titleFontSize']}")
        print(f"  toc-item font-size: {cover_base['tocItemFontSize']}")
        page.screenshot(path="reports/v35_cover_baseline.png")

        # ── 1b. Title leaf — bump reader-size, expect NO change ─
        page.evaluate(
            "document.getElementById('ctrl-size').value = '28'; "
            "document.getElementById('ctrl-size').dispatchEvent(new Event('input'));"
            "document.getElementById('ctrl-spacing').value = '2.4'; "
            "document.getElementById('ctrl-spacing').dispatchEvent(new Event('input'));"
        )
        page.wait_for_timeout(700)
        cover_big = page.evaluate(
            """
          () => {
            const layout = document.querySelector('.bible-cover-layout');
            const title = document.querySelector('.cc-title');
            const tocItem = document.querySelector('.bcl-canon-list li');
            return {
              readerSize: getComputedStyle(document.documentElement)
                            .getPropertyValue('--reader-size').trim(),
              layoutFontSize: getComputedStyle(layout).fontSize,
              layoutLineHeight: getComputedStyle(layout).lineHeight,
              titleFontSize: getComputedStyle(title).fontSize,
              tocItemFontSize: tocItem ? getComputedStyle(tocItem).fontSize : null,
            };
          }
        """
        )
        print(f"\nAFTER reader-size 28 — reader-size={cover_big['readerSize']}")
        print(f"  layout font-size: {cover_big['layoutFontSize']}")
        print(f"  layout line-height: {cover_big['layoutLineHeight']}")
        print(f"  title font-size: {cover_big['titleFontSize']}")
        print(f"  toc-item font-size: {cover_big['tocItemFontSize']}")
        assert cover_big['layoutFontSize'] == cover_base['layoutFontSize']
        assert cover_big['layoutLineHeight'] == cover_base['layoutLineHeight']
        assert cover_big['titleFontSize'] == cover_base['titleFontSize']
        assert cover_big['tocItemFontSize'] == cover_base['tocItemFontSize']
        print("  OK — title leaf typography is fixed across reader-size change")
        page.screenshot(path="reports/v35_cover_with_big_reader_size.png")

        # ── Reset reader controls for cleaner reading-room test
        page.evaluate(
            "document.getElementById('ctrl-size').value = '18'; "
            "document.getElementById('ctrl-size').dispatchEvent(new Event('input'));"
            "document.getElementById('ctrl-spacing').value = '1.9'; "
            "document.getElementById('ctrl-spacing').dispatchEvent(new Event('input'));"
        )
        page.wait_for_timeout(500)

        # ── 2. Scripture text centering — open Gen 1 with folio
        page.goto("http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
                  wait_until="networkidle")
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.click("#companion-toggle")
        page.wait_for_timeout(800)

        spread = page.evaluate(
            """
          () => {
            const reader = document.getElementById('reader');
            const scrCol = document.querySelector('.scripture-column');
            const folio = document.querySelector('.folio-column');
            const passage = scrCol.querySelector('.passage');
            const verseSpan = passage.querySelector('[data-pid]');
            return {
              readerRect: reader.getBoundingClientRect().toJSON(),
              scrColRect: scrCol.getBoundingClientRect().toJSON(),
              scrColPaddingLeft: getComputedStyle(scrCol).paddingLeft,
              folioRect: folio.getBoundingClientRect().toJSON(),
              passageRect: passage.getBoundingClientRect().toJSON(),
              verseRect: verseSpan ? verseSpan.getBoundingClientRect().toJSON() : null,
              markerCount: document.querySelectorAll('.cr-folio-marker').length,
            };
          }
        """
        )
        rd = spread['readerRect']
        sc = spread['scrColRect']
        fo = spread['folioRect']
        pa = spread['passageRect']
        print(f"\nLAYOUT (1440 viewport, folio visible):")
        print(f"  reader: {rd['x']:.0f} → {rd['right']:.0f} (width {rd['width']:.0f})")
        print(f"  scripture col: {sc['x']:.0f} → {sc['right']:.0f} "
              f"(padding-left {spread['scrColPaddingLeft']})")
        print(f"  folio col: {fo['x']:.0f} → {fo['right']:.0f}")
        print(f"  passage: {pa['x']:.0f} → {pa['right']:.0f}")
        # Scripture column itself should have explicit left padding > 0
        pl = float(spread['scrColPaddingLeft'].replace('px', ''))
        assert pl >= 40, f"scripture left padding too small: {pl}px"
        print(f"  OK — scripture column padding-left = {pl}px")
        # Folio markers still rendered
        assert spread['markerCount'] >= 5
        print(f"  OK — {spread['markerCount']} folio markers rendered")

        # ── Confirm folio cluster tracks verse top
        anchor_check = page.evaluate(
            """
          () => {
            const v = document.querySelector('.scripture-column [data-pid="gen.1.1"]');
            const c = document.querySelector('.cr-folio-cluster[data-anchor-pid="gen.1.1"]');
            return {
              verseTop: v.offsetTop,
              clusterTop: parseFloat(c.style.top || '0'),
            };
          }
        """
        )
        print(f"\n  gen.1.1 verse top={anchor_check['verseTop']} "
              f"cluster top={anchor_check['clusterTop']}")
        assert abs(anchor_check['clusterTop'] - anchor_check['verseTop']) <= 2
        print("  OK — folio cluster still aligned with gen.1.1 verse")

        page.screenshot(path="reports/v35_reading_room.png")

        # ── 3. Change reader-size in reading room — folio reflows,
        # but folio sizes stay fixed (already covered by v34); also
        # confirm scripture-column padding is unchanged.
        page.evaluate(
            "document.getElementById('ctrl-size').value = '24'; "
            "document.getElementById('ctrl-size').dispatchEvent(new Event('input'));"
        )
        page.wait_for_timeout(700)
        scaled = page.evaluate(
            """
          () => ({
            paddingLeft: getComputedStyle(document.querySelector('.scripture-column')).paddingLeft,
            folioFontSize: getComputedStyle(document.querySelector('.folio-column')).fontSize,
            scriptureSize: getComputedStyle(document.querySelector('.passage')).fontSize,
          })
        """
        )
        print(f"\nAFTER reader-size 24:")
        print(f"  scripture-col padding-left: {scaled['paddingLeft']}")
        print(f"  folio-col font-size: {scaled['folioFontSize']}")
        print(f"  scripture body font-size: {scaled['scriptureSize']}")
        assert scaled['paddingLeft'] == spread['scrColPaddingLeft']
        # folio-col font stays 18px (v34 fix)
        assert scaled['folioFontSize'] == '18px'
        page.screenshot(path="reports/v35_reading_size24.png")
        print("  OK — scripture body scales, folio + padding stable")

        b.close()
    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
