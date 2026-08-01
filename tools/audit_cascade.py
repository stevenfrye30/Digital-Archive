#!/usr/bin/env python3
"""audit_cascade.py — where the stylesheet fights itself.

The reader is one file of ~1.13 MB carrying a hundred tasks of layered
CSS, plus a `.deep` scope class and ID-weight chrome rules. New rules
are placed by archaeology and, when they lose, they lose SILENTLY —
eight times in the 2026-08-01 session alone.

This does not change anything. It measures, so that any restructuring
is done on evidence:

  DEAD       rules that match elements but never win a single property
             on this page at this viewport.

             READ THIS BEFORE DELETING ANYTHING: the audit walks INTO
             media queries, so every rule written for the ≤720 world
             looks dead at 1440px. "Dead" here means "shadowed in the
             state I measured", never "unused". A rule is only a real
             deletion candidate if it is dead across every page AND
             every viewport, and the surface battery still passes
             without it.
  CONTESTED  the property/element pairs with the deepest override stacks
             — the places where the next rule will probably lose too
  WEIGHT     how much of each page's cascade is ID-weight or !important

It resolves the cascade the way a browser does (importance, then
specificity, then document order) over the rules that actually match.

    python tools/audit_cascade.py                # every surveyed page
    python tools/audit_cascade.py --page cover
    python tools/audit_cascade.py --top 30
"""
from __future__ import annotations

import argparse
import http.server
import json
import socket
import socketserver
import sys
import threading
from contextlib import closing
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "reports" / "cascade_audit.md"

PAGES = {
    "entrance": "",
    "cover": "?text=bible_kjv.json",
    "reading": "?text=thus-spake-zarathustra_common.json&__enter=1",
    "room": "map/christianity.html",
    "shelf": "shelf/philosophy.html",
    "hall": "hall/",
    "philosophy": "philosophy.html",
}

# Resolve the cascade over matching rules only. Returns, per page:
#   rules[]  {sel, spec, order, props, wins}
JS = r"""
() => {
  const spec = (sel) => {
    // a diagnostic-grade specificity: ids, then classes/attrs/pseudo-classes,
    // then element names. Good enough to rank rules against each other.
    let s = sel.replace(/\([^)]*\)/g, '');
    const ids = (s.match(/#[\w-]+/g) || []).length;
    const cls = (s.match(/\.[\w-]+|\[[^\]]+\]|:(?!:)[\w-]+/g) || []).length;
    const els = (s.match(/(^|[\s>+~])[a-zA-Z][\w-]*/g) || []).length;
    return ids * 10000 + cls * 100 + els;
  };
  const rules = [];
  let order = 0;
  const walk = (list) => {
    for (const r of list) {
      if (r.type === 1) {
        const props = [];
        for (let i = 0; i < r.style.length; i++) {
          const p = r.style[i];
          props.push({ p, imp: r.style.getPropertyPriority(p) === 'important' });
        }
        if (props.length) {
          for (const sel of r.selectorText.split(',')) {
            rules.push({ sel: sel.trim(), spec: spec(sel.trim()),
                         order: order++, props, wins: 0, matched: 0 });
          }
        }
      } else if (r.cssRules && r.cssRules.length) {
        walk(r.cssRules);
      }
    }
  };
  for (const ss of document.styleSheets) { try { walk(ss.cssRules); } catch (e) {} }

  // element -> declarations that reach it
  const byEl = new Map();
  rules.forEach((rule, ri) => {
    let els = [];
    try { els = document.querySelectorAll(rule.sel); } catch (e) { return; }
    rule.matched = els.length;
    els.forEach(el => {
      let bucket = byEl.get(el);
      if (!bucket) { bucket = []; byEl.set(el, bucket); }
      bucket.push(ri);
    });
  });

  // resolve per element per property; count wins and stack depth
  const contested = new Map();   // "prop @ selectorOfWinner" -> {n, depth, sample}
  byEl.forEach((ris, el) => {
    const perProp = new Map();
    ris.forEach(ri => {
      rules[ri].props.forEach(({ p, imp }) => {
        let arr = perProp.get(p);
        if (!arr) { arr = []; perProp.set(p, arr); }
        arr.push({ ri, imp });
      });
    });
    perProp.forEach((arr, p) => {
      arr.sort((a, b) => {
        if (a.imp !== b.imp) return a.imp ? 1 : -1;
        const A = rules[a.ri], B = rules[b.ri];
        if (A.spec !== B.spec) return A.spec - B.spec;
        return A.order - B.order;
      });
      const win = arr[arr.length - 1];
      rules[win.ri].wins++;
      if (arr.length >= 3) {
        const key = p + ' @ ' + rules[win.ri].sel;
        const cur = contested.get(key) || { n: 0, depth: 0, losers: [] };
        cur.n++;
        cur.depth = Math.max(cur.depth, arr.length);
        arr.slice(0, -1).forEach(l => {
          const s = rules[l.ri].sel;
          if (cur.losers.indexOf(s) < 0 && cur.losers.length < 4) cur.losers.push(s);
        });
        contested.set(key, cur);
      }
    });
  });

  const dead = rules.filter(r => r.matched > 0 && r.wins === 0)
                    .map(r => ({ sel: r.sel, matched: r.matched,
                                 props: r.props.map(x => x.p).slice(0, 4) }));
  const idWeight = rules.filter(r => r.spec >= 10000).length;
  const impCount = rules.reduce((n, r) => n + r.props.filter(p => p.imp).length, 0);
  return {
    nRules: rules.length,
    nDecls: rules.reduce((n, r) => n + r.props.length, 0),
    nMatching: rules.filter(r => r.matched > 0).length,
    dead, idWeight, impCount,
    contested: [...contested.entries()]
      .map(([k, v]) => ({ key: k, n: v.n, depth: v.depth, losers: v.losers }))
      .sort((a, b) => b.depth - a.depth || b.n - a.n).slice(0, 40),
  };
}
"""


