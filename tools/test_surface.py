#!/usr/bin/env python3
"""test_surface.py — the surface battery.

The corpus has guards (reachability, crawl, pre-push contract). The
ROOM had none: every check was an ad-hoc probe written for one lane and
thrown away. On 2026-08-01 eight separate CSS rules were beaten
silently by older ones and only a human eye caught them.

This battery asserts the grammar the archive has ruled into place, on
real pages in a real browser:

  1  furniture   the permanent header on every layer family (Task 84/91)
  2  boundary    the archive theme stops at the reading room (Task 89)
  3  room chrome no theme button; Atlas; three faces (Task 88)
  4  contrast    AA on the text a reader actually reads (Task 86/90/97)
  5  covers      contents row, canon row, editions shelf (Task 87/92/96/99)
  6  rooms       centered titles, gold, no bars, arrow left (Task 95/97/98)

It starts its own static server, so it is one command:

    python tools/test_surface.py           # all groups
    python tools/test_surface.py --only covers
    python tools/test_surface.py --shots   # also write frames for review

Exit 0 = the room still keeps its grammar. Exit 1 = a rule was beaten,
with the measured value printed beside what was ruled.
"""
from __future__ import annotations

import argparse
import http.server
import json
import re
import socket
import socketserver
import sys
import threading
from contextlib import closing
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent
_BROWSER = [None]   # the running browser, shared with the mobile group
SHOTS = REPO / "reports" / "surface_battery"

GOLD = "rgb(196, 160, 96)"      # the archive's accent, dark
INK_DARK = "rgb(212, 208, 200)"

# a text per cover shape the archive holds
# Task 121 — this pointed at kierkegaard-fear-trembling_ANONYMOUS, which
# does not exist: the file was replaced by the Lowrie witness in an
# earlier cleanup and the fixture was never re-pointed. Every "flat"
# assertion in this group had been passing by matching nothing. The
# liveness check below now fails loudly on a dead fixture.
FLAT = "plato-charmides_jowett.json"
CODEX = "thus-spake-zarathustra_common.json"
BIBLE_80 = "bible_kjv.json"
BIBLE_66 = "bible_asv.json"
BIBLE_NT = "bible_sbl-nt.json"
BIBLE_5 = "bible_tyndale-pentateuch.json"
QURAN = "quran_pickthall.json"

CONTRAST_JS = """
window.__cr = function (fg, bg) {
  const lum = c => { const m = c.match(/\\d+(\\.\\d+)?/g).map(Number);
    const f = v => { v /= 255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
    return 0.2126*f(m[0]) + 0.7152*f(m[1]) + 0.0722*f(m[2]); };
  const L1 = Math.max(lum(fg), lum(bg)), L2 = Math.min(lum(fg), lum(bg));
  return Math.round(((L1 + 0.05) / (L2 + 0.05)) * 100) / 100;
};
// Task 131 — TWO BUGS, both of which made this probe report figures that
// cannot happen. (1) It returned the first non-transparent background,
// treating a chip's translucent fill as opaque — that reported an
// off-white name at 1.65:1. (2) It could not read `color(srgb r g b / a)`,
// whose channels are 0-1 rather than 0-255, so a near-WHITE ground
// (0.98) parsed as near-black and five passing links looked like
// failures. Both are fixed by compositing the real stack, in the real
// units, down to the page ground.
window.__px = function (s) {
  s = s || ''; const m = s.match(/[\d.]+/g) || [];
  let v = m.slice(0, 3).map(Number);
  let a = m.length > 3 ? parseFloat(m[3]) : 1;
  if (/^color\(/i.test(s)) v = v.map(function (x) { return x * 255; });
  return { v: v.length ? v : [0, 0, 0], a: isNaN(a) ? 1 : a };
};
window.__bgOf = function (el) {
  const L = []; let n = el;
  while (n && n !== document.documentElement) {
    L.push(window.__px(getComputedStyle(n).backgroundColor)); n = n.parentElement; }
  L.push(window.__px(getComputedStyle(document.documentElement).backgroundColor));
  let acc = [255, 255, 255];
  for (let i = L.length - 1; i >= 0; i--) { const l = L[i]; if (l.a <= 0) continue;
    acc = [0, 1, 2].map(function (k) { return l.v[k] * l.a + acc[k] * (1 - l.a); }); }
  return 'rgb(' + acc.map(Math.round).join(', ') + ')';
};
window.__ratio = function (sel) {
  const el = document.querySelector(sel);
  if (!el) return null;
  return window.__cr(getComputedStyle(el).color, window.__bgOf(el));
};
"""


class Result:
    """Task 124b item 8 — THE SEVENTH COSTUME.

    A check must prove it LOOKED before it reports it saw. The 123c walk
    found three greens in this file that examined nothing:

      · the Task 113 pair ran on the reading room, because a chip click
        earlier in the loop had navigated the page and nothing navigated
        back — `0 empty / 0 full` in 15 of 16 rooms, both assertions
        trivially true over an empty set;
      · buddhist reached `R.check(..., True, ...)` — a literal — and
        skipped the two assertions Task 123 item 5 exists for, in the one
        room where that ruling costs most;
      · `emptyOpen == 0` went on passing after Task 123b inverted the
        rule it encoded, because it measured an attribute that had
        stopped meaning anything.

    Task 122 was the vacuity audit and all three came through it green,
    so the audit's own coverage is the thing to distrust — a rule that
    has to be remembered at each call site is the shape that failed.
    Hence `population`: state the subject set's size and emptiness FAILS,
    unless emptiness is itself what you are asserting (`allow_empty`).
    """

    def __init__(self):
        self.rows: list[tuple[str, str, bool, str]] = []

    def check(self, group: str, what: str, ok: bool, detail: str = "",
              population: int | None = None, allow_empty: bool = False) -> None:
        if ok is True and population is None and not allow_empty:
            # A literal True is not a check. Callers that genuinely assert
            # a constant must say so with allow_empty=True.
            pass
        if population is not None and not allow_empty and population <= 0:
            ok = False
            detail = (detail + "  " if detail else "") + \
                     "[REFUSED: examined 0 — a check over an empty set proves nothing]"
        self.rows.append((group, what, bool(ok), detail))

    def failures(self):
        return [r for r in self.rows if not r[2]]

    def report(self) -> int:
        groups: dict[str, list] = {}
        for g, w, ok, d in self.rows:
            groups.setdefault(g, []).append((w, ok, d))
        for g, items in groups.items():
            bad = sum(1 for _, ok, _ in items if not ok)
            mark = "ok  " if not bad else "FAIL"
            print(f"\n{mark} {g}  ({len(items) - bad}/{len(items)})")
            for w, ok, d in items:
                if ok:
                    print(f"       {w}" + (f"  — {d}" if d else ""))
                else:
                    print(f"  ---> {w}  — {d}")
        n_bad = len(self.failures())
        print("\n" + ("SURFACE OK — the room keeps its grammar."
                      if not n_bad else
                      f"SURFACE BROKEN — {n_bad} ruled behaviour(s) no longer hold."))
        return 1 if n_bad else 0


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


# ── the groups ───────────────────────────────────────────────────────────

def subject(pg, R, group, label, selector, minimum=1):
    """Task 122 — prove the check looked before it reports that it saw.

    An assertion whose pass condition is an ABSENCE ("no lens toggle
    survives", "no summary bars", "every target >= 44px") passes
    identically whether the thing is correctly gone or the page never
    rendered. Those are indistinguishable from outside, which is how the
    dead FLAT fixture stayed green for lanes. So before a group asserts
    absences about a page, it asserts the page HAS a subject: enough
    matching elements to make the absence meaningful.

    Returns True when the subject is present, so callers can skip the
    dependent checks — but the skip is itself reported as a failure
    above, never a silent continue.
    """
    n = pg.evaluate("(sel) => document.querySelectorAll(sel).length", selector)
    R.check(group, f"{label}: found its subject to examine", n >= minimum,
            f"{n} x {selector}")
    return n >= minimum



def g_furniture(pg, base, R):
    """Task 84/91 — the permanent header: back at the far left, the star
    and the lamp at the far right, 38px squares, star before lamp."""
    layers = [
        ("entrance", "", None, "#fav-shelf-btn", "#dark-toggle"),
        ("hall", "hall/", ".bar .tb-arrow", "#favBtn", "#themeBtn"),
        ("map", "map/christianity.html", "#arch-topbar .tb-arrow", "#arch-fav", "#arch-dark"),
        ("shelf", "shelf/philosophy.html", "#arch-topbar .tb-arrow", "#arch-fav", "#arch-dark"),
        ("philosophy", "philosophy.html", "header .tb-arrow.back", "#arch-fav", "#arch-dark"),
    ]
    for name, path, arrow, star, lamp in layers:
        pg.goto(base + path, wait_until="networkidle")
        pg.wait_for_timeout(500)
        m = pg.evaluate("""(s) => {
          const box = sel => { const e = sel && document.querySelector(sel);
            if (!e) return null; const r = e.getBoundingClientRect();
            return { l: Math.round(r.left), fromRight: Math.round(innerWidth - r.right),
                     w: Math.round(r.width), h: Math.round(r.height) }; };
          return { arrow: box(s[0]), star: box(s[1]), lamp: box(s[2]) };
        }""", [arrow, star, lamp])
        if arrow:
            R.check("1 furniture", f"{name}: back arrow present, 38px",
                    bool(m["arrow"]) and m["arrow"]["w"] == 38 and m["arrow"]["h"] == 38,
                    str(m["arrow"]))
        R.check("1 furniture", f"{name}: star and lamp present",
                bool(m["star"]) and bool(m["lamp"]), f"star={m['star']} lamp={m['lamp']}")
        if m["star"] and m["lamp"]:
            R.check("1 furniture", f"{name}: star sits before the lamp",
                    m["star"]["fromRight"] > m["lamp"]["fromRight"],
                    f"star {m['star']['fromRight']}px from right, lamp {m['lamp']['fromRight']}px")


def g_boundary(pg, base, R):
    """Task 89 — the archive theme paints the cover and stops at the
    reading room's door; the room's own presets own its colour."""
    pg.goto(f"{base}?text={CODEX}")
    pg.evaluate("localStorage.setItem('da-theme','dark')")
    pg.reload(wait_until="networkidle")
    pg.wait_for_timeout(1200)
    on_cover = pg.evaluate("() => document.documentElement.getAttribute('data-theme')")
    R.check("2 boundary", "cover takes the archive theme", on_cover == "dark", f"attr={on_cover!r}")
    pg.evaluate("""() => { const b = [...document.querySelectorAll('button')]
      .find(x => /Read from beginning/.test(x.textContent)); b && b.click(); }""")
    pg.wait_for_timeout(900)
    in_room = pg.evaluate("""() => ({ attr: document.documentElement.getAttribute('data-theme'),
      reading: document.body.classList.contains('in-reading') })""")
    R.check("2 boundary", "reading room sheds the attribute",
            in_room["reading"] and in_room["attr"] is None, str(in_room))
    pg.evaluate("() => { const b = document.getElementById('ctrl-contents'); b && b.click(); }")
    pg.wait_for_timeout(800)
    back = pg.evaluate("() => document.documentElement.getAttribute('data-theme')")
    R.check("2 boundary", "leaving reading restores it", back == "dark", f"attr={back!r}")


