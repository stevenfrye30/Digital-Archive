"""v46 — AO · 009 How Long, O LORD? (Lament Before Heaven).

Verifies the ninth Atlas Object class is wired end-to-end:
  · Folio marker present at Psalm 13:1 with the new ▾ glyph.
  · Chamber renders six lament cries held by a dotted vertical
    axis of address.
  · The fourth cry (Lamentations 3) is rendered as three Hebrew-
    letter triplets (א ב ג) — the acrostic structure holding.
  · The third cry (Psalm 88) carries an italic marginal note
    acknowledging the unresolved form.
  · Six echo refrains stack beneath with dotted left rule.
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
        (r for r in data["genealogy"] if r["id"] == "psa13-lament-cry"),
        None,
    )
    assert rec, "AO · 009 record missing"
    print("DATA — psa13-lament-cry:")
    print(f"  kind:    {rec['kind']}")
    print(f"  title:   {rec['title']}")
    print(f"  anchors: {[a['target'].split('::').pop() for a in rec['anchors']]}")
    print(f"  AO siglum:   {rec['atlas_object']['siglum']}")
    print(f"  AO class:    {rec['atlas_object']['class']}")
    print(f"  lament cries:  {len(rec['lament_cries'])}")
    print(f"  echo refrains: {len(rec['echo_refrains'])}")
    assert rec["kind"] == "lament-structure"
    assert rec["atlas_object"]["siglum"] == "AO · 009"
    assert rec["atlas_object"]["class"] == "lament-structure"
    assert len(rec["lament_cries"]) == 6
    # Cry iv has the acrostic
    fourth = rec["lament_cries"][3]
    assert "acrostic" in fourth and len(fourth["acrostic"]) == 3
    assert fourth["acrostic"][0]["letter_he"] == "א"
    assert fourth["acrostic"][1]["letter_he"] == "ב"
    assert fourth["acrostic"][2]["letter_he"] == "ג"
    print(f"  acrostic triads: א ב ג (Lamentations 3:1–9)")
    # Cry iii has the unresolved note
    third = rec["lament_cries"][2]
    assert "does not turn" in (third.get("unresolved_note") or "")
    print(f"  unresolved cry: Psalm 88 — '{third['unresolved_note']}'")
    print("OK — data structure is correct\n")

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=psa.13.1",
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

        # ── Marker present at psa.13.1 ────────────────────────
        psa131 = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="psa.13.1"]');
            if (!c) return null;
            return Array.from(c.querySelectorAll('.cr-folio-marker')).map(m => ({
              kind: m.dataset.kind,
              aria: m.getAttribute('aria-label'),
            }));
          }
        """
        )
        print(f"Psalm 13:1 cluster markers:")
        for m in psa131 or []:
            print(f"  · {m['kind']:<22} {m['aria']}")
        assert psa131
        ao009 = next(
            (m for m in psa131
             if "How Long" in (m["aria"] or "")),
            None,
        )
        assert ao009, psa131
        assert ao009["kind"] == "lament-structure"
        print("  OK — AO · 009 marker (▾ lament-structure) present at psa.13.1\n")

        # ── Open the chamber ──────────────────────────────────
        page.evaluate("_openFolioObject('psa13-lament-cry')")
        page.wait_for_timeout(900)

        snap = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.lament-chamber');
            if (!leaf) return null;
            const cries = Array.from(leaf.querySelectorAll('.lm-cry'));
            const refrains = Array.from(leaf.querySelectorAll('.lm-refrain'));
            const axis = leaf.querySelector('.lm-axis');
            const sections = Array.from(
              leaf.querySelectorAll('.cc-section-heading .cc-section-title')
            ).map(el => el.textContent);
            return {
              siglum: leaf.querySelector('.cc-aor-siglum')?.textContent,
              sections,
              hasAxis: !!axis,
              cryCount: cries.length,
              cries: cries.map(C => ({
                acrostic: C.dataset.acrostic || null,
                unresolved: C.dataset.unresolved || null,
                numeral: C.querySelector('.lm-cry-numeral')?.textContent,
                ref: C.querySelector('.lm-cry-ref')?.textContent,
                tradition: C.querySelector('.lm-cry-tradition')?.textContent,
                hasText: !!C.querySelector('.lm-cry-text'),
                hasAcrostic: !!C.querySelector('.lm-acrostic'),
                triadLetters: Array.from(
                  C.querySelectorAll('.lm-acrostic-letter-he')
                ).map(l => l.textContent),
                marginNote: C.querySelector('.lm-cry-margin-note')?.textContent,
              })),
              refrainCount: refrains.length,
              refrains: refrains.map(R => ({
                text: R.querySelector('.lm-refrain-text')?.textContent,
                ref: R.querySelector('.lm-refrain-ref')?.textContent,
              })),
            };
          }
        """
        )
        assert snap, "lament chamber did not render"
        print("CHAMBER — lament:")
        print(f"  siglum:   {snap['siglum']!r}")
        print(f"  sections: {snap['sections']}")
        print(f"  axis container: {snap['hasAxis']}")
        print(f"  cries ({snap['cryCount']}):")
        for c in snap['cries']:
            tag = []
            if c['acrostic']:   tag.append("ACROSTIC")
            if c['unresolved']: tag.append("UNRESOLVED")
            tagstr = " · " + " · ".join(tag) if tag else ""
            print(f"    {c['numeral']:>4} · {c['ref']:<22} {c['tradition']}{tagstr}")
            if c['hasAcrostic']:
                print(f"         triads: {c['triadLetters']}")
            if c['marginNote']:
                print(f"         note: {c['marginNote'][:80]!r}")
        print(f"  refrains ({snap['refrainCount']}):")
        for R in snap['refrains']:
            print(f"    · {(R['text'] or '')[:60]!r}  {R['ref']}")

        assert snap["siglum"] == "AO · 009"
        assert snap["sections"] == [
            "Cries", "Echo Refrains", "Anchorings",
        ]
        # Six cries with the axis container
        assert snap["hasAxis"]
        assert snap["cryCount"] == 6
        # The fourth cry has the acrostic with three triads
        fourth = snap["cries"][3]
        assert fourth["acrostic"] == "true"
        assert fourth["hasAcrostic"]
        assert fourth["triadLetters"] == ["א", "ב", "ג"]
        # The third cry has the unresolved marker
        third = snap["cries"][2]
        assert third["unresolved"] == "true"
        assert "does not turn" in (third["marginNote"] or "")
        # Non-acrostic, non-unresolved cries have hasText
        for i in (0, 1, 4, 5):
            assert snap["cries"][i]["hasText"], snap["cries"][i]
        # Six refrains
        assert snap["refrainCount"] == 6
        # The famous "How long" refrain is present
        assert any("How long" in (R["text"] or "") for R in snap["refrains"])
        # "Though he slay me" — the lament that endures
        assert any("yet will I trust" in (R["text"] or "") for R in snap["refrains"])
        print("\n  OK — six cries with acrostic triplets (Lam 3) and unresolved note (Ps 88); six refrains")

        # ── Visual atmosphere check ───────────────────────────
        atmosphere = page.evaluate(
            """
          () => {
            const axis = document.querySelector('.lm-axis');
            const cry = document.querySelector('.lm-cry');
            const text = cry.querySelector('.lm-cry-text');
            const refrainBorder = getComputedStyle(
              document.querySelector('.lm-refrain')
            );
            // The axis-mundi line is in ::before — we approximate via
            // padding-left as proxy.
            return {
              axisPadLeft: getComputedStyle(axis).paddingLeft,
              cryTextStyle: text ? getComputedStyle(text).fontStyle : null,
              cryTextSize: text ? getComputedStyle(text).fontSize : null,
              refrainBorderLeftStyle: refrainBorder.borderLeftStyle,
            };
          }
        """
        )
        print(f"\nVISUAL atmosphere:")
        print(f"  axis padding-left:        {atmosphere['axisPadLeft']}")
        print(f"  cry text:                 {atmosphere['cryTextStyle']} {atmosphere['cryTextSize']}")
        print(f"  refrain border-left:      {atmosphere['refrainBorderLeftStyle']}")
        assert atmosphere["cryTextStyle"] == "italic"
        # The refrain column border is dotted — broken-but-unsevered
        assert atmosphere["refrainBorderLeftStyle"] == "dotted"
        print("  OK — italic cry text, dotted refrain border (broken-but-unsevered axis)\n")

        # Screenshots
        page.screenshot(path="reports/v46_lament_top.png")
        page.evaluate(
            "() => { const el = document.querySelector('.lm-cry[data-acrostic]');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v46_lament_acrostic.png")
        page.evaluate(
            "() => { const el = document.querySelector('.lm-cry[data-unresolved]');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v46_lament_unresolved.png")
        page.evaluate(
            "() => { const el = document.querySelector('.lm-refrains');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v46_lament_refrains.png")
        page.evaluate(
            "() => { const el = document.querySelector('.cc-archive');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v46_lament_archive.png")

        # ── Recurrence at Lamentations 3:1 ────────────────────
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=lam.3.1",
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
        lam_marker = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="lam.3.1"]');
            return c ? !!c.querySelector(
              '.cr-folio-marker[data-kind="lament-structure"]'
            ) : false;
          }
        """
        )
        print(f"Lamentations 3:1 AO · 009 marker present: {lam_marker}")
        assert lam_marker
        page.evaluate("_openFolioObject('psa13-lament-cry')")
        page.wait_for_timeout(900)
        recur = page.evaluate(
            """
          () => {
            const r = document.querySelector(
              '.folio-leaf.lament-chamber .cc-recurrence-rubric');
            return r ? {
              lead: r.querySelector('.ccr-lead')?.textContent,
              where: r.querySelector('.ccr-where')?.textContent,
            } : null;
          }
        """
        )
        print(f"  recurrence rubric: {recur}")
        # BOOK_NAMES renders 'psa' as 'Psalms' (canonical plural form)
        assert recur and "13:1" in (recur["where"] or "") \
            and "Psalm" in (recur["where"] or "")
        print("  OK — AO · 009 recurs at Lamentations 3:1 with recurrence rubric\n")
        page.screenshot(path="reports/v46_lament_lamentations.png")

        b.close()
    print("ALL CHECKS PASSED — AO · 009 is operational, distinct, and recurring")


if __name__ == "__main__":
    main()
