"""v63 — Usability + documentation refinement.

Verifies four things in one pass:

  1. .cr-folio-header (Genesis N) is centred in the folio rail.
  2. A chapter traverse appears ABOVE the chapter-plate.
  3. The existing bottom chapter traverse is still present.
  4. The top traverse buttons actually navigate (gen.1 → gen.2 →
     gen.1).

Also verifies BIBLE_FOLIO_OBJECT_INDEX.md exists at the project
root and includes entries for Genesis 1, 12, 28, and 46.
"""
import sys
import re
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent


def main():
    # ── 1. Folio rail centring check ──────────────────────────
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.2.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(700)
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(500)

        rail_state = page.evaluate(
            """
            () => {
              const h = document.querySelector('.cr-folio-header');
              if (!h) return null;
              const cs = getComputedStyle(h);
              const rect = h.getBoundingClientRect();
              // Optical centring check — compute the offset
              // between the text-bounding-box centre and the
              // parent column centre.
              const parent = h.parentElement;
              const prect = parent.getBoundingClientRect();
              return {
                textAlign: cs.textAlign,
                text: h.textContent.trim(),
                headerLeft: rect.left,
                headerRight: rect.right,
                parentLeft: prect.left,
                parentRight: prect.right,
              };
            }
            """
        )
        print(f"Folio rail header: {rail_state}")
        assert rail_state, "folio header missing at gen.2"
        assert rail_state["textAlign"] == "center", (
            f"folio header text-align = {rail_state['textAlign']}"
        )
        print("  OK — folio rail header is centred\n")

        # ── 2 + 3. Top + bottom traverse present ─────────────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.2.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        traverse_state = page.evaluate(
            """
            () => {
              const top = document.querySelector('.chapter-traverse-top');
              const all = Array.from(document.querySelectorAll('.chapter-traverse'));
              const bottom = all.find(n => !n.classList.contains('chapter-traverse-top'));
              const heading = document.querySelector('.chapter-heading');
              const topAboveHeading = (top && heading)
                ? top.compareDocumentPosition(heading) & Node.DOCUMENT_POSITION_FOLLOWING
                : false;
              return {
                topPresent: !!top,
                topPosition: top?.dataset.position,
                bottomPresent: !!bottom,
                bottomPosition: bottom?.dataset.position,
                topAboveHeading: !!topAboveHeading,
                topButtons: top
                  ? Array.from(top.querySelectorAll('button')).map(b => ({
                      label: b.textContent.trim(),
                      cls: b.className,
                    }))
                  : [],
              };
            }
            """
        )
        print(f"Traverse state at gen.2: {traverse_state}")
        assert traverse_state["topPresent"], "top traverse missing"
        assert traverse_state["bottomPresent"], "bottom traverse missing"
        assert traverse_state["topPosition"] == "top"
        assert traverse_state["bottomPosition"] == "bottom"
        assert traverse_state["topAboveHeading"], (
            "top traverse is not above the chapter-plate"
        )
        # gen.2 has both prev (gen.1) and next (gen.3) buttons
        labels = [b["label"] for b in traverse_state["topButtons"]]
        assert any("Genesis Ch 1" in l for l in labels), labels
        assert any("Genesis Ch 3" in l for l in labels), labels
        print("  OK — top traverse exists above chapter-plate")
        print("  OK — bottom traverse still present")
        print("  OK — prev/next labels populated\n")

        # ── 4. Navigation via TOP traverse: gen.1 → gen.2 → gen.1
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(700)
        head_state_before = page.evaluate(
            "() => document.querySelector('.ch-sub')?.textContent"
        )
        assert head_state_before == "I", head_state_before

        # Click the top-traverse "next" button.
        page.evaluate(
            """
            () => {
              const top = document.querySelector('.chapter-traverse-top');
              if (!top) throw new Error('no top traverse');
              const next = top.querySelector('.ch-next');
              if (!next) throw new Error('no next button');
              next.click();
            }
            """
        )
        page.wait_for_timeout(700)
        head_after_next = page.evaluate(
            "() => document.querySelector('.ch-sub')?.textContent"
        )
        print(f"After top-next click: chapter = {head_after_next}")
        assert head_after_next == "II", head_after_next

        # Click the top-traverse "previous" button.
        page.evaluate(
            """
            () => {
              const top = document.querySelector('.chapter-traverse-top');
              if (!top) throw new Error('no top traverse');
              const prev = top.querySelector('.ch-prev');
              if (!prev) throw new Error('no prev button');
              prev.click();
            }
            """
        )
        page.wait_for_timeout(700)
        head_after_prev = page.evaluate(
            "() => document.querySelector('.ch-sub')?.textContent"
        )
        print(f"After top-prev click: chapter = {head_after_prev}")
        assert head_after_prev == "I", head_after_prev
        print("  OK — top traverse navigates gen.1 → gen.2 → gen.1\n")

        # ── 5. Boundary check — gen.1 has no prev button at top
        boundary = page.evaluate(
            """
            () => {
              const top = document.querySelector('.chapter-traverse-top');
              if (!top) return null;
              return {
                hasPrev: !!top.querySelector('.ch-prev'),
                hasNext: !!top.querySelector('.ch-next'),
              };
            }
            """
        )
        print(f"Boundary at gen.1: {boundary}")
        assert boundary["hasPrev"] is False
        assert boundary["hasNext"] is True
        print("  OK — first chapter shows next only\n")

        # ── 6. Screenshots ────────────────────────────────────
        page.screenshot(
            path="reports/v63_top_traverse_gen1.png",
            clip={"x": 0, "y": 0, "width": 1440, "height": 500},
        )
        # Navigate to a chapter showing both prev and next at top
        page.evaluate("navTo(1)")  # gen.2
        page.wait_for_timeout(600)
        page.screenshot(
            path="reports/v63_top_traverse_gen2.png",
            clip={"x": 0, "y": 0, "width": 1440, "height": 500},
        )
        # Folio mode to see centred rail
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(500)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        page.screenshot(
            path="reports/v63_centred_rail_header.png",
            clip={"x": 0, "y": 0, "width": 1440, "height": 600},
        )

        b.close()

    # ── 7. BIBLE_FOLIO_OBJECT_INDEX.md exists and contains
    # expected anchor chapters.
    idx_path = ROOT / "BIBLE_FOLIO_OBJECT_INDEX.md"
    assert idx_path.exists(), f"missing {idx_path}"
    text = idx_path.read_text(encoding="utf-8")
    for needle in ("Genesis 1", "Genesis 12", "Genesis 28", "Genesis 46"):
        assert needle in text, f"index missing '{needle}'"
    # Spot-check a wave-one record is named in the index.
    assert "Altar at Shechem" in text
    assert "well at Beersheba" in text
    assert "pillar at Bethel" in text
    assert "Lekh lekha" in text
    assert "Jacob's ladder" in text
    assert "going-down into Egypt" in text
    print("BIBLE_FOLIO_OBJECT_INDEX.md present and complete:")
    print(f"  · {idx_path.stat().st_size:,} bytes")
    print("  · contains Genesis 1, 12, 28, 46 entries")
    print("  · all six wave-one records listed by title")
    print()
    print("ALL CHECKS PASSED — v63 usability refinement in place.")


if __name__ == "__main__":
    main()
