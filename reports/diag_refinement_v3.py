"""Verify the v3 Bible title leaf + reading room refinement pass."""
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
        page.wait_for_selector(".bible-cover-layout", timeout=10000)
        page.wait_for_timeout(400)

        leaf = page.evaluate(
            """
          () => {
            const reader = document.getElementById('reader');
            const layout = document.querySelector('.bible-cover-layout');
            const enter = document.querySelector('.bcl-enter-btn');
            const cite = document.querySelector('.bible-cover-layout .cite-corner');
            const oldCite = document.querySelector('.cite-disclosure');
            const ctrlCols = document.getElementById('ctrl-columns');
            const ctrlColsStyle = ctrlCols ? getComputedStyle(ctrlCols) : null;
            return {
              viewportHeight: innerHeight,
              readerScrollHeight: reader.scrollHeight,
              readerClientHeight: reader.clientHeight,
              fitsNoScroll: reader.scrollHeight <= reader.clientHeight + 4,
              enterRect: enter ? enter.getBoundingClientRect().toJSON() : null,
              citeCornerRect: cite ? cite.getBoundingClientRect().toJSON() : null,
              citeCornerInTopRight: cite
                ? (cite.getBoundingClientRect().right >= layout.getBoundingClientRect().right - 80
                  && cite.getBoundingClientRect().top - layout.getBoundingClientRect().top <= 40)
                : false,
              legacyCiteDisclosureMissing: oldCite === null,
              ctrlColumnsDisplayOnTitleLeaf: ctrlColsStyle ? ctrlColsStyle.display : 'n/a',
              bookCount: document.querySelectorAll('.bcl-canon-list li').length,
              sections: Array.from(document.querySelectorAll('.bcl-canon-section')).map(s => ({
                canon: s.dataset.canon,
                label: s.querySelector('.bcl-canon-label')?.textContent,
                count: s.querySelectorAll('li').length,
              })),
              wrappedNames: Array.from(document.querySelectorAll('.bcl-canon-list li')).filter(li => {
                const name = li.querySelector('.cc-toc-name');
                if (!name) return false;
                const r = name.getBoundingClientRect();
                const cs = getComputedStyle(name);
                const lineH = parseFloat(cs.lineHeight) || (parseFloat(cs.fontSize) * 1.2);
                return r.height > lineH * 1.4;
              }).map(li => li.querySelector('.cc-toc-name').textContent),
            };
          }
        """
        )
        print("LEAF:", leaf)
        assert leaf["fitsNoScroll"], (
            f"reader scrolls: {leaf['readerScrollHeight']} > {leaf['readerClientHeight']}"
        )
        assert leaf["enterRect"]["bottom"] <= leaf["viewportHeight"] + 1, (
            "Enter button below fold"
        )
        assert leaf["citeCornerInTopRight"], (
            f"Cite corner not in top-right: {leaf['citeCornerRect']}"
        )
        assert leaf["legacyCiteDisclosureMissing"], "Old centered cite-disclosure still present"
        assert leaf["ctrlColumnsDisplayOnTitleLeaf"] == "none", (
            f"Column switcher visible on title leaf: {leaf['ctrlColumnsDisplayOnTitleLeaf']}"
        )
        assert leaf["bookCount"] == 80, f"Expected 80 books, got {leaf['bookCount']}"
        print("WRAPPED:", leaf["wrappedNames"])

        page.screenshot(path="reports/v3_titleleaf.png")

        # Enter the reading room
        page.click(".bcl-enter-btn")
        page.wait_for_timeout(400)

        room = page.evaluate(
            """
          () => {
            const ctrlCols = document.getElementById('ctrl-columns');
            const ctrlColsStyle = ctrlCols ? getComputedStyle(ctrlCols) : null;
            const heading = document.querySelector('.chapter-room-heading');
            const headingRect = heading ? heading.getBoundingClientRect().toJSON() : null;
            return {
              inReading: document.body.classList.contains('in-reading'),
              chapterRoom: document.body.classList.contains('chapter-room'),
              colsClass: Array.from(document.body.classList).filter(c => c.startsWith('cols-')),
              ctrlColumnsDisplay: ctrlColsStyle ? ctrlColsStyle.display : 'n/a',
              headingTop: headingRect ? headingRect.top : null,
              activeColOpt: document.querySelector('#ctrl-columns .col-opt.active')?.dataset.cols,
              colOpts: Array.from(document.querySelectorAll('#ctrl-columns .col-opt')).map(el => el.textContent),
            };
          }
        """
        )
        print("ROOM:", room)
        assert room["inReading"], "Not in reading mode"
        assert room["chapterRoom"], "Not in chapter-room"
        assert room["ctrlColumnsDisplay"] != "none", (
            f"Column switcher hidden in reading room: {room['ctrlColumnsDisplay']}"
        )
        assert "cols-single" in room["colsClass"], (
            f"Default not cols-single: {room['colsClass']}"
        )
        assert room["colOpts"] == ["single", "dual", "wide"], (
            f"Column option labels wrong: {room['colOpts']}"
        )
        assert room["activeColOpt"] == "single"
        # Heading should be relatively near top now (< 100px ideally)
        assert room["headingTop"] is not None and room["headingTop"] < 200, (
            f"Heading too far down: {room['headingTop']}"
        )

        page.screenshot(path="reports/v3_reading_single.png")

        # Switch to dual
        page.evaluate("document.querySelector('#ctrl-columns .col-opt[data-cols=\"dual\"]').click()")
        page.wait_for_timeout(200)
        dual = page.evaluate(
            """
          () => {
            const inner = document.getElementById('reader-inner');
            const cs = getComputedStyle(inner);
            return {
              colsClass: Array.from(document.body.classList).filter(c => c.startsWith('cols-')),
              columnCount: cs.columnCount,
              maxWidth: cs.maxWidth,
              activeColOpt: document.querySelector('#ctrl-columns .col-opt.active')?.dataset.cols,
            };
          }
        """
        )
        print("DUAL:", dual)
        assert "cols-dual" in dual["colsClass"]
        assert dual["columnCount"] == "2", f"columnCount: {dual['columnCount']}"
        assert dual["activeColOpt"] == "dual"
        page.screenshot(path="reports/v3_reading_dual.png")

        # Switch to wide
        page.evaluate("document.querySelector('#ctrl-columns .col-opt[data-cols=\"wide\"]').click()")
        page.wait_for_timeout(200)
        wide = page.evaluate(
            """
          () => {
            const inner = document.getElementById('reader-inner');
            const cs = getComputedStyle(inner);
            return {
              colsClass: Array.from(document.body.classList).filter(c => c.startsWith('cols-')),
              columnCount: cs.columnCount,
              maxWidth: cs.maxWidth,
              activeColOpt: document.querySelector('#ctrl-columns .col-opt.active')?.dataset.cols,
            };
          }
        """
        )
        print("WIDE:", wide)
        assert "cols-wide" in wide["colsClass"]
        assert wide["columnCount"] == "1"
        assert wide["activeColOpt"] == "wide"
        page.screenshot(path="reports/v3_reading_wide.png")

        # Verify clicking Cite opens the corner panel
        page.goto(URL, wait_until="networkidle")
        page.wait_for_selector(".bible-cover-layout", timeout=10000)
        page.wait_for_timeout(400)
        page.click(".bible-cover-layout .cite-corner > summary")
        page.wait_for_timeout(200)
        cite_open = page.evaluate(
            """
          () => {
            const cite = document.querySelector('.bible-cover-layout .cite-corner');
            const panel = cite?.querySelector('.cc-citations');
            const panelRect = panel ? panel.getBoundingClientRect().toJSON() : null;
            return {
              isOpen: cite?.open,
              panelVisible: panel && panelRect.width > 100,
              panelRect,
            };
          }
        """
        )
        print("CITE OPEN:", cite_open)
        assert cite_open["isOpen"], "Cite disclosure failed to open"
        assert cite_open["panelVisible"], "Cite panel not visible after open"
        page.screenshot(path="reports/v3_cite_open.png")

        b.close()
    print("ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
