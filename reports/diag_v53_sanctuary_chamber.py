"""v53 — AO · 012 The House Filled With Glory (The Layered Sanctuary).

Verifies the twelfth Atlas Object class is wired end-to-end:
  · Folio marker present at Exodus 40:34 with the new ⊞ glyph.
  · Chamber renders five concentrically narrowing layers
    (depths 1-5) with max-widths approximately
    560 → 480 → 400 → 340 → 280 pixels.
  · Threshold rubrics appear BEFORE layers 2-4 only; no rubric
    above the indwelling glory (layer 5).
  · The indwelling layer carries a warmer gradient + gold rule.
  · Vocabulary of Nearness section renders five terms.
  · Recurrence rubric fires on a second anchoring.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import re
from playwright.sync_api import sync_playwright


def pxnum(s):
    m = re.match(r"([\d.]+)", s.strip())
    return float(m.group(1)) if m else 0.0


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=exo.40.34",
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

        # ── Marker present at exo.40.34 with ⊞ glyph
        exo4034 = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="exo.40.34"]');
            if (!c) return null;
            return Array.from(c.querySelectorAll('.cr-folio-marker')).map(m => ({
              kind: m.dataset.kind,
              aria: m.getAttribute('aria-label'),
              weight: m.dataset.anchorWeight,
            }));
          }
        """
        )
        print(f"Exodus 40:34 cluster markers:")
        for m in exo4034 or []:
            print(f"  · {m['kind']:<22} weight={m['weight']:<12} {m['aria']}")
        assert exo4034
        sanctum = next(
            (m for m in exo4034
             if "House Filled With Glory" in (m["aria"] or "")),
            None,
        )
        assert sanctum, exo4034
        assert sanctum["kind"] == "sacred-space"
        assert sanctum["weight"] == "originating"
        print("  OK — AO · 012 marker (⊞ sacred-space) present + originating at exo.40.34\n")

        # ── Open the chamber
        page.evaluate("_openFolioObject('exo40-sanctuary-glory')")
        page.wait_for_timeout(1500)

        snap = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.sanctuary-chamber');
            if (!leaf) return null;
            const layers = Array.from(leaf.querySelectorAll('.sa-layer'));
            const thresholds = Array.from(leaf.querySelectorAll('.sa-threshold'));
            const terms = Array.from(leaf.querySelectorAll('.sa-term-row'));
            const sections = Array.from(
              leaf.querySelectorAll('.cc-section-heading .cc-section-title')
            ).map(el => el.textContent);
            return {
              siglum: leaf.querySelector('.cc-aor-siglum')?.textContent,
              gravity: leaf.dataset.gravity,
              sections,
              layerCount: layers.length,
              layers: layers.map(L => ({
                depth: L.dataset.depth,
                indwelling: L.dataset.indwelling || null,
                name: L.querySelector('.sa-layer-name')?.textContent,
                hebrew: L.querySelector('.sa-layer-hebrew')?.textContent,
                translit: L.querySelector('.sa-layer-translit')?.textContent,
                maxWidth: getComputedStyle(L).maxWidth,
                witness: !!L.querySelector('.sa-layer-witness'),
              })),
              thresholdCount: thresholds.length,
              thresholds: thresholds.map(t => t.textContent),
              termCount: terms.length,
              terms: terms.map(t => ({
                lang: t.dataset.lang,
                script: t.querySelector('.sa-term-script')?.textContent,
                translit: t.querySelector('.sa-term-translit')?.textContent,
              })),
            };
          }
        """
        )
        assert snap, "sanctuary chamber did not render"
        print("CHAMBER — sanctuary:")
        print(f"  siglum:   {snap['siglum']!r}")
        print(f"  gravity:  {snap['gravity']}")
        print(f"  sections: {snap['sections']}")
        print(f"  layers ({snap['layerCount']}):")
        for L in snap['layers']:
            mark = " · INDWELLING" if L['indwelling'] else ""
            print(f"    depth {L['depth']} · {L['name']:<22} "
                  f"{L['hebrew']:<18} max-width={L['maxWidth']}{mark}")
        print(f"  thresholds ({snap['thresholdCount']}):")
        for t in snap['thresholds']:
            print(f"    {t!r}")
        print(f"  vocabulary terms ({snap['termCount']}):")
        for t in snap['terms']:
            print(f"    · ({t['lang']}) {t['script']:<22} {t['translit']}")

        # Five layers, depths 1-5
        assert snap["siglum"] == "AO · 012"
        assert snap["gravity"] == "originating"
        assert snap["sections"] == [
            "The Approach", "Vocabulary of Nearness", "Anchorings",
        ]
        assert snap["layerCount"] == 5
        for i, L in enumerate(snap["layers"]):
            assert L["depth"] == str(i + 1), L
            assert L["name"], L
            assert L["witness"], L
        # The fifth is indwelling
        assert snap["layers"][4]["indwelling"] == "true"
        assert "Glory" in snap["layers"][4]["name"]

        # Max-width narrows from layer 1 → 5
        widths = [pxnum(L["maxWidth"]) for L in snap["layers"]]
        print(f"\n  max-widths: {widths}")
        for i in range(len(widths) - 1):
            assert widths[i] > widths[i + 1], (widths[i], widths[i + 1], i)
        assert widths[0] >= 540  # depth 1 is at least 540px
        assert widths[4] <= 300  # depth 5 narrows to about 280px
        print("  OK — five layers, depths 1-5, max-widths narrow concentrically")

        # Thresholds: BEFORE layers 2, 3, 4 only; NONE before
        # layer 5 (the glory enters the room, not the other way).
        assert snap["thresholdCount"] == 3, snap["thresholdCount"]
        threshold_blob = " | ".join(snap["thresholds"])
        # Expected thresholds correspond to layers 2-4
        assert "into his courts" in threshold_blob
        assert "first veil" in threshold_blob
        assert "second veil" in threshold_blob
        print("  OK — three threshold rubrics (before layers 2,3,4); none before the Glory\n")

        # Vocabulary: 5 terms
        assert snap["termCount"] == 5
        translits = [t["translit"] for t in snap["terms"]]
        for required in ["qodesh", "parocheth", "kavod", "keruvim", "doxa"]:
            assert any(required in (t or "") for t in translits), required
        print("  OK — vocabulary of nearness: qodesh, parocheth, kavod, keruvim, doxa\n")

        # ── Visual atmosphere check — indwelling layer differs
        atmosphere = page.evaluate(
            """
          () => {
            const layers = document.querySelectorAll('.sa-layer');
            const first = layers[0];
            const glory = document.querySelector('.sa-layer[data-indwelling="true"]');
            return {
              firstBg: getComputedStyle(first).backgroundImage,
              gloryBg: getComputedStyle(glory).backgroundImage,
              firstBorderTopWidth: getComputedStyle(first).borderTopWidth,
              gloryBorderTopWidth: getComputedStyle(glory).borderTopWidth,
              gloryMarginTop: getComputedStyle(glory).marginTop,
            };
          }
        """
        )
        print(f"VISUAL atmosphere:")
        print(f"  first bg:  {atmosphere['firstBg'][:60]!r}...")
        print(f"  glory bg:  {atmosphere['gloryBg'][:60]!r}...")
        print(f"  first border-top-width: {atmosphere['firstBorderTopWidth']}")
        print(f"  glory border-top-width: {atmosphere['gloryBorderTopWidth']}")
        print(f"  glory margin-top:       {atmosphere['gloryMarginTop']}")
        assert atmosphere["firstBg"] != atmosphere["gloryBg"]
        # Glory has 2px gold rule above; first has 1px standard
        assert pxnum(atmosphere["gloryBorderTopWidth"]) > pxnum(atmosphere["firstBorderTopWidth"])
        # Glory has more margin-top breath
        assert pxnum(atmosphere["gloryMarginTop"]) >= 40
        print("  OK — Glory carries warmer gradient + thicker gold rule + wider breath\n")

        # Screenshots
        page.screenshot(path="reports/v53_sanctuary_top.png")
        page.evaluate(
            "() => { const el = document.querySelectorAll('.sa-layer')[2];"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v53_sanctuary_mid.png")
        page.evaluate(
            "() => { const el = document.querySelector('.sa-layer[data-indwelling]');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v53_sanctuary_glory.png")
        page.evaluate(
            "() => { const el = document.querySelector('.sa-vocabulary');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v53_sanctuary_vocabulary.png")
        page.evaluate(
            "() => { const el = document.querySelector('.cc-archive');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v53_sanctuary_archive.png")

        # ── Recurrence at Isaiah 6:1
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
        isa_marker = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="isa.6.1"]');
            return c ? !!c.querySelector(
              '.cr-folio-marker[data-kind="sacred-space"]'
            ) : false;
          }
        """
        )
        print(f"Isaiah 6:1 AO · 012 marker present: {isa_marker}")
        assert isa_marker
        page.evaluate("_openFolioObject('exo40-sanctuary-glory')")
        page.wait_for_timeout(900)
        recur = page.evaluate(
            """
          () => {
            const r = document.querySelector(
              '.folio-leaf.sanctuary-chamber .cc-recurrence-rubric');
            return r ? {
              lead: r.querySelector('.ccr-lead')?.textContent,
              where: r.querySelector('.ccr-where')?.textContent,
            } : null;
          }
        """
        )
        print(f"  recurrence rubric: {recur}")
        assert recur and "Exodus 40:34" in (recur["where"] or "")
        print("  OK — AO · 012 recurs at Isaiah 6:1 with recurrence rubric\n")
        page.screenshot(path="reports/v53_sanctuary_isaiah.png")

        b.close()
    print("ALL CHECKS PASSED — AO · 012 sanctuary chamber is operational")


if __name__ == "__main__":
    main()
