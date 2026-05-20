"""v52 — Inwardness consolidation.

Verifies three small atmospheric refinements that deepen the
codex's spatial intelligence:
  · Lede paragraphs at originating chambers narrow to max-width
    540px (centred) — the text recedes inward.
  · Section headings at originating chambers carry an extra
    fade-in (acp-emerge) starting 420ms into the leaf settle —
    layered emergence.
  · Codex Preface now lists eight rubrics, ending with
    "On inwardness".
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import re
from playwright.sync_api import sync_playwright


def pxnum(s):
    m = re.match(r"([\d.]+)", s.strip())
    return float(m.group(1)) if m else 0.0


def secs(s):
    m = re.match(r"([\d.]+)s", s.strip())
    return float(m.group(1)) if m else 0.0


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── Originating chamber: lede narrows + section heading
        # gains layered emergence animation.
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.6",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.evaluate("() => localStorage.removeItem('atlas:encounters:v1')")
        page.click("#companion-toggle")
        page.wait_for_timeout(700)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        page.evaluate("_openFolioObject('gen1-cosmology-firmament')")
        page.wait_for_timeout(1500)

        orig = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf');
            const lede = leaf?.querySelector('[class$="-lede"], .cc-lede');
            const head = leaf?.querySelector('.cc-section-heading');
            return {
              gravity: leaf?.dataset.gravity,
              ledeMaxWidth: lede ? getComputedStyle(lede).maxWidth : null,
              ledeMarginLeft: lede ? getComputedStyle(lede).marginLeft : null,
              ledeMarginRight: lede ? getComputedStyle(lede).marginRight : null,
              headAnimationName: head ? getComputedStyle(head).animationName : null,
              headAnimationDelay: head ? getComputedStyle(head).animationDelay : null,
              headAnimationDuration: head ? getComputedStyle(head).animationDuration : null,
              headAnimationFill: head ? getComputedStyle(head).animationFillMode : null,
            };
          }
        """
        )
        print("ORIGINATING chamber (gen.1.6, AO·001):")
        print(f"  gravity: {orig['gravity']}")
        print(f"  lede max-width:    {orig['ledeMaxWidth']}")
        print(f"  lede margin left:  {orig['ledeMarginLeft']}")
        print(f"  lede margin right: {orig['ledeMarginRight']}")
        print(f"  section heading animation: {orig['headAnimationName']}")
        print(f"  section heading delay:     {orig['headAnimationDelay']}")
        print(f"  section heading duration:  {orig['headAnimationDuration']}")
        print(f"  section heading fill mode: {orig['headAnimationFill']}")
        assert orig["gravity"] == "originating"
        # Lede narrows to <= 540px
        ledemw = pxnum(orig["ledeMaxWidth"] or "9999px")
        assert ledemw <= 540, ledemw
        # Lede is centred (auto margins)
        # Browsers may compute "auto" as a px value; we check that
        # left == right (centred)
        assert orig["ledeMarginLeft"] == orig["ledeMarginRight"]
        # Section heading carries acp-emerge animation
        assert "acp-emerge" in (orig["headAnimationName"] or "")
        assert secs(orig["headAnimationDelay"]) >= 0.4
        assert orig["headAnimationFill"] == "backwards"
        print("  OK — lede narrowed + section heading layered emergence wired\n")

        # ── Echo chamber: lede does NOT narrow; no layered emergence
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=psa.104.5",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        page.evaluate("_openFolioObject('gen1-cosmology-firmament')")
        page.wait_for_timeout(900)

        echo = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf');
            const lede = leaf?.querySelector('[class$="-lede"], .cc-lede');
            const head = leaf?.querySelector('.cc-section-heading');
            return {
              gravity: leaf?.dataset.gravity,
              ledeMaxWidth: lede ? getComputedStyle(lede).maxWidth : null,
              headAnimationName: head ? getComputedStyle(head).animationName : null,
              headAnimationDelay: head ? getComputedStyle(head).animationDelay : null,
            };
          }
        """
        )
        print(f"ECHO chamber (psa.104.5):")
        print(f"  gravity: {echo['gravity']}")
        print(f"  lede max-width:           {echo['ledeMaxWidth']}")
        print(f"  section heading animation:{echo['headAnimationName']}")
        print(f"  section heading delay:    {echo['headAnimationDelay']}")
        assert echo["gravity"] == "echo"
        # Echo lede should NOT be constrained to 540px (max-width should be 'none' or larger)
        echo_mw = echo["ledeMaxWidth"] or "none"
        if echo_mw not in ("none", "9999px"):
            echo_mw_num = pxnum(echo_mw)
            assert echo_mw_num > 540 or echo_mw == "none", echo
        # Echo section heading should NOT have acp-emerge
        assert "acp-emerge" not in (echo["headAnimationName"] or "none")
        print("  OK — echo chambers do not narrow / do not layer-emerge\n")

        # ── Codex Preface — eight rubrics now
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.click(".bcl-codex-preface-link")
        page.wait_for_timeout(400)
        rubrics = page.evaluate(
            """
          () => Array.from(document.querySelectorAll(
            '.atlas-codex-preface .acp-rubric-name'
          )).map(el => el.textContent)
        """
        )
        print(f"Codex Preface rubrics ({len(rubrics)}):")
        for r in rubrics:
            print(f"  ⁕ {r}")
        assert len(rubrics) == 8
        assert "inwardness" in rubrics[7].lower()
        print("  OK — eighth rubric 'On inwardness' present\n")
        page.screenshot(path="reports/v52_preface_eight.png", full_page=False)

        # Capture inwardness atmosphere from the originating chamber
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.6",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(700)
        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        page.evaluate("_openFolioObject('gen1-cosmology-firmament')")
        page.wait_for_timeout(1400)
        page.screenshot(path="reports/v52_inward_originating.png")

        b.close()
    print("ALL CHECKS PASSED — inwardness consolidation is operational")


if __name__ == "__main__":
    main()
