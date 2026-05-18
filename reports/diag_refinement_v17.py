"""v17 — richer folio sidebar, scripture still byte-identical."""
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
        const entries = Array.from(document.querySelectorAll('.cr-folio-entry'));
        return {
          passageRect: passage?.getBoundingClientRect().toJSON() || null,
          readerInnerW: document.getElementById('reader-inner').getBoundingClientRect().width,
          folioDisplay: folioCS?.display,
          folioWidth: folioCS && folioCS.display !== 'none'
            ? folio.getBoundingClientRect().width : null,
          folioRect: folio && folioCS?.display !== 'none'
            ? folio.getBoundingClientRect().toJSON() : null,
          marginWitnessesInScripture: document.querySelectorAll(
            '.cr-row .cr-margin-witness'
          ).length,
          entryCount: entries.length,
          entries: entries.map(el => ({
            kind: el.dataset.kind,
            title: el.querySelector('.cr-folio-title')?.textContent,
            hasThumb: !!el.querySelector('.cr-folio-thumb'),
            meta: el.querySelector('.cr-folio-meta')?.textContent,
          })),
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

        # ── Genesis 1 ── scripture invariance ─────────────────────────
        goto_chapter("gen.1")
        off = measure(page)
        page.screenshot(path="reports/v17_gen1_off.png")

        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        right = measure(page)
        page.screenshot(path="reports/v17_gen1_right.png")

        page.click("#companion-swap")
        page.wait_for_timeout(500)
        left = measure(page)
        page.screenshot(path="reports/v17_gen1_left.png")

        print("\n=== Genesis 1 — scripture invariance ===")
        for label, s in [("off", off), ("right", right), ("left", left)]:
            r = s["passageRect"]
            print(
                f"  {label:5s}  passage left={r['left']:6.1f} right={r['right']:6.1f} "
                f"width={r['width']:6.1f}  stream-height={s['readerInnerHeight']:5d}  "
                f"folio-width={s['folioWidth']}  inline-witnesses={s['marginWitnessesInScripture']}"
            )

        # Scripture: byte-identical across all three states
        for s in [off, right, left]:
            assert s["marginWitnessesInScripture"] == 0
        for attr in ("left", "right", "width", "top", "bottom", "height"):
            vals = [off["passageRect"][attr], right["passageRect"][attr], left["passageRect"][attr]]
            assert max(vals) - min(vals) <= 0.5, (
                f"Passage {attr} drifted: {vals}"
            )
        heights = [off["readerInnerHeight"], right["readerInnerHeight"], left["readerInnerHeight"]]
        assert max(heights) - min(heights) <= 0.5, (
            f"Scripture stream height drifted: {heights}"
        )

        # Folio sidebar width 220-280 range
        assert 220 <= right["folioWidth"] <= 280, (
            f"Folio width out of range: {right['folioWidth']}"
        )

        # Right vs left positioning
        vp_w = 1440
        assert right["folioRect"]["right"] >= vp_w - 1
        assert left["folioRect"]["left"] <= 1

        # NO overlap with scripture
        assert right["folioRect"]["left"] >= right["passageRect"]["right"], (
            f"Folio overlaps scripture (right): folio.left={right['folioRect']['left']} "
            f"passage.right={right['passageRect']['right']}"
        )
        assert left["folioRect"]["right"] <= left["passageRect"]["left"], (
            f"Folio overlaps scripture (left): folio.right={left['folioRect']['right']} "
            f"passage.left={left['passageRect']['left']}"
        )

        # Thumbnail present for plate kind
        plate_entry = next((e for e in right["entries"] if e["kind"] == "plate"), None)
        assert plate_entry is not None
        assert plate_entry["hasThumb"], "Plate entry missing thumbnail"
        # Plate metadata includes artist + year
        assert "Doré" in plate_entry["meta"], (
            f"Plate metadata missing artist: {plate_entry['meta']}"
        )

        # ── Genesis 4: 2 witnesses, plate one carries thumbnail ───────
        goto_chapter("gen.4")
        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        gen4 = measure(page)
        print(f"\nGenesis 4 entries: {gen4['entryCount']}")
        for e in gen4["entries"]:
            print(f"  [{e['kind']}] thumb={e['hasThumb']}  {e['title']}")
        assert gen4["entryCount"] == 2
        assert gen4["marginWitnessesInScripture"] == 0
        plate_count = sum(1 for e in gen4["entries"] if e["kind"] == "plate" and e["hasThumb"])
        assert plate_count == 1, f"Expected 1 thumbnail in gen.4, got {plate_count}"
        page.screenshot(path="reports/v17_gen4.png")

        # ── Genesis 11: 3 witnesses ───────────────────────────────────
        goto_chapter("gen.11")
        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        gen11 = measure(page)
        print(f"\nGenesis 11 entries: {gen11['entryCount']}")
        for e in gen11["entries"]:
            print(f"  [{e['kind']}] thumb={e['hasThumb']}  {e['title']}")
        assert gen11["entryCount"] == 3
        assert gen11["marginWitnessesInScripture"] == 0
        page.screenshot(path="reports/v17_gen11.png")

        # ── Object viewer still works ────────────────────────────────
        goto_chapter("gen.1")
        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        page.click(".cr-folio-entry")
        page.wait_for_timeout(700)
        viewer_open = page.evaluate(
            "() => document.body.classList.contains('viewer-active')"
        )
        assert viewer_open
        # measure image
        plate = page.evaluate(
            "() => { const i = document.querySelector('.folio-plate'); return { h: i.getBoundingClientRect().height, vp: innerHeight }; }"
        )
        print(f"Object viewer plate height: {plate['h']:.0f}px ({plate['h']/plate['vp']:.0%} of viewport)")
        assert plate["h"] / plate["vp"] >= 0.78
        page.screenshot(path="reports/v17_object_viewer.png")
        page.mouse.click(50, 50)
        page.wait_for_timeout(500)
        assert not page.evaluate(
            "() => document.body.classList.contains('viewer-active')"
        )

        # ── TOC unchanged ────────────────────────────────────────────
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

        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
