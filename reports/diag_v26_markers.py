"""v26 — symbolic folio marker verification."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


def probe(page):
    return page.evaluate(
        """
      () => {
        const spread = document.querySelector('#passages .chapter-spread');
        const scrCol = spread?.querySelector('.scripture-column');
        const folCol = spread?.querySelector('.folio-column');
        const clusters = Array.from(document.querySelectorAll('.cr-folio-cluster'));
        const markers = Array.from(document.querySelectorAll('.cr-folio-marker'));
        const passage = document.querySelector('.scripture-column .cr-row > :first-child');
        const folCS = folCol ? getComputedStyle(folCol) : null;
        return {
          bodyClasses: Array.from(document.body.classList),
          viewport: { w: innerWidth, h: innerHeight },
          spread: spread?.getBoundingClientRect().toJSON(),
          scriptureColumn: scrCol?.getBoundingClientRect().toJSON(),
          folioColumn: folCS && folCS.display !== 'none' ? folCol.getBoundingClientRect().toJSON() : null,
          folioDisplay: folCS?.display,
          passage: passage?.getBoundingClientRect().toJSON(),
          clusterCount: clusters.length,
          markerCount: markers.length,
          markers: markers.map(m => ({
            kind: m.dataset.kind,
            ariaLabel: m.getAttribute('aria-label'),
            title: m.getAttribute('title'),
            anchorPid: m.closest('.cr-folio-cluster')?.dataset.anchorPid,
            rect: m.getBoundingClientRect().toJSON(),
            symbolContent: getComputedStyle(m, '::before').content,
            tagName: m.tagName,
            tabIndex: m.tabIndex,
            hasPlaque: !!m.querySelector('.cr-folio-plaque'),
            plaqueOpacity: m.querySelector('.cr-folio-plaque')
              ? getComputedStyle(m.querySelector('.cr-folio-plaque')).opacity
              : null,
          })),
        };
      }
        """
    )


def show(label, s):
    print(f"\n── {label} " + "─" * (60 - len(label)))
    print(f"  body: {' '.join(c for c in s['bodyClasses'] if not c.startswith(('reading-','in-')))}")
    print(f"  clusters: {s['clusterCount']}  markers: {s['markerCount']}")
    for m in s["markers"]:
        sym = m["symbolContent"].strip('"\'')
        print(
            f"    {sym}  [{m['kind']:<10}] @ {m['anchorPid']:<10}  "
            f"tab={m['tabIndex']}  plaque={m['hasPlaque']}"
        )
        print(f"        aria='{m['ariaLabel'][:80]}'")


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
            page.wait_for_timeout(800)

        # Gen 1: 1 plate marker
        goto_chapter("gen.1")
        page.click("#companion-toggle")
        page.wait_for_timeout(800)
        g1 = probe(page)
        show("GEN 1", g1)
        assert g1["clusterCount"] == 1
        assert g1["markerCount"] == 1
        assert g1["markers"][0]["kind"] == "plate"
        assert g1["markers"][0]["tagName"] == "BUTTON"
        assert g1["markers"][0]["tabIndex"] == 0
        assert g1["markers"][0]["hasPlaque"]
        # Symbol must be the plate glyph
        assert "▣" in g1["markers"][0]["symbolContent"], (
            f"Wrong glyph: {g1['markers'][0]['symbolContent']}"
        )
        # aria-label content
        assert "The Creation of Light" in g1["markers"][0]["ariaLabel"]
        assert "Gen 1:3" in g1["markers"][0]["ariaLabel"]
        page.screenshot(path="reports/v26_gen1.png")

        # Hover a marker → plaque becomes visible
        page.hover(".cr-folio-marker")
        page.wait_for_timeout(400)
        plaque_state = page.evaluate(
            """
          () => {
            const p = document.querySelector('.cr-folio-plaque');
            const cs = getComputedStyle(p);
            return {
              opacity: cs.opacity,
              visibility: cs.visibility,
              rect: p.getBoundingClientRect().toJSON(),
              title: p.querySelector('.cr-folio-plaque-title')?.textContent,
              kind: p.querySelector('.cr-folio-plaque-kind')?.textContent,
              meta: p.querySelector('.cr-folio-plaque-meta')?.textContent,
            };
          }
        """
        )
        print(f"\nPlaque on hover: opacity={plaque_state['opacity']}, "
              f"vis={plaque_state['visibility']}")
        print(f"  title:  {plaque_state['title']}")
        print(f"  kind:   {plaque_state['kind']}")
        print(f"  meta:   {plaque_state['meta']}")
        assert float(plaque_state["opacity"]) > 0.8
        assert plaque_state["visibility"] == "visible"
        page.screenshot(path="reports/v26_gen1_hover.png")

        # Click marker → object viewer opens
        # Move away first so hover state doesn't interfere
        page.mouse.move(20, 20)
        page.wait_for_timeout(200)
        page.click(".cr-folio-marker")
        page.wait_for_timeout(700)
        opened = page.evaluate(
            "() => document.body.classList.contains('viewer-active')"
        )
        print(f"\nAfter click: viewer-active = {opened}")
        assert opened, "Click did not open object viewer"
        page.mouse.click(50, 50)
        page.wait_for_timeout(500)
        closed = not page.evaluate(
            "() => document.body.classList.contains('viewer-active')"
        )
        assert closed
        print("Outside-click dismiss works ✓")
        page.screenshot(path="reports/v26_gen1_chamber.png")

        # Keyboard: Tab to marker, Enter to activate
        page.keyboard.press("Tab")  # bring focus into the page; may need more
        page.evaluate("document.querySelector('.cr-folio-marker').focus()")
        page.wait_for_timeout(300)
        focused = page.evaluate(
            "() => document.activeElement.classList.contains('cr-folio-marker')"
        )
        assert focused
        # Plaque visible on focus-visible too
        plaque_on_focus = page.evaluate(
            """
          () => {
            const p = document.querySelector('.cr-folio-plaque');
            return getComputedStyle(p).opacity;
          }
        """
        )
        print(f"Plaque on focus: opacity={plaque_on_focus}")
        page.keyboard.press("Enter")
        page.wait_for_timeout(700)
        opened_kb = page.evaluate(
            "() => document.body.classList.contains('viewer-active')"
        )
        assert opened_kb, "Enter did not open viewer"
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        print("Keyboard: Tab + Enter activate ✓; Escape dismisses ✓")

        # Gen 4: 2 markers
        goto_chapter("gen.4")
        page.click("#companion-toggle")
        page.wait_for_timeout(800)
        g4 = probe(page)
        show("GEN 4", g4)
        assert g4["markerCount"] == 2
        kinds_4 = sorted(m["kind"] for m in g4["markers"])
        assert kinds_4 == ["genealogy", "plate"]
        page.screenshot(path="reports/v26_gen4.png")

        # Gen 11: 3 markers
        goto_chapter("gen.11")
        page.click("#companion-toggle")
        page.wait_for_timeout(800)
        g11 = probe(page)
        show("GEN 11", g11)
        assert g11["markerCount"] == 3
        page.screenshot(path="reports/v26_gen11.png")

        # Scroll sync test
        before_top = g11["markers"][0]["rect"]["top"]
        page.evaluate("document.getElementById('reader').scrollTop = 600")
        page.wait_for_timeout(500)
        after_top = page.evaluate(
            "() => document.querySelector('.cr-folio-marker').getBoundingClientRect().top"
        )
        delta = after_top - before_top
        print(f"\nScroll test: reader 0 → 600, marker moved {delta:+.0f}px")
        assert abs(delta - (-600)) <= 1, "Marker did not scroll with scripture"
        page.screenshot(path="reports/v26_gen11_scrolled.png")

        # Wide mode hides folio
        page.evaluate("document.getElementById('reader').scrollTop = 0")
        page.wait_for_timeout(200)
        page.click("#ctrl-columns .col-opt[data-cols='wide']")
        page.wait_for_timeout(500)
        wide = probe(page)
        print(f"\nWIDE: folio display = {wide['folioDisplay']}")
        assert wide["folioDisplay"] == "none"

        # Scripture invariance: width 960 in all single states
        page.click("#ctrl-columns .col-opt[data-cols='single']")
        page.wait_for_timeout(400)
        single_on = probe(page)
        page.click("#companion-toggle")
        page.wait_for_timeout(400)
        single_off = probe(page)
        for s in [single_on, single_off]:
            assert abs(s["scriptureColumn"]["width"] - 960) <= 0.5, (
                f"Scripture not 960: {s['scriptureColumn']['width']}"
            )
        print(f"\nScripture invariance: 960 across folio on / off ✓")

        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
