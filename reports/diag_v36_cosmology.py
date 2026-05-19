"""v36 — Genesis 1 Cosmology Chamber prototype.

Verifies the chamber opens, renders all five sections, and
visually separates archive synthesis from primary/secondary
material.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.6",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(900)
        page.click("#companion-toggle")
        page.wait_for_timeout(700)
        # Surface tertiary markers so the cosmology-firmament marker is visible
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(500)

        # Open the chamber by record id
        opened = page.evaluate(
            """
          () => {
            if (typeof _openFolioObject !== 'function') return false;
            _openFolioObject('gen1-cosmology-firmament');
            return true;
          }
        """
        )
        assert opened
        page.wait_for_timeout(900)

        state = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.cosmology-chamber');
            if (!leaf) return null;
            return {
              exists: true,
              authority: leaf.dataset.authority,
              hasProvenance: !!leaf.querySelector('.folio-leaf-provenance'),
              hasVerse: !!leaf.querySelector('.folio-leaf-verse'),
              hasTitle: !!leaf.querySelector('.folio-leaf-title'),
              hasLede: !!leaf.querySelector('.cc-lede'),
              sectionHeadings: Array.from(
                leaf.querySelectorAll('.cc-section-heading .cc-section-title')
              ).map(el => el.textContent),
              hasDiagram: !!leaf.querySelector('.cc-diagram-svg'),
              diagramLabels: Array.from(
                leaf.querySelectorAll('.cc-d-label')
              ).map(el => el.textContent.trim()),
              hebrewTerms: Array.from(
                leaf.querySelectorAll('.cc-term-hebrew')
              ).map(el => el.textContent.trim()),
              translitTerms: Array.from(
                leaf.querySelectorAll('.cc-term-translit')
              ).map(el => el.textContent.trim()),
              comparativeTitles: Array.from(
                leaf.querySelectorAll('.cc-comp-title')
              ).map(el => el.textContent.trim()),
              hasArchivePanel: !!leaf.querySelector('.cc-archive'),
              archiveRubric: leaf.querySelector('.cc-archive-rubric')?.textContent.trim(),
              archiveHeading: leaf.querySelector('.cc-archive-heading')?.textContent.trim(),
              archiveBodyLen: (leaf.querySelector('.cc-archive-body')?.textContent || '').length,
              archiveNotePresent: !!leaf.querySelector('.cc-archive-note'),
              archiveBgColor: leaf.querySelector('.cc-archive')
                ? getComputedStyle(leaf.querySelector('.cc-archive')).backgroundColor
                : null,
              archiveBorderLeft: leaf.querySelector('.cc-archive')
                ? getComputedStyle(leaf.querySelector('.cc-archive')).borderLeftColor
                : null,
              hasColophon: !!leaf.querySelector('.folio-leaf-colophon'),
            };
          }
        """
        )
        assert state, "cosmology chamber did not render"
        print("─── Cosmology chamber ───")
        for k, v in state.items():
            print(f"  {k}: {v}")

        assert state['authority'] == 'tertiary'
        assert state['hasProvenance']
        assert state['hasVerse']
        assert state['hasTitle']
        assert state['hasLede']
        assert state['sectionHeadings'] == [
            'Diagram', 'Terminology', 'Comparative Context'
        ], state['sectionHeadings']
        assert state['hasDiagram']
        # Diagram labels include the key Hebrew transliterations
        labels_blob = ' '.join(state['diagramLabels']).lower()
        for key in ('rāqîaʿ', 'tehôm', 'ʾereṣ', 'mayim'):
            assert key.lower() in labels_blob, f"missing label: {key}"
        # Hebrew terms — 5 entries
        assert len(state['hebrewTerms']) == 5
        assert state['translitTerms'] == [
            'tehôm', 'rāqîaʿ', 'shāmayim', 'mayim', 'ʾereṣ'
        ], state['translitTerms']
        # Comparative titles
        assert state['comparativeTitles'] == [
            'Enūma Eliš (Babylon)',
            'Nun and Nut (Egypt)',
            'A note on dependence',
        ], state['comparativeTitles']
        # Archive synthesis panel — clearly differentiated
        assert state['hasArchivePanel']
        assert state['archiveRubric'] == 'Archive Synthesis · Tertiary'
        assert state['archiveHeading'] == 'Archive Commentary'
        assert state['archiveBodyLen'] > 200
        assert state['archiveNotePresent']
        # Background color differs from leaf default (some tinted bg)
        print(f"\n  archive panel bg: {state['archiveBgColor']}")
        print(f"  archive panel border-left: {state['archiveBorderLeft']}")
        # rgba(118, 116, 110, 0.07) — anything not white/transparent
        assert 'rgb' in (state['archiveBgColor'] or '')
        # Verify the archive bg is visibly distinct from page bg
        page_bg = page.evaluate(
            "() => getComputedStyle(document.body).backgroundColor"
        )
        print(f"  body bg for comparison:    {page_bg}")
        assert state['archiveBgColor'] != page_bg, (
            'archive panel bg should differ from page bg'
        )
        print("\nOK — chamber renders all five sections with differentiated archive panel")

        # Capture full-chamber screenshot. Scroll inside the viewer to
        # capture each region individually too.
        page.screenshot(path="reports/v36_cosmology_top.png", full_page=False)
        # Scroll the chamber down to capture lower regions
        page.evaluate(
            """
          () => {
            const v = document.getElementById('object-viewer');
            v.scrollTop = v.scrollHeight / 3;
          }
        """
        )
        page.wait_for_timeout(300)
        page.screenshot(path="reports/v36_cosmology_middle.png")
        page.evaluate(
            """
          () => {
            const v = document.getElementById('object-viewer');
            v.scrollTop = v.scrollHeight;
          }
        """
        )
        page.wait_for_timeout(300)
        page.screenshot(path="reports/v36_cosmology_bottom.png")
        # Full-page screenshot
        page.screenshot(path="reports/v36_cosmology_full.png", full_page=True)

        b.close()
    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
