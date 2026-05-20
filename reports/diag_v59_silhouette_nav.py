"""v59 — Silhouette/weight refinement + navigation coherence.

Captures snapshots for:
  1. Dense gen.1 rail (ARCHIVE depth) — silhouette read.
  2. Mixed secondary + tertiary stack (mocked).
  3. Sparse chapter rail (e.g. exo.40 — only one originating AO).
  4. Navigation back-flow from Bible cover.

Run with --phase before|after.
"""
import sys
import argparse
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["before", "after"], default="before")
    args = ap.parse_args()
    label = args.phase

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── 1. Dense Genesis 1 rail ──────────────────────────────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
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
        page.wait_for_timeout(500)
        page.mouse.move(0, 0)
        page.wait_for_timeout(200)

        # Compute box sizes / glyph sizes per tier
        tier_metrics = page.evaluate(
            """
            () => {
              const get = (sel) => {
                const m = document.querySelector(sel);
                if (!m) return null;
                const cs = getComputedStyle(m);
                const rect = m.getBoundingClientRect();
                return {
                  width: rect.width,
                  height: rect.height,
                  fontSize: cs.fontSize,
                  borderWidth: cs.borderTopWidth,
                  borderStyle: cs.borderTopStyle,
                  background: cs.backgroundColor,
                  opacity: cs.opacity,
                  color: cs.color,
                };
              };
              return {
                tertiary: get('.cr-folio-marker[data-authority="tertiary"]'),
              };
            }
            """
        )
        print(f"[{label.upper()}] Tertiary in dense rail:")
        for k, v in (tier_metrics.get("tertiary") or {}).items():
            print(f"  {k}: {v}")

        page.screenshot(
            path=f"reports/v59_{label}_gen1_dense.png",
            clip={"x": 0, "y": 80, "width": 1440, "height": 760},
        )

        # ── 2. Mixed secondary + tertiary stack (mock) ───────────
        page.evaluate(
            """
            () => {
              const ms = document.querySelectorAll('.cr-folio-marker');
              for (let i = 0; i < ms.length; i++) {
                if (i % 2 === 0) ms[i].dataset.authority = 'secondary';
              }
              if (typeof _positionFolioEntries === 'function') {
                _positionFolioEntries();
              }
            }
            """
        )
        page.wait_for_timeout(400)
        page.mouse.move(0, 0)
        page.wait_for_timeout(200)
        secondary_metrics = page.evaluate(
            """
            () => {
              const m = document.querySelector('.cr-folio-marker[data-authority="secondary"]');
              if (!m) return null;
              const cs = getComputedStyle(m);
              const rect = m.getBoundingClientRect();
              return {
                width: rect.width,
                height: rect.height,
                fontSize: cs.fontSize,
                borderWidth: cs.borderTopWidth,
                background: cs.backgroundColor,
              };
            }
            """
        )
        print(f"[{label.upper()}] Secondary in mixed rail:")
        for k, v in (secondary_metrics or {}).items():
            print(f"  {k}: {v}")

        page.screenshot(
            path=f"reports/v59_{label}_mixed_stack.png",
            clip={"x": 0, "y": 80, "width": 1440, "height": 760},
        )

        # ── 3. Sparse chapter rail (exo.40 — one AO) ─────────────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=exo.40.34",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(600)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        page.mouse.move(0, 0)
        page.wait_for_timeout(200)
        page.screenshot(
            path=f"reports/v59_{label}_sparse_rail.png",
            clip={"x": 0, "y": 80, "width": 1440, "height": 700},
        )

        # ── 4. Navigation back-flow ──────────────────────────────
        # Start on the Bible cover.
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.screenshot(path=f"reports/v59_{label}_nav_cover.png")

        # Click the "← Bible Versions" back button on the cover.
        # The button class is .bcl-back-to-versions.
        page.evaluate(
            """
            () => {
              const btn = document.querySelector('.bcl-back-to-versions');
              if (btn) btn.click();
            }
            """
        )
        page.wait_for_timeout(1200)

        landing = page.evaluate(
            """
            () => {
              const crumb = document.getElementById('browse-crumb');
              const title = document.getElementById('browse-title');
              const tiles = document.getElementById('browse-tiles');
              return {
                crumb: crumb ? crumb.textContent.trim() : null,
                title: title ? title.textContent.trim() : null,
                tileCount: tiles ? tiles.querySelectorAll('.text-tile').length : 0,
              };
            }
            """
        )
        print(f"[{label.upper()}] Cover → back landing:")
        for k, v in landing.items():
            print(f"  {k}: {v!r}")
        page.screenshot(path=f"reports/v59_{label}_nav_after_back.png")

        b.close()
    print(f"\n{label.upper()} snapshots complete.")


if __name__ == "__main__":
    main()