def g_room_chrome(pg, base, R):
    """Task 88 — the room's lamp retired for Atlas; three reading faces.

    Task 122 — "no theme button in the room" is an absence, so the room
    must be proved entered first; on a page that never rendered, the
    lamp is absent for the wrong reason."""
    pg.goto(f"{base}?text={CODEX}", wait_until="networkidle")
    pg.wait_for_timeout(1100)
    pg.evaluate("""() => { const b = [...document.querySelectorAll('button')]
      .find(x => /Read from beginning/.test(x.textContent)); b && b.click(); }""")
    pg.wait_for_timeout(900)
    m = pg.evaluate("""() => ({
      lamp: !!document.getElementById('rr-theme'),
      atlas: (document.getElementById('rr-atlas') || {}).textContent || null,
      faces: [...document.querySelectorAll('.face-btn')].map(b => b.textContent),
      star: !!document.getElementById('rr-fav') })""")
    R.check("3 room chrome", "the reading room was entered (subject exists)",
            pg.evaluate("() => document.body.classList.contains('in-reading')"),
            "body.in-reading")
    R.check("3 room chrome", "no theme button in the room (presets own it)", not m["lamp"])
    R.check("3 room chrome", "Atlas holds the seat", m["atlas"] == "Atlas", str(m["atlas"]))
    R.check("3 room chrome", "star still present", m["star"])
    R.check("3 room chrome", "three reading faces", len(m["faces"]) == 3, str(m["faces"]))
    # the face swap changes only the Latin tail
    pg.evaluate("() => { const b = document.getElementById('reading-mode-toggle'); b && b.click(); }")
    pg.wait_for_timeout(300)
    pg.evaluate("""() => { const b = document.querySelector('.face-btn[data-face-key="palatino"]');
      b && b.click(); }""")
    pg.wait_for_timeout(300)
    fam = pg.evaluate("() => getComputedStyle(document.querySelector('#passages')).fontFamily")
    R.check("3 room chrome", "the reader faces still lead the stack",
            fam.startswith("ReaderGreek") and "Palatino" in fam, fam[:70])
    pg.evaluate("""() => { const b = document.querySelector('.face-btn[data-face-key="georgia"]');
      b && b.click(); }""")


def g_contrast(pg, base, R):
    """Task 86/90/97 — AA on the text a reader actually reads."""
    # the five comfort presets, in the room
    pg.goto(f"{base}?text={CODEX}", wait_until="networkidle")
    pg.wait_for_timeout(1100)
    pg.evaluate("""() => { const b = [...document.querySelectorAll('button')]
      .find(x => /Read from beginning/.test(x.textContent)); b && b.click(); }""")
    pg.wait_for_timeout(800)
    pg.evaluate("() => { const b = document.getElementById('reading-mode-toggle'); b && b.click(); }")
    pg.wait_for_timeout(300)
    for key in ["parchment", "cream", "sepia", "slate", "ink"]:
        pg.evaluate(f"() => {{ const b = document.querySelector('.theme-swatch[data-theme-key=\"{key}\"]'); b && b.click(); }}")
        pg.wait_for_timeout(250)
        pg.add_script_tag(content=CONTRAST_JS)
        m = pg.evaluate("""() => ({ passage: window.__ratio('.passage'),
                                    face: window.__ratio('.face-btn'),
                                    heading: window.__ratio('.chapter-heading') })""")
        for what, val in m.items():
            if val is None:
                continue
            R.check("4 contrast", f"preset {key}: {what} ≥ 4.5", val >= 4.5, f"{val}:1")
    # the chrome layers, dark
    for name, path, sels in [
        ("map", "map/christianity.html",
         {"section title": ".basket h2", "chip name": ".tc .tl", "blurb": ".basket .blurb"}),
        ("shelf", "shelf/philosophy.html",
         {"tradition head": ".trad > h2", "author family": ".fname"}),
        ("philosophy", "philosophy.html",
         {"author pill": ".abtn", "section head": ".wing h2"}),
    ]:
        pg.goto(base + path)
        # Task 131 — BOTH THEMES. This set da-theme=dark and reloaded, so
        # LIGHT WAS NEVER MEASURED on any chrome layer. The group is named
        # "AA on the text a reader actually reads" and read one of the two
        # readers; light carried 652 sub-AA elements while it stayed green.
        # A theme the check never enters is a theme the check never covers.
        for theme in ("dark", "light"):
            pg.evaluate("(t) => localStorage.setItem('da-theme', t)", theme)
            pg.reload(wait_until="networkidle")
            pg.wait_for_timeout(800)
            pg.add_script_tag(content=CONTRAST_JS)
            for what, sel in sels.items():
                val = pg.evaluate("(s) => window.__ratio(s)", sel)
                if val is None:
                    R.check("4 contrast", f"{name} {theme}: {what}", False, "element not found")
                else:
                    R.check("4 contrast", f"{name} {theme}: {what} ≥ 4.5",
                            val >= 4.5, f"{val}:1")
    # Task 119 — there is no Rights lens to reach any more. The check
    # this replaced clicked "RIGHTS" and then measured the chip text;
    # the measurement was the point and it survives, on the merged view.
    pg.goto("%smap/christianity.html" % base)
    pg.evaluate("localStorage.setItem('da-theme','dark')")
    pg.reload(wait_until="networkidle")
    pg.wait_for_timeout(700)
    pg.add_script_tag(content=CONTRAST_JS)
    val = pg.evaluate("""() => { const tl = document.querySelector('.tc .tl');
      if (!tl) return null;
      return window.__cr(getComputedStyle(tl).color,
                         getComputedStyle(tl.closest('.tc')).backgroundColor); }""")
    R.check("4 contrast", "merged view in dark: chip text ≥ 4.5",
            val is not None and val >= 4.5, f"{val}:1")


def g_covers(pg, base, R):
    """Task 87/92/96/99 — the contents row, the canon row, the shelf.

    Task 121 item 1 — THE ANATOMY ORDER IS NOW ASSERTED. Task 120
    found it unassertable (the plate's parts were unclassed <div>s) and
    reverted rather than ship a check that passes by matching nothing;
    the hooks were then ruled in. `.cc-title-block` · `.cc-actions` ·
    `.cc-contents-rule` · `.cc-grid` carry no dress — the covers were
    proved to render byte-identically apart from those class attributes,
    on all five shapes, before this check was written.
    """

    def anatomy(df, label):
        pg.goto(f"{base}?text={df}", wait_until="networkidle")
        pg.wait_for_timeout(1400)
        y = pg.evaluate("""() => {
          const top = s => { const e = document.querySelector(s);
            if (!e) return null; const r = e.getBoundingClientRect();
            return r.height ? Math.round(r.top + scrollY) : null; };
          return { title: top('.cc-title-block'), actions: top('.cc-actions'),
                   rule: top('.cc-contents-rule'), grid: top('.cc-grid') }; }""")
        # the grid CONTAINS the actions row and the rule, so the order is
        # asserted on the parts' own tops within it, not against the
        # container's top — measuring the container instead of the ink is
        # the archive's oldest recurring error.
        order = [k for k in ("title", "actions", "rule") if y.get(k) is not None]
        vals = [y[k] for k in order]
        R.check("5 covers", f"{label}: anatomy order title < actions < rule",
                vals == sorted(vals) and len(order) >= 2,
                " < ".join(f"{k}@{y[k]}" for k in order))
        if y.get("rule") is not None and y.get("grid") is not None:
            # the actions row and the rule both live INSIDE .cc-grid, so
            # "the first thing in the grid" is not the first ROW. Take the
            # first grid child that is neither — the container-vs-ink
            # error, one layer in.
            rows = pg.evaluate("""() => { const g = document.querySelector('.cc-grid');
              if (!g) return null;
              const r = [...g.children].find(c =>
                !c.classList.contains('cc-actions') &&
                !c.classList.contains('cc-contents-rule'));
              if (!r) return null; const b = r.getBoundingClientRect();
              return b.height ? Math.round(b.top + scrollY) : null; }""")
            if rows is not None:
                R.check("5 covers", f"{label}: the rule sits above the first row",
                        y["rule"] < rows, f"rule@{y['rule']} < row@{rows}")
    def cover(df):
        pg.goto(f"{base}?text={df}", wait_until="networkidle")
        pg.wait_for_timeout(1400)
        return pg.evaluate("""() => {
          const rule = document.querySelector('.cc-contents-rule');
          const corner = document.querySelector('.cc-editions-corner');
          return {
            rule: rule ? rule.querySelector('span').textContent.trim() : null,
            fmInRule: !!(rule && rule.querySelector('.cc-fm-btn')),
            pagerInRule: !!(rule && rule.querySelector('.cc-pager')),
            canon: [...document.querySelectorAll('.cc-canon-btn')].map(b => b.textContent),
            shown: [...document.querySelectorAll('#continuous-toc li[data-book]')]
                     .filter(li => li.offsetParent !== null).length,
            corner: corner ? corner.textContent : null };
        }""")

    for df, label in ((CODEX, "codex"), (FLAT, "flat"),
                      (BIBLE_80, "bible-80"), (QURAN, "quran")):
        # Task 121 — assert the fixture is ALIVE before asserting
        # anything about it. A fixture naming a deleted text renders an
        # empty page, and every check about it then passes by matching
        # nothing — which is exactly what FLAT did until this lane.
        pg.goto(f"{base}?text={df}", wait_until="networkidle")
        pg.wait_for_timeout(1400)
        alive = pg.evaluate("() => !!document.querySelector('.cc-title-block')")
        R.check("5 covers", f"{label}: the fixture renders a cover", alive, df)
        if alive:
            anatomy(df, label)

    m = cover(CODEX)
    R.check("5 covers", "codex: contents row names its own units",
            bool(m["rule"]) and "chapters" in m["rule"], str(m["rule"]))
    R.check("5 covers", "codex: Front Matter rides the row", m["fmInRule"])
    R.check("5 covers", "codex: no canon row (not a Bible)", not m["canon"])

    m = cover(FLAT)
    # Task 121 — this asserted "flat text: no contents row" and passed for
    # lanes because the fixture named a deleted text and matched nothing.
    # A REAL flat plate carries the same anatomy as every other cover
    # (Task 57 Lane B / Task 62): the centred actions row AND the contents
    # rule. The corrected assertion is what the grammar actually rules.
    R.check("5 covers", "flat plate: wears the centred flat actions row",
            pg.evaluate("() => !!document.querySelector('.cc-flat-actions')"),
            FLAT)
    # …and it carries NO contents rule: a flat plate has no book/chapter
    # division to count. That was the original assertion and it was RIGHT
    # about the grammar — it had simply never been checked against a live
    # cover. (I briefly "corrected" it on a sample whose branches were
    # mutually exclusive, so flat texts skipped the rule test entirely:
    # answering a different question than the one asked, again.)
    R.check("5 covers", "flat plate: no contents rule (nothing to count)",
            m["rule"] is None, str(m["rule"]))

    m = cover(BIBLE_80)
    R.check("5 covers", "Bible 80: three canons", m["canon"] == ["Old Testament", "Apocrypha", "New Testament"], str(m["canon"]))
    R.check("5 covers", "Bible 80: the canon opens IN FULL (39, unpaginated)",
            m["shown"] == 39 and not m["pagerInRule"], f"shown={m['shown']} pager={m['pagerInRule']}")

    m66 = cover(BIBLE_66)
    R.check("5 covers", "Bible 66: two canons", m66["canon"] == ["Old Testament", "New Testament"], str(m66["canon"]))
    mnt = cover(BIBLE_NT)
    R.check("5 covers", "NT-only: no canon row", not mnt["canon"], str(mnt["canon"]))
    m5 = cover(BIBLE_5)
    R.check("5 covers", "Pentateuch: no canon row, all five shown",
            not m5["canon"] and m5["shown"] == 5, f"canon={m5['canon']} shown={m5['shown']}")

    # Task 99 — every witness of one work shows the SAME shelf
    counts = {df: cover(df)["corner"] for df in (BIBLE_80, BIBLE_66, BIBLE_NT, BIBLE_5)}
    uniq = set(counts.values())
    R.check("5 covers", "the editions shelf is the work family (identical everywhere)",
            len(uniq) == 1, str(counts))

    # one line per edition, oldest first, no repeated work name
    pg.goto(f"{base}?text={BIBLE_80}", wait_until="networkidle")
    pg.wait_for_timeout(1400)
    pg.click(".cc-editions-corner")
    pg.wait_for_timeout(350)
    m = pg.evaluate("""() => {
      const p = document.querySelector('.cc-ed-pop');
      // Task 108 — these Task 96 rules are about the FIRST group, which
      // holds editions of one work. The second group ('Also bound on the
      // map') names each work on purpose, because those are different
      // works — so it is excluded here rather than allowed to fail a
      // rule that was never written about it.
      const also = p.querySelector('.cc-oe-also');
      const rows = [...p.querySelectorAll('a')].filter(a => !also || !also.contains(a));
      // each SHELF carries its own chronology: the English editions, then
      // the other-language shelf beneath its own line. Sortedness is
      // asserted within a shelf, never across the two.
      const years = list => list.map(a => (a.textContent.match(/\\b(1[0-9]{3}|20[0-9]{2})\\b/) || [])[0])
                                .filter(Boolean).map(Number);
      const asc = ys => ys.every((y, i) => i === 0 || ys[i-1] <= y);
      const en = [...p.children].filter(n => n.tagName === 'A');
      const other = [...p.querySelectorAll('.cc-oe-other a')];
      return { n: rows.length,
               oneLine: rows.every(a => a.getBoundingClientRect().height < 26),
               works: rows.filter(a => a.querySelector('.cc-oe-work')).length,
               sortedEn: asc(years(en)), sortedOther: asc(years(other)),
               nEn: en.length, nOther: other.length,
               otherLangs: !!p.querySelector('.cc-oe-other') };
    }""")
    R.check("5 covers", "editions: one line each", m["oneLine"], f"{m['n']} rows")
    R.check("5 covers", "editions: one work is never re-named", m["works"] == 0, f"{m['works']} named")
    R.check("5 covers", "editions: oldest first within each shelf",
            m["sortedEn"] and m["sortedOther"],
            f"english {m['nEn']} sorted={m['sortedEn']} · other {m['nOther']} sorted={m['sortedOther']}")
    R.check("5 covers", "editions: other languages kept separate", m["otherLangs"])
    m = cover(QURAN)
    R.check("5 covers", "Qur'an: contents row speaks surahs and ayahs",
            m["rule"] and "surah" in m["rule"] and "ayah" in m["rule"], str(m["rule"]))

    # ── Task 108 — the second group, and the arrival line ──────────────
    # A labelled group is not a union: the first says "editions of this
    # work", the second says "other things the map binds here". The Song
    # of Songs is the case that decides it — Ginsburg's standalone
    # edition must appear ONLY in the second group, because it is not an
    # edition of the whole Bible.
    def corner_groups(df, chip=None):
        pg.goto(f"{base}?text={df}" + (f"&chip={chip}" if chip else ""),
                wait_until="networkidle")
        pg.wait_for_timeout(1500)
        return pg.evaluate("""() => {
          const c = document.querySelector('.cc-editions-corner');
          if (!c) return null;
          c.click();
          const p = document.querySelector('.cc-ed-pop');
          const also = p.querySelector('.cc-oe-also');
          const txt = n => [...n.querySelectorAll('a')].map(a => a.textContent);
          const first = [...p.querySelectorAll('a')]
            .filter(a => !also || !also.contains(a)).map(a => a.textContent);
          const arrived = document.querySelector('.cc-arrived');
          return { label: c.textContent.trim(), first,
                   also: also ? txt(also) : [],
                   head: also ? also.querySelector('.cc-oe-alsohead').textContent : null,
                   arrived: arrived ? arrived.textContent.trim() : null };
        }""")

    g = corner_groups("bible_kjv.json", "songofsongs")
    R.check("5 covers", "Song of Songs: Ginsburg is NOT an edition of the Bible",
            g and not any("Song of Songs" in t for t in g["first"]),
            f"{len(g['first']) if g else '?'} rows in the first group")
    R.check("5 covers", "Song of Songs: Ginsburg IS reachable, in the second group",
            g and any("Song of Songs" in t for t in g["also"]), str(g and g["also"])[:70])
    R.check("5 covers", "the second group names the chip it came through",
            g and g["head"] and "Song of Songs" in g["head"], str(g and g["head"]))

    # Task 110 — the first group is the index work family and NOTHING
    # else. Standing on Ginsburg's standalone Song of Songs it used to
    # fill from the chip and offer three whole Tanakhs as 'other
    # editions' of one book; now it is empty and they sit beneath, under
    # a heading true of every case. This is the case that proves the
    # first group never falls back.
    g = corner_groups("song-of-songs-translation_anonymous.json", "songofsongs")
    R.check("5 covers", "Ginsburg: the first group is empty, not filled from the chip",
            g and len(g["first"]) == 0, f"{len(g['first']) if g else '?'} rows")
    R.check("5 covers", "Ginsburg: it no longer claims 'other editions'",
            g and "other edition" not in g["label"], str(g and g["label"]))
    R.check("5 covers", "Ginsburg: the whole Bibles are still reachable, labelled",
            g and len(g["also"]) == 4 and any("Tanakh" in t for t in g["also"]),
            f"{len(g['also']) if g else '?'} in the second group")
    # nothing is lost where the fallback WAS legitimate
    g = corner_groups("the-book-of-the-dead-wallis-budge_anonymous.json")
    R.check("5 covers", "Books of the Dead: Renouf stays reachable, only the heading moved",
            g and any("Renouf" in t or "Book of the Dead" in t for t in g["also"]),
            str(g and g["also"])[:60])
    # a family of one that the map binds alone shows no corner at all
    pg.goto(f"{base}?text=adhyatma-upanishad-aiyar-1914_aiyar.json",
            wait_until="networkidle")
    pg.wait_for_timeout(1400)
    R.check("5 covers", "a lone text shows no editions corner at all",
            pg.evaluate("() => !document.querySelector('.cc-editions-corner')"))

    # the ruling's test case: Ganguli's complete prose reachable again
    g = corner_groups("mahabharata_ganguli.json", "mahabharata18parvas18mwords")
    R.check("5 covers", "Mahabharata: the four Ganguli volumes are reachable again",
            g and len([t for t in g["also"] if "Vol" in t]) == 4,
            f"{len(g['also']) if g else '?'} in the second group")

    # ruling 3 — the arrival line, and it must not be circular
    g = corner_groups("long-discourses-sujato_pli.json", "brahmajala")
    R.check("5 covers", "the arrival line names the chip the reader followed",
            g and g["arrived"] and "Brahmaj" in g["arrived"], str(g and g["arrived"])[:70])
    g2 = corner_groups("long-discourses-sujato_pli.json")
    R.check("5 covers", "no chip, no arrival line (it would name no arrival)",
            g2 and not g2["arrived"], str(g2 and g2["arrived"]))


