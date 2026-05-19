"""v40 — AO · 003 The Antediluvian Line (Adam → Noah).

Verifies the third Atlas Object class is wired end-to-end:
  · Folio marker present at Genesis 5:1.
  · Chamber renders ten generation rows with hairline descent
    stems between them.
  · Enoch row carries a quiet rupture (different cadence,
    dotted descent stems on either side, his rubric displayed).
  · Temporal-continuity stemma renders ten lifespan bars with
    sensible positions; Enoch's bar is the dotted anomaly.
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
        (r for r in data["genealogy"] if r["id"] == "gen5-antediluvian-line"),
        None,
    )
    assert rec, "AO · 003 record missing"
    print("DATA — gen5-antediluvian-line:")
    print(f"  kind:    {rec['kind']}")
    print(f"  title:   {rec['title']}")
    print(f"  anchors: {[a['target'].split('::').pop() for a in rec['anchors']]}")
    print(f"  generations: {len(rec['generations'])}")
    print(f"  AO siglum:   {rec['atlas_object']['siglum']}")
    print(f"  AO class:    {rec['atlas_object']['class']}")
    assert rec["kind"] == "genealogy"
    assert rec["atlas_object"]["siglum"] == "AO · 003"
    assert rec["atlas_object"]["class"] == "genealogical-lineage"
    assert len(rec["generations"]) == 10
    # Enoch is generation index 6 (zero-based) and is marked
    # special: "interruption"
    enoch = rec["generations"][6]
    assert enoch["name_en"] == "Enoch", enoch
    assert enoch["special"] == "interruption"
    # Birth/death years computed
    adam = rec["generations"][0]
    noah = rec["generations"][9]
    assert adam["birth_year"] == 0
    assert adam["death_year"] == 930
    assert noah["birth_year"] == 1056
    print(f"  Adam:  AM {adam['birth_year']}–{adam['death_year']}")
    print(f"  Enoch: AM {enoch['birth_year']}–{enoch['death_year']} [interruption]")
    print(f"  Noah:  AM {noah['birth_year']}–{noah['death_year']}")
    print("OK — data structure is correct\n")

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.5.1",
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

        # ── Marker at Genesis 5:1 ─────────────────────────────
        gen51 = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="gen.5.1"]');
            if (!c) return null;
            return Array.from(c.querySelectorAll('.cr-folio-marker')).map(m => ({
              kind: m.dataset.kind,
              aria: m.getAttribute('aria-label'),
            }));
          }
        """
        )
        print(f"Gen 5:1 cluster markers:")
        for m in gen51 or []:
            print(f"  · {m['kind']:<22} {m['aria']}")
        assert gen51, "no markers at gen.5.1"
        kinds = [m["kind"] for m in gen51]
        assert "genealogy" in kinds
        # Find the one belonging to AO · 003 (its aria-label
        # contains the title)
        ao003 = next(
            (m for m in gen51
             if "Antediluvian Line" in (m["aria"] or "")),
            None,
        )
        assert ao003, gen51
        print("  OK — AO · 003 marker present at gen.5.1\n")

        # ── Open the chamber ──────────────────────────────────
        page.evaluate("_openFolioObject('gen5-antediluvian-line')")
        page.wait_for_timeout(900)

        snap = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.lineage-chamber');
            if (!leaf) return null;
            const gens = Array.from(leaf.querySelectorAll('.lc-generation'));
            const stems = Array.from(leaf.querySelectorAll('.lc-descent-stem'));
            const stemmaBars = Array.from(leaf.querySelectorAll('.lc-stemma-bar'));
            const sections = Array.from(
              leaf.querySelectorAll('.cc-section-heading .cc-section-title')
            ).map(el => el.textContent);
            const ruptureQuote = leaf.querySelector('.lc-gen-rupture');
            const archive = leaf.querySelector('.cc-archive');
            return {
              hasRubric: !!leaf.querySelector('.cc-atlas-object-rubric'),
              siglum: leaf.querySelector('.cc-aor-siglum')?.textContent,
              sections,
              generationsCount: gens.length,
              generations: gens.map(g => ({
                special: g.dataset.special || null,
                name: g.querySelector('.lc-gen-name-en')?.textContent,
                hebrew: g.querySelector('.lc-gen-name-he')?.textContent,
                lifespan: g.querySelector('.lc-gen-lifespan')?.textContent,
                witness: g.querySelector('.lc-gen-witness')?.textContent,
              })),
              stems: stems.map(s => ({
                rupture: s.classList.contains('lc-stem-rupture'),
              })),
              stemmaBars: stemmaBars.map(b => ({
                left: b.style.left,
                width: b.style.width,
              })),
              ruptureQuote: ruptureQuote?.textContent,
              hasArchive: !!archive,
            };
          }
        """
        )
        assert snap, "lineage chamber did not render"
        print("CHAMBER — lineage:")
        print(f"  siglum:   {snap['siglum']!r}")
        print(f"  sections: {snap['sections']}")
        print(f"  generations rendered: {snap['generationsCount']}")
        for g in snap["generations"]:
            mark = f" [{g['special']}]" if g['special'] else ""
            print(f"    · {g['name']:<12} {g['hebrew']!r}  ::  {g['lifespan']}  ({g['witness']}){mark}")
        # 10 generations, 9 stems between them
        assert snap["generationsCount"] == 10
        assert len(snap["stems"]) == 9
        # Enoch is the special row
        enoch_row = snap["generations"][6]
        assert enoch_row["name"] == "Enoch"
        assert enoch_row["special"] == "interruption"
        # Rupture stems on either side of Enoch (indices 5 and 6
        # in the stems list — stem 5 sits between Jared and Enoch;
        # stem 6 between Enoch and Methuselah)
        assert snap["stems"][5]["rupture"], "stem before Enoch should be dotted"
        assert snap["stems"][6]["rupture"], "stem after Enoch should be dotted"
        # The other stems are NOT rupture stems
        for i, s in enumerate(snap["stems"]):
            if i not in (5, 6):
                assert not s["rupture"], f"stem {i} should not be a rupture"
        print(f"  OK — Enoch interruption stems visibly different (stems 5,6 dotted)")
        # Rupture quote present
        assert snap["ruptureQuote"]
        assert "walked with God" in snap["ruptureQuote"]
        print(f"  rupture quote: {snap['ruptureQuote'][:80]!r}")
        # Stemma — 10 bars
        assert len(snap["stemmaBars"]) == 10
        # Adam's bar should start at 0% left
        adam_bar = snap["stemmaBars"][0]
        assert adam_bar["left"].startswith("0"), adam_bar
        # Enoch's bar (index 6) is the special — confirm it's
        # narrower than the surrounding bars (lifespan 365 vs
        # ~900 for others). Width is a percentage string.
        widths = [float(b["width"].rstrip("%")) for b in snap["stemmaBars"]]
        enoch_width = widths[6]
        avg_other = sum(w for i, w in enumerate(widths) if i != 6) / 9
        print(f"  stemma — Enoch width: {enoch_width:.1f}%, avg of others: {avg_other:.1f}%")
        assert enoch_width < avg_other * 0.6, (
            f"Enoch's bar should be visibly shorter: {enoch_width} vs avg {avg_other}"
        )
        # Archive panel
        assert snap["hasArchive"]
        print("  OK — temporal continuity stemma renders with Enoch as anomaly\n")

        # Screenshots
        page.screenshot(path="reports/v40_lineage_top.png")
        page.evaluate(
            "() => { const el = document.querySelector('.lc-generation[data-special]');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v40_lineage_enoch.png")
        page.evaluate(
            "() => { const el = document.querySelector('.lc-stemma');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v40_lineage_stemma.png")
        page.evaluate(
            "() => { const el = document.querySelector('.cc-archive');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v40_lineage_archive.png")

        # ── Recurrence at 1 Chronicles 1:1 ────────────────────
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=1ch.1.1",
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
        ch_marker = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="1ch.1.1"]');
            return c ? !!c.querySelector('.cr-folio-marker[data-kind="genealogy"]') : false;
          }
        """
        )
        print(f"1 Chronicles 1:1 AO · 003 marker present: {ch_marker}")
        assert ch_marker, "AO · 003 should recur at 1ch.1.1"
        page.evaluate("_openFolioObject('gen5-antediluvian-line')")
        page.wait_for_timeout(900)
        recur = page.evaluate(
            """
          () => {
            const r = document.querySelector(
              '.folio-leaf.lineage-chamber .cc-recurrence-rubric');
            return r ? {
              lead: r.querySelector('.ccr-lead')?.textContent,
              where: r.querySelector('.ccr-where')?.textContent,
            } : null;
          }
        """
        )
        print(f"  recurrence rubric: {recur}")
        assert recur and "Genesis 5" in (recur["where"] or "")
        print("  OK — AO · 003 recurs at 1 Chronicles 1:1 with recurrence rubric\n")
        page.screenshot(path="reports/v40_lineage_chronicles.png")

        b.close()
    print("ALL CHECKS PASSED — AO · 003 is operational, distinct, and recurring")


if __name__ == "__main__":
    main()
