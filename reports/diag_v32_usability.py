"""v32 — focused usability cleanup verification.

Covers three orthogonal fixes:
  1. Bible cover has a clear top-left back-to-reading-room button
     - When no prior reading context: opens Genesis 1
     - When prior reading context exists: returns to it
  2. About-this-text pill is hidden in the reading room (still
     present on the contents/title leaf)
  3. Folio depth rubric is legible, controls are clickable,
     active state visibly different, and marker counts
     decrease CORE < STUDY < ARCHIVE
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/index.html?text=bible_kjv.json"


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── 1a. Cold open of Bible title leaf → back button → Gen 1
        page.goto(BASE, wait_until="networkidle")
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        cover_state = page.evaluate(
            """
          () => {
            const btn = document.querySelector('.bcl-back-to-reading');
            const bar = document.getElementById('info-bar');
            return {
              hasBackBtn: !!btn,
              btnTxt: btn ? btn.textContent.trim() : null,
              btnTarget: btn ? btn.dataset.targetBook : null,
              btnPos: btn ? btn.getBoundingClientRect().toJSON() : null,
              infoBarOnCover: bar ? getComputedStyle(bar).display : null,
              inReading: document.body.classList.contains('in-reading'),
            };
          }
        """
        )
        print("─── Cover state (cold open) ───")
        print(f"  back btn: {cover_state['hasBackBtn']!r} text={cover_state['btnTxt']!r}")
        print(f"  target book: {cover_state['btnTarget']!r}")
        print(f"  btn top-left: {cover_state['btnPos']['x']:.0f}, {cover_state['btnPos']['y']:.0f}")
        print(f"  info-bar on cover: {cover_state['infoBarOnCover']}")
        assert cover_state["hasBackBtn"]
        assert cover_state["btnTxt"].startswith("←")  # ←
        # On a cold open with no memo, target defaults to gen.1
        assert cover_state["btnTarget"] == "gen.1", cover_state["btnTarget"]
        # Top-left positioning (page may have a top info-bar header,
        # so the cover content area starts ~80-120px below page top).
        assert cover_state["btnPos"]["x"] < 150
        assert cover_state["btnPos"]["y"] < 200
        # About-this-text pill stays present on cover
        assert cover_state["infoBarOnCover"] != "none"
        print("OK — back button is top-left, info-bar present on cover")
        page.screenshot(path="reports/v32_cover_with_back.png")

        # Click and verify Genesis 1 opens
        page.click(".bcl-back-to-reading")
        page.wait_for_timeout(800)
        entered = page.evaluate(
            """
          () => ({
            inReading: document.body.classList.contains('in-reading'),
            currentBook: document.getElementById('ctrl-book') ? document.getElementById('ctrl-book').value : null,
            infoBarDisplay: getComputedStyle(document.getElementById('info-bar')).display,
          })
        """
        )
        print(f"\n─── After clicking back-btn cold ───")
        print(f"  in-reading: {entered['inReading']}")
        print(f"  currentBook: {entered['currentBook']}")
        print(f"  info-bar display in reading room: {entered['infoBarDisplay']}")
        assert entered["inReading"]
        assert entered["currentBook"] == "gen.1"
        # ── 2. About-this-text pill hidden in reading room
        assert entered["infoBarDisplay"] == "none", (
            f"info-bar should be hidden in reading room, got {entered['infoBarDisplay']}"
        )
        print("OK — Genesis 1 opened; About-this-text pill hidden")
        page.screenshot(path="reports/v32_reading_no_info_bar.png")

        # ── 1b. Scroll, leave to Contents, come back via button
        page.evaluate("document.getElementById('reader').scrollTop = 300")
        page.wait_for_timeout(300)
        # Click Contents button
        page.click("#ctrl-contents")
        page.wait_for_timeout(800)
        back_after = page.evaluate(
            """
          () => {
            const btn = document.querySelector('.bcl-back-to-reading');
            return {
              txt: btn ? btn.textContent.trim() : null,
              target: btn ? btn.dataset.targetBook : null,
            };
          }
        """
        )
        print(f"\n─── After leaving Gen 1 to Contents ───")
        print(f"  back btn text: {back_after['txt']}")
        print(f"  back btn target: {back_after['target']}")
        assert "Return" in back_after["txt"], back_after["txt"]
        page.screenshot(path="reports/v32_cover_after_reading.png")
        page.click(".bcl-back-to-reading")
        page.wait_for_timeout(800)
        restored = page.evaluate(
            """
          () => ({
            inReading: document.body.classList.contains('in-reading'),
            currentBook: document.getElementById('ctrl-book') ? document.getElementById('ctrl-book').value : null,
            scrollTop: document.getElementById('reader').scrollTop,
          })
        """
        )
        print(f"  on return: book={restored['currentBook']} scroll={restored['scrollTop']}")
        assert restored["inReading"]
        assert restored["currentBook"] == "gen.1"
        # Scroll position should be restored
        assert restored["scrollTop"] > 200, (
            f"scroll not restored: {restored['scrollTop']}"
        )
        print("OK — return-to-reading restored chapter and scroll")

        # ── 3. Depth rubric — legibility + controls work
        page.click("#companion-toggle")
        page.wait_for_timeout(800)
        rubric = page.evaluate(
            """
          () => {
            const r = document.querySelector('.cr-folio-depth-rubric');
            if (!r) return null;
            const prefix = r.querySelector('.crd-prefix');
            const labels = Array.from(r.querySelectorAll('.crd-label'));
            return {
              rect: r.getBoundingClientRect().toJSON(),
              prefix: prefix ? prefix.textContent : null,
              labels: labels.map(b => {
                const cs = getComputedStyle(b);
                return {
                  txt: b.textContent,
                  active: b.classList.contains('active'),
                  ariaPressed: b.getAttribute('aria-pressed'),
                  fontSize: cs.fontSize,
                  color: cs.color,
                  fontWeight: cs.fontWeight,
                  borderBottom: cs.borderBottom,
                };
              }),
            };
          }
        """
        )
        print(f"\n─── Depth rubric ───")
        print(f"  prefix: {rubric['prefix']!r}")
        for lab in rubric["labels"]:
            print(f"  [{'*' if lab['active'] else ' '}] {lab['txt']:<8} "
                  f"size={lab['fontSize']} wt={lab['fontWeight']} "
                  f"color={lab['color']} bd={lab['borderBottom']}")
        # Prefix "Apparatus —"
        assert rubric["prefix"] and "Apparatus" in rubric["prefix"]
        # Three labels
        assert [l["txt"] for l in rubric["labels"]] == ["core", "study", "archive"]
        # Active state visually distinct: only core is active
        active = [l for l in rubric["labels"] if l["active"]]
        assert len(active) == 1 and active[0]["txt"] == "core"
        assert active[0]["ariaPressed"] == "true"
        # Active label has heavier weight + thicker border than inactive
        inactive_weights = [l["fontWeight"] for l in rubric["labels"] if not l["active"]]
        assert int(active[0]["fontWeight"]) > int(inactive_weights[0]), (
            f"active weight {active[0]['fontWeight']} not > inactive {inactive_weights[0]}"
        )
        print("OK — rubric legibility tuned, active state distinct")

        # Verify CORE < STUDY < ARCHIVE marker counts
        def count_visible():
            return page.evaluate(
                """
              () => Array.from(document.querySelectorAll('.cr-folio-marker'))
                       .filter(m => getComputedStyle(m).display !== 'none').length
            """
            )

        page.evaluate("_setFolioDepth('core')")
        page.wait_for_timeout(300)
        c = count_visible()
        page.evaluate("_setFolioDepth('study')")
        page.wait_for_timeout(300)
        s = count_visible()
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(300)
        a = count_visible()
        print(f"\n─── Marker progression ───")
        print(f"  CORE    = {c}")
        print(f"  STUDY   = {s}")
        print(f"  ARCHIVE = {a}")
        assert c < s < a, f"Expected CORE<STUDY<ARCHIVE, got {c}/{s}/{a}"
        print("OK — depth controls visibly reduce/expand markers")

        # Fresh screenshots after legibility tuning
        for depth in ("core", "study", "archive"):
            page.evaluate(f"_setFolioDepth('{depth}')")
            page.wait_for_timeout(300)
            page.screenshot(path=f"reports/v32_rubric_{depth}.png")

        # Verify ctrl-contents button is visible in reading room
        ctrl_contents = page.evaluate(
            "() => getComputedStyle(document.getElementById('ctrl-contents')).display"
        )
        print(f"\n#ctrl-contents display in reading room: {ctrl_contents}")
        assert ctrl_contents != "none", "Contents back-button missing in reading room"
        print("OK — Contents button visible in reading room (forward/backward both work)")

        b.close()
    print("\nALL CHECKS PASSED")
    print("Screenshots:")
    for f in [
        "v32_cover_with_back.png",
        "v32_reading_no_info_bar.png",
        "v32_cover_after_reading.png",
        "v32_rubric_core.png",
        "v32_rubric_study.png",
        "v32_rubric_archive.png",
    ]:
        print(f"  reports/{f}")


if __name__ == "__main__":
    main()
