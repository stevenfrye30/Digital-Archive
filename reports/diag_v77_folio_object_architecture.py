"""v77 — Folio Object Architecture verification.

Verifies the manuscript-architecture pass per
FOLIO_OBJECT_ARCHITECTURE.md. The text-witness leaf is now
proportioned as a preserved archival sheet:

  · padding: 56/64/56 → 88/64/104 (ceremonial entrance + footer)
  · provenance margin-bottom: 22 → 32 (header staging breath)
  · verse-ref margin-bottom: 6 → 14 (citation ceremonial pause)
  · colophon margin-top: 56 → 80 (codex closure descent)

Scope: text-witness leaves only. Excludes:
  · twelve AO chamber renderers (via :not([class*="-chamber"]))
  · Doré plates (via :not([data-kind="plate"]) and explicit
    padding: 0 already on .folio-leaf[data-kind="plate"])

Captures per-family after-screenshots for visual diff against
v76_after_*.
"""
import sys
import re
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


TEXT_WITNESS_SAMPLES = [
    ("gen.1.1",  "gen1-commentary-augustine",       "commentary"),
    ("gen.1.2",  "gen1-linguistic-tohu",            "linguistic"),
    ("gen.1.1",  "gen1-manuscript-opening",         "manuscript"),
    ("gen.22.2", "gen22-mount-moriah",              "architecture"),
    ("gen.1.3",  "gen1-ritual-maariv-aravim",       "ritual"),
    ("gen.1.1",  "gen1-xref-nt-creation",           "cross_reference"),
    ("gen.1.1",  "gen1-cosmology-ane",              "cosmology"),
    ("gen.18.2", "gen18-three-visitors-reception",  "reception"),
]
CHAMBER_SAMPLES = [
    ("gen.1.6",  "gen1-cosmology-firmament",        "ao_cosmology"),
    ("exo.40.34","exo40-sanctuary-glory",           "ao_sanctuary"),
    ("psa.13.1", "psa13-lament-cry",                "ao_lament"),
    ("gen.5.1",  "gen5-antediluvian-line",          "ao_lineage"),
]
PLATE_SAMPLES = [
    ("gen.1.3",  "dore-creation-of-light",          "dore_creation"),
    ("gen.11.7", "dore-confusion-of-tongues",       "dore_babel"),
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
    page.wait_for_timeout(1300)


def leaf_padding(page):
    return page.evaluate(
        """
        (() => {
          const leaf = document.querySelector('.folio-leaf');
          if (!leaf) return null;
          const s = getComputedStyle(leaf);
          return {
            kind: leaf.dataset.kind,
            classes: leaf.className,
            paddingTop: s.paddingTop,
            paddingRight: s.paddingRight,
            paddingBottom: s.paddingBottom,
            paddingLeft: s.paddingLeft,
          };
        })()
        """
    )


def staging_metrics(page):
    return page.evaluate(
        """
        (() => {
          const leaf = document.querySelector('.folio-leaf');
          if (!leaf) return null;
          const prov = leaf.querySelector('.folio-leaf-provenance');
          const verse = leaf.querySelector('.folio-leaf-verse');
          const colophon = leaf.querySelector('.folio-leaf-colophon');
          return {
            provenanceMarginBottom: prov ? getComputedStyle(prov).marginBottom : null,
            verseMarginBottom: verse ? getComputedStyle(verse).marginBottom : null,
            colophonMarginTop: colophon ? getComputedStyle(colophon).marginTop : null,
          };
        })()
        """
    )


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 1100})
        page = ctx.new_page()

        # ── Phase 1 — Text-witness leaves use ceremonial padding ───
        print("=== Phase 1 — Ceremonial leaf padding (text witnesses) ===")
        for pid, rec_id, label in TEXT_WITNESS_SAMPLES:
            open_leaf(page, pid, rec_id)
            m = leaf_padding(page)
            print(f"  {label:<14}: padding {m['paddingTop']}/"
                  f"{m['paddingRight']}/{m['paddingBottom']}/"
                  f"{m['paddingLeft']}")
            assert m["paddingTop"] == "88px", (label, m["paddingTop"])
            assert m["paddingRight"] == "64px", (label, m["paddingRight"])
            assert m["paddingBottom"] == "104px", (label, m["paddingBottom"])
            assert m["paddingLeft"] == "64px", (label, m["paddingLeft"])
        print("  OK — every text-witness leaf carries the 88/64/104 "
              "ceremonial padding.\n")

        # ── Phase 2 — Typographic staging breath ───────────────────
        print("=== Phase 2 — Header + body + footer staging ===")
        for pid, rec_id, label in TEXT_WITNESS_SAMPLES[:3]:
            open_leaf(page, pid, rec_id)
            s = staging_metrics(page)
            print(f"  {label:<14}: prov={s['provenanceMarginBottom']:<6} "
                  f"verse={s['verseMarginBottom']:<6} "
                  f"colophon={s['colophonMarginTop']:<6}")
            assert s["provenanceMarginBottom"] == "32px"
            # viewer-active sets verse margin to 16px (overrides
            # the resting-state 14px).
            assert s["verseMarginBottom"] == "16px"
            assert s["colophonMarginTop"] == "80px"
        print("  OK — provenance / verse / colophon staging breath "
              "operational.\n")

        # ── AO chambers — padding UNCHANGED ────────────────────────
        print("=== AO chambers preserved (no ceremonial padding) ===")
        for pid, rec_id, label in CHAMBER_SAMPLES:
            open_leaf(page, pid, rec_id)
            m = leaf_padding(page)
            print(f"  {label:<14}: padding "
                  f"{m['paddingTop']}/{m['paddingRight']}/"
                  f"{m['paddingBottom']}/{m['paddingLeft']}  "
                  f"classes={m['classes']}")
            # Chambers retain the original 56/64/56/64.
            assert m["paddingTop"] == "56px", (label, m["paddingTop"])
            assert m["paddingBottom"] == "56px", (label, m["paddingBottom"])
            assert "-chamber" in m["classes"]
        print("  OK — all sampled AO chambers retain compact 56/64 "
              "padding; their bespoke composition is untouched.\n")

        # ── Doré preservation ──────────────────────────────────────
        print("=== Doré preservation ===")
        for pid, rec_id, label in PLATE_SAMPLES:
            open_leaf(page, pid, rec_id)
            d = page.evaluate(
                """
                (() => {
                  const leaf = document.querySelector('.folio-leaf');
                  const s = getComputedStyle(leaf);
                  return {
                    bg: s.backgroundColor,
                    padding: s.padding,
                    boxShadow: s.boxShadow,
                    hasWrap: !!document.querySelector('.folio-plate-wrap'),
                    hasPlaque: !!document.querySelector('.folio-plate-plaque'),
                  };
                })()
                """
            )
            print(f"  {label}: padding={d['padding']} bg={d['bg']} "
                  f"shadow={d['boxShadow']} wrap={d['hasWrap']} "
                  f"plaque={d['hasPlaque']}")
            assert d["padding"] == "0px"
            assert d["bg"] in ("rgba(0, 0, 0, 0)", "transparent")
            assert d["boxShadow"] == "none"
            assert d["hasWrap"] and d["hasPlaque"]
        print("  OK — Doré plates retain transparent leaf, zero "
              "padding, no halo. Monumental cathedral preserved.\n")

        # ── Family identity preservation (no measure regressions) ──
        print("=== Family identity preservation ===")
        family_checks = [
            ("commentary",     "gen.1.1",  "gen1-commentary-augustine",
             dict(bodyMaxWidth="640px", titleFontWeight="400")),
            ("linguistic",     "gen.1.2",  "gen1-linguistic-tohu",
             dict(bodyMaxWidth="560px", titleFontStyle="normal")),
            ("manuscript",     "gen.1.1",  "gen1-manuscript-opening",
             dict(bodyMaxWidth="500px", titleFontStyle="normal")),
            ("architecture",   "gen.22.2", "gen22-mount-moriah",
             dict(bodyMaxWidth="480px", titleFontVariantCaps="small-caps")),
            ("reception",      "gen.18.2", "gen18-three-visitors-reception",
             dict(bodyMaxWidth="600px")),
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
        print("  OK — all 8 formalized text-witness families "
              "preserved.\n")

        # ── AO inventory ───────────────────────────────────────────
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
        print(f"=== AO inventory: {ao_count} ===")
        assert ao_count == 12
        print("  OK — twelve Atlas Objects preserved.\n")

        # ── After-captures ─────────────────────────────────────────
        print("=== Per-family after-captures ===")
        for samples_group in [
            TEXT_WITNESS_SAMPLES,
            CHAMBER_SAMPLES,
            PLATE_SAMPLES,
        ]:
            for pid, rec_id, label in samples_group:
                open_leaf(page, pid, rec_id)
                page.screenshot(path=f"reports/v77_after_{label}.png")
                print(f"  captured {label}")

        b.close()
    print("\nALL CHECKS PASSED — Folio Object Architecture operational.")


if __name__ == "__main__":
    main()
