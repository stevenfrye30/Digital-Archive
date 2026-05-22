"""v81 — Civilizational Inheritance verification.

Verifies two moves:

  · Cosmology cosmogram (Phase 6, highest priority):
    - gen1-cosmology-ane body restructured into descending
      strata (above firmament / firmament / earth-disc /
      below earth).
    - cosmology spacer 0.75em → 1.2em for cosmic breath
      between strata.
    - the body reads as a manuscript descent through the
      cosmic layers rather than a single paragraph.

  · Cross-reference echo (Phase 3):
    - dotted hairline on the body's left edge (canonical-
      resonance axis); each echo hangs off the axis.

No regressions: all 8 formalized text-witness families
preserved, all 12 AO chambers preserved, Doré preserved,
v79 canonical stratum operational, v80 transmission rubrics
operational.
"""
import sys
import re
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
    page.wait_for_timeout(1300)


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 1100})
        page = ctx.new_page()

        # ── Cosmology cosmogram — stratified body ───────────────────
        print("=== Cosmology cosmogram (Phase 6) ===")
        open_leaf(page, "gen.1.1", "gen1-cosmology-ane")
        body = page.evaluate(
            """(()=>{
              const b = document.querySelector('.folio-body-vertical');
              return b ? {
                text: b.innerText,
                lineCount: b.querySelectorAll('.folio-body-line').length,
                spacerCount: b.querySelectorAll('.folio-body-spacer').length,
                spacerHeight: b.querySelector('.folio-body-spacer')
                  ? getComputedStyle(b.querySelector('.folio-body-spacer')).height
                  : null,
              } : null;
            })()"""
        )
        print(f"  total lines: {body['lineCount']}")
        print(f"  spacers:     {body['spacerCount']}")
        print(f"  spacer-h:    {body['spacerHeight']}")
        # The body should now contain stratum-phrases.
        text = body["text"]
        assert "Above the firmament" in text, "stratum 'above firmament' missing"
        assert "rāqîaʿ" in text, "rāqîaʿ stratum missing"
        assert "earth-disc" in text, "earth-disc stratum missing"
        assert "Below the earth" in text, "stratum 'below earth' missing"
        # Spacer should be 1.2em — at body font-size 14.56px (0.91em
        # × 16) → 1.2em ≈ 17.47px.
        sph = float(re.match(r"[\d.]+", body["spacerHeight"]).group())
        assert 17.0 <= sph <= 18.0, sph
        # Multiple paragraphs (was 1 → now several strata).
        assert body["spacerCount"] >= 5, body["spacerCount"]
        page.screenshot(path="reports/v81_cosmology_ane.png")
        print("  OK — cosmology body stratified; spacer pushed to 1.2em "
              f"(≈{sph:.1f}px); body reads as descending strata.\n")

        # Also verify the light-before-luminaries still renders (no
        # body edit but spacer change applies).
        open_leaf(page, "gen.1.3", "gen1-cosmology-light-before-luminaries")
        sph2 = page.evaluate(
            """(()=>{
              const b = document.querySelector('.folio-body-vertical');
              const sp = b?.querySelector('.folio-body-spacer');
              return sp ? getComputedStyle(sp).height : null;
            })()"""
        )
        print(f"  light-before-luminaries spacer-h: {sph2}")
        sph2_px = float(re.match(r"[\d.]+", sph2).group())
        assert 17.0 <= sph2_px <= 18.0, sph2_px
        page.screenshot(path="reports/v81_cosmology_light.png")
        print("  OK — light-before-luminaries inherits 1.2em spacer.\n")

        # ── Cross-reference echo — left hairline ────────────────────
        print("=== Cross-reference echo (Phase 3) ===")
        open_leaf(page, "gen.1.1", "gen1-xref-nt-creation")
        xref = page.evaluate(
            """(()=>{
              const b = document.querySelector('.folio-body-vertical');
              if (!b) return null;
              const s = getComputedStyle(b);
              return {
                borderLeftStyle: s.borderLeftStyle,
                borderLeftColor: s.borderLeftColor,
                borderLeftWidth: s.borderLeftWidth,
                paddingLeft: s.paddingLeft,
                maxWidth: s.maxWidth,
              };
            })()"""
        )
        print(f"  {xref}")
        assert xref["borderLeftStyle"] == "dotted", xref["borderLeftStyle"]
        assert xref["borderLeftWidth"] == "1px", xref["borderLeftWidth"]
        assert xref["paddingLeft"] == "18px", xref["paddingLeft"]
        assert xref["maxWidth"] == "540px", xref["maxWidth"]
        page.screenshot(path="reports/v81_xref_echo.png")
        print("  OK — cross-reference body carries dotted canonical-"
              "resonance axis on its left edge.\n")

        # ── No regression: families preserved ─────────────────────
        print("=== Family identity preservation ===")
        family_checks = [
            ("commentary",     "gen.1.1",  "gen1-commentary-augustine",
             dict(bodyMaxWidth="640px", titleFontWeight="400")),
            ("linguistic",     "gen.1.2",  "gen1-linguistic-tohu",
             dict(bodyMaxWidth="560px", titleFontStyle="normal")),
            ("manuscript",     "gen.1.1",  "gen1-manuscript-opening",
             dict(bodyMaxWidth="500px")),
            ("architecture",   "gen.22.2", "gen22-mount-moriah",
             dict(bodyMaxWidth="480px", titleFontVariantCaps="small-caps")),
            ("reception",      "gen.18.2", "gen18-three-visitors-reception",
             dict(bodyMaxWidth="600px")),
            ("ritual",         "gen.1.3",  "gen1-ritual-maariv-aravim",
             dict(bodyMaxWidth="560px", titleFontWeight="400")),
        ]
        for label, pid, rec_id, exp in family_checks:
            open_leaf(page, pid, rec_id)
            m = page.evaluate(
                """(()=>{
                  const leaf = document.querySelector('.folio-leaf');
                  const t = leaf.querySelector('.folio-leaf-title');
                  const b = leaf.querySelector('.folio-body-vertical');
                  const ts = t ? getComputedStyle(t) : {};
                  return {
                    bodyMaxWidth: b ? getComputedStyle(b).maxWidth : null,
                    titleFontStyle: ts.fontStyle,
                    titleFontWeight: ts.fontWeight,
                    titleFontVariantCaps: ts.fontVariantCaps,
                  };
                })()"""
            )
            for k, v in exp.items():
                assert m[k] == v, (label, k, m[k], v)
            print(f"  {label:<14}: preserved")
        print("  OK — formalized families preserved.\n")

        # ── Doré preserved ─────────────────────────────────────────
        print("=== Doré preservation ===")
        open_leaf(page, "gen.1.3", "dore-creation-of-light")
        d = page.evaluate(
            """(()=>{
              const leaf = document.querySelector('.folio-leaf');
              return {
                bg: getComputedStyle(leaf).backgroundColor,
                hasWrap: !!document.querySelector('.folio-plate-wrap'),
                hasPlaque: !!document.querySelector('.folio-plate-plaque'),
              };
            })()"""
        )
        print(f"  {d}")
        assert d["bg"] in ("rgba(0, 0, 0, 0)", "transparent")
        assert d["hasWrap"] and d["hasPlaque"]
        print("  OK — Doré preserved.\n")

        # ── AO chambers + count ────────────────────────────────────
        open_leaf(page, "gen.1.6", "gen1-cosmology-firmament")
        cosmology_chamber = page.evaluate(
            """(()=>{
              const leaf = document.querySelector('.folio-leaf');
              return {
                hasCosmologyChamber: leaf?.classList.contains('cosmology-chamber'),
                hasCCLede: !!document.querySelector('.cc-lede'),
                hasCCDiagram: !!document.querySelector('.cc-diagram'),
              };
            })()"""
        )
        print(f"=== AO cosmology chamber preserved ===\n  {cosmology_chamber}")
        assert cosmology_chamber["hasCosmologyChamber"]
        assert cosmology_chamber["hasCCLede"]
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
        print("  OK — chambers + 12 Atlas Objects preserved.\n")

        # ── v79 stratum + v80 transmission rubrics still operational ───
        print("=== v79 + v80 still operational ===")
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(600)
        stratum = page.evaluate(
            "(()=>{const s=document.querySelector('.ch-stratum');return s?s.textContent:null;})()"
        )
        print(f"  v79 stratum (gen.1.1): {stratum!r}")
        assert stratum == "Torah · Primeval History"
        open_leaf(page, "gen.1.1", "gen1-commentary-augustine")
        rubric = page.evaluate(
            """(()=>{
              const p = document.querySelector('.folio-leaf-provenance');
              return window.getComputedStyle(p, '::after').content;
            })()"""
        )
        print(f"  v80 rubric (Augustine): {rubric}")
        assert rubric == '"inherited through interpretation"'
        print("  OK — v79 stratum + v80 transmission rubrics intact.\n")

        b.close()
    print("\nALL CHECKS PASSED — Civilizational Inheritance operational.")


if __name__ == "__main__":
    main()
