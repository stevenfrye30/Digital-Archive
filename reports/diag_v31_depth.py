"""v31 — layered folio depth controls (CORE / STUDY / ARCHIVE).

Verifies, on the live local server:
  • Default depth = CORE
  • Marker visibility per depth matches authority tiers
  • Per-cluster "+N" indicator counts only deeper-tier records
  • Clusters with neither visible markers nor deeper records collapse
  • Clicking "+N" advances depth one step
  • DEBUG_FOLIO surfaces depth + P/S/T tier counts per cluster

Captures CORE / STUDY / ARCHIVE screenshots at Gen 1:1 and Gen 1:3
for visual diff review.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from collections import Counter
from pathlib import Path
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent.parent
BASE = "http://localhost:8765/index.html?text=bible_kjv.json"


def main():
    # ── Data audit — confirm Gen 1 tier distribution ──────────
    with open(ROOT / "data" / "bible_kjv.json", encoding="utf-8") as f:
        data = json.load(f)
    g1 = [r for r in data["genealogy"]
          if any(a.get("target", "").split("::").pop().startswith("gen.1.")
                 for a in r.get("anchors", []))]
    tier = Counter(r.get("authority", "?") for r in g1)
    print(f"Genesis 1 ({len(g1)} witnesses):")
    print(f"  primary   = {tier.get('primary', 0)}")
    print(f"  secondary = {tier.get('secondary', 0)}")
    print(f"  tertiary  = {tier.get('tertiary', 0)}")
    expected = {"primary": 5, "secondary": 4, "tertiary": 13}
    for k, v in expected.items():
        assert tier.get(k, 0) == v, (
            f"tier mismatch: {k} expected {v}, got {tier.get(k, 0)}"
        )
    print("OK — Genesis 1 tier distribution matches 5/4/13 expectation\n")

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(f"{BASE}&p=gen.1.1", wait_until="networkidle")
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.click("#companion-toggle")
        page.wait_for_timeout(800)

        # ── 1. Default depth = CORE ────────────────────────
        body_classes = page.evaluate(
            "() => Array.from(document.body.classList).filter(c => c.startsWith('folio-depth-'))"
        )
        print(f"Initial body folio-depth classes: {body_classes}")
        assert body_classes == ["folio-depth-core"], (
            f"expected only folio-depth-core, got {body_classes}"
        )
        print("OK — default depth is CORE")

        # ── 2. Rubric is present ─────────────────────────────
        rubric = page.evaluate(
            """
          () => {
            const r = document.querySelector('.cr-folio-depth-rubric');
            if (!r) return null;
            return {
              labels: Array.from(r.querySelectorAll('.crd-label')).map(b => ({
                txt: b.textContent,
                active: b.classList.contains('active'),
              })),
            };
          }
        """
        )
        assert rubric, "rubric missing"
        assert [l["txt"] for l in rubric["labels"]] == ["core", "study", "archive"]
        assert rubric["labels"][0]["active"]
        print(f"OK — rubric: {rubric['labels']}\n")

        # ── 3. For each depth mode capture visibility + tier state
        def snapshot():
            return page.evaluate(
                """
              () => {
                const clusters = Array.from(document.querySelectorAll('.cr-folio-cluster'));
                return clusters.map(c => {
                  const cs = getComputedStyle(c);
                  const markers = Array.from(c.querySelectorAll('.cr-folio-marker'));
                  const visible = markers.filter(m => getComputedStyle(m).display !== 'none').length;
                  const deeper = c.querySelector(':scope > .cr-folio-deeper');
                  return {
                    pid: c.dataset.anchorPid,
                    display: cs.display,
                    empty: c.classList.contains('cr-folio-cluster-empty'),
                    total: markers.length,
                    visible,
                    tierP: Number(c.dataset.tierPrimary || 0),
                    tierS: Number(c.dataset.tierSecondary || 0),
                    tierT: Number(c.dataset.tierTertiary || 0),
                    deeper: deeper ? deeper.textContent : null,
                    deeperAria: deeper ? deeper.getAttribute('aria-label') : null,
                  };
                });
              }
            """
            )

        for depth in ("core", "study", "archive"):
            page.evaluate(f"_setFolioDepth('{depth}')")
            page.wait_for_timeout(400)
            snap = snapshot()
            vis_tot = sum(c["visible"] for c in snap)
            mark_tot = sum(c["total"] for c in snap)
            empty_clusters = sum(1 for c in snap if c["empty"])
            indicators = [c for c in snap if c["deeper"]]
            print(f"--- {depth.upper()} ---")
            print(f"  visible markers: {vis_tot}/{mark_tot}")
            print(f"  empty clusters: {empty_clusters}")
            print(f"  +N indicators: {len(indicators)}")
            for c in snap:
                line = (
                    f"    {c['pid']:<10} P{c['tierP']}/S{c['tierS']}/T{c['tierT']} "
                    f"vis={c['visible']}/{c['total']} "
                    f"empty={c['empty']} "
                    f"deeper={c['deeper']}"
                )
                print(line)

            # Per-cluster invariants
            for c in snap:
                if depth == "core":
                    assert c["visible"] == c["tierP"], (
                        f"{c['pid']} CORE visible {c['visible']} != tierP {c['tierP']}"
                    )
                    expected_deeper = c["tierS"] + c["tierT"]
                elif depth == "study":
                    assert c["visible"] == c["tierP"] + c["tierS"]
                    expected_deeper = c["tierT"]
                else:
                    assert c["visible"] == c["tierP"] + c["tierS"] + c["tierT"]
                    expected_deeper = 0
                if expected_deeper > 0:
                    assert c["deeper"] == f"+{expected_deeper}", (
                        f"{c['pid']} {depth}: expected +{expected_deeper}, got {c['deeper']}"
                    )
                else:
                    assert c["deeper"] is None, (
                        f"{c['pid']} {depth}: stale deeper indicator {c['deeper']}"
                    )
                # Empty rule
                if c["visible"] == 0 and expected_deeper == 0:
                    assert c["empty"], f"{c['pid']} {depth}: should be empty"
                else:
                    assert not c["empty"], f"{c['pid']} {depth}: should not be empty"
            print(f"  OK — all clusters consistent at {depth.upper()}")
            page.screenshot(path=f"reports/v31_{depth}_gen1_1.png")

        # ── 4. Reset to CORE, click "+N" → STUDY
        page.evaluate("_setFolioDepth('core')")
        page.wait_for_timeout(300)
        clicked = page.evaluate(
            """
          () => {
            const btn = document.querySelector('.cr-folio-cluster .cr-folio-deeper');
            if (!btn) return false;
            btn.click();
            return true;
          }
        """
        )
        assert clicked, "no +N button to click on Gen 1:1"
        page.wait_for_timeout(400)
        next_depth = page.evaluate(
            "() => Array.from(document.body.classList).filter(c => c.startsWith('folio-depth-'))[0]"
        )
        assert next_depth == "folio-depth-study", (
            f"clicking +N from CORE should advance to STUDY, got {next_depth}"
        )
        print("\nOK — clicking +N advanced CORE -> STUDY")

        # And STUDY +N -> ARCHIVE
        clicked2 = page.evaluate(
            """
          () => {
            const btn = document.querySelector('.cr-folio-cluster .cr-folio-deeper');
            if (!btn) return false;
            btn.click();
            return true;
          }
        """
        )
        page.wait_for_timeout(400)
        last_depth = page.evaluate(
            "() => Array.from(document.body.classList).filter(c => c.startsWith('folio-depth-'))[0]"
        )
        assert last_depth == "folio-depth-archive", last_depth
        print("OK — clicking +N advanced STUDY -> ARCHIVE")

        # ── 5. DEBUG_FOLIO surfaces depth + tier info
        page.evaluate("_setFolioDepth('study')")
        page.wait_for_timeout(300)
        page.evaluate("window.toggleFolioDebug()")
        page.wait_for_timeout(400)
        debug_sample = page.evaluate(
            """
          () => {
            const c = document.querySelector('.cr-folio-cluster:not(.cr-folio-cluster-empty)');
            return {
              hasClass: document.body.classList.contains('debug-folio'),
              debugAttr: c ? c.dataset.debug : null,
            };
          }
        """
        )
        print(f"\nDEBUG_FOLIO sample: {debug_sample}")
        assert debug_sample["hasClass"]
        assert debug_sample["debugAttr"]
        # Verify depth + tier counts present in debug text
        for token in ("study", "P", "S", "T"):
            assert token in debug_sample["debugAttr"], (
                f"missing '{token}' in debug overlay: {debug_sample['debugAttr']}"
            )
        print("OK — DEBUG_FOLIO surfaces depth + P/S/T tier counts")
        page.evaluate("window.toggleFolioDebug()")
        page.wait_for_timeout(200)

        # ── 6. Same three screenshots at Gen 1:3
        page.goto(f"{BASE}&p=gen.1.3", wait_until="networkidle")
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.click("#companion-toggle")
        page.wait_for_timeout(800)
        for depth in ("core", "study", "archive"):
            page.evaluate(f"_setFolioDepth('{depth}')")
            page.wait_for_timeout(400)
            page.screenshot(path=f"reports/v31_{depth}_gen1_3.png")

        b.close()
    print("\nALL CHECKS PASSED — depth controls operational at CORE/STUDY/ARCHIVE")
    print("Screenshots:")
    for d in ("core", "study", "archive"):
        print(f"  reports/v31_{d}_gen1_1.png")
        print(f"  reports/v31_{d}_gen1_3.png")


if __name__ == "__main__":
    main()
