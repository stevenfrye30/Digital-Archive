"""v18 — final polish verification.

  - Scripture invariance still holds at multiple viewport widths
  - Folio never overlaps scripture (collapses below 1320px)
  - Folio entries carry no thumbnail
  - Object viewer image >= 80% viewport height
  - Citation panel has shadow + small-caps header
  - Reading position preserved across Contents → re-enter cycle
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


def measure_scripture(page):
    return page.evaluate(
        """
      () => {
        const passage = document.querySelector('.cr-row .passage') || document.querySelector('.cr-row > :first-child');
        const folio = document.getElementById('folio');
        const folioCS = folio ? getComputedStyle(folio) : null;
        return {
          passageRect: passage?.getBoundingClientRect().toJSON() || null,
          folioDisplay: folioCS?.display,
          folioRect: folio && folioCS?.display !== 'none' ? folio.getBoundingClientRect().toJSON() : null,
          folioWidth: folioCS && folioCS.display !== 'none' ? folio.getBoundingClientRect().width : null,
        };
      }
        """
    )


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()

        # ─── 1440×900: standard ───
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        def goto_chapter(ch):
            page.goto(
                f"http://localhost:8765/index.html?text=bible_kjv.json&p={ch}.1",
                wait_until="networkidle",
            )
            page.wait_for_function(
                "typeof currentData === 'object' && currentData && currentData.passages",
                timeout=15000,
            )
            page.wait_for_timeout(500)

        # Scripture invariance check at 1440
        goto_chapter("gen.1")
        off = measure_scripture(page)
        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        right = measure_scripture(page)
        page.click("#companion-swap")
        page.wait_for_timeout(500)
        left = measure_scripture(page)

        print("=== Scripture invariance at 1440×900 ===")
        for label, s in [("off", off), ("right", right), ("left", left)]:
            r = s["passageRect"]
            print(
                f"  {label:5s}  passage left={r['left']:6.1f} right={r['right']:6.1f} "
                f"width={r['width']:6.1f}  folio={s['folioWidth']}"
            )

        for attr in ("left", "right", "width"):
            vals = [off["passageRect"][attr], right["passageRect"][attr], left["passageRect"][attr]]
            assert max(vals) - min(vals) <= 0.5, f"Passage {attr} drifted: {vals}"

        # Folio width in target range, no overlap
        assert 180 <= right["folioWidth"] <= 280
        assert right["folioRect"]["left"] >= right["passageRect"]["right"], "Folio overlaps scripture on right"
        assert left["folioRect"]["right"] <= left["passageRect"]["left"], "Folio overlaps scripture on left"

        # No thumbnails in folio
        thumb_count = page.evaluate("() => document.querySelectorAll('.cr-folio-thumb').length")
        assert thumb_count == 0, f"Folio still has {thumb_count} thumbnails"
        page.screenshot(path="reports/v18_gen1_folio_right.png")

        # ─── Test responsive collapse below 1320px ───
        ctx2 = b.new_context(viewport={"width": 1280, "height": 800})
        page2 = ctx2.new_page()
        page2.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
            wait_until="networkidle",
        )
        page2.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page2.wait_for_timeout(500)
        page2.click("#companion-toggle")
        page2.wait_for_timeout(500)
        narrow = measure_scripture(page2)
        print(f"\n=== Narrow viewport 1280×800 ===")
        print(f"  scripture: {narrow['passageRect']['width']:.0f}px  folio display: {narrow['folioDisplay']}")
        # Scripture remains at 960; folio collapsed
        assert abs(narrow["passageRect"]["width"] - 960) <= 1, (
            f"Scripture compressed at 1280: width={narrow['passageRect']['width']}"
        )
        assert narrow["folioDisplay"] == "none", "Folio should collapse below 1320px"
        page2.screenshot(path="reports/v18_narrow_viewport.png")
        ctx2.close()

        # ─── Object viewer monumental check ───
        page.evaluate("document.querySelector('.cr-folio-entry').click()")
        page.wait_for_timeout(700)
        plate = page.evaluate(
            """
          () => {
            const img = document.querySelector('.folio-plate');
            const plaque = document.querySelector('.folio-plate-plaque');
            return {
              h: img.getBoundingClientRect().height,
              vp: innerHeight,
              plaqueBottom: plaque.getBoundingClientRect().bottom,
              backdropBg: getComputedStyle(document.getElementById('object-viewer')).backgroundImage,
            };
          }
        """
        )
        print(f"\n=== Object viewer ===")
        print(f"  image: {plate['h']:.0f}px ({plate['h']/plate['vp']:.0%} of viewport)")
        print(f"  plaque bottom: {plate['plaqueBottom']:.0f}")
        assert plate["h"] / plate["vp"] >= 0.80
        assert plate["plaqueBottom"] <= plate["vp"]
        assert "radial-gradient" in plate["backdropBg"]
        page.screenshot(path="reports/v18_object_viewer.png")
        page.mouse.click(50, 50)
        page.wait_for_timeout(700)
        assert not page.evaluate(
            "() => document.body.classList.contains('viewer-active')"
        )

        # ─── Navigation memo: contents → re-enter restores scroll ───
        # Scroll halfway down
        page.evaluate("document.getElementById('reader').scrollTop = 800")
        page.wait_for_timeout(300)
        before_scroll = page.evaluate("() => document.getElementById('reader').scrollTop")
        before_folio_left = page.evaluate("() => document.body.classList.contains('folio-left')")
        before_companion = page.evaluate("() => document.body.classList.contains('companion-mode')")
        # Go to Contents
        page.click("#ctrl-contents")
        page.wait_for_timeout(500)
        # Re-enter same chapter
        page.evaluate("document.querySelector('.bcl-canon-list li').click()")
        page.wait_for_timeout(700)
        after_scroll = page.evaluate("() => document.getElementById('reader').scrollTop")
        after_folio_left = page.evaluate("() => document.body.classList.contains('folio-left')")
        after_companion = page.evaluate("() => document.body.classList.contains('companion-mode')")
        print(f"\n=== Navigation memo ===")
        print(f"  scroll  {before_scroll} → {after_scroll}")
        print(f"  folio-left  {before_folio_left} → {after_folio_left}")
        print(f"  companion-mode  {before_companion} → {after_companion}")
        assert abs(after_scroll - before_scroll) <= 5, (
            f"Reading scroll not restored: {before_scroll} → {after_scroll}"
        )
        assert after_companion == before_companion
        assert after_folio_left == before_folio_left

        # ─── Citation panel ───
        page.goto("http://localhost:8765/index.html?text=bible_kjv.json", wait_until="networkidle")
        page.wait_for_selector(".bible-cover-layout", timeout=10000)
        page.wait_for_timeout(400)
        page.click(".cite-corner > summary")
        page.wait_for_timeout(300)
        cite = page.evaluate(
            """
          () => {
            const panel = document.querySelector('.cite-corner .cc-citations');
            return {
              boxShadow: getComputedStyle(panel).boxShadow,
              hasBefore: !!getComputedStyle(panel, '::before').content,
              beforeContent: getComputedStyle(panel, '::before').content,
              w: panel.getBoundingClientRect().width,
            };
          }
        """
        )
        print(f"\n=== Citation panel ===")
        print(f"  width: {cite['w']:.0f}, box-shadow: {cite['boxShadow'][:80]}…")
        print(f"  ::before content: {cite['beforeContent']}")
        assert "rgba" in cite["boxShadow"]  # has actual shadow
        assert "Citation" in cite["beforeContent"]  # has rubric label
        page.screenshot(path="reports/v18_cite_panel.png")

        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
