"""v16 — scripture-sovereign architecture verification."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


def measure(page):
    return page.evaluate(
        """
      () => {
        const cr = document.querySelector('.cr-row');
        const passage = cr?.querySelector('.passage') || cr?.firstElementChild;
        const folio = document.getElementById('folio');
        const folioCS = folio ? getComputedStyle(folio) : null;
        return {
          passageRect: passage?.getBoundingClientRect().toJSON() || null,
          readerInnerW: document.getElementById('reader-inner').getBoundingClientRect().width,
          folioDisplay: folioCS?.display,
          folioPosition: folioCS?.position,
          folioRect: folio && folioCS?.display !== 'none'
            ? folio.getBoundingClientRect().toJSON() : null,
          marginWitnessesInScripture: document.querySelectorAll(
            '.cr-row .cr-margin-witness'
          ).length,
          folioWitnesses: Array.from(
            document.querySelectorAll('#folio .folio-witness')
          ).map(el => el.querySelector('.folio-title')?.textContent),
          // Total scripture stream height
          readerInnerHeight: document.getElementById('reader-inner').scrollHeight,
        };
      }
        """
    )


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
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

        # ── Genesis 1 ── across folio off / right / left ──────────────
        goto_chapter("gen.1")
        off = measure(page)
        page.screenshot(path="reports/v16_gen1_off.png")

        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        right = measure(page)
        page.screenshot(path="reports/v16_gen1_right.png")

        page.click("#companion-swap")
        page.wait_for_timeout(500)
        left = measure(page)
        page.screenshot(path="reports/v16_gen1_left.png")

        print("\n=== Genesis 1 — scripture invariance check ===")
        for label, s in [("off", off), ("right", right), ("left", left)]:
            r = s["passageRect"]
            print(
                f"  {label:5s}  passage left={r['left']:6.1f} right={r['right']:6.1f} "
                f"width={r['width']:6.1f}  scripture-stream-height={s['readerInnerHeight']:5d}  "
                f"folio-witnesses-in-scripture={s['marginWitnessesInScripture']}  "
                f"folio-sidebar={s['folioDisplay']}"
            )

        # Scripture must be byte-identical across all three states
        for s in [off, right, left]:
            assert s["marginWitnessesInScripture"] == 0, (
                "Witnesses leaked back into scripture stream"
            )
        # Passage rect identical in position, width, and height across all 3 states
        for attr in ("left", "right", "width", "top", "bottom", "height"):
            vals = [off["passageRect"][attr], right["passageRect"][attr], left["passageRect"][attr]]
            assert max(vals) - min(vals) <= 0.5, (
                f"Passage {attr} drifted: {vals}"
            )
        # Reader-inner width also constant
        widths = [off["readerInnerW"], right["readerInnerW"], left["readerInnerW"]]
        assert max(widths) - min(widths) <= 0.5, f"reader-inner width drifted: {widths}"
        # Total stream height constant
        heights = [off["readerInnerHeight"], right["readerInnerHeight"], left["readerInnerHeight"]]
        assert max(heights) - min(heights) <= 0.5, (
            f"Scripture stream height drifted: {heights} (alignment gaps)"
        )

        # Folio sidebar present when on
        assert off["folioDisplay"] == "none", f"Folio leaked when off: {off['folioDisplay']}"
        assert right["folioDisplay"] == "block"
        assert left["folioDisplay"] == "block"
        # Right vs left: sidebar position differs
        assert right["folioRect"]["right"] >= 1430, (
            f"folio not on right edge: {right['folioRect']}"
        )
        assert left["folioRect"]["left"] <= 10, f"folio not on left edge: {left['folioRect']}"
        # Witness present in both right and left
        assert "The Creation of Light" in right["folioWitnesses"]
        assert "The Creation of Light" in left["folioWitnesses"]

        # ── Genesis 4: 2 witnesses ────────────────────────────────────
        goto_chapter("gen.4")
        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        gen4 = measure(page)
        print(f"\nGenesis 4 folio witnesses: {gen4['folioWitnesses']}")
        assert len(gen4["folioWitnesses"]) == 2
        assert gen4["marginWitnessesInScripture"] == 0
        page.screenshot(path="reports/v16_gen4.png")

        # ── Genesis 11: 3 witnesses ───────────────────────────────────
        goto_chapter("gen.11")
        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        gen11 = measure(page)
        print(f"\nGenesis 11 folio witnesses: {gen11['folioWitnesses']}")
        assert len(gen11["folioWitnesses"]) == 3
        assert gen11["marginWitnessesInScripture"] == 0
        page.screenshot(path="reports/v16_gen11.png")

        # ── Object viewer still works ────────────────────────────────
        goto_chapter("gen.1")
        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        page.click('#folio .folio-witness')
        page.wait_for_timeout(700)
        viewer_open = page.evaluate(
            "() => document.body.classList.contains('viewer-active')"
        )
        assert viewer_open, "Clicking sidebar witness did not open viewer"
        page.mouse.click(50, 50)
        page.wait_for_timeout(500)
        viewer_closed = not page.evaluate(
            "() => document.body.classList.contains('viewer-active')"
        )
        assert viewer_closed
        print("\nObject viewer: open + outside-click dismiss work ✓")

        # ── TOC still unchanged ────────────────────────────────────────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json",
            wait_until="networkidle",
        )
        page.wait_for_selector(".bible-cover-layout", timeout=10000)
        page.wait_for_timeout(400)
        toc = page.evaluate(
            "() => ({ overflow: document.documentElement.scrollHeight - innerHeight, books: document.querySelectorAll('.bcl-canon-list li').length })"
        )
        assert toc["overflow"] == 0
        assert toc["books"] == 80
        print(f"TOC unchanged: overflow={toc['overflow']}, books={toc['books']} ✓")

        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
