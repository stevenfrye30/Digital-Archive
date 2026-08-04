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

# Task 148 item 2 — THE ROOM SET IS DERIVED FROM WHAT A FILE IS.
#
# This used to read `"Task 111 " in <page text>`: a room was any page
# still carrying a comment from a 2026-07 lane. That is not a property of
# a room, it is a property of an editorial note, and lanes kept deleting
# them. By HEAD before this fix exactly ONE page still matched — and
# Task 146 removed the comment carrying it, taking the population to
# ZERO — while this file went on printing its findings and writing its
# artifact. A survey that had stopped looking still reported that it saw.
#
# What actually distinguishes the three non-rooms is that they are
# REDIRECT STUBS: map/index.html, map/abrahamic.html and
# map/eastasian.html are noindex pages whose whole body is a
# `<meta http-equiv="refresh">` to the Hall (Tasks 40b and 45). That is
# a fact about the file, so a page that becomes a stub, or a stub that
# becomes a room, needs no edit here (§8.1e).
#
# Validated the way build_room_toc.py validates its own derivation: this
# rule reproduces the {index, abrahamic, eastasian} set that tool names
# by hand, exactly — 3 stubs, 16 rooms.
def _is_stub(path):
    return 'http-equiv="refresh"' in io.open(path, encoding="utf-8").read()


ROOMS = sorted(
    f[:-5] for f in os.listdir(MAP)
    if f.endswith(".html") and not _is_stub(os.path.join(MAP, f))
)
# §8.1b — an empty population must REFUSE, not pass.
if not ROOMS:
    raise SystemExit("inventory_chips: the room set is EMPTY — refusing to "
                     "report on nothing. Check map/*.html.")


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
    # Task 149 item 3 — §8.1b, THE OTHER EMPTINESS. Task 148 fixed the
    # room SET; this is the SWEEP going empty underneath a room set that
    # is perfectly correct. If nothing renders — the block named a
    # missing server, but a bad REPO root, a moved structure.json, a page
    # that 404s under a renamed path and a browser that fails to paint
    # all land in the same place — every per-room sweep returns {} and
    # this file used to serialize that over the tracked artifact and exit
    # 0. The truncation IS the report, and it looks exactly like a sweep
    # that found the archive had no chips.
    #
    # So the guard is written on the OUTCOME rather than on any one
    # cause, and it runs BEFORE the write: nothing is serialized until
    # the sweep has proved it looked.
    refusals = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        for room in ROOMS:
            names = chip_names(room)
            report[room] = {"n_names": len(names)}
            if not names:
                refusals.append(
                    "%s: 0 authored chip names — structure.json missing under "
                    "%s" % (room, os.path.normpath(CFG_MAPS)))
            for mode in ("light", "dark"):
                resp = pg.goto(base + "map/%s.html" % room,
                               wait_until="networkidle")
                # the page it THINKS it is on (Task 124b item 1): a 404
                # body renders happily and sweeps to nothing.
                if resp is None or not resp.ok:
                    refusals.append("%s/%s: page did not load (%s)" % (
                        room, mode, "no response" if resp is None
                        else "HTTP %d" % resp.status))
                    continue
                pg.evaluate(
                    "(m)=>document.documentElement.setAttribute('data-theme',m)",
                    mode)
                pg.wait_for_timeout(200)
                pg.evaluate(OPEN_ALL)
                pg.wait_for_timeout(260)
                report[room][mode] = pg.evaluate(SWEEP, names)
                if not sum(v["n"] for v in report[room][mode].values()):
                    refusals.append(
                        "%s/%s: swept 0 chips from %d authored names"
                        % (room, mode, len(names)))
        pg.close()
        b.close()
    httpd.shutdown()

    if refusals:
        print("inventory_chips: REFUSING TO WRITE — the sweep did not look "
              "at what it claims to report on (%d finding(s)):" % len(refusals))
        for r in refusals[:20]:
            print("  · " + r)
        if len(refusals) > 20:
            print("  · … and %d more" % (len(refusals) - 20))
        print("tools/chip_inventory.json is UNCHANGED. An empty sweep is a "
              "broken instrument, not a finding about the archive.")
        raise SystemExit(1)

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
