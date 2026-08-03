# -*- coding: utf-8 -*-
"""Task 116 phase 1 — what actually renders a text chip, in all 16 rooms.

SWEPT BY CONTENT, NOT BY CLASS NAME. That instruction is the whole
reason this lane exists: the Task 111 survey searched `span.te`, found
none in buddhist, concluded the thing was absent — buddhist used
`div.ed`. So nothing here starts from a class list.

Chips are identified by WHAT THEY SAY. Each room's own structure.json
holds the authored chip names; we find the DOM node whose text is one
of those names, then climb to the outermost ancestor still carrying
just that one name. That ancestor IS the chip box, whatever it is
called. Families are forced open first, or a collapsed room reports
nothing and the silence reads as absence (the Task 114 trap).
"""
from __future__ import print_function

import io
import json
import os
import socket
import socketserver
import http.server
import threading
from contextlib import closing

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MAP = os.path.join(REPO, "map")
MAPS = os.path.join(REPO, "maps")
# structure.json left the served tree in Task 138 — it is a build input, and
# maps/ is deployed. It now sits with the scripts that build from it, which
# lives in the PARENT repo, one level above this one.
CFG_MAPS = os.path.join(REPO, os.pardir, "05_scripts", "configs", "maps")

ROOMS = sorted(
    f[:-5] for f in os.listdir(MAP)
    if f.endswith(".html")
    and "Task 111 " in io.open(os.path.join(MAP, f), encoding="utf-8").read()
)


def chip_names(room):
    p = os.path.join(CFG_MAPS, room, "structure.json")
    if not os.path.exists(p):
        return []
    d = json.load(io.open(p, encoding="utf-8"))
    names = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("chips", "texts", "items", "entries") and isinstance(v, list):
                    for c in v:
                        if isinstance(c, dict):
                            n = c.get("name") or c.get("title") or c.get("t")
                            if n:
                                names.append(n)
                        elif isinstance(c, str):
                            names.append(c)
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(d)
    return names


SWEEP = r"""
(names) => {
  const want = new Set(names.map(s => s.replace(/\s+/g, ' ').trim()));
  const norm = s => (s || '').replace(/\s+/g, ' ').trim();

  // How many authored names live inside this element? The chip box is the
  // largest ancestor that still holds exactly one — climbing stops the
  // moment a parent gathers a second chip, which is what makes it a
  // container rather than a chip. Nothing here names a class.
  const nameCount = el => {
    let n = 0;
    if (want.has(norm(el.textContent))) return 1;
    el.querySelectorAll('*').forEach(d => {
      if (want.has(norm(d.textContent)) || want.has(norm(d.getAttribute('title') || ''))) {
        // count only the outermost carrier of each name
        if (!d.parentElement || (norm(d.parentElement.textContent) !== norm(d.textContent)
            && !want.has(norm(d.parentElement.getAttribute('title') || '')))) n++;
      }
    });
    return n;
  };
  const STOP = { DETAILS: 1, SECTION: 1, MAIN: 1, BODY: 1, HTML: 1, UL: 1, OL: 1 };
  const isBlock = e => {
    const d = getComputedStyle(e).display;
    return d === 'block' || d === 'flex' || d === 'grid';
  };
  const boxOf = el => {
    let b = el;
    while (b.parentElement && !STOP[b.parentElement.tagName]
           && b.parentElement.children.length <= 4
           && nameCount(b.parentElement) === 1
           // a block wrapper around an inline chip is a CONTAINER that
           // happens to hold one chip, not a bigger chip. Without this the
           // sweep reports div.fambody as a chip in every room whose
           // family has exactly one member.
           && !(isBlock(b.parentElement) && !isBlock(b))) {
      b = b.parentElement;
    }
    return b;
  };

  const seen = new Set(), out = {};
  // a carrier says an authored name in its TEXT or in its title attribute
  // (buddhist splits the visible name across <b> and <span>, so text
  // equality alone cannot see it — the Task 114 failure, again)
  document.querySelectorAll('*').forEach(el => {
    const t = norm(el.textContent);
    const ttl = norm(el.getAttribute('title') || '');
    const isCarrier = (want.has(t) && el.children.length <= 3) || want.has(ttl);
    if (!isCarrier) return;
    const box = boxOf(el);
    if (seen.has(box)) return;
    seen.add(box);

    const s = getComputedStyle(box);
    const r = box.getBoundingClientRect();
    if (!r.width || !r.height) return;

    const state = Array.from(box.classList)
      .filter(c => /^(g|a|r|m-held|m-several|m-restricted|x|mx)$/.test(c))
      .sort().join('+') || 'none';
    const sig = box.tagName.toLowerCase() + '.' +
      Array.from(box.classList)
        .filter(c => !/^(g|a|r|x|mx|on|open)$|^m-/.test(c))
        .sort().join('.');

    // the dot: first empty inline child of chip-dot size
    let dot = null;
    box.querySelectorAll('*').forEach(c => {
      if (dot) return;
      if (norm(c.textContent)) return;
      const cr = c.getBoundingClientRect();
      if (cr.width > 0 && cr.width <= 18 && cr.height <= 18) {
        dot = { w: +cr.width.toFixed(1), h: +cr.height.toFixed(1),
                fromLeft: +(cr.left - r.left).toFixed(1),
                bg: getComputedStyle(c).backgroundColor };
      }
    });

    // where the NAME's ink actually starts (measure ink, not the box)
    let nameLeft = null;
    const rng = document.createRange();
    const tw = document.createTreeWalker(box, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = tw.nextNode())) {
      if (!n.textContent.trim()) continue;
      rng.selectNodeContents(n);
      const rr = rng.getClientRects()[0];
      if (rr) { nameLeft = +(rr.left - r.left).toFixed(1); break; }
    }

    if (!out[sig]) {
      out[sig] = {
        n: 0, tag: box.tagName.toLowerCase(),
        classes: Array.from(box.classList).join(' '),
        pad: s.paddingTop + ' ' + s.paddingRight + ' ' +
             s.paddingBottom + ' ' + s.paddingLeft,
        radius: s.borderTopLeftRadius + '/' + s.borderBottomRightRadius,
        borderW: [s.borderTopWidth, s.borderRightWidth,
                  s.borderBottomWidth, s.borderLeftWidth].join('/'),
        borderS: [s.borderTopStyle, s.borderRightStyle,
                  s.borderBottomStyle, s.borderLeftStyle].join('/'),
        borderC: s.borderLeftColor,
        bg: s.backgroundColor, color: s.color,
        font: s.fontSize + '/' + s.fontWeight,
        display: s.display,
        dot: dot, nameLeft: nameLeft,
        sample: (t || ttl).slice(0, 40),
        states: {},
      };
    }
    out[sig].n += 1;
    // fills are state-dependent, so record per state — sampling one chip
    // per signature would report whichever state happened to come first
    if (!out[sig].states[state]) {
      out[sig].states[state] = {
        n: 0, bg: s.backgroundColor, borderC: s.borderLeftColor,
        borderW: s.borderLeftWidth, color: s.color,
        dotBg: dot ? dot.bg : null,
      };
    }
    out[sig].states[state].n += 1;
  });
  return out;
}
"""

