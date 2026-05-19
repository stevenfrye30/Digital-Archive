"""v34 — folio synchronization refinement.

Verifies:
  1. Folio markers reflow when scripture font-size / line-height change
     (markers stay aligned with their anchor verses)
  2. Folio typography is decoupled from scripture controls
     (marker size and rubric size remain stable as --reader-size moves)
  3. "Apparatus" prefix removed; only CORE · STUDY · ARCHIVE remains
"""
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
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)

        def snapshot():
            return page.evaluate(
                """
              () => {
                const sample = pid => {
                  const v = document.querySelector(
                    `.scripture-column [data-pid="${pid}"]`);
                  const c = document.querySelector(
                    `.cr-folio-cluster[data-anchor-pid="${pid}"]`);
                  return {
                    pid,
                    verseTop: v ? v.offsetTop : null,
                    verseRect: v ? v.getBoundingClientRect().y : null,
                    clusterTopStyle: c ? parseFloat(c.style.top || '0') : null,
                    clusterRect: c ? c.getBoundingClientRect().y : null,
                  };
                };
                const markerSample = document.querySelector('.cr-folio-marker[data-authority="primary"]');
                const labelSample = document.querySelector(
                  '.cr-folio-depth-rubric .crd-label.active');
                return {
                  readerSize: getComputedStyle(document.documentElement)
                                .getPropertyValue('--reader-size').trim(),
                  readerLeading: getComputedStyle(document.documentElement)
                                .getPropertyValue('--reader-leading').trim(),
                  folioColFontSize: getComputedStyle(
                    document.querySelector('.folio-column')).fontSize,
                  markerFontSize: markerSample ? getComputedStyle(markerSample).fontSize : null,
                  markerWidth: markerSample ? getComputedStyle(markerSample).width : null,
                  rubricFontSize: labelSample ? getComputedStyle(labelSample).fontSize : null,
                  verses: ['gen.1.1', 'gen.1.3', 'gen.1.7', 'gen.1.14', 'gen.1.27']
                    .map(sample),
                };
              }
            """
            )

        # ── Baseline at default reader-size
        base = snapshot()
        print(f"BASELINE — reader-size={base['readerSize']} leading={base['readerLeading']}")
        print(f"  folio-column font-size: {base['folioColFontSize']}")
        print(f"  marker font: {base['markerFontSize']} width: {base['markerWidth']}")
        print(f"  rubric label font: {base['rubricFontSize']}")
        for v in base['verses']:
            print(f"  {v['pid']:<10} verse top={v['verseTop']} cluster top={v['clusterTopStyle']}")

        # Compute initial offset between cluster.top and verse.offsetTop
        offsets_before = [
            v['clusterTopStyle'] - v['verseTop']
            for v in base['verses'] if v['clusterTopStyle'] is not None and v['verseTop'] is not None
        ]
        print(f"  cluster-verse offsets (px): {offsets_before}")

        # ── Bump scripture font-size from 18 → 26
        page.evaluate(
            "document.getElementById('ctrl-size').value = '26'; "
            "document.getElementById('ctrl-size').dispatchEvent(new Event('input'));"
        )
        page.wait_for_timeout(700)
        big = snapshot()
        print(f"\nAFTER size 26 — reader-size={big['readerSize']}")
        print(f"  folio-column font-size: {big['folioColFontSize']}")
        print(f"  marker font: {big['markerFontSize']} width: {big['markerWidth']}")
        print(f"  rubric label font: {big['rubricFontSize']}")
        for v in big['verses']:
            print(f"  {v['pid']:<10} verse top={v['verseTop']} cluster top={v['clusterTopStyle']}")

        # ── Verify folio sizing did NOT scale with scripture
        assert big['folioColFontSize'] == base['folioColFontSize'], (
            f"folio col font scaled: {base['folioColFontSize']} -> {big['folioColFontSize']}"
        )
        assert big['markerFontSize'] == base['markerFontSize'], "marker font scaled"
        assert big['markerWidth'] == base['markerWidth'], "marker width scaled"
        assert big['rubricFontSize'] == base['rubricFontSize'], "rubric font scaled"
        print("  OK — folio sizing is stable across scripture-size change")

        # ── Verify markers DID reflow (cluster tops shifted with verses)
        # Each verse should have moved DOWN (later verses more so) and the
        # cluster's `top` style should track that movement.
        for v_base, v_big in zip(base['verses'], big['verses']):
            assert v_big['verseTop'] is not None and v_base['verseTop'] is not None
            verse_delta = v_big['verseTop'] - v_base['verseTop']
            cluster_delta = (v_big['clusterTopStyle'] or 0) - (v_base['clusterTopStyle'] or 0)
            print(f"  {v_base['pid']:<10} verse Δ={verse_delta:+d} cluster Δ={cluster_delta:+d}")
            # Clusters that previously sat AT the verse top should move
            # by the same amount; collision-shifted clusters can move
            # by more (downward) but never less than the verse shift.
            assert cluster_delta >= verse_delta - 2, (
                f"{v_base['pid']} cluster did not track verse: "
                f"verse moved {verse_delta} but cluster only moved {cluster_delta}"
            )
        print("  OK — folio clusters reflowed to track verse positions")

        # ── Bump line-height from 1.9 → 2.6
        page.evaluate(
            "document.getElementById('ctrl-spacing').value = '2.6'; "
            "document.getElementById('ctrl-spacing').dispatchEvent(new Event('input'));"
        )
        page.wait_for_timeout(700)
        spaced = snapshot()
        print(f"\nAFTER leading 2.6 — leading={spaced['readerLeading']}")
        for v in spaced['verses']:
            print(f"  {v['pid']:<10} verse top={v['verseTop']} cluster top={v['clusterTopStyle']}")
        for v_big, v_spaced in zip(big['verses'], spaced['verses']):
            verse_delta = v_spaced['verseTop'] - v_big['verseTop']
            cluster_delta = (v_spaced['clusterTopStyle'] or 0) - (v_big['clusterTopStyle'] or 0)
            print(f"  {v_big['pid']:<10} verse Δ={verse_delta:+d} cluster Δ={cluster_delta:+d}")
            assert cluster_delta >= verse_delta - 2
        # Folio typography still stable
        assert spaced['folioColFontSize'] == base['folioColFontSize']
        assert spaced['markerFontSize'] == base['markerFontSize']
        assert spaced['rubricFontSize'] == base['rubricFontSize']
        print("  OK — line-spacing change reflowed markers, folio sizing stable")

        # ── 3. "Apparatus" prefix removed
        rubric = page.evaluate(
            """
          () => {
            const r = document.querySelector('.cr-folio-depth-rubric');
            return {
              text: r ? r.textContent : null,
              hasPrefix: !!(r && r.querySelector('.crd-prefix')),
              labelTexts: r ? Array.from(r.querySelectorAll('.crd-label')).map(b => b.textContent) : [],
            };
          }
        """
        )
        print(f"\nRUBRIC textContent: {rubric['text']!r}")
        print(f"  has .crd-prefix child: {rubric['hasPrefix']}")
        print(f"  label texts: {rubric['labelTexts']}")
        assert not rubric['hasPrefix']
        assert 'Apparatus' not in (rubric['text'] or '')
        assert rubric['labelTexts'] == ['core', 'study', 'archive']
        print("  OK — Apparatus label removed; only CORE · STUDY · ARCHIVE remain")

        # Reset and capture screenshots
        page.evaluate(
            "document.getElementById('ctrl-size').value = '18'; "
            "document.getElementById('ctrl-size').dispatchEvent(new Event('input'));"
            "document.getElementById('ctrl-spacing').value = '1.9'; "
            "document.getElementById('ctrl-spacing').dispatchEvent(new Event('input'));"
        )
        page.wait_for_timeout(800)
        page.screenshot(path="reports/v34_default.png")
        page.evaluate(
            "document.getElementById('ctrl-size').value = '24'; "
            "document.getElementById('ctrl-size').dispatchEvent(new Event('input'));"
        )
        page.wait_for_timeout(800)
        page.screenshot(path="reports/v34_size24.png")

        b.close()
    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
