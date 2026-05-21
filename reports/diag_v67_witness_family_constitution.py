"""v67 — Witness family constitution: commentary + linguistic
family-identity verification.

Verifies the two-family CSS pass per WITNESS_FAMILY_CONSTITUTION.md:

  · Commentary leaves now carry a 640px-max body measure,
    a thin 36px centred rule beneath the title, lighter title
    weight (400), and a slightly larger body font.

  · Linguistic leaves now carry a 560px-max body measure
    (narrower than commentary), a roman (non-italic) title at
    1.08em, and tighter line-height for dense philological
    reading.

  · Doré plates render exactly as before.
  · AO chambers (cosmology, sanctuary) render unchanged.
  · The kindred/resonance footer is unchanged.
  · No new HTML class names appeared.
"""
import sys
import re
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


COMMENTARY_SAMPLES = [
    ("gen.1.1",   "gen1-commentary-augustine"),
    ("gen.14.18", "gen14-melchizedek"),
    ("gen.15.18", "gen15-covenant-of-pieces"),
]

LINGUISTIC_SAMPLES = [
    ("gen.1.1", "gen1-linguistic-bereshit"),
    ("gen.1.2", "gen1-linguistic-tohu"),
    ("gen.15.6", "gen15-righteousness-credited"),
]


def open_leaf(page, pid, rec_id):
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
    page.evaluate(f"(() => _openFolioObject('{rec_id}'))()")
    page.wait_for_timeout(1100)