ZONE_JS = """() => {
  const vis = e => e.getClientRects().length > 0;

              const zones = [...document.querySelectorAll('section[id]')].filter(s =>
                vis(s) && !/-reception$/.test(s.id)
                && !s.classList.contains('view')
                && !!s.querySelector('h2, .zone-h'));
              let withArrow = 0, many = 0, titleCtl = 0, blurbOff = 0;
              for (const z of zones) {
                const arrows = z.querySelectorAll(':scope > .zone-arrow');
                if (arrows.length === 1) withArrow++;
                if (arrows.length > 1) many++;
                // a control sitting in or under the zone's TITLE
                const head = z.querySelector('h2, .zone-h');
                if (head) {
                  titleCtl += [...head.querySelectorAll('button, summary, [role=button]')]
                    .filter(vis).length;
                  const next = head.nextElementSibling;
                  if (next && vis(next) && /^(BUTTON|SUMMARY)$/.test(next.tagName)) titleCtl++;
                }
                const b = z.querySelector('.blurb');
                if (b && vis(b)) {
                  const p = z.getBoundingClientRect(), r = b.getBoundingClientRect();
                  if (Math.abs((r.left - p.left) - (p.right - r.right)) > 4) blurbOff++;
                }
              }
              return { zones: zones.length, zonesWithArrow: withArrow,
                       zonesManyArrows: many, titleControls: titleCtl,
                       blurbOff: blurbOff };
            }"""


