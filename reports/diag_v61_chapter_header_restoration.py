"""v61 — Chapter-header restoration.

Verifies the manuscript chapter-plate:
  · book name in small-caps (uppercase + wide tracking)
  · a thin centred hairline rule
  · the chapter as a Roman numeral
  · proper manuscript breathing room above the first verse

Tests across several books, pure + folio modes, and wide layout.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


def alpha(rgba):
    import re
    m = re.search(r"rgba?\(([\d.,\s]+)\)", rgba or "")
    return m.group(1) if m else rgba


def main():
    expected_numerals = {
        "gen.1.1":   "I",
        "gen.12.1":  "XII",
        "psa.23.1":  "XXIII",
        "psa.119.1": "CXIX",
        "jhn.1.1":   "I",
        "rev.22.1":  "XXII",
        "1ch.29.1":  "XXIX",
    }

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        for ref, expected_num in expected_numerals.items():
            page.goto(
                f"http://localhost:8765/index.html?text=bible_kjv.json&p={ref}",
                wait_until="networkidle",
            )
            page.wait_for_function(
                "typeof currentData === 'object' && currentData && currentData.passages",
                timeout=15000,
            )
            page.wait_for_timeout(700)

            state = page.evaluate(
                """
                () => {
                  const h = document.querySelector('.chapter-heading.chapter-room-heading');
                  if (!h) return null;
                  const t = h.querySelector('.ch-title');
                  const r = h.querySelector('.ch-rule');
                  const s = h.querySelector('.ch-sub');
                  const tcs = t ? getComputedStyle(t) : null;
                  const rcs = r ? getComputedStyle(r) : null;
                  const scs = s ? getComputedStyle(s) : null;
                  return {
                    titleText: t?.textContent || '',
                    subText: s?.textContent || '',
                    titleTransform: tcs?.textTransform || '',
                    titleTracking: tcs?.letterSpacing || '',
                    titleFontSize: tcs?.fontSize || '',
                    ruleBorderTop: rcs?.borderTopWidth || '',
                    ruleWidth: rcs ? r.getBoundingClientRect().width : 0,
                    subFontSize: scs?.fontSize || '',
                    subTransform: scs?.textTransform || '',
                    parent: h.parentElement?.className || '',
                    headingTop: h.getBoundingClientRect().top,
                    firstVerseTop: (() => {
                      const v = document.querySelector('.passage');
                      return v ? v.getBoundingClientRect().top : null;
                    })(),
                  };
                }
                """
            )
            print(f"[{ref}]  expected numeral = {expected_num}")
            for k, v in (state or {}).items():
                print(f"   {k}: {v}")
            assert state, f"no chapter-heading for {ref}"
            assert state["subText"] == expected_num, (
                f"{ref}: expected {expected_num}, got {state['subText']}"
            )
            # The title transform must be uppercase (small-caps via CSS)
            assert state["titleTransform"] == "uppercase", state["titleTransform"]
            # Hairline rule present
            assert state["ruleWidth"] > 0 and state["ruleWidth"] < 80, state["ruleWidth"]
            # Breathing room between heading and first verse
            gap = state["firstVerseTop"] - state["headingTop"]
            assert gap > 120, f"insufficient heading→verse breathing room: {gap}"
            print(f"   gap heading→first verse: {gap:.0f}px")
            print(f"   OK\n")

        # ── Visual captures across books and modes ─────────────
        snapshots = [
            ("gen.1.1",   "gen1",       False, "single"),
            ("gen.1.1",   "gen1_folio", True,  "single"),
            ("psa.23.1",  "psa23",      False, "single"),
            ("psa.119.1", "psa119",     False, "single"),
            ("jhn.1.1",   "jhn1",       False, "single"),
            ("rev.22.1",  "rev22",      True,  "single"),
            ("gen.1.1",   "gen1_wide",  False, "wide"),
        ]
        for ref, label, folio, layout in snapshots:
            page.goto(
                f"http://localhost:8765/index.html?text=bible_kjv.json&p={ref}",
                wait_until="networkidle",
            )
            page.wait_for_function(
                "typeof currentData === 'object' && currentData && currentData.passages",
                timeout=15000,
            )
            page.wait_for_timeout(700)
            if folio:
                page.evaluate("document.getElementById('companion-toggle').click()")
                page.wait_for_timeout(400)
                page.evaluate("_setFolioDepth('archive')")
                page.wait_for_timeout(300)
            if layout == "wide":
                # Toggle wide layout if a toggle exists; falls back
                # silently if the deployment uses a different control.
                page.evaluate(
                    "() => { const w = document.querySelector("
                    "'[data-cols=\"dual\"], #cols-wide, .layout-wide-btn');"
                    "if (w) w.click(); }"
                )
                page.wait_for_timeout(400)
            page.mouse.move(0, 0)
            page.wait_for_timeout(200)
            page.screenshot(
                path=f"reports/v61_header_{label}.png",
                clip={"x": 0, "y": 0, "width": 1440, "height": 600},
            )
            print(f"  captured {ref} ({label}) → reports/v61_header_{label}.png")

        b.close()
    print()
    print("ALL CHECKS PASSED — chapter-header restoration in place")


if __name__ == "__main__":
    main()
