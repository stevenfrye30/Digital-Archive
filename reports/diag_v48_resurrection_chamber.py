"""v48 — AO · 011 Bones Clothed With Breath (Resurrection and Renewal).

Verifies the eleventh Atlas Object class is wired end-to-end:
  · Folio marker present at Ezekiel 37:10 with the new ⊛ glyph.
  · Chamber renders six rupture-then-return pairings, each with
    a dim "before" / hairline scar / full-intensity "after".
  · The fourth pair (John 20) carries the wound-mark rubric;
    the sixth (Revelation 21) is the consummation.
  · The "before" text is visibly dimmer (lower alpha) than the
    "after" text — breath returning is felt in the typography.
  · Breath vocabulary section renders ruach / pneuma / anastasis
    etc.
  · Recurrence rubric fires on a second anchoring.
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
    with open(ROOT / "data/bible_kjv.json", encoding="utf-8") as f:
        data = json.load(f)
    rec = next(
        (r for r in data["genealogy"] if r["id"] == "eze37-bones-breath"),
        None,
    )
    assert rec, "AO · 011 record missing"
    print("DATA — eze37-bones-breath:")
    print(f"  kind:    {rec['kind']}")
    print(f"  title:   {rec['title']}")
    print(f"  anchors: {[a['target'].split('::').pop() for a in rec['anchors']]}")
    print(f"  AO siglum:   {rec['atlas_object']['siglum']}")
    print(f"  AO class:    {rec['atlas_object']['class']}")
    print(f"  return moments:    {len(rec['return_moments'])}")
    print(f"  breath vocabulary: {len(rec['breath_vocabulary'])}")
    assert rec["kind"] == "resurrection-renewal"
    assert rec["atlas_object"]["siglum"] == "AO · 011"
    assert rec["atlas_object"]["class"] == "resurrection-renewal"
    assert len(rec["return_moments"]) == 6
    # Fourth has the wound mark
    fourth = rec["return_moments"][3]
    assert fourth.get("wound_mark") is True
    assert "John 20" in fourth["ref"]
    # Sixth is consummation
    sixth = rec["return_moments"][5]
    assert sixth.get("consummation") is True
    assert "Revelation 21" in sixth["ref"]
    print(f"  John 20 carries WOUND_MARK")
    print(f"  Rev 21 is the CONSUMMATION")
    print("OK — data structure is correct\n")

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=eze.37.10",
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

        # ── Marker present at eze.37.10 ───────────────────────
        eze3710 = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="eze.37.10"]');
            if (!c) return null;
            return Array.from(c.querySelectorAll('.cr-folio-marker')).map(m => ({
              kind: m.dataset.kind,
              aria: m.getAttribute('aria-label'),
            }));
          }
        """
        )
        print(f"Ezekiel 37:10 cluster markers:")
        for m in eze3710 or []:
            print(f"  · {m['kind']:<22} {m['aria']}")
        assert eze3710
        ao011 = next(
            (m for m in eze3710
             if "Bones Clothed With Breath" in (m["aria"] or "")),
            None,
        )
        assert ao011, eze3710
        assert ao011["kind"] == "resurrection-renewal"
        print("  OK — AO · 011 marker (⊛ resurrection-renewal) present at eze.37.10\n")

        # ── Open the chamber ──────────────────────────────────
        page.evaluate("_openFolioObject('eze37-bones-breath')")
        page.wait_for_timeout(900)

        snap = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.resurrection-chamber');
            if (!leaf) return null;
            const returns = Array.from(leaf.querySelectorAll('.rs-return'));
            const terms = Array.from(leaf.querySelectorAll('.rs-term-row'));
            const sections = Array.from(
              leaf.querySelectorAll('.cc-section-heading .cc-section-title')
            ).map(el => el.textContent);
            return {
              siglum: leaf.querySelector('.cc-aor-siglum')?.textContent,
              sections,
              returnCount: returns.length,
              returns: returns.map(R => ({
                consummation: R.dataset.consummation || null,
                wound: R.dataset.wound || null,
                numeral: R.querySelector('.rs-return-numeral')?.textContent,
                ref: R.querySelector('.rs-return-ref')?.textContent,
                hasBefore: !!R.querySelector('.rs-before'),
                hasScar: !!R.querySelector('.rs-scar'),
                hasAfter: !!R.querySelector('.rs-after'),
                woundMark: R.querySelector('.rs-wound-mark')?.textContent,
                hasFootnote: !!R.querySelector('.rs-return-footnote'),
              })),
              termCount: terms.length,
              terms: terms.map(T => ({
                lang: T.dataset.lang,
                script: T.querySelector('.rs-term-script')?.textContent,
                translit: T.querySelector('.rs-term-translit')?.textContent,
              })),
            };
          }
        """
        )
        assert snap, "resurrection chamber did not render"
        print("CHAMBER — resurrection:")
        print(f"  siglum:   {snap['siglum']!r}")
        print(f"  sections: {snap['sections']}")
        print(f"  return moments ({snap['returnCount']}):")
        for R in snap['returns']:
            tag = []
            if R['wound']:        tag.append("WOUND")
            if R['consummation']: tag.append("CONSUMMATION")
            tagstr = " · " + " · ".join(tag) if tag else ""
            print(f"    {R['numeral']:>4} · {R['ref']:<28}{tagstr}")
            print(f"         before={R['hasBefore']} scar={R['hasScar']} after={R['hasAfter']} "
                  f"footnote={R['hasFootnote']}")
            if R['woundMark']:
                print(f"         wound mark: {R['woundMark']!r}")
        print(f"  vocabulary terms ({snap['termCount']}):")
        for T in snap['terms']:
            print(f"    · ({T['lang']}) {T['script']:<14} {T['translit']}")

        assert snap["siglum"] == "AO · 011"
        assert snap["sections"] == [
            "Returns", "Breath Vocabulary", "Anchorings",
        ]
        assert snap["returnCount"] == 6
        # Every return has before / scar / after
        for r in snap["returns"]:
            assert r["hasBefore"], r
            assert r["hasScar"], r
            assert r["hasAfter"], r
        # Fourth has the wound mark
        fourth = snap["returns"][3]
        assert fourth["wound"] == "true"
        assert "wounds remain" in (fourth["woundMark"] or "")
        # Sixth is consummation
        sixth = snap["returns"][5]
        assert sixth["consummation"] == "true"
        # Footnotes on i (ruach), iv (wounds), v (egeirō)
        assert snap["returns"][0]["hasFootnote"]  # Ezekiel ruach
        assert snap["returns"][3]["hasFootnote"]  # John 20 wounds
        assert snap["returns"][4]["hasFootnote"]  # 1 Cor egeirō
        # Five vocabulary terms (2 Hebrew + 3 Greek)
        assert snap["termCount"] == 5
        langs = [T["lang"] for T in snap["terms"]]
        assert langs.count("he") == 2
        assert langs.count("el") == 3
        # Key terms
        scripts = [T["script"] for T in snap["terms"]]
        assert any("רוּחַ" in (s or "") for s in scripts)
        assert any("πνεῦμα" in (s or "") for s in scripts)
        assert any("ἀνάστασις" in (s or "") for s in scripts)
        print("\n  OK — six rupture/return pairs (John 20 wound, Rev 21 consummation), five vocabulary terms")

        # ── Visual atmosphere check: before is visibly dimmer
        # than after; the breath returns in the type itself.
        atmosphere = page.evaluate(
            """
          () => {
            const r = document.querySelector('.rs-return');
            const before = r.querySelector('.rs-before');
            const after = r.querySelector('.rs-after');
            const scar = r.querySelector('.rs-scar');
            const woundReturn = document.querySelector(
              '.rs-return[data-wound="true"]');
            const cons = document.querySelector(
              '.rs-return[data-consummation="true"]');
            return {
              beforeColor: getComputedStyle(before).color,
              beforeSize: getComputedStyle(before).fontSize,
              afterColor: getComputedStyle(after).color,
              afterSize: getComputedStyle(after).fontSize,
              scarHeight: getComputedStyle(scar).borderTopWidth,
              scarColor: getComputedStyle(scar).borderTopColor,
              woundScarColor: woundReturn
                ? getComputedStyle(woundReturn.querySelector('.rs-scar')).borderTopColor
                : null,
              consBgImage: getComputedStyle(cons).backgroundImage,
              firstBgImage: getComputedStyle(r).backgroundImage,
            };
          }
        """
        )
        print(f"\nVISUAL atmosphere:")
        print(f"  before  color:   {atmosphere['beforeColor']}  size: {atmosphere['beforeSize']}")
        print(f"  after   color:   {atmosphere['afterColor']}  size: {atmosphere['afterSize']}")
        print(f"  scar:            {atmosphere['scarColor']} {atmosphere['scarHeight']}")
        print(f"  wound scar:      {atmosphere['woundScarColor']}")
        print(f"  cons  bg-image:  {(atmosphere['consBgImage'] or '')[:60]}...")
        print(f"  first bg-image:  {(atmosphere['firstBgImage'] or '')[:60]}...")
        # Before is dimmer than after — breath returns in alpha
        before_alpha = alpha(atmosphere["beforeColor"])
        after_alpha = alpha(atmosphere["afterColor"])
        print(f"  before alpha {before_alpha}  after alpha {after_alpha}")
        assert before_alpha < after_alpha
        # And smaller — breath returns in size
        before_sz = float(atmosphere["beforeSize"].rstrip("px"))
        after_sz = float(atmosphere["afterSize"].rstrip("px"))
        assert after_sz > before_sz
        # Scar is a hairline
        assert atmosphere["scarHeight"] == "1px"
        # Wound moment has a slightly darker scar color
        assert atmosphere["woundScarColor"] != atmosphere["scarColor"]
        # Consummation has a richer gradient
        assert atmosphere["consBgImage"] != atmosphere["firstBgImage"]
        print("  OK — before is dimmer + smaller than after; wound scar visibly darker; consummation distinct\n")

        # Screenshots
        page.screenshot(path="reports/v48_resurrection_top.png")
        page.evaluate(
            "() => { const el = document.querySelector('.rs-return[data-wound]');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v48_resurrection_wounds.png")
        page.evaluate(
            "() => { const el = document.querySelector('.rs-return[data-consummation]');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v48_resurrection_consummation.png")
        page.evaluate(
            "() => { const el = document.querySelector('.rs-vocabulary');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v48_resurrection_vocabulary.png")
        page.evaluate(
            "() => { const el = document.querySelector('.cc-archive');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v48_resurrection_archive.png")

        # ── Recurrence at John 20:27 ──────────────────────────
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=jhn.20.27",
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
        jhn_marker = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="jhn.20.27"]');
            return c ? !!c.querySelector(
              '.cr-folio-marker[data-kind="resurrection-renewal"]'
            ) : false;
          }
        """
        )
        print(f"John 20:27 AO · 011 marker present: {jhn_marker}")
        assert jhn_marker
        page.evaluate("_openFolioObject('eze37-bones-breath')")
        page.wait_for_timeout(900)
        recur = page.evaluate(
            """
          () => {
            const r = document.querySelector(
              '.folio-leaf.resurrection-chamber .cc-recurrence-rubric');
            return r ? {
              lead: r.querySelector('.ccr-lead')?.textContent,
              where: r.querySelector('.ccr-where')?.textContent,
            } : null;
          }
        """
        )
        print(f"  recurrence rubric: {recur}")
        assert recur and "Ezekiel 37:10" in (recur["where"] or "")
        print("  OK — AO · 011 recurs at John 20:27 with recurrence rubric\n")
        page.screenshot(path="reports/v48_resurrection_john20.png")

        b.close()
    print("ALL CHECKS PASSED — AO · 011 is operational, distinct, and recurring")


if __name__ == "__main__":
    main()
