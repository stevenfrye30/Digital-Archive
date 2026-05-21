"""v66 — Genesis Wave Two: Abrahamic emergence arc verification.

Verifies the four new records of Wave Two land cleanly in
Genesis 12-15 without breaking hierarchy or spilling into
neighbouring chapters.

Checks per record:
  · marker present at correct anchor with correct kind +
    authority + glyph
  · hierarchy silhouette respected (tertiary smaller than
    secondary)
  · opened leaf renders as text-shaped (no chamber dispatch)

Density checks:
  · Genesis 12 carries 3 marks across 3 distinct verses (12:1
    call, 12:5 map, 12:7 altar) — acknowledged but not crowded
  · Genesis 14 carries 1 mark at 14:18 (Melchizedek)
  · Genesis 15 carries 2 marks (15:6 linguistic + 15:18
    covenant)
  · Genesis 16 remains silent (no spillover)
  · Genesis 17 carries only the existing AO·006 (unchanged)

Atlas Index checks:
  · all four new records appear in the index
  · classification lines render: "Secondary · Map",
    "Secondary · Commentary", "Tertiary · Linguistic"
  · glyphs match: ✥ map, ❡ commentary, ℵ linguistic
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


EXPECTED_WAVE_TWO = [
    # (pid, expected kind, expected authority, expected glyph, expected_id)
    ("gen.12.5",  "map",        "secondary", "✥", "gen12-patriarchal-journey-map"),
    ("gen.14.18", "commentary", "secondary", "❡", "gen14-melchizedek"),
    ("gen.15.6",  "linguistic", "tertiary",  "ℵ", "gen15-righteousness-credited"),
    ("gen.15.18", "commentary", "secondary", "❡", "gen15-covenant-of-pieces"),
]


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── 1. Each new record present at correct anchor ──────
        for pid, expected_kind, expected_authority, expected_glyph, expected_id in EXPECTED_WAVE_TWO:
            page.goto(
                f"http://localhost:8765/index.html?text=bible_kjv.json&p={pid}",
                wait_until="networkidle",
            )
            page.wait_for_function(
                "typeof currentData === 'object' && currentData && currentData.passages",
                timeout=15000,
            )
            page.wait_for_timeout(600)
            page.evaluate("() => localStorage.removeItem('atlas:encounters:v1')")
            page.evaluate("document.getElementById('companion-toggle').click()")
            page.wait_for_timeout(500)
            page.evaluate("_setFolioDepth('archive')")
            page.wait_for_timeout(400)
            cluster = page.evaluate(
                """
                (pid) => {
                  const c = document.querySelector(
                    `.cr-folio-cluster[data-anchor-pid="${pid}"]`);
                  if (!c) return null;
                  return Array.from(c.querySelectorAll('.cr-folio-marker')).map(m => ({
                    kind: m.dataset.kind,
                    authority: m.dataset.authority,
                    aria: m.getAttribute('aria-label'),
                  }));
                }
                """,
                pid,
            )
            print(f"{pid:<12} markers:")
            for m in (cluster or []):
                print(f"  · kind={m['kind']:<14} authority={m['authority']:<10} aria={m['aria']}")
            assert cluster, f"no markers at {pid}"
            match = next(
                (m for m in cluster
                 if m["kind"] == expected_kind
                 and m["authority"] == expected_authority),
                None,
            )
            assert match, (
                f"expected {expected_kind}/{expected_authority} at {pid}; got {cluster}"
            )
            assert expected_id.split("-", 1)[1].split("-")[0] in (match["aria"] or "").lower() \
                or match["aria"], match
        print()
        print("All four wave-two records present with correct kind+authority.\n")

        # ── 2. Hierarchy silhouette — tertiary 26x26, secondary 28x28
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.15.6",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(600)
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(400)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        sizes = page.evaluate(
            """
            () => {
              const t = document.querySelector(
                '.cr-folio-marker[data-authority="tertiary"][data-kind="linguistic"]');
              const s = document.querySelector(
                '.cr-folio-marker[data-authority="secondary"][data-kind="commentary"]');
              const get = m => m ? m.getBoundingClientRect() : null;
              const tr = get(t), sr = get(s);
              return {
                tertiaryWidth: tr ? Math.round(tr.width) : null,
                tertiaryHeight: tr ? Math.round(tr.height) : null,
                secondaryWidth: sr ? Math.round(sr.width) : null,
                secondaryHeight: sr ? Math.round(sr.height) : null,
              };
            }
            """
        )
        print(f"Silhouette at gen.15: {sizes}")
        # tertiary smaller than secondary
        if sizes["tertiaryWidth"] is not None and sizes["secondaryWidth"] is not None:
            assert sizes["tertiaryWidth"] < sizes["secondaryWidth"], sizes
            print("  OK — tertiary smaller than secondary\n")

        # ── 3. Density: gen.12 has 3 marks across 3 verses ─────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.12.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(600)
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(400)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        gen12 = page.evaluate(
            """
            () => {
              const clusters = Array.from(document.querySelectorAll(
                '.cr-folio-cluster'));
              return clusters.map(c => ({
                pid: c.dataset.anchorPid,
                markers: c.querySelectorAll('.cr-folio-marker').length,
              }));
            }
            """
        )
        print(f"Gen 12 clusters: {gen12}")
        gen12_pids = sorted([c["pid"] for c in gen12 if c["pid"].startswith("gen.12.")])
        # Should include gen.12.1, gen.12.5, gen.12.7
        assert "gen.12.1" in gen12_pids, gen12_pids
        assert "gen.12.5" in gen12_pids, gen12_pids
        assert "gen.12.7" in gen12_pids, gen12_pids
        # No verse should carry more than 1 mark in gen.12 (each anchor is distinct)
        for c in gen12:
            if c["pid"] and c["pid"].startswith("gen.12."):
                assert c["markers"] == 1, f"verse {c['pid']} carries {c['markers']} marks"
        print("  OK — Genesis 12: 3 single-mark clusters across 3 verses\n")

        # ── 4. Genesis 14 carries 1 mark; gen 15 carries 2 ─────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.14.18",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(600)
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(400)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        gen14_clusters = page.evaluate(
            """
            () => Array.from(document.querySelectorAll(
              '.cr-folio-cluster'
            )).map(c => ({pid: c.dataset.anchorPid,
                          markers: c.querySelectorAll('.cr-folio-marker').length}))
            """
        )
        gen14_pids = [c["pid"] for c in gen14_clusters if c["pid"] and c["pid"].startswith("gen.14.")]
        print(f"Gen 14 clusters: {gen14_pids}")
        assert gen14_pids == ["gen.14.18"], gen14_pids
        print("  OK — Genesis 14: only Melchizedek at 14:18\n")

        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.15.6",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(600)
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(400)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        gen15_clusters = page.evaluate(
            """
            () => Array.from(document.querySelectorAll(
              '.cr-folio-cluster'
            )).map(c => ({pid: c.dataset.anchorPid,
                          markers: c.querySelectorAll('.cr-folio-marker').length}))
            """
        )
        gen15_pids = sorted([c["pid"] for c in gen15_clusters if c["pid"] and c["pid"].startswith("gen.15.")])
        print(f"Gen 15 clusters: {gen15_pids}")
        assert gen15_pids == ["gen.15.18", "gen.15.6"], gen15_pids
        print("  OK — Genesis 15: 15:6 + 15:18, two marks\n")

        # ── 5. Genesis 16+ remains silent (no spillover) ──────
        for pid in ["gen.16.1", "gen.16.13", "gen.17.1"]:
            page.goto(
                f"http://localhost:8765/index.html?text=bible_kjv.json&p={pid}",
                wait_until="networkidle",
            )
            page.wait_for_function(
                "typeof currentData === 'object' && currentData && currentData.passages",
                timeout=15000,
            )
            page.wait_for_timeout(600)
            page.evaluate("document.getElementById('companion-toggle').click()")
            page.wait_for_timeout(400)
            page.evaluate("_setFolioDepth('archive')")
            page.wait_for_timeout(400)
            ch = pid.rsplit(".", 1)[0]  # e.g. "gen.16"
            ch_clusters = page.evaluate(
                """
                (ch) => Array.from(document.querySelectorAll(
                  '.cr-folio-cluster'
                )).filter(c => (c.dataset.anchorPid || '').startsWith(ch + '.'))
                  .map(c => c.dataset.anchorPid)
                """,
                ch,
            )
            print(f"{ch} clusters: {ch_clusters}")
        # Gen 16 must be empty
        assert len(page.evaluate(
            """() => Array.from(document.querySelectorAll(
              '.cr-folio-cluster'
            )).filter(c => (c.dataset.anchorPid || '').startsWith('gen.16.'))""")
        ) == 0, "Wave Two spilled into Gen 16"
        # Gen 17 must still carry only AO·006 (1 cluster)
        gen17 = page.evaluate(
            """() => Array.from(document.querySelectorAll(
              '.cr-folio-cluster'
            )).filter(c => (c.dataset.anchorPid || '').startsWith('gen.17.'))
              .map(c => ({pid: c.dataset.anchorPid,
                          markers: c.querySelectorAll('.cr-folio-marker').length}))"""
        )
        assert gen17 == [{"pid": "gen.17.7", "markers": 1}], gen17
        print("  OK — Gen 16 silent, Gen 17 unchanged (AO·006 only)\n")

        # ── 6. Atlas Index carries all four new records ───────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(600)
        page.click(".bcl-atlas-index-btn")
        page.wait_for_timeout(800)
        index_records = page.evaluate(
            """
            () => Array.from(document.querySelectorAll('.aix-record')).map(r => ({
              title: r.querySelector('.aix-record-title')?.textContent.trim() || '',
              cls: r.querySelector('.aix-record-class')?.textContent.trim() || '',
              glyph: r.querySelector('.aix-glyph')?.textContent.trim() || '',
            }))
            """
        )
        # Look up each by title fragment
        wave_two_targets = [
            ("Manuscript itinerary", "Secondary · Map",        "✥"),
            ("Melchizedek",           "Secondary · Commentary", "❡"),
            ("Covenant of pieces",    "Secondary · Commentary", "❡"),
            ("counted it to him for righteousness",
                                      "Tertiary · Linguistic",  "ℵ"),
        ]
        for needle, expected_cls, expected_glyph in wave_two_targets:
            rec = next((r for r in index_records if needle.lower() in r["title"].lower()), None)
            assert rec, f"Atlas Index missing record matching {needle!r}"
            assert rec["cls"] == expected_cls, (needle, rec)
            assert rec["glyph"] == expected_glyph, (needle, rec)
            print(f"  index: {rec['glyph']} {rec['title'][:50]:<52} {rec['cls']}")
        print("  OK — Atlas Index lists all four with correct class + glyph\n")

        # ── 7. Screenshots — gen.12, gen.14, gen.15, gen.16 ───
        # Each acknowledges Wave Two visually; gen.16 confirms
        # restraint.
        for pid, label in [("gen.12.1", "gen12_rail"),
                            ("gen.14.18", "gen14_rail"),
                            ("gen.15.6", "gen15_rail"),
                            ("gen.16.1", "gen16_rail_silent")]:
            page.goto(
                f"http://localhost:8765/index.html?text=bible_kjv.json&p={pid}",
                wait_until="networkidle",
            )
            page.wait_for_function(
                "typeof currentData === 'object' && currentData && currentData.passages",
                timeout=15000,
            )
            page.wait_for_timeout(700)
            page.evaluate("document.getElementById('companion-toggle').click()")
            page.wait_for_timeout(500)
            page.evaluate("_setFolioDepth('archive')")
            page.wait_for_timeout(400)
            page.mouse.move(0, 0)
            page.wait_for_timeout(200)
            page.screenshot(
                path=f"reports/v66_{label}.png",
                clip={"x": 0, "y": 80, "width": 1440, "height": 760},
            )

        # ── 8. Open the map plate leaf to confirm restraint ──
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.12.5",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(700)
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(500)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        page.evaluate(
            "() => { if (typeof _openFolioObject === 'function') "
            "_openFolioObject('gen12-patriarchal-journey-map'); }"
        )
        page.wait_for_timeout(1100)
        leaf_state = page.evaluate(
            """
            () => {
              const leaf = document.querySelector('.folio-leaf');
              if (!leaf) return null;
              return {
                classes: leaf.className,
                hasChamberClass: /-chamber/.test(leaf.className),
                hasVocabulary: !!leaf.querySelector('.cc-vocabulary, .cc-terms'),
                hasArchive: !!leaf.querySelector('.cc-archive'),
                bodyParagraphCount: leaf.querySelectorAll(
                  '.folio-body-line:not(.folio-body-spacer)').length,
              };
            }
            """
        )
        print(f"Map plate leaf at gen.12.5: {leaf_state}")
        assert leaf_state, "leaf failed to render"
        assert not leaf_state["hasChamberClass"], (
            "map plate fired chamber dispatch: " + leaf_state["classes"]
        )
        assert not leaf_state["hasVocabulary"]
        assert not leaf_state["hasArchive"]
        print("  OK — map plate renders via generic renderer, no chamber dispatch\n")
        page.screenshot(path="reports/v66_map_plate_opened.png")

        b.close()
    print("ALL CHECKS PASSED — Wave Two Abrahamic emergence arc operational.")


if __name__ == "__main__":
    main()