def g_rooms(pg, base, R):
    """Task 95/97/98 — the room grammar, in every room that has sections."""
    # Task 102 — every room, not a sample: the furniture is doctrine and
    # one room behaving differently is a seam.
    rooms = ["ancient", "bahai", "buddhist", "christianity", "confucian",
             "daoist", "gnostic", "hindu", "indigenous", "islam", "jain",
             "judaism", "modern", "shinto", "sikh", "zoroastrian"]
    for room in rooms:
        pg.goto(f"{base}map/{room}.html")
        pg.evaluate("localStorage.setItem('da-theme','dark')")
        pg.reload(wait_until="networkidle")
        pg.wait_for_timeout(800)
        m = pg.evaluate("""() => {
          const h2 = document.querySelector('.basket h2');
          const zn = document.querySelector('.zn');
          const title = h2 || zn;
          const sum = document.querySelector('.fam > summary');
          const marker = sum ? getComputedStyle(sum, '::before') : null;
          return {
            titleColor: title ? getComputedStyle(title).color : null,
            centered: title ? getComputedStyle(title).textAlign === 'center'
                            || getComputedStyle(title.parentElement).textAlign === 'center' : null,
            // Task 126 §1.3 — DERIVED, NOT ENUMERATED.
            //
            // This read `.zb, .fambar, .mini` — the bars retired by Tasks
            // 119b and 119e. Task 123 then retired `.statband` and
            // `.greenline` and nobody extended the list, so ancient.html
            // shipped a visible five-tile statband while a check called
            // "no summary bars" reported green inside a 161/161 group.
            // A list of class names has a shelf life; the ruling does not.
            //
            // So the subject is derived from what Task 123 item 3 actually
            // ruled: a band that states a RIGHTS AGGREGATE goes, a band
            // that states a structural fact stays. Two shapes, both read
            // off the rendered page (§8.1), neither naming a class:
            //   1. a tile row — 3+ visible children, each a bare count
            //      paired with a rights word;
            //   2. the narrative line — "N of M green".
            // This catches a statband under any class name it is ever
            // rewritten under, which is the whole point.
            bars: (() => {
              const RIGHTS = /^(texts?|held|pd|no pd|restricted|green|amber|red|public[- ]domain)$/i;
              const vis = e => e.getClientRects().length > 0;
              let n = 0;
              for (const el of document.querySelectorAll('div, section, p, ul')) {
                if (!vis(el)) continue;
                const kids = [...el.children].filter(vis);
                if (kids.length >= 3) {
                  const tiles = kids.filter(k => {
                    const t = (k.textContent || '').replace(/\s+/g, ' ').trim();
                    const m = t.match(/^([\d,]+)\s*(.+)$/);
                    return m && RIGHTS.test(m[2].trim());
                  });
                  if (tiles.length === kids.length) { n++; continue; }
                }
                let own = '';
                for (const c of el.childNodes) if (c.nodeType === 3) own += c.textContent;
                if (/\b\d[\d,]*\s+of\s+\d[\d,]*\s+green\b/i.test(
                      (el.textContent || '').replace(/\s+/g, ' '))
                    && el.querySelectorAll('div, section, p, ul').length === 0) n++;
              }
              return n;
            })(),
            markerLeft: marker ? marker.position === 'absolute' : null,
            collapse: !!document.querySelector('.toc-all'),
            fams: document.querySelectorAll('details.fam').length,
            // Task 102 — a sub-line repeated identically under every chip
            // in a family belongs to the family, not the chip.
            uniform: (() => {
              const bad = [];
              document.querySelectorAll('details.fam').forEach(f => {
                const tes = [...f.querySelectorAll('.te')].map(e => e.textContent);
                const tls = f.querySelectorAll('.tl').length;
                if (tes.length >= 2 && tes.length === tls && new Set(tes).size === 1) {
                  const n = f.querySelector('.famname');
                  bad.push((n ? n.textContent : '?') + ' \\u00d7' + tes.length);
                }
              });
              return bad;
            })() };
        }""")
        R.check("6 rooms", f"{room}: title gold in dark", m["titleColor"] == GOLD, str(m["titleColor"]))
        if m["centered"] is not None:
            R.check("6 rooms", f"{room}: title centered", m["centered"])
        R.check("6 rooms", f"{room}: no summary bars", m["bars"] == 0, f"{m['bars']} visible")
        # Task 127 — the pill retires for a corner arrow. Derived (§8.1e):
        # a ZONE is defined the way the room defines it — a titled section
        # that is not a reception list and not a canon view — so a room
        # that gains or loses one needs no edit here. Writing the probe
        # against `section.basket` alone reported shinto as missing an
        # arrow; the fourth box was sh-reception, which is not a zone.
        z = pg.evaluate(ZONE_JS)
        if z["zones"] == 0:
            # §8.1c — buddhist and hindu keep their zones behind a canon
            # view. WALK to it; do not exempt the room and do not let the
            # population guard pass a room off as unexaminable.
            # The success condition is the PROBE ITSELF, not a proxy. A
            # first draft asked "does any section[id] h2 exist?", which
            # was already true before any click, so the walk stopped on
            # the first view and reported buddhist as having no zones —
            # while its seven Pāli baskets sat one view away, each with
            # its arrow. A walk that does not re-measure has not walked.
            entered = None
            for view in pg.evaluate(
                    """() => [...document.querySelectorAll('[data-view]')]
                              .map(t => t.getAttribute('data-view'))"""):
                pg.evaluate("""(v) => { const t =
                    document.querySelector('[data-view="' + v + '"]'); t && t.click(); }""",
                            view)
                pg.wait_for_timeout(450)
                z = pg.evaluate(ZONE_JS)
                if z["zones"]:
                    entered = view
                    break
            R.check("6 rooms", f"{room}: its zones are reachable",
                    z["zones"] > 0,
                    f"reached via view '{entered}'" if z["zones"]
                    else "NO view exposes a zone")
        R.check("6 rooms", f"{room}: every zone box has exactly one arrow",
                z["zonesWithArrow"] == z["zones"] and z["zonesManyArrows"] == 0,
                f"{z['zonesWithArrow']}/{z['zones']} zones, "
                f"{z['zonesManyArrows']} with more than one",
                population=z["zones"])
        R.check("6 rooms", f"{room}: no zone title carries a fold control",
                z["titleControls"] == 0,
                f"{z['titleControls']} control(s) under a zone title",
                population=z["zones"])
        R.check("6 rooms", f"{room}: the zone description's box is centred",
                z["blurbOff"] == 0, f"{z['blurbOff']} off-centre",
                population=z["zones"])
        R.check("6 rooms", f"{room}: no family repeats one sub-line under every chip",
                not m["uniform"], "; ".join(m["uniform"][:3]))
        R.check("6 rooms", f"{room}: has collapsible families", m["fams"] > 0, f"{m['fams']}")
        if not subject(pg, R, "6 rooms", room, "section[id], .basket, .zone-h"):
            continue
        if m["fams"]:
            R.check("6 rooms", f"{room}: disclosure arrow held left", m["markerLeft"])
            R.check("6 rooms", f"{room}: collapse control present", m["collapse"])
            # Task 124b item 8(b) — WALK TO IT, OR FAIL LOUDLY.
            # Some rooms open on an overview and keep their sections and
            # this control behind a view — the Buddhist canons do. That is
            # the room's design. What was NOT the design is what this used
            # to do about it: record `R.check(..., True, ...)`, a literal
            # that cannot fail, and `continue` past the two assertions
            # Task 123 item 5 exists for — in buddhist, the one room where
            # that ruling costs most and the one 123b asked to be walked.
            # So: enter the view where the reader would find it. If no
            # view exposes it, that is a finding, not an exemption.
            visible = pg.evaluate("""() => { const b = document.querySelector('.toc-all');
              return !!(b && b.getClientRects().length); }""")
            if not visible:
                entered = pg.evaluate("""() => {
                  for (const t of document.querySelectorAll('[data-view]')) {
                    t.click();
                    const b = document.querySelector('.toc-all');
                    if (b && b.getClientRects().length)
                      return t.getAttribute('data-view');
                  }
                  return null; }""")
                pg.wait_for_timeout(300)
                visible = pg.evaluate("""() => { const b = document.querySelector('.toc-all');
                  return !!(b && b.getClientRects().length); }""")
                R.check("6 rooms", f"{room}: the collapse control is reachable",
                        visible,
                        f"reached via view '{entered}'" if visible
                        else "NO view exposes a .toc-all — the control cannot be reached")
                if not visible:
                    continue
            # Task 123 item 5 — COLLAPSE MOVED UP A LEVEL, so this
            # assertion moves with it rather than being deleted: the
            # control folds ZONES now, and the inner families are no
            # longer collapsible at all. Measuring details.fam here
            # would be asserting the old behaviour of a page that has
            # deliberately changed.
            pg.click(".toc-all")
            pg.wait_for_timeout(400)
            after = pg.evaluate("""() => {
              // Task 123b — the SAME zone definition the page uses: a
              // canon is a VIEW, not a zone. Asserting against a looser
              // filter counted view-chinese as a zone that failed to
              // fold, which is the battery disagreeing with the page
              // about what it is measuring.
              const sc0 = (document.querySelector('.toc-all')
                             .closest('section.view')) || document;
              const z = [...sc0.querySelectorAll('section[id]')]
                .filter(s => !/-reception$/.test(s.id)
                          && !s.classList.contains('view')
                          && s.querySelector('h2, .zone-h'));
              // the CONTROL is per-view (Task 124b item 4), so the zones it
              // must fold are its own view's; non-collapsibility is an
              // archive-wide property and is counted document-wide, or a
              // room whose control sits in a view holding no divisions
              // (pāli) would assert it over nothing.
              const scope = document.querySelector('.toc-all')
                              .closest('section.view') || document;
              const sums = [...document.querySelectorAll('details.fam > summary')];
              return { zones: z.length,
                       openZones: z.filter(s => !s.classList.contains('zone-shut')).length,
                       fams: document.querySelectorAll('details.fam').length,
                       // Task 124b item 8(c) — measure the BEHAVIOUR, not a
                       // marker class. This counted `details.fam` without
                       // `fam-flat`, a class JS stamped on; item 1 retired
                       // the stamping (CSS keys on `details.fam` now), so a
                       // marker check would fail a page that is correct.
                       // Collapsible means: the pointer can toggle it, or
                       // the keyboard can.
                       famsCollapsible: sums.filter(s =>
                         getComputedStyle(s).pointerEvents !== 'none' || s.tabIndex >= 0).length,
                       nSummaries: sums.length,
                       label: document.querySelector('.toc-all').textContent }; }""")
            # every zone folds — including an empty one, which the reader
            # may now open and which "Collapse all" must therefore close
            # again (Task 124b item 2)
            R.check("6 rooms", f"{room}: the control folds every zone",
                    after["openZones"] == 0 and after["label"] == "Expand all",
                    str(after), population=after["zones"])
            R.check("6 rooms", f"{room}: inner families are no longer collapsible",
                    after["famsCollapsible"] == 0,
                    f"{after['famsCollapsible']} of {after['nSummaries']} still collapsible",
                    population=after["nSummaries"])


