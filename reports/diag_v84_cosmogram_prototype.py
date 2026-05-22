"""v84 — The Cosmogram Prototype verification.

Verifies the masterpiece-prototype move: a tall vertically-
descending manuscript cosmogram becomes the cosmology chamber's
centerpiece artifact.

The new SVG composition (viewBox 480 × 880, portrait) shows
five cosmographic strata stacked top-to-bottom:

  I.   MAYIM MĒʿAL LĀ-RĀQÎAʿ   (the upper cosmic waters)
  II.  RĀQÎAʿ                  (the firmament — sky-vault)
  III. ʾEREṢ                   (the earth — disc on pillars)
  IV.  MAYIM MITTAḤAT LĀ-RĀQÎAʿ (the lower waters — tehôm)
  V.   SHEOL                   (the depths — shadow-land)

A dashed cosmic axis runs the full height. Each stratum carries
its Hebrew name (transliterated, small-caps, italic), an English
gloss, and a symbolic typographic mark (water pattern, firmament
dome with celestial bodies, earth horizon with pillars, lower
waters, descent into Sheol).

The composition is line-and-type only — no colored fills, no
educational chrome, no infographic logic. The reader's eye
descends through the cosmos.

No regressions: cosmology AO chamber preserved (now enhanced),
all other chambers preserved, families preserved, Doré
preserved.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


def open_leaf(page, pid, rec_id):
    page.goto(
        f"http://localhost:8765/index.html?text=bible_kjv.json&p={pid}",
        wait_until="networkidle",
    )
    page.wait_for_function(
        "typeof currentData === 'object' && currentData && currentData.passages",
        timeout=15000,
    )
    page.wait_for_timeout(700)
    page.evaluate("() => localStorage.removeItem('atlas:encounters:v1')")
    page.evaluate("() => localStorage.removeItem('archive:records-seen:v1')")
    page.evaluate("document.getElementById('companion-toggle').click()")
    page.wait_for_timeout(500)
    page.evaluate("_setFolioDepth('archive')")
    page.wait_for_timeout(400)
    page.evaluate(f"(() => _openFolioObject('{rec_id}'))()")
    page.wait_for_timeout(1500)


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 2400})
        page = ctx.new_page()

        # ── The Cosmogram ──────────────────────────────────────────
        print("=== The Cosmogram (masterpiece prototype) ===")
        open_leaf(page, "gen.1.6", "gen1-cosmology-firmament")
        cosmogram = page.evaluate(
            """(()=>{
              const svg = document.querySelector('.cc-diagram-svg');
              if (!svg) return { svgFound: false };
              const names = Array.from(svg.querySelectorAll('.cc-d-name'))
                .map(n => n.textContent.trim());
              const glosses = Array.from(svg.querySelectorAll('.cc-d-gloss'))
                .map(g => g.textContent.trim());
              const viewBox = svg.getAttribute('viewBox');
              const wrap = document.querySelector('.cc-diagram');
              const wrapStyle = wrap ? getComputedStyle(wrap) : null;
              return {
                svgFound: true,
                viewBox,
                strataNames: names,
                strataGlosses: glosses,
                hasMarkDots: svg.querySelectorAll('.cc-d-mark').length,
                hasDeepGlyph: svg.querySelectorAll('.cc-d-deep').length,
                hasAxisLine: svg.querySelectorAll('line[stroke-dasharray]').length > 0,
                hasWaterPattern: !!svg.querySelector('defs pattern#cc-water'),
                hasDeepPattern: !!svg.querySelector('defs pattern#cc-deep'),
                wrapBackground: wrapStyle?.background || null,
                wrapBorder: wrapStyle?.border || null,
              };
            })()"""
        )
        print(f"  svg viewBox:        {cosmogram['viewBox']}")
        print(f"  strata names:       {cosmogram['strataNames']}")
        print(f"  strata glosses:     {cosmogram['strataGlosses']}")
        print(f"  inter-stratum dots: {cosmogram['hasMarkDots']}")
        print(f"  deep glyph:         {cosmogram['hasDeepGlyph']}")
        print(f"  axis line:          {cosmogram['hasAxisLine']}")
        print(f"  water pattern:      {cosmogram['hasWaterPattern']}")
        print(f"  deep pattern:       {cosmogram['hasDeepPattern']}")
        assert cosmogram["svgFound"]
        # Vertical aspect ratio — viewBox should be tall
        assert cosmogram["viewBox"] == "0 0 480 880"
        # Five strata (cosmographic descent)
        assert cosmogram["strataNames"] == [
            "MAYIM MĒʿAL LĀ-RĀQÎAʿ",
            "RĀQÎAʿ",
            "ʾEREṢ",
            "MAYIM MITTAḤAT LĀ-RĀQÎAʿ",
            "SHEOL",
        ]
        assert cosmogram["strataGlosses"] == [
            "the upper cosmic waters",
            "the firmament — sky-vault hammered out",
            "the earth — a disc resting on pillars",
            "the lower waters — tehôm, the deep",
            "the depths — the shadow-land",
        ]
        # 4 inter-stratum dots (between 5 strata)
        assert cosmogram["hasMarkDots"] == 4
        # 1 deep-glyph (the threefold dot closing the descent)
        assert cosmogram["hasDeepGlyph"] == 1
        # Cosmic axis dashed line present
        assert cosmogram["hasAxisLine"]
        # Both water patterns defined
        assert cosmogram["hasWaterPattern"]
        assert cosmogram["hasDeepPattern"]
        print("  OK — 5-stratum vertical cosmogram with Hebrew names, "
              "English glosses, inter-stratum dots, axis line, "
              "and water patterns.\n")
        page.screenshot(path="reports/v84_cosmogram_final.png")

        # ── Cosmology chamber still functional ─────────────────────
        print("=== Cosmology chamber structure preserved ===")
        chamber = page.evaluate(
            """(()=>{
              const leaf = document.querySelector('.folio-leaf');
              return {
                hasCosmologyChamber: leaf?.classList.contains('cosmology-chamber'),
                hasCCLede: !!document.querySelector('.cc-lede'),
                hasCCTerms: !!document.querySelector('.cc-terms'),
                hasCCDiagram: !!document.querySelector('.cc-diagram'),
                sectionHeadings: document.querySelectorAll('.cc-section-heading').length,
              };
            })()"""
        )
        print(f"  {chamber}")
        assert chamber["hasCosmologyChamber"]
        assert chamber["hasCCLede"]
        assert chamber["hasCCTerms"]
        assert chamber["hasCCDiagram"]
        assert chamber["sectionHeadings"] >= 3  # Diagram, Terminology, Comparative
        print("  OK — cosmology chamber structure intact; cosmogram "
              "now the centerpiece artifact.\n")

        # ── All other AO chambers untouched ────────────────────────
        print("=== Other AO chambers preserved ===")
        chambers = [
            ("exo.40.34", "exo40-sanctuary-glory",  "sanctuary-chamber"),
            ("psa.13.1",  "psa13-lament-cry",       "lament-chamber"),
            ("gen.5.1",   "gen5-antediluvian-line", "lineage-chamber"),
        ]
        for pid, rec_id, expected_cls in chambers:
            open_leaf(page, pid, rec_id)
            has = page.evaluate(
                f"(()=>document.querySelector('.folio-leaf')?.classList.contains('{expected_cls}'))()"
            )
            print(f"  {expected_cls:<20} {pid}: {has}")
            assert has, (expected_cls, pid)
        print("  OK — sanctuary, lament, lineage chambers preserved.\n")

        # ── Family preservation ────────────────────────────────────
        print("=== Families preserved ===")
        for label, pid, rec_id, exp_max in [
            ("commentary",   "gen.1.1",  "gen1-commentary-augustine", "640px"),
            ("linguistic",   "gen.1.2",  "gen1-linguistic-tohu",     "560px"),
            ("architecture", "gen.22.2", "gen22-mount-moriah",       "480px"),
            ("manuscript",   "gen.1.1",  "gen1-manuscript-opening",  "500px"),
        ]:
            open_leaf(page, pid, rec_id)
            bm = page.evaluate(
                "(()=>{const b=document.querySelector('.folio-body-vertical');return b?getComputedStyle(b).maxWidth:null;})()"
            )
            assert bm == exp_max, (label, bm, exp_max)
            print(f"  {label:<14} {bm}")

        # ── Doré preserved ─────────────────────────────────────────
        open_leaf(page, "gen.1.3", "dore-creation-of-light")
        dore = page.evaluate(
            """(()=>({
              bg: getComputedStyle(document.querySelector('.folio-leaf')).backgroundColor,
              hasWrap: !!document.querySelector('.folio-plate-wrap'),
              hasPlaque: !!document.querySelector('.folio-plate-plaque'),
            }))()"""
        )
        print(f"  Doré: {dore}")
        assert dore["bg"] in ("rgba(0, 0, 0, 0)", "transparent")
        assert dore["hasWrap"] and dore["hasPlaque"]

        # AO count
        ao_count = page.evaluate(
            """(()=>{
              const ids = new Set();
              const recs = (currentData && currentData.genealogy) || [];
              for (const r of recs) {
                if (r && r.atlas_object && r.atlas_object.id) ids.add(r.atlas_object.id);
              }
              return ids.size;
            })()"""
        )
        print(f"  AO count: {ao_count}")
        assert ao_count == 12
        print("  OK — all families + 12 Atlas Objects preserved.\n")

        # ── Prior pillars preserved ────────────────────────────────
        print("=== Prior pillars preserved ===")
        # Stratum + density + transmission rubric all still operate
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.22.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(600)
        density = page.evaluate("(()=>document.querySelector('.chapter-room-heading')?.dataset.density)()")
        stratum = page.evaluate("(()=>document.querySelector('.ch-stratum')?.textContent)()")
        print(f"  gen.22.1 density: {density!r}, stratum: {stratum!r}")
        assert density == "center"
        assert stratum == "Torah · Patriarchal History"
        print("  OK — v79 + v82 still operational.\n")

        b.close()
    print("\nALL CHECKS PASSED — The Cosmogram masterpiece prototype "
          "operational.")


if __name__ == "__main__":
    main()
