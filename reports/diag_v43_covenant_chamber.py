"""v43 — AO · 006 The Covenant Formula (I Will Be Your God).

Verifies the sixth Atlas Object class is wired end-to-end:
  · Folio marker present at Genesis 17:7 with the new ⊟ glyph.
  · Chamber renders seven bipartite formula occurrences
    (declaration · pivot · response · full quote), with the
    seventh (apocalyptic consummation) visibly set apart.
  · Five witness/seal clauses stack beneath.
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
        (r for r in data["genealogy"] if r["id"] == "gen17-covenant-formula"),
        None,
    )
    assert rec, "AO · 006 record missing"
    print("DATA — gen17-covenant-formula:")
    print(f"  kind:    {rec['kind']}")
    print(f"  title:   {rec['title']}")
    print(f"  anchors: {[a['target'].split('::').pop() for a in rec['anchors']]}")
    print(f"  AO siglum:   {rec['atlas_object']['siglum']}")
    print(f"  AO class:    {rec['atlas_object']['class']}")
    print(f"  formula occurrences: {len(rec['formula_occurrences'])}")
    print(f"  witness clauses:     {len(rec['witness_clauses'])}")
    assert rec["kind"] == "covenant-formula"
    assert rec["atlas_object"]["siglum"] == "AO · 006"
    assert rec["atlas_object"]["class"] == "covenant-formula"
    assert len(rec["formula_occurrences"]) == 7
    seventh = rec["formula_occurrences"][6]
    assert seventh.get("consummation") is True
    assert "Apocalyptic" in seventh["era"]
    print(f"  consummation (vii): {seventh['era']} · {seventh['ref']}")
    print("OK — data structure is correct\n")

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.17.7",
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

        # ── Marker present at gen.17.7 ────────────────────────
        gen177 = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="gen.17.7"]');
            if (!c) return null;
            return Array.from(c.querySelectorAll('.cr-folio-marker')).map(m => ({
              kind: m.dataset.kind,
              aria: m.getAttribute('aria-label'),
            }));
          }
        """
        )
        print(f"Gen 17:7 cluster markers:")
        for m in gen177 or []:
            print(f"  · {m['kind']:<22} {m['aria']}")
        assert gen177
        ao006 = next(
            (m for m in gen177
             if "Covenant Formula" in (m["aria"] or "")),
            None,
        )
        assert ao006, gen177
        assert ao006["kind"] == "covenant-formula"
        print("  OK — AO · 006 marker (⊟ covenant-formula) present at gen.17.7\n")

        # ── Open the chamber ──────────────────────────────────
        page.evaluate("_openFolioObject('gen17-covenant-formula')")
        page.wait_for_timeout(900)

        snap = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.covenant-chamber');
            if (!leaf) return null;
            const occs = Array.from(leaf.querySelectorAll('.vc-occurrence'));
            const witnesses = Array.from(leaf.querySelectorAll('.vc-witness'));
            const sections = Array.from(
              leaf.querySelectorAll('.cc-section-heading .cc-section-title')
            ).map(el => el.textContent);
            return {
              siglum: leaf.querySelector('.cc-aor-siglum')?.textContent,
              sections,
              occurrenceCount: occs.length,
              occurrences: occs.map(O => ({
                consummation: O.dataset.consummation || null,
                numeral: O.querySelector('.vc-occurrence-numeral')?.textContent,
                era: O.querySelector('.vc-occurrence-era')?.textContent,
                ref: O.querySelector('.vc-occurrence-ref')?.textContent,
                godSide: O.querySelector('.vc-god-side')?.textContent,
                peopleSide: O.querySelector('.vc-people-side')?.textContent,
                pivot: O.querySelector('.vc-pivot')?.textContent,
                quoteLen: (O.querySelector('.vc-occurrence-quote')?.textContent || '').length,
              })),
              witnessCount: witnesses.length,
              witnesses: witnesses.map(W => ({
                text: W.querySelector('.vc-witness-quote')?.textContent,
                ref: W.querySelector('.vc-witness-ref')?.textContent,
              })),
            };
          }
        """
        )
        assert snap, "covenant chamber did not render"
        print("CHAMBER — covenant:")
        print(f"  siglum:   {snap['siglum']!r}")
        print(f"  sections: {snap['sections']}")
        print(f"  formula occurrences ({snap['occurrenceCount']}):")
        for o in snap['occurrences']:
            tag = " · CONSUMMATION" if o['consummation'] else ""
            print(f"    {o['numeral']:>4} · {o['era']}  · {o['ref']}{tag}")
            print(f"         GOD:    {o['godSide']!r}")
            print(f"         pivot:  {o['pivot']!r}")
            print(f"         PEOPLE: {o['peopleSide']!r}")
        print(f"  witness clauses ({snap['witnessCount']}):")
        for w in snap['witnesses']:
            print(f"    · {(w['text'] or '')[:70]!r}  {w['ref']}")

        assert snap["siglum"] == "AO · 006"
        assert snap["sections"] == [
            "Covenant Formula", "Witness and Seal", "Anchorings",
        ]
        # Seven bipartite occurrences
        assert snap["occurrenceCount"] == 7
        # Every occurrence has both sides + pivot + full quote
        for o in snap["occurrences"]:
            assert o["godSide"], o
            assert o["peopleSide"], o
            assert o["pivot"] == "·"
            assert o["quoteLen"] > 30
        # Seventh occurrence is the consummation
        last = snap["occurrences"][6]
        assert last["consummation"] == "true"
        assert "Apocalyptic" in (last["era"] or "")
        # Five witness clauses
        assert snap["witnessCount"] == 5
        # The "one voice" answer is there
        assert any("one voice" in (w["text"] or "") for w in snap["witnesses"])
        print("\n  OK — seven bipartite occurrences, consummation set apart, witnesses present")

        # ── Visual atmosphere check: consummation differentiation
        atmosphere = page.evaluate(
            """
          () => {
            const cons = document.querySelector('.vc-occurrence[data-consummation="true"]');
            const sixth = document.querySelectorAll('.vc-occurrence')[5];
            const pivot = document.querySelector('.vc-pivot');
            return {
              consBgImage: getComputedStyle(cons).backgroundImage,
              sixthBgImage: getComputedStyle(sixth).backgroundImage,
              consBorderTop: getComputedStyle(cons).borderTopColor,
              pivotAlign: getComputedStyle(pivot.parentElement).textAlign,
              godSideAlign: getComputedStyle(
                document.querySelector('.vc-god-side')
              ).textAlign,
              godSideFont: getComputedStyle(
                document.querySelector('.vc-god-side')
              ).fontStyle,
            };
          }
        """
        )
        print(f"\nVISUAL atmosphere:")
        print(f"  consummation bg-image: {(atmosphere['consBgImage'] or '')[:80]}...")
        print(f"  sixth        bg-image: {atmosphere['sixthBgImage'] or 'none'}")
        print(f"  bipartite align: {atmosphere['pivotAlign']}")
        print(f"  god-side font:   {atmosphere['godSideFont']}")
        assert "gradient" in (atmosphere["consBgImage"] or "")
        assert atmosphere["consBgImage"] != atmosphere["sixthBgImage"]
        assert atmosphere["pivotAlign"] == "center"
        assert atmosphere["godSideFont"] == "italic"
        print("  OK — consummation set apart with parchment gradient; bipartite centered italic\n")

        # Screenshots
        page.screenshot(path="reports/v43_covenant_top.png")
        page.evaluate(
            "() => { const el = document.querySelector('.vc-occurrence[data-consummation]');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v43_covenant_consummation.png")
        page.evaluate(
            "() => { const el = document.querySelector('.vc-witnesses');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v43_covenant_witnesses.png")
        page.evaluate(
            "() => { const el = document.querySelector('.cc-archive');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v43_covenant_archive.png")

        # ── Recurrence at Jeremiah 31:33 (the new covenant) ───
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=jer.31.33",
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
        jer_marker = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="jer.31.33"]');
            return c ? !!c.querySelector(
              '.cr-folio-marker[data-kind="covenant-formula"]'
            ) : false;
          }
        """
        )
        print(f"Jeremiah 31:33 (new covenant) AO · 006 marker present: {jer_marker}")
        assert jer_marker
        page.evaluate("_openFolioObject('gen17-covenant-formula')")
        page.wait_for_timeout(900)
        recur = page.evaluate(
            """
          () => {
            const r = document.querySelector(
              '.folio-leaf.covenant-chamber .cc-recurrence-rubric');
            return r ? {
              lead: r.querySelector('.ccr-lead')?.textContent,
              where: r.querySelector('.ccr-where')?.textContent,
            } : null;
          }
        """
        )
        print(f"  recurrence rubric: {recur}")
        assert recur and "Genesis 17:7" in (recur["where"] or "")
        print("  OK — AO · 006 recurs at Jeremiah 31:33 with recurrence rubric\n")
        page.screenshot(path="reports/v43_covenant_jeremiah.png")

        b.close()
    print("ALL CHECKS PASSED — AO · 006 is operational, distinct, and recurring")


if __name__ == "__main__":
    main()