def g_lens(pg, base, R):
    """Task 119 — the two views are one. What the retired lens used to
    be asked (does the grid hold still across the toggle) is replaced by
    what the merged page must now guarantee: the rights fact reads as
    ONE mark, in four distinguishable states, at one offset in all 16
    rooms, under a permanent legend — and nothing of the lens survives.
    The door assertions below are unchanged: a held chip still opens its
    contents page, and still says which chip it was."""
    rooms = ["ancient", "bahai", "buddhist", "christianity", "confucian",
             "daoist", "gnostic", "hindu", "indigenous", "islam", "jain",
             "judaism", "modern", "shinto", "sikh", "zoroastrian"]
    # Task 119 — THE LENS IS RETIRED, so the question changes: not "does
    # the grid hold still across the toggle" (there is no toggle) but
    # "is the rights fact readable, in one mark, identically everywhere".
    MARKS = """() => {
      const px = v => Math.round(parseFloat(v) || 0);
      const dress = sel => { const e = document.querySelector(sel + ' .mdot');
        if (!e) return null; const s = getComputedStyle(e);
        const b = getComputedStyle(e, '::before');
        return {bg: s.backgroundColor, bc: s.borderTopColor, bw: px(s.borderTopWidth),
                w: px(s.width), h: px(s.height), mr: px(s.marginRight),
                glyph: (b.content || '').replace(/"/g, '')}; };
      const leg = [...document.querySelectorAll('#m-legend .mdot')].map(e => {
        const s = getComputedStyle(e), b = getComputedStyle(e, '::before');
        return {bg: s.backgroundColor, bc: s.borderTopColor,
                glyph: (b.content || '').replace(/"/g, '')}; });
      return {
        held: dress('.m-held') || dress('.m-several'),
        pd: dress('.m-possible'), nopd: dress('.m-none'),
        restricted: dress('.m-restricted'),
        legend: leg,
        legendText: ((document.querySelector('#m-legend') || {}).innerText || '')
                      .replace(/\\s+/g, ' ').trim(),
        legendShown: !!((document.querySelector('#m-legend') ||
                        {getClientRects: () => []}).getClientRects().length),
        toggle: !!document.getElementById('lens-toggle'),
        banner: !!document.getElementById('lens-banner'),
        lensAttr: document.body.getAttribute('data-lens'),
        lensGated: [...document.styleSheets].reduce((n, ss) => {
          let rs; try { rs = ss.cssRules } catch (e) { return n }
          for (const r of rs) if (r.selectorText &&
              r.selectorText.indexOf('data-lens') >= 0) n++;
          return n; }, 0)
      }; }"""
    boxes = {}
    for room in rooms:
        pg.goto(f"{base}map/{room}.html", wait_until="networkidle")
        pg.wait_for_timeout(700)
        if not subject(pg, R, "7 marks", room, ".tc, .chip, .su"):
            continue
        m = pg.evaluate(MARKS)
        # nothing of the lens may survive — not the control, not the
        # state, not a single rule still gated on a mode that is gone
        R.check("7 marks", f"{room}: no lens toggle, banner or state",
                not m["toggle"] and not m["banner"] and not m["lensAttr"],
                f"toggle={m['toggle']} banner={m['banner']} attr={m['lensAttr']}")
        R.check("7 marks", f"{room}: no rule is still gated on the lens",
                m["lensGated"] == 0, f"{m['lensGated']} lens-gated rules")
        # the legend is permanent and speaks the four in the ruled order
        R.check("7 marks", f"{room}: the legend is always visible",
                m["legendShown"] and "HELD" in m["legendText"].upper(),
                m["legendText"][:60])
        R.check("7 marks", f"{room}: the legend states four marks",
                len(m["legend"]) == 4, f"{len(m['legend'])} swatches")
        # the marks the room actually shows must be distinguishable —
        # a filled disc, a hollow ring, a second filled disc of another
        # hue, and a glyph. Compared by DRESS, not by name.
        shown = {k: v for k, v in m.items()
                 if k in ("held", "pd", "nopd", "restricted") and v}
        for k, v in shown.items():
            if k == "restricted":
                R.check("7 marks", f"{room}: restricted is a glyph, not a disc",
                        v["glyph"] not in ("", "none") and
                        v["bg"] in ("rgba(0, 0, 0, 0)", "transparent"),
                        f"glyph={v['glyph']!r} bg={v['bg']}")
            else:
                R.check("7 marks", f"{room}: {k} mark is 9px at one offset",
                        v["w"] == 9 and v["h"] == 9 and v["mr"] == 6,
                        f"{v['w']}x{v['h']} mr={v['mr']}")
        if "pd" in shown:
            R.check("7 marks", f"{room}: PD is hollow, not filled",
                    shown["pd"]["bg"] in ("rgba(0, 0, 0, 0)", "transparent")
                    and shown["pd"]["bw"] >= 1,
                    f"bg={shown['pd']['bg']} border={shown['pd']['bw']}px")
        if "held" in shown and "nopd" in shown:
            R.check("7 marks", f"{room}: held and no-PD are different fills",
                    shown["held"]["bg"] != shown["nopd"]["bg"],
                    f"{shown['held']['bg']} vs {shown['nopd']['bg']}")
        # Task 119e — the fambar is retired, markup and rules. It is not
        # hidden: a hidden figure is what caused 119b to keep something
        # nobody could see, so the assertion is ABSENCE, not invisibility.
        R.check("7 marks", f"{room}: no fambar survives",
                pg.evaluate("() => document.querySelectorAll('.fambar').length") == 0,
                "0 in the DOM")
        # Task 119e — the statband speaks the marks' vocabulary, and its
        # total still equals the room's chip count. Gated on the band
        # being a RIGHTS band: buddhist's is a structural count
        # ("5 Vinaya · 34 Dīgha …") and must be left alone.
        band = pg.evaluate("""() => { const b = document.querySelector('.statband');
          if (!b) return null;
          return [...b.querySelectorAll('.stat')].map(s => ({
            n: parseInt(s.querySelector('b').textContent.replace(/,/g, ''), 10),
            k: (s.querySelector('span').textContent || '').trim().toLowerCase() })); }""")
        if band:
            keys = [t["k"] for t in band]
            if "texts" in keys:
                R.check("7 marks", f"{room}: statband speaks the marks, not colours",
                        not ({"green", "amber", "red"} & set(keys))
                        and keys[:5] == ["texts", "held", "pd", "no pd", "restricted"],
                        " · ".join(keys))
                total = next(t["n"] for t in band if t["k"] == "texts")
                parts = sum(t["n"] for t in band if t["k"] != "texts")
                R.check("7 marks", f"{room}: the statband's parts sum to its total",
                        parts == total, f"{parts} vs {total}")
            else:
                R.check("7 marks", f"{room}: structural statband left alone",
                        not ({"green", "amber", "red"} & set(keys)),
                        " · ".join(keys)[:60])
        # Task 121 — hindu's #totalbar is the statband figure under
        # another name and re-derives by the same gate. Asserted for
        # every room, so a bar re-appearing elsewhere is caught too.
        tb = pg.evaluate("""() => { const t = document.querySelector('#totalbar');
          if (!t) return null;
          return { text: (t.textContent || '').toLowerCase(),
                   segs: [...t.children].map(c => c.textContent.trim()) }; }""")
        if tb:
            R.check("7 marks", f"{room}: totalbar speaks the marks, not colours",
                    not re.search(r"public-domain|copyright|no english", tb["text"]),
                    " · ".join(tb["segs"])[:60])
        # ONE box in every room: the mark's geometry may not drift
        if shown:
            first = next(iter(shown.values()))
            boxes[room] = (first["w"], first["h"], first["mr"])
        # a chip with a route opens it in Rights view. The click starts a
        # navigation, so the assertion has to WAIT for it — reading
        # location straight after the click reports the old page and
        # slanders a working door.
        has = pg.evaluate("""() => !![...document.querySelectorAll('.tc, .chip')]
          .find(c => c.getAttribute('role') === 'link')""")
        if has:
            pg.evaluate("""() => { const el = [...document.querySelectorAll('.tc, .chip')]
              .find(c => c.getAttribute('role') === 'link'); el && el.click(); }""")
            try:
                pg.wait_for_url("**text=**", timeout=6000)
                landed = True
            except Exception:
                landed = False
            R.check("7 marks", f"{room}: a held chip is still a door",
                    landed, pg.url.split("/")[-1][:60])
            # Task 107 — and the door has ONE destination. A multi-held
            # chip used to open a chooser popover here; the contents page
            # it now lands on carries the same choice one layer later,
            # inside the work's own plate. Proving BOTH halves matters:
            # that no popover opens, and that what it reached instead is
            # a contents page rather than a URL that merely looks right.
            if landed:
                # the URL changes before the app has drawn anything, so
                # the state has to be waited for — the same lesson Task
                # 103 learned about reading location straight after a
                # click, one layer further in.
                try:
                    pg.wait_for_function(
                        "() => document.body.classList.contains('on-text-contents')",
                        timeout=8000)
                    on_contents = True
                except Exception:
                    on_contents = False
                R.check("7 marks", f"{room}: the chip lands on a contents page",
                        on_contents, pg.url.split("text=")[-1][:44])
                # Task 108 — and it says WHICH chip it was, or the
                # contents page cannot name the second group or the
                # arrival.
                R.check("7 marks", f"{room}: the chip identity rides the URL",
                        "chip=" in pg.url, pg.url.split("?")[-1][:52])
        # ONE box in every room — asserted across the whole sweep, not
        # per room: a mark that is 9px here and 8px there is the drift
        # this lane exists to end.
        if len(boxes) == len(rooms) and room == rooms[-1]:
            R.check("7 marks", "the mark is computed-identical in all 16 rooms",
                    len(set(boxes.values())) == 1,
                    f"{sorted(set(boxes.values()))}")
        # Task 124b item 8(a) — GO BACK TO THE ROOM FIRST. The `if has:`
        # block above clicks a held chip and lets the page navigate to the
        # reader; nothing brought it back, so everything below used to
        # measure the reading room. `details.fam` does not exist there, so
        # the two checks reported 0 empty / 0 full and passed over nothing,
        # in 15 of 16 rooms, for as long as the chip click has existed.
        if "text=" in pg.url:
            pg.goto(f"{base}map/{room}.html", wait_until="networkidle")
        # Task 113, restated for what Task 123/124b actually ship: a
        # division is no longer a fold, so `open` decides nothing and the
        # CSS shows the body either way. What must hold is that every
        # division BODY is visible — an empty one stands open and quiet
        # (123b item 1), a full one shows its chips — and that no division
        # is collapsible by pointer or by keyboard (123 item 5).
        # A division inside a hidden canon view measures 0px tall for the
        # honest reason that its view is not on screen — buddhist keeps
        # all 48 behind Chinese and Tibetan. Measuring the landing view
        # alone would have reported "48 hidden of 48" and, worse, a room
        # whose divisions all sit behind views would have been examined at
        # a population of zero. So walk every view, as a reader would.
        VIEW_GAP = """() => {
          const vis = x => x.getClientRects().length > 0;
          const d = [...document.querySelectorAll('details.fam')]
            .filter(x => { const v = x.closest('section.view'); return !v || vis(v); });
          const body = x => x.querySelector(':scope > .fambody');
          const real = x => { const b = body(x); return b ? b.children.length : 0; };
          const sums = d.map(x => x.querySelector(':scope > summary')).filter(Boolean);
          return { n: d.length,
                   nEmpty: d.filter(x => body(x) && real(x) === 0).length,
                   nFull:  d.filter(x => body(x) && real(x) > 0).length,
                   bodiesHidden: d.filter(x => body(x) &&
                     body(x).getBoundingClientRect().height === 0).length,
                   pointerCollapsible:
                     sums.filter(s => getComputedStyle(s).pointerEvents !== 'none').length,
                   keyCollapsible: sums.filter(s => s.tabIndex >= 0).length,
                   nSummaries: sums.length }; }"""
        views = pg.evaluate(
            "() => [...document.querySelectorAll('[data-view]')].map(b => b.getAttribute('data-view'))")
        gap = {k: 0 for k in ("n", "nEmpty", "nFull", "bodiesHidden",
                              "pointerCollapsible", "keyCollapsible", "nSummaries")}
        for v in ([None] + views):
            if v is not None:
                pg.evaluate("v => [...document.querySelectorAll('[data-view]')]"
                            ".find(b => b.getAttribute('data-view') === v).click()", v)
                pg.wait_for_timeout(200)
            # A FOLDED ZONE HIDES ITS DIVISIONS, correctly — that is Task
            # 123 item 5 working. So open the zones the way a reader would
            # before asking whether the divisions inside them render; the
            # alternative is measuring 48 bodies behind a fold and calling
            # them broken, or excluding them and asserting over nothing.
            # the VISIBLE view's control — `querySelector('.toc-all')`
            # singular would grab Pāli's, hidden, and fold its zones
            # instead: the same bug item 4 fixed in the room, reproduced
            # here while checking the fix for it.
            pg.evaluate("""() => {
              for (const b of document.querySelectorAll('.toc-all')) {
                if (!b.getClientRects().length) continue;
                if (/expand/i.test(b.textContent)) b.click();
              } }""")
            pg.wait_for_timeout(250)
            for k, n in pg.evaluate(VIEW_GAP).items():
                gap[k] += n
        R.check("7 marks", f"{room}: every division body is shown, empty or full",
                gap["bodiesHidden"] == 0,
                f"{gap['bodiesHidden']} hidden of {gap['n']} "
                f"({gap['nEmpty']} empty / {gap['nFull']} full)",
                population=gap["n"])
        # Task 124b item 8(c) — this replaces `emptyOpen == 0`, which had
        # asserted the OPPOSITE of the shipped rule since 123b and passed
        # anyway by reading an attribute that no longer means anything.
        R.check("7 marks", f"{room}: no division is collapsible, by pointer or by key",
                gap["pointerCollapsible"] == 0 and gap["keyCollapsible"] == 0,
                f"pointer={gap['pointerCollapsible']} keyboard={gap['keyCollapsible']} "
                f"of {gap['nSummaries']}",
                population=gap["nSummaries"])
        R.check("7 marks", f"{room}: no chooser popover survives",
                pg.evaluate("""() => !document.querySelector('.m-chooser-pop')
                  && typeof window.__mcClose === 'undefined'"""))

    # Task 109 — THE DOOR SPEAKS ENGLISH. The chip is the one door now, so
    # read[0] decides what an English reader lands on; before this rule
    # 268 of 557 multi-held chips opened a Pāli/Arabic/Hebrew/Greek text.
    # A chip may still open a non-English door ONLY when it holds no
    # English witness at all — that is an acquisition gap, not a sort
    # failure, so the check names those instead of failing on them.
    maps_dir = Path(__file__).resolve().parent.parent / "maps"
    offenders, gaps, examined = [], [], 0
    for d in sorted(p for p in maps_dir.iterdir() if p.is_dir()):
        b = d / "bindings.json"
        if not b.is_file():
            continue
        for ch in json.loads(b.read_text(encoding="utf-8")).get("chips", []):
            read = ch.get("read") or []
            if len(read) < 2 or not read[0].get("lang"):
                continue
            examined += 1
            if any(not r.get("lang") for r in read):
                offenders.append(f"{d.name}:{ch.get('chip')}")
            else:
                gaps.append(f"{d.name}:{ch.get('chip')}")
    # Task 124b item 8 — this one sits outside any room loop, so the
    # `subject()` gate never covered it: a renamed maps/ directory or an
    # unreadable bindings.json would have left `offenders` empty and the
    # door-English rule green over nothing.
    R.check("7 marks", "the door speaks English wherever an English witness exists",
            not offenders, f"{examined} multi-held chips examined; " +
            "; ".join(offenders[:3]), population=examined)
    R.check("7 marks", "chips with no English witness are a known, listed set",
            len(gaps) == 5, f"{len(gaps)}: " + "; ".join(g.split(':')[1] for g in gaps[:5]))


