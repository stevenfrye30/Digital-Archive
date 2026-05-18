"""v24 — test folio across viewport sizes the user might be using."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


def test_viewport(p, width, height):
    ctx = p.new_context(viewport={"width": width, "height": height})
    page = ctx.new_page()
    page.goto(
        "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.4.1",
        wait_until="networkidle",
    )
    page.wait_for_function(
        "typeof currentData === 'object' && currentData && currentData.passages",
        timeout=15000,
    )
    page.wait_for_timeout(700)
    # Toggle folio
    page.click("#companion-toggle")
    page.wait_for_timeout(700)
    state = page.evaluate(
        """
      () => {
        const spread = document.querySelector('#passages .chapter-spread');
        const sc = spread?.querySelector('.scripture-column');
        const fc = spread?.querySelector('.folio-column');
        const fcCS = fc ? getComputedStyle(fc) : null;
        const tog = document.getElementById('companion-toggle');
        const togCS = getComputedStyle(tog);
        return {
          spreadDisplay: spread ? getComputedStyle(spread).display : 'no-spread',
          spreadWidth: spread?.getBoundingClientRect().width,
          scriptureWidth: sc?.getBoundingClientRect().width,
          folioDisplay: fcCS?.display,
          folioWidth: fc?.getBoundingClientRect().width,
          companionMode: document.body.classList.contains('companion-mode'),
          colsSingle: document.body.classList.contains('cols-single'),
          toggleOpacity: togCS.opacity,
          togglePE: togCS.pointerEvents,
          entryCount: document.querySelectorAll('.cr-folio-entry').length,
          firstEntryTitle: document.querySelector('.cr-folio-title')?.textContent,
        };
      }
        """
    )
    ctx.close()
    return state


def main():
    test_widths = [
        ("Standard 1440×900", 1440, 900),
        ("Effective 1423 (1440 with scrollbar)", 1423, 900),
        ("1420 — just above collapse threshold", 1420, 900),
        ("1410 — exactly at collapse threshold", 1410, 900),
        ("1400 — below threshold", 1400, 900),
        ("1366 — common laptop", 1366, 768),
        ("1280 — narrower laptop", 1280, 800),
    ]
    with sync_playwright() as p:
        b = p.chromium.launch()
        for label, w, h in test_widths:
            print(f"\n── {label} ({w}×{h}) " + "─" * (45 - len(label)))
            try:
                state = test_viewport(b, w, h)
                fd = state['folioDisplay'] or 'none'
                print(f"  spread.display:      {state['spreadDisplay']}")
                print(f"  scripture width:     {state['scriptureWidth']}")
                print(f"  folio.display:       {fd}")
                print(f"  folio.width:         {state['folioWidth']}")
                print(f"  companion-mode:      {state['companionMode']}")
                print(f"  cols-single:         {state['colsSingle']}")
                print(f"  toggle.opacity/pe:   {state['toggleOpacity']} / {state['togglePE']}")
                print(f"  folio entries:       {state['entryCount']}")
                print(f"  first entry:         {state['firstEntryTitle']}")
            except Exception as e:
                print(f"  ERROR: {e}")
        b.close()


if __name__ == "__main__":
    main()
