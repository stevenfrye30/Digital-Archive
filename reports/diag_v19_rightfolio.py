"""Capture folio-RIGHT state to verify visibility."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(
        "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
        wait_until="networkidle",
    )
    page.wait_for_function(
        "typeof currentData === 'object' && currentData && currentData.passages",
        timeout=15000,
    )
    page.wait_for_timeout(700)
    page.click("#companion-toggle")
    page.wait_for_timeout(700)
    page.screenshot(path="reports/v19_folio_right.png")

    # Also test clicking only the "Folio side" swap from a clean state
    page.goto(
        "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
        wait_until="networkidle",
    )
    page.wait_for_timeout(700)
    page.click("#companion-swap")
    page.wait_for_timeout(700)
    page.screenshot(path="reports/v19_after_swap_only.png")
    cls = page.evaluate("() => Array.from(document.body.classList)")
    print("After clicking only 'Folio side':", cls)
    folio = page.evaluate(
        "() => { const f = document.getElementById('folio'); const cs = getComputedStyle(f); return { display: cs.display, rect: f.getBoundingClientRect().toJSON() }; }"
    )
    print("Folio state:", folio)

    b.close()
