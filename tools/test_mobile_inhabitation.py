#!/usr/bin/env python3
"""test_mobile_inhabitation.py — Inhabit four passages in a mobile viewport.

Measures, after the May 15 2026 mobile reading refinement, how much
vertical space the Reading Room chrome occupies above the first
passage on a phone-sized viewport. Captures screenshots for visual
review.

Not a unit test. A reading-flow inspection.

Targets:
  - Genesis 1:1 (ASV)               bible_asv.json :: gen.1.1
  - Apannaka-jataka opening          jataka-chalmers-vol1_chalmers.json :: 1.1
  - Plato Crito opening              plato-crito_jowett.json :: 1
  - Katha Upanishad with apparatus   upanishads-muller-part2_muller-part2.json :: 5.80

Run with the static server on :8765 already running.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "reports" / "mobile_inhabitation"
OUT.mkdir(parents=True, exist_ok=True)

VIEWPORT = {"width": 390, "height": 844}  # iPhone 12 / 13 / 14 standard
BASE = "http://localhost:8765/"

TARGETS = [
    ("genesis-1-1",     "bible_asv.json",                            "gen.1.1"),
    ("apannaka-1-1",    "jataka_chalmers-vol1.json",                 "1.1"),
    ("republic-10-1",   "plato-republic_jowett.json",                "10.1"),
    ("katha-5-80",      "upanishads-muller-part2_muller-part2.json", "5.80"),
]


def inhabit(page, name, data_file, pid):
    url = f"{BASE}?text={data_file}&p={pid}"
    page.goto(url, wait_until="networkidle")
    # Wait for passages to render
    try:
        page.wait_for_selector(".passage", timeout=10000)
    except Exception:
        print(f"  [{name}] passage selector not found within 10s")
        page.screenshot(path=str(OUT / f"{name}-error.png"), full_page=False)
        return None

    # Measure: viewport height, first-passage top, chrome height above it
    metrics = page.evaluate("""() => {
        const vp = { w: window.innerWidth, h: window.innerHeight };
        const first = document.querySelector('.passage');
        const r = first ? first.getBoundingClientRect() : null;
        // Identify what sits in chrome at scrollTop=0
        const elements = ['#controls', '#info-bar', '#translation-bar', '#nav-bar', '#status'];
        const chrome = {};
        for (const sel of elements) {
            const el = document.querySelector(sel);
            if (el) {
                const cs = window.getComputedStyle(el);
                if (cs.display !== 'none') {
                    chrome[sel] = el.offsetHeight;
                }
            }
        }
        // Reader top padding (computed)
        const reader = document.querySelector('#reader');
        const readerPadTop = reader ? parseFloat(window.getComputedStyle(reader).paddingTop) : 0;
        // Chapter heading (if present)
        const heading = document.querySelector('.chapter-heading');
        const headingHeight = heading ? heading.offsetHeight : 0;
        // Details disclosure state
        const det = document.querySelector('details.display-options');
        return {
            viewport: vp,
            first_passage_top: r ? r.top : null,
            first_passage_text: first ? first.textContent.slice(0, 80) : null,
            chrome_pieces: chrome,
            reader_pad_top: readerPadTop,
            chapter_heading_height: headingHeight,
            display_options_open: det ? det.open : null,
        };
    }""")

    page.screenshot(path=str(OUT / f"{name}-portrait.png"), full_page=False)
    # Also snapshot with display-options expanded
    page.evaluate("() => { const d = document.querySelector('details.display-options'); if (d) d.open = true; }")
    time.sleep(0.2)
    page.screenshot(path=str(OUT / f"{name}-portrait-display-open.png"), full_page=False)
    page.evaluate("() => { const d = document.querySelector('details.display-options'); if (d) d.open = false; }")
    return metrics


def main():
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport=VIEWPORT, device_scale_factor=2,
                                  is_mobile=True, has_touch=True,
                                  user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1")
        page = ctx.new_page()
        for name, data_file, pid in TARGETS:
            print(f"\n=== {name} ===")
            m = inhabit(page, name, data_file, pid)
            if m:
                results[name] = m
                chrome_total = sum(m["chrome_pieces"].values())
                print(f"  viewport:                 {m['viewport']}")
                print(f"  chrome pieces:            {m['chrome_pieces']}")
                print(f"  reader pad-top:           {m['reader_pad_top']}px")
                print(f"  chapter heading:          {m['chapter_heading_height']}px")
                total_above = chrome_total + m["reader_pad_top"] + m["chapter_heading_height"]
                print(f"  total chrome above text:  {total_above:.0f}px ({100*total_above/m['viewport']['h']:.0f}% of viewport)")
                print(f"  first passage rect top:   {m['first_passage_top']:.0f}px")
                print(f"  display options open:     {m['display_options_open']}")
                print(f"  first passage opening:    {m['first_passage_text']!r}")
        browser.close()

    (OUT / "metrics.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWrote screenshots and metrics to {OUT}")


if __name__ == "__main__":
    main()
