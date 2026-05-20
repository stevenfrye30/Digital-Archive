"""v58 — Hierarchy legibility refinement.

Captures before/after snapshots of:
  1. The dense Genesis 1 cluster (full ARCHIVE depth).
  2. A single tertiary marker in resting + hover state.
  3. A single secondary marker in resting + hover state, mocked
     by temporarily promoting one record's authority via JS.
  4. A mixed secondary + tertiary cluster (mocked).

Pass `--phase before` or `--phase after` to label outputs.
The diagnostic also reports computed opacity / color / border
on tertiary and secondary so the editorial note can quote
exact values.
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

        # ── Genesis 1 dense cluster (ARCHIVE depth) ──────────────
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

        # Computed values on the FIRST tertiary marker
        tertiary_state = page.evaluate(
            """
            () => {
              const m = document.querySelector('.cr-folio-marker[data-authority="tertiary"]');
              if (!m) return null;
              const cs = getComputedStyle(m);
              return {
                opacity: cs.opacity,
                color: cs.color,
                background: cs.backgroundColor,
                border: cs.borderTop,
                fontSize: cs.fontSize,
              };
            }
            """
        )
        print(f"[{label.upper()}] Tertiary resting (gen.1):")
        for k, v in (tertiary_state or {}).items():
            print(f"  {k}: {v}")

        # Hover the same marker (force pseudo-class via JS evaluate)
        page.evaluate(
            """
            () => {
              const m = document.querySelector('.cr-folio-marker[data-authority="tertiary"]');
              if (m) m.dispatchEvent(new MouseEvent('mouseenter', {bubbles:true}));
            }
            """
        )
        # Actual hover requires Playwright's hover API
        first_marker = page.query_selector(
            '.cr-folio-marker[data-authority="tertiary"]'
        )
        if first_marker:
            first_marker.hover()
            page.wait_for_timeout(400)
            tertiary_hover = page.evaluate(
                """
                () => {
                  const m = document.querySelector(
                    '.cr-folio-marker[data-authority="tertiary"]:hover'
                  );
                  if (!m) return null;
                  const cs = getComputedStyle(m);
                  return {
                    opacity: cs.opacity,
                    color: cs.color,
                    background: cs.backgroundColor,
                    border: cs.borderTop,
                  };
                }
                """
            )
            print(f"[{label.upper()}] Tertiary hover (gen.1):")
            for k, v in (tertiary_hover or {}).items():
                print(f"  {k}: {v}")
            page.screenshot(
                path=f"reports/v58_{label}_tertiary_hover.png",
                clip={"x": 0, "y": 80, "width": 1440, "height": 600},
            )

        # Genesis 1 dense stack overall — move cursor off so no hover
        page.mouse.move(0, 0)
        page.wait_for_timeout(300)
        page.screenshot(
            path=f"reports/v58_{label}_gen1_dense.png",
            clip={"x": 0, "y": 80, "width": 1440, "height": 700},
        )

        # ── Mock secondary marker via direct DOM tweak ───────────
        # Promote the first marker temporarily so we can capture
        # secondary visual values. This is *capture-only* — does
        # not persist; no data model change.
        page.evaluate(
            """
            () => {
              const m = document.querySelector('.cr-folio-marker');
              if (m) m.dataset.authority = 'secondary';
              // also clone-and-promote a second one to make it
              // a mixed stack
              const ms = document.querySelectorAll('.cr-folio-marker');
              if (ms[2]) ms[2].dataset.authority = 'secondary';
            }
            """
        )
        page.wait_for_timeout(300)
        page.mouse.move(0, 0)
        page.wait_for_timeout(200)
        secondary_state = page.evaluate(
            """
            () => {
              const m = document.querySelector('.cr-folio-marker[data-authority="secondary"]');
              if (!m) return null;
              const cs = getComputedStyle(m);
              return {
                opacity: cs.opacity,
                color: cs.color,
                background: cs.backgroundColor,
                border: cs.borderTop,
                fontSize: cs.fontSize,
              };
            }
            """
        )
        print(f"[{label.upper()}] Secondary resting (mocked):")
        for k, v in (secondary_state or {}).items():
            print(f"  {k}: {v}")

        page.screenshot(
            path=f"reports/v58_{label}_mixed_stack.png",
            clip={"x": 0, "y": 80, "width": 1440, "height": 700},
        )

        sec_marker = page.query_selector(
            '.cr-folio-marker[data-authority="secondary"]'
        )
        if sec_marker:
            sec_marker.hover()
            page.wait_for_timeout(400)
            secondary_hover = page.evaluate(
                """
                () => {
                  const m = document.querySelector(
                    '.cr-folio-marker[data-authority="secondary"]:hover'
                  );
                  if (!m) return null;
                  const cs = getComputedStyle(m);
                  return {
                    opacity: cs.opacity,
                    color: cs.color,
                    background: cs.backgroundColor,
                    border: cs.borderTop,
                  };
                }
                """
            )
            print(f"[{label.upper()}] Secondary hover (mocked):")
            for k, v in (secondary_hover or {}).items():
                print(f"  {k}: {v}")
            page.screenshot(
                path=f"reports/v58_{label}_secondary_hover.png",
                clip={"x": 0, "y": 80, "width": 1440, "height": 600},
            )

        b.close()
    print(f"\n{label.upper()} snapshot complete.")


if __name__ == "__main__":
    main()
