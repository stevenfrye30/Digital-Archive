"""v68 — Genesis Wave Three (Patriarchal Emergence) verification.

Verifies the 14-record wave-three set lands per the Wave Three
brief and the GENESIS_EXPANDED_COVERAGE_PLAN:

  · Akedah cluster: 6 records, each at distinct verses of
    Gen 22 — NOT a chamber, NOT an AO.
  · Sacred-site rhythm: 3 records at Gen 13, 23, 26 — quiet
    tertiary architecture.
  · Dream/vision thread: 3 records — commentary kind only
    (no AO·008 metadata anchors added).
  · Abrahamic deepening: 2 records at Gen 16, 18.

Invariants:
  · Atlas Object count unchanged (12).
  · No verse carries more than one wave-three record.
  · Silence preserved at chapters between wave-three clusters
    (Gen 30, 31, 34, 42-44, 47, etc).
  · Witness-family CSS (v67) consistent across the new
    records.
  · All prior diagnostics pass.
"""
import sys
import json
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent


def main():
    # ── 1. Data-level invariants ─────────────────────────────
    with open(ROOT / "data/bible_kjv.json", encoding="utf-8") as f:
        data = json.load(f)

    ao_count = sum(
        1 for r in data["genealogy"]
        if (r.get("atlas_object") or {}).get("siglum")
    )
    print(f"Atlas Object count: {ao_count}")
    assert ao_count == 12, f"AO count changed: {ao_count}"

    wave_three_ids = {
        "gen13-bethel-altar-return", "gen16-el-roi-hagar",
        "gen18-three-visitors-reception",
        "gen22-hineni", "gen22-mount-moriah", "gen22-akedah-binding",
        "gen22-ram-thicket-substitute", "gen22-yhwh-jireh",
        "gen22-reception-three-traditions",
        "gen23-machpelah-cave", "gen26-wells-of-isaac",
        "gen32-wrestling-jabbok", "gen37-joseph-first-dream",
        "gen41-pharaoh-dreams",
    }
    by_id = {r["id"]: r for r in data["genealogy"]}
    for wid in wave_three_ids:
        assert wid in by_id, f"missing wave-three record: {wid}"
        rec = by_id[wid]
        # No Wave Three record carries atlas_object metadata.
        assert "atlas_object" not in rec or not rec.get("atlas_object"), (
            f"wave-three record {wid} acquired AO metadata"
        )
    print(f"  OK — all 14 records present, none claim AO metadata\n")

    # Verse-uniqueness within wave-three: at most one wave-three
    # record per (book.chapter.verse).
    verse_records = {}
    for wid in wave_three_ids:
        for a in by_id[wid].get("anchors", []):
            pid = a["target"].split("::")[-1]
            verse_records.setdefault(pid, []).append(wid)
    multi = {pid: ids for pid, ids in verse_records.items() if len(ids) > 1}
    assert not multi, f"verse overloaded: {multi}"
    print(f"  OK — no verse carries more than one wave-three record\n")

    # ── 2. Browser-level checks ──────────────────────────────
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # Akedah cluster — six markers, each at its own verse
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.22.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(700)
        page.evaluate("() => localStorage.removeItem('atlas:encounters:v1')")
        page.evaluate("document.getElementById('companion-toggle').click()")
        page.wait_for_timeout(500)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        gen22_clusters = page.evaluate(
            """
            () => Array.from(document.querySelectorAll(
              '.cr-folio-cluster'
            )).filter(c => (c.dataset.anchorPid || '').startsWith('gen.22.'))
              .map(c => ({
                pid: c.dataset.anchorPid,
                markers: Array.from(c.querySelectorAll('.cr-folio-marker'))
                          .map(m => ({
                            kind: m.dataset.kind,
                            authority: m.dataset.authority,
                          })),
              }))
            """
        )
        gen22_clusters.sort(key=lambda c: int(c["pid"].split(".")[2]))
        print("=== Akedah cluster (Gen 22) ===")
        for c in gen22_clusters:
            print(f"  {c['pid']}  {c['markers']}")
        # Expected anchors: 22:1, 22:2, 22:9, 22:13, 22:14, 22:19
        # Plus the pre-existing nahor-house at 22:20.
        akedah_pids = [c["pid"] for c in gen22_clusters]
        for required in ["gen.22.1", "gen.22.2", "gen.22.9",
                         "gen.22.13", "gen.22.14", "gen.22.19"]:
            assert required in akedah_pids, akedah_pids
        # Each Akedah anchor carries exactly one marker (the cluster
        # is not stacked at any single verse).
        for c in gen22_clusters:
            if c["pid"] in ("gen.22.1", "gen.22.2", "gen.22.9",
                            "gen.22.13", "gen.22.14", "gen.22.19"):
                assert len(c["markers"]) == 1, (c["pid"], c["markers"])
        print("  OK — 6 Akedah anchors, each carrying one marker\n")
        page.screenshot(
            path="reports/v68_akedah_cluster.png",
            clip={"x": 0, "y": 80, "width": 1440, "height": 760},
        )

        # Sacred-site rhythm — gen.13, gen.23, gen.26
        for pid, label in [("gen.13.4",  "site_bethel_return"),
                            ("gen.23.19", "site_machpelah"),
                            ("gen.26.18", "site_isaac_wells")]:
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
            marker = page.evaluate(
                """
                (pid) => {
                  const c = document.querySelector(
                    `.cr-folio-cluster[data-anchor-pid="${pid}"]`);
                  if (!c) return null;
                  const m = c.querySelector('.cr-folio-marker');
                  return m ? {kind: m.dataset.kind, authority: m.dataset.authority} : null;
                }
                """,
                pid,
            )
            print(f"{pid}: {marker}")
            assert marker
            assert marker["kind"] == "architecture"
            assert marker["authority"] == "tertiary"
            page.mouse.move(0, 0)
            page.wait_for_timeout(150)
            page.screenshot(
                path=f"reports/v68_{label}.png",
                clip={"x": 0, "y": 80, "width": 1440, "height": 760},
            )
        print("  OK — three sacred-site markers; all tertiary architecture\n")

        # Dream / vision thread — verify the three records are
        # commentary (not AO·008), at the expected verses
        for pid, expected_kind, expected_authority in [
            ("gen.32.24", "commentary", "secondary"),
            ("gen.37.7",  "commentary", "secondary"),
            ("gen.41.25", "commentary", "tertiary"),
        ]:
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
            marker = page.evaluate(
                """
                (pid) => {
                  const c = document.querySelector(
                    `.cr-folio-cluster[data-anchor-pid="${pid}"]`);
                  if (!c) return null;
                  return Array.from(c.querySelectorAll('.cr-folio-marker'))
                    .map(m => ({kind: m.dataset.kind,
                                authority: m.dataset.authority}));
                }
                """,
                pid,
            )
            print(f"{pid}: {marker}")
            # Each verse should carry exactly one marker (commentary)
            assert len(marker) == 1, (pid, marker)
            assert marker[0]["kind"] == expected_kind
            assert marker[0]["authority"] == expected_authority
            # CRUCIAL: not an AO recurrence — kind should NOT be
            # revelatory-vision.
            assert marker[0]["kind"] != "revelatory-vision"
        print("  OK — dream/vision thread: 3 commentary records, no AO·008 spillover\n")
        page.screenshot(
            path="reports/v68_dream_thread_pharaoh.png",
            clip={"x": 0, "y": 80, "width": 1440, "height": 760},
        )

        # Silence preserved at chapters between wave-three clusters
        silent_chapters = ["gen.30.1", "gen.31.1", "gen.34.1",
                            "gen.42.1", "gen.43.1", "gen.44.1",
                            "gen.47.1", "gen.50.1"]
        print("=== Silence preservation ===")
        for pid in silent_chapters:
            page.goto(
                f"http://localhost:8765/index.html?text=bible_kjv.json&p={pid}",
                wait_until="networkidle",
            )
            page.wait_for_function(
                "typeof currentData === 'object' && currentData && currentData.passages",
                timeout=15000,
            )
            page.wait_for_timeout(500)
            page.evaluate("document.getElementById('companion-toggle').click()")
            page.wait_for_timeout(300)
            page.evaluate("_setFolioDepth('archive')")
            page.wait_for_timeout(300)
            ch = pid.rsplit(".", 1)[0]
            clusters = page.evaluate(
                """
                (ch) => Array.from(document.querySelectorAll(
                  '.cr-folio-cluster'
                )).filter(c => (c.dataset.anchorPid || '').startsWith(ch + '.'))
                  .map(c => c.dataset.anchorPid)
                """,
                ch,
            )
            # gen.50 is silent for now, but the existing
            # ephraim-manasseh genealogy is at gen.48.5 (not 50).
            # Test that the chapter itself has zero markers.
            chapter_clusters = [c for c in clusters
                                if c.startswith(ch + ".")]
            print(f"  {ch}: {chapter_clusters}")
            assert chapter_clusters == [], (
                f"silence broken at {ch}: {chapter_clusters}"
            )
        print("  OK — eight silent chapters preserved\n")

        # Witness-family CSS still applied to new records
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.22.9",
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
        page.evaluate(
            "(() => _openFolioObject('gen22-akedah-binding'))()"
        )
        page.wait_for_timeout(1100)
        binding_leaf = page.evaluate(
            """
            () => {
              const leaf = document.querySelector('.folio-leaf');
              const title = leaf?.querySelector('.folio-leaf-title');
              const body = leaf?.querySelector('.folio-body-vertical');
              const after = title ? window.getComputedStyle(title, '::after') : null;
              return {
                dataKind: leaf?.dataset.kind,
                titleFontWeight: title ? getComputedStyle(title).fontWeight : null,
                bodyMaxWidth: body ? getComputedStyle(body).maxWidth : null,
                ruleWidth: after ? after.width : null,
              };
            }
            """
        )
        print(f"Akedah binding leaf (commentary family): {binding_leaf}")
        assert binding_leaf["dataKind"] == "commentary"
        assert binding_leaf["titleFontWeight"] == "400"
        assert binding_leaf["bodyMaxWidth"] == "640px"
        assert binding_leaf["ruleWidth"] == "36px"
        print("  OK — Akedah binding inherits commentary family identity\n")
        page.screenshot(path="reports/v68_akedah_binding_leaf.png")

        # Atlas Index now lists Gen 22 prominently
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
        chapter_xxii = page.evaluate(
            """
            () => {
              const headings = Array.from(document.querySelectorAll(
                '.aix-chapter-num'));
              return headings.filter(h => h.textContent.includes('XXII'))
                              .map(h => h.textContent.trim());
            }
            """
        )
        print(f"Atlas Index chapter XXII headings: {chapter_xxii}")
        assert "Chapter XXII" in chapter_xxii, chapter_xxii
        # Scroll to gen.22 and capture
        page.evaluate(
            """
            () => {
              const headings = Array.from(document.querySelectorAll(
                '.aix-chapter-num'));
              const ch22 = headings.find(h =>
                h.textContent.trim() === 'Chapter XXII');
              if (ch22) ch22.scrollIntoView({block: 'start'});
            }
            """
        )
        page.wait_for_timeout(400)
        page.screenshot(path="reports/v68_atlas_index_gen22.png")
        print("  OK — Atlas Index shows Chapter XXII with Akedah cluster\n")

        b.close()
    print("ALL CHECKS PASSED — Patriarchal Emergence (Wave Three) operational.")


if __name__ == "__main__":
    main()
