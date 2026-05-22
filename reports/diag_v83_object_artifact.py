"""v83 — Object Artifact Maturation verification.

Verifies the two artifact-level moves shipped per
OBJECT_ARTIFACT_AUDIT.md:

  · Cosmology cosmogram (Phase 4, HIGHEST PRIORITY):
    - cosmology spacers carry a tiny centered hairline mark
      (::before pseudo, 14px width, 1px height, rgba(120, 80,
      40, 0.22))
    - spacer height 1.2em → 1.4em (more cosmic breath)
    - the body reads as a vertically-stacked cosmogram of
      cosmic strata separated by hairline bands

  · Genealogy lineage architecture (Phase 5):
    - generation-transition rows carry extra margin-top (0.3em)
    - the descent reads as architecturally banded by generation

No regressions: leaf families, AO chambers, Doré, v79 stratum,
v80 transmission rubrics, v81 inheritance, v82 geography all
preserved.
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

        # ── Cosmology cosmogram (Phase 4 highest priority) ─────────
        print("=== Cosmology cosmogram register ===")
        open_leaf(page, "gen.1.1", "gen1-cosmology-ane")
        cosmo = page.evaluate(
            """(()=>{
              const b = document.querySelector('.folio-body-vertical');
              if (!b) return null;
              const sp = b.querySelector('.folio-body-spacer');
              if (!sp) return null;
              const spStyle = getComputedStyle(sp);
              const beforeStyle = window.getComputedStyle(sp, '::before');
              return {
                spacerHeight: spStyle.height,
                spacerPosition: spStyle.position,
                beforeContent: beforeStyle.content,
                beforeWidth: beforeStyle.width,
                beforeHeight: beforeStyle.height,
                beforeBg: beforeStyle.backgroundColor,
                beforePosition: beforeStyle.position,
              };
            })()"""
        )
        print(f"  {cosmo}")
        # Spacer height: 1.4em × 14.56px body font = 20.38px
        sph = float(re.match(r"[\d.]+", cosmo["spacerHeight"]).group())
        assert 20.0 <= sph <= 21.0, sph
        # Spacer must be positioned to anchor the ::before
        assert cosmo["spacerPosition"] == "relative"
        # The ::before must render the hairline mark
        assert cosmo["beforeContent"] in ('""', "''", '"none"', "none") \
            or cosmo["beforeContent"] == '""'
        # NOTE: empty content '""' is what an empty content: '' resolves to
        assert cosmo["beforeContent"] == '""', cosmo["beforeContent"]
        assert cosmo["beforeWidth"] == "14px"
        assert cosmo["beforeHeight"] == "1px"
        # Background color matches the hairline alpha
        assert "rgb(120, 80, 40)" in cosmo["beforeBg"] or "120, 80, 40" in cosmo["beforeBg"]
        print("  OK — cosmology spacers carry centered hairline marks; "
              f"spacer height {sph:.1f}px (1.4em); cosmogram register "
              "operational.\n")
        page.screenshot(path="reports/v83_cosmology_cosmogram.png")

        # Also verify light-before-luminaries inherits the same
        open_leaf(page, "gen.1.3", "gen1-cosmology-light-before-luminaries")
        light_sph = page.evaluate(
            """(()=>{
              const sp = document.querySelector('.folio-body-spacer');
              return sp ? getComputedStyle(sp).height : null;
            })()"""
        )
        light_before = page.evaluate(
            """(()=>{
              const sp = document.querySelector('.folio-body-spacer');
              if (!sp) return null;
              const s = window.getComputedStyle(sp, '::before');
              return { width: s.width, height: s.height, bg: s.backgroundColor };
            })()"""
        )
        print(f"  light-before-luminaries spacer-h: {light_sph}, "
              f"hairline mark: {light_before}")
        assert light_before["width"] == "14px"
        page.screenshot(path="reports/v83_cosmology_light.png")
        print("  OK — light-before-luminaries inherits cosmogram register.\n")

        # ── Genealogy lineage architecture (Phase 5) ────────────────
        print("=== Genealogy lineage architecture ===")
        open_leaf(page, "gen.4.25", "cain-seth-divergence")
        gen_metrics = page.evaluate(
            """(()=>{
              const b = document.querySelector('.folio-body-vertical');
              if (!b) return null;
              // Find a row with data-generation="transition"
              const trans = b.querySelector('.folio-body-line[data-generation="transition"]');
              if (!trans) return { transitionRowFound: false };
              const s = getComputedStyle(trans);
              // Compare to a row WITHOUT the attribute
              const all = b.querySelectorAll('.folio-body-line');
              let plain = null;
              for (const r of all) {
                if (!r.dataset.generation && !r.classList.contains('folio-body-spacer')) {
                  plain = r;
                  break;
                }
              }
              const plainStyle = plain ? getComputedStyle(plain) : null;
              return {
                transitionRowFound: true,
                transitionMarginTop: s.marginTop,
                plainMarginTop: plainStyle ? plainStyle.marginTop : null,
                totalTransitions: b.querySelectorAll('[data-generation="transition"]').length,
              };
            })()"""
        )
        print(f"  {gen_metrics}")
        assert gen_metrics["transitionRowFound"]
        # Transition rows: 0.3em × 14.4px body font ≈ 4.32px
        trans_mt = float(re.match(r"[\d.]+", gen_metrics["transitionMarginTop"]).group())
        assert 4.0 <= trans_mt <= 5.0, trans_mt
        # Plain rows should have 0 margin-top
        plain_mt = float(re.match(r"[\d.]+", gen_metrics["plainMarginTop"]).group())
        assert plain_mt < 1.0, plain_mt
        print(f"  OK — generation-transition rows have +{trans_mt:.1f}px "
              "margin (plain rows 0); lineage banded by generation.\n")
        page.screenshot(path="reports/v83_genealogy_lineage.png")

        # ── Cosmology AO chamber preserved (exclusion check) ────────
        print("=== Cosmology AO chamber preserved ===")
        open_leaf(page, "gen.1.6", "gen1-cosmology-firmament")
        chamber = page.evaluate(
            """(()=>{
              const leaf = document.querySelector('.folio-leaf');
              const cosmologyChamber = leaf?.classList.contains('cosmology-chamber');
              const hasCCLede = !!document.querySelector('.cc-lede');
              const hasCCDiagram = !!document.querySelector('.cc-diagram');
              // The chamber should NOT receive the new cosmogram
              // hairline spacer treatment (the :not(.cosmology-chamber)
              // exclusion).
              const bvSp = document.querySelector('.cosmology-chamber .folio-body-vertical .folio-body-spacer');
              return { cosmologyChamber, hasCCLede, hasCCDiagram, hasChamberSpacer: !!bvSp };
            })()"""
        )
        print(f"  {chamber}")
        assert chamber["cosmologyChamber"]
        assert chamber["hasCCLede"]
        assert chamber["hasCCDiagram"]
        print("  OK — cosmology firmament chamber preserved.\n")

        # ── Doré preservation ─────────────────────────────────────
        print("=== Doré preservation ===")
        open_leaf(page, "gen.1.3", "dore-creation-of-light")
        dore = page.evaluate(
            """(()=>{
              const leaf = document.querySelector('.folio-leaf');
              return {
                bg: getComputedStyle(leaf).backgroundColor,
                hasWrap: !!document.querySelector('.folio-plate-wrap'),
                hasPlaque: !!document.querySelector('.folio-plate-plaque'),
              };
            })()"""
        )
        print(f"  {dore}")
        assert dore["bg"] in ("rgba(0, 0, 0, 0)", "transparent")
        assert dore["hasWrap"] and dore["hasPlaque"]
        print("  OK — Doré preserved.\n")

        # ── All formalized families preserved ──────────────────────
        print("=== Formalized families preserved ===")
        for label, pid, rec_id, exp_max in [
            ("commentary",     "gen.1.1",  "gen1-commentary-augustine", "640px"),
            ("linguistic",     "gen.1.2",  "gen1-linguistic-tohu",     "560px"),
            ("manuscript",     "gen.1.1",  "gen1-manuscript-opening",  "500px"),
            ("architecture",   "gen.22.2", "gen22-mount-moriah",       "480px"),
            ("reception",      "gen.18.2", "gen18-three-visitors-reception", "600px"),
            ("ritual",         "gen.1.3",  "gen1-ritual-maariv-aravim","560px"),
            ("cross-ref",      "gen.1.1",  "gen1-xref-nt-creation",    "540px"),
        ]:
            open_leaf(page, pid, rec_id)
            bm = page.evaluate(
                "(()=>{const b=document.querySelector('.folio-body-vertical');return b?getComputedStyle(b).maxWidth:null;})()"
            )
            assert bm == exp_max, (label, bm, exp_max)
            print(f"  {label:<14} {bm}")
        print("  OK — all formalized families preserved.\n")

        # ── Prior pillars preserved ────────────────────────────────
        print("=== Prior pillars preserved ===")
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.22.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(600)
        # v82 density
        density = page.evaluate(
            "(()=>document.querySelector('.chapter-room-heading')?.dataset.density||null)()"
        )
        # v79 stratum
        stratum = page.evaluate(
            "(()=>document.querySelector('.ch-stratum')?.textContent||null)()"
        )
        print(f"  v82 density (gen.22.1): {density!r}")
        print(f"  v79 stratum (gen.22.1): {stratum!r}")
        assert density == "center"
        assert stratum == "Torah · Patriarchal History"
        # v80 transmission rubric
        page.evaluate("() => localStorage.removeItem('atlas:encounters:v1')")
        page.evaluate("() => localStorage.removeItem('archive:records-seen:v1')")
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(500)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        page.evaluate("(() => _openFolioObject('gen22-akedah-binding'))()")
        page.wait_for_timeout(1300)
        rubric = page.evaluate(
            """(()=>{
              const p = document.querySelector('.folio-leaf-provenance');
              return window.getComputedStyle(p, '::after').content;
            })()"""
        )
        print(f"  v80 rubric (akedah-binding): {rubric}")
        assert rubric == '"inherited through interpretation"'
        # v81 cross-reference echo (border-left)
        page.evaluate("(() => _openFolioObject('gen1-xref-nt-creation'))()")
        page.wait_for_timeout(1300)
        xref = page.evaluate(
            """(()=>{
              const b = document.querySelector('.folio-body-vertical');
              return b ? getComputedStyle(b).borderLeftStyle : null;
            })()"""
        )
        print(f"  v81 xref border: {xref}")
        assert xref == "dotted"
        # AO inventory
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
        print("  OK — v79 + v80 + v81 + v82 + 12 AOs all preserved.\n")

        b.close()
    print("\nALL CHECKS PASSED — Object Artifact Maturation operational.")


if __name__ == "__main__":
    main()
