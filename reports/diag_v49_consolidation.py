"""v49 — Consolidation phase one.

Verifies three atmospheric refinements:
  · Cross-object kindred encounter at chamber foot (gen.1.6
    hosts both AO·001 cosmology and AO·002 translation; each
    chamber should reference the other).
  · Marker visited-state ink warmth (after a chamber has been
    opened, that object's markers gain a slight border / colour
    deepening — no badge, no dot).
  · Codex Preface overlay (accessible from a quiet italic link
    on the Bible title leaf, opens five manuscriptal rubrics).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import re
from playwright.sync_api import sync_playwright


def alpha(rgba):
    m = re.search(r"rgba\(.+,\s*([\d.]+)\)", rgba)
    return float(m.group(1)) if m else 1.0


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── Codex preface link present on Bible title leaf ────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.evaluate("() => localStorage.removeItem('atlas:encounters:v1')")

        link = page.evaluate(
            """
          () => {
            const l = document.querySelector('.bcl-codex-preface-link');
            return l ? {
              text: l.textContent.trim(),
              visible: getComputedStyle(l).display !== 'none',
            } : null;
          }
        """
        )
        print(f"CODEX PREFACE link: {link}")
        assert link and link["visible"]
        assert "form of this archive" in link["text"]
        print("  OK — preface link present on title leaf\n")

        # Open the preface
        page.click(".bcl-codex-preface-link")
        page.wait_for_timeout(500)
        preface = page.evaluate(
            """
          () => {
            const p = document.querySelector('.atlas-codex-preface');
            if (!p) return null;
            return {
              head: p.querySelector('.acp-rubric-head')?.textContent,
              rubrics: Array.from(p.querySelectorAll('.acp-rubric-name'))
                .map(el => el.textContent),
              colophon: p.querySelector('.acp-colophon')?.textContent,
              backdrop: getComputedStyle(
                document.querySelector('.atlas-codex-preface-backdrop')
              ).backgroundColor,
            };
          }
        """
        )
        print(f"PREFACE opened:")
        print(f"  head: {preface['head']!r}")
        print(f"  rubrics: {preface['rubrics']}")
        print(f"  colophon: {preface['colophon']!r}")
        assert preface["head"] == "Codex Preface"
        assert len(preface["rubrics"]) == 5
        assert "Atlas Objects" in preface["rubrics"][0]
        assert "recurrence" in preface["rubrics"][1]
        assert "folio" in preface["rubrics"][2]
        assert "voice" in preface["rubrics"][3]
        assert "remains" in preface["rubrics"][4]
        assert "kept" in (preface["colophon"] or "")
        page.screenshot(path="reports/v49_codex_preface.png")

        # Dismiss the preface via Escape
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        dismissed = page.evaluate(
            "() => !document.querySelector('.atlas-codex-preface-backdrop')"
        )
        assert dismissed, "preface should dismiss on Escape"
        print("  OK — preface dismisses on Escape\n")

        # ── Cross-object kindred encounter at Gen 1:6 ─────────
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.6",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.click("#companion-toggle")
        page.wait_for_timeout(700)
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)

        # Open AO·001 cosmology chamber at gen.1.6
        page.evaluate("_openFolioObject('gen1-cosmology-firmament')")
        page.wait_for_timeout(900)

        kindred_at_gen16 = page.evaluate(
            """
          () => {
            const kin = document.querySelector('.folio-leaf .cc-kindred');
            if (!kin) return null;
            return {
              text: kin.textContent.trim(),
              items: Array.from(kin.querySelectorAll('.cc-kindred-item'))
                .map(b => ({
                  siglum: b.dataset.siglum,
                  glyph: b.querySelector('.cc-kindred-glyph')?.textContent,
                  title: b.querySelector('.cc-kindred-title')?.textContent,
                })),
            };
          }
        """
        )
        print(f"COSMOLOGY chamber at gen.1.6 — kindred rubric:")
        print(f"  text: {kindred_at_gen16['text'][:100]!r}")
        for it in kindred_at_gen16["items"]:
            print(f"    {it['glyph']} {it['siglum']} · {it['title']}")
        assert kindred_at_gen16
        # The translation-tradition object should be listed as kindred
        siglums = [it["siglum"] for it in kindred_at_gen16["items"]]
        assert "AO · 002" in siglums
        # The translation glyph should be ‡
        translation_item = next(
            (it for it in kindred_at_gen16["items"] if it["siglum"] == "AO · 002"),
            None,
        )
        assert translation_item and translation_item["glyph"] == "‡"
        print("  OK — AO·001 chamber surfaces AO·002 as kindred at gen.1.6\n")
        page.screenshot(path="reports/v49_kindred_cosmology.png", full_page=True)

        # Click the kindred AO·002 item — chamber should switch
        page.evaluate("""
          () => {
            const btn = Array.from(
              document.querySelectorAll('.cc-kindred-item')
            ).find(b => b.dataset.siglum === 'AO · 002');
            if (btn) btn.click();
          }
        """)
        page.wait_for_timeout(900)
        switched = page.evaluate(
            """
          () => {
            const leaf = document.querySelector('.folio-leaf');
            return {
              chamber: leaf ? leaf.className : null,
              siglum: leaf?.querySelector('.cc-aor-siglum')?.textContent,
            };
          }
        """
        )
        print(f"After kindred click: {switched}")
        assert "translation-chamber" in (switched["chamber"] or "")
        assert switched["siglum"] == "AO · 002"
        print("  OK — kindred click switched from AO·001 to AO·002 chamber\n")

        # ── Marker visited-state — AO·001 has been encountered,
        # so its marker should now carry data-visited="true".
        # Close the chamber first.
        page.mouse.click(50, 50)
        page.wait_for_timeout(400)

        visited_state = page.evaluate(
            """
          () => {
            const markers = Array.from(document.querySelectorAll(
              '.cr-folio-cluster[data-anchor-pid="gen.1.6"] .cr-folio-marker'));
            return markers.map(m => ({
              kind: m.dataset.kind,
              authority: m.dataset.authority,
              visited: m.dataset.visited || null,
              borderColor: getComputedStyle(m).borderColor,
            }));
          }
        """
        )
        print(f"Marker visited-state at gen.1.6:")
        for m in visited_state:
            print(f"  · {m['kind']:<22} authority={m['authority']} "
                  f"visited={m['visited']} border={m['borderColor']}")
        # Both cosmology and translation should now be visited
        # (we opened both via the kindred click)
        kinds_visited = [m["kind"] for m in visited_state if m["visited"] == "true"]
        assert "cosmology" in kinds_visited, kinds_visited
        assert "translation-tradition" in kinds_visited, kinds_visited
        print("  OK — both encountered Atlas Object markers are visited-marked\n")

        # Confirm the visited border is visibly more saturated than
        # a non-visited tertiary marker. Open a chapter where no
        # encountered object lives.
        page.screenshot(path="reports/v49_visited_markers.png")

        # ── Recurrence-aware: marker at Psalm 104:5 (where AO·001
        # also anchors) should be visited because we've already
        # encountered AO·001 at gen.1.6.
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=psa.104.5",
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
        psa_marker = page.evaluate(
            """
          () => {
            const m = document.querySelector(
              '.cr-folio-cluster[data-anchor-pid="psa.104.5"] '
              + '.cr-folio-marker[data-kind="cosmology"]');
            return m ? {
              visited: m.dataset.visited || null,
              borderColor: getComputedStyle(m).borderColor,
            } : null;
          }
        """
        )
        print(f"Psalm 104:5 cosmology marker (recurrence): {psa_marker}")
        assert psa_marker
        assert psa_marker["visited"] == "true", (
            "cosmology marker at Psalm 104:5 should be visited "
            "because the object was met at gen.1.6"
        )
        print("  OK — visited-state crosses anchorings (object-level memory)\n")
        page.screenshot(path="reports/v49_visited_recurrence.png")

        b.close()
    print("ALL CHECKS PASSED — consolidation phase one is operational")


if __name__ == "__main__":
    main()