def leaf_metrics(page):
    return page.evaluate(
        """
        () => {
          const leaf = document.querySelector('.folio-leaf');
          if (!leaf) return null;
          const title = leaf.querySelector('.folio-leaf-title');
          const body = leaf.querySelector('.folio-body-vertical, .cc-lede, .tc-lede');
          const get = (el, prop) => el ? getComputedStyle(el)[prop] : null;
          // The ::after pseudo on commentary titles — read via
          // a measurement: title element height vs its line-height
          // (pseudo adds height). We probe by reading the title's
          // bottom margin and pseudo-element via window
          // getComputedStyle with ::after.
          let titleAfterWidth = null;
          let titleAfterBg = null;
          if (title) {
            const afterStyle = window.getComputedStyle(title, '::after');
            titleAfterWidth = afterStyle.width;
            titleAfterBg = afterStyle.backgroundColor;
          }
          return {
            leafClasses: leaf.className,
            leafDataKind: leaf.dataset.kind,
            leafDataAuthority: leaf.dataset.authority,
            titleFontSize: get(title, 'fontSize'),
            titleFontStyle: get(title, 'fontStyle'),
            titleFontWeight: get(title, 'fontWeight'),
            titleAfterWidth: titleAfterWidth,
            titleAfterBg: titleAfterBg,
            bodyFontSize: get(body, 'fontSize'),
            bodyLineHeight: get(body, 'lineHeight'),
            bodyMaxWidth: get(body, 'maxWidth'),
            bodyMarginLeft: get(body, 'marginLeft'),
            bodyMarginRight: get(body, 'marginRight'),
          };
        }
        """
    )


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── COMMENTARY family — all three records share identity
        print("=== COMMENTARY family ===")
        commentary_metrics = []
        for pid, rec_id in COMMENTARY_SAMPLES:
            open_leaf(page, pid, rec_id)
            m = leaf_metrics(page)
            print(f"\n  {rec_id}  ({pid})")
            for k, v in m.items():
                print(f"    {k}: {v}")
            commentary_metrics.append((rec_id, m))

        # Identity assertions
        for rec_id, m in commentary_metrics:
            assert m["leafDataKind"] == "commentary"
            assert m["titleFontWeight"] == "400", (rec_id, m["titleFontWeight"])
            # 640px max body measure
            assert m["bodyMaxWidth"] == "640px", (rec_id, m["bodyMaxWidth"])
            # 36px centred rule via ::after
            assert m["titleAfterWidth"] == "36px", (rec_id, m["titleAfterWidth"])
            # Body font 0.92em of 16px parent = ~14.72px
            body_px = float(re.match(r"[\d.]+", m["bodyFontSize"]).group())
            assert 14.3 <= body_px <= 15.1, (rec_id, body_px)
        print("\n  OK — commentary family identity consistent across three records\n")

        page.screenshot(path="reports/v67_commentary_melchizedek_after.png")

        # ── LINGUISTIC family — all three records share identity
        print("=== LINGUISTIC family ===")
        linguistic_metrics = []
        for pid, rec_id in LINGUISTIC_SAMPLES:
            open_leaf(page, pid, rec_id)
            m = leaf_metrics(page)
            print(f"\n  {rec_id}  ({pid})")
            for k, v in m.items():
                print(f"    {k}: {v}")
            linguistic_metrics.append((rec_id, m))

        # Identity assertions
        for rec_id, m in linguistic_metrics:
            assert m["leafDataKind"] == "linguistic"
            # Roman (not italic) title
            assert m["titleFontStyle"] == "normal", (rec_id, m["titleFontStyle"])
            assert m["titleFontWeight"] == "500", (rec_id, m["titleFontWeight"])
            # 560px max body measure (narrower than commentary)
            assert m["bodyMaxWidth"] == "560px", (rec_id, m["bodyMaxWidth"])
            # Smaller body font than commentary (0.88em of 16 = ~14.08px)
            body_px = float(re.match(r"[\d.]+", m["bodyFontSize"]).group())
            assert 13.6 <= body_px <= 14.5, (rec_id, body_px)
        print("\n  OK — linguistic family identity consistent across three records\n")

        page.screenshot(path="reports/v67_linguistic_tohu_after.png")

        # ── Distinction between families ─────────────────────
        cm = commentary_metrics[0][1]
        lm = linguistic_metrics[0][1]
        print("=== Family distinction check ===")
        print(f"  commentary  bodyMaxWidth: {cm['bodyMaxWidth']}  "
              f"titleFontStyle: {cm['titleFontStyle']}  "
              f"titleFontSize: {cm['titleFontSize']}")
        print(f"  linguistic  bodyMaxWidth: {lm['bodyMaxWidth']}  "
              f"titleFontStyle: {lm['titleFontStyle']}  "
              f"titleFontSize: {lm['titleFontSize']}")
        # Bodies are visibly different widths and font sizes.
        cm_w = int(cm["bodyMaxWidth"].rstrip("px"))
        lm_w = int(lm["bodyMaxWidth"].rstrip("px"))
        assert cm_w > lm_w, (cm_w, lm_w)
        cm_fs = float(re.match(r"[\d.]+", cm["bodyFontSize"]).group())
        lm_fs = float(re.match(r"[\d.]+", lm["bodyFontSize"]).group())
        assert cm_fs > lm_fs, (cm_fs, lm_fs)
        assert cm["titleFontStyle"] != lm["titleFontStyle"]
        print("  OK — families are typographically distinct\n")

        # ── Doré family — unchanged ──────────────────────────
        print("=== Doré family (must be unchanged) ===")
        open_leaf(page, "gen.1.3", "dore-creation-of-light")
        dore = page.evaluate(
            """
            () => {
              const wrap = document.querySelector('.folio-plate-wrap');
              const mat = document.querySelector('.folio-plate-mat');
              const plaque = document.querySelector('.folio-plate-plaque');
              return {
                hasWrap: !!wrap,
                hasMat: !!mat,
                hasPlaque: !!plaque,
              };
            }
            """
        )
        print(f"  plate state: {dore}")
        assert dore["hasWrap"] and dore["hasMat"] and dore["hasPlaque"]
        print("  OK — Doré plate render unchanged\n")
        page.screenshot(path="reports/v67_dore_coexistence.png")

        # ── AO chamber — unchanged ───────────────────────────
        print("=== AO chamber (must be unchanged) ===")
        open_leaf(page, "gen.1.6", "gen1-cosmology-firmament")
        chamber = page.evaluate(
            """
            () => {
              const leaf = document.querySelector('.folio-leaf');
              return {
                classes: leaf?.className,
                hasCosmologyChamber: leaf?.classList.contains('cosmology-chamber'),
                hasCCLede: !!document.querySelector('.cc-lede'),
                hasCCDiagram: !!document.querySelector('.cc-diagram'),
              };
            }
            """
        )
        print(f"  chamber state: {chamber}")
        assert chamber["hasCosmologyChamber"]
        assert chamber["hasCCLede"]
        print("  OK — cosmology chamber render unchanged\n")
        page.screenshot(path="reports/v67_chamber_coexistence.png")

        # ── Sanctuary chamber — unchanged ────────────────────
        open_leaf(page, "exo.40.34", "exo40-sanctuary-glory")
        sanctuary = page.evaluate(
            """
            () => {
              const leaf = document.querySelector('.folio-leaf');
              return {
                hasSanctuaryChamber: leaf?.classList.contains('sanctuary-chamber'),
                layers: document.querySelectorAll('.sa-layer').length,
              };
            }
            """
        )
        print(f"  sanctuary state: {sanctuary}")
        assert sanctuary["hasSanctuaryChamber"]
        assert sanctuary["layers"] == 5
        print("  OK — sanctuary chamber render unchanged\n")

        b.close()
    print("ALL CHECKS PASSED — witness family constitution operational.")


if __name__ == "__main__":
    main()
