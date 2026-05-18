"""Print reader's full child tree with rendered heights, to find
what's filling the column when only bible-cover-layout should be."""
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

        tree = page.evaluate(
            """
          () => {
            const out = [];
            function walk(el, depth) {
              if (depth > 4) return;
              const cs = getComputedStyle(el);
              const r = el.getBoundingClientRect();
              out.push({
                tag: el.tagName.toLowerCase(),
                id: el.id || '',
                cls: el.className?.toString?.().slice(0, 40) || '',
                depth,
                display: cs.display,
                position: cs.position,
                top: r.top,
                bottom: r.bottom,
                height: r.height,
                offsetH: el.offsetHeight,
              });
              for (const c of el.children) walk(c, depth + 1);
            }
            walk(document.getElementById('reader'), 0);
            const inner = document.getElementById('reader-inner');
            return {
              tree: out,
              readerInnerOffsetH: inner.offsetHeight,
              readerInnerScrollH: inner.scrollHeight,
              readerClientH: document.getElementById('reader').clientHeight,
              readerScrollH: document.getElementById('reader').scrollHeight,
            };
          }
        """
        )
        print(f"reader.clientHeight: {tree['readerClientH']}")
        print(f"reader.scrollHeight: {tree['readerScrollH']}")
        print(f"reader-inner.offsetHeight: {tree['readerInnerOffsetH']}")
        print(f"reader-inner.scrollHeight: {tree['readerInnerScrollH']}")
        print()
        for e in tree["tree"]:
            sig = e["tag"]
            if e["id"]:
                sig += f"#{e['id']}"
            if e["cls"]:
                sig += "." + e["cls"].split()[0]
            indent = "  " * e["depth"]
            marker = "" if e["display"] != "none" else " (hidden)"
            print(
                f"{indent}{sig:<40} disp={e['display']:<10} pos={e['position']:<8} "
                f"top={e['top']:6.1f} bot={e['bottom']:6.1f} h={e['height']:6.1f} "
                f"offsetH={e['offsetH']:4}{marker}"
            )
        b.close()


if __name__ == "__main__":
    main()
