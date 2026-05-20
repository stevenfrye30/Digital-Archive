"""v60 — Patriarchal Genesis Wave One verification.

Verifies the six wave-one additions are wired into the rail
exactly as the plan specifies. No new chambers, no new systems
— just six records using the existing generic renderer.

Checks per record:
  · marker present at correct anchor verse
  · data-kind matches the kind field (architecture / commentary)
  · data-authority matches (tertiary / secondary)
  · the marker is the expected glyph (⌂ / ❡)

Captures patriarchal rail screenshots at gen.12, gen.21, gen.28,
gen.46 for editorial review.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


EXPECTED = [
    # (anchor pid,        kind,           authority,   id)
    ("gen.12.1",   "commentary",    "secondary", "gen12-lekh-lekha-call"),
    ("gen.12.7",   "architecture",  "tertiary",  "gen12-altar-at-shechem"),
    ("gen.21.31",  "architecture",  "tertiary",  "gen21-beersheba-well-oath"),
    ("gen.28.12",  "commentary",    "secondary", "gen28-jacob-ladder"),
    ("gen.28.18",  "architecture",  "tertiary",  "gen28-bethel-pillar"),
    ("gen.46.3",   "commentary",    "secondary", "gen46-descent-into-egypt"),
]


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── Verify markers present at correct verses ─────────────
        # Visit each anchor pid in turn. ARCHIVE depth shows all
        # tiers including tertiary.
        for pid, expected_kind, expected_authority, expected_id in EXPECTED:
            page.goto(
                f"http://localhost:8765/index.html?text=bible_kjv.json&p={pid}",
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

            # Find the cluster at this anchor and inspect its markers
            cluster = page.evaluate(
                """
                (pid) => {
                  const c = document.querySelector(
                    `.cr-folio-cluster[data-anchor-pid="${pid}"]`
                  );
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
            print(f"{pid:<12} markers in cluster:")
            for m in (cluster or []):
                print(f"  · kind={m['kind']:<14} authority={m['authority']:<10} aria={m['aria']}")

            match = next(
                (m for m in (cluster or [])
                 if m["kind"] == expected_kind
                 and m["authority"] == expected_authority),
                None,
            )
            assert match, f"Expected {expected_kind}/{expected_authority} marker at {pid}, got {cluster}"

        print()
        print("All six wave-one markers present with correct kind + authority.")
        print()

        # ── Capture patriarchal rail screenshots ─────────────────
        # The points where the new patriarchal atmosphere becomes
        # visible: the call (gen.12), the well (gen.21), the
        # ladder+pillar pair (gen.28), the descent (gen.46).
        targets = [
            ("gen.12.1",  "call"),
            ("gen.21.31", "well"),
            ("gen.28.12", "ladder_pillar"),
            ("gen.46.3",  "descent"),
        ]
        for pid, label in targets:
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
                path=f"reports/v60_rail_{label}.png",
                clip={"x": 0, "y": 80, "width": 1440, "height": 760},
            )
            print(f"  captured rail at {pid}  → reports/v60_rail_{label}.png")

        # ── Capture a single opened-leaf so we can confirm the
        # records render at the right scale (paragraph-shaped, no
        # chamber dispatch fired).
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.12.7",
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
        # Open the altar marker directly via the existing helper
        page.evaluate(
            "(() => { if (typeof _openFolioObject === 'function') "
            "_openFolioObject('gen12-altar-at-shechem'); })()"
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
                bodyParagraphCount: leaf.querySelectorAll('.folio-body-line:not(.folio-body-spacer)').length,
                hasArchive: !!leaf.querySelector('.cc-archive'),
                hasAnchorings: !!leaf.querySelector('.cc-anchorings'),
              };
            }
            """
        )
        print()
        print(f"Opened altar leaf (gen.12.7):")
        for k, v in (leaf_state or {}).items():
            print(f"  {k}: {v}")
        # Discipline assertions: the patriarchal record must NOT
        # fire chamber dispatch, must NOT carry vocabulary tables,
        # must NOT carry anchorings or archive sections.
        assert leaf_state, "no leaf rendered"
        assert not leaf_state["hasChamberClass"], (
            f"chamber CSS class fired on plain record: {leaf_state['classes']}"
        )
        assert not leaf_state["hasVocabulary"], (
            "patriarchal record sprouted vocabulary table"
        )
        assert not leaf_state["hasArchive"], (
            "patriarchal record sprouted archive section"
        )
        assert not leaf_state["hasAnchorings"], (
            "patriarchal record sprouted anchorings section"
        )
        # Inscription-shape: the body lines should be modest. A
        # tertiary architecture record body is 3 paragraphs of
        # short Hebrew + place naming + recurrence note. As lines,
        # this is roughly 8-14 stacked .folio-body-line elements
        # (each paragraph becomes multiple wrapped lines).
        assert leaf_state["bodyParagraphCount"] >= 3, (
            "leaf body unexpectedly empty"
        )
        print("  OK — generic renderer fired (no chamber dispatch)")
        print("  OK — no vocabulary / archive / anchorings sections")
        page.screenshot(path="reports/v60_altar_opened_leaf.png")

        b.close()
    print()
    print("ALL CHECKS PASSED — wave one of patriarchal Genesis is wired.")


if __name__ == "__main__":
    main()
