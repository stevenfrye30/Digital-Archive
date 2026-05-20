"""v44 — AO · 007 The Fear of the LORD (Wisdom's Beginning).

Verifies the seventh Atlas Object class is wired end-to-end:
  · Folio marker present at Proverbs 1:7 with the new ⁕ glyph.
  · Chamber renders six wisdom sayings stacked vertically with
    pause markers between them.
  · Each saying is centered, italic, with a numeral above and
    a small-caps reference beneath.
  · Compression layer renders the Hebrew phrase yirʾat YHWH,
    three lexical notes, and the LXX/Vulgate trail.
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
        (r for r in data["genealogy"] if r["id"] == "prov1-wisdom-fear"),
        None,
    )
    assert rec, "AO · 007 record missing"
    print("DATA — prov1-wisdom-fear:")
    print(f"  kind:    {rec['kind']}")
    print(f"  title:   {rec['title']}")
    print(f"  anchors: {[a['target'].split('::').pop() for a in rec['anchors']]}")
    print(f"  AO siglum:   {rec['atlas_object']['siglum']}")
    print(f"  AO class:    {rec['atlas_object']['class']}")
    print(f"  wisdom sayings: {len(rec['wisdom_sayings'])}")
    print(f"  compression notes: {len(rec['compression']['notes'])}")
    assert rec["kind"] == "wisdom-saying"
    assert rec["atlas_object"]["siglum"] == "AO · 007"
    assert rec["atlas_object"]["class"] == "wisdom-saying"
    assert len(rec["wisdom_sayings"]) == 6
    assert rec["compression"]["phrase_he"] == "יִרְאַת יְהוָה"
    print("OK — data structure is correct\n")

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=pro.1.7",
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

        # ── Marker present at pro.1.7 ─────────────────────────
        pro17 = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="pro.1.7"]');
            if (!c) return null;
            return Array.from(c.querySelectorAll('.cr-folio-marker')).map(m => ({
              kind: m.dataset.kind,
              aria: m.getAttribute('aria-label'),
            }));
          }
        """
        )
        print(f"Proverbs 1:7 cluster markers:")
        for m in pro17 or []:
            print(f"  · {m['kind']:<22} {m['aria']}")
        assert pro17
        ao007 = next(
            (m for m in pro17
             if "Fear of the LORD" in (m["aria"] or "")),
            None,
        )
        assert ao007, pro17
        assert ao007["kind"] == "wisdom-saying"
        print("  OK — AO · 007 marker (⁕ wisdom-saying) present at pro.1.7\n")

        # ── Open the chamber ──────────────────────────────────
        page.evaluate("_openFolioObject('prov1-wisdom-fear')")
        page.wait_for_timeout(900)

        snap = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.wisdom-chamber');
            if (!leaf) return null;
            const sayings = Array.from(leaf.querySelectorAll('.ws-saying'));
            const pauses = Array.from(leaf.querySelectorAll('.ws-pause'));
            const comp = leaf.querySelector('.ws-compression');
            const notes = Array.from(leaf.querySelectorAll('.ws-comp-note'));
            const sections = Array.from(
              leaf.querySelectorAll('.cc-section-heading .cc-section-title')
            ).map(el => el.textContent);
            return {
              siglum: leaf.querySelector('.cc-aor-siglum')?.textContent,
              sections,
              sayingCount: sayings.length,
              sayings: sayings.map(s => ({
                numeral: s.querySelector('.ws-saying-numeral')?.textContent,
                text: s.querySelector('.ws-saying-text')?.textContent,
                ref: s.querySelector('.ws-saying-ref')?.textContent,
              })),
              pauseCount: pauses.length,
              pauseChars: pauses.map(p => p.textContent),
              hasCompression: !!comp,
              compHebrew: comp?.querySelector('.ws-comp-hebrew')?.textContent,
              compTranslit: comp?.querySelector('.ws-comp-translit')?.textContent,
              compEnglish: comp?.querySelector('.ws-comp-english')?.textContent,
              noteCount: notes.length,
              noteHeads: notes.map(n => n.querySelector('.ws-comp-note-head')?.textContent),
              compTrailLines: Array.from(
                comp?.querySelectorAll('.ws-comp-trail-line') || []
              ).map(t => t.textContent),
            };
          }
        """
        )
        assert snap, "wisdom chamber did not render"
        print("CHAMBER — wisdom:")
        print(f"  siglum:   {snap['siglum']!r}")
        print(f"  sections: {snap['sections']}")
        print(f"  sayings ({snap['sayingCount']}):")
        for s in snap['sayings']:
            print(f"    {s['numeral']:>4} · {s['ref']}")
            print(f"         {(s['text'] or '')[:80]!r}")
        print(f"  pauses between sayings: {snap['pauseCount']} ({set(snap['pauseChars'])})")
        print(f"  compression:")
        print(f"    hebrew:    {snap['compHebrew']!r}")
        print(f"    translit:  {snap['compTranslit']!r}")
        print(f"    english:   {snap['compEnglish']!r}")
        print(f"    notes ({snap['noteCount']}):")
        for h in snap['noteHeads']:
            print(f"      · {h}")
        print(f"    trail lines: {snap['compTrailLines']}")

        assert snap["siglum"] == "AO · 007"
        assert snap["sections"] == [
            "Sayings", "Compression", "Anchorings",
        ]
        # Six sayings + five pause markers between them
        assert snap["sayingCount"] == 6
        assert snap["pauseCount"] == 5
        assert set(snap["pauseChars"]) == {"·"}
        # Each saying has numeral, text, ref
        for s in snap["sayings"]:
            assert s["numeral"], s
            assert s["text"], s
            assert s["ref"], s
        # The Job and Ecclesiastes sayings are present
        refs = [s["ref"] for s in snap["sayings"]]
        assert "Job 28:28" in refs
        assert "Ecclesiastes 12:13" in refs
        assert "James 3:17" in refs
        # Compression layer
        assert snap["hasCompression"]
        assert snap["compHebrew"] == "יִרְאַת יְהוָה"
        assert "yir" in (snap["compTranslit"] or "")
        assert snap["noteCount"] == 3
        # Trail lines include LXX and Vulgate
        trail_blob = " ".join(snap["compTrailLines"])
        assert "LXX" in trail_blob and "Vulgate" in trail_blob
        print("\n  OK — six sayings with five pauses, compression layer with Hebrew + 3 notes + LXX/Vulgate trail")

        # ── Visual atmosphere check ───────────────────────────
        atmosphere = page.evaluate(
            """
          () => {
            const s = document.querySelector('.ws-saying');
            const text = s.querySelector('.ws-saying-text');
            return {
              sayingAlign: getComputedStyle(s).textAlign,
              textStyle: getComputedStyle(text).fontStyle,
              textSize: getComputedStyle(text).fontSize,
              sayingPaddingTop: getComputedStyle(s).paddingTop,
            };
          }
        """
        )
        print(f"\nVISUAL atmosphere:")
        print(f"  saying align: {atmosphere['sayingAlign']}")
        print(f"  saying text:  {atmosphere['textStyle']} {atmosphere['textSize']}")
        print(f"  padding-top:  {atmosphere['sayingPaddingTop']}")
        assert atmosphere["sayingAlign"] == "center"
        assert atmosphere["textStyle"] == "italic"
        # Saying text should be larger than the surrounding lede prose
        assert float(atmosphere["textSize"].rstrip("px")) > 18
        # Generous padding around each saying (>=22px top)
        assert float(atmosphere["sayingPaddingTop"].rstrip("px")) >= 22
        print("  OK — sayings centered, italic, larger than prose, generous breath\n")

        # Screenshots
        page.screenshot(path="reports/v44_wisdom_top.png")
        page.evaluate(
            "() => { const el = document.querySelectorAll('.ws-saying')[2];"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v44_wisdom_middle.png")
        page.evaluate(
            "() => { const el = document.querySelector('.ws-compression');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v44_wisdom_compression.png")
        page.evaluate(
            "() => { const el = document.querySelector('.cc-archive');"
            "if (el) el.scrollIntoView({block: 'center'}); }"
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v44_wisdom_archive.png")

        # ── Recurrence at Job 28:28 ───────────────────────────
        page.mouse.click(50, 50)
        page.wait_for_timeout(300)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=job.28.28",
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
        job_marker = page.evaluate(
            """
          () => {
            const c = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="job.28.28"]');
            return c ? !!c.querySelector(
              '.cr-folio-marker[data-kind="wisdom-saying"]'
            ) : false;
          }
        """
        )
        print(f"Job 28:28 AO · 007 marker present: {job_marker}")
        assert job_marker
        page.evaluate("_openFolioObject('prov1-wisdom-fear')")
        page.wait_for_timeout(900)
        recur = page.evaluate(
            """
          () => {
            const r = document.querySelector(
              '.folio-leaf.wisdom-chamber .cc-recurrence-rubric');
            return r ? {
              lead: r.querySelector('.ccr-lead')?.textContent,
              where: r.querySelector('.ccr-where')?.textContent,
            } : null;
          }
        """
        )
        print(f"  recurrence rubric: {recur}")
        assert recur and "Proverbs 1:7" in (recur["where"] or "")
        print("  OK — AO · 007 recurs at Job 28:28 with recurrence rubric\n")
        page.screenshot(path="reports/v44_wisdom_job.png")

        b.close()
    print("ALL CHECKS PASSED — AO · 007 is operational, distinct, and recurring")


if __name__ == "__main__":
    main()
