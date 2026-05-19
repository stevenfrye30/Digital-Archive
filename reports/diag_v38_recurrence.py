"""v38 — recurring Atlas Object encounter continuity.

Verifies:
  1. Encounter memory persists per Atlas Object in localStorage.
  2. When the reader meets the same object through a different
     anchoring, the chamber surfaces a quiet recurrence rubric.
  3. The firmament record now anchors on Genesis 1:6, Psalm 104:5,
     and Job 38:4 — markers actually appear at each.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent


def main():
    # ── Data assertion: three canon anchors ─────────────────────
    with open(ROOT / "data/bible_kjv.json", encoding="utf-8") as f:
        data = json.load(f)
    rec = next(r for r in data["genealogy"]
               if r["id"] == "gen1-cosmology-firmament")
    anchors = [a["target"].split("::").pop() for a in rec.get("anchors", [])]
    print(f"DATA — firmament anchors: {anchors}")
    assert "gen.1.6" in anchors
    assert "psa.104.5" in anchors
    assert "job.38.4" in anchors
    print("OK — data carries three canon anchorings\n")

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── First encounter: Genesis 1:6 ───────────────────────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.6",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        # Clear any prior encounter state
        page.evaluate(
            "() => localStorage.removeItem('atlas:encounters:v1')"
        )
        page.click("#companion-toggle")
        page.wait_for_timeout(700)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        page.evaluate("_openFolioObject('gen1-cosmology-firmament')")
        page.wait_for_timeout(800)

        first_state = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.cosmology-chamber');
            const recur = leaf?.querySelector('.cc-recurrence-rubric');
            const stored = JSON.parse(localStorage.getItem('atlas:encounters:v1') || '{}');
            return {
              hasRecurrence: !!recur,
              recurrenceText: recur?.textContent || null,
              stored,
            };
          }
        """
        )
        print("FIRST encounter (Genesis 1:6):")
        print(f"  recurrence rubric: {first_state['hasRecurrence']} "
              f"(text: {first_state['recurrenceText']!r})")
        print(f"  stored: {first_state['stored']}")
        assert not first_state["hasRecurrence"], (
            "should not show recurrence on first encounter"
        )
        # Encounter map records first encounter
        oid = "atlas:object:cosmology:ane-three-tier"
        assert oid in first_state["stored"]
        first = first_state["stored"][oid]["first"]
        assert first["pid"] == "gen.1.6"
        assert "Genesis 1:6" in first["ref"]
        print("  OK — first encounter stored, no rubric shown")
        page.screenshot(path="reports/v38_first_encounter_gen1.png")

        # Dismiss the chamber
        page.mouse.click(50, 50)
        page.wait_for_timeout(400)

        # ── Navigate to Psalm 104 and verify a folio marker exists
        # for the same Atlas Object at psa.104.5.
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=psa.104.5",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(900)
        page.click("#companion-toggle")
        page.wait_for_timeout(700)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)

        psalm_marker = page.evaluate(
            """
          () => {
            const cluster = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="psa.104.5"]');
            if (!cluster) return null;
            const marker = cluster.querySelector('.cr-folio-marker');
            return {
              clusterPid: cluster.dataset.anchorPid,
              markerKind: marker?.dataset.kind,
              markerAuthority: marker?.dataset.authority,
              markerAria: marker?.getAttribute('aria-label'),
            };
          }
        """
        )
        print(f"\nPSALM 104 marker present: {psalm_marker}")
        assert psalm_marker is not None
        assert psalm_marker["clusterPid"] == "psa.104.5"
        assert psalm_marker["markerKind"] == "cosmology"
        assert psalm_marker["markerAuthority"] == "tertiary"
        print("  OK — Atlas Object marker recurs at Psalm 104:5")
        page.screenshot(path="reports/v38_psalm_104_marker.png")

        # ── Second encounter: open the chamber from Psalm 104:5
        page.evaluate("_openFolioObject('gen1-cosmology-firmament')")
        page.wait_for_timeout(800)
        second_state = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.cosmology-chamber');
            const recur = leaf?.querySelector('.cc-recurrence-rubric');
            const lead = recur?.querySelector('.ccr-lead')?.textContent;
            const where = recur?.querySelector('.ccr-where')?.textContent;
            const verse = leaf?.querySelector('.folio-leaf-verse')?.textContent;
            const stored = JSON.parse(localStorage.getItem('atlas:encounters:v1') || '{}');
            return {
              hasRecurrence: !!recur,
              recurrenceLead: lead,
              recurrenceWhere: where,
              chamberVerse: verse,
              stored,
            };
          }
        """
        )
        print(f"\nSECOND encounter (Psalm 104:5):")
        print(f"  chamber verse: {second_state['chamberVerse']!r}")
        print(f"  recurrence rubric: {second_state['hasRecurrence']}")
        print(f"    lead: {second_state['recurrenceLead']!r}")
        print(f"    where: {second_state['recurrenceWhere']!r}")
        print(f"  stored seenAt: {second_state['stored'][oid].get('seenAt')}")
        assert second_state["hasRecurrence"], (
            "recurrence rubric should appear on second-anchoring encounter"
        )
        assert second_state["recurrenceLead"] == "First encountered"
        assert "Genesis 1:6" in (second_state["recurrenceWhere"] or "")
        # The chamber's own verse line should now read Psa 104:5
        chamber_v = second_state["chamberVerse"] or ""
        assert ("Psa" in chamber_v or "Psalm" in chamber_v) and "104:5" in chamber_v, chamber_v
        # The encounter map now records both anchorings as seen
        seen = second_state["stored"][oid].get("seenAt", {})
        assert "gen.1.6" in seen and "psa.104.5" in seen
        print("  OK — recurrence rubric appears; both anchorings remembered")
        page.screenshot(path="reports/v38_second_encounter_psalm.png")

        # ── Third encounter: Job 38:4 — same recurrence behavior
        page.mouse.click(50, 50)
        page.wait_for_timeout(400)
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=job.38.4",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(900)
        page.click("#companion-toggle")
        page.wait_for_timeout(700)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        # Verify marker at job.38.4
        job_marker = page.evaluate(
            """
          () => !!document.querySelector(
            '.cr-folio-cluster[data-anchor-pid="job.38.4"] .cr-folio-marker[data-kind="cosmology"]')
        """
        )
        assert job_marker, "marker missing at Job 38:4"
        print(f"\nJOB 38 marker present: {job_marker}")
        page.evaluate("_openFolioObject('gen1-cosmology-firmament')")
        page.wait_for_timeout(800)
        third = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf.cosmology-chamber');
            const recur = leaf?.querySelector('.cc-recurrence-rubric');
            const where = recur?.querySelector('.ccr-where')?.textContent;
            const verse = leaf?.querySelector('.folio-leaf-verse')?.textContent;
            return {
              hasRecurrence: !!recur,
              recurrenceWhere: where,
              chamberVerse: verse,
            };
          }
        """
        )
        print(f"THIRD encounter (Job 38:4): {third}")
        assert third["hasRecurrence"]
        # Still points to the FIRST encounter (Genesis), not Psalm
        assert "Genesis 1:6" in (third["recurrenceWhere"] or "")
        assert "Job" in (third["chamberVerse"] or "")
        print("  OK — recurrence rubric still names the first encounter")
        page.screenshot(path="reports/v38_third_encounter_job.png")

        b.close()
    print("\nALL CHECKS PASSED — Atlas Object recurrence is live")


if __name__ == "__main__":
    main()
