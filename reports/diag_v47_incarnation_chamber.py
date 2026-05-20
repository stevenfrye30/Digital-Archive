"""v47 — AO · 010 The Word Became Flesh (Tent, Temple, Flesh).

Verifies the tenth Atlas Object class is wired end-to-end:
  · Folio marker present at Exodus 25:8 with the new ⊙ glyph.
  · Chamber renders six indwelling dwelling blocks in a narrow
    centered measure with warm parchment gradient backgrounds.
  · The sixth block (consummation) is the chamber's culminating
    air (warmer gradient, fuller gold rule).
  · Dwelling vocabulary section renders five Hebrew/Greek terms.
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
        (r for r in data["genealogy"] if r["id"] == "joh1-incarnation-dwelling"),
        None,
    )
    assert rec, "AO · 010 record missing"
    print("DATA — joh1-incarnation-dwelling:")
    print(f"  kind:    {rec['kind']}")
    print(f"  title:   {rec['title']}")
    print(f"  anchors: {[a['target'].split('::').pop() for a in rec['anchors']]}")
    print(f"  AO siglum:   {rec['atlas_object']['siglum']}")
    print(f"  AO class:    {rec['atlas_object']['class']}")
    print(f"  indwelling moments:    {len(rec['indwelling_moments'])}")
    print(f"  dwelling vocabulary:   {len(rec['dwelling_vocabulary'])}")
    assert rec["kind"] == "incarnational-presence"
    assert rec["atlas_object"]["siglum"] == "AO · 010"
    assert rec["atlas_object"]["class"] == "incarnational-presence"
    assert len(rec["indwelling_moments"]) == 6
    sixth = rec["indwelling_moments"][5]
    assert sixth.get("consummation") is True
    assert "Revelation 21" in sixth["ref"]
    print(f"  consummation (vi): {sixth['tradition']}")
    print("OK — data structure is correct\n")

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=exo.25.8",
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

        # ── Marker present at exo.25.8 ────────────────────────
        exo258 = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="exo.25.8"]');
            if (!c) return null;
            return Array.from(c.querySelectorAll('.cr-folio-marker')).map(m => ({
              kind: m.dataset.kind,
              aria: m.getAttribute('aria-label'),
            }));
          }
        """
        )
        print(f"Exodus 25:8 cluster markers:")
        for m in exo258 or []:
            print(f"  · {m['kind']:<22} {m['aria']}")
        assert exo258
        ao010 = next(
            (m for m in exo258
             if "Word Became Flesh" in (m["aria"] or "")),
            None,
        )
        assert ao010, exo258
        assert ao010["kind"] == "incarnational-presence"
        print("  OK — AO · 010 marker (⊙ incarnational-presence) present at exo.25.8\n")

        # ── Open the chamber ──────────────────────────────────
        page.evaluate("_openFolioObject('joh1-incarnation-dwelling')")
        page.wait_for_timeout(900)

        snap = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.incarnation-chamber');
            if (!leaf) return null;
            const dwellings = Array.from(leaf.querySelectorAll('.in-dwelling'));
            const terms = Array.from(leaf.querySelectorAll('.in-term-row'));
            const sections = Array.from(
              leaf.querySelectorAll('.cc-section-heading .cc-section-title')
            ).map(el => el.textContent);
            return {
              siglum: leaf.querySelector('.cc-aor-siglum')?.textContent,
              sections,
              dwellingCount: dwellings.length,
              dwellings: dwellings.map(D => ({
                consummation: D.dataset.consummation || null,
                numeral: D.querySelector('.in-dwelling-numeral')?.textContent,
                ref: D.querySelector('.in-dwelling-ref')?.textContent,
                tradition: D.querySelector('.in-dwelling-tradition')?.textContent,
                rubric: D.querySelector('.in-dwelling-rubric')?.textContent,
                hasText: !!D.querySelector('.in-dwelling-text'),
                hasFootnote: !!D.querySelector('.in-dwelling-footnote'),
              })),
              termCount: terms.length,
              terms: terms.map(T => ({
                lang: T.dataset.lang,
                script: T.querySelector('.in-term-script')?.textContent,
                translit: T.querySelector('.in-term-translit')?.textContent,
                gloss: T.querySelector('.in-term-gloss')?.textContent,
              })),
            };
          }
        """
        )
        assert snap, "incarnation chamber did not render"
        print("CHAMBER — incarnation:")
        print(f"  siglum:   {snap['siglum']!r}")
        print(f"  sections: {snap['sections']}")
        print(f"  dwellings ({snap['dwellingCount']}):")
        for D in snap['dwellings']:
            tag = " · CONSUMMATION" if D['consummation'] else ""
            print(f"    {D['numeral']:>4} · {D['ref']:<26} {D['tradition']}{tag}")
            print(f"         rubric:   {D['rubric']!r}")
            print(f"         hasText:  {D['hasText']}  hasFootnote: {D['hasFootnote']}")
        print(f"  vocabulary terms ({snap['termCount']}):")
        for T in snap['terms']:
            print(f"    · ({T['lang']}) {T['script']:<14} {T['translit']:<14} {(T['gloss'] or '')[:60]}")

        assert snap["siglum"] == "AO · 010"
        assert snap["sections"] == [
            "Dwellings", "Dwelling Vocabulary", "Anchorings",
        ]
        assert snap["dwellingCount"] == 6
        # Sixth is consummation
        assert snap["dwellings"][5]["consummation"] == "true"
        # All have rubric + text
        for d in snap["dwellings"]:
            assert d["rubric"], d
            assert d["hasText"], d
        # Footnotes on iii (Immanuel translation) and iv (Greek)
        assert snap["dwellings"][2]["hasFootnote"]
        assert snap["dwellings"][3]["hasFootnote"]
        # Five vocabulary terms, Hebrew + Greek
        assert snap["termCount"] == 5
        langs = [T["lang"] for T in snap["terms"]]
        assert "he" in langs and "el" in langs
        # Key terms present
        scripts = [T["script"] for T in snap["terms"]]
        assert any("שָׁכַן" in (s or "") for s in scripts)
        assert any("מִשְׁכָּן" in (s or "") for s in scripts)
        assert any("σκηνόω" in (s or "") for s in scripts)
        assert any("עִמָּנוּ" in (s or "") for s in scripts)
        print("\n  OK — six dwellings with rubrics/text, footnotes on Immanuel and John 1; five vocabulary terms (shakhan, mishkan, Immanuel, skēnoō, skēnē)")

        # ── Visual atmosphere check ───────────────────────────
        atmosphere = page.evaluate(
            """
          () => {
            const dwellings = document.querySelectorAll('.in-dwelling');
            const first = dwellings[0];
            const cons = document.querySelector(
              '.in-dwelling[data-consummation="true"]');
            const text = first.querySelector('.in-dwelling-text');
            const heb = document.querySelector(
              '.in-term-row[data-lang="he"] .in-term-script');
            return {
              firstBgImage: getComputedStyle(first).backgroundImage,
              consBgImage: getComputedStyle(cons).backgroundImage,
              firstMaxWidth: getComputedStyle(first).maxWidth,
              textAlign: getComputedStyle(text).textAlign,
              textStyle: getComputedStyle(text).fontStyle,
              hebDir: heb.dir,
              hebFontFamily: getComputedStyle(heb).fontFamily,
            };
          }
        """
        )
        print(f"\nVISUAL atmosphere:")
        print(f"  first  bg-image: {(atmosphere['firstBgImage'] or '')[:70]}...")
        print(f"  consum bg-image: {(atmosphere['consBgImage'] or '')[:70]}...")
        print(f"  dwelling max-width: {atmosphere['firstMaxWidth']}")
        print(f"  text align/style:   {atmosphere['textAlign']} {atmosphere['textStyle']}")
        print(f"  Hebrew dir/font:    {atmosphere['hebDir']} / {atmosphere['hebFontFamily'][:30]}")
        # Both dwellings carry warm parchment gradients
        assert "gradient" in (atmosphere["firstBgImage"] or "")
        assert "gradient" in (atmosphere["consBgImage"] or "")
        # Consummation has a richer gradient
        assert atmosphere["firstBgImage"] != atmosphere["consBgImage"]
        # Narrow measure — under 540px max-width (intimate column)
        mw = float(atmosphere["firstMaxWidth"].rstrip("px"))
        assert mw <= 540, mw
        # Text centered italic
        assert atmosphere["textAlign"] == "center"
        assert atmosphere["textStyle"] == "italic"
        # Hebrew renders RTL with SBL Hebrew font
        assert atmosphere["hebDir"] == "rtl"
        assert "SBL Hebrew" in atmosphere["hebFontFamily"]
        print("  OK — narrow intimate measure (<=540px); centered italic text; warm parchment; Hebrew RTL\n")

        # Screenshots
        page.screenshot(path="reports/v47_incarnation_top.png")
        page.evaluate(
            "() => { const el = document.querySelectorAll('.in-dwelling')[2];"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v47_incarnation_immanuel.png")
        page.evaluate(
            "() => { const el = document.querySelector('.in-dwelling[data-consummation]');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v47_incarnation_consummation.png")
        page.evaluate(
            "() => { const el = document.querySelector('.in-vocabulary');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v47_incarnation_vocabulary.png")
        page.evaluate(
            "() => { const el = document.querySelector('.cc-archive');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v47_incarnation_archive.png")

        # ── Recurrence at John 1:14 ───────────────────────────
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=jhn.1.14",
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
        joh_marker = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="jhn.1.14"]');
            return c ? !!c.querySelector(
              '.cr-folio-marker[data-kind="incarnational-presence"]'
            ) : false;
          }
        """
        )
        print(f"John 1:14 AO · 010 marker present: {joh_marker}")
        assert joh_marker
        page.evaluate("_openFolioObject('joh1-incarnation-dwelling')")
        page.wait_for_timeout(900)
        recur = page.evaluate(
            """
          () => {
            const r = document.querySelector(
              '.folio-leaf.incarnation-chamber .cc-recurrence-rubric');
            return r ? {
              lead: r.querySelector('.ccr-lead')?.textContent,
              where: r.querySelector('.ccr-where')?.textContent,
            } : null;
          }
        """
        )
        print(f"  recurrence rubric: {recur}")
        assert recur and "Exodus 25:8" in (recur["where"] or "")
        print("  OK — AO · 010 recurs at John 1:14 with recurrence rubric\n")
        page.screenshot(path="reports/v47_incarnation_john.png")

        b.close()
    print("ALL CHECKS PASSED — AO · 010 is operational, distinct, and recurring")


if __name__ == "__main__":
    main()
