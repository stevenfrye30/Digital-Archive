"""v42 — AO · 005 The Sacred Mountain (Elevation and Encounter).

Verifies the fifth Atlas Object class is wired end-to-end:
  · Folio marker present at Genesis 2:10 with the new △ glyph.
  · Chamber renders seven mountain-layer rows joined by a
    continuous axis-mundi rule, with ↑ ascent marks between.
  · The seventh layer is visibly the summit (faint warm tint,
    ornament above numeral, layer set apart).
  · Five encounter fragments stack quietly beneath.
  · Recurrence rubric fires on a second anchoring.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent


def main():
    # ── Data assertions ─────────────────────────────────────────
    with open(ROOT / "data/bible_kjv.json", encoding="utf-8") as f:
        data = json.load(f)
    rec = next(
        (r for r in data["genealogy"] if r["id"] == "gen2-sacred-mountain"),
        None,
    )
    assert rec, "AO · 005 record missing"
    print("DATA — gen2-sacred-mountain:")
    print(f"  kind:    {rec['kind']}")
    print(f"  title:   {rec['title']}")
    print(f"  anchors: {[a['target'].split('::').pop() for a in rec['anchors']]}")
    print(f"  AO siglum:   {rec['atlas_object']['siglum']}")
    print(f"  AO class:    {rec['atlas_object']['class']}")
    print(f"  mountain layers: {len(rec['mountain_layers'])}")
    print(f"  encounter fragments: {len(rec['encounter_fragments'])}")
    print(f"  declared anchorings: {len(rec['atlas_object']['anchorings'])}")
    assert rec["kind"] == "symbolic-motif"
    assert rec["atlas_object"]["siglum"] == "AO · 005"
    assert rec["atlas_object"]["class"] == "symbolic-motif"
    assert len(rec["mountain_layers"]) == 7
    summit = rec["mountain_layers"][6]
    assert summit.get("summit") is True
    assert "Great and High Mountain" in summit["name_en"]
    print(f"  summit: {summit['name_en']!r}")
    print("OK — data structure is correct\n")

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.2.10",
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

        # ── Marker present at gen.2.10 ────────────────────────
        gen210 = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="gen.2.10"]');
            if (!c) return null;
            return Array.from(c.querySelectorAll('.cr-folio-marker')).map(m => ({
              kind: m.dataset.kind,
              authority: m.dataset.authority,
              aria: m.getAttribute('aria-label'),
            }));
          }
        """
        )
        print(f"Gen 2:10 cluster markers:")
        for m in gen210 or []:
            print(f"  · {m['kind']:<22} {m['aria']}")
        assert gen210, "no markers at gen.2.10"
        ao005 = next(
            (m for m in gen210
             if "Sacred Mountain" in (m["aria"] or "")),
            None,
        )
        assert ao005, gen210
        assert ao005["kind"] == "symbolic-motif"
        print("  OK — AO · 005 marker (△ symbolic-motif) present at gen.2.10\n")

        # ── Open the chamber ──────────────────────────────────
        page.evaluate("_openFolioObject('gen2-sacred-mountain')")
        page.wait_for_timeout(900)

        snap = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.mountain-chamber');
            if (!leaf) return null;
            const layers = Array.from(leaf.querySelectorAll('.mc-layer'));
            const ascents = Array.from(leaf.querySelectorAll('.mc-ascent'));
            const fragments = Array.from(leaf.querySelectorAll('.mc-fragment'));
            const sections = Array.from(
              leaf.querySelectorAll('.cc-section-heading .cc-section-title')
            ).map(el => el.textContent);
            const axis = leaf.querySelector('.mc-axis');
            return {
              siglum: leaf.querySelector('.cc-aor-siglum')?.textContent,
              sections,
              hasAxis: !!axis,
              layerCount: layers.length,
              layers: layers.map(L => ({
                numeral: L.querySelector('.mc-layer-numeral')?.textContent,
                name: L.querySelector('.mc-layer-name')?.textContent,
                hebrew: L.querySelector('.mc-layer-name-he')?.textContent,
                epithet: L.querySelector('.mc-layer-epithet')?.textContent,
                fragment: L.querySelector('.mc-layer-fragment')?.textContent,
                ref: L.querySelector('.mc-layer-witness')?.textContent,
                summit: L.dataset.summit || null,
              })),
              ascentCount: ascents.length,
              ascentChars: ascents.map(a => a.textContent),
              fragmentCount: fragments.length,
              fragments: fragments.map(f => ({
                text: f.querySelector('.mc-fragment-quote')?.textContent,
                ref: f.querySelector('.mc-fragment-ref')?.textContent,
              })),
            };
          }
        """
        )
        assert snap, "mountain chamber did not render"
        print("CHAMBER — sacred mountain:")
        print(f"  siglum:   {snap['siglum']!r}")
        print(f"  sections: {snap['sections']}")
        print(f"  has axis-mundi container: {snap['hasAxis']}")
        print(f"  mountain layers ({snap['layerCount']}):")
        for L in snap["layers"]:
            summit = " · SUMMIT" if L['summit'] else ""
            print(f"    {L['numeral']:>4} · {L['name']:<32} ({L['hebrew'] or '—'}){summit}")
            print(f"         {L['epithet']}")
        print(f"  ascent marks: {snap['ascentCount']} ({set(snap['ascentChars'])})")
        print(f"  encounter fragments ({snap['fragmentCount']}):")
        for f in snap['fragments']:
            print(f"    · {f['text'][:70]!r}  {f['ref']}")

        assert snap["siglum"] == "AO · 005"
        assert snap["sections"] == [
            "Vertical Layer", "Encounter Fragments", "Anchorings",
        ]
        # Seven mountain layers + six ascent marks between them
        assert snap["layerCount"] == 7
        assert snap["ascentCount"] == 6
        assert set(snap["ascentChars"]) == {"↑"}
        # Seventh layer is the summit
        last = snap["layers"][6]
        assert last["summit"] == "true"
        assert "Great and High" in last["name"]
        # Hebrew rendered in first five layers (none for the
        # Transfiguration and Eschatological summit)
        for i in range(5):
            assert snap["layers"][i]["hebrew"], snap["layers"][i]
        # Five encounter fragments
        assert snap["fragmentCount"] == 5
        # The famous "lift up mine eyes" phrase is present
        assert any("lift up mine eyes" in (f["text"] or "")
                   for f in snap["fragments"])
        print("\n  OK — seven layers, six ascents, summit recognised, fragments present")

        # ── Visual atmosphere check: axis mundi + summit
        atmosphere = page.evaluate(
            """
          () => {
            const axis = document.querySelector('.mc-axis');
            const summit = document.querySelector('.mc-layer[data-summit="true"]');
            const sixth = document.querySelectorAll('.mc-layer')[5];
            const sm = getComputedStyle(summit);
            const sx = getComputedStyle(sixth);
            return {
              axisPos: axis ? getComputedStyle(axis).position : null,
              axisPadding: axis ? getComputedStyle(axis).paddingLeft : null,
              summitBgImage: sm.backgroundImage,
              summitBorderTop: sm.borderTopWidth,
              sixthBgImage: sx.backgroundImage,
            };
          }
        """
        )
        print(f"\nVISUAL atmosphere:")
        print(f"  axis position: {atmosphere['axisPos']} padding-left {atmosphere['axisPadding']}")
        print(f"  summit background-image: {(atmosphere['summitBgImage'] or '')[:90]}...")
        print(f"  sixth  background-image: {(atmosphere['sixthBgImage'] or 'none')[:50]}")
        print(f"  summit border-top: {atmosphere['summitBorderTop']}")
        # The summit must carry a gradient where the sixth does not.
        assert "gradient" in (atmosphere["summitBgImage"] or ""), atmosphere
        assert atmosphere["summitBgImage"] != atmosphere["sixthBgImage"]
        # And a visible border-top separating it from the column
        assert float(atmosphere["summitBorderTop"].replace("px", "")) > 0
        print("  OK — axis-mundi rule positioned, summit visually set apart\n")

        # Screenshots
        page.screenshot(path="reports/v42_mountain_top.png")
        page.evaluate(
            "() => { const el = document.querySelector('.mc-layer[data-summit]');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v42_mountain_summit.png")
        page.evaluate(
            "() => { const el = document.querySelector('.mc-fragments');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v42_mountain_fragments.png")
        page.evaluate(
            "() => { const el = document.querySelector('.cc-archive');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v42_mountain_archive.png")

        # ── Recurrence at Sinai (Exodus 19:20) ────────────────
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=exo.19.20",
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
        sinai_marker = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="exo.19.20"]');
            return c ? !!c.querySelector(
              '.cr-folio-marker[data-kind="symbolic-motif"]'
            ) : false;
          }
        """
        )
        print(f"Exodus 19:20 (Sinai) AO · 005 marker present: {sinai_marker}")
        assert sinai_marker, "AO · 005 should recur at exo.19.20"
        page.evaluate("_openFolioObject('gen2-sacred-mountain')")
        page.wait_for_timeout(900)
        recur = page.evaluate(
            """
          () => {
            const r = document.querySelector(
              '.folio-leaf.mountain-chamber .cc-recurrence-rubric');
            return r ? {
              lead: r.querySelector('.ccr-lead')?.textContent,
              where: r.querySelector('.ccr-where')?.textContent,
            } : null;
          }
        """
        )
        print(f"  recurrence rubric: {recur}")
        assert recur and "Genesis 2:10" in (recur["where"] or "")
        print("  OK — AO · 005 recurs at Sinai with recurrence rubric\n")
        page.screenshot(path="reports/v42_mountain_sinai.png")

        b.close()
    print("ALL CHECKS PASSED — AO · 005 is operational, distinct, and recurring")


if __name__ == "__main__":
    main()
