"""v56 — Codex reading consolidation.

Captures verification screenshots and confirms structural CSS
changes applied. Not exhaustive — the user explicitly asked
for screenshots-sufficient verification.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import re
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()

        # ── Desktop verification (1440x900) ─────────────────────
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.17.7",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.evaluate("() => localStorage.removeItem('atlas:encounters:v1')")
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(700)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        page.evaluate("_openFolioObject('gen17-covenant-formula')")
        page.wait_for_timeout(1500)

        atmosphere = page.evaluate(
            """
          () => {
            const lede = document.querySelector('.folio-leaf [class*="-lede"]');
            const anchorings = document.querySelector('.folio-leaf .cc-anchorings');
            const archive = document.querySelector('.folio-leaf .cc-archive');
            const kindredItem = document.querySelector('.folio-leaf .cc-kindred-item');
            const resonanceItem = document.querySelector('.folio-leaf .cc-resonance-item');
            return {
              ledeMaxWidth: lede ? getComputedStyle(lede).maxWidth : null,
              anchoringsMaxWidth: anchorings ? getComputedStyle(anchorings).maxWidth : null,
              archiveMaxWidth: archive ? getComputedStyle(archive).maxWidth : null,
              kindredColor: kindredItem ? getComputedStyle(kindredItem).color : null,
              resonanceColor: resonanceItem ? getComputedStyle(resonanceItem).color : null,
            };
          }
        """
        )
        print("Desktop atmospherics (covenant chamber at gen.17.7):")
        print(f"  lede max-width:       {atmosphere['ledeMaxWidth']}")
        print(f"  anchorings max-width: {atmosphere['anchoringsMaxWidth']}")
        print(f"  archive max-width:    {atmosphere['archiveMaxWidth']}")
        print(f"  kindred item color:   {atmosphere['kindredColor']}")
        print(f"  resonance item color: {atmosphere['resonanceColor']}")
        # Reading-measure constraints applied
        # (originating-gravity narrows lede to 540px; the universal
        # rule at 640px applies only at echoes; check anchorings)
        assert "620" in (atmosphere["anchoringsMaxWidth"] or "")
        assert "680" in (atmosphere["archiveMaxWidth"] or "")
        # Kindred + resonance items recede slightly (alpha drops)
        def alpha(s):
            m = re.search(r"rgba\(.+,\s*([\d.]+)\)", s or "")
            return float(m.group(1)) if m else 1.0
        ralpha = alpha(atmosphere["resonanceColor"])
        print(f"  resonance alpha: {ralpha}")
        # New softer resonance value: 0.74
        assert 0.72 <= ralpha <= 0.76
        # Kindred only renders when same-verse co-presence exists.
        # gen.17.7 hosts only AO·006, so no kindred line here.
        if atmosphere["kindredColor"]:
            kalpha = alpha(atmosphere["kindredColor"])
            print(f"  kindred alpha: {kalpha}")
            assert 0.76 <= kalpha <= 0.80
        print("  OK — reading measures + folio-weight softening applied\n")

        page.screenshot(path="reports/v56_desktop_covenant.png")

        # Confirm kindred softening at a verse where kindred renders
        page.evaluate("_closeFolioObject && _closeFolioObject()")
        page.wait_for_timeout(400)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.6",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(500)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        page.evaluate("_openFolioObject('gen1-cosmology-firmament')")
        page.wait_for_timeout(1200)
        kindred_alpha = page.evaluate(
            """
          () => {
            const k = document.querySelector('.cc-kindred-item');
            return k ? getComputedStyle(k).color : null;
          }
        """
        )
        print(f"Kindred at gen.1.6 (where co-presence exists): {kindred_alpha}")
        kalpha = alpha(kindred_alpha)
        print(f"  kindred alpha: {kalpha}")
        assert 0.76 <= kalpha <= 0.80
        print("  OK — kindred softened to 0.78\n")
        ctx.close()

        # ── Narrow viewport (380x800) ──────────────────────────
        ctx2 = b.new_context(viewport={"width": 380, "height": 800})
        page2 = ctx2.new_page()
        page2.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=exo.40.34",
            wait_until="networkidle",
        )
        page2.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page2.wait_for_timeout(1000)
        # On narrow widths the folio button may be repositioned;
        # the chapter-room flow may differ. We just confirm the
        # vocabulary grid stacks via direct media query check.
        narrow = page2.evaluate(
            """
          () => {
            // We're below 600px — the media query should apply.
            const probe = document.createElement('div');
            probe.className = 'cc-terms';
            probe.innerHTML = '<div class="cc-term-row"></div>';
            document.body.appendChild(probe);
            const row = probe.querySelector('.cc-term-row');
            const cs = getComputedStyle(row);
            const cols = cs.gridTemplateColumns;
            probe.remove();
            return {
              viewport: window.innerWidth,
              cosmologyGridCols: cols,
            };
          }
        """
        )
        print(f"Narrow viewport (380px):")
        print(f"  cc-term-row grid-template-columns: {narrow['cosmologyGridCols']}")
        # On narrow widths, grid should be single column (a single
        # track width, no "px 1fr" pattern). The CSS rule says
        # `grid-template-columns: 1fr` — computed as the inner
        # width of the parent in px or "1fr"-equivalent.
        cols = narrow["cosmologyGridCols"] or ""
        # Either "1fr", "<width>px" (single track), or contains a single
        # number. Multi-column would have "140px 1fr" → two tracks.
        track_count = len([t for t in cols.split() if t])
        assert track_count == 1, f"vocabulary grid still multi-column on narrow: {cols}"
        print("  OK — vocabulary grid stacks to single column under 600px\n")

        # Capture a narrow-viewport screenshot of the title leaf
        page2.screenshot(path="reports/v56_narrow_title.png")
        ctx2.close()

        # ── Print emulation ────────────────────────────────────
        ctx3 = b.new_context(viewport={"width": 1024, "height": 900})
        page3 = ctx3.new_page()
        page3.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.6",
            wait_until="networkidle",
        )
        page3.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page3.wait_for_timeout(800)
        page3.evaluate("document.getElementById('companion-toggle').click()")
        page3.wait_for_timeout(500)
        page3.evaluate("_setFolioDepth('archive')")
        page3.wait_for_timeout(400)
        page3.evaluate("_openFolioObject('gen1-cosmology-firmament')")
        page3.wait_for_timeout(1200)
        # Emulate print media
        page3.emulate_media(media="print")
        page3.wait_for_timeout(400)
        print_state = page3.evaluate(
            """
          () => {
            const viewer = document.getElementById('object-viewer');
            const leaf = document.querySelector('.folio-leaf');
            const plaque = document.querySelector('.cc-resonance-plaque');
            return {
              viewerBg: viewer ? getComputedStyle(viewer).backgroundColor : null,
              viewerPosition: viewer ? getComputedStyle(viewer).position : null,
              leafAnimation: leaf ? getComputedStyle(leaf).animationName : null,
              plaqueDisplay: plaque ? getComputedStyle(plaque).display : null,
            };
          }
        """
        )
        print(f"Print emulation:")
        print(f"  viewer background: {print_state['viewerBg']}")
        print(f"  viewer position:   {print_state['viewerPosition']}")
        print(f"  leaf animation:    {print_state['leafAnimation']}")
        print(f"  plaque display:    {print_state['plaqueDisplay']}")
        # In print: viewer becomes static + white, leaf animation is
        # disabled, plaques are hidden.
        assert print_state["viewerPosition"] == "static"
        assert print_state["leafAnimation"] in ("none", "")
        assert print_state["plaqueDisplay"] == "none"
        print("  OK — print media collapses chrome, disables animations, hides hover plaques\n")
        page3.screenshot(path="reports/v56_print_emulation.png")

        b.close()
    print("ALL CHECKS PASSED — codex reading consolidation in place")


if __name__ == "__main__":
    main()
