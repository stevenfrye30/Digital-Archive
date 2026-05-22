"""v79 — Codex Orientation: canonical stratum rubric.

Verifies the single move that builds the macro-orientation
layer: a quiet two-segment "Macro · Section" line beneath the
Roman numeral chapter mark.

  · Torah · Primeval History           gen.1 - gen.11
  · Torah · Patriarchal History        gen.12 - gen.50
  · Torah · The Going Out              exo.1 - exo.18
  · Torah · Sinai Covenant             exo.19 - exo.40
  · Torah · Priestly Code              lev
  · Torah · Wilderness                 num
  · Torah · Deuteronomy                deu
  · Hebrew Bible · Historical Books    jos jdg rut sam ki ch ezr neh est
  · Hebrew Bible · Wisdom & Hymnody    job psa pro ecc sng
  · Hebrew Bible · Latter Prophets     isa jer lam eze dan
  · Hebrew Bible · The Twelve          hos joe amo oba jon mic nah hab zep hag zec mal
  · New Testament · Gospel             mat mrk luk jhn
  · New Testament · Apostolic Acts     act
  · New Testament · Pauline Letters    rom 1co 2co gal eph php col 1th 2th 1ti 2ti tit phm
  · New Testament · Catholic Letters   heb jas 1pe 2pe 1jo 2jo 3jo jud
  · New Testament · Apocalypse         rev

Verifies the rubric renders correctly across the canon and
that no leaf-constitution work regressed.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright


CANON_SAMPLES = [
    # (pid, expected_stratum, label)
    ("gen.1.1",   "Torah · Primeval History",       "gen1"),
    ("gen.5.1",   "Torah · Primeval History",       "gen5"),
    ("gen.11.7",  "Torah · Primeval History",       "gen11"),
    ("gen.12.1",  "Torah · Patriarchal History",    "gen12"),
    ("gen.22.1",  "Torah · Patriarchal History",    "gen22"),
    ("gen.50.1",  "Torah · Patriarchal History",    "gen50"),
    ("exo.3.1",   "Torah · The Going Out",          "exo3"),
    ("exo.18.1",  "Torah · The Going Out",          "exo18"),
    ("exo.19.1",  "Torah · Sinai Covenant",         "exo19"),
    ("exo.40.34", "Torah · Sinai Covenant",         "exo40"),
    ("lev.1.1",   "Torah · Priestly Code",          "lev"),
    ("num.1.1",   "Torah · Wilderness",             "num"),
    ("deu.6.4",   "Torah · Deuteronomy",            "deu"),
    ("jos.1.1",   "Hebrew Bible · Historical Books","jos"),
    ("rut.1.1",   "Hebrew Bible · Historical Books","rut"),
    ("job.3.3",   "Hebrew Bible · Wisdom & Hymnody","job"),
    ("psa.23.1",  "Hebrew Bible · Wisdom & Hymnody","psa"),
    ("pro.1.7",   "Hebrew Bible · Wisdom & Hymnody","pro"),
    ("isa.6.1",   "Hebrew Bible · Latter Prophets", "isa"),
    ("jer.31.33", "Hebrew Bible · Latter Prophets", "jer"),
    ("eze.1.1",   "Hebrew Bible · Latter Prophets", "eze"),
    ("dan.7.9",   "Hebrew Bible · Latter Prophets", "dan"),
    ("hos.6.1",   "Hebrew Bible · The Twelve",      "hos"),
    ("mat.5.1",   "New Testament · Gospel",         "mat"),
    ("jhn.1.14",  "New Testament · Gospel",         "jhn"),
    ("act.2.1",   "New Testament · Apostolic Acts", "act"),
    ("rom.8.1",   "New Testament · Pauline Letters","rom"),
    ("heb.4.9",   "New Testament · Catholic Letters","heb"),
    ("1jn.4.7",   "New Testament · Catholic Letters","1jn"),
    ("rev.4.1",   "New Testament · Apocalypse",     "rev"),
]


def open_chapter(page, pid):
    page.goto(
        f"http://localhost:8765/index.html?text=bible_kjv.json&p={pid}",
        wait_until="networkidle",
    )
    page.wait_for_function(
        "typeof currentData === 'object' && currentData && currentData.passages",
        timeout=15000,
    )
    page.wait_for_timeout(600)


def stratum_text(page):
    return page.evaluate(
        """(()=>{const s=document.querySelector('.ch-stratum');return s?s.textContent:null;})()"""
    )


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # ── Canonical stratum coverage ─────────────────────────────
        print("=== Canonical stratum coverage ===")
        sample_screenshots = {
            "gen1", "gen22", "lev", "psa", "isa", "hos",
            "jhn", "act", "rom", "rev",
        }
        for pid, expected, label in CANON_SAMPLES:
            open_chapter(page, pid)
            s = stratum_text(page)
            ok = "OK" if s == expected else "FAIL"
            print(f"  [{ok}] {pid:<10}  → {s!r}")
            assert s == expected, (pid, s, expected)
            if label in sample_screenshots:
                page.screenshot(path=f"reports/v79_stratum_{label}.png")
        print(f"\n  OK — all {len(CANON_SAMPLES)} canonical positions render "
              "their stratum rubric.\n")

        # ── Stratum visual register ────────────────────────────────
        print("=== Stratum visual register ===")
        open_chapter(page, "gen.1.1")
        metrics = page.evaluate(
            """(()=>{
              const s = document.querySelector('.ch-stratum');
              if (!s) return null;
              const cs = getComputedStyle(s);
              return {
                fontFamily: cs.fontFamily,
                fontStyle: cs.fontStyle,
                fontVariantCaps: cs.fontVariantCaps,
                letterSpacing: cs.letterSpacing,
                marginTop: cs.marginTop,
                color: cs.color,
              };
            })()"""
        )
        print(f"  {metrics}")
        assert metrics["fontStyle"] == "italic"
        assert metrics["fontVariantCaps"] in ("small-caps", "all-small-caps")
        print("  OK — stratum renders as italic small-caps with "
              "letter-spacing and quiet color.\n")

        # ── No regression: object opening still works ──────────────
        print("=== No regression: leaf opening ===")
        page.goto(
            "http://localhost:8765/index.html?text=bible_kjv.json&p=gen.1.1",
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
        page.evaluate("(() => _openFolioObject('gen1-commentary-augustine'))()")
        page.wait_for_timeout(1300)
        leaf_state = page.evaluate(
            """(()=>{
              const leaf = document.querySelector('.folio-leaf');
              return leaf ? {
                kind: leaf.dataset.kind,
                bodyMax: getComputedStyle(leaf.querySelector('.folio-body-vertical')).maxWidth,
              } : null;
            })()"""
        )
        print(f"  augustine leaf: {leaf_state}")
        assert leaf_state["kind"] == "commentary"
        assert leaf_state["bodyMax"] == "640px"
        print("  OK — leaf opening preserved.\n")

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
        print("  OK — 12 Atlas Objects preserved.\n")

        # ── Atmospheric captures ───────────────────────────────────
        print("=== Genesis chapter views (visible stratum) ===")
        for pid, label in [
            ("gen.1.1",  "gen01_creation"),
            ("gen.12.1", "gen12_call"),
            ("gen.22.1", "gen22_akedah"),
            ("gen.50.1", "gen50_close"),
        ]:
            open_chapter(page, pid)
            page.screenshot(path=f"reports/v79_chapter_{label}.png")
            print(f"  captured {label}")

        b.close()
    print("\nALL CHECKS PASSED — Codex Orientation operational.")


if __name__ == "__main__":
    main()