OPEN_ALL = """
() => {
  document.querySelectorAll('details').forEach(d => d.open = true);
}
"""


def free_port():
    with closing(socket.socket()) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main():
    port = free_port()
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(  # noqa: E731
        *a, directory=str(REPO), **k)
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    httpd.log_message = lambda *a, **k: None
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d/" % port

    report = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        for room in ROOMS:
            names = chip_names(room)
            report[room] = {"n_names": len(names)}
            for mode in ("light", "dark"):
                pg.goto(base + "map/%s.html" % room, wait_until="networkidle")
                pg.evaluate(
                    "(m)=>document.documentElement.setAttribute('data-theme',m)",
                    mode)
                pg.wait_for_timeout(200)
                pg.evaluate(OPEN_ALL)
                pg.wait_for_timeout(260)
                report[room][mode] = pg.evaluate(SWEEP, names)
        pg.close()
        b.close()
    httpd.shutdown()

    out = os.path.join(HERE, "chip_inventory.json")
    io.open(out, "w", encoding="utf-8", newline="\n").write(
        json.dumps(report, indent=1, ensure_ascii=False))

    print("=== CHIP BOXES BY ROOM (light) ===")
    sigs = {}
    for room in ROOMS:
        d = report[room]["light"]
        tot = sum(v["n"] for v in d.values())
        print("\n%-13s %d authored names, %d chips found, %d distinct box(es)"
              % (room, report[room]["n_names"], tot, len(d)))
        for k, v in sorted(d.items(), key=lambda kv: -kv[1]["n"]):
            print("   %-20s n=%-4d pad=%-24s rad=%-11s bw=%-14s bs=%s"
                  % (k, v["n"], v["pad"], v["radius"], v["borderW"], v["borderS"]))
            print("   %-20s bg=%-22s dot=%-7s nameL=%-6s"
                  % ("", v["bg"], (v["dot"] or {}).get("fromLeft"), v["nameLeft"]))
            sigs.setdefault(k, []).append(room)
    print("\n=== BOX SIGNATURES ACROSS ROOMS ===")
    for k, rs in sorted(sigs.items(), key=lambda kv: -len(kv[1])):
        print("  %-22s %2d rooms: %s" % (k, len(rs), ", ".join(rs)))
    print("\nwrote " + out)


if __name__ == "__main__":
    main()
