#!/usr/bin/env python3
"""walk_layers.py — render any layer, at either width, in either theme.

WHY THIS EXISTS. Until Task 126 every mobile claim in this program rested
on the battery, because the browser tool available to the terminal side
pins its viewport at 1280px. Nothing had ever SEEN the archive at phone
width. The reading room — the deepest layer, holding 1,059 texts — had
been described entirely by assertions, and two of those assertions turned
out to be measuring something other than what they were named for
(doctrine §8.1d).

The battery answers "does the ruled grammar still hold?". This answers a
different question, the one a steward asks on a walk: **what does a
reader actually meet?** It renders, it measures, it writes frames. It
asserts nothing and it fails nothing — a walk that returns 1 would be a
battery, and the archive already has one.

    python tools/walk_layers.py --list
    python tools/walk_layers.py                       # every layer, both
                                                      # widths, both themes
    python tools/walk_layers.py --layer reading --width phone --theme dark
    python tools/walk_layers.py --layer hall entrance --out review/task131

Device emulation is real: `is_mobile=True` drives media queries, layout
and touch, so a phone frame is a phone frame and not a narrow desktop.

What it reports per visit, all measured on the RENDERED page (§8.1):
  overflow   horizontal scroll beyond the viewport
  off        elements crossing the viewport's left or right edge
  under44/38 interactive targets under the ruled floor for that width
             (44 at phone, 38 at desktop — 106-P2 item 4's deliberate split)
  ink        the reading column's real left/right gaps, from text nodes
  err        console errors and page errors
"""
from __future__ import annotations

import argparse
import http.server
import json
import socket
import socketserver
import sys
import threading
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("walk_layers needs playwright:  pip install playwright "
             "&& playwright install chromium")

REPO = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO / "review" / "walk"

DESKTOP = {"width": 1440, "height": 900}
PHONE = {"width": 390, "height": 844}

# A text per cover shape, so a walk covers the four the archive holds.
CODEX = "thus-spake-zarathustra_common.json"
FLAT = "plato-charmides_jowett.json"
BIBLE_80 = "bible_kjv.json"
BIBLE_66 = "bible_asv.json"

# name -> (path, settle_ms, enter_reading)
LAYERS: dict[str, tuple[str, int, bool]] = {
    "entrance":     ("index.html", 2500, False),
    "hall":         ("hall/index.html", 1800, False),
    "room-rich":    ("map/christianity.html", 2200, False),
    "room-dense":   ("map/buddhist.html", 2600, False),
    "room-sparse":  ("map/bahai.html", 1800, False),
    "shelf-philo":  ("shelf/philosophy.html", 1800, False),
    "shelf-lit":    ("shelf/literature.html", 1800, False),
    "shelf-eso":    ("shelf/esoteric.html", 1800, False),
    "philosophy":   ("philosophy.html", 1800, False),
    "cover-flat":   (f"index.html?text={FLAT}", 3000, False),
    "cover-codex":  (f"index.html?text={CODEX}", 3000, False),
    "cover-b80":    (f"index.html?text={BIBLE_80}", 3500, False),
    "cover-b66":    (f"index.html?text={BIBLE_66}", 3500, False),
    "reading":      (f"index.html?text={CODEX}", 3000, True),
    "reading-big":  (f"index.html?text={BIBLE_80}", 4000, True),
}

