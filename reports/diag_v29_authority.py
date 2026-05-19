"""v29 — authority class verification on Gen 1 markers + chambers."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from playwright.sync_api import sync_playwright


def main():
    # ── Data audit ─────────────────────────────────────────
    with open("data/bible_kjv.json", encoding="utf-8") as f:
        data = json.load(f)
    from collections import Counter
    auth_all = Counter(r.get("authority", "?") for r in data["genealogy"])
    g1 = [r for r in data["genealogy"]
          if any(a.get("target","").split("::").pop().startswith("gen.1.")
                 for a in r.get("anchors", []))]
    auth_g1 = Counter(r.get("authority", "?") for r in g1)
    print(f"All records by authority:        {dict(auth_all)}")
    print(f"Genesis 1 records by authority:  {dict(auth_g1)}")

    print("\nGenesis 1 records (sorted by authority then verse):")
    g1_sorted = sorted(g1, key=lambda r: (
        {'primary': 0, 'secondary': 1, 'tertiary': 2}.get(r.get('authority', 'z'), 9),
        r['anchors'][0]['target'].split('::').pop(),
    ))
    for r in g1_sorted:
        pid = r['anchors'][0]['target'].split('::').pop()
        a = r.get('authority', '?')
        k = r.get('kind', '?')
        t = r['title'][:60]
        print(f"  [{a:<10}] {k:<18} @{pid:<10} {t}")

    # ── DOM audit ──────────────────────────────────────────
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.click("#companion-toggle")
        page.wait_for_timeout(800)

        markers = page.evaluate(
            """
          () => Array.from(document.querySelectorAll('.cr-folio-marker')).map(m => {
            const cs = getComputedStyle(m);
            return {
              authority: m.dataset.authority,
              kind: m.dataset.kind,
              borderStyle: cs.borderStyle,
              ariaLabel: m.getAttribute('aria-label'),
            };
          })
        """
        )
        print(f"\n22 markers in DOM:")
        for m in markers:
            print(f"  [{m['authority']:<10}] {m['kind']:<18} border={m['borderStyle']:<7}")
            print(f"             aria: {m['ariaLabel'][:80]}")

        # Verify visual differentiation: border-style per authority
        styles_by_auth = {}
        for m in markers:
            styles_by_auth.setdefault(m['authority'], set()).add(m['borderStyle'])
        print(f"\nBorder styles per authority class:")
        for auth, styles in styles_by_auth.items():
            print(f"  {auth:<10} → {styles}")
        assert "solid" in styles_by_auth.get("primary", set())
        assert "dashed" in styles_by_auth.get("secondary", set())
        assert "dotted" in styles_by_auth.get("tertiary", set())
        print("✓ Distinct border style per authority class")

        # Hover one of each authority class and capture
        page.screenshot(path="reports/v29_markers.png")

        # Hover a PRIMARY marker (Doré plate)
        page.hover('.cr-folio-marker[data-authority="primary"]')
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v29_plaque_primary.png")

        # Hover a SECONDARY marker
        page.hover('.cr-folio-marker[data-authority="secondary"]')
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v29_plaque_secondary.png")

        # Hover a TERTIARY marker
        page.hover('.cr-folio-marker[data-authority="tertiary"]')
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v29_plaque_tertiary.png")

        # Click a TERTIARY marker → chamber should show provenance header
        page.mouse.move(20, 20)
        page.wait_for_timeout(200)
        page.click('.cr-folio-marker[data-authority="tertiary"]')
        page.wait_for_timeout(700)
        chamber = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf');
            const provHdr = leaf?.querySelector('.folio-leaf-provenance');
            return {
              hasProvenance: !!provHdr,
              authority: leaf?.dataset.authority,
              hdrText: provHdr?.textContent?.slice(0, 200),
            };
          }
        """
        )
        print(f"\nChamber (tertiary): hasProvenance={chamber['hasProvenance']}  authority={chamber['authority']}")
        print(f"  header text: {chamber['hdrText']}")
        assert chamber['hasProvenance']
        page.screenshot(path="reports/v29_chamber_tertiary.png")

        page.mouse.click(50, 50)
        page.wait_for_timeout(500)

        # Click a PRIMARY non-plate (manuscript witness)
        # Find marker by aria-label
        page.evaluate(
            """
          () => {
            const m = Array.from(document.querySelectorAll('.cr-folio-marker'))
              .find(x => x.dataset.authority === 'primary' && x.dataset.kind === 'manuscript');
            if (m) m.click();
          }
        """
        )
        page.wait_for_timeout(700)
        chamber2 = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf');
            const provHdr = leaf?.querySelector('.folio-leaf-provenance');
            return {
              hasProvenance: !!provHdr,
              authority: leaf?.dataset.authority,
              hdrText: provHdr?.textContent?.slice(0, 200),
            };
          }
        """
        )
        print(f"\nChamber (primary manuscript): hasProvenance={chamber2['hasProvenance']}")
        print(f"  header text: {chamber2['hdrText']}")
        page.screenshot(path="reports/v29_chamber_primary.png")

        b.close()
    print("\nALL CHECKS COMPLETE")


if __name__ == "__main__":
    main()
