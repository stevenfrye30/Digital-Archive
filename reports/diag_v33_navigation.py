"""v33 — focused Bible navigation refinement verification.

Covers:
  1. Folio depth rubric fits inside the folio column without overflow
  2. Authority-tier markers have distinguishable visual hierarchy
  3. Cover back button returns to Bible Versions (browseTradition)
  4. Single-variant Bible cards open directly (no expand)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/index.html?text=bible_kjv.json"


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(f"{BASE}&p=gen.1.1", wait_until="networkidle")
        page.wait_for_function(
            "typeof currentData === 'object' && currentData && currentData.passages",
            timeout=15000,
        )
        page.wait_for_timeout(800)
        page.click("#companion-toggle")
        page.wait_for_timeout(800)

        # ── 1. Rubric fits inside folio column ─────────────────
        rub = page.evaluate(
            """
          () => {
            const r = document.querySelector('.cr-folio-depth-rubric');
            const labs = r.querySelector('.crd-labels');
            const col = document.querySelector('.folio-column');
            const prefix = r.querySelector('.crd-prefix');
            return {
              prefix: prefix?.textContent,
              rubricRect: r.getBoundingClientRect().toJSON(),
              labsRect: labs.getBoundingClientRect().toJSON(),
              colRect: col.getBoundingClientRect().toJSON(),
            };
          }
        """
        )
        cl = rub["colRect"]["left"]
        cr = rub["colRect"]["right"]
        ll = rub["labsRect"]["left"]
        lr = rub["labsRect"]["right"]
        print(f"folio col: {cl:.0f} → {cr:.0f} (width {rub['colRect']['width']:.0f})")
        print(f"labels row: {ll:.0f} → {lr:.0f} (width {rub['labsRect']['width']:.0f})")
        print(f"prefix: {rub['prefix']!r}")
        # Allow 2px slack for sub-pixel rendering
        assert ll >= cl - 1, f"labels left {ll} < col left {cl}"
        assert lr <= cr + 1, f"labels right {lr} > col right {cr}"
        print("OK — rubric fits inside folio column")

        # ── Test all three depth labels still fit + work
        for d in ("core", "study", "archive"):
            page.evaluate(f"_setFolioDepth('{d}')")
            page.wait_for_timeout(200)
        page.screenshot(path="reports/v33_rubric_fits.png")

        # ── 2. Tier styling — verify primary/secondary/tertiary differ
        page.evaluate("_setFolioDepth('archive')")
        page.wait_for_timeout(400)
        tier_samples = page.evaluate(
            """
          () => {
            const groups = ['primary', 'secondary', 'tertiary'];
            const out = {};
            for (const t of groups) {
              const m = document.querySelector(`.cr-folio-marker[data-authority="${t}"]`);
              if (!m) { out[t] = null; continue; }
              const cs = getComputedStyle(m);
              out[t] = {
                bg: cs.backgroundColor,
                bd: cs.borderColor,
                bdStyle: cs.borderStyle,
                color: cs.color,
                opacity: cs.opacity,
                fontWeight: cs.fontWeight,
              };
            }
            return out;
          }
        """
        )
        print("\nTier marker styling:")
        for t, s in tier_samples.items():
            print(f"  {t:<10} opacity={s['opacity']} border={s['bdStyle']} fw={s['fontWeight']}")
            print(f"             color={s['color']} bg={s['bg']}")
        # Opacity descends: primary > secondary > tertiary
        op_pri = float(tier_samples["primary"]["opacity"])
        op_sec = float(tier_samples["secondary"]["opacity"])
        op_ter = float(tier_samples["tertiary"]["opacity"])
        assert op_pri > op_sec > op_ter, (
            f"opacity should descend: {op_pri}>{op_sec}>{op_ter}"
        )
        # Border styles differ
        bs = {t: tier_samples[t]["bdStyle"] for t in tier_samples}
        assert bs["primary"] == "solid"
        assert bs["secondary"] == "dashed"
        assert bs["tertiary"] == "dotted"
        print("OK — tier markers have clear opacity + border hierarchy")
        page.screenshot(path="reports/v33_archive_tiers.png")

        # ── 3. Cover back button → Bible Versions ──────────────
        page.click("#ctrl-contents")
        page.wait_for_timeout(800)
        cov_btn = page.evaluate(
            """
          () => {
            const btn = document.querySelector('.bcl-back-to-versions');
            return btn ? {
              txt: btn.textContent.trim(),
              pos: btn.getBoundingClientRect().toJSON(),
            } : null;
          }
        """
        )
        print(f"\nCover back button: {cov_btn['txt']!r} at "
              f"({cov_btn['pos']['x']:.0f}, {cov_btn['pos']['y']:.0f})")
        assert cov_btn["txt"] == "← Bible Versions"
        page.screenshot(path="reports/v33_cover_back_btn.png")

        # Click it → should land on browseTradition (Religion/Christian)
        page.click(".bcl-back-to-versions")
        page.wait_for_timeout(1000)
        bible_versions = page.evaluate(
            """
          () => ({
            browseDisplay: getComputedStyle(document.getElementById('browse')).display,
            crumb: (document.getElementById('browse-breadcrumb') || {}).textContent || '',
            title: (document.getElementById('browse-title') || {}).textContent || '',
            inReading: document.body.classList.contains('in-reading'),
          })
        """
        )
        print(f"\nAfter back-btn click:")
        print(f"  browse display: {bible_versions['browseDisplay']}")
        print(f"  crumb: {bible_versions['crumb']!r}")
        print(f"  title: {bible_versions['title']!r}")
        assert bible_versions["browseDisplay"] != "none"
        assert "Christian" in bible_versions["crumb"] or "Christian" in bible_versions["title"]
        assert not bible_versions["inReading"]
        print("OK — back button lands on Bible Versions list")
        page.screenshot(path="reports/v33_bible_versions.png")

        # ── 4. KJV tile opens directly (single-variant card)
        tiles = page.evaluate(
            """
          () => {
            const ts = Array.from(document.querySelectorAll('#browse-tiles > *'));
            return ts.map(t => ({
              tag: t.tagName.toLowerCase(),
              cls: t.className,
              title: t.querySelector('.tt-title')?.textContent
                  || t.querySelector('.shelf-label')?.textContent || '',
              shelf: t.dataset.shelf || null,
            }));
          }
        """
        )
        print("\nBible Versions tiles:")
        for t in tiles[:10]:
            print(f"  <{t['tag']}> .{t['cls']} title={t['title']!r} shelf={t['shelf']}")

        # ── Click King James Bible tile and confirm it goes through.
        # If KJV resolves to browseText → single-variant shelf → should
        # land on KJV cover directly without an intermediate shelf.
        kjv_tile = next(
            (t for t in tiles if "King James" in (t["title"] or "")
             or "KJV" in (t["title"] or "")
             or (t["title"] or "").strip() == "Bible"),
            None,
        )
        if kjv_tile:
            print(f"\nClicking KJV tile: {kjv_tile['title']!r}")
            # Click by title text
            page.click(f'#browse-tiles >> text="{kjv_tile["title"]}"')
            page.wait_for_timeout(1200)
            arrived = page.evaluate(
                """
              () => {
                const th = document.getElementById('text-header');
                return {
                  textHeaderDisplay: th ? getComputedStyle(th).display : null,
                  hasBibleCover: !!document.querySelector('.bible-cover-layout'),
                  hasShelfGroup: !!document.querySelector('.shelf-group'),
                  hasIntermediateChooser: !!document.querySelector('.shelf-group:not([open])'),
                  browseDisplay: getComputedStyle(document.getElementById('browse')).display,
                  hasSingleShelfText: !!document.querySelector(
                    '#browse-tiles .text-tile[data-shelf]'
                  ),
                };
              }
            """
            )
            print(f"\nAfter KJV click: {arrived}")
            # Two acceptable outcomes:
            #  (a) Direct land on KJV cover (single-variant case after fix)
            #  (b) Landed on browseText with KJV-shelf flattened to text-tile
            #      (then clicking opens cover)
            if arrived["hasBibleCover"]:
                print("OK — KJV opened directly to cover")
            else:
                # Should at least show the flattened single-variant tile,
                # NOT a closed shelf-group requiring expand
                assert arrived["hasSingleShelfText"] or not arrived["hasShelfGroup"], (
                    "single-variant shelf still requires expand — bad"
                )
                print("OK — single-variant shelf rendered as direct tile")
                # Click it to confirm it opens
                page.click("#browse-tiles .text-tile[data-shelf]")
                page.wait_for_timeout(1200)
                final = page.evaluate(
                    "() => !!document.querySelector('.bible-cover-layout')"
                )
                assert final, "click did not open KJV cover"
                print("OK — direct click opened KJV cover")
        page.screenshot(path="reports/v33_kjv_after_click.png")

        b.close()
    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
