"""v82 — Civilizational Geography verification.

Verifies the density-aware chapter-heading register that
introduces geographic depth to the codex:

  · data-density="silent"   — wilderness; no records anchored;
                              wider breath + faded rule
  · data-density="center"   — canonical gravity; lengthened &
                              intensified rule
  · data-density="standard" — ordinary inhabited terrain

Centers (hardcoded canonical-gravity list):
  Torah:  gen.1, gen.22, exo.3, exo.19, exo.20, exo.40,
          lev.16, deu.6
  Hebrew Bible: psa.13, psa.22, psa.23, isa.6, isa.53
  NT:     mat.5, jhn.1, rev.4, rev.21, rev.22

No regressions: leaf families, AO chambers, Doré, v79 stratum,
v80 rubrics, v81 cosmogram + xref echo all preserved.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


SAMPLES = [
    # (pid, expected_density, label)
    # Genesis: dense capital, sparse, silent wilderness, sacred centre
    ("gen.1.1",   "center",   "gen1_creation_center"),
    ("gen.2.1",   "standard", "gen2_sabbath"),
    ("gen.5.1",   "standard", "gen5_lineage"),
    ("gen.8.1",   "silent",   "gen8_silent_wilderness"),
    ("gen.10.1",  "silent",   "gen10_silent"),
    ("gen.12.1",  "standard", "gen12_call"),
    ("gen.20.1",  "silent",   "gen20_silent"),
    ("gen.22.1",  "center",   "gen22_akedah_center"),
    ("gen.30.1",  "silent",   "gen30_silent"),
    ("gen.50.1",  "silent",   "gen50_silent_close"),
    # Torah centers beyond Genesis
    ("exo.3.1",   "center",   "exo3_burning_bush"),
    ("exo.19.1",  "center",   "exo19_sinai"),
    ("exo.20.1",  "center",   "exo20_decalogue"),
    ("exo.40.34", "center",   "exo40_glory"),
    ("lev.16.1",  "center",   "lev16_atonement"),
    ("deu.6.4",   "center",   "deu6_shema"),
    # Wisdom & Prophets centers
    ("psa.13.1",  "center",   "psa13_lament"),
    ("psa.22.1",  "center",   "psa22_forsaken"),
    ("psa.23.1",  "center",   "psa23_shepherd"),
    ("isa.6.1",   "center",   "isa6_throne"),
    ("isa.53.5",  "center",   "isa53_servant"),
    # NT centers
    ("mat.5.1",   "center",   "mat5_mount"),
    ("jhn.1.14",  "center",   "jhn1_word"),
    ("rev.4.1",   "center",   "rev4_throne"),
    ("rev.21.1",  "center",   "rev21_new"),
    ("rev.22.1",  "center",   "rev22_close"),
    # Inhabited but not centers
    ("psa.150.1", "silent",   "psa150_silent"),
    ("lev.1.1",   "silent",   "lev1_silent"),
    ("job.1.1",   "silent",   "job1_silent"),
]


def open_chapter(page, pid):
    page.goto(
        f"http://localhost:8765/index.html?text=bible_kjv.json&p={pid}",
        wait_until="networkidle",
    )
    page.wait_for_function(
        "typeof currentData === 'object' && currentData && currentData.passages",
        timeout=15000,
    )
    page.wait_for_timeout(600)


def density_attr(page):
    return page.evaluate(
        """(()=>{
          const h = document.querySelector('.chapter-room-heading');
          return h ? h.dataset.density || null : null;
        })()"""
    )


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── Density coverage ───────────────────────────────────────
        print("=== Density coverage across canon ===")
        sample_screenshots = {
            "gen1_creation_center",
            "gen8_silent_wilderness",
            "gen22_akedah_center",
            "gen50_silent_close",
            "isa53_servant",
            "psa23_shepherd",
            "rev22_close",
            "psa150_silent",
        }
        for pid, expected, label in SAMPLES:
            open_chapter(page, pid)
            actual = density_attr(page)
            ok = "OK" if actual == expected else "FAIL"
            print(f"  [{ok}] {pid:<10}  → {actual!r:<12}  ({label})")
            assert actual == expected, (pid, actual, expected)
            if label in sample_screenshots:
                page.screenshot(path=f"reports/v82_density_{label}.png")
        print(f"\n  OK — all {len(SAMPLES)} density attributions correct.\n")

        # ── Silent chapter register — wider breath ────────────────
        print("=== Silent chapter — wilderness register ===")
        open_chapter(page, "gen.8.1")
        silent = page.evaluate(
            """(()=>{
              const h = document.querySelector('.chapter-room-heading');
              const r = h?.querySelector('.ch-rule');
              return {
                paddingTop: getComputedStyle(h).paddingTop,
                paddingBottom: getComputedStyle(h).paddingBottom,
                ruleWidth: r ? getComputedStyle(r).width : null,
                ruleColor: r ? getComputedStyle(r).borderTopColor : null,
              };
            })()"""
        )
        print(f"  silent: {silent}")
        # Silent: padding 56/64 (was 36/44)
        assert silent["paddingTop"] == "56px"
        assert silent["paddingBottom"] == "64px"
        # Rule narrower (36px vs default 44px)
        assert silent["ruleWidth"] == "36px"
        # Rule color faded (alpha 0.28 vs 0.42)
        assert "0.28" in silent["ruleColor"], silent["ruleColor"]
        print("  OK — silent chapter carries wilderness register "
              "(wider breath, faded narrower rule).\n")

        # ── Center chapter register — lengthened rule ──────────────
        print("=== Center chapter — canonical-gravity register ===")
        open_chapter(page, "gen.22.1")
        center = page.evaluate(
            """(()=>{
              const h = document.querySelector('.chapter-room-heading');
              const r = h?.querySelector('.ch-rule');
              return {
                paddingTop: getComputedStyle(h).paddingTop,
                ruleWidth: r ? getComputedStyle(r).width : null,
                ruleColor: r ? getComputedStyle(r).borderTopColor : null,
              };
            })()"""
        )
        print(f"  center: {center}")
        # Center: rule width 64px (was 44), intensified (alpha 0.58)
        assert center["ruleWidth"] == "64px"
        assert "0.58" in center["ruleColor"], center["ruleColor"]
        print("  OK — center chapter carries lengthened intensified rule.\n")

        # ── Standard chapter — unchanged ───────────────────────────
        print("=== Standard chapter — unchanged default ===")
        open_chapter(page, "gen.12.1")
        standard = page.evaluate(
            """(()=>{
              const h = document.querySelector('.chapter-room-heading');
              const r = h?.querySelector('.ch-rule');
              return {
                paddingTop: getComputedStyle(h).paddingTop,
                ruleWidth: r ? getComputedStyle(r).width : null,
              };
            })()"""
        )
        print(f"  standard: {standard}")
        assert standard["paddingTop"] == "36px"
        assert standard["ruleWidth"] == "44px"
        print("  OK — standard chapters retain the default register.\n")

        # ── No regression: prior layers preserved ─────────────────
        print("=== Prior-layer preservation ===")
        # v79 stratum
        open_chapter(page, "gen.1.1")
        stratum = page.evaluate(
            "(()=>{const s=document.querySelector('.ch-stratum');return s?s.textContent:null;})()"
        )
        print(f"  v79 stratum (gen.1.1): {stratum!r}")
        assert stratum == "Torah · Primeval History"
        # v80 transmission rubric
        page.evaluate("() => localStorage.removeItem('atlas:encounters:v1')")
        page.evaluate("() => localStorage.removeItem('archive:records-seen:v1')")
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(500)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        page.evaluate("(() => _openFolioObject('gen1-commentary-augustine'))()")
        page.wait_for_timeout(1300)
        rubric = page.evaluate(
            """(()=>{
              const p = document.querySelector('.folio-leaf-provenance');
              return window.getComputedStyle(p, '::after').content;
            })()"""
        )
        print(f"  v80 rubric (Augustine): {rubric}")
        assert rubric == '"inherited through interpretation"'
        # v81 cosmology cosmogram + cross-reference echo
        page.evaluate("(() => _openFolioObject('gen1-cosmology-ane'))()")
        page.wait_for_timeout(1300)
        cosmology_body = page.evaluate(
            """(()=>document.querySelector('.folio-body-vertical')?.innerText||'')()"""
        )
        assert "Above the firmament" in cosmology_body
        assert "Below the earth" in cosmology_body
        page.evaluate("(() => _openFolioObject('gen1-xref-nt-creation'))()")
        page.wait_for_timeout(1300)
        xref_border = page.evaluate(
            """(()=>{
              const b = document.querySelector('.folio-body-vertical');
              return b ? getComputedStyle(b).borderLeftStyle : null;
            })()"""
        )
        print(f"  v81 cosmology stratified + xref hairline: "
              f"({'Above the firmament' in cosmology_body}, {xref_border})")
        assert xref_border == "dotted"
        print("  OK — v79 + v80 + v81 all intact.\n")

        # ── Family preservation + AO inventory ─────────────────────
        print("=== Family + AO preservation ===")
        page.evaluate("(() => _openFolioObject('gen1-commentary-augustine'))()")
        page.wait_for_timeout(1300)
        commentary = page.evaluate(
            """(()=>{
              const leaf = document.querySelector('.folio-leaf');
              return {
                bodyMax: getComputedStyle(leaf.querySelector('.folio-body-vertical')).maxWidth,
                titleWeight: getComputedStyle(leaf.querySelector('.folio-leaf-title')).fontWeight,
              };
            })()"""
        )
        print(f"  commentary: {commentary}")
        assert commentary["bodyMax"] == "640px"
        assert commentary["titleWeight"] == "400"
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
        print("  OK — families + 12 Atlas Objects preserved.\n")

        b.close()
    print("\nALL CHECKS PASSED — Civilizational Geography operational.")


if __name__ == "__main__":
    main()
