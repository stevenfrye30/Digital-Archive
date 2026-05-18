"""v24 — exhaustive folio pipeline tracer.

Hooks every stage of the folio render with console.log and
reports the trace + DOM state at each step.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


INSTRUMENT_JS = """
() => {
  window.__FOLIO_TRACE__ = [];
  function trace(...args) {
    const msg = args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ');
    window.__FOLIO_TRACE__.push(msg);
    console.log('[FOLIO]', msg);
  }
  window.__trace = trace;

  // Wrap key functions
  const origRender = window.render;
  if (origRender) {
    window.render = function(passages, query) {
      trace('render() called with', passages.length, 'passages');
      const r = origRender.apply(this, arguments);
      const spread = document.querySelector('#passages .chapter-spread');
      trace('after render: chapter-spread =', !!spread);
      if (spread) {
        const sc = spread.querySelector('.scripture-column');
        const fc = spread.querySelector('.folio-column');
        trace('  scripture-column =', !!sc, '  folio-column =', !!fc);
      }
      return r;
    };
  } else {
    trace('NO window.render at instrument time');
  }

  const origRCF = window.renderCompanionFolio;
  if (origRCF) {
    window.renderCompanionFolio = function() {
      trace('renderCompanionFolio() entered, body.companion-mode =',
        document.body.classList.contains('companion-mode'));
      const r = origRCF.apply(this, arguments);
      const fc = document.querySelector('#passages .chapter-spread .folio-column');
      const entries = document.querySelectorAll('.cr-folio-entry');
      trace('  after RCF: folio-column =', !!fc, ' entries =', entries.length);
      return r;
    };
  } else {
    trace('NO window.renderCompanionFolio at instrument time');
  }

  const origRCRF = window._renderChapterRoomFolio;
  if (origRCRF) {
    window._renderChapterRoomFolio = function() {
      trace('_renderChapterRoomFolio() entered');
      trace('  chapter-room =', document.body.classList.contains('chapter-room'));
      trace('  companion-mode =', document.body.classList.contains('companion-mode'));
      const fc = document.querySelector('#passages .chapter-spread .folio-column');
      trace('  folio-column query =', !!fc);
      if (fc) trace('  folio-column innerHTML.length =', fc.innerHTML.length);
      const r = origRCRF.apply(this, arguments);
      const entries = document.querySelectorAll('.cr-folio-entry');
      trace('  after _RCRF: entries in DOM =', entries.length);
      return r;
    };
  } else {
    trace('NO window._renderChapterRoomFolio at instrument time');
  }

  const origPos = window._positionFolioEntries;
  if (origPos) {
    window._positionFolioEntries = function() {
      const entries = document.querySelectorAll('.cr-folio-entry');
      trace('_positionFolioEntries() entered, entries =', entries.length);
      const r = origPos.apply(this, arguments);
      const positioned = Array.from(entries).map(e => e.style.top || '(none)');
      trace('  positions:', positioned.join(','));
      return r;
    };
  }
}
"""


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        # Listen to console messages
        console_msgs = []
        page.on("console", lambda m: console_msgs.append(f"[{m.type}] {m.text}"))

        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(500)
        # Instrument NOW (after functions are defined)
        page.evaluate(INSTRUMENT_JS)

        # Force a re-render
        page.evaluate("filterAndRender()")
        page.wait_for_timeout(300)

        print("─── after initial filterAndRender (NO folio) ───")
        trace = page.evaluate("() => window.__FOLIO_TRACE__")
        for t in trace:
            print(f"  {t}")

        # Now toggle folio
        print("\n─── clicking companion-toggle ───")
        page.evaluate("window.__FOLIO_TRACE__ = []")
        page.click("#companion-toggle")
        page.wait_for_timeout(700)

        trace = page.evaluate("() => window.__FOLIO_TRACE__")
        for t in trace:
            print(f"  {t}")

        # DOM state
        dom = page.evaluate(
            """
          () => {
            const spread = document.querySelector('#passages .chapter-spread');
            const fc = spread?.querySelector('.folio-column');
            const fcCS = fc ? getComputedStyle(fc) : null;
            return {
              bodyClasses: Array.from(document.body.classList),
              spreadExists: !!spread,
              folioColumnExists: !!fc,
              folioColumnDisplay: fcCS?.display,
              folioColumnHTML: fc?.innerHTML.slice(0, 300),
              folioEntryCount: document.querySelectorAll('.cr-folio-entry').length,
            };
          }
        """
        )
        print("\n─── DOM state after toggle ───")
        for k, v in dom.items():
            print(f"  {k}: {v}")

        # Navigate to another chapter while companion-mode is on
        print("\n─── navigating to Gen 4 (currentBook = gen.1 → gen.4) ───")
        page.evaluate("window.__FOLIO_TRACE__ = []")
        page.evaluate("currentBook = 'gen.4'; filterAndRender();")
        page.wait_for_timeout(700)
        trace = page.evaluate("() => window.__FOLIO_TRACE__")
        for t in trace:
            print(f"  {t}")
        dom2 = page.evaluate(
            """
          () => ({
            entries: document.querySelectorAll('.cr-folio-entry').length,
            titles: Array.from(document.querySelectorAll('.cr-folio-title')).map(e => e.textContent),
          })
        """
        )
        print(f"  → entries: {dom2['entries']}  titles: {dom2['titles']}")

        b.close()


if __name__ == "__main__":
    main()
