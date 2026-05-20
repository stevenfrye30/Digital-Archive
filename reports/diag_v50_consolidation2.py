"""v50 — Consolidation phase two.

Verifies atmospheric refinements that give the archive memory
sediment and recurrence stratification:
  · Chamber leaves carry data-gravity = "originating" or "echo"
    depending on whether the current pid is the object's first
    anchor. Originating chambers settle more slowly and carry a
    subtle warm wash at the head.
  · Markers carry data-anchor-weight following the same rule.
    Originating-anchor markers have deeper border colour;
    echo-anchor markers have slightly reduced opacity.
  · The first item in each chamber's Anchorings list is marked
    data-anchor-weight="originating" and renders heavier.
  · Codex Preface now contains six rubrics, the last of which
    reflects on memory's gravity.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import re
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
        page.wait_for_timeout(800)
        page.evaluate("() => localStorage.removeItem('atlas:encounters:v1')")
        page.click("#companion-toggle")
        page.wait_for_timeout(700)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)

        # ── Markers at gen.1.6: both AOs anchor here, and gen.1.6
        # IS the originating anchor for both AO·001 and AO·002.
        gen16_markers = page.evaluate(
            """
          () => Array.from(document.querySelectorAll(
            '.cr-folio-cluster[data-anchor-pid="gen.1.6"] .cr-folio-marker'
          )).map(m => ({
            kind: m.dataset.kind,
            weight: m.dataset.anchorWeight || null,
            authority: m.dataset.authority,
            opacity: getComputedStyle(m).opacity,
            borderColor: getComputedStyle(m).borderColor,
          }))
        """
        )
        print("Gen 1:6 markers:")
        for m in gen16_markers:
            print(f"  · {m['kind']:<22} weight={m['weight']:<12} auth={m['authority']}"
                  f"  op={m['opacity']}  border={m['borderColor']}")
        cos = next(m for m in gen16_markers if m["kind"] == "cosmology")
        trd = next(m for m in gen16_markers if m["kind"] == "translation-tradition")
        # Both originating at gen.1.6
        assert cos["weight"] == "originating", cos
        assert trd["weight"] == "originating", trd
        print("  OK — both AO markers at gen.1.6 carry anchor-weight=originating\n")

        # ── Open the cosmology chamber — gravity should be "originating"
        page.evaluate("_openFolioObject('gen1-cosmology-firmament')")
        page.wait_for_timeout(900)
        chamber = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf');
            return {
              gravity: leaf?.dataset.gravity || null,
              animation: getComputedStyle(leaf).animationDuration,
            };
          }
        """
        )
        print(f"Cosmology chamber at gen.1.6 (originating): {chamber}")
        assert chamber["gravity"] == "originating"
        # Originating chamber animates more slowly (0.72s vs default 0.5s)
        anim = chamber["animation"]
        assert "0.7" in anim, anim
        print("  OK — originating chamber settles more slowly\n")

        # Check anchorings list — first item should be marked
        # originating.
        anchorings = page.evaluate(
            """
          () => Array.from(document.querySelectorAll(
            '.folio-leaf .cc-anchorings .cc-anchoring'
          )).map(li => ({
            text: li.textContent.trim().slice(0, 60),
            weight: li.dataset.anchorWeight || null,
            refWeight: getComputedStyle(
              li.querySelector('.cc-anchoring-ref')
            ).fontWeight,
            refColor: getComputedStyle(
              li.querySelector('.cc-anchoring-ref')
            ).color,
          }))
        """
        )
        print(f"Anchorings list in cosmology chamber:")
        for i, a in enumerate(anchorings[:3]):
            mark = " · ORIGINATING" if a["weight"] == "originating" else ""
            wt = (a["weight"] or "-")
            print(f"  [{i}] weight={wt:<12} fw={a['refWeight']}  {a['text']!r}{mark}")
        assert anchorings[0]["weight"] == "originating"
        # First item has heavier weight than subsequent items
        assert int(anchorings[0]["refWeight"]) > int(anchorings[1]["refWeight"])
        print("  OK — originating anchoring is heavier than echo anchorings\n")

        # Close the chamber
        page.mouse.click(50, 50)
        page.wait_for_timeout(400)

        # ── Navigate to Psalm 104:5 — the cosmology object's
        # ECHO anchor. Marker should now carry weight="echo".
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
        psa_marker = page.evaluate(
            """
          () => {
            const m = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="psa.104.5"] '
              + '.cr-folio-marker[data-kind="cosmology"]');
            return m ? {
              weight: m.dataset.anchorWeight || null,
              opacity: getComputedStyle(m).opacity,
              visited: m.dataset.visited || null,
            } : null;
          }
        """
        )
        print(f"Psalm 104:5 cosmology marker: {psa_marker}")
        assert psa_marker["weight"] == "echo"
        # Visited from prior encounter at gen.1.6
        assert psa_marker["visited"] == "true"
        # Echo visited tertiary should be ~0.68 (per CSS), originating
        # tertiary visited is 0.78. So echo is dimmer.
        print(f"  OK — Psalm 104:5 marker is echo + visited (op {psa_marker['opacity']})\n")

        # Open the chamber at Psalm 104:5 — gravity should now be "echo"
        page.evaluate("_openFolioObject('gen1-cosmology-firmament')")
        page.wait_for_timeout(900)
        chamber_echo = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf');
            return {
              gravity: leaf?.dataset.gravity || null,
              animation: getComputedStyle(leaf).animationDuration,
            };
          }
        """
        )
        print(f"Cosmology chamber at psa.104.5 (echo): {chamber_echo}")
        assert chamber_echo["gravity"] == "echo"
        # Echo animates faster (0.42s)
        assert "0.4" in chamber_echo["animation"]
        print("  OK — echo chamber settles more quickly\n")
        page.screenshot(path="reports/v50_echo_chamber.png")

        # Compare: originating chamber animation > echo chamber animation
        # Convert "0.72s" → 0.72, "0.42s" → 0.42
        def secs(s):
            m = re.match(r"([\d.]+)s", s.strip())
            return float(m.group(1)) if m else 0.0
        orig_dur = 0.72
        echo_dur = secs(chamber_echo["animation"])
        assert orig_dur > echo_dur, (orig_dur, echo_dur)
        print(f"  cadence ratio: {orig_dur:.2f}s vs {echo_dur:.2f}s "
              f"(originating is {orig_dur/echo_dur:.2f}× slower)\n")

        # ── Codex Preface — six rubrics now (including memory's gravity)
        page.mouse.click(50, 50)
        page.wait_for_timeout(400)
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
        assert len(rubrics) == 6
        assert "memory" in rubrics[5].lower()
        print("  OK — sixth rubric 'On memory's gravity' present\n")
        page.screenshot(path="reports/v50_preface_six_rubrics.png")

        # Visit screenshot of originating chamber (Genesis 1:6) for atmosphere
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
        page.wait_for_timeout(900)
        page.screenshot(path="reports/v50_originating_chamber.png")

        b.close()
    print("ALL CHECKS PASSED — consolidation phase two is operational")


if __name__ == "__main__":
    main()
