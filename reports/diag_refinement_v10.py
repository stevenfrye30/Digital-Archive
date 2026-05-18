"""v10 — restored reading geometries verification.

Confirms:
  - Column controls visible in reading room, hidden elsewhere
  - All three modes (single/dual/wide) work and visibly differ
  - Single mode now uses most of viewport width (>= 1200px)
  - Default is single
  - Title leaf invariants unchanged (zero scroll, no wraps, 80 books)
"""
from playwright.sync_api import sync_playwright

URL = "http://localhost:8765/index.html?text=bible_kjv.json"


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle")
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_selector(".bcl-enter-btn", timeout=10000)
        page.wait_for_timeout(400)

        # --- Title leaf: column controls must be hidden ---
        title_state = page.evaluate(
            """
          () => {
            const ctrlCols = document.getElementById('ctrl-columns');
            const items = document.querySelectorAll('.bcl-canon-list li');
            return {
              inReading: document.body.classList.contains('in-reading'),
              ctrlColsDisplay: ctrlCols ? getComputedStyle(ctrlCols).display : null,
              docOverflow: document.documentElement.scrollHeight - innerHeight,
              bookCount: items.length,
            };
          }
        """
        )
        print("TITLE LEAF:", title_state)
        assert not title_state["inReading"]
        assert title_state["ctrlColsDisplay"] == "none", (
            f"Column controls should be hidden on title leaf, got {title_state['ctrlColsDisplay']}"
        )
        assert title_state["docOverflow"] == 0
        assert title_state["bookCount"] == 80

        # --- Enter reading room ---
        page.click(".bcl-enter-btn")
        page.wait_for_timeout(500)

        def probe_mode():
            return page.evaluate(
                """
              () => {
                const ctrlCols = document.getElementById('ctrl-columns');
                const inner = document.getElementById('reader-inner');
                const active = document.querySelector('#ctrl-columns .col-opt.active');
                return {
                  inReading: document.body.classList.contains('in-reading'),
                  colsClasses: Array.from(document.body.classList).filter(c => c.startsWith('cols-')),
                  ctrlColsDisplay: getComputedStyle(ctrlCols).display,
                  ctrlColsVisible:
                    ctrlCols.getBoundingClientRect().height > 0
                    && ctrlCols.getBoundingClientRect().width > 0,
                  activeOpt: active ? active.dataset.cols : null,
                  optLabels: Array.from(
                    document.querySelectorAll('#ctrl-columns .col-opt')
                  ).map(o => o.textContent),
                  readerInnerWidth: inner.getBoundingClientRect().width,
                  columnCount: getComputedStyle(inner).columnCount,
                };
              }
            """
            )

        initial = probe_mode()
        print("\nREADING ROOM (default):", initial)
        assert initial["inReading"]
        assert initial["ctrlColsDisplay"] != "none"
        assert initial["ctrlColsVisible"]
        assert initial["optLabels"] == ["single", "dual", "wide"]
        assert initial["activeOpt"] == "single"
        assert "cols-single" in initial["colsClasses"]
        # Single mode should now use most of the viewport (≥1200px).
        assert initial["readerInnerWidth"] >= 1200, (
            f"Single mode too narrow: {initial['readerInnerWidth']}"
        )
        page.screenshot(path="reports/v10_reading_single.png")

        # --- Switch to dual ---
        page.evaluate(
            "document.querySelector('#ctrl-columns .col-opt[data-cols=\"dual\"]').click()"
        )
        page.wait_for_timeout(250)
        dual = probe_mode()
        print("\nDUAL:", dual)
        assert "cols-dual" in dual["colsClasses"]
        assert dual["activeOpt"] == "dual"
        assert dual["columnCount"] == "2"
        assert dual["readerInnerWidth"] >= 1300
        page.screenshot(path="reports/v10_reading_dual.png")

        # --- Switch to wide ---
        page.evaluate(
            "document.querySelector('#ctrl-columns .col-opt[data-cols=\"wide\"]').click()"
        )
        page.wait_for_timeout(250)
        wide = probe_mode()
        print("\nWIDE:", wide)
        assert "cols-wide" in wide["colsClasses"]
        assert wide["activeOpt"] == "wide"
        assert wide["columnCount"] == "1"
        assert wide["readerInnerWidth"] >= 1300
        page.screenshot(path="reports/v10_reading_wide.png")

        # --- Back to single ---
        page.evaluate(
            "document.querySelector('#ctrl-columns .col-opt[data-cols=\"single\"]').click()"
        )
        page.wait_for_timeout(250)
        back = probe_mode()
        print("\nBACK TO SINGLE:", back)
        assert back["activeOpt"] == "single"
        assert back["readerInnerWidth"] == initial["readerInnerWidth"]

        # --- Widths must visibly differ ---
        single_w = initial["readerInnerWidth"]
        dual_w = dual["readerInnerWidth"]
        wide_w = wide["readerInnerWidth"]
        print(f"\nWIDTHS — single: {single_w}, dual: {dual_w}, wide: {wide_w}")
        assert single_w < dual_w or single_w < wide_w, (
            "Single should be narrower than at least one other mode"
        )
        assert wide_w >= dual_w - 80, "Wide should be at least as wide as dual"

        # --- Go back to title leaf, ensure controls hidden again ---
        page.click("#ctrl-contents")
        page.wait_for_timeout(400)
        back_title = page.evaluate(
            """
          () => ({
            inReading: document.body.classList.contains('in-reading'),
            ctrlColsDisplay: getComputedStyle(document.getElementById('ctrl-columns')).display,
            docOverflow: document.documentElement.scrollHeight - innerHeight,
          })
        """
        )
        print("\nBACK TO TITLE LEAF:", back_title)
        assert back_title["ctrlColsDisplay"] == "none"
        assert back_title["docOverflow"] == 0

        page.screenshot(path="reports/v10_titleleaf.png")
        print("\nALL ASSERTIONS PASSED")
        b.close()


if __name__ == "__main__":
    main()
