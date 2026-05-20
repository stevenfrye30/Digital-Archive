"""v57 — Biblical Corpus Deepening (first wave).

Verifies three refinements:
  1. Canonical genre intelligence — body[data-canon-genre] stamps
     per book class, with subtle margin-bottom deltas on .passage
     (felt, not displayed).
  2. Silent folio empty state — no "No witnesses anchored to this
     chapter." text; the parchment is undisturbed when empty.
  3. Scripture printworthiness — passages avoid page-break-inside,
     chapter headings avoid page-break-after, folio sidebar is
     suppressed in print so scripture reclaims the full measure.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import re
from playwright.sync_api import sync_playwright


def pxnum(s):
    m = re.match(r"([\d.]+)", (s or "").strip())
    return float(m.group(1)) if m else 0.0


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── 1. Canonical genre intelligence ──────────────────────
        #
        # Probe four representative book classes and confirm the
        # body carries the right genre stamp plus a distinct
        # passage margin-bottom.

        probes = [
            ("gen.1.1",   "torah",      "1.1"),   # baseline
            ("psa.1.1",   "wisdom",     "1.3"),   # breath
            ("isa.1.1",   "prophets",   "1.0"),   # density
            ("jhn.1.1",   "gospel",     "1.1"),   # baseline (narrative)
            ("rev.1.1",   "apocalypse", "1.35"),  # pause
        ]
        for ref, expected_genre, expected_margin in probes:
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
                  const genre = document.body.dataset.canonGenre || '';
                  const passage = document.querySelector('.passage');
                  return {
                    genre,
                    margin: passage ? getComputedStyle(passage).marginBottom : null,
                    fontSize: passage ? getComputedStyle(passage).fontSize : null,
                  };
                }
                """
            )
            margin_px = pxnum(state["margin"])
            font_px = pxnum(state["fontSize"])
            ratio = round(margin_px / font_px, 2) if font_px else None
            print(f"{ref:<10} genre={state['genre']:<11} margin={state['margin']!s:<10} (≈{ratio}em)")
            assert state["genre"] == expected_genre, (ref, state["genre"], expected_genre)
            # Compare ratio to expected em; tolerate ±0.03em rounding
            assert ratio is not None
            assert abs(ratio - float(expected_margin)) < 0.05, (
                ref, ratio, expected_margin
            )
        print("  OK — five book classes stamp correctly with distinct cadence\n")

        # ── 2. Silent folio empty state ──────────────────────────
        #
        # Find a chapter with no Atlas Object anchors — e.g. lev.10
        # (Aaron's sons; no AO at present) — and confirm that under
        # companion mode the folio column carries NO empty-state
        # message.
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=lev.10.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(700)
        empty_probe = page.evaluate(
            """
            () => {
              const col = document.querySelector(
                '#passages .chapter-spread .folio-column'
              );
              if (!col) return { exists: false };
              return {
                exists: true,
                hasEmptyDiv: !!col.querySelector('.cr-folio-empty'),
                text: col.textContent.trim(),
                clusters: col.querySelectorAll('.cr-folio-cluster').length,
              };
            }
            """
        )
        print(f"Leviticus 10 folio column: {empty_probe}")
        if empty_probe["exists"]:
            assert not empty_probe["hasEmptyDiv"], (
                "empty-state div still rendering"
            )
            assert "No witnesses" not in (empty_probe["text"] or "")
            print("  OK — chapter with no anchors renders nothing (silent)\n")

        # ── 3. Scripture printworthiness ─────────────────────────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(700)
        page.emulate_media(media="print")
        page.wait_for_timeout(300)
        print_state = page.evaluate(
            """
            () => {
              const passage = document.querySelector('.passage');
              const heading = document.querySelector('.chapter-heading');
              const spread = document.querySelector('#passages .chapter-spread');
              const folioCol = document.querySelector(
                '#passages .chapter-spread .folio-column'
              );
              return {
                passagePageBreak: passage ? getComputedStyle(passage).pageBreakInside : null,
                passageBreak: passage ? getComputedStyle(passage).breakInside : null,
                headingPageBreakAfter: heading ? getComputedStyle(heading).pageBreakAfter : null,
                headingBreakAfter: heading ? getComputedStyle(heading).breakAfter : null,
                spreadDisplay: spread ? getComputedStyle(spread).display : null,
                folioColDisplay: folioCol ? getComputedStyle(folioCol).display : null,
              };
            }
            """
        )
        print(f"Print emulation @ gen.1.1:")
        for k, v in print_state.items():
            print(f"  {k}: {v}")
        # Page-break-inside avoid on passage
        assert print_state["passagePageBreak"] in ("avoid",)
        assert print_state["passageBreak"] in ("avoid", "avoid-page")
        # Chapter heading: avoid orphaning. Modern engines map
        # the legacy page-break-after to the standard break-after,
        # so either reporting an empty legacy value or 'avoid-page'
        # on the standard property is acceptable.
        assert (
            print_state["headingPageBreakAfter"] == "avoid"
            or print_state["headingBreakAfter"] in ("avoid", "avoid-page")
        )
        # Folio column suppressed in print
        if print_state["folioColDisplay"] is not None:
            assert print_state["folioColDisplay"] == "none"
        print("  OK — scripture printworthiness rules apply\n")

        page.screenshot(path="reports/v57_print_scripture.png", full_page=False)

        b.close()
    print("ALL CHECKS PASSED — biblical corpus deepening v57 operational")


if __name__ == "__main__":
    main()
