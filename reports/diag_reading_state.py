"""Probe reading-room state: are column controls visible? width?"""
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

        # Enter the reading room
        page.click(".bcl-enter-btn")
        page.wait_for_timeout(500)

        report = page.evaluate(
            """
          () => {
            const ctrlCols = document.getElementById('ctrl-columns');
            const ctrlsBar = document.getElementById('controls');
            const opts = Array.from(document.querySelectorAll('#ctrl-columns .col-opt'));
            const inner = document.getElementById('reader-inner');
            return {
              inReading: document.body.classList.contains('in-reading'),
              colsClasses: Array.from(document.body.classList).filter(c => c.startsWith('cols-')),
              ctrlBarDisplay: ctrlsBar ? getComputedStyle(ctrlsBar).display : null,
              ctrlColsExists: !!ctrlCols,
              ctrlColsDisplay: ctrlCols ? getComputedStyle(ctrlCols).display : null,
              ctrlColsRect: ctrlCols ? ctrlCols.getBoundingClientRect().toJSON() : null,
              optLabels: opts.map(o => o.textContent),
              activeOpt: document.querySelector('#ctrl-columns .col-opt.active')?.dataset.cols,
              readerInnerWidth: inner ? inner.getBoundingClientRect().width : null,
              readerInnerMaxWidth: inner ? getComputedStyle(inner).maxWidth : null,
              readerInnerColumnCount: inner ? getComputedStyle(inner).columnCount : null,
              viewportWidth: innerWidth,
            };
          }
        """
        )
        import json
        print(json.dumps(report, indent=2))

        page.screenshot(path="reports/probe_reading_state.png", full_page=False)
        b.close()


if __name__ == "__main__":
    main()