PROBE_JS = r"""({vw, floor}) => {
  const de = document.documentElement, out = {
    title: document.title, theme: de.getAttribute('data-theme'),
    overflow: de.scrollWidth - window.innerWidth,
    floor: floor, offscreen: [], tiny: [], ink: null };

  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (!r.width && !r.height) continue;
    // a skip-link parked at -999px is a pattern, not a defect
    if (r.right < -200 || r.left > vw + 200) continue;
    if (r.right > vw + 1 || r.left < -1)
      out.offscreen.push({ tag: el.tagName.toLowerCase(),
        cls: String(el.className || '').slice(0, 50),
        left: Math.round(r.left), right: Math.round(r.right),
        text: (el.textContent || '').trim().slice(0, 40) });
  }

  for (const el of document.querySelectorAll(
       'a,button,input,select,summary,[role=button],[role=link]')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) continue;
    if (cs.position === 'fixed' && r.width < 2) continue;
    if (r.height < floor || r.width < floor)
      out.tiny.push({ tag: el.tagName.toLowerCase(),
        cls: String(el.className || '').slice(0, 34),
        w: Math.round(r.width), h: Math.round(r.height),
        text: (el.textContent || '').trim().slice(0, 28) });
  }

  // the reading column, measured as ink and not as the box that holds it
  const ps = [...document.querySelectorAll('.passage')].filter(p =>
      p.getAttribute('data-role') !== 'heading'
      && (p.textContent || '').trim().length > 80
      && getComputedStyle(p).display !== 'none');
  if (ps.length) {
    let lo = Infinity, hi = -Infinity;
    for (const p of ps.slice(0, 10))
      for (const n of p.childNodes) {
        if (n.nodeType !== 3 || !n.nodeValue.trim()) continue;
        const rg = document.createRange(); rg.selectNodeContents(n);
        for (const r of rg.getClientRects()) {
          if (r.width < 2) continue;
          lo = Math.min(lo, r.left); hi = Math.max(hi, r.right); }
      }
    if (lo < Infinity)
      out.ink = { left: Math.round(lo), right: Math.round(vw - hi),
                  width: Math.round(hi - lo),
                  asym: Math.round(Math.abs(lo - (vw - hi))),
                  passages: ps.length };
  }
  return out;
}"""


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def serve(root: Path, port: int):
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(  # noqa: E731
        *a, directory=str(root), **k)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    httpd.log_message = lambda *a, **k: None
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def enter_reading(pg):
    """Click through a cover into the body of the text."""
    pg.evaluate("""() => { const b = [...document.querySelectorAll('button,a')]
        .find(x => /Read from beginning|Begin reading|Start reading/i
                   .test(x.textContent)); b && b.click(); }""")
    pg.wait_for_timeout(1800)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Render archive layers at either width, in either theme.")
    ap.add_argument("--layer", nargs="*", metavar="NAME",
                    help="layers to walk (default: all). --list to see them")
    ap.add_argument("--width", choices=["desktop", "phone", "both"],
                    default="both")
    ap.add_argument("--theme", choices=["dark", "light", "both"], default="both")
    ap.add_argument("--out", default=str(DEFAULT_OUT),
                    help="directory for frames + report.json")
    ap.add_argument("--list", action="store_true", help="list layer names")
    a = ap.parse_args()

    if a.list:
        print("layers:")
        for k, (p, _, rd) in LAYERS.items():
            print(f"  {k:14s} {p}{'   (walks into the text)' if rd else ''}")
        return 0

    chosen = a.layer or list(LAYERS)
    unknown = [c for c in chosen if c not in LAYERS]
    if unknown:
        print("unknown layer(s): %s\n  try --list" % ", ".join(unknown))
        return 2

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    port = free_port()
    serve(REPO, port)
    base = f"http://127.0.0.1:{port}/"

    modes = [("desktop", DESKTOP, False), ("phone", PHONE, True)]
    if a.width != "both":
        modes = [m for m in modes if m[0] == a.width]
    themes = ["dark", "light"] if a.theme == "both" else [a.theme]

    report = []
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for mode, vp, mobile in modes:
            for theme in themes:
                ctx = br.new_context(viewport=vp, is_mobile=mobile,
                                     has_touch=mobile,
                                     device_scale_factor=2 if mobile else 1)
                ctx.add_init_script(
                    "try{localStorage.setItem('da-theme','%s')}catch(e){}" % theme)
                pg = ctx.new_page()
                errs: list[str] = []
                pg.on("console", lambda m: errs.append(f"{m.type}: {m.text[:150]}")
                      if m.type == "error" else None)
                pg.on("pageerror", lambda e: errs.append(f"pageerror: {str(e)[:150]}"))

                for name in chosen:
                    path, settle, reading = LAYERS[name]
                    errs.clear()
                    try:
                        pg.goto(base + path, wait_until="domcontentloaded",
                                timeout=45000)
                        pg.wait_for_timeout(settle)
                        if reading:
                            enter_reading(pg)
                    except Exception as e:                       # noqa: BLE001
                        report.append({"layer": name, "mode": mode,
                                       "theme": theme, "FATAL": str(e)[:200]})
                        print(f"  FATAL {name} {mode} {theme}: {str(e)[:80]}")
                        continue
                    # §8.1d in this tool's own report: the ruled floor is
                    # 44 at phone widths and 38 at desktop (106-P2 item 4
                    # calls that split deliberate). Reporting desktop
                    # targets against 44 would name a violation that no
                    # ruling states.
                    floor = 44 if mobile else 38
                    d = pg.evaluate(PROBE_JS,
                                    {"vw": vp["width"], "floor": floor})
                    stem = f"{name}_{mode}_{theme}"
                    pg.screenshot(path=str(out / f"{stem}.png"))
                    d.update(layer=name, mode=mode, theme=theme,
                             frame=stem + ".png", console=errs[:10])
                    report.append(d)
                    ink = d["ink"]
                    print(f"  {stem:34s} overflow={d['overflow']:>4} "
                          f"off={len(d['offscreen']):>2} "
                          f"under{floor}={len(d['tiny']):>3} "
                          f"err={len(errs)}"
                          + (f"  ink {ink['left']}/{ink['right']} "
                             f"(asym {ink['asym']})" if ink else ""))
                ctx.close()
        br.close()

    (out / "report.json").write_text(json.dumps(report, indent=1),
                                     encoding="utf-8")
    visits = len(report)
    print(f"\n  {visits} visit(s) -> {out}")
    # A walk reports; it does not fail. But a walk that rendered nothing
    # is not a clean walk, it is a broken harness (§8.1b).
    if not visits:
        print("  STOP: rendered 0 pages — the harness did not run.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
