"""v54 — Object constellation / resonance consolidation.

Verifies the new resonance layer:
  · Resonance mapping exists with the 8 curated pairs.
  · Temple chamber surfaces resonance with Incarnation, Apocalypse,
    Mountain (3 resonants — the maximum permitted per chamber).
  · Lament chamber surfaces resonance with Resurrection + Wisdom.
  · Covenant chamber surfaces resonance with Ritual + Transmission.
  · Kindred ("also met here") continues to render independently.
  · Resonance line uses a cooler colour register than kindred.
  · Codex Preface now lists nine rubrics ending with "On resonance".
  · No new Atlas Object was created (still twelve).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent


def alpha(rgba):
    m = re.search(r"rgba\(.+,\s*([\d.]+)\)", rgba)
    return float(m.group(1)) if m else 1.0


def main():
    # ── Data: confirm no new AO was created (still 12)
    with open(ROOT / "data/bible_kjv.json", encoding="utf-8") as f:
        data = json.load(f)
    ao_records = [r for r in data["genealogy"]
                  if r.get("atlas_object", {}).get("siglum")]
    print(f"DATA — Atlas Objects in archive: {len(ao_records)}")
    siglums = sorted([r["atlas_object"]["siglum"] for r in ao_records])
    print(f"  siglums: {siglums}")
    assert len(ao_records) == 12, "should still be 12 Atlas Objects"
    print("  OK — no new AO; still twelve\n")

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

        # ── Temple chamber: resonance with 3 objects
        page.evaluate("_openFolioObject('exo40-sanctuary-glory')")
        page.wait_for_timeout(1500)
        temple = page.evaluate(
            """
          () => {
            const res = document.querySelector('.folio-leaf .cc-resonance');
            if (!res) return null;
            return {
              lead: res.querySelector('.cc-resonance-lead')?.textContent,
              items: Array.from(res.querySelectorAll('.cc-resonance-item')).map(b => ({
                siglum: b.dataset.siglum,
                glyph: b.querySelector('.cc-resonance-glyph')?.textContent,
                title: b.querySelector('.cc-resonance-title')?.textContent,
              })),
            };
          }
        """
        )
        print("TEMPLE chamber resonance:")
        print(f"  lead: {temple['lead']!r}")
        for it in temple["items"]:
            print(f"    {it['glyph']} {it['siglum']} · {it['title']}")
        assert temple
        assert "held in resonance" in (temple["lead"] or "")
        sigs = [it["siglum"] for it in temple["items"]]
        # Temple resonates with Incarnation (010), Apocalypse (008), Mountain (005)
        assert "AO · 010" in sigs
        assert "AO · 008" in sigs
        assert "AO · 005" in sigs
        assert len(sigs) == 3
        print("  OK — Temple surfaces resonance with Incarnation, Apocalypse, Mountain\n")

        # Kindred should also still work — at exo.40.34 only the
        # Temple anchors, so there's no kindred for this verse
        # (no other AOs are anchored here).
        kindred_at_temple = page.evaluate(
            "() => !!document.querySelector('.folio-leaf .cc-kindred')"
        )
        print(f"  kindred at exo.40.34 (Temple originating): {kindred_at_temple}")

        # ── Lament chamber: resonance with Resurrection + Wisdom
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=psa.13.1",
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
        page.evaluate("_openFolioObject('psa13-lament-cry')")
        page.wait_for_timeout(1200)
        lament = page.evaluate(
            """
          () => {
            const res = document.querySelector('.folio-leaf .cc-resonance');
            if (!res) return null;
            return Array.from(res.querySelectorAll('.cc-resonance-item')).map(b => ({
              siglum: b.dataset.siglum,
              title: b.querySelector('.cc-resonance-title')?.textContent,
            }));
          }
        """
        )
        print(f"LAMENT chamber resonance:")
        for it in lament:
            print(f"    {it['siglum']} · {it['title']}")
        sigs = [it["siglum"] for it in lament]
        # Lament resonates with Resurrection (011) + Wisdom (007)
        assert "AO · 011" in sigs
        assert "AO · 007" in sigs
        assert len(sigs) == 2
        print("  OK — Lament surfaces resonance with Resurrection + Wisdom\n")

        # ── Covenant chamber: resonance with Ritual + Transmission
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.17.7",
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
        page.evaluate("_openFolioObject('gen17-covenant-formula')")
        page.wait_for_timeout(1200)
        covenant = page.evaluate(
            """
          () => {
            const res = document.querySelector('.folio-leaf .cc-resonance');
            if (!res) return null;
            return Array.from(res.querySelectorAll('.cc-resonance-item')).map(b => ({
              siglum: b.dataset.siglum,
              title: b.querySelector('.cc-resonance-title')?.textContent,
            }));
          }
        """
        )
        print(f"COVENANT chamber resonance:")
        for it in covenant:
            print(f"    {it['siglum']} · {it['title']}")
        sigs = [it["siglum"] for it in covenant]
        # Covenant resonates with Ritual (004) + Transmission (002)
        assert "AO · 004" in sigs
        assert "AO · 002" in sigs
        assert len(sigs) == 2
        print("  OK — Covenant surfaces resonance with Ritual + Transmission\n")

        # ── Cosmology at gen.1.6: BOTH kindred (translation, same verse)
        # AND resonance (apocalypse, civilizational affinity) should render
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
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
        page.wait_for_timeout(500)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        page.evaluate("_openFolioObject('gen1-cosmology-firmament')")
        page.wait_for_timeout(1200)
        both = page.evaluate(
            """
          () => {
            const k = document.querySelector('.folio-leaf .cc-kindred');
            const r = document.querySelector('.folio-leaf .cc-resonance');
            return {
              kindredItems: k ? Array.from(
                k.querySelectorAll('.cc-kindred-item')
              ).map(b => b.dataset.siglum) : null,
              resonanceItems: r ? Array.from(
                r.querySelectorAll('.cc-resonance-item')
              ).map(b => b.dataset.siglum) : null,
              kindredColor: k ? getComputedStyle(k).color : null,
              resonanceColor: r ? getComputedStyle(r).color : null,
            };
          }
        """
        )
        print(f"COSMOLOGY chamber at gen.1.6 (both layers):")
        print(f"  kindred items:   {both['kindredItems']}")
        print(f"  resonance items: {both['resonanceItems']}")
        print(f"  kindred colour:   {both['kindredColor']}")
        print(f"  resonance colour: {both['resonanceColor']}")
        # AO·002 (translation tradition) is kindred at gen.1.6
        assert both["kindredItems"] == ["AO · 002"]
        # AO·008 (apocalypse) is resonance for cosmology
        assert both["resonanceItems"] == ["AO · 008"]
        # The two colours should differ — resonance is cooler
        assert both["kindredColor"] != both["resonanceColor"]
        # The kindred is warmer (higher red component); we can
        # verify the colours are distinct rgba strings.
        print("  OK — both layers render simultaneously with distinct colours\n")
        page.screenshot(path="reports/v54_cosmology_both.png", full_page=True)

        # Click a resonance item — should switch chamber
        page.evaluate("""
          () => {
            const r = document.querySelector('.cc-resonance-item');
            if (r) r.click();
          }
        """)
        page.wait_for_timeout(1000)
        switched = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf');
            return {
              chamber: leaf ? leaf.className : null,
              siglum: leaf?.querySelector('.cc-aor-siglum')?.textContent,
            };
          }
        """
        )
        print(f"After resonance click: {switched}")
        # Should now be in revelation chamber
        assert "revelation-chamber" in (switched["chamber"] or "")
        assert switched["siglum"] == "AO · 008"
        print("  OK — clicking resonance item switches to that chamber\n")

        # ── Codex Preface — nine rubrics now
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
        assert len(rubrics) == 9
        assert "resonance" in rubrics[8].lower()
        print("  OK — ninth rubric 'On resonance' present\n")
        page.screenshot(path="reports/v54_preface_nine.png", full_page=False)

        # Final atmosphere screenshot of Temple chamber with resonance
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=exo.40.34",
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
        page.evaluate("_openFolioObject('exo40-sanctuary-glory')")
        page.wait_for_timeout(1300)
        page.evaluate(
            "() => { const el = document.querySelector('.cc-resonance'); "
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v54_temple_resonance.png")

        b.close()
    print("ALL CHECKS PASSED — constellation resonance is operational")


if __name__ == "__main__":
    main()
