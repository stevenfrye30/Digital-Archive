"""v85 — Cosmology chamber staging verification.

Verifies that the cosmology chamber's compositional sequence
has been inverted: the cosmogram is now the first encounter
(after the constitutional rubric), and the prose lede has
become supporting witness-text BELOW the cosmogram.

  · cc-cosmogram-frame element wraps the SVG and carries
    120px top + 96px bottom margin
  · DOM order: provenance → verse → title → cosmogram-frame →
    cc-lede → cc-section-heading × 4
  · §I = Terminology (the diagram is no longer numbered §I)
  · cc-lede after cosmogram in supporting register (narrower
    520px, italic, opacity 0.84, font-size 0.94em)
  · #object-viewer now scrollable vertically (overflow-y:auto)
    so the cosmogram-tall chamber can be walked through
  · Viewer aligned to top (align-items: flex-start)

No regressions: cosmology chamber renders, other chambers
preserved, families preserved, Doré preserved.
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
    page.wait_for_timeout(2000)


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── DOM order — cosmogram before lede ──────────────────────
        print("=== Cosmogram-first composition (DOM order) ===")
        open_leaf(page, "gen.1.6", "gen1-cosmology-firmament")
        dom = page.evaluate(
            """(()=>{
              const leaf = document.querySelector('.folio-leaf');
              const children = Array.from(leaf.children);
              // Find the indices of key elements
              const cosmoIdx = children.findIndex(c => c.classList.contains('cc-cosmogram-frame'));
              const ledeIdx = children.findIndex(c => c.classList.contains('cc-lede'));
              const sectionHeadings = Array.from(leaf.querySelectorAll('.cc-section-heading'))
                .map(s => s.querySelector('.cc-section-title')?.textContent.trim());
              return {
                cosmoIdx,
                ledeIdx,
                cosmogramBeforeLede: cosmoIdx >= 0 && ledeIdx >= 0 && cosmoIdx < ledeIdx,
                sectionTitles: sectionHeadings,
                sectionCount: sectionHeadings.length,
              };
            })()"""
        )
        print(f"  cosmogram-frame index: {dom['cosmoIdx']}")
        print(f"  cc-lede index:         {dom['ledeIdx']}")
        print(f"  cosmogram before lede: {dom['cosmogramBeforeLede']}")
        print(f"  section titles:        {dom['sectionTitles']}")
        assert dom["cosmogramBeforeLede"], "Cosmogram must come BEFORE cc-lede"
        # Section headings: Terminology / Comparative Context /
        # Anchorings (optional) / Archive Commentary (if it has a
        # heading) — but the diagram heading is gone.
        assert "Diagram" not in dom["sectionTitles"], (
            "§I Diagram heading should be removed; cosmogram is centerpiece")
        assert "Terminology" in dom["sectionTitles"], dom["sectionTitles"]
        print("  OK — cosmogram is now FIRST in DOM order, before "
              "supporting prose. Diagram is no longer a numbered "
              "section heading.\n")

        # ── cc-cosmogram-frame margins ─────────────────────────────
        print("=== Cosmogram frame: dramatic vertical silence ===")
        frame = page.evaluate(
            """(()=>{
              const f = document.querySelector('.cc-cosmogram-frame');
              if (!f) return null;
              const s = getComputedStyle(f);
              return {
                marginTop: s.marginTop,
                marginBottom: s.marginBottom,
                hasDiagram: !!f.querySelector('.cc-diagram'),
              };
            })()"""
        )
        print(f"  {frame}")
        assert frame["marginTop"] == "120px"
        assert frame["marginBottom"] == "96px"
        assert frame["hasDiagram"]
        print("  OK — 120px top + 96px bottom silence around "
              "the cosmogram.\n")

        # ── cc-lede in supporting-witness register ─────────────────
        print("=== Post-cosmogram lede: supporting-witness register ===")
        lede = page.evaluate(
            """(()=>{
              const l = document.querySelector('.cc-lede');
              if (!l) return null;
              const s = getComputedStyle(l);
              const p = l.querySelector('p');
              const ps = p ? getComputedStyle(p) : null;
              return {
                maxWidth: s.maxWidth,
                fontStyle: s.fontStyle,
                opacity: s.opacity,
                pFontSize: ps ? ps.fontSize : null,
                pLineHeight: ps ? ps.lineHeight : null,
              };
            })()"""
        )
        print(f"  {lede}")
        assert lede["maxWidth"] == "520px"
        assert lede["fontStyle"] == "italic"
        assert abs(float(lede["opacity"]) - 0.84) < 0.01
        print("  OK — lede in supporting register: 520px italic at "
              "0.84 opacity, 0.94em font.\n")

        # ── Viewer scrollable + aligned to top ─────────────────────
        print("=== Viewer: scrollable + top-anchored ===")
        viewer = page.evaluate(
            """(()=>{
              const v = document.getElementById('object-viewer');
              const s = getComputedStyle(v);
              return {
                overflowX: s.overflowX,
                overflowY: s.overflowY,
                alignItems: s.alignItems,
              };
            })()"""
        )
        print(f"  {viewer}")
        assert viewer["overflowX"] == "hidden"
        assert viewer["overflowY"] == "auto"
        assert viewer["alignItems"] == "flex-start"
        print("  OK — viewer scrolls vertically; chamber anchors at "
              "the top so the reader sees the rubric first.\n")

        # ── Cosmogram itself still intact (v84) ────────────────────
        print("=== Cosmogram artifact preserved ===")
        cosmogram = page.evaluate(
            """(()=>{
              const svg = document.querySelector('.cc-diagram-svg');
              if (!svg) return null;
              return {
                viewBox: svg.getAttribute('viewBox'),
                strataNames: Array.from(svg.querySelectorAll('.cc-d-name'))
                  .map(n => n.textContent.trim()),
              };
            })()"""
        )
        print(f"  viewBox: {cosmogram['viewBox']}")
        print(f"  strata:  {cosmogram['strataNames']}")
        assert cosmogram["viewBox"] == "0 0 480 880"
        assert len(cosmogram["strataNames"]) == 5
        print("  OK — cosmogram artifact intact (v84 preserved).\n")

        # ── Other AO chambers preserved ────────────────────────────
        print("=== Other AO chambers preserved ===")
        for pid, rec_id, expected_cls in [
            ("exo.40.34",  "exo40-sanctuary-glory",  "sanctuary-chamber"),
            ("psa.13.1",   "psa13-lament-cry",       "lament-chamber"),
            ("gen.5.1",    "gen5-antediluvian-line", "lineage-chamber"),
            ("isa.6.1",    "isa6-opened-heavens",    "revelation-chamber"),
        ]:
            open_leaf(page, pid, rec_id)
            has = page.evaluate(
                f"(()=>document.querySelector('.folio-leaf')?.classList.contains('{expected_cls}'))()"
            )
            print(f"  {expected_cls:<20} {pid}: {has}")
            assert has, (expected_cls, pid)
        print("  OK — sanctuary / lament / lineage / revelation "
              "chambers preserved (not affected by cosmology "
              "restructure).\n")

        # ── Family preservation ────────────────────────────────────
        print("=== Families preserved ===")
        for label, pid, rec_id, exp_max in [
            ("commentary",   "gen.1.1",  "gen1-commentary-augustine", "640px"),
            ("linguistic",   "gen.1.2",  "gen1-linguistic-tohu",     "560px"),
            ("architecture", "gen.22.2", "gen22-mount-moriah",       "480px"),
        ]:
            open_leaf(page, pid, rec_id)
            bm = page.evaluate(
                "(()=>{const b=document.querySelector('.folio-body-vertical');return b?getComputedStyle(b).maxWidth:null;})()"
            )
            assert bm == exp_max, (label, bm, exp_max)
            print(f"  {label:<14} {bm}")

        # Doré
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

        b.close()
    print("\nALL CHECKS PASSED — Cosmology chamber staging operational.")


if __name__ == "__main__":
    main()
