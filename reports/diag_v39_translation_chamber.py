"""v39 — AO · 002 Firmament Translation Tradition.

Verifies that the second Atlas Object class is wired end-to-end:
  · A folio marker appears at Genesis 1:6 alongside AO · 001.
  · The chamber renders with a materially different rhythm:
    witness slips, semantic-shift notes, lineage strip.
  · Provenance and encounter-memory infrastructure are reused.
  · The two Atlas Objects coexist on the same verse without
    visual collision.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent


def main():
    # ── Data: AO · 002 record exists with the expected shape
    with open(ROOT / "data/bible_kjv.json", encoding="utf-8") as f:
        data = json.load(f)
    rec = next(
        (r for r in data["genealogy"]
         if r["id"] == "gen1-firmament-translation-tradition"),
        None,
    )
    assert rec, "AO · 002 record missing"
    print("DATA — gen1-firmament-translation-tradition:")
    print(f"  kind:     {rec['kind']}")
    print(f"  title:    {rec['title']}")
    print(f"  anchors:  {[a['target'].split('::').pop() for a in rec['anchors']]}")
    print(f"  fragments:    {len(rec['witness_fragments'])}")
    print(f"  shift notes:  {len(rec['semantic_shift'])}")
    print(f"  lineage stops:{len(rec['lineage_stops'])}")
    print(f"  AO siglum: {rec['atlas_object']['siglum']}")
    print(f"  AO class:  {rec['atlas_object']['class']}")
    assert rec["kind"] == "translation-tradition"
    assert rec["atlas_object"]["siglum"] == "AO · 002"
    assert rec["atlas_object"]["class"] == "translation-tradition"
    assert len(rec["witness_fragments"]) == 4
    assert len(rec["semantic_shift"]) == 4
    assert len(rec["lineage_stops"]) == 4

    # Confirm AO · 001 still anchors on gen.1.6 (coexistence)
    cosmology = next(
        r for r in data["genealogy"] if r["id"] == "gen1-cosmology-firmament"
    )
    anchors_cos = [a["target"].split("::").pop() for a in cosmology["anchors"]]
    assert "gen.1.6" in anchors_cos
    print(f"\n  AO · 001 still anchors at: {anchors_cos}")
    print("  OK — two Atlas Objects coexist on Genesis 1:6\n")

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
        page.wait_for_timeout(600)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)

        # ── Two markers at gen.1.6: cosmology + translation-tradition
        gen16_cluster = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="gen.1.6"]');
            if (!c) return null;
            return Array.from(c.querySelectorAll('.cr-folio-marker')).map(m => ({
              kind: m.dataset.kind,
              authority: m.dataset.authority,
              aria: m.getAttribute('aria-label'),
            }));
          }
        """
        )
        print(f"gen.1.6 cluster markers:")
        for m in gen16_cluster or []:
            print(f"  · {m['kind']:<22} {m['authority']}  ::  {m['aria']}")
        assert gen16_cluster
        kinds_here = [m["kind"] for m in gen16_cluster]
        assert "cosmology" in kinds_here, kinds_here
        assert "translation-tradition" in kinds_here, kinds_here
        print("  OK — both AO markers present at gen.1.6\n")

        # ── Open the translation-tradition chamber by id
        opened = page.evaluate(
            "() => { _openFolioObject('gen1-firmament-translation-tradition'); return true; }"
        )
        page.wait_for_timeout(900)

        state = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.translation-chamber');
            if (!leaf) return null;
            const slips = Array.from(leaf.querySelectorAll('.tc-witness'));
            const shift = Array.from(leaf.querySelectorAll('.tc-shift-item'));
            const lineage = Array.from(leaf.querySelectorAll('.tc-lineage-stop'));
            const conn = Array.from(leaf.querySelectorAll('.tc-lineage-connector'));
            const sections = Array.from(
              leaf.querySelectorAll('.cc-section-heading .cc-section-title')
            ).map(el => el.textContent);
            const aor = leaf.querySelector('.cc-atlas-object-rubric .cc-aor-siglum');
            const archive = leaf.querySelector('.cc-archive');
            return {
              hasRubric: !!aor,
              siglum: aor?.textContent,
              authority: leaf.dataset.authority,
              kind: leaf.dataset.kind,
              sections,
              slips: slips.map(s => ({
                lang: s.dataset.lang,
                tradition: s.querySelector('.tc-witness-tradition')?.textContent,
                witnessId: s.querySelector('.tc-witness-id')?.textContent,
                script: s.querySelector('.tc-witness-script')?.textContent,
                term: s.querySelector('.tc-witness-term')?.textContent,
                translit: s.querySelector('.tc-witness-translit')?.textContent,
              })),
              shiftHeads: shift.map(s =>
                s.querySelector('.tc-shift-head')?.textContent),
              lineageStops: lineage.map(s => ({
                lang: s.dataset.lang,
                tradition: s.querySelector('.tc-lineage-tradition')?.textContent,
                term: s.querySelector('.tc-lineage-term')?.textContent,
              })),
              connectors: conn.length,
              hasArchive: !!archive,
              archiveRubric: archive?.querySelector('.cc-archive-rubric')?.textContent,
            };
          }
        """
        )
        assert state, "translation chamber did not render"
        print("CHAMBER — translation-tradition:")
        print(f"  kind:     {state['kind']}")
        print(f"  authority:{state['authority']}")
        print(f"  rubric siglum: {state['siglum']!r}")
        print(f"  sections: {state['sections']}")
        print(f"  slips ({len(state['slips'])}):")
        for s in state['slips']:
            print(f"    · {s['tradition']:<26} ({s['lang']}) term={s['term']!r}")
            print(f"        script: {s['script'][:60]!r}")
        print(f"  shift notes ({len(state['shiftHeads'])}):")
        for h in state['shiftHeads']:
            print(f"    · {h}")
        print(f"  lineage stops ({len(state['lineageStops'])}):")
        for st in state['lineageStops']:
            print(f"    · {st['tradition']:<26} term={st['term']!r}")
        print(f"  connectors between stops: {state['connectors']}")
        print(f"  archive panel: {state['hasArchive']} rubric={state['archiveRubric']}")

        assert state["kind"] == "translation-tradition"
        assert state["siglum"] == "AO · 002"
        assert state["sections"] == [
            "Witness Fragments", "Semantic Shift",
            "Transmission Lineage", "Anchorings",
        ], state["sections"]
        # Four witness slips, one per language
        assert [s["lang"] for s in state["slips"]] == ["he", "el", "la", "en"]
        # The Hebrew slip carries the focus term rāqîaʿ
        he = next(s for s in state["slips"] if s["lang"] == "he")
        assert "רָקִיעַ" in (he["term"] or ""), he
        # The Greek slip carries stereōma
        el = next(s for s in state["slips"] if s["lang"] == "el")
        assert "στερέωμα" in (el["term"] or ""), el
        # Lineage chain: 4 stops + 3 connectors
        assert len(state["lineageStops"]) == 4
        assert state["connectors"] == 3
        # Archive panel reused
        assert state["hasArchive"]
        assert "Tertiary" in (state["archiveRubric"] or "")
        print("\nOK — chamber renders all witness/lineage/archive structure")

        # ── Atmosphere: Hebrew script font + RTL direction
        hebrew_check = page.evaluate(
            """
          () => {
            const he = document.querySelector(
              '.tc-witness[data-lang="he"] .tc-witness-script');
            const cs = getComputedStyle(he);
            return {
              dir: he.dir,
              align: cs.textAlign,
              family: cs.fontFamily,
              fontSize: cs.fontSize,
            };
          }
        """
        )
        print(f"\nHEBREW slip atmosphere: {hebrew_check}")
        assert hebrew_check["dir"] == "rtl"
        # Witness script font-size is materially larger than gloss
        sizes = page.evaluate(
            """
          () => {
            const s = document.querySelector('.tc-witness-script');
            const g = document.querySelector('.tc-witness-gloss');
            return {
              script: parseFloat(getComputedStyle(s).fontSize),
              gloss:  parseFloat(getComputedStyle(g).fontSize),
            };
          }
        """
        )
        print(f"  witness script vs gloss: {sizes}")
        assert sizes["script"] > sizes["gloss"], (
            "witness script should be larger than its gloss"
        )
        print("  OK — witness material visually dominates archive prose\n")

        # Screenshots
        page.screenshot(path="reports/v39_translation_top.png")
        page.evaluate(
            "() => { const el = document.querySelector('.tc-lineage'); "
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v39_translation_lineage.png")
        page.evaluate(
            "() => { const el = document.querySelector('.cc-archive'); "
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v39_translation_archive.png")

        # ── Recurrence: navigate to Ezekiel 1 and confirm the same
        # AO · 002 marker appears there too, with the recurrence
        # rubric firing in the chamber.
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=eze.1.22",
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
        eze_marker = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="eze.1.22"]');
            if (!c) return null;
            const m = c.querySelector(
              '.cr-folio-marker[data-kind="translation-tradition"]');
            return m ? { aria: m.getAttribute('aria-label') } : null;
          }
        """
        )
        print(f"EZEKIEL 1:22 marker: {eze_marker}")
        assert eze_marker, "AO · 002 should recur at Ezekiel 1:22"
        page.evaluate("_openFolioObject('gen1-firmament-translation-tradition')")
        page.wait_for_timeout(900)
        recur = page.evaluate(
            """
          () => {
            const r = document.querySelector(
              '.folio-leaf.translation-chamber .cc-recurrence-rubric');
            return r ? {
              lead: r.querySelector('.ccr-lead')?.textContent,
              where: r.querySelector('.ccr-where')?.textContent,
            } : null;
          }
        """
        )
        print(f"  recurrence rubric: {recur}")
        assert recur, "recurrence rubric should fire on second anchoring"
        assert "Genesis 1:6" in (recur["where"] or "")
        print("  OK — AO · 002 recurs at Ezekiel 1:22 with recurrence rubric")
        page.screenshot(path="reports/v39_translation_ezekiel.png")

        b.close()
    print("\nALL CHECKS PASSED — AO · 002 is operational, distinct, and recurring")


if __name__ == "__main__":
    main()
