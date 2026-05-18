"""v22 — folio width, scripture zone-centering, wide composition."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from playwright.sync_api import sync_playwright


def probe(page):
    return page.evaluate(
        """
      () => {
        const folio = document.getElementById('folio');
        const fcs = getComputedStyle(folio);
        const reader = document.getElementById('reader');
        const rcs = getComputedStyle(reader);
        const passage = document.querySelector('.cr-row > :first-child');
        const fr = folio.getBoundingClientRect();
        const pr = passage?.getBoundingClientRect();
        return {
          bodyClasses: Array.from(document.body.classList),
          viewport: { w: innerWidth, h: innerHeight },
          reader: {
            padLeft: rcs.paddingLeft,
            padRight: rcs.paddingRight,
            rect: reader.getBoundingClientRect().toJSON(),
            contentLeft: reader.getBoundingClientRect().left + parseFloat(rcs.paddingLeft),
            contentRight: reader.getBoundingClientRect().right - parseFloat(rcs.paddingRight),
          },
          folio: {
            display: fcs.display,
            width: fcs.width,
            rect: fcs.display !== 'none' ? fr.toJSON() : null,
          },
          passage: pr?.toJSON() || null,
          sharedArea: pr && fcs.display !== 'none'
            ? Math.max(0, Math.min(fr.right, pr.right) - Math.max(fr.left, pr.left)) *
              Math.max(0, Math.min(fr.bottom, pr.bottom) - Math.max(fr.top, pr.top))
            : 0,
          entryCount: document.querySelectorAll('.cr-folio-entry').length,
        };
      }
        """
    )


def main():
    print("=" * 60)
    print("DATA AUDIT — witness records anchored to Genesis chapters")
    print("=" * 60)
    with open("data/bible_kjv.json", encoding="utf-8") as f:
        data = json.load(f)
    from collections import defaultdict
    by_ch = defaultdict(list)
    for r in data.get("genealogy", []):
        for a in r.get("anchors", []):
            pid = (a.get("target") or "").split("::").pop()
            parts = pid.split(".")
            if len(parts) < 2:
                continue
            by_ch[f"{parts[0]}.{parts[1]}"].append(r)
    print(f"Total witness records: {len(data.get('genealogy', []))}")
    for ch in ["gen.1", "gen.4", "gen.11"]:
        records = by_ch.get(ch, [])
        print(f"  {ch}: {len(records)} witness(es)")
        for r in records:
            print(f"     - [{r.get('kind')}] {r.get('title')}")
    print("\nNote: Genesis 1 has exactly 1 witness in the data file.")
    print("That is curation, not a rendering bug. Authoring more")
    print("witnesses for Gen 1 would be a separate task.\n")

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        def goto_chapter(ch):
            page.goto(
                f"http://localhost:8765/index.html?text=bible_kjv.json&p={ch}.1",
                wait_until="networkidle",
            )
            page.wait_for_function(
                "typeof currentData === 'object' && currentData && currentData.passages",
                timeout=15000,
            )
            page.wait_for_timeout(700)

        # ── SINGLE FOLIO OFF ─────────────────────────────────────
        goto_chapter("gen.1")
        off = probe(page)
        page.screenshot(path="reports/v22_single_off.png")

        # ── SINGLE FOLIO RIGHT ───────────────────────────────────
        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        right = probe(page)
        page.screenshot(path="reports/v22_single_right.png")

        # ── SINGLE FOLIO LEFT ────────────────────────────────────
        page.click("#companion-swap")
        page.wait_for_timeout(500)
        left = probe(page)
        page.screenshot(path="reports/v22_single_left.png")

        # ── WIDE ─────────────────────────────────────────────────
        page.click("#ctrl-columns .col-opt[data-cols='wide']")
        page.wait_for_timeout(500)
        wide = probe(page)
        page.screenshot(path="reports/v22_wide.png")

        # ── MULTI-WITNESS at Gen 11 ──────────────────────────────
        page.click("#ctrl-columns .col-opt[data-cols='single']")
        page.wait_for_timeout(400)
        goto_chapter("gen.11")
        page.click("#companion-toggle")
        page.wait_for_timeout(500)
        gen11 = probe(page)
        page.screenshot(path="reports/v22_gen11.png")

        def show(label, s):
            print(f"\n── {label} " + "─" * (60 - len(label)))
            pr = s["passage"]
            fr = s["folio"]["rect"]
            print(f"  body: {' '.join(c for c in s['bodyClasses'] if not c.startswith(('reading-', 'in-')))}")
            print(f"  scripture:    L={pr['left']:6.0f} R={pr['right']:6.0f} W={pr['width']:4.0f}")
            avail_l = s["reader"]["contentLeft"]
            avail_r = s["reader"]["contentRight"]
            print(f"  reader avail: L={avail_l:6.0f} R={avail_r:6.0f} W={avail_r-avail_l:4.0f}")
            print(f"  scripture margins inside reader avail: L={pr['left']-avail_l:.0f}  R={avail_r-pr['right']:.0f}")
            if fr:
                print(f"  folio:        L={fr['left']:6.0f} R={fr['right']:6.0f} W={fr['width']:4.0f}")
                print(f"  shared area:  {s['sharedArea']:.1f} px²")
            else:
                lm = pr["left"]
                rm = s["viewport"]["w"] - pr["right"]
                print(f"  folio:        (hidden)")
                print(f"  scripture viewport margins: L={lm:.0f}  R={rm:.0f}")
            print(f"  entries: {s['entryCount']}")

        show("SINGLE, FOLIO OFF", off)
        show("SINGLE, FOLIO RIGHT", right)
        show("SINGLE, FOLIO LEFT", left)
        show("WIDE", wide)
        show("GEN 11 (multi-witness)", gen11)

        # Assertions
        print("\n=== Assertions ===")
        # Folio width
        assert right["folio"]["rect"]["width"] >= 280, (
            f"Folio still too narrow: {right['folio']['rect']['width']}"
        )
        assert left["folio"]["rect"]["width"] >= 280
        print(f"  folio width ≥ 280: right={right['folio']['rect']['width']:.0f}, left={left['folio']['rect']['width']:.0f} ✓")

        # No overlap
        assert right["sharedArea"] == 0
        assert left["sharedArea"] == 0
        print(f"  folio↔scripture shared area = 0 in both states ✓")

        # Scripture centered in remaining zone
        # folio-right: scripture should be centered in [0, viewport-folio_width]
        avail_w_right = right["viewport"]["w"] - right["folio"]["rect"]["width"]
        expected_left_right = (avail_w_right - right["passage"]["width"]) / 2
        assert abs(right["passage"]["left"] - expected_left_right) <= 1, (
            f"Folio-right: scripture not centered in remaining zone "
            f"(left={right['passage']['left']}, expected={expected_left_right})"
        )
        print(f"  folio-right: scripture centered in remaining zone ✓")

        # folio-left: scripture should be centered in [folio_width, viewport]
        expected_left_for_left = left["folio"]["rect"]["width"] + (avail_w_right - left["passage"]["width"]) / 2
        assert abs(left["passage"]["left"] - expected_left_for_left) <= 1, (
            f"Folio-left: scripture not centered in remaining zone "
            f"(left={left['passage']['left']}, expected={expected_left_for_left})"
        )
        print(f"  folio-left: scripture centered in remaining zone ✓")

        # Scripture width unchanged
        for s in [off, right, left]:
            assert abs(s["passage"]["width"] - 960) <= 0.5, (
                f"Scripture width drifted from 960: {s['passage']['width']}"
            )
        print(f"  scripture width = 960 across all single states ✓")

        # Folio off: scripture centered in full viewport
        lm = off["passage"]["left"]
        rm = off["viewport"]["w"] - off["passage"]["right"]
        assert abs(lm - rm) <= 1, f"Folio off: scripture not centered (L={lm}, R={rm})"
        print(f"  folio off: scripture centered in viewport (L=R={lm:.0f}) ✓")

        # Wide centered
        wide_lm = wide["passage"]["left"]
        wide_rm = wide["viewport"]["w"] - wide["passage"]["right"]
        assert abs(wide_lm - wide_rm) <= 1, (
            f"Wide not centered: L={wide_lm}, R={wide_rm}"
        )
        assert wide_lm >= 40, f"Wide hugs the edge: L={wide_lm}"
        print(f"  wide: scripture centered (L={wide_lm:.0f} = R={wide_rm:.0f}) ✓")

        # Wide has no folio
        assert wide["folio"]["display"] == "none"
        print(f"  wide: folio hidden ✓")

        # Multi-witness rendering
        assert gen11["entryCount"] == 3
        print(f"  Gen 11: 3 entries ✓")

        b.close()
    print("\nALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
