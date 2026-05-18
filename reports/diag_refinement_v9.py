"""v9 — canon labels strengthened. Capture screenshot."""
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

        info = page.evaluate(
            """
          () => {
            const labels = Array.from(document.querySelectorAll('.bcl-canon-label'));
            return {
              docOverflow: document.documentElement.scrollHeight - innerHeight,
              labels: labels.map(l => ({
                text: l.textContent,
                fontSize: getComputedStyle(l).fontSize,
                color: getComputedStyle(l).color,
                opacity: getComputedStyle(l).opacity,
                letterSpacing: getComputedStyle(l).letterSpacing,
              })),
            };
          }
        """
        )
        print("LABELS:")
        for L in info["labels"]:
            print(f"  {L['text']}")
            print(f"    fontSize={L['fontSize']}  color={L['color']}  opacity={L['opacity']}")
        print(f"\ndocument overflow: {info['docOverflow']}px")

        assert info["docOverflow"] == 0

        page.screenshot(path="reports/v9_titleleaf.png")

        # Close-up of one canon label region
        sec = page.locator('.bcl-canon-section[data-canon="old-testament"]')
        sec.screenshot(path="reports/v9_label_ot.png")
        sec_a = page.locator('.bcl-canon-section[data-canon="apocrypha"]')
        sec_a.screenshot(path="reports/v9_label_apoc.png")
        sec_n = page.locator('.bcl-canon-section[data-canon="new-testament"]')
        sec_n.screenshot(path="reports/v9_label_nt.png")

        b.close()
    print("ALL PASSED")


if __name__ == "__main__":
    main()
