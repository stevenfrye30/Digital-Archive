import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(
        "http://localhost:8765/index.html?text=bible_kjv.json",
        wait_until="networkidle",
    )
    page.wait_for_selector(".bible-cover-layout", timeout=10000)
    page.wait_for_timeout(500)
    page.click(".cite-corner > summary")
    page.wait_for_timeout(400)
    page.screenshot(path="reports/v19_cite_panel_fixed.png")
    b.close()
