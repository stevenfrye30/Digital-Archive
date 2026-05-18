"""v15 — verify text column is stable across folio toggle and side."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


def measure_passage(page, label):
    """Return passage rect of the first verse in chapter."""
    return page.evaluate(
        """
      (label) => {
        const row = document.querySelector('.cr-row');
        if (!row) return { label, missing: true };
        const passage = row.querySelector('.passage') || row.firstElementChild;
        const witnesses = Array.from(
          document.querySelectorAll('.cr-margin-witness:not([hidden])')
        ).filter(w => getComputedStyle(w).display !== 'none');
        return {
          label,
          passageRect: passage.getBoundingClientRect().toJSON(),
          witnessCount: witnesses.length,
          witnessTitles: witnesses.map(w => w.querySelector('.cr-mw-title')?.textContent),
          firstWitnessRect: witnesses[0]?.getBoundingClientRect().toJSON() || null,
          readerInnerWidth: document.getElementById('reader-inner').getBoundingClientRect().width,
        };
      }
        """,
        label,
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
            page.wait_for_timeout(400)

        # ---- Genesis 1: text column stability across 3 states ----
        goto_chapter("gen.1")
        off = measure_passage(page, "folio off")
        page.screenshot(path="reports/v15_gen1_folio_off.png")
        # folio on, right side
        page.click("#companion-toggle")
        page.wait_for_timeout(400)
        right = measure_passage(page, "folio right")
        page.screenshot(path="reports/v15_gen1_folio_right.png")
        # folio on, left side
        page.click("#companion-swap")
        page.wait_for_timeout(400)
        left = measure_passage(page, "folio left")
        page.screenshot(path="reports/v15_gen1_folio_left.png")

        print("\n=== Genesis 1 passage rect across folio states ===")
        for s in [off, right, left]:
            r = s["passageRect"]
            print(
                f"  {s['label']:14s}  left={r['left']:6.1f}  right={r['right']:6.1f}  "
                f"width={r['width']:6.1f}  readerInner={s['readerInnerWidth']:6.1f}  "
                f"witnesses={s['witnessCount']}"
            )

        # Text column WIDTH must be constant across all three states
        widths = [off["passageRect"]["width"], right["passageRect"]["width"], left["passageRect"]["width"]]
        assert max(widths) - min(widths) <= 1, (
            f"Text column width drifted: {widths}"
        )

        # Verify witness placement: folio-right witness is to the RIGHT of passage,
        # folio-left witness is to the LEFT of passage.
        assert right["firstWitnessRect"]["left"] > right["passageRect"]["right"], (
            "Folio-right witness should be to the right of passage"
        )
        assert left["firstWitnessRect"]["right"] < left["passageRect"]["left"], (
            "Folio-left witness should be to the left of passage"
        )

        # ---- Genesis 4: should show both witnesses ----
        goto_chapter("gen.4")
        page.click("#companion-toggle")
        page.wait_for_timeout(400)
        gen4 = measure_passage(page, "gen.4")
        print(f"\n=== Genesis 4 witnesses: {gen4['witnessCount']} ===")
        for t in gen4["witnessTitles"]:
            print(f"  - {t}")
        assert gen4["witnessCount"] == 2, (
            f"Expected 2 witnesses in Gen 4, got {gen4['witnessCount']}: {gen4['witnessTitles']}"
        )
        page.screenshot(path="reports/v15_gen4_folio_on.png")

        # ---- Genesis 11: should show three witnesses ----
        goto_chapter("gen.11")
        page.click("#companion-toggle")
        page.wait_for_timeout(400)
        gen11 = measure_passage(page, "gen.11")
        print(f"\n=== Genesis 11 witnesses: {gen11['witnessCount']} ===")
        for t in gen11["witnessTitles"]:
            print(f"  - {t}")
        assert gen11["witnessCount"] == 3, (
            f"Expected 3 witnesses in Gen 11, got {gen11['witnessCount']}: {gen11['witnessTitles']}"
        )
        page.screenshot(path="reports/v15_gen11_folio_on.png")

        # ---- Object viewer still works ----
        goto_chapter("gen.1")
        page.click("#companion-toggle")
        page.wait_for_timeout(400)
        page.click('.cr-margin-witness[data-kind="plate"]')
        page.wait_for_timeout(600)
        viewer_open = page.evaluate(
            "() => document.body.classList.contains('viewer-active')"
        )
        assert viewer_open
        page.mouse.click(50, 50)  # outside click dismisses
        page.wait_for_timeout(500)
        viewer_closed = not page.evaluate(
            "() => document.body.classList.contains('viewer-active')"
        )
        assert viewer_closed
        print("\nObject viewer: open + outside-click dismiss work ✓")

        # ---- TOC unchanged ----
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json",
            wait_until="networkidle",
        )
        page.wait_for_selector(".bible-cover-layout", timeout=10000)
        page.wait_for_timeout(400)
        toc = page.evaluate(
            """
          () => ({
            docOverflow: document.documentElement.scrollHeight - innerHeight,
            books: document.querySelectorAll('.bcl-canon-list li').length,
          })
        """
        )
        print(f"\nTOC: overflow={toc['docOverflow']}, books={toc['books']}")
        assert toc["docOverflow"] == 0
        assert toc["books"] == 80

        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
