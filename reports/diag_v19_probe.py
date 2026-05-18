"""v19 — real diagnostics before any change.

Reports exact pixel measurements for:
  1. Citation panel vs canon-book buttons (title leaf)
  2. Folio visibility, geometry, render state (reading room)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── PART 1: Title leaf citation overlap ─────────────────────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json",
            wait_until="networkidle",
        )
        page.wait_for_selector(".bible-cover-layout", timeout=10000)
        page.wait_for_timeout(500)

        cite_rect_closed = page.evaluate(
            "() => document.querySelector('.cite-corner > summary').getBoundingClientRect().toJSON()"
        )
        print(f"\n┌── TITLE LEAF ──────────────────────────────────────")
        print(f"│ Citation summary closed rect: {cite_rect_closed}")

        # Open citation panel
        page.click(".cite-corner > summary")
        page.wait_for_timeout(300)
        cite_info = page.evaluate(
            """
          () => {
            const panel = document.querySelector('.cite-corner .cc-citations');
            const books = Array.from(document.querySelectorAll('.bcl-canon-list li'));
            const layoutRect = document.querySelector('.bible-cover-layout').getBoundingClientRect();
            const panelRect = panel.getBoundingClientRect().toJSON();
            const overlaps = books.filter(li => {
              const r = li.getBoundingClientRect();
              return !(r.right < panelRect.left || r.left > panelRect.right ||
                       r.bottom < panelRect.top || r.top > panelRect.bottom);
            }).map(li => ({
              num: li.querySelector('.cc-toc-num')?.textContent.trim(),
              name: li.querySelector('.cc-toc-name')?.textContent.trim(),
              rect: li.getBoundingClientRect().toJSON(),
            }));
            return {
              panelRect,
              layoutRect,
              totalBooks: books.length,
              overlappingCount: overlaps.length,
              overlapping: overlaps.slice(0, 8),
            };
          }
        """
        )
        print(f"│ Citation panel rect: {cite_info['panelRect']}")
        print(f"│ Bible cover layout rect: {cite_info['layoutRect']}")
        print(f"│ Total books: {cite_info['totalBooks']}")
        print(f"│ BOOKS OVERLAPPED BY CITATION PANEL: {cite_info['overlappingCount']}")
        for o in cite_info["overlapping"]:
            print(f"│   #{o['num']} {o['name']}  {o['rect']}")
        print("└────────────────────────────────────────────────────")

        # ── PART 2: Reading room folio visibility ───────────────────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(700)

        # State BEFORE clicking Folio button
        before = page.evaluate(
            """
          () => {
            const folio = document.getElementById('folio');
            const cs = folio ? getComputedStyle(folio) : null;
            return {
              bodyClasses: Array.from(document.body.classList),
              folioInDOM: !!folio,
              folioCSS_display: cs?.display,
              folioCSS_position: cs?.position,
              folioCSS_visibility: cs?.visibility,
              folioCSS_opacity: cs?.opacity,
              folioRect: folio?.getBoundingClientRect().toJSON(),
              folioInnerHTML_len: folio?.querySelector('#folio-inner')?.innerHTML.length || 0,
              folioEntryCount: document.querySelectorAll('.cr-folio-entry').length,
              chapterRoom: document.body.classList.contains('chapter-room'),
              companionMode: document.body.classList.contains('companion-mode'),
              viewportW: innerWidth,
              viewportH: innerHeight,
            };
          }
        """
        )
        print(f"\n┌── READING ROOM (BEFORE Folio toggle) ──────────────")
        for k, v in before.items():
            print(f"│ {k}: {v}")
        print("└────────────────────────────────────────────────────")

        # Click Folio button
        page.click("#companion-toggle")
        page.wait_for_timeout(600)

        after = page.evaluate(
            """
          () => {
            const folio = document.getElementById('folio');
            const cs = folio ? getComputedStyle(folio) : null;
            const passage = document.querySelector('.cr-row .passage') || document.querySelector('.cr-row > :first-child');
            const folioRect = folio?.getBoundingClientRect().toJSON();
            const passageRect = passage?.getBoundingClientRect().toJSON();
            let overlap = null;
            if (folioRect && passageRect) {
              overlap = !(folioRect.right < passageRect.left || folioRect.left > passageRect.right ||
                          folioRect.bottom < passageRect.top || folioRect.top > passageRect.bottom);
            }
            // Records that SHOULD be in folio per data
            const recordsForGen1 = (currentData.genealogy || []).filter(r => {
              const a = r.anchors?.[0]?.target;
              if (!a) return false;
              return a.split('::').pop().startsWith('gen.1.');
            }).map(r => ({ kind: r.kind, title: r.title }));
            return {
              bodyClasses: Array.from(document.body.classList),
              folioCSS_display: cs?.display,
              folioCSS_position: cs?.position,
              folioCSS_visibility: cs?.visibility,
              folioCSS_opacity: cs?.opacity,
              folioCSS_width: cs?.width,
              folioCSS_zIndex: cs?.zIndex,
              folioCSS_top: cs?.top,
              folioCSS_right: cs?.right,
              folioCSS_left: cs?.left,
              folioRect,
              passageRect,
              overlapWithScripture: overlap,
              folioInnerHTML_len: folio?.querySelector('#folio-inner')?.innerHTML.length || 0,
              folioInnerFirstChild: folio?.querySelector('#folio-inner > *:first-child')?.outerHTML?.slice(0, 200),
              folioEntryCount: document.querySelectorAll('.cr-folio-entry').length,
              entries: Array.from(document.querySelectorAll('.cr-folio-entry')).map(el => ({
                title: el.querySelector('.cr-folio-title')?.textContent,
                kind: el.dataset.kind,
                rect: el.getBoundingClientRect().toJSON(),
              })),
              recordsForGen1,
              currentBook: typeof currentBook !== 'undefined' ? currentBook : '(unset)',
            };
          }
        """
        )
        print(f"\n┌── READING ROOM (AFTER Folio toggle) ───────────────")
        for k, v in after.items():
            if isinstance(v, list) and len(v) > 5:
                print(f"│ {k}: ({len(v)} items)")
                for item in v[:3]:
                    print(f"│   {item}")
            else:
                print(f"│ {k}: {v}")
        print("└────────────────────────────────────────────────────")

        # Try the side switch
        page.click("#companion-swap")
        page.wait_for_timeout(500)
        left_state = page.evaluate(
            """
          () => {
            const folio = document.getElementById('folio');
            const cs = getComputedStyle(folio);
            return {
              bodyClasses: Array.from(document.body.classList),
              folioRect: folio.getBoundingClientRect().toJSON(),
              folioLeft: cs.left,
              folioRight: cs.right,
            };
          }
        """
        )
        print(f"\n┌── AFTER Folio side swap ────────────────────────────")
        for k, v in left_state.items():
            print(f"│ {k}: {v}")
        print("└────────────────────────────────────────────────────")

        page.screenshot(path="reports/v19_probe_reading.png")
        b.close()


if __name__ == "__main__":
    main()
