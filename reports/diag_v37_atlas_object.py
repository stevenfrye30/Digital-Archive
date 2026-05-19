"""v37 — Atlas Object Field transition (conceptual layer).

Verifies the cosmology chamber now opens with a quiet object
rubric (siglum + class + civilizations) and closes with an
"Anchorings" list. Atmosphere preserved; no dashboard chrome.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent


def main():
    # ── Data-layer assertion: gen1-cosmology-firmament carries
    # the atlas_object metadata block. ───────────────────────────
    with open(ROOT / "data/bible_kjv.json", encoding="utf-8") as f:
        data = json.load(f)
    rec = next(r for r in data["genealogy"]
               if r["id"] == "gen1-cosmology-firmament")
    ao = rec.get("atlas_object")
    assert ao, "atlas_object missing on gen1-cosmology-firmament"
    print("DATA — atlas_object on gen1-cosmology-firmament:")
    print(f"  id:       {ao['id']}")
    print(f"  class:    {ao['class']}")
    print(f"  siglum:   {ao['siglum']}")
    print(f"  civilizations: {ao['civilizations']}")
    print(f"  anchorings ({len(ao['anchorings'])}):")
    for a in ao["anchorings"]:
        ext = " [external]" if a.get("external") else ""
        print(f"    · {a['ref']}{ext}")
    print(f"  linked Atlas Objects: {ao['linked']}")

    assert ao["siglum"] == "AO · 001"
    assert ao["class"] == "cosmological-motif"
    assert len(ao["anchorings"]) == 5
    assert any(a.get("external") for a in ao["anchorings"])
    print("OK — data layer carries Atlas Object identity\n")

    # ── Chamber renders the new pieces ──────────────────────────
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
        page.click("#companion-toggle")
        page.wait_for_timeout(700)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        page.evaluate("_openFolioObject('gen1-cosmology-firmament')")
        page.wait_for_timeout(900)

        snap = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.cosmology-chamber');
            if (!leaf) return null;
            const rubric = leaf.querySelector('.cc-atlas-object-rubric');
            const sig = rubric ? rubric.querySelector('.cc-aor-siglum') : null;
            const cls = rubric ? rubric.querySelector('.cc-aor-class') : null;
            const civ = rubric ? rubric.querySelector('.cc-aor-civilizations') : null;
            const anchorings = leaf.querySelector('.cc-anchorings');
            const items = anchorings
              ? Array.from(anchorings.querySelectorAll('.cc-anchoring')).map(li => ({
                  ref: li.querySelector('.cc-anchoring-ref')?.textContent,
                  note: li.querySelector('.cc-anchoring-note')?.textContent,
                  external: li.classList.contains('cc-anchoring-external'),
                  here: li.classList.contains('cc-anchoring-here'),
                }))
              : null;
            const sectionHeads = Array.from(
              leaf.querySelectorAll('.cc-section-heading .cc-section-title')
            ).map(el => el.textContent);
            return {
              hasRubric: !!rubric,
              siglum: sig?.textContent,
              klass: cls?.textContent,
              civilizations: civ?.textContent,
              rubricRect: rubric ? rubric.getBoundingClientRect().toJSON() : null,
              anchoringsCount: items ? items.length : 0,
              items,
              sectionHeads,
            };
          }
        """
        )
        assert snap, "chamber not rendered"
        print("CHAMBER — rendered Atlas Object pieces:")
        print(f"  has rubric: {snap['hasRubric']}")
        print(f"  siglum:   {snap['siglum']!r}")
        print(f"  class:    {snap['klass']!r}")
        print(f"  civs:     {snap['civilizations']!r}")
        print(f"  section heads: {snap['sectionHeads']}")
        print(f"  anchorings ({snap['anchoringsCount']}):")
        for it in snap["items"] or []:
            mark = []
            if it["here"]:     mark.append("HERE")
            if it["external"]: mark.append("EXT")
            mtag = " [" + ",".join(mark) + "]" if mark else ""
            print(f"    · {it['ref']}{mtag} — {it['note']}")

        assert snap["hasRubric"]
        assert snap["siglum"] == "AO · 001"
        assert "cosmological motif" in (snap["klass"] or "")
        assert "Israel" in (snap["civilizations"] or "")
        assert snap["anchoringsCount"] == 5
        # Section heads now include "Anchorings"
        assert "Anchorings" in snap["sectionHeads"], snap["sectionHeads"]
        # The current verse (gen.1.6) should be marked "here"
        here_items = [it for it in snap["items"] if it["here"]]
        assert len(here_items) == 1, here_items
        assert "Genesis 1:6" in here_items[0]["ref"], here_items[0]["ref"]
        # External text (Enūma Eliš) is in the list and flagged
        ext_items = [it for it in snap["items"] if it["external"]]
        assert any("Enūma Eliš" in (it["ref"] or "") for it in ext_items)
        print("\nOK — chamber surfaces siglum + anchorings + 'here' marker")

        # Visual atmosphere check — the rubric font is small,
        # italic, small-caps; not a UI badge.
        rubric_style = page.evaluate(
            """
          () => {
            const r = document.querySelector('.cc-atlas-object-rubric');
            const cs = getComputedStyle(r);
            return {
              fontStyle: cs.fontStyle,
              fontVariant: cs.fontVariant,
              fontSize: cs.fontSize,
              letterSpacing: cs.letterSpacing,
              borderBottomStyle: cs.borderBottomStyle,
              color: cs.color,
            };
          }
        """
        )
        print(f"\nRUBRIC visual register: {rubric_style}")
        assert rubric_style["fontStyle"] == "italic"
        assert "small-caps" in rubric_style["fontVariant"]
        # Hairline dotted rule beneath
        assert rubric_style["borderBottomStyle"] == "dotted"
        print("OK — rubric uses italic small-caps + hairline dotted rule")

        # Screenshots — chamber head and anchorings section
        page.evaluate("document.getElementById('object-viewer').scrollTop = 0;")
        page.wait_for_timeout(300)
        page.screenshot(path="reports/v37_chamber_head.png")
        page.evaluate("""
          () => {
            const a = document.querySelector('.cc-anchorings');
            if (a) a.scrollIntoView({block: 'center'});
          }
        """)
        page.wait_for_timeout(300)
        page.screenshot(path="reports/v37_anchorings.png")

        b.close()
    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
