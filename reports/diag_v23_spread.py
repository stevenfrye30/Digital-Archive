"""v23 — shared-scroll chapter spread verification."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


def probe(page, label):
    return page.evaluate(
        """
      () => {
        const spread = document.querySelector('#passages .chapter-spread');
        const scrCol = spread?.querySelector('.scripture-column');
        const folCol = spread?.querySelector('.folio-column');
        const entries = Array.from(document.querySelectorAll('.cr-folio-entry'));
        const folCS = folCol ? getComputedStyle(folCol) : null;
        const passage = document.querySelector('.scripture-column .cr-row > :first-child') ||
                        document.querySelector('.cr-row > :first-child');
        return {
          bodyClasses: Array.from(document.body.classList),
          viewport: { w: innerWidth, h: innerHeight },
          spread: spread ? spread.getBoundingClientRect().toJSON() : null,
          scriptureColumn: scrCol ? scrCol.getBoundingClientRect().toJSON() : null,
          folioColumn: folCS && folCS.display !== 'none'
            ? folCol.getBoundingClientRect().toJSON() : null,
          folioDisplay: folCS?.display,
          passage: passage?.getBoundingClientRect().toJSON(),
          entryCount: entries.length,
          entries: entries.map(e => ({
            title: e.querySelector('.cr-folio-title')?.textContent,
            anchorPid: e.dataset.anchorPid,
            top: e.style.top,
            rect: e.getBoundingClientRect().toJSON(),
          })),
          // Find anchor verses for entries
          anchorVerses: entries.map(e => {
            const pid = e.dataset.anchorPid;
            if (!pid) return null;
            const v = document.querySelector(`.scripture-column [data-pid="${pid}"]`);
            return v ? {
              pid,
              rect: v.getBoundingClientRect().toJSON(),
              offsetTop: v.offsetTop,
            } : null;
          }).filter(Boolean),
        };
      }
        """
    )


def show(label, s):
    print(f"\n── {label} " + "─" * (60 - len(label)))
    print(f"  body: {' '.join(c for c in s['bodyClasses'] if not c.startswith(('reading-','in-')))}")
    if s["spread"]:
        sp = s["spread"]
        print(f"  spread: L={sp['left']:.0f} R={sp['right']:.0f} W={sp['width']:.0f}")
    if s["scriptureColumn"]:
        sc = s["scriptureColumn"]
        print(f"  scripture col: L={sc['left']:.0f} R={sc['right']:.0f} W={sc['width']:.0f}")
    if s["passage"]:
        p = s["passage"]
        print(f"  v1 passage:    L={p['left']:.0f} R={p['right']:.0f} W={p['width']:.0f}")
    if s["folioColumn"]:
        f = s["folioColumn"]
        print(f"  folio column:  L={f['left']:.0f} R={f['right']:.0f} W={f['width']:.0f}")
    else:
        print(f"  folio column:  (hidden)")
    print(f"  folio entries: {s['entryCount']}")
    for e, v in zip(s["entries"], s["anchorVerses"]):
        delta = e["rect"]["top"] - v["rect"]["top"] if v else None
        print(f"    - {e['title'][:40]}")
        print(f"        anchor {e['anchorPid']} verse.top={v['rect']['top']:.0f}  entry.top={e['rect']['top']:.0f}  Δ={delta:+.0f}px")


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        def goto_chapter(ch):
            page.goto(
                f"http://localhost:8765/index.html?text=bible_kjv.json&p={ch}.1",
                wait_until="networkidle",
            )
            page.wait_for_function(
                "typeof currentData === 'object' && currentData && currentData.passages",
                timeout=15000,
            )
            page.wait_for_timeout(800)

        # ── Genesis 1 folio right ────────────────────────────────
        goto_chapter("gen.1")
        page.click("#companion-toggle")
        page.wait_for_timeout(800)
        right1 = probe(page, "Gen 1 — folio right")
        show("GEN 1, folio right", right1)
        page.screenshot(path="reports/v23_gen1_right.png")

        # Swap to left
        page.click("#companion-swap")
        page.wait_for_timeout(800)
        left1 = probe(page, "Gen 1 — folio left")
        show("GEN 1, folio left", left1)
        page.screenshot(path="reports/v23_gen1_left.png")

        # ── Genesis 4 ────────────────────────────────────────────
        goto_chapter("gen.4")
        page.click("#companion-toggle")
        page.wait_for_timeout(800)
        g4 = probe(page, "Gen 4")
        show("GEN 4 — 2 witnesses", g4)
        page.screenshot(path="reports/v23_gen4.png")

        # ── Genesis 11 ───────────────────────────────────────────
        goto_chapter("gen.11")
        page.click("#companion-toggle")
        page.wait_for_timeout(800)
        g11 = probe(page, "Gen 11")
        show("GEN 11 — 3 witnesses", g11)
        page.screenshot(path="reports/v23_gen11.png")

        # ── Wide mode ────────────────────────────────────────────
        page.click("#ctrl-columns .col-opt[data-cols='wide']")
        page.wait_for_timeout(500)
        wide = probe(page, "Wide")
        show("WIDE", wide)
        page.screenshot(path="reports/v23_wide.png")

        # ── Scroll test: scroll reader, folio should move with scripture
        page.click("#ctrl-columns .col-opt[data-cols='single']")
        page.wait_for_timeout(500)
        goto_chapter("gen.11")
        page.click("#companion-toggle")
        page.wait_for_timeout(800)
        before_scroll = probe(page, "before scroll")
        if before_scroll["entries"]:
            before_entry_top = before_scroll["entries"][0]["rect"]["top"]
            before_verse_top = before_scroll["anchorVerses"][0]["rect"]["top"]
        page.evaluate("document.getElementById('reader').scrollTop = 600")
        page.wait_for_timeout(500)
        after_scroll = probe(page, "after scroll 600px")
        if after_scroll["entries"]:
            after_entry_top = after_scroll["entries"][0]["rect"]["top"]
            after_verse_top = after_scroll["anchorVerses"][0]["rect"]["top"]
            entry_delta = after_entry_top - before_entry_top
            verse_delta = after_verse_top - before_verse_top
            print(f"\nSCROLL TEST:")
            print(f"  scroll 0 → 600px")
            print(f"  first entry moved by:  {entry_delta:+.0f}px")
            print(f"  first verse moved by:  {verse_delta:+.0f}px")
            assert abs(entry_delta - verse_delta) <= 1, (
                "Folio entry did not scroll with scripture verse"
            )
        page.screenshot(path="reports/v23_scrolled.png")

        # ── Assertions
        # Gen 1: 1 entry, near anchor verse
        assert right1["entryCount"] == 1
        assert right1["entries"][0]["title"] == "The Creation of Light"
        e = right1["entries"][0]
        v = right1["anchorVerses"][0]
        assert abs(e["rect"]["top"] - v["rect"]["top"]) <= 30, (
            f"Folio entry not near anchor verse (Δ={e['rect']['top']-v['rect']['top']})"
        )

        # Gen 4: 2 entries
        assert g4["entryCount"] == 2

        # Gen 11: 3 entries
        assert g11["entryCount"] == 3

        # Wide: no folio column
        assert wide["folioColumn"] is None

        # Scripture positions
        # Folio right at 1440 viewport: scripture should be at viewport's left half
        # Folio left at 1440 viewport: scripture should be at viewport's right half
        # In all cases, scripture width should be 960
        for s in [right1, left1, g4, g11]:
            assert abs(s["scriptureColumn"]["width"] - 960) <= 0.5, (
                f"Scripture column not 960: {s['scriptureColumn']['width']}"
            )

        # Wide centered
        wide_lm = wide["scriptureColumn"]["left"]
        wide_rm = wide["viewport"]["w"] - wide["scriptureColumn"]["right"]
        assert abs(wide_lm - wide_rm) <= 1, f"Wide not centered: L={wide_lm} R={wide_rm}"

        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