def free_port() -> int:
    with closing(socket.socket()) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def serve(port: int):
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(  # noqa: E731
        *a, directory=str(REPO), **k)
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    httpd.log_message = lambda *a, **k: None
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", choices=sorted(PAGES), action="append")
    ap.add_argument("--top", type=int, default=20)
    a = ap.parse_args()
    port = free_port()
    serve(port)
    base = f"http://127.0.0.1:{port}/"
    pages = a.page or list(PAGES)
    lines = ["# Cascade audit", "",
             "*Where the stylesheet fights itself. Generated by "
             "`tools/audit_cascade.py`; nothing here is changed by running it.*", "",
             "**A rule listed as dead is shadowed IN THE MEASURED STATE — one "
             "viewport (1440px), one page, one theme. The audit walks into media "
             "queries, so every mobile rule looks dead here. Dead is not unused; "
             "treat it as a lead, never a licence to delete.**", ""]
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_context(viewport={"width": 1440, "height": 1000}).new_page()
        for name in pages:
            url = base + PAGES[name]
            pg.goto(url.replace("&__enter=1", ""), wait_until="networkidle")
            pg.wait_for_timeout(1400)
            if name == "reading":
                pg.evaluate("""() => { const b = [...document.querySelectorAll('button')]
                  .find(x => /Read from beginning/.test(x.textContent)); b && b.click(); }""")
                pg.wait_for_timeout(900)
            m = pg.evaluate(JS)
            print(f"\n=== {name} ===")
            print(f"  rules {m['nRules']} ({m['nMatching']} match something) · "
                  f"declarations {m['nDecls']} · ID-weight rules {m['idWeight']} · "
                  f"!important declarations {m['impCount']}")
            print(f"  DEAD in this state (shadowed here; mobile rules look "
                  f"dead at this width): {len(m['dead'])}")
            for d in m["dead"][:a.top]:
                print(f"     {d['sel'][:66]:66} x{d['matched']:<4} {','.join(d['props'])}")
            print("  CONTESTED (deepest override stacks):")
            for c in m["contested"][:a.top]:
                print(f"     depth {c['depth']:<3} {c['key'][:72]}")
                for l in c["losers"][:3]:
                    print(f"            loses: {l[:66]}")
            lines += [f"## {name}", "",
                      f"- rules **{m['nRules']}** ({m['nMatching']} match something)",
                      f"- declarations **{m['nDecls']}**",
                      f"- ID-weight rules **{m['idWeight']}**",
                      f"- `!important` declarations **{m['impCount']}**",
                      f"- **dead** (match elements, win nothing): **{len(m['dead'])}**", ""]
            if m["dead"]:
                lines += ["| selector | elements | properties |", "|---|---:|---|"]
                lines += [f"| `{d['sel']}` | {d['matched']} | {', '.join(d['props'])} |"
                          for d in m["dead"][:40]]
                lines.append("")
            if m["contested"]:
                lines += ["Deepest override stacks:", "",
                          "| depth | property @ winner | it beats |", "|---:|---|---|"]
                lines += [f"| {c['depth']} | `{c['key']}` | "
                          + "; ".join(f"`{x}`" for x in c["losers"][:3]) + " |"
                          for c in m["contested"][:20]]
                lines.append("")
        b.close()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwritten: {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
