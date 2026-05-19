"""v27 — Genesis 1 calibration stress test."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.click("#companion-toggle")
        page.wait_for_timeout(800)

        # Top of chapter
        page.screenshot(path="reports/v27_gen1_top.png")

        # Inventory + per-cluster diagnostics
        info = page.evaluate(
            """
          () => {
            const clusters = Array.from(document.querySelectorAll('.cr-folio-cluster'));
            const markers = Array.from(document.querySelectorAll('.cr-folio-marker'));
            const spread = document.querySelector('#passages .chapter-spread');
            const passage = document.querySelector('.scripture-column .cr-row > :first-child');
            return {
              markerCount: markers.length,
              clusterCount: clusters.length,
              passageRect: passage.getBoundingClientRect().toJSON(),
              clusters: clusters.map(c => {
                const rect = c.getBoundingClientRect();
                const ms = c.querySelectorAll('.cr-folio-marker');
                const anchor = c.dataset.anchorPid;
                const verse = spread.querySelector(`.scripture-column [data-pid="${anchor}"]`);
                const vRect = verse?.getBoundingClientRect();
                return {
                  anchor,
                  markerCount: ms.length,
                  kinds: Array.from(ms).map(m => m.dataset.kind),
                  glyphs: Array.from(ms).map(m =>
                    getComputedStyle(m, '::before').content.replace(/['"]/g, '')
                  ),
                  top: rect.top,
                  height: rect.height,
                  verseTop: vRect?.top,
                  collisionDelta: vRect ? Math.round(rect.top - vRect.top) : null,
                };
              }),
              docOverflow: document.documentElement.scrollHeight - innerHeight,
              readerScrollH: document.getElementById('reader').scrollHeight,
            };
          }
        """
        )

        print(f"Genesis 1 — {info['markerCount']} markers across {info['clusterCount']} clusters")
        print(f"Scripture rect: L={info['passageRect']['left']:.0f} R={info['passageRect']['right']:.0f} W={info['passageRect']['width']:.0f}")
        print(f"Reader scrollHeight: {info['readerScrollH']}px (viewport 900)")
        print()
        for c in info['clusters']:
            print(f"  {c['anchor']:<10} ×{c['markerCount']:<2}  top={c['top']:.0f}  h={c['height']:.0f}  Δ={c['collisionDelta']}")
            print(f"             {' '.join(f'{g}({k})' for g, k in zip(c['glyphs'], c['kinds']))}")

        # Verify cluster sizes
        clusters_by_anchor = {c['anchor']: c for c in info['clusters']}
        assert clusters_by_anchor['gen.1.1']['markerCount'] == 5
        assert clusters_by_anchor['gen.1.3']['markerCount'] == 3
        assert clusters_by_anchor['gen.1.27']['markerCount'] == 3
        assert info['markerCount'] == 22

        # Capture individual cluster zones
        # 1:1 cluster
        page.evaluate("document.getElementById('reader').scrollTop = 0")
        page.wait_for_timeout(300)
        page.screenshot(path="reports/v27_cluster_1_1.png", clip={
            "x": 0, "y": 100, "width": 1440, "height": 600
        })

        # 1:3 cluster — scroll to it
        v3 = page.evaluate(
            "() => document.querySelector('.scripture-column [data-pid=\"gen.1.3\"]').offsetTop"
        )
        page.evaluate(f"document.getElementById('reader').scrollTop = {max(0, v3 - 250)}")
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v27_cluster_1_3.png")

        # 1:27 cluster
        v27 = page.evaluate(
            "() => document.querySelector('.scripture-column [data-pid=\"gen.1.27\"]').offsetTop"
        )
        page.evaluate(f"document.getElementById('reader').scrollTop = {v27 - 250}")
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v27_cluster_1_27.png")

        # Hover dense 1:1 cluster — plaque on first marker
        page.evaluate("document.getElementById('reader').scrollTop = 0")
        page.wait_for_timeout(400)
        page.hover('.cr-folio-cluster[data-anchor-pid="gen.1.1"] .cr-folio-marker')
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v27_cluster_1_1_hover.png")

        # Hover end marker of dense cluster
        page.hover(
            ".cr-folio-cluster[data-anchor-pid='gen.1.1'] .cr-folio-marker:last-child"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v27_cluster_1_1_lastmarker.png")

        # Debug mode capture
        page.evaluate("toggleFolioDebug()")
        page.evaluate("document.getElementById('reader').scrollTop = 0")
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v27_debug_top.png", full_page=False)

        # Full chapter scroll capture
        page.evaluate("toggleFolioDebug()")
        page.wait_for_timeout(200)
        page.evaluate("document.getElementById('reader').scrollTop = 0")
        page.wait_for_timeout(400)
        # Iterate scroll positions, capture
        scroll_h = info['readerScrollH']
        steps = 4
        for i, frac in enumerate([0.0, 0.33, 0.66, 0.95]):
            scroll = int(scroll_h * frac)
            page.evaluate(f"document.getElementById('reader').scrollTop = {scroll}")
            page.wait_for_timeout(400)
            page.screenshot(path=f"reports/v27_scroll_{i}.png")

        # Plaque overlap analysis — check that hovering each marker
        # in 1:1 cluster doesn't position a plaque that's clipped
        # by the viewport or overlaps scripture.
        page.evaluate("document.getElementById('reader').scrollTop = 0")
        page.wait_for_timeout(400)
        overlap_report = page.evaluate(
            """
          () => {
            const cluster = document.querySelector('.cr-folio-cluster[data-anchor-pid="gen.1.1"]');
            const markers = cluster.querySelectorAll('.cr-folio-marker');
            const results = [];
            const passage = document.querySelector('.scripture-column [data-pid="gen.1.1"]');
            const pRect = passage.getBoundingClientRect();
            for (const m of markers) {
              const plaque = m.querySelector('.cr-folio-plaque');
              // Compute plaque rect as if visible: read its computed
              // position (we cannot programmatically trigger :hover
              // for measurement, but offsetParent + offsets give us
              // the layout box).
              const mRect = m.getBoundingClientRect();
              // Plaque is position:absolute relative to marker.
              // CSS rules: right: calc(100% + 10px) — so left edge
              // would be at marker.left - 10 - plaque.width.
              const plaqueW = 240;
              const plaqueH = plaque.offsetHeight || 90;
              const plaqueLeft = mRect.left - 10 - plaqueW;
              const plaqueTop = mRect.top + mRect.height/2 - plaqueH/2;
              const plaqueRight = plaqueLeft + plaqueW;
              const plaqueBottom = plaqueTop + plaqueH;
              const overlapsScripture = !(
                plaqueRight < pRect.left || plaqueLeft > pRect.right ||
                plaqueBottom < pRect.top  || plaqueTop > pRect.bottom
              );
              const clippedLeft  = plaqueLeft < 0;
              const clippedTop   = plaqueTop  < 0;
              results.push({
                kind: m.dataset.kind,
                glyph: getComputedStyle(m, '::before').content.replace(/['"]/g, ''),
                plaqueLeft: Math.round(plaqueLeft),
                plaqueTop: Math.round(plaqueTop),
                plaqueRight: Math.round(plaqueRight),
                plaqueBottom: Math.round(plaqueBottom),
                overlapsScripture,
                clippedLeft,
                clippedTop,
              });
            }
            return results;
          }
        """
        )
        print("\nPlaque overlap analysis (gen.1.1 cluster, folio-RIGHT):")
        for r in overlap_report:
            flags = []
            if r['overlapsScripture']: flags.append('OVERLAPS-SCRIPTURE')
            if r['clippedLeft']: flags.append('CLIPPED-LEFT')
            if r['clippedTop']: flags.append('CLIPPED-TOP')
            tag = (' ' + ' '.join(flags)) if flags else ''
            print(f"  {r['glyph']} {r['kind']:<18} plaque: ({r['plaqueLeft']},{r['plaqueTop']}) - ({r['plaqueRight']},{r['plaqueBottom']}){tag}")

        b.close()
    print("\nALL CHECKS COMPLETE")


if __name__ == "__main__":
    main()
