"""Diagnose: what's the actual click-target geometry inside the viewer?"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
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
        page.click(".bcl-enter-btn")
        page.wait_for_timeout(500)
        page.click("#companion-toggle")
        page.wait_for_timeout(400)
        page.wait_for_selector('.cr-margin-witness[data-kind="plate"]', timeout=5000)
        page.click('.cr-margin-witness[data-kind="plate"]')
        page.wait_for_timeout(700)

        info = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf[data-kind="plate"]');
            const wrap = document.querySelector('.folio-plate-wrap');
            const img = document.querySelector('.folio-plate');
            const plaque = document.querySelector('.folio-plate-plaque');
            const viewer = document.getElementById('object-viewer');
            const inner = document.getElementById('viewer-inner');
            function probe(x, y) {
              const el = document.elementFromPoint(x, y);
              if (!el) return null;
              const path = [];
              let n = el;
              while (n && n !== document.body) {
                path.push(n.tagName + (n.id ? '#' + n.id : '') + (n.className ? '.' + (typeof n.className === 'string' ? n.className.split(' ')[0] : '') : ''));
                n = n.parentElement;
              }
              return { x, y, path };
            }
            return {
              viewer: viewer.getBoundingClientRect().toJSON(),
              inner: inner.getBoundingClientRect().toJSON(),
              leaf: leaf.getBoundingClientRect().toJSON(),
              wrap: wrap.getBoundingClientRect().toJSON(),
              img: img.getBoundingClientRect().toJSON(),
              plaque: plaque.getBoundingClientRect().toJSON(),
              probe_left_middle: probe(150, 450),
              probe_right_middle: probe(1290, 450),
              probe_far_corner: probe(50, 50),
              probe_below_image: probe(720, 850),
            };
          }
        """
        )
        import json
        print(json.dumps(info, indent=2))
        b.close()

if __name__ == "__main__":
    main()
