"""v67 — Witness family before-state probe.

Captures the current rendering of commentary and linguistic
witnesses so we have a baseline for the family-identity
refinement. Also captures Doré + AO chamber leaves to ensure
coexistence after the refinement.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


SAMPLES = [
    # (pid, record_id, label)
    ("gen.1.1",   "gen1-commentary-augustine",        "commentary_augustine_before"),
    ("gen.14.18", "gen14-melchizedek",                "commentary_melchizedek_before"),
    ("gen.15.18", "gen15-covenant-of-pieces",         "commentary_covenant_pieces_before"),
    ("gen.1.1",   "gen1-linguistic-bereshit",         "linguistic_bereshit_before"),
    ("gen.1.2",   "gen1-linguistic-tohu",             "linguistic_tohu_before"),
    ("gen.15.6",  "gen15-righteousness-credited",     "linguistic_righteousness_before"),
    ("gen.1.3",   "dore-creation-of-light",           "plate_dore_before"),
    ("gen.1.6",   "gen1-cosmology-firmament",         "chamber_cosmology_before"),
]


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        for pid, rec_id, label in SAMPLES:
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
            page.evaluate(
                f"(() => _openFolioObject('{rec_id}'))()"
            )
            page.wait_for_timeout(1200)
            # Capture computed metrics on the rendered leaf.
            metrics = page.evaluate(
                """
                () => {
                  const leaf = document.querySelector('.folio-leaf');
                  if (!leaf) return null;
                  const title = leaf.querySelector('.folio-leaf-title');
                  const verse = leaf.querySelector('.folio-leaf-verse');
                  const body = leaf.querySelector('.folio-body-vertical, .cc-lede, .tc-lede');
                  const get = (el, prop) => el ? getComputedStyle(el)[prop] : null;
                  return {
                    leafClasses: leaf.className,
                    leafDataKind: leaf.dataset.kind,
                    leafDataAuthority: leaf.dataset.authority,
                    leafWidth: Math.round(leaf.getBoundingClientRect().width),
                    leafMaxWidth: get(leaf, 'maxWidth'),
                    titleFontSize: get(title, 'fontSize'),
                    titleFontStyle: get(title, 'fontStyle'),
                    titleFontWeight: get(title, 'fontWeight'),
                    verseFontSize: get(verse, 'fontSize'),
                    bodyFontSize: get(body, 'fontSize'),
                    bodyLineHeight: get(body, 'lineHeight'),
                    bodyMaxWidth: get(body, 'maxWidth'),
                    bodyMargin: get(body, 'margin'),
                  };
                }
                """
            )
            print(f"=== {label} ({rec_id}) ===")
            for k, v in (metrics or {}).items():
                print(f"  {k}: {v}")
            print()
            page.screenshot(path=f"reports/v67_{label}.png")

        b.close()


if __name__ == "__main__":
    main()
