"""Probe production at different user states + cache scenarios."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

PROD_URL = "https://stevenfrye30.github.io/Digital-Archive/?text=bible_kjv.json&p=gen.1.1"


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()

        # ── Scenario 1: fresh load WITHOUT clicking Folio toggle ─
        print("=" * 60)
        print("SCENARIO 1: fresh load, NO companion-toggle clicked")
        print("=" * 60)
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(PROD_URL, wait_until="networkidle", timeout=30000)
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(1500)
        state = page.evaluate(
            """
          () => ({
            companionMode: document.body.classList.contains('companion-mode'),
            markers: document.querySelectorAll('.cr-folio-marker').length,
            chapterSpread: !!document.querySelector('.chapter-spread'),
            folioColumn: !!document.querySelector('.folio-column'),
            folioColumnDisplay: document.querySelector('.folio-column')
              ? getComputedStyle(document.querySelector('.folio-column')).display
              : null,
            companionToggle: document.getElementById('companion-toggle')?.textContent,
            companionTogglePE: getComputedStyle(document.getElementById('companion-toggle'))?.pointerEvents,
            cols: Array.from(document.body.classList).filter(c => c.startsWith('cols-')),
          })
        """
        )
        print(state)
        page.screenshot(path="reports/v28_prod_initial.png")

        # ── Scenario 2: click Folio toggle
        print("\n" + "=" * 60)
        print("SCENARIO 2: after clicking Folio toggle")
        print("=" * 60)
        page.click("#companion-toggle")
        page.wait_for_timeout(1000)
        state2 = page.evaluate(
            """
          () => ({
            companionMode: document.body.classList.contains('companion-mode'),
            markers: document.querySelectorAll('.cr-folio-marker').length,
            firstMarkerRect: document.querySelector('.cr-folio-marker')?.getBoundingClientRect().toJSON(),
            firstMarkerOpacity: document.querySelector('.cr-folio-marker')
              ? getComputedStyle(document.querySelector('.cr-folio-marker')).opacity
              : null,
            folioColumnDisplay: document.querySelector('.folio-column')
              ? getComputedStyle(document.querySelector('.folio-column')).display
              : null,
            folioColumnRect: document.querySelector('.folio-column')
              ? document.querySelector('.folio-column').getBoundingClientRect().toJSON()
              : null,
          })
        """
        )
        print(state2)
        page.screenshot(path="reports/v28_prod_after_toggle.png")
        ctx.close()

        # ── Scenario 3: simulate stale browser cache via "old" service-worker-less load
        # ── Test at common viewport widths ──────────────────────
        for w in [1440, 1366, 1280, 1024]:
            print(f"\n=== viewport {w}×900 ===")
            ctx = b.new_context(viewport={"width": w, "height": 900})
            page = ctx.new_page()
            page.goto(PROD_URL, wait_until="networkidle", timeout=30000)
            page.wait_for_function(
                "typeof currentData === 'object' && currentData && currentData.passages",
                timeout=15000,
            )
            page.wait_for_timeout(1000)
            try:
                page.click("#companion-toggle", timeout=4000)
                page.wait_for_timeout(700)
            except Exception:
                pass
            r = page.evaluate(
                """
              () => ({
                companion: document.body.classList.contains('companion-mode'),
                cols: Array.from(document.body.classList).filter(c => c.startsWith('cols-')),
                fc: document.querySelector('.folio-column')
                  ? getComputedStyle(document.querySelector('.folio-column')).display
                  : 'no-folio-column',
                markers: document.querySelectorAll('.cr-folio-marker').length,
                togglePE: getComputedStyle(document.getElementById('companion-toggle')).pointerEvents,
              })
            """
            )
            print(f"  {r}")
            ctx.close()

        b.close()


if __name__ == "__main__":
    main()
