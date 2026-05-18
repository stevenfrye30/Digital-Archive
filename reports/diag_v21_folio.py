"""v21 — folio mode-gating + visibility diagnostic.

Reports the exact state per the user's required scenarios:
  A. Initial mode state on entering reading room
  B. After Folio toggle in SINGLE mode
  C. After switching to WIDE mode
  D. After returning to SINGLE mode
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright


def probe(page, label):
    return page.evaluate(
        """
      () => {
        const folio = document.getElementById('folio');
        const fcs = getComputedStyle(folio);
        const tog = document.getElementById('companion-toggle');
        const swap = document.getElementById('companion-swap');
        const togCS = getComputedStyle(tog);
        const swapCS = getComputedStyle(swap);
        const passage = document.querySelector('.cr-row > :first-child');
        const fr = folio.getBoundingClientRect();
        const pr = passage?.getBoundingClientRect();
        const sharedArea = pr
          ? Math.max(0, Math.min(fr.right, pr.right) - Math.max(fr.left, pr.left)) *
            Math.max(0, Math.min(fr.bottom, pr.bottom) - Math.max(fr.top, pr.top))
          : null;
        const entries = Array.from(document.querySelectorAll('.cr-folio-entry'));
        return {
          bodyClasses: Array.from(document.body.classList),
          colsSingle: document.body.classList.contains('cols-single'),
          colsWide: document.body.classList.contains('cols-wide'),
          companionMode: document.body.classList.contains('companion-mode'),
          folioLeft: document.body.classList.contains('folio-left'),
          folio: {
            display: fcs.display,
            visibility: fcs.visibility,
            opacity: fcs.opacity,
            zIndex: fcs.zIndex,
            left: fcs.left,
            right: fcs.right,
            maxWidth: fcs.maxWidth,
            backgroundImage: fcs.backgroundImage.slice(0, 100),
            rect: fr.toJSON(),
            innerChildCount: folio.querySelector('#folio-inner')?.children.length || 0,
          },
          companionToggle: {
            text: tog.textContent.trim(),
            opacity: togCS.opacity,
            pointerEvents: togCS.pointerEvents,
            ariaPressed: tog.getAttribute('aria-pressed'),
          },
          companionSwap: {
            text: swap.textContent.trim(),
            opacity: swapCS.opacity,
            pointerEvents: swapCS.pointerEvents,
          },
          entryCount: entries.length,
          firstEntry: entries[0]?.querySelector('.cr-folio-title')?.textContent,
          allEntries: entries.map(e => e.querySelector('.cr-folio-title')?.textContent),
          passageRect: pr?.toJSON() || null,
          sharedArea,
        };
      }
        """
    )


def print_state(label, s):
    print(f"\n┌── {label} " + "─" * (60 - len(label)))
    print(f"│ body: {' '.join(c for c in s['bodyClasses'] if c not in ('reading-compact', 'in-reading'))}")
    print(f"│ scripture: {s['passageRect']['left']:.0f}..{s['passageRect']['right']:.0f} (w={s['passageRect']['width']:.0f})")
    print(f"│ folio: display={s['folio']['display']:<8} rect={s['folio']['rect']['left']:.0f}..{s['folio']['rect']['right']:.0f} (w={s['folio']['rect']['width']:.0f})")
    print(f"│ folio entries: {s['entryCount']}  first: {s['firstEntry']}")
    print(f"│ companion-toggle: text='{s['companionToggle']['text']}' opacity={s['companionToggle']['opacity']} pe={s['companionToggle']['pointerEvents']}")
    print(f"│ companion-swap:   text='{s['companionSwap']['text']}' opacity={s['companionSwap']['opacity']} pe={s['companionSwap']['pointerEvents']}")
    print(f"│ shared area scripture×folio: {s['sharedArea']:.1f} px²")
    print("└" + "─" * 65)


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # Enter Genesis 1 reading room
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(700)

        # ── A. Initial state: single, no folio
        a = probe(page, "A. Initial single, folio off")
        print_state("A. Initial single, folio off", a)
        assert a["colsSingle"], "Expected cols-single at startup"
        assert not a["companionMode"]
        assert a["folio"]["display"] == "none"
        # Buttons enabled
        assert a["companionToggle"]["pointerEvents"] != "none"

        # ── B. Click Folio (toggle on) in single mode
        page.click("#companion-toggle")
        page.wait_for_timeout(600)
        b_state = probe(page, "B. single + folio on (right)")
        print_state("B. single + folio on (right)", b_state)
        assert b_state["companionMode"]
        assert b_state["folio"]["display"] == "block"
        assert b_state["folio"]["rect"]["width"] >= 200
        assert b_state["entryCount"] == 1
        assert b_state["firstEntry"] == "The Creation of Light"
        assert b_state["sharedArea"] == 0, f"Folio overlaps scripture: {b_state['sharedArea']}"
        page.screenshot(path="reports/v21_single_folio_right.png")

        # ── B'. Click Folio side
        page.click("#companion-swap")
        page.wait_for_timeout(600)
        bp = probe(page, "B'. single + folio on (left)")
        print_state("B'. single + folio on (left)", bp)
        assert bp["folioLeft"]
        assert bp["folio"]["display"] == "block"
        assert bp["sharedArea"] == 0
        page.screenshot(path="reports/v21_single_folio_left.png")

        # ── C. Switch to WIDE mode
        page.click("#ctrl-columns .col-opt[data-cols='wide']")
        page.wait_for_timeout(600)
        c = probe(page, "C. wide — folio hidden, controls disabled")
        print_state("C. wide — folio hidden, controls disabled", c)
        assert c["colsWide"]
        assert c["folio"]["display"] == "none", "Folio must be hidden in wide mode"
        assert c["companionToggle"]["pointerEvents"] == "none", (
            "Folio toggle must be disabled in wide mode"
        )
        assert c["companionSwap"]["pointerEvents"] == "none", (
            "Folio side must be disabled in wide mode"
        )
        assert float(c["companionToggle"]["opacity"]) < 0.5
        page.screenshot(path="reports/v21_wide_folio_disabled.png")

        # ── D. Switch back to SINGLE mode
        page.click("#ctrl-columns .col-opt[data-cols='single']")
        page.wait_for_timeout(600)
        d = probe(page, "D. back to single — folio reactivated (state preserved)")
        print_state("D. back to single — folio reactivated", d)
        assert d["colsSingle"]
        # companion-mode survived the round-trip
        assert d["companionMode"]
        assert d["folio"]["display"] == "block"
        assert d["entryCount"] >= 1
        assert d["companionToggle"]["pointerEvents"] != "none"
        page.screenshot(path="reports/v21_single_again_visible.png")

        # ── Scripture invariance check across all single-mode states
        rects = [b_state, bp, d]
        print("\n=== Scripture rect invariance across single-mode folio states ===")
        for s in rects:
            pr = s["passageRect"]
            print(f"  left={pr['left']:.0f} right={pr['right']:.0f} width={pr['width']:.0f}")
        # All should be the same
        lefts = [s["passageRect"]["left"] for s in rects]
        rights = [s["passageRect"]["right"] for s in rects]
        widths = [s["passageRect"]["width"] for s in rects]
        assert max(lefts) - min(lefts) <= 0.5
        assert max(rights) - min(rights) <= 0.5
        assert max(widths) - min(widths) <= 0.5

        # ── Multi-witness sanity check
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.11.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(700)
        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        g11 = probe(page, "Genesis 11")
        print(f"\nGenesis 11 entries: {g11['entryCount']} → {g11['allEntries']}")
        assert g11["entryCount"] == 3

        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
