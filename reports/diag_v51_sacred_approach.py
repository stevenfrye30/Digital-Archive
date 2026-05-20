"""v51 — Spatial consolidation: sacred approach.

Verifies the archive's new threshold/inwardness behaviours:
  · Originating chambers carry an animation-delay (~180ms) so
    the scrim holds dark before the leaf settles.
  · Originating chambers carry extra spacing beneath title
    (sanctuary breath); echo chambers do not.
  · Per-class spatial signatures: revelation chamber's first
    section heading carries extra threshold breath; wisdom
    chamber's lede has more rest at originating.
  · Codex Preface now lists seven rubrics ending with "On
    threshold".
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import re
from playwright.sync_api import sync_playwright


def secs(s):
    m = re.match(r"([\d.]+)s", s.strip())
    return float(m.group(1)) if m else 0.0


def pxnum(s):
    m = re.match(r"([\d.]+)", s.strip())
    return float(m.group(1)) if m else 0.0


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── Originating chamber threshold pre-pause + sanctuary breath
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
        page.wait_for_timeout(1200)

        orig = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf');
            const title = leaf?.querySelector(':scope > .folio-leaf-title');
            const verse = leaf?.querySelector(':scope > .folio-leaf-verse');
            return {
              gravity: leaf?.dataset.gravity,
              duration: getComputedStyle(leaf).animationDuration,
              delay: getComputedStyle(leaf).animationDelay,
              fillMode: getComputedStyle(leaf).animationFillMode,
              titleBottom: title ? getComputedStyle(title).marginBottom : null,
              verseBottom: verse ? getComputedStyle(verse).marginBottom : null,
            };
          }
        """
        )
        print("ORIGINATING chamber (gen.1.6, AO·001):")
        print(f"  gravity: {orig['gravity']}")
        print(f"  animation: {orig['duration']}, delay {orig['delay']}, "
              f"fill {orig['fillMode']}")
        print(f"  title margin-bottom: {orig['titleBottom']}")
        print(f"  verse margin-bottom: {orig['verseBottom']}")
        assert orig["gravity"] == "originating"
        # Threshold pre-pause: animation-delay should be ~0.18s
        assert secs(orig["delay"]) >= 0.15, orig
        assert orig["fillMode"] == "backwards"
        # Sanctuary breath: title margin-bottom should be >= 38px
        # (viewer-active variant 46px)
        assert pxnum(orig["titleBottom"]) >= 38, orig
        print("  OK — pre-pause held + sanctuary breath below title\n")

        # ── Echo chamber: no pre-pause, plain spacing
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
            const title = leaf?.querySelector(':scope > .folio-leaf-title');
            return {
              gravity: leaf?.dataset.gravity,
              duration: getComputedStyle(leaf).animationDuration,
              delay: getComputedStyle(leaf).animationDelay,
              titleBottom: title ? getComputedStyle(title).marginBottom : null,
            };
          }
        """
        )
        print(f"ECHO chamber (psa.104.5, AO·001):")
        print(f"  gravity: {echo['gravity']}")
        print(f"  animation: {echo['duration']}, delay {echo['delay']}")
        print(f"  title margin-bottom: {echo['titleBottom']}")
        assert echo["gravity"] == "echo"
        # Echo: no significant delay
        assert secs(echo["delay"]) < 0.05, echo
        # Echo: standard title spacing (less than originating)
        echo_title_bottom = pxnum(echo["titleBottom"] or "0")
        orig_title_bottom = pxnum(orig["titleBottom"] or "0")
        assert echo_title_bottom < orig_title_bottom, (
            echo_title_bottom, orig_title_bottom
        )
        print("  OK — no pre-pause, tighter title spacing on echo\n")

        # ── Per-class spatial signature: revelation chamber at
        # originating (isa.6.1) should have extra threshold above
        # first section heading.
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=isa.6.1",
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
        page.evaluate("_openFolioObject('isa6-opened-heavens')")
        page.wait_for_timeout(900)

        revelation = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.revelation-chamber');
            const head = leaf?.querySelector('.cc-section-heading');
            return {
              gravity: leaf?.dataset.gravity,
              firstHeadPadTop: head ? getComputedStyle(head).paddingTop : null,
              firstHeadMarginTop: head ? getComputedStyle(head).marginTop : null,
            };
          }
        """
        )
        print(f"REVELATION chamber at isa.6.1 (originating):")
        print(f"  gravity: {revelation['gravity']}")
        print(f"  first section padding-top: {revelation['firstHeadPadTop']}")
        print(f"  first section margin-top:  {revelation['firstHeadMarginTop']}")
        assert revelation["gravity"] == "originating"
        # The revelation chamber's first section gets padding-top: 32px
        assert pxnum(revelation["firstHeadPadTop"]) >= 30
        print("  OK — apocalyptic threshold breath above first section\n")

        # ── Wisdom chamber at originating
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=pro.1.7",
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
        page.evaluate("_openFolioObject('prov1-wisdom-fear')")
        page.wait_for_timeout(900)

        wisdom = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.wisdom-chamber');
            const lede = leaf?.querySelector('.ws-lede');
            return {
              gravity: leaf?.dataset.gravity,
              ledeMarginBottom: lede ? getComputedStyle(lede).marginBottom : null,
              ledeMarginTop: lede ? getComputedStyle(lede).marginTop : null,
            };
          }
        """
        )
        print(f"WISDOM chamber at pro.1.7 (originating):")
        print(f"  gravity: {wisdom['gravity']}")
        print(f"  lede margin-top: {wisdom['ledeMarginTop']}")
        print(f"  lede margin-bottom: {wisdom['ledeMarginBottom']}")
        assert wisdom["gravity"] == "originating"
        # Wisdom at originating gets enlarged lede spacing (margin-top: 18px, margin-bottom: 36px)
        assert pxnum(wisdom["ledeMarginBottom"]) >= 32
        print("  OK — wisdom chamber breathes wider at originating\n")

        # ── Codex Preface — seven rubrics now
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
        assert len(rubrics) == 7
        assert "threshold" in rubrics[6].lower()
        print("  OK — seventh rubric 'On threshold' present\n")
        page.screenshot(path="reports/v51_preface_seven.png")

        # Final atmosphere screenshot of an originating chamber
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.17.7",
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
        page.evaluate("_openFolioObject('gen17-covenant-formula')")
        page.wait_for_timeout(1100)
        page.screenshot(path="reports/v51_covenant_originating.png")

        b.close()
    print("ALL CHECKS PASSED — spatial consolidation is operational")


if __name__ == "__main__":
    main()
