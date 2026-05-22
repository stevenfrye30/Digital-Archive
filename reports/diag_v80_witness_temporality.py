"""v80 — Witness Temporality verification.

Verifies the transmission rubric — a single italic small-caps
phrase appended to the provenance block, declaring each witness
family's temporal posture. Implementation: pure CSS ::after on
.folio-leaf-provenance, scoped by data-kind.

Family rubrics:
  · manuscript           preserved through transmission
  · commentary           inherited through interpretation
  · linguistic           witnessed in philology
  · architecture         held in land-memory
  · ritual               carried through generations
  · reception-history    layered across centuries
  · cross-reference      echoing through scripture
  · cosmology            read against the world-picture
  · plate (Doré)         (none — plaque carries its own temporality)
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


EXPECTED_RUBRICS = {
    "manuscript":        '"preserved through transmission"',
    "commentary":        '"inherited through interpretation"',
    "linguistic":        '"witnessed in philology"',
    "architecture":      '"held in land-memory"',
    "ritual":            '"carried through generations"',
    "reception-history": '"layered across centuries"',
    "cross-reference":   '"echoing through scripture"',
    "cosmology":         '"read against the world-picture"',
}

SAMPLES = [
    ("manuscript",        "gen.1.1",  "gen1-manuscript-opening"),
    ("commentary",        "gen.1.1",  "gen1-commentary-augustine"),
    ("commentary",        "gen.12.1", "gen12-lekh-lekha-call"),
    ("commentary",        "gen.22.9", "gen22-akedah-binding"),
    ("linguistic",        "gen.1.2",  "gen1-linguistic-tohu"),
    ("linguistic",        "gen.22.1", "gen22-hineni"),
    ("architecture",      "gen.22.2", "gen22-mount-moriah"),
    ("architecture",      "gen.12.7", "gen12-altar-at-shechem"),
    ("architecture",      "gen.28.18","gen28-bethel-pillar"),
    ("ritual",            "gen.1.3",  "gen1-ritual-maariv-aravim"),
    ("reception-history", "gen.18.2", "gen18-three-visitors-reception"),
    ("reception-history", "gen.22.19","gen22-reception-three-traditions"),
    ("cross-reference",   "gen.1.1",  "gen1-xref-nt-creation"),
    ("cosmology",         "gen.1.1",  "gen1-cosmology-ane"),
    ("cosmology",         "gen.1.3",  "gen1-cosmology-light-before-luminaries"),
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
    page.evaluate("() => localStorage.removeItem('archive:records-seen:v1')")
    page.evaluate("document.getElementById('companion-toggle').click()")
    page.wait_for_timeout(500)
    page.evaluate("_setFolioDepth('archive')")
    page.wait_for_timeout(400)
    page.evaluate(f"(() => _openFolioObject('{rec_id}'))()")
    page.wait_for_timeout(1300)


def rubric_text(page):
    return page.evaluate(
        """(()=>{
          const p = document.querySelector('.folio-leaf-provenance');
          if (!p) return null;
          return window.getComputedStyle(p, '::after').content;
        })()"""
    )


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 1100})
        page = ctx.new_page()

        # ── Family transmission rubrics ─────────────────────────────
        print("=== Family transmission rubrics ===")
        captured_families = set()
        for kind, pid, rec_id in SAMPLES:
            open_leaf(page, pid, rec_id)
            actual = rubric_text(page)
            expected = EXPECTED_RUBRICS[kind]
            ok = "OK" if actual == expected else "FAIL"
            print(f"  [{ok}] {kind:<18} {rec_id:<40} → {actual}")
            assert actual == expected, (rec_id, actual, expected)
            if kind not in captured_families:
                page.screenshot(
                    path=f"reports/v80_rubric_{kind.replace('-', '_')}.png"
                )
                captured_families.add(kind)
        print(f"\n  OK — all {len(EXPECTED_RUBRICS)} families render their "
              "transmission rubric.\n")

        # ── Doré preservation: no rubric on plate plaque ────────────
        print("=== Doré plate has no transmission rubric ===")
        open_leaf(page, "gen.1.3", "dore-creation-of-light")
        plate_rubric = page.evaluate(
            """(()=>{
              const p = document.querySelector('.folio-leaf-provenance');
              if (!p) return 'no_provenance_element';
              return window.getComputedStyle(p, '::after').content;
            })()"""
        )
        plaque_intact = page.evaluate(
            """(()=>{
              return {
                hasWrap: !!document.querySelector('.folio-plate-wrap'),
                hasPlaque: !!document.querySelector('.folio-plate-plaque'),
                plateTitle: document.querySelector('.folio-plate-title')?.textContent,
              };
            })()"""
        )
        print(f"  plate-provenance::after  → {plate_rubric}")
        print(f"  plate plaque state       → {plaque_intact}")
        # Plates don't have provenance element at all (rendered via
        # _renderPlate), so the rubric query returns 'no_provenance_element'.
        # OR if the leaf has provenance, the content rule is 'none'.
        assert plate_rubric in ("no_provenance_element", "none", '"none"')
        assert plaque_intact["hasWrap"] and plaque_intact["hasPlaque"]
        print("  OK — Doré plate preserved; no transmission rubric "
              "competes with the plaque's existing temporality.\n")

        # ── Rubric typographic register ─────────────────────────────
        print("=== Rubric typographic register ===")
        open_leaf(page, "gen.1.1", "gen1-commentary-augustine")
        cs = page.evaluate(
            """(()=>{
              const p = document.querySelector('.folio-leaf-provenance');
              if (!p) return null;
              const s = window.getComputedStyle(p, '::after');
              return {
                fontStyle: s.fontStyle,
                fontVariantCaps: s.fontVariantCaps,
                letterSpacing: s.letterSpacing,
                opacity: s.opacity,
                marginTop: s.marginTop,
                color: s.color,
              };
            })()"""
        )
        print(f"  {cs}")
        assert cs["fontStyle"] == "italic"
        assert cs["fontVariantCaps"] in ("small-caps", "all-small-caps")
        print("  OK — rubric renders as italic small-caps with "
              "quiet color.\n")

        # ── No regression: family identities ───────────────────────
        print("=== Family identity preservation ===")
        family_checks = [
            ("commentary",     "gen.1.1",  "gen1-commentary-augustine",
             dict(bodyMaxWidth="640px", titleFontWeight="400")),
            ("linguistic",     "gen.1.2",  "gen1-linguistic-tohu",
             dict(bodyMaxWidth="560px", titleFontStyle="normal")),
            ("manuscript",     "gen.1.1",  "gen1-manuscript-opening",
             dict(bodyMaxWidth="500px")),
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
                """(()=>{
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

        # ── AO inventory ───────────────────────────────────────────
        ao_count = page.evaluate(
            """(()=>{
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
        print("  OK — 12 Atlas Objects preserved.\n")

        # ── v79 canonical stratum preserved ─────────────────────────
        print("=== Canonical stratum preserved ===")
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
            wait_until="networkidle",
        )
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(600)
        stratum = page.evaluate(
            "(()=>{const s=document.querySelector('.ch-stratum');return s?s.textContent:null;})()"
        )
        print(f"  gen.1.1 stratum: {stratum!r}")
        assert stratum == "Torah · Primeval History"
        print("  OK — v79 canonical stratum rubric still operational.\n")

        b.close()
    print("\nALL CHECKS PASSED — Witness Temporality operational.")


if __name__ == "__main__":
    main()
