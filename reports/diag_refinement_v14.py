"""v14 — enlarged Doré plate + multi-witness coverage verification."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # --- WITNESS COVERAGE: Genesis 1, 4, 11 ---
        # Each is opened via direct URL so we can confirm what the
        # rendering pipeline puts in the margin against the data audit.
        chapter_targets = [
            ("gen.1", 1),   # Creation of Light only
            ("gen.4", 2),   # Cain Slays Abel + Cain & Seth genealogy
            ("gen.11", 3),  # Shem to Terah + Terah's house + Confusion of Tongues
        ]
        for chKey, expected in chapter_targets:
            url = f"http://localhost:8765/index.html?text=bible_kjv.json&p={chKey}.1"
            page.goto(url, wait_until="networkidle")
            page.wait_for_function(
                "typeof currentData === 'object' && currentData && currentData.passages",
                timeout=15000,
            )
            page.wait_for_timeout(500)
            # Activate folio
            page.click("#companion-toggle")
            page.wait_for_timeout(400)
            # Count margin witnesses
            count = page.evaluate(
                """
              () => {
                const items = document.querySelectorAll('.cr-margin-witness');
                return Array.from(items).map(el => ({
                  kind: el.dataset.kind,
                  title: el.querySelector('.cr-mw-title')?.textContent || '',
                }));
              }
            """
            )
            print(f"\n{chKey} — found {len(count)} margin witness(es):")
            for w in count:
                print(f"  [{w['kind']}] {w['title']}")
            assert len(count) == expected, (
                f"{chKey} expected {expected} witnesses, got {len(count)}: {count}"
            )

        # --- PLATE SIZE: at 1440×900 ---
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(500)
        page.click("#companion-toggle")
        page.wait_for_timeout(400)
        page.wait_for_selector('.cr-margin-witness[data-kind="plate"]', timeout=5000)
        page.click('.cr-margin-witness[data-kind="plate"]')
        page.wait_for_timeout(700)

        plate_info = page.evaluate(
            """
          () => {
            const img = document.querySelector('.folio-plate');
            const plaque = document.querySelector('.folio-plate-plaque');
            const wrap = document.querySelector('.folio-plate-wrap');
            return {
              imgWidth: img.getBoundingClientRect().width,
              imgHeight: img.getBoundingClientRect().height,
              wrapWidth: wrap.getBoundingClientRect().width,
              plaqueBottom: plaque.getBoundingClientRect().bottom,
              vp: innerHeight,
              docOverflow: document.documentElement.scrollHeight - innerHeight,
            };
          }
        """
        )
        print(f"\nPLATE GEOMETRY (1440×900):")
        print(f"  image: {plate_info['imgWidth']:.0f} × {plate_info['imgHeight']:.0f}")
        print(f"  image height / vp = {plate_info['imgHeight'] / plate_info['vp']:.0%}")
        print(f"  wrap width:    {plate_info['wrapWidth']:.0f}")
        print(f"  plaque bottom: {plate_info['plaqueBottom']:.0f} (vp {plate_info['vp']})")
        print(f"  doc overflow:  {plate_info['docOverflow']}")

        assert plate_info["imgHeight"] / plate_info["vp"] >= 0.80, (
            f"Image not large enough: {plate_info['imgHeight']:.0f}/{plate_info['vp']}"
        )
        assert plate_info["plaqueBottom"] <= plate_info["vp"] + 1, (
            f"Plaque below viewport: {plate_info['plaqueBottom']}"
        )
        assert plate_info["docOverflow"] == 0, (
            f"Document scroll appeared: {plate_info['docOverflow']}"
        )

        # --- Click handlers still correct ---
        # On-object (image center) — stays open
        cx = plate_info["wrapWidth"] / 2 + page.evaluate(
            "() => document.querySelector('.folio-plate-wrap').getBoundingClientRect().left"
        )
        cy = page.evaluate(
            "() => { const r = document.querySelector('.folio-plate').getBoundingClientRect(); return (r.top + r.bottom) / 2; }"
        )
        page.mouse.click(int(cx), int(cy))
        page.wait_for_timeout(250)
        assert page.evaluate("() => document.body.classList.contains('viewer-active')"), \
            "Click on image wrongly closed"
        # Outside (dimmed area to left) — closes
        page.mouse.click(150, 450)
        page.wait_for_timeout(500)
        assert not page.evaluate("() => document.body.classList.contains('viewer-active')"), \
            "Click outside did not close"
        print("\nclick on image: stays open ✓")
        print("click outside:  closes ✓")

        page.screenshot(path="reports/v14_plate_enlarged.png")

        # Re-open and capture
        page.click('.cr-margin-witness[data-kind="plate"]')
        page.wait_for_timeout(500)
        page.screenshot(path="reports/v14_plate_opened.png")

        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