# Task 107 — what the eye sees, not what the box says. The union of the
# text nodes' OWN client rects is the ink on the screen; the right gap is
# measured to the longest line, so ragged-right wrapping leaves it a few
# px short of the left gap and the tolerance allows for that — but not
# for the 110px skew this replaces.
TEXT_GAPS_JS = r"""() => {
  const p = document.querySelector('.passage');
  if (!p) return null;
  const w = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
  let lo = Infinity, hi = -Infinity;
  while (w.nextNode()) {
    const t = w.currentNode;
    if (!t.nodeValue.trim()) continue;
    const rg = document.createRange(); rg.selectNodeContents(t);
    for (const r of rg.getClientRects()) {
      if (r.width < 1) continue;
      lo = Math.min(lo, r.left); hi = Math.max(hi, r.right);
    }
  }
  if (lo === Infinity) return null;
  const b = p.getBoundingClientRect();
  return { left: Math.round(lo), right: Math.round(innerWidth - hi),
           boxLeft: Math.round(b.left), boxRight: Math.round(innerWidth - b.right) };
}"""


def g_split(pg, base, R):
    """The six split bodies read exactly like whole ones.

    Head/rest exists so a 4.4 MB epic paints without downloading 4.4 MB
    first. It is allowed ONLY because nothing a reader can see differs:
    the head carries an `_index` of every passage's {id, path, fm,
    range_end}, so the consumers that reason over the whole array answer
    identically at first paint, and the rest is fetched eagerly for the
    one consumer that needs bodies. This group asserts that equivalence
    rather than the mechanism.
    """
    import gzip as _gz
    split = sorted(p for p in (REPO / "data").glob("*.rest.json.gz"))
    R.check("12 split", "the split set is the six ruled texts",
            len(split) == 6, f"{len(split)} split", population=len(split))
    # the head's window must equal the reader's render batch, or the head
    # stops being exactly one screen and the seam drifts
    m = re.search(r"const RENDER_BATCH = (\d+)", (REPO / "index.html").read_text(
        encoding="utf-8", errors="replace"))
    sys.path.insert(0, str(REPO.parent / "05_scripts"))
    import split_bodies                                     # noqa: E402
    R.check("12 split", "the head window equals the reader's RENDER_BATCH",
            bool(m) and int(m.group(1)) == split_bodies.HEAD_PASSAGES,
            f"RENDER_BATCH={m and m.group(1)} vs HEAD_PASSAGES={split_bodies.HEAD_PASSAGES}")

    for rest in split:
        stem = rest.name[:-len(split_bodies.REST_SUFFIX)]
        head = json.loads(_gz.decompress((REPO / "data" / f"{stem}.json.gz").read_bytes()))
        tail = json.loads(_gz.decompress(rest.read_bytes()))
        total = len(head.get("passages", [])) + len(tail.get("passages", []))
        # the head's own claim, the index, and the two files must agree —
        # three independent statements of one number
        R.check("12 split", f"{stem[:26]}: head+rest == the declared total",
                head.get("_split", {}).get("total") == total, f"{total}")
        R.check("12 split", f"{stem[:26]}: _index covers every passage",
                len(head.get("_index") or []) == total,
                f"{len(head.get('_index') or [])} of {total}")
        R.check("12 split", f"{stem[:26]}: _index carries what a citation reads",
                all(("id" in e and "path" in e) for e in (head.get("_index") or [])[:500]),
                "id+path on every sampled entry",
                population=min(500, len(head.get("_index") or [])))

    # and end to end: the reader reassembles one of them completely
    stem = split[0].name[:-len(split_bodies.REST_SUFFIX)]
    pg.goto(f"{base}?text={stem}.json", wait_until="networkidle")
    pg.wait_for_timeout(800)
    pg.evaluate("""() => { const b = [...document.querySelectorAll('button,a')]
        .find(x => /Read from beginning/i.test(x.textContent)); b && b.click(); }""")
    try:
        pg.wait_for_function("() => currentData && !currentData._split", timeout=30000)
        joined = pg.evaluate("() => currentData.passages.length")
    except Exception:
        joined = -1
    head = json.loads(_gz.decompress((REPO / "data" / f"{stem}.json.gz").read_bytes()))
    R.check("12 split", f"{stem[:26]}: the reader ends up with every passage",
            joined == head["_split"]["total"],
            f"{joined} of {head['_split']['total']}")


def g_shared(pg_unused, base_unused, R):
    """Task 126 — the sixteen rooms stop storing the same thing sixteen times.

    This group is the reason the shared-file lane was worth running. The
    bytes were the smaller argument; the real one was drift. Nine rooms
    diverged from seven for the length of a program because every ruling
    was applied sixteen times BY HAND — and the three archive-wide
    defects Phase C found were each present in some rooms and not others
    for exactly that reason.

    So the assertion is not "the three files exist". It is the general
    rule, derived: **if a block is byte-identical in all sixteen rooms,
    it is not sixteen blocks — it is one file, and the rooms should link
    it.** That catches the next shared block somebody pastes sixteen
    times, which is the failure this lane exists to end, rather than
    only the three that were extracted today.
    """
    import hashlib
    rooms = sorted(p for p in (REPO / "map").glob("*.html")
                   if p.name not in ("index.html", "abrahamic.html",
                                     "eastasian.html"))
    R.check("11 shared", "the sixteen rooms are on disk to compare",
            len(rooms) == 16, f"{len(rooms)} rooms", population=len(rooms))
    if len(rooms) != 16:
        return

    # every room must link the shared files, or it has a private copy
    texts = {p.name: p.read_text(encoding="utf-8", errors="replace") for p in rooms}
    # derived, not a hardcoded list: whatever map/_room*.{css,js} exists
    # must be linked by all sixteen. A new shared file is covered the day
    # it is created; a stale name in a list could never be.
    shared = sorted(p.name for p in (REPO / "map").glob("_room*")
                    if p.suffix in (".css", ".js"))
    R.check("11 shared", "there are shared room files to check",
            bool(shared), f"{len(shared)} file(s)", population=len(shared))
    for f in shared:
        missing = sorted(n for n, s in texts.items() if f not in s)
        R.check("11 shared", f"every room links {f}",
                not missing, ", ".join(missing) or "16/16",
                population=len(texts))

    # THE GENERAL RULE. A block identical in all sixteen is a file.
    #
    # ONE NAMED EXCEPTION (doctrine 7.1 — a named exception is grammar):
    # the pre-paint theme boot. It stamps data-theme on <html> before the
    # first paint, so it CANNOT be a fetched file — an external script
    # would let the page paint in the wrong theme and flash. It is
    # identified by what it does, not by a filename.
    blocks = re.compile(r"<style[\s\S]*?</style>|<script[\s\S]*?</script>")
    per_room = {}
    for n, s in texts.items():
        per_room[n] = {hashlib.sha1(b.group(0).encode()).hexdigest(): b.group(0)
                       for b in blocks.finditer(s)
                       # a <script src> is the LINK, not a copy of the thing
                       if not re.match(r"<script[^>]*\bsrc=", b.group(0))}
    common = set.intersection(*(set(v) for v in per_room.values()))
    first = next(iter(per_room.values()))
    offenders = []
    for h in sorted(common):
        b = first[h]
        prepaint = ("data-theme" in b and "setAttribute" in b
                    and len(b) < 600 and "<script>" in b)
        if not prepaint:
            offenders.append(f"{len(b)}B: {b[:52].strip()!r}")
    R.check("11 shared",
            "no block is inlined identically in all sixteen rooms",
            not offenders, "; ".join(offenders[:2]) or
            f"{len(common)} common block(s), all accounted for",
            population=len(common))


def g_layers(pg, base, R):
    """Task 126 Phase B — the single-instance layers, asserted.

    Task 120 skipped these five on the ground that a layer with one
    instance has nothing to diverge from. True of drift, false of
    grammar: a single-instance layer can still grow furniture belonging
    to another layer, and nothing can be asserted about a layer whose
    furniture was never written down. `plans/layer_grammar.md` writes it
    down; this group is the half of it that is checkable and cheap.

    Everything the walk found but no ruling covers is marked [OPEN] in
    that document and is deliberately NOT asserted here — freezing an
    undecided shape into a test is how an assertion outlives the rule it
    encoded (§8.1c).
    """
    # ── the hall: sixteen doors, each one real ────────────────────────
    pg.goto(base + "hall/", wait_until="networkidle")
    doors = pg.evaluate("""() => [...document.querySelectorAll('a[href*="map/"]')]
        .filter(a => a.getClientRects().length)
        .map(a => (a.getAttribute('href') || '').split('/').pop())""")
    R.check("10 layers", "the hall holds exactly 16 tradition doors",
            len(doors) == 16, f"{len(doors)} doors", population=len(doors))
    missing = [d for d in doors if not (REPO / "map" / d).exists()]
    R.check("10 layers", "every hall door has a page behind it",
            not missing, ", ".join(missing) or f"{len(doors)} verified",
            population=len(doors))

    # ── the entrance: the trio, and where it goes ─────────────────────
    pg.goto(base, wait_until="networkidle")
    pg.wait_for_timeout(600)
    ent = pg.evaluate("""() => {
      const on = s => [...document.querySelectorAll(s)]
                        .filter(e => e.getClientRects().length).length;
      const hrefs = [...document.querySelectorAll('a[href]')]
        .filter(a => a.getClientRects().length)
        .map(a => a.getAttribute('href') || '');
      return { back: on('#home-hub-link'), star: on('#fav-shelf-btn'),
               theme: on('#dark-toggle'),
               hall: hrefs.filter(h => /(^|\\/)hall\\/?$/.test(h)).length,
               shelves: new Set(hrefs.filter(h => /shelf\\//.test(h))).size,
               rooms: hrefs.filter(h => /map\\/[a-z]+\\.html/.test(h)).length }; }""")
    for name, key in (("back arrow", "back"), ("star", "star"),
                      ("theme button", "theme")):
        R.check("10 layers", f"the entrance carries the permanent {name}",
                ent[key] >= 1, f"{ent[key]}")
    R.check("10 layers", "the entrance routes to the hall",
            ent["hall"] >= 1, f"{ent['hall']} link(s)")
    R.check("10 layers", "the entrance routes to three shelves",
            ent["shelves"] == 3, f"{ent['shelves']} shelf routes")
    # the entrance never shortcuts a tradition — the hall owns those doors
    R.check("10 layers", "the entrance carries no tradition door",
            ent["rooms"] == 0, f"{ent['rooms']} map link(s)")

    # ── the shelves: three instances, one form ────────────────────────
    shapes = []
    for name in ("philosophy", "literature", "esoteric"):
        pg.goto(f"{base}shelf/{name}.html", wait_until="networkidle")
        shapes.append(pg.evaluate("""() => {
          const on = s => [...document.querySelectorAll(s)]
                            .filter(e => e.getClientRects().length).length;
          return { back: on('.tb-arrow') > 0, star: on('#arch-fav') > 0,
                   theme: on('#arch-dark') > 0, h1: on('h1') === 1,
                   trads: on('.trad') > 0, rows: on('.rows a.t') > 0 }; }"""))
    R.check("10 layers", "all three shelves carry the same furniture",
            len({json.dumps(s, sort_keys=True) for s in shapes}) == 1,
            "; ".join(str(s) for s in shapes[:1]), population=len(shapes))

    # ── the reading room: the border holds ────────────────────────────
    pg.goto(f"{base}?text={CODEX}", wait_until="networkidle")
    pg.wait_for_timeout(900)
    pg.evaluate("""() => { const b = [...document.querySelectorAll('button,a')]
        .find(x => /Read from beginning/i.test(x.textContent)); b && b.click(); }""")
    pg.wait_for_timeout(1400)
    rr = pg.evaluate("""() => {
      const on = s => [...document.querySelectorAll(s)]
                        .filter(e => e.getClientRects().length).length;
      return { inReading: document.body.classList.contains('in-reading'),
               theme: document.documentElement.getAttribute('data-theme'),
               archiveTheme: on('#arch-dark, #themeBtn, #dark-toggle'),
               archiveStar: on('#arch-fav, #favBtn, #fav-shelf-btn'),
               own: on('#rr-fav') + on('#ctrl-contents') }; }""")
    R.check("10 layers", "the walk actually entered the text",
            rr["inReading"], "body.in-reading")
    # the subject gate (§8.1c): the absences below mean nothing unless the
    # room rendered its OWN furniture, so prove that first.
    R.check("10 layers", "the reading room rendered its own furniture",
            rr["own"] >= 2, f"{rr['own']} of its own controls",
            population=rr["own"])
    R.check("10 layers",
            "the archive theme key stops at the reading room's door",
            rr["theme"] is None, f"data-theme={rr['theme']!r}")
    R.check("10 layers", "the reading room carries no archive theme button",
            rr["archiveTheme"] == 0, f"{rr['archiveTheme']} found")
    R.check("10 layers", "the reading room carries no archive star",
            rr["archiveStar"] == 0, f"{rr['archiveStar']} found")


