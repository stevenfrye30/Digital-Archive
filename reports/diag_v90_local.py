"""v90 — Atlas Object Architecture (local verification).

Verifies the Gen 1:1 cosmology object:
  - Static, non-scrolling chamber (no overflow at chamber or
    panel level; no scrollbar)
  - Vertical left tab rail with five tabs (Cosmogram / Witness /
    Terminology / Comparative / Commentary)
  - One tab layer only; no nested tabs
  - Cosmogram tab: SVG fills the artifact panel and dominates
  - Each other tab fits the static panel without overflow
  - Object visually independent (object-specific vellum,
    inner frame, no footer/colophon)
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


def open_object(page, pid, rec_id):
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
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── Build marker ──────────────────────────────────────────
        page.goto("http://localhost:8765/index.html",
                  wait_until="networkidle")
        marker = page.evaluate(
            "document.querySelector('meta[name=atlas-build]').content")
        print(f"build marker: {marker}")
        assert marker == "v90-static-object-architecture"

        # ── Open Gen 1:1 cosmology object ─────────────────────────
        open_object(page, "gen.1.1", "gen1-cosmology-ane")

        # ── Architecture present? ─────────────────────────────────
        arch = page.evaluate(
            """(()=>{
              const leaf = document.querySelector('.folio-leaf.cosmology-chamber');
              if (!leaf) return null;
              const header = leaf.querySelector('.cc-object-header');
              const frame = leaf.querySelector('.cc-object-frame');
              const rail = leaf.querySelector('.cc-tab-rail');
              const stage = leaf.querySelector('.cc-tab-stage');
              const items = rail ? rail.querySelectorAll('.cc-tab-rail-item') : [];
              return {
                hasHeader: !!header,
                hasFrame: !!frame,
                hasRail: !!rail,
                hasStage: !!stage,
                tabCount: items.length,
                tabLabels: Array.from(items).map(i => i.textContent),
                hasOldNav: !!leaf.querySelector('.cc-chamber-nav'),
                hasFooter: !!leaf.querySelector('.folio-leaf-colophon') &&
                  getComputedStyle(leaf.querySelector('.folio-leaf-colophon')).display !== 'none',
              };
            })()""")
        print(f"architecture: {arch}")
        assert arch is not None
        assert arch["hasHeader"], "Missing cc-object-header"
        assert arch["hasFrame"], "Missing cc-object-frame"
        assert arch["hasRail"], "Missing cc-tab-rail"
        assert arch["hasStage"], "Missing cc-tab-stage"
        assert arch["tabCount"] == 5, f"Expected 5 tabs, got {arch['tabCount']}"
        assert arch["tabLabels"] == [
            "Cosmogram", "Witness", "Terminology", "Comparative", "Commentary"
        ]
        assert not arch["hasOldNav"], "Old v89 horizontal nav still present"
        assert not arch["hasFooter"], "Footer should be hidden in this object"
        print("  OK — five-tab static frame; no v89 nav; no footer.\n")

        # ── No scroll anywhere ────────────────────────────────────
        # Test every tab.
        tabs = ["Cosmogram", "Witness", "Terminology",
                "Comparative", "Commentary"]
        for tab in tabs:
            page.evaluate(f"""(() => {{
              const btns = document.querySelectorAll('.cc-tab-rail-item');
              for (const b of btns) {{ if (b.textContent === '{tab}') b.click(); }}
            }})()""")
            page.wait_for_timeout(450)
            m = page.evaluate("""(()=>{
              const leaf = document.querySelector('.folio-leaf.cosmology-chamber');
              const rail = leaf.querySelector('.cc-tab-rail');
              const stage = leaf.querySelector('.cc-tab-stage');
              const activePanel = stage.querySelector('.cc-panel--active');
              const activeTab = rail.querySelector('.cc-tab-rail-item--active');
              const leafCS = getComputedStyle(leaf);
              const stageCS = getComputedStyle(stage);
              const panelCS = activePanel ? getComputedStyle(activePanel) : null;
              const leafRect = leaf.getBoundingClientRect();
              const stageRect = stage.getBoundingClientRect();
              const panelRect = activePanel ? activePanel.getBoundingClientRect() : null;
              return {
                activePanel: activePanel?.dataset.panel,
                activeTab: activeTab?.textContent,
                leafOverflow: leafCS.overflow,
                leafScroll: leaf.scrollHeight > leaf.clientHeight + 1,
                stageOverflow: stageCS.overflow,
                stageScroll: stage.scrollHeight > stage.clientHeight + 1,
                panelScroll: activePanel ?
                  (activePanel.scrollHeight > activePanel.clientHeight + 1) : false,
                leafW: Math.round(leafRect.width),
                leafH: Math.round(leafRect.height),
                stageW: Math.round(stageRect.width),
                stageH: Math.round(stageRect.height),
                panelW: panelRect ? Math.round(panelRect.width) : null,
                panelH: panelRect ? Math.round(panelRect.height) : null,
                panelScrollH: activePanel?.scrollHeight,
                panelClientH: activePanel?.clientHeight,
              };
            })()""")
            print(f"[{tab}]: active panel={m['activePanel']!r}, "
                  f"active tab={m['activeTab']!r}")
            print(f"  leaf {m['leafW']}×{m['leafH']} overflow={m['leafOverflow']} "
                  f"scroll={m['leafScroll']}")
            print(f"  stage {m['stageW']}×{m['stageH']} overflow={m['stageOverflow']} "
                  f"scroll={m['stageScroll']}")
            print(f"  panel {m['panelW']}×{m['panelH']} "
                  f"scrollH={m['panelScrollH']} clientH={m['panelClientH']} "
                  f"scroll={m['panelScroll']}")
            assert m["activePanel"] == tab.lower(), (tab, m["activePanel"])
            assert m["activeTab"] == tab
            assert m["leafScroll"] is False, f"Leaf scrolls in {tab} tab"
            assert m["stageScroll"] is False, f"Stage scrolls in {tab} tab"
            assert m["panelScroll"] is False, f"Panel scrolls in {tab} tab"
            page.screenshot(path=f"reports/v90_LOCAL_tab_{tab.lower()}.png")
            print()

        # ── Cosmogram tab: SVG dominates ──────────────────────────
        page.evaluate("""(() => {
          const btns = document.querySelectorAll('.cc-tab-rail-item');
          for (const b of btns) { if (b.textContent === 'Cosmogram') b.click(); }
        })()""")
        page.wait_for_timeout(500)
        svg = page.evaluate("""(()=>{
          const s = document.querySelector('.cc-diagram-svg');
          if (!s) return null;
          const r = s.getBoundingClientRect();
          const stage = document.querySelector('.cc-tab-stage');
          const sr = stage.getBoundingClientRect();
          return {
            svgW: Math.round(r.width),
            svgH: Math.round(r.height),
            stageW: Math.round(sr.width),
            stageH: Math.round(sr.height),
            fillH: (r.height / sr.height),
            aspect: r.width / r.height,
          };
        })()""")
        print(f"cosmogram SVG: {svg}")
        assert svg["svgH"] > 600, f"Cosmogram too short: {svg['svgH']}"
        assert svg["fillH"] > 0.85, (
            f"Cosmogram not dominant — only fills {svg['fillH']:.2f} of stage height")
        assert 0.50 < svg["aspect"] < 0.60, (
            f"Cosmogram aspect ratio distorted: {svg['aspect']}")
        print("  OK — cosmogram is large and dominant.\n")

        # ── No nested tabs ────────────────────────────────────────
        nested = page.evaluate("""(()=>{
          const stage = document.querySelector('.cc-tab-stage');
          if (!stage) return null;
          // Check the cosmology chamber's active stage for any
          // child tab/tablist (only the rail above stage should
          // carry role=tablist).
          const nestedTablist = stage.querySelector('[role=tablist]');
          const nestedAccordion = stage.querySelector('details, .accordion');
          const nestedExpand = stage.querySelector('.read-more, .more-toggle');
          return {
            nestedTablist: !!nestedTablist,
            nestedAccordion: !!nestedAccordion,
            nestedExpand: !!nestedExpand,
          };
        })()""")
        print(f"nested-tab audit: {nested}")
        assert not nested["nestedTablist"]
        assert not nested["nestedAccordion"]
        assert not nested["nestedExpand"]
        print("  OK — one tab layer only, no nested rabbit holes.\n")

        # ── Object visually independent from reading room ────────
        # The cosmology chamber's background is different from the
        # default folio-leaf reader-bg.
        indep = page.evaluate("""(()=>{
          const leaf = document.querySelector('.folio-leaf.cosmology-chamber');
          const cs = getComputedStyle(leaf);
          return {
            background: cs.background,
            boxShadow: cs.boxShadow,
            maxWidth: cs.maxWidth,
            padding: cs.padding,
            display: cs.display,
            flexDirection: cs.flexDirection,
          };
        })()""")
        print(f"object frame: maxWidth={indep['maxWidth']} "
              f"padding={indep['padding']} display={indep['display']} "
              f"flexDirection={indep['flexDirection']}")
        print(f"  background snippet: {indep['background'][:200]}")
        print(f"  boxShadow snippet:  {indep['boxShadow'][:200]}")
        assert indep["display"] == "flex"
        assert indep["flexDirection"] == "column"
        # Distinct background (not the default #e6dac0 reader-bg)
        assert "e3d6b9" in indep["background"].lower() or \
               "227, 214, 185" in indep["background"], (
                 f"Object vellum should differ from reading-room parchment, "
                 f"got: {indep['background']}")
        # Inner frame box-shadow present
        assert "inset" in indep["boxShadow"], (
            f"Expected inset box-shadow for plate-edge frame, got: "
            f"{indep['boxShadow']}")
        print("  OK — object frame is visually independent.\n")

        # ── Short text-witness still opens normally ──────────────
        print("=== Short text witness (Augustine) unaffected ===")
        open_object(page, "gen.1.1", "gen1-commentary-augustine")
        ctrl = page.evaluate("""(()=>{
          const leaf = document.querySelector('.folio-leaf');
          if (!leaf) return null;
          const cs = getComputedStyle(leaf);
          const r = leaf.getBoundingClientRect();
          return {
            classes: leaf.className,
            display: cs.display,
            overflowY: cs.overflowY,
            width: Math.round(r.width),
            height: Math.round(r.height),
          };
        })()""")
        print(f"  {ctrl}")
        assert "cosmology-chamber" not in ctrl["classes"]
        # Augustine should not adopt the object frame layout.
        assert ctrl["display"] != "flex" or "cosmology" not in ctrl["classes"]
        page.screenshot(path="reports/v90_LOCAL_short_witness.png")
        print("  OK — short witness opens with its own layout.\n")

        b.close()
    print("ALL CHECKS PASSED — v90 Atlas Object Architecture operational.")


if __name__ == "__main__":
    main()
