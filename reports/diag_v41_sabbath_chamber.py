"""v41 — AO · 004 The Sabbath Pattern (Consecrated Time).

Verifies the fourth Atlas Object class is wired end-to-end:
  · Folio marker present at Genesis 2:1.
  · Chamber renders seven rhythm rows with the seventh set apart
    (different cadence, consecration rubric replacing refrain).
  · A threshold ornament marks the move into the seventh day.
  · Five recurrence fragments stack vertically below.
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
        (r for r in data["genealogy"] if r["id"] == "gen2-sabbath-pattern"),
        None,
    )
    assert rec, "AO · 004 record missing"
    print("DATA — gen2-sabbath-pattern:")
    print(f"  kind:    {rec['kind']}")
    print(f"  title:   {rec['title']}")
    print(f"  anchors: {[a['target'].split('::').pop() for a in rec['anchors']]}")
    print(f"  AO siglum:   {rec['atlas_object']['siglum']}")
    print(f"  AO class:    {rec['atlas_object']['class']}")
    print(f"  sevenfold rhythm: {len(rec['sevenfold_rhythm'])} movements")
    print(f"  recurrence fragments: {len(rec['recurrence_fragments'])}")
    assert rec["kind"] == "ritual"
    assert rec["atlas_object"]["siglum"] == "AO · 004"
    assert rec["atlas_object"]["class"] == "sacred-time"
    assert len(rec["sevenfold_rhythm"]) == 7
    # Seventh movement is consecrated
    seventh = rec["sevenfold_rhythm"][6]
    assert seventh.get("consecrated") is True
    assert seventh["numeral"] == "vii"
    assert "sanctified" in (seventh.get("consecration") or "")
    print(f"  seventh movement: {seventh['numeral']} · CONSECRATED")
    print(f"    consecration: {seventh['consecration'][:80]!r}")
    print("OK — data structure is correct\n")

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.2.1",
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

        # ── Marker at Genesis 2:1 ─────────────────────────────
        gen21 = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="gen.2.1"]');
            if (!c) return null;
            return Array.from(c.querySelectorAll('.cr-folio-marker')).map(m => ({
              kind: m.dataset.kind,
              aria: m.getAttribute('aria-label'),
            }));
          }
        """
        )
        print(f"Gen 2:1 cluster markers:")
        for m in gen21 or []:
            print(f"  · {m['kind']:<22} {m['aria']}")
        assert gen21, "no markers at gen.2.1"
        ao004 = next(
            (m for m in gen21
             if "Sabbath Pattern" in (m["aria"] or "")),
            None,
        )
        assert ao004, gen21
        assert ao004["kind"] == "ritual"
        print("  OK — AO · 004 marker (ritual ⁂) present at gen.2.1\n")

        # ── Open the chamber ──────────────────────────────────
        page.evaluate("_openFolioObject('gen2-sabbath-pattern')")
        page.wait_for_timeout(900)

        snap = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.sabbath-chamber');
            if (!leaf) return null;
            const days = Array.from(leaf.querySelectorAll('.sc-day'));
            const threshold = leaf.querySelector('.sc-threshold');
            const fragments = Array.from(leaf.querySelectorAll('.sc-fragment'));
            const sections = Array.from(
              leaf.querySelectorAll('.cc-section-heading .cc-section-title')
            ).map(el => el.textContent);
            const archive = leaf.querySelector('.cc-archive');
            return {
              siglum: leaf.querySelector('.cc-aor-siglum')?.textContent,
              sections,
              daysCount: days.length,
              days: days.map(d => ({
                numeral: d.querySelector('.sc-day-numeral')?.textContent,
                consecrated: d.dataset.consecrated || null,
                hasRefrain: !!d.querySelector('.sc-day-refrain'),
                hasConsecration: !!d.querySelector('.sc-day-consecration'),
                refrain: d.querySelector('.sc-day-refrain')?.textContent,
                consecration: d.querySelector('.sc-day-consecration')?.textContent,
              })),
              hasThreshold: !!threshold,
              thresholdText: threshold?.textContent,
              fragmentCount: fragments.length,
              fragments: fragments.map(f => ({
                ref: f.querySelector('.sc-fragment-ref')?.textContent,
                tradition: f.querySelector('.sc-fragment-tradition')?.textContent,
              })),
              hasArchive: !!archive,
            };
          }
        """
        )
        assert snap, "sabbath chamber did not render"
        print("CHAMBER — sabbath:")
        print(f"  siglum:   {snap['siglum']!r}")
        print(f"  sections: {snap['sections']}")
        print(f"  days rendered: {snap['daysCount']}")
        for d in snap['days']:
            mark = " · CONSECRATED" if d['consecrated'] else ""
            line = (f"    {d['numeral']:>4}{mark}  "
                    f"refrain={'·' if d['hasRefrain'] else ' '}  "
                    f"consecration={'·' if d['hasConsecration'] else ' '}")
            print(line)
        print(f"  threshold ornament: {snap['hasThreshold']} ({snap['thresholdText']!r})")
        print(f"  recurrence fragments: {snap['fragmentCount']}")
        for f in snap['fragments']:
            print(f"    · {f['ref']:<20} {f['tradition']}")

        assert snap["siglum"] == "AO · 004"
        assert snap["sections"] == [
            "Sevenfold Rhythm", "Recurrence Through Tradition", "Anchorings",
        ]
        # Seven day rows
        assert snap["daysCount"] == 7
        # Days 1-6 have refrains, day 7 has consecration
        for i in range(6):
            assert snap["days"][i]["hasRefrain"], (
                f"day {i+1} should have refrain"
            )
            assert not snap["days"][i]["hasConsecration"]
            assert not snap["days"][i]["consecrated"]
        assert snap["days"][6]["consecrated"] == "true"
        assert not snap["days"][6]["hasRefrain"]
        assert snap["days"][6]["hasConsecration"]
        print("  OK — six refrains then seventh-day consecration (formula broken)")
        # Threshold ornament present
        assert snap["hasThreshold"]
        assert snap["thresholdText"] == "⁘"
        print("  OK — threshold ornament marks the move into consecrated time")
        # Five recurrence fragments
        assert snap["fragmentCount"] == 5
        # Archive panel reused
        assert snap["hasArchive"]
        print("  OK — five recurrence fragments + archive commentary")

        # ── Visual atmosphere check: seventh-day cadence
        atmosphere = page.evaluate(
            """
          () => {
            const sixth = document.querySelectorAll('.sc-day')[5];
            const seventh = document.querySelectorAll('.sc-day')[6];
            return {
              sixthAlign: getComputedStyle(sixth).textAlign,
              seventhAlign: getComputedStyle(seventh).textAlign,
              sixthBg: getComputedStyle(sixth).backgroundColor,
              seventhBg: getComputedStyle(seventh).backgroundColor,
              seventhPaddingTop: getComputedStyle(seventh).paddingTop,
              sixthPaddingTop: getComputedStyle(sixth).paddingTop,
            };
          }
        """
        )
        print(f"\nVISUAL DIFFERENCE between six and seven:")
        print(f"  align: sixth={atmosphere['sixthAlign']} seventh={atmosphere['seventhAlign']}")
        print(f"  padding-top: sixth={atmosphere['sixthPaddingTop']} seventh={atmosphere['seventhPaddingTop']}")
        print(f"  background: sixth={atmosphere['sixthBg']} seventh={atmosphere['seventhBg']}")
        # The seventh day must be centered and have more breath
        assert atmosphere["seventhAlign"] == "center"
        assert float(atmosphere["seventhPaddingTop"].replace("px", "")) > float(
            atmosphere["sixthPaddingTop"].replace("px", "")
        )
        # And visibly tinted
        assert atmosphere["seventhBg"] != atmosphere["sixthBg"]
        print("  OK — seventh-day rhythm visibly set apart\n")

        # Screenshots
        page.screenshot(path="reports/v41_sabbath_top.png")
        page.evaluate(
            "() => { const el = document.querySelector('.sc-day[data-consecrated]');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v41_sabbath_seventh.png")
        page.evaluate(
            "() => { const el = document.querySelector('.sc-recurrence');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v41_sabbath_recurrence.png")
        page.evaluate(
            "() => { const el = document.querySelector('.cc-archive');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v41_sabbath_archive.png")

        # ── Recurrence at Hebrews 4:9 ─────────────────────────
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=heb.4.9",
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
        heb_marker = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="heb.4.9"]');
            return c ? !!c.querySelector('.cr-folio-marker[data-kind="ritual"]') : false;
          }
        """
        )
        print(f"Hebrews 4:9 AO · 004 marker present: {heb_marker}")
        assert heb_marker, "AO · 004 should recur at heb.4.9"
        page.evaluate("_openFolioObject('gen2-sabbath-pattern')")
        page.wait_for_timeout(900)
        recur = page.evaluate(
            """
          () => {
            const r = document.querySelector(
              '.folio-leaf.sabbath-chamber .cc-recurrence-rubric');
            return r ? {
              lead: r.querySelector('.ccr-lead')?.textContent,
              where: r.querySelector('.ccr-where')?.textContent,
            } : null;
          }
        """
        )
        print(f"  recurrence rubric: {recur}")
        assert recur and "Genesis 2:1" in (recur["where"] or "")
        print("  OK — AO · 004 recurs at Hebrews 4:9 with recurrence rubric\n")
        page.screenshot(path="reports/v41_sabbath_hebrews.png")

        b.close()
    print("ALL CHECKS PASSED — AO · 004 is operational, distinct, and recurring")


if __name__ == "__main__":
    main()