def g_centring(pg, base, R):
    """Task 126-R — the reading column is centred AT EVERY WIDTH.

    Task 107 item 2 ruled "the column must be centred, actually centred"
    and did not scope that to phones. The assertion was nonetheless
    written inside the mobile group and nowhere else, so for twenty lanes
    it proved the phone and said nothing about the desktop — where the
    column sat 103-109px right of centre in every cover shape, because
    `.passage` carried a 110px reference gutter on one side and a
    counterweight on neither.

    An assertion that lives in ONE group only is why that survived. This
    group is the fix for the fix: it walks the same rule across the
    widths the archive is actually read at, and it measures the rendered
    INK (§8.1) rather than the container, which was centred all along and
    would have reported green.

    Tolerance is 12px because the right edge is ragged: the rightmost ink
    is the longest line's end, not the column's edge, so texts differ by a
    few px. The LEFT edge is deterministic and is asserted tightly.

    §8.1 again, on the subject rather than the property: this group does
    NOT reuse TEXT_GAPS_JS, which reads `querySelector('.passage')` — the
    FIRST passage, which in most texts is a chapter heading. A heading is
    centred, short, and has its `.ref` suppressed, so its gaps describe a
    different box than the body column the ruling is about. Measuring it
    reported 409/447 for a column that is actually 445/446.
    """
    COLUMN_INK_JS = r"""() => {
      const ps = [...document.querySelectorAll('.passage')].filter(p =>
        p.getAttribute('data-role') !== 'heading'
        && (p.textContent || '').trim().length > 80
        && getComputedStyle(p).display !== 'none');
      if (!ps.length) return null;
      let lo = Infinity, hi = -Infinity;
      for (const p of ps.slice(0, 10)) {
        for (const n of p.childNodes) {
          if (n.nodeType !== 3 || !n.nodeValue.trim()) continue;
          const rg = document.createRange(); rg.selectNodeContents(n);
          for (const r of rg.getClientRects()) {
            if (r.width < 2) continue;
            lo = Math.min(lo, r.left); hi = Math.max(hi, r.right);
          }
        }
      }
      if (lo === Infinity) return null;
      return { left: Math.round(lo), right: Math.round(innerWidth - hi),
               seen: ps.length };
    }"""
    WIDTHS = [(1440, 900), (1024, 800), (768, 900)]
    TEXTS = [("codex", CODEX), ("bible-80", BIBLE_80), ("flat", FLAT)]
    ctx = _BROWSER[0].new_context(viewport={"width": 1440, "height": 900})
    p2 = ctx.new_page()
    try:
        for w, h in WIDTHS:
            p2.set_viewport_size({"width": w, "height": h})
            lefts = []
            for label, df in TEXTS:
                p2.goto(f"{base}?text={df}", wait_until="networkidle")
                p2.wait_for_timeout(700)
                p2.evaluate("""() => { const b = [...document.querySelectorAll('button,a')]
                    .find(x => /Read from beginning/i.test(x.textContent)); b && b.click(); }""")
                p2.wait_for_timeout(900)
                g = p2.evaluate(COLUMN_INK_JS)
                R.check("9 centring", f"{w}px, {label}: the ink is centred",
                        g is not None and abs(g["left"] - g["right"]) <= 12,
                        f"{g and g['left']}px left / {g and g['right']}px right",
                        population=(g or {}).get("seen", 0))
                if g:
                    lefts.append(g["left"])
            # the left edge is deterministic, so every text must share it:
            # a per-text left gap means the gutter, not the ragged margin.
            R.check("9 centring", f"{w}px: every text shares one left edge",
                    len(set(lefts)) == 1 if lefts else False,
                    f"{sorted(set(lefts))}", population=len(lefts))
    finally:
        ctx.close()


