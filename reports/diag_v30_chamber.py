"""v30 — compact plate chamber + native tooltip removal."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.click("#companion-toggle")
        page.wait_for_timeout(800)

        # ── No native title attribute on markers ─────────────
        titles = page.evaluate(
            """
          () => Array.from(document.querySelectorAll('.cr-folio-marker'))
                 .map(m => m.getAttribute('title'))
        """
        )
        assert all(t is None for t in titles), (
            f"Found native title attr on {sum(1 for t in titles if t)} markers"
        )
        print(f"✓ No native title attr on any of {len(titles)} markers")

        # aria-label still present
        labels = page.evaluate(
            """
          () => Array.from(document.querySelectorAll('.cr-folio-marker'))
                 .map(m => m.getAttribute('aria-label'))
        """
        )
        assert all(labels), "Missing aria-label"
        print(f"✓ All {len(labels)} markers carry aria-label")

        # ── Plate chamber compactness ────────────────────────
        # Click the Doré plate marker
        page.evaluate(
            "Array.from(document.querySelectorAll('.cr-folio-marker'))"
            ".find(m => m.dataset.kind === 'plate').click()"
        )
        page.wait_for_timeout(700)

        chamber = page.evaluate(
            """
          () => {
            const img = document.querySelector('.folio-plate');
            const plaque = document.querySelector('.folio-plate-plaque');
            const wrap = document.querySelector('.folio-plate-wrap');
            const title = document.querySelector('.folio-plate-title');
            const verse = document.querySelector('.folio-plate-verse');
            const prov  = document.querySelector('.folio-plate-prov');
            const auth  = document.querySelector('.folio-plate-authority');
            return {
              viewportH: innerHeight,
              imgH: img.getBoundingClientRect().height,
              imgW: img.getBoundingClientRect().width,
              plaqueH: plaque.getBoundingClientRect().height,
              wrapH: wrap.getBoundingClientRect().height,
              wrapBottom: wrap.getBoundingClientRect().bottom,
              titleH: title?.getBoundingClientRect().height,
              versePresent: !!verse,
              provPresent: !!prov,
              authPresent: !!auth,
              titleFontSize: title ? getComputedStyle(title).fontSize : null,
              docOverflow: document.documentElement.scrollHeight - innerHeight,
              viewerScroll: document.getElementById('object-viewer').scrollTop,
            };
          }
        """
        )
        print(f"\nPlate chamber at 1440×900:")
        print(f"  image:     {chamber['imgW']:.0f} × {chamber['imgH']:.0f}")
        print(f"  plaque:    height {chamber['plaqueH']:.0f}")
        print(f"  wrap:      height {chamber['wrapH']:.0f}, bottom={chamber['wrapBottom']:.0f}")
        print(f"  title:     {chamber['titleFontSize']} (height {chamber['titleH']:.0f})")
        print(f"  doc overflow:  {chamber['docOverflow']}")
        print(f"  viewer scroll: {chamber['viewerScroll']}")
        assert chamber['wrapBottom'] <= chamber['viewportH'] + 1, (
            f"Chamber overflows viewport: {chamber['wrapBottom']} > {chamber['viewportH']}"
        )
        # Image height should be ≥ 80% of viewport
        assert chamber['imgH'] / chamber['viewportH'] >= 0.78
        # Plaque should be reasonably compact (was ~140px before)
        assert chamber['plaqueH'] <= 100, (
            f"Plaque still too tall: {chamber['plaqueH']}"
        )
        print(f"  image height / viewport = {chamber['imgH']/chamber['viewportH']:.0%}")
        print(f"  plaque height (target ≤ 100): {chamber['plaqueH']:.0f} ✓")
        page.screenshot(path="reports/v30_chamber_compact.png")

        # Verify outside-click still dismisses
        page.mouse.click(50, 50)
        page.wait_for_timeout(500)
        closed = not page.evaluate(
            "() => document.body.classList.contains('viewer-active')"
        )
        assert closed
        print("✓ Outside-click still dismisses chamber")

        # Open Doré again and capture
        page.evaluate(
            "Array.from(document.querySelectorAll('.cr-folio-marker'))"
            ".find(m => m.dataset.kind === 'plate').click()"
        )
        page.wait_for_timeout(700)
        page.screenshot(path="reports/v30_dore_compact.png")

        b.close()
    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
