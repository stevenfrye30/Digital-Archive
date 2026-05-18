"""Walk every container on the title leaf and report any element
whose scrollHeight exceeds clientHeight, OR whose bounding bottom
exceeds the viewport. This catches the microscopic scrollbar
visible on Windows Chrome but not on headless Linux.
"""
from playwright.sync_api import sync_playwright

URL = "http://localhost:8765/index.html?text=bible_kjv.json"


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        # Simulate a Windows-style scrollbar that takes pixel space
        # (Chrome on Windows typically reserves ~17px for the scrollbar).
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle")
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_selector(".bible-cover-layout", timeout=10000)
        page.wait_for_timeout(400)

        report = page.evaluate(
            """
          () => {
            const vp = innerHeight;
            const out = [];
            function walk(el, depth) {
              if (!el || depth > 8) return;
              const cs = getComputedStyle(el);
              const r = el.getBoundingClientRect();
              const overflowsSelf = el.scrollHeight > el.clientHeight + 0.5;
              const exceedsViewport = r.bottom > vp + 0.5;
              if (overflowsSelf || exceedsViewport || depth <= 3) {
                out.push({
                  tag: el.tagName.toLowerCase(),
                  id: el.id || null,
                  cls: el.className?.toString?.().slice(0, 60) || '',
                  depth,
                  rect: { top: r.top, bottom: r.bottom, height: r.height },
                  scrollH: el.scrollHeight,
                  clientH: el.clientHeight,
                  overflowY: cs.overflowY,
                  paddingBottom: cs.paddingBottom,
                  paddingTop: cs.paddingTop,
                  marginBottom: cs.marginBottom,
                  boxSizing: cs.boxSizing,
                  scrollsItself: overflowsSelf,
                  bottomBeyondViewport: r.bottom - vp,
                });
              }
              for (const c of el.children) walk(c, depth + 1);
            }
            walk(document.documentElement, 0);
            return {
              vpH: innerHeight,
              docScrollH: document.documentElement.scrollHeight,
              docClientH: document.documentElement.clientHeight,
              bodyScrollH: document.body.scrollHeight,
              bodyClientH: document.body.clientHeight,
              scrollbarReserved:
                window.innerWidth - document.documentElement.clientWidth,
              elements: out,
            };
          }
        """
        )
        print("--- DOCUMENT --------------------------------------------")
        print(f"  viewport innerHeight:   {report['vpH']}")
        print(f"  documentElement.scrollH: {report['docScrollH']}")
        print(f"  documentElement.clientH: {report['docClientH']}")
        print(f"  body.scrollHeight:      {report['bodyScrollH']}")
        print(f"  body.clientHeight:      {report['bodyClientH']}")
        print(
            f"  scrollbar reserved px:  {report['scrollbarReserved']} "
            "(0 = no scrollbar visible)"
        )
        doc_overflow = report["docScrollH"] - report["vpH"]
        print(f"\n  DOCUMENT OVERFLOW: {doc_overflow}px")

        print("\n--- CONTAINERS & OVERFLOW SOURCES ----------------------")
        for e in report["elements"]:
            sig = f"{e['tag']}"
            if e["id"]:
                sig += f"#{e['id']}"
            if e["cls"]:
                sig += f".{e['cls'].split()[0]}"
            indent = "  " * e["depth"]
            line = f"{indent}{sig}"
            line += f"  h={e['rect']['height']:.0f}"
            line += f"  bottom={e['rect']['bottom']:.0f}"
            line += f"  scrollH={e['scrollH']}/clientH={e['clientH']}"
            if e["scrollsItself"]:
                line += f"  !! SCROLLS ({e['scrollH'] - e['clientH']}px)"
            if e["bottomBeyondViewport"] > 0:
                line += f"  !! BEYOND VP +{e['bottomBeyondViewport']:.1f}"
            print(line)

        b.close()


if __name__ == "__main__":
    main()
