"""v76 — Atmospheric/material refinement pass.

Verifies the two-move refinement per
LEAF_MATERIAL_INDEPENDENCE_AUDIT.md:

  Move A — Replace warm halo with dark absorption.
    box-shadow:
      0 6px 28px -8px rgba(0,0,0,0.55),   /* weight beneath */
      0 0 100px 16px rgba(0,0,0,0.42);    /* chamber attenuation */
    Both layers are dark (no warm cream halo).

  Move B — Vellum-shift parchment.
    --reader-bg: #f3e8c8 → #ede3cc
    (HSL saturation 64% → 41%; B channel slightly raised)

  Move C — Ink unchanged at #2e2418.

  Doré preserved (box-shadow: none).
  All formalized families preserved.
  AO chambers preserved.

Captures per-family after-screenshots + theme-variant captures.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


SAMPLES = [
    ("gen.1.1",  "gen1-commentary-augustine",       "commentary"),
    ("gen.1.2",  "gen1-linguistic-tohu",            "linguistic"),
    ("gen.1.1",  "gen1-manuscript-opening",         "manuscript"),
    ("gen.22.2", "gen22-mount-moriah",              "architecture"),
    ("gen.1.3",  "gen1-ritual-maariv-aravim",       "ritual"),
    ("gen.1.1",  "gen1-xref-nt-creation",           "cross_reference"),
    ("gen.1.1",  "gen1-cosmology-ane",              "cosmology"),
    ("gen.18.2", "gen18-three-visitors-reception",  "reception"),
    ("gen.1.3",  "dore-creation-of-light",          "dore"),
    ("gen.11.7", "dore-confusion-of-tongues",       "dore_babel"),
    ("gen.1.6",  "gen1-cosmology-firmament",        "ao_cosmology"),
    ("exo.40.34","exo40-sanctuary-glory",           "ao_sanctuary"),
]
THEMES = [
    ("default",  None,       None),
    ("dark",     "#1a1a1e",  "#e0e0e0"),
    ("sepia",    "#e8d5a8",  "#3a2818"),
    ("neutral",  "#f0f0ea",  "#222"),
]

VELLUM_RGB = "rgb(237, 227, 204)"   # #ede3cc
INK_RGB = "rgb(46, 36, 24)"          # #2e2418


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
    page.wait_for_timeout(1300)


def apply_theme(page, bg, fg):
    if bg is None:
        page.evaluate(
            "document.documentElement.style.removeProperty('--reader-bg');"
            "document.documentElement.style.removeProperty('--reader-fg');"
        )
    else:
        page.evaluate(
            f"document.documentElement.style.setProperty('--reader-bg','{bg}');"
            f"document.documentElement.style.setProperty('--reader-fg','{fg}');"
        )
    page.wait_for_timeout(300)


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── Move A — Dark-absorption shadow stack ───────────────────
        print("=== Move A — Dark-absorption shadow stack ===")
        open_leaf(page, "gen.1.1", "gen1-commentary-augustine")
        bs = page.evaluate(
            "(()=>getComputedStyle(document.querySelector('.folio-leaf')).boxShadow)()"
        )
        print(f"  box-shadow: {bs}")
        # The prior warm halo (245, 220, 170) must be GONE; both
        # layers must be dark rgb(0, 0, 0).
        assert "245, 220, 170" not in bs, (
            "warm halo still present — pass failed")
        assert "rgb(0, 0, 0)" in bs or "0, 0, 0" in bs, (
            "dark absorption shadow not present")
        # Both shadow layers should be present.
        assert bs.count("rgba") == 2 or bs.count("rgb(0, 0, 0)") >= 2, (
            f"expected 2 dark layers, got: {bs}")
        print("  OK — warm halo removed; two-layer dark stack "
              "(weight + attenuation) present.\n")

        # ── Move B — Vellum-shift parchment ─────────────────────────
        print("=== Move B — Vellum-shift parchment ===")
        bg = page.evaluate(
            "(()=>getComputedStyle(document.querySelector('.folio-leaf')).backgroundColor)()"
        )
        color = page.evaluate(
            "(()=>getComputedStyle(document.querySelector('.folio-leaf')).color)()"
        )
        print(f"  parchment bg: {bg}  (vellum target {VELLUM_RGB})")
        print(f"  ink color:    {color}  (target {INK_RGB})")
        assert bg == VELLUM_RGB, (bg, VELLUM_RGB)
        assert color == INK_RGB, (color, INK_RGB)
        print("  OK — parchment shifted to vellum; ink preserved.\n")

        # ── Theme-independence ──────────────────────────────────────
        print("=== Theme-independence across reading-room atmospheres ===")
        for theme, bg_val, fg_val in THEMES:
            open_leaf(page, "gen.1.1", "gen1-commentary-augustine")
            apply_theme(page, bg_val, fg_val)
            page.wait_for_timeout(350)
            st = page.evaluate(
                """(() => {
                    const leaf = document.querySelector('.folio-leaf');
                    const s = getComputedStyle(leaf);
                    return { bg: s.backgroundColor, color: s.color, shadow: s.boxShadow };
                })()"""
            )
            print(f"  theme={theme:<8} bg={st['bg']} color={st['color']}")
            assert st["bg"] == VELLUM_RGB, (theme, st["bg"])
            assert st["color"] == INK_RGB, (theme, st["color"])
            # Shadow stack must persist
            assert "245, 220, 170" not in st["shadow"]
        apply_theme(page, None, None)
        print(f"  OK — vellum + dark-absorption stable across "
              f"{len(THEMES)} themes.\n")

        # ── Doré preservation ──────────────────────────────────────
        print("=== Doré preservation (monumental, cathedral-like) ===")
        for pid, rec_id, label in [
            ("gen.1.3",  "dore-creation-of-light",     "creation"),
            ("gen.11.7", "dore-confusion-of-tongues",  "babel"),
            ("gen.4.8",  "dore-cain-slays-abel",       "cain"),
        ]:
            open_leaf(page, pid, rec_id)
            d = page.evaluate(
                """(() => {
                    const leaf = document.querySelector('.folio-leaf');
                    const s = getComputedStyle(leaf);
                    return {
                        bg: s.backgroundColor,
                        boxShadow: s.boxShadow,
                        hasWrap: !!document.querySelector('.folio-plate-wrap'),
                        hasPlaque: !!document.querySelector('.folio-plate-plaque'),
                    };
                })()"""
            )
            print(f"  {label}: bg={d['bg']} shadow={d['boxShadow']} "
                  f"wrap={d['hasWrap']} plaque={d['hasPlaque']}")
            assert d["bg"] in ("rgba(0, 0, 0, 0)", "transparent")
            assert d["boxShadow"] == "none"
            assert d["hasWrap"] and d["hasPlaque"]
        print("  OK — Doré plates preserved (transparent leaf, no "
              "halo or attenuation, plaque intact).\n")

        # ── Family identities preserved (no regression) ────────────
        print("=== Family identities preserved ===")
        family_checks = [
            ("commentary",     "gen.1.1",  "gen1-commentary-augustine",
             dict(bodyMaxWidth="640px", titleFontWeight="400")),
            ("linguistic",     "gen.1.2",  "gen1-linguistic-tohu",
             dict(bodyMaxWidth="560px", titleFontStyle="normal")),
            ("architecture",   "gen.22.2", "gen22-mount-moriah",
             dict(bodyMaxWidth="480px", titleFontVariantCaps="small-caps")),
            ("reception",      "gen.18.2", "gen18-three-visitors-reception",
             dict(bodyMaxWidth="600px")),
            ("manuscript",     "gen.1.1",  "gen1-manuscript-opening",
             dict(bodyMaxWidth="500px", titleFontStyle="normal")),
            ("ritual",         "gen.1.3",  "gen1-ritual-maariv-aravim",
             dict(bodyMaxWidth="560px", titleFontWeight="400")),
            ("cross-ref",      "gen.1.1",  "gen1-xref-nt-creation",
             dict(bodyMaxWidth="540px")),
            ("cosmology",      "gen.1.1",  "gen1-cosmology-ane",
             dict(bodyMaxWidth="620px")),
        ]
        for label, pid, rec_id, exp in family_checks:
            open_leaf(page, pid, rec_id)
            m = page.evaluate(
                """(() => {
                    const leaf = document.querySelector('.folio-leaf');
                    const t = leaf.querySelector('.folio-leaf-title');
                    const b = leaf.querySelector('.folio-body-vertical');
                    const ts = t ? getComputedStyle(t) : {};
                    return {
                        bodyMaxWidth: b ? getComputedStyle(b).maxWidth : null,
                        titleFontStyle: ts.fontStyle,
                        titleFontWeight: ts.fontWeight,
                        titleFontVariantCaps: ts.fontVariantCaps,
                    };
                })()"""
            )
            print(f"  {label:<14}: {m}")
            for k, v in exp.items():
                assert m[k] == v, (label, k, m[k], v)
        print("  OK — all 8 formalized families preserved.\n")

        # ── AO chambers ─────────────────────────────────────────────
        print("=== AO chambers preserved ===")
        open_leaf(page, "gen.1.6", "gen1-cosmology-firmament")
        cosmology = page.evaluate(
            """(() => {
                const leaf = document.querySelector('.folio-leaf');
                return {
                    hasCosmologyChamber: leaf?.classList.contains('cosmology-chamber'),
                    hasCCLede: !!document.querySelector('.cc-lede'),
                    hasCCDiagram: !!document.querySelector('.cc-diagram'),
                };
            })()"""
        )
        print(f"  cosmology: {cosmology}")
        assert cosmology["hasCosmologyChamber"] and cosmology["hasCCLede"]
        open_leaf(page, "exo.40.34", "exo40-sanctuary-glory")
        sanctuary = page.evaluate(
            """(() => {
                const leaf = document.querySelector('.folio-leaf');
                return {
                    hasSanctuaryChamber: leaf?.classList.contains('sanctuary-chamber'),
                    layers: document.querySelectorAll('.sa-layer').length,
                };
            })()"""
        )
        print(f"  sanctuary: {sanctuary}")
        assert sanctuary["hasSanctuaryChamber"] and sanctuary["layers"] == 5
        ao_count = page.evaluate(
            """(() => {
                const ids = new Set();
                const recs = (currentData && currentData.genealogy) || [];
                for (const r of recs) {
                    if (r && r.atlas_object && r.atlas_object.id) ids.add(r.atlas_object.id);
                }
                return ids.size;
            })()"""
        )
        print(f"  AO count: {ao_count}")
        assert ao_count == 12
        print("  OK — chambers + 12 Atlas Objects preserved.\n")

        # ── Per-family after-captures ──────────────────────────────
        print("=== Per-family after-captures ===")
        for pid, rec_id, label in SAMPLES:
            open_leaf(page, pid, rec_id)
            page.screenshot(path=f"reports/v76_after_{label}.png")
            print(f"  captured {label}")

        # ── Theme-variant captures ─────────────────────────────────
        print("\n=== Theme-variant captures (commentary leaf) ===")
        for theme, bg_val, fg_val in THEMES:
            open_leaf(page, "gen.1.1", "gen1-commentary-augustine")
            apply_theme(page, bg_val, fg_val)
            page.wait_for_timeout(400)
            page.screenshot(path=f"reports/v76_after_theme_{theme}.png")
            print(f"  captured theme={theme}")

        b.close()
    print("\nALL CHECKS PASSED — atmospheric/material refinement "
          "operational.")


if __name__ == "__main__":
    main()
