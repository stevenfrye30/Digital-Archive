"""v45 — AO · 008 The Opened Heavens (Visionary Disclosure).

Verifies the eighth Atlas Object class is wired end-to-end:
  · Folio marker present at Isaiah 6:1 with the new ◎ glyph.
  · Chamber renders five threshold-vision blocks, each with a
    dim threshold rubric (reduced opacity) above the unveiled
    canonical text (full intensity).
  · The fifth vision (consummation) is visibly the chamber's
    most luminous air (warmer gradient, fuller gold rule).
  · Five vision fragments stack beneath.
  · Recurrence rubric fires on a second anchoring.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent


def main():
    with open(ROOT / "data/bible_kjv.json", encoding="utf-8") as f:
        data = json.load(f)
    rec = next(
        (r for r in data["genealogy"] if r["id"] == "isa6-opened-heavens"),
        None,
    )
    assert rec, "AO · 008 record missing"
    print("DATA — isa6-opened-heavens:")
    print(f"  kind:    {rec['kind']}")
    print(f"  title:   {rec['title']}")
    print(f"  anchors: {[a['target'].split('::').pop() for a in rec['anchors']]}")
    print(f"  AO siglum:   {rec['atlas_object']['siglum']}")
    print(f"  AO class:    {rec['atlas_object']['class']}")
    print(f"  threshold visions: {len(rec['threshold_visions'])}")
    print(f"  vision fragments:  {len(rec['vision_fragments'])}")
    assert rec["kind"] == "revelatory-vision"
    assert rec["atlas_object"]["siglum"] == "AO · 008"
    assert rec["atlas_object"]["class"] == "revelatory-vision"
    assert len(rec["threshold_visions"]) == 5
    fifth = rec["threshold_visions"][4]
    assert fifth.get("consummation") is True
    assert "Revelation 21" in fifth["ref"]
    print(f"  consummation (v): {fifth['tradition']}")
    print("OK — data structure is correct\n")

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=isa.6.1",
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

        # ── Marker present at isa.6.1 ─────────────────────────
        isa61 = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="isa.6.1"]');
            if (!c) return null;
            return Array.from(c.querySelectorAll('.cr-folio-marker')).map(m => ({
              kind: m.dataset.kind,
              aria: m.getAttribute('aria-label'),
            }));
          }
        """
        )
        print(f"Isaiah 6:1 cluster markers:")
        for m in isa61 or []:
            print(f"  · {m['kind']:<22} {m['aria']}")
        assert isa61
        ao008 = next(
            (m for m in isa61
             if "Opened Heavens" in (m["aria"] or "")),
            None,
        )
        assert ao008, isa61
        assert ao008["kind"] == "revelatory-vision"
        print("  OK — AO · 008 marker (◎ revelatory-vision) present at isa.6.1\n")

        # ── Open the chamber ──────────────────────────────────
        page.evaluate("_openFolioObject('isa6-opened-heavens')")
        page.wait_for_timeout(900)

        snap = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.revelation-chamber');
            if (!leaf) return null;
            const visions = Array.from(leaf.querySelectorAll('.rc-vision'));
            const fragments = Array.from(leaf.querySelectorAll('.rc-fragment'));
            const sections = Array.from(
              leaf.querySelectorAll('.cc-section-heading .cc-section-title')
            ).map(el => el.textContent);
            return {
              siglum: leaf.querySelector('.cc-aor-siglum')?.textContent,
              sections,
              visionCount: visions.length,
              visions: visions.map(V => ({
                consummation: V.dataset.consummation || null,
                numeral: V.querySelector('.rc-vision-numeral')?.textContent,
                ref: V.querySelector('.rc-vision-ref')?.textContent,
                tradition: V.querySelector('.rc-vision-tradition')?.textContent,
                threshold: V.querySelector('.rc-vision-threshold')?.textContent,
                unveiledLen: (V.querySelector('.rc-vision-unveiled')?.textContent || '').length,
              })),
              fragmentCount: fragments.length,
              fragments: fragments.map(F => ({
                text: F.querySelector('.rc-fragment-quote')?.textContent,
                ref: F.querySelector('.rc-fragment-ref')?.textContent,
              })),
            };
          }
        """
        )
        assert snap, "revelation chamber did not render"
        print("CHAMBER — revelation:")
        print(f"  siglum:   {snap['siglum']!r}")
        print(f"  sections: {snap['sections']}")
        print(f"  threshold visions ({snap['visionCount']}):")
        for V in snap['visions']:
            tag = " · CONSUMMATION" if V['consummation'] else ""
            print(f"    {V['numeral']:>4} · {V['ref']:<22} {V['tradition']}{tag}")
            print(f"         threshold: {V['threshold']!r}")
            print(f"         unveiled length: {V['unveiledLen']} chars")
        print(f"  vision fragments ({snap['fragmentCount']}):")
        for F in snap['fragments']:
            print(f"    · {(F['text'] or '')[:70]!r}  {F['ref']}")

        assert snap["siglum"] == "AO · 008"
        assert snap["sections"] == [
            "Threshold Visions", "Vision Fragments", "Anchorings",
        ]
        # Five threshold visions
        assert snap["visionCount"] == 5
        for V in snap["visions"]:
            assert V["numeral"], V
            assert V["ref"], V
            assert V["threshold"], V
            assert V["unveiledLen"] > 30, V
        last = snap["visions"][4]
        assert last["consummation"] == "true"
        # Five vision fragments
        assert snap["fragmentCount"] == 5
        # The "heavens were opened" phrase is present
        assert any("heavens were opened" in (F["text"] or "") for F in snap["fragments"])
        print("\n  OK — five threshold visions (consummation v marked), five fragments, all sections present")

        # ── Visual atmosphere check ───────────────────────────
        atmosphere = page.evaluate(
            """
          () => {
            const v = document.querySelectorAll('.rc-vision');
            const first = v[0];
            const cons = document.querySelector('.rc-vision[data-consummation="true"]');
            const th = first.querySelector('.rc-vision-threshold');
            const un = first.querySelector('.rc-vision-unveiled');
            return {
              firstBgImage: getComputedStyle(first).backgroundImage,
              consBgImage: getComputedStyle(cons).backgroundImage,
              firstBorderTopColor: getComputedStyle(first).borderTopColor,
              firstBorderTopWidth: getComputedStyle(first).borderTopWidth,
              consBorderTopColor: getComputedStyle(cons).borderTopColor,
              consBorderTopWidth: getComputedStyle(cons).borderTopWidth,
              thresholdColor: getComputedStyle(th).color,
              unveiledColor: getComputedStyle(un).color,
              unveiledAlign: getComputedStyle(un).textAlign,
              unveiledStyle: getComputedStyle(un).fontStyle,
            };
          }
        """
        )
        print(f"\nVISUAL atmosphere:")
        print(f"  first   bg-image:   {(atmosphere['firstBgImage'] or '')[:70]}...")
        print(f"  consum  bg-image:   {(atmosphere['consBgImage'] or '')[:70]}...")
        print(f"  first   gold rule:  {atmosphere['firstBorderTopColor']} {atmosphere['firstBorderTopWidth']}")
        print(f"  consum  gold rule:  {atmosphere['consBorderTopColor']} {atmosphere['consBorderTopWidth']}")
        print(f"  threshold text color: {atmosphere['thresholdColor']}")
        print(f"  unveiled  text color: {atmosphere['unveiledColor']}")
        print(f"  unveiled align/style: {atmosphere['unveiledAlign']} {atmosphere['unveiledStyle']}")
        # Both first and consummation carry gradients but they differ
        assert "gradient" in (atmosphere["firstBgImage"] or "")
        assert "gradient" in (atmosphere["consBgImage"] or "")
        assert atmosphere["firstBgImage"] != atmosphere["consBgImage"]
        # Consummation gold rule is at least as thick AND its color
        # is visibly richer (different RGBA than the first vision's
        # gold rule).
        first_w = float(atmosphere["firstBorderTopWidth"].rstrip("px"))
        cons_w = float(atmosphere["consBorderTopWidth"].rstrip("px"))
        assert cons_w >= first_w, (first_w, cons_w)
        assert atmosphere["consBorderTopColor"] != atmosphere["firstBorderTopColor"], (
            atmosphere["firstBorderTopColor"], atmosphere["consBorderTopColor"]
        )
        # Threshold text is dimmer than unveiled text — parse alphas
        # from "rgba(r, g, b, a)" strings.
        import re
        def alpha(rgba):
            m = re.search(r"rgba\(.+,\s*([\d.]+)\)", rgba)
            return float(m.group(1)) if m else 1.0
        th_alpha = alpha(atmosphere["thresholdColor"])
        un_alpha = alpha(atmosphere["unveiledColor"])
        print(f"  threshold alpha: {th_alpha}  unveiled alpha: {un_alpha}")
        assert th_alpha < un_alpha, (th_alpha, un_alpha)
        # Unveiled is centered italic
        assert atmosphere["unveiledAlign"] == "center"
        assert atmosphere["unveiledStyle"] == "italic"
        print("  OK — threshold dimmer than unveiled; consummation visibly more luminous\n")

        # Screenshots
        page.screenshot(path="reports/v45_revelation_top.png")
        page.evaluate(
            "() => { const el = document.querySelectorAll('.rc-vision')[2];"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v45_revelation_middle.png")
        page.evaluate(
            "() => { const el = document.querySelector('.rc-vision[data-consummation]');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v45_revelation_consummation.png")
        page.evaluate(
            "() => { const el = document.querySelector('.cc-archive');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v45_revelation_archive.png")

        # ── Recurrence at Revelation 4:1 ──────────────────────
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=rev.4.1",
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
        rev_marker = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="rev.4.1"]');
            return c ? !!c.querySelector(
              '.cr-folio-marker[data-kind="revelatory-vision"]'
            ) : false;
          }
        """
        )
        print(f"Revelation 4:1 AO · 008 marker present: {rev_marker}")
        assert rev_marker
        page.evaluate("_openFolioObject('isa6-opened-heavens')")
        page.wait_for_timeout(900)
        recur = page.evaluate(
            """
          () => {
            const r = document.querySelector(
              '.folio-leaf.revelation-chamber .cc-recurrence-rubric');
            return r ? {
              lead: r.querySelector('.ccr-lead')?.textContent,
              where: r.querySelector('.ccr-where')?.textContent,
            } : null;
          }
        """
        )
        print(f"  recurrence rubric: {recur}")
        assert recur and "Isaiah 6:1" in (recur["where"] or "")
        print("  OK — AO · 008 recurs at Revelation 4:1 with recurrence rubric\n")
        page.screenshot(path="reports/v45_revelation_rev4.png")

        b.close()
    print("ALL CHECKS PASSED — AO · 008 is operational, distinct, and recurring")


if __name__ == "__main__":
    main()