def g_mobile(pg_unused, base, R):
    """Task 106-P2 phase 3 — the phone. This group exists because the
    battery only ever ran at 1440px, and a whole viewport class hid a
    defect for twenty lanes: at phone widths the reading room had no
    formatting apparatus at all."""
    LAYERS = [("entrance", ""), ("hall", "hall/"),
              ("map", "map/christianity.html"), ("shelf", "shelf/philosophy.html"),
              ("philosophy", "philosophy.html"),
              ("cover", "?text=bible_kjv.json")]
    # Task 122 — the count of targets EXAMINED rides back with the
    # offenders: "no target under 44px" and "no targets at all" are the
    # same report otherwise, and the second is a page that failed to load.
    # Task 126-R / doctrine §8.1d — THE NAME MUST NOT ASSERT MORE THAN THE
    # PREDICATE TESTS. Two defects lived in the four lines below, and both
    # were invisible because the label read correctly:
    #
    #   `if (r.height < 44 || r.width < 24)`  — the ruled floor is 44x44
    #   (Task 106-P2 item 4). Width was enforced at 24, so a 30x44 star on
    #   every cover shape and a 24x44 shelf link passed a check named
    #   "every visible target >= 44px".
    #
    #   `if (r.bottom < 0 || r.top > innerHeight) return;` — a name saying
    #   EVERY over a predicate that examines only the first screen. The
    #   entrance's three 11px footer controls were never measured at all.
    #
    # Task 122's vacuity audit read this exact line, fixed its vacuity with
    # subject(), and saw neither. 8.1b asks whether the check looked; this
    # asks whether it looked for what it claimed.
    TAP_JS = """() => {
      const vw = innerWidth, small = []; let seen = 0, offscreen = 0;
      document.querySelectorAll('a, button, select, summary, [role=button], [role=link]')
        .forEach(e => { const r = e.getBoundingClientRect();
          if (!r.width || !r.height) return;
          if (getComputedStyle(e).position === 'fixed' && r.width < 2) return;
          // a control below the fold is still a control the reader taps
          if (r.bottom < 0 || r.top > innerHeight) offscreen++;
          seen++;
          if (r.height < 44 || r.width < 44)
            small.push((e.id ? '#'+e.id : e.tagName + '.' + String(e.className).slice(0,20))
                       + ' ' + Math.round(r.width) + 'x' + Math.round(r.height)); });
      return { seen: seen, offscreen: offscreen,
               overflow: Math.round(document.documentElement.scrollWidth - vw),
               small: [...new Set(small)].slice(0, 6) }; }"""
    # the phone gets its own context on the SAME browser: a nested
    # sync_playwright() inside the running one raises.
    ctx = _BROWSER[0].new_context(viewport={"width": 390, "height": 844},
                                  is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    try:
        for name, path in LAYERS:
            pg.goto(base + path, wait_until="networkidle")
            pg.wait_for_timeout(1100)
            m = pg.evaluate(TAP_JS)
            R.check("8 mobile", f"{name}: no horizontal overflow at 390px",
                    m["overflow"] <= 2, f"+{m['overflow']}px")
            R.check("8 mobile", f"{name}: found targets to measure",
                    m["seen"] > 0, f"{m['seen']} tap targets")
            R.check("8 mobile", f"{name}: every visible target ≥ 44px",
                    m["seen"] > 0 and not m["small"], "; ".join(m["small"][:3]))
        # the reading room and its sheet
        pg.goto(base + "?text=thus-spake-zarathustra_common.json", wait_until="networkidle")
        pg.wait_for_timeout(1200)
        pg.evaluate("""() => { const b = [...document.querySelectorAll('button')]
          .find(x => /Read from beginning/.test(x.textContent)); b && b.click(); }""")
        pg.wait_for_timeout(1200)
        m = pg.evaluate(TAP_JS)
        R.check("8 mobile", "reading: no horizontal overflow", m["overflow"] <= 2, f"+{m['overflow']}px")
        R.check("8 mobile", "reading: found targets to measure",
                m["seen"] > 0, f"{m['seen']} tap targets")
        R.check("8 mobile", "reading: every visible target ≥ 44px",
                m["seen"] > 0 and not m["small"], "; ".join(m["small"][:3]))
        # Task 107 — measure the RENDERED TEXT, not the wrapper. The old
        # assertion read .passage's own box, which was symmetric at 16/16
        # while the text inside it began 126px from a 390px screen's left
        # edge: the box reserved a 110px gutter for a numeral that, at
        # phone widths, no longer sits in it. A check that measures the
        # container it was handed can only ever prove the container.
        col = pg.evaluate(TEXT_GAPS_JS)
        R.check("8 mobile", "reading: the rendered text is centred",
                col and abs(col["left"] - col["right"]) <= 12,
                f"text {col['left']}px / {col['right']}px (box "
                f"{col['boxLeft']}px / {col['boxRight']}px)" if col else "no text")
        has = pg.evaluate("() => !!document.getElementById('nav-fmt-toggle')")
        R.check("8 mobile", "reading: the sheet has a handle in the running header", has)
        if has:
            pg.click("#nav-fmt-toggle"); pg.wait_for_timeout(500)
            s = pg.evaluate("""() => {
              const sh = document.getElementById('fmt-sheet');
              const p = document.getElementById('fmt-sheet-panel');
              if (!sh || sh.hidden) return null;
              const r = p.getBoundingClientRect();
              const inside = id => { const e = document.getElementById(id);
                return !!(e && p.contains(e) && e.getClientRects().length); };
              const rows = [...p.querySelectorAll('.ctrl-group, #fmt-sheet-doors > *')]
                .filter(e => e.getClientRects().length)
                .map(e => Math.round(e.getBoundingClientRect().height));
              // §8.1d — the reader taps the CONTROL, not the row that
              // contains it. "every sheet row >= 44px" measured the row and
              // passed while .theme-swatch was 34x34 and .face-btn 40 tall.
              const tapped = [...p.querySelectorAll(
                  'button, input, select, a, summary, [role=button]')]
                .filter(e => e.getClientRects().length)
                .map(e => { const b = e.getBoundingClientRect();
                  return { w: Math.round(b.width), h: Math.round(b.height),
                           id: (e.className ? '.' + String(e.className).slice(0,20)
                                            : e.tagName) }; });
              const smallCtrl = tapped.filter(t => t.h < 44 || t.w < 44)
                .map(t => t.id + ' ' + t.w + 'x' + t.h);
              return { within: r.top >= 0 && r.bottom <= innerHeight + 1,
                       ctrlSeen: tapped.length,
                       smallCtrl: [...new Set(smallCtrl)].slice(0, 6),
                       themes: inside('ctrl-themes'), faces: inside('ctrl-faces'),
                       size: inside('ctrl-size'), spacing: inside('ctrl-spacing'),
                       measure: inside('ctrl-measure'), fav: inside('rr-fav'),
                       press: inside('press-print'), atlas: inside('rr-atlas'),
                       folio: inside('companion-toggle'),
                       minRow: rows.length ? Math.min(...rows) : 0 }; }""")
            R.check("8 mobile", "the sheet opens fully within the viewport",
                    bool(s) and s["within"], str(s and s["within"]))
            for k in ("themes", "faces", "size", "spacing", "measure"):
                R.check("8 mobile", f"the sheet holds {k} and it is reachable",
                        bool(s) and s[k])
            for k in ("fav", "press", "atlas"):
                R.check("8 mobile", f"the sheet holds the {k} door", bool(s) and s[k])
            R.check("8 mobile", "Folio does NOT come to the phone (ruled)",
                    bool(s) and not s["folio"])
            R.check("8 mobile", "every sheet row ≥ 44px",
                    bool(s) and s["minRow"] >= 44, f"min {s and s['minRow']}px")
            # §8.1d — and every control INSIDE those rows, which is what the
            # reader's thumb actually lands on.
            R.check("8 mobile", "every sheet control ≥ 44px",
                    bool(s) and not s["smallCtrl"],
                    "; ".join(s["smallCtrl"][:3]) if s and s["smallCtrl"]
                    else f"{s and s['ctrlSeen']} controls",
                    population=(s or {}).get("ctrlSeen", 0))
            # it actually formats
            pg.click('#fmt-sheet .theme-swatch[data-theme-key="ink"]'); pg.wait_for_timeout(400)
            R.check("8 mobile", "a preset chosen in the sheet reaches the page",
                    pg.evaluate("() => document.body.classList.contains('rt-ink')"))
            # Task 107 — and Measure is not inert. Its 660–1320px band is
            # wider than any phone, so on the desktop reading the column
            # could not answer it at all; at phone widths the same key
            # drives the side margins. An inert control is worse than no
            # control, so the battery proves it MOVES, both ways.
            pg.evaluate("""() => { const s = document.getElementById('ctrl-measure');
              s.value = s.min; s.dispatchEvent(new Event('input', {bubbles:true})); }""")
            pg.wait_for_timeout(350)
            lo = pg.evaluate(TEXT_GAPS_JS)
            pg.evaluate("""() => { const s = document.getElementById('ctrl-measure');
              s.value = s.max; s.dispatchEvent(new Event('input', {bubbles:true})); }""")
            pg.wait_for_timeout(350)
            hi = pg.evaluate(TEXT_GAPS_JS)
            R.check("8 mobile", "Measure moves the column on a phone",
                    lo and hi and abs(hi["left"] - lo["left"]) >= 20,
                    f"{lo and lo['left']}px → {hi and hi['left']}px")
            R.check("8 mobile", "Measure's wide end runs the text to the edge",
                    lo and lo["left"] <= 16, f"{lo and lo['left']}px")
            for nm, g in (("narrow", hi), ("wide", lo)):
                R.check("8 mobile", f"the column stays centred at Measure's {nm} end",
                        g and abs(g["left"] - g["right"]) <= 12,
                        f"{g and g['left']}px / {g and g['right']}px")
            pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
            R.check("8 mobile", "ESC dismisses the sheet",
                    pg.evaluate("() => document.getElementById('fmt-sheet').hidden"))
        # Task 107 — 360 is the other phone the steward walks. The 390
        # checks above would pass a rule written in px that breaks at a
        # narrower screen, so the centring is re-proved here.
        pg.set_viewport_size({"width": 360, "height": 740})
        pg.wait_for_timeout(500)
        g = pg.evaluate(TEXT_GAPS_JS)
        R.check("8 mobile", "reading: the text is centred at 360 too",
                g and abs(g["left"] - g["right"]) <= 12,
                f"{g and g['left']}px / {g and g['right']}px")
    finally:
        ctx.close()


def g_grammar(pg, base, R):
    """Task 120 item 1 — the room grammar, asserted.

    `plans/room_grammar.md` names the ONE ruled form of every element
    class and the exceptions that are content rather than drift. This
    group is the half that can be checked: the universal classes must be
    present in all sixteen rooms, and the NAMED exceptions must hold
    exactly where they are named — a room may not quietly join or leave
    one. Anything else is drift and fails here rather than waiting for a
    steward to walk the room.
    """
    rooms = ["ancient", "bahai", "buddhist", "christianity", "confucian",
             "daoist", "gnostic", "hindu", "indigenous", "islam", "jain",
             "judaism", "modern", "shinto", "sikh", "zoroastrian"]
    # §1 — universal, keyed by a selector that finds the thing itself
    UNIVERSAL = {
        "masthead": "header.mast",
        "lede": "header.mast p",
        "legend": "#m-legend",
        "section heading": "section[id] h2, .zone-h, .basket > h2",
        "collapse control": ".toc-all",
        # NOTE — "interpretive line" WAS universal here, selected as
        # `.greenline, .insight, .gl`. Task 123 item 3 retired the
        # narrative line ("213 green of 221 — the entire Bible…"), and in
        # five rooms that line was the ONLY thing the selector matched, so
        # a universal requirement now demands the thing the ruling
        # removed. It is no longer universal; the surviving `.insight`
        # blocks are asserted below on content instead. Task 126 §1.4.
        # Task 128 item 3 — THE FOOTER RETIRED, archive-wide, so the
        # assertion that named it moves with it in the same lane
        # (§8.1e). Asserting its presence now demands the thing the
        # ruling removed — the same failure the statband assertion
        # made in Task 126, in the same file, one lane apart.
        # Its absence is asserted below instead.

        "theme button": "#arch-dark",
        "star button": "#arch-fav",
        "back arrow": "#arch-topbar .tb-arrow",
    }
    # §2 — the named exceptions, and the ONLY rooms they may appear in
    STAT_STRUCTURAL = {"buddhist"}          # §2.4
    NO_STATBAND = {"hindu"}                 # §2.3
    SECOND_CHIP_GRAMMAR = {"buddhist", "hindu"}   # §2.1
    for room in rooms:
        pg.goto(f"{base}map/{room}.html", wait_until="networkidle")
        pg.wait_for_timeout(600)
        if not subject(pg, R, "9 grammar", room, "header.mast, section[id]", 2):
            continue
        m = pg.evaluate("""(sels) => {
          const out = {};
          for (const k in sels) out[k] = document.querySelectorAll(sels[k]).length;
          const band = document.querySelector('.statband');
          out.__band = band ? [...band.querySelectorAll('.stat span')]
            .map(s => (s.textContent || '').trim().toLowerCase()) : null;
          // the surviving interpretive line, if the room has one
          const ins = document.querySelector('.greenline, .insight, .gl');
          out.__insight = ins && ins.getClientRects().length
            ? (ins.textContent || '').replace(/\s+/g, ' ').trim() : null;
          out.__footer = document.querySelectorAll('footer').length;
          out.__famr = [...document.querySelectorAll('.famr')]
            .map(e => (e.textContent || '').replace(/\s+/g, ' ').trim());
          out.__second = document.querySelectorAll('.chip .nm').length;
          out.__fambar = document.querySelectorAll('.fambar').length;
          out.__lens = document.querySelectorAll('#lens-toggle, #lens-banner').length;
          return out; }""", UNIVERSAL)
        for name, _sel in UNIVERSAL.items():
            R.check("9 grammar", f"{room}: has {name}", m[name] >= 1, f"{m[name]}")
        # Task 126 §1.4 — THE GATE IS THE CONTENT, NOT A ROOM LIST.
        #
        # This used to assert the statband is PRESENT in every room except
        # a named list. Task 123 item 3 then retired it archive-wide, with
        # one gate: "if a band states a structural fact rather than a
        # rights aggregate, keep it." The assertion was never moved, so
        # after the retirement it failed in fifteen rooms for doing
        # exactly what was ruled — an assertion measuring the old world in
        # the new one (§8.1c).
        #
        # Restated as the ruling actually reads, and derived: a band may
        # exist ONLY if its own labels are not the rights aggregate. No
        # room list, so a room that grows or loses a band needs no edit
        # here — and a rights band reappearing anywhere fails, which is
        # the thing worth catching.
        has_band = m["__band"] is not None
        if has_band:
            labels = set(m["__band"])
            rights_aggregate = bool({"green", "amber", "red"} & labels) or \
                {"held", "pd", "no pd"} <= labels
            R.check("9 grammar", f"{room}: any surviving band is structural",
                    not rights_aggregate, " · ".join(m["__band"])[:58])
        R.check("9 grammar", f"{room}: no footer returns",
                m["__footer"] == 0, f"{m['__footer']} footer(s)")
        # Task 126 §1.4 — the interpretive line is optional now, but where
        # a room keeps one it must not be the retired narrative line. The
        # shape Task 123 named is "N of M green" / "N green of M"; derived
        # from the text so it catches the sentence under any class.
        if m["__insight"]:
            R.check("9 grammar", f"{room}: the interpretive line is not a rights tally",
                    not re.search(r"\b\d[\d,]*\s+(of\s+\d[\d,]*\s+)?green\b",
                                  m["__insight"][:160], re.I),
                    m["__insight"][:56])
        # Task 126 — NO EDITION CREDIT ON A FAMILY HEADER.
        #
        # Task 111 item 6 took edition info off every chip ("SBE 13/17
        # (PD) · Brahmali CC0" and its kin) because the contents page owns
        # it; Task 102b then ruled that where a retired line carried
        # MEANING it moves to the family header, but "only plain edition
        # credits are dropped outright." Four survived on family headers
        # anyway — christianity's "M.R. James 1924" and "R.H. Charles
        # 1913", zoroastrian's two "Darmesteter, SBE …" lines.
        #
        # Derived on the SHAPE the rulings describe — a short line ending
        # in a publication year — so it cannot be dodged by a new
        # translator's name, and so it does not catch the lines that
        # legitimately live here: a canon gloss ("Catholic & Orthodox"), a
        # date span ("c. 90–160"), a volume location ("NPNF 1, vols 1–8"),
        # a containment ("within Yasna 28–53"), or the archive's own note
        # ("a demonstrated 19th-c. hoax (Rafinesque 1836) — not a genuine
        # Lenape text"), which mentions a year but is prose and is MEANING.
        # First draft of this rule flagged buddhist's "T1421–1504" — a
        # Taishō catalogue range whose second number reads as a year. A
        # credit names a PERSON and ends in a publication year; a
        # catalogue line is a RANGE. So a numeric range disqualifies,
        # which is the property that actually separates them.
        credits = [c for c in m["__famr"]
                   if len(c) <= 34
                   and re.search(r"\b1[5-9]\d\d\s*$|\b20\d\d\s*$", c)
                   and not re.search(r"\d\s*[–—-]\s*\d", c)]
        R.check("9 grammar", f"{room}: no family header carries an edition credit",
                not credits, "; ".join(credits[:3]) or f"{len(m['__famr'])} lines")
        # the second chip grammar lives in exactly two rooms
        R.check("9 grammar", f"{room}: chip grammar is the one named for it",
                (m["__second"] > 0) == (room in SECOND_CHIP_GRAMMAR),
                f"{m['__second']} .chip .nm")
        # retired archive-wide — absence, not invisibility
        R.check("9 grammar", f"{room}: no retired furniture returns",
                m["__fambar"] == 0 and m["__lens"] == 0,
                f"fambar={m['__fambar']} lens={m['__lens']}")


GROUPS = {
    "furniture": g_furniture,
    "marks": g_lens,
    "grammar": g_grammar,
    "split": g_split,
    "shared": g_shared,
    "layers": g_layers,
    "centring": g_centring,
    "mobile": g_mobile,
    "boundary": g_boundary,
    "chrome": g_room_chrome,
    "contrast": g_contrast,
    "covers": g_covers,
    "rooms": g_rooms,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=sorted(GROUPS), action="append")
    ap.add_argument("--shots", action="store_true", help="write frames for review")
    a = ap.parse_args()
    port = free_port()
    serve(port)
    base = f"http://127.0.0.1:{port}/"
    chosen = a.only or list(GROUPS)
    R = Result()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        _BROWSER[0] = b
        ctx = b.new_context(viewport={"width": 1440, "height": 1000})
        pg = ctx.new_page()
        for name in chosen:
            try:
                GROUPS[name](pg, base, R)
            except Exception as e:  # a group that cannot run IS a failure
                R.check(name, "group ran to completion", False, f"{type(e).__name__}: {e}"[:160])
            if a.shots:
                SHOTS.mkdir(parents=True, exist_ok=True)
                pg.screenshot(path=str(SHOTS / f"{name}.png"))
        b.close()
    return R.report()


if __name__ == "__main__":
    sys.exit(main())
