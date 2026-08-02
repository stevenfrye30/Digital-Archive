# -*- coding: utf-8 -*-
"""Task 119b item 3 — every sentence a READER sees that names the lens.

The moment the STRUCTURE/RIGHTS toggle retires, any sentence naming it
becomes false. The masthead lede is the known case and it is not
authored markup — it is assembled at runtime inside a script — so a
source grep cannot find it and a source grep also drowns in CSS
selectors and code comments containing the word "lens" (the first
version of this tool reported 1,569 "clauses", nearly all of them
`body[data-lens=` selectors).

So this reads the RENDERED page, in BOTH lens states, and looks only at
text a reader can actually see.

TWO CLASSES, the ruling's own distinction:
  LENS-NAMING    — names the toggle, a view, or the act of switching.
                   False the moment the toggle goes. Must be rewritten
                   or deleted IN THE SAME EDIT that retires it.
  COLOUR-MEANING — says only what a colour or mark MEANS. Still true
                   under one view; stays untouched.

Reports. Changes nothing.
"""
from __future__ import print_function

import io
import json
import os
import re
import socket
import socketserver
import http.server
import threading
from contextlib import closing

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MAP = os.path.join(REPO, "map")

ROOMS = sorted(
    f[:-5] for f in os.listdir(MAP)
    if f.endswith(".html")
    and "Task 111 " in io.open(os.path.join(MAP, f), encoding="utf-8").read()
)

NAMING = re.compile(
    r"(rights lens|structure view|rights view|structure mode|rights mode|"
    r"\bthis view\b|\bthe other view\b|\bboth views\b|\bre-?colou?rs?\b|"
    r"\btoggle\b|\bswitch(?:ing)? to\b|\blens\b)", re.I)

# Task 119c — THE SHARPER TEST, which supersedes NAMING as the gate:
# not "does the sentence name the lens" but "is the sentence still TRUE
# once one mark carries four states". A sentence can name no instrument
# and still be false — "Coloured by what the archive holds" is the case
# that proved it: strip the lens parenthetical and it passes a
# lens-naming test while asserting the marks mean holdings, which after
# the merge they do not (held is one of four).
MEANING = re.compile(
    r"\bcolou?r(?:ed|s|ing)?\b|\bmarks?\b|\bdot\b|\bshaded?\b|"
    r"\bgreen\b|\bamber\b|\bred\b|\borange\b|\bhollow\b|\bfilled\b", re.I)

# a claim about what the colour/mark MEANS, as opposed to a count that
# merely uses the word (e.g. "213 green of 221")
CLAIM = re.compile(
    r"\bcolou?r(?:ed|ing)?\s+by\b|\bcolou?r\s*=|\bmeans?\b|\bshows?\b|"
    r"\bindicates?\b|\bmarks?\b(?!\s+\d)|\bwhat the archive holds\b|"
    r"\bcoloured by\b|\bcolou?r-coded\b", re.I)

COLOUR = re.compile(r"\b(green|amber|red|colour|color)\b", re.I)

VISIBLE_TEXT = """
() => {
  const out = [];
  const seen = new Set();
  document.querySelectorAll(
    'header.mast p, .blurb, .greenline, .insight, .statband, .legend, '
    + '#m-legend, .lg, .stat, .keyrow, .zone-h, .basket > h2, footer, '
    + '.fam > summary, .caveat, .note, .canon-note'
  ).forEach(e => {
    const s = getComputedStyle(e);
    if (s.display === 'none' || s.visibility === 'hidden') return;
    const t = (e.innerText || e.textContent || '').replace(/\\s+/g, ' ').trim();
    if (t && t.length > 12 && !seen.has(t)) { seen.add(t); out.push(t); }
  });
  return out;
}
"""

SENT = re.compile(r"[^.!?]*[.!?]|[^.!?]+$")


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

    found = {}     # normalised sentence -> {rooms, views, sample}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        for room in ROOMS:
            for view in ("structure", "rights"):
                pg.goto(base + "map/%s.html?lens=%s" % (room, view),
                        wait_until="networkidle")
                pg.wait_for_timeout(300)
                for block in pg.evaluate(VISIBLE_TEXT):
                    for m in SENT.finditer(block):
                        s = " ".join(m.group().split())
                        if len(s) < 13:
                            continue
                        names = bool(NAMING.search(s))
                        # the sharper gate: asserts what a mark MEANS
                        claims = bool(MEANING.search(s) and CLAIM.search(s))
                        if not (names or claims):
                            continue
                        key = re.sub(r"\d+", "N", s)
                        d = found.setdefault(key, {"rooms": set(), "views": set(),
                                                   "sample": s, "names": names,
                                                   "claims": claims})
                        d["rooms"].add(room)
                        d["views"].add(view)
        pg.close()
        b.close()
    httpd.shutdown()

    print("TASK 119b ITEM 3 — LENS-NAMING SWEEP (rendered text, both views)\n")
    if not found:
        print("  no reader-visible sentence names the lens.")
        return
    print("  %d distinct reader-visible sentences name the lens.\n" % len(found))
    for key, d in sorted(found.items(), key=lambda kv: -len(kv[1]["rooms"])):
        tag = ("NAMES-LENS" if d["names"] else "") +               (" + " if d["names"] and d["claims"] else "") +               ("CLAIMS-MEANING" if d["claims"] else "")
        newly = "   <== MISSED BY THE FIRST SWEEP" if (d["claims"] and not d["names"]) else ""
        print("  [%2d/16 rooms · %s] %s%s" %
              (len(d["rooms"]), "+".join(sorted(d["views"])), tag, newly))
        print("      %s" % d["sample"][:300])
        if len(d["rooms"]) < len(ROOMS):
            print("      rooms: %s" % ", ".join(sorted(d["rooms"])))
        print("")

    out = os.path.join(HERE, "lens_clause_sweep.json")
    io.open(out, "w", encoding="utf-8", newline="\n").write(json.dumps(
        {k: {"rooms": sorted(v["rooms"]), "views": sorted(v["views"]),
             "sample": v["sample"]} for k, v in found.items()},
        indent=1, ensure_ascii=False))
    print("wrote " + out)


if __name__ == "__main__":
    main()
