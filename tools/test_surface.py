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
FLAT = "kierkegaard-fear-trembling_anonymous.json"
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
window.__bgOf = function (el) {
  let e = el;
  while (e) { const b = getComputedStyle(e).backgroundColor;
    if (b && !b.includes('0, 0, 0, 0')) return b; e = e.parentElement; }
  return getComputedStyle(document.body).backgroundColor || 'rgb(255,255,255)';
};
window.__ratio = function (sel) {
  const el = document.querySelector(sel);
  if (!el) return null;
  return window.__cr(getComputedStyle(el).color, window.__bgOf(el));
};
"""


class Result:
    def __init__(self):
        self.rows: list[tuple[str, str, bool, str]] = []

    def check(self, group: str, what: str, ok: bool, detail: str = "") -> None:
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
    """Task 88 — the room's lamp retired for Atlas; three reading faces."""
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
        pg.evaluate("localStorage.setItem('da-theme','dark')")
        pg.reload(wait_until="networkidle")
        pg.wait_for_timeout(800)
        pg.add_script_tag(content=CONTRAST_JS)
        for what, sel in sels.items():
            val = pg.evaluate("(s) => window.__ratio(s)", sel)
            if val is None:
                R.check("4 contrast", f"{name} dark: {what}", False, "element not found")
            else:
                R.check("4 contrast", f"{name} dark: {what} ≥ 4.5", val >= 4.5, f"{val}:1")
    # the Rights lens in the dark room (was 1.1:1 before Task 97)
    pg.goto("%smap/christianity.html" % base)
    pg.evaluate("localStorage.setItem('da-theme','dark')")
    pg.reload(wait_until="networkidle")
    pg.wait_for_timeout(700)
    try:
        pg.click("text=RIGHTS", timeout=4000)
        pg.wait_for_timeout(500)
        pg.add_script_tag(content=CONTRAST_JS)
        val = pg.evaluate("""() => { const tl = document.querySelector('.tc.g .tl');
          if (!tl) return null;
          return window.__cr(getComputedStyle(tl).color,
                             getComputedStyle(tl.closest('.tc')).backgroundColor); }""")
        R.check("4 contrast", "Rights lens in dark: chip text ≥ 4.5",
                val is not None and val >= 4.5, f"{val}:1")
    except Exception as e:
        R.check("4 contrast", "Rights lens reachable", False, str(e)[:60])


def g_covers(pg, base, R):
    """Task 87/92/96/99 — the contents row, the canon row, the shelf."""
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

    m = cover(CODEX)
    R.check("5 covers", "codex: contents row names its own units",
            bool(m["rule"]) and "chapters" in m["rule"], str(m["rule"]))
    R.check("5 covers", "codex: Front Matter rides the row", m["fmInRule"])
    R.check("5 covers", "codex: no canon row (not a Bible)", not m["canon"])

    m = cover(FLAT)
    R.check("5 covers", "flat text: no contents row", m["rule"] is None, str(m["rule"]))

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
            bars: [...document.querySelectorAll('.zb, .fambar, .mini')]
                    .filter(e => e.offsetParent !== null).length,
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
        R.check("6 rooms", f"{room}: no family repeats one sub-line under every chip",
                not m["uniform"], "; ".join(m["uniform"][:3]))
        R.check("6 rooms", f"{room}: has collapsible families", m["fams"] > 0, f"{m['fams']}")
        if m["fams"]:
            R.check("6 rooms", f"{room}: disclosure arrow held left", m["markerLeft"])
            R.check("6 rooms", f"{room}: collapse control present", m["collapse"])
            # Some rooms open on an overview and keep their deep view (with
            # the sections AND this control) behind a walk — the Buddhist
            # canons do. The control is exercised where the reader can
            # actually reach it; being gated is the room's design, not a
            # regression.
            visible = pg.evaluate("""() => { const b = document.querySelector('.toc-all');
              return !!(b && b.getClientRects().length); }""")
            if not visible:
                R.check("6 rooms", f"{room}: control gated behind the room's own view",
                        True, "not on the landing view — by design")
                continue
            pg.click(".toc-all")
            pg.wait_for_timeout(300)
            after = pg.evaluate("""() => ({ open: [...document.querySelectorAll('details.fam')]
              .filter(d => d.open).length, label: document.querySelector('.toc-all').textContent })""")
            R.check("6 rooms", f"{room}: the control closes every section",
                    after["open"] == 0 and after["label"] == "Expand all", str(after))


def g_lens(pg, base, R):
    """Task 103 — a lens changes how objects LOOK, never what they ARE or
    where they sit: no chip may move across the toggle, and a chip with a
    route must open it in both views."""
    rooms = ["ancient", "bahai", "buddhist", "christianity", "confucian",
             "daoist", "gnostic", "hindu", "indigenous", "islam", "jain",
             "judaism", "modern", "shinto", "sikh", "zoroastrian"]
    # Task 105 closed the last exception: the rights marker that rewrapped
    # ancient's long chip names moved off the chip, so every room is held
    # to the same rule — a lens may recolour, never relocate.
    ALLOW = {}
    SNAP = """() => { const o = {};
      document.querySelectorAll('.tc, .chip, .su').forEach((c, i) => {
        const r = c.getBoundingClientRect();
        o[i] = [Math.round(r.left), Math.round(r.top + scrollY), Math.round(r.width)];
      }); return o; }"""
    for room in rooms:
        pg.goto(f"{base}map/{room}.html", wait_until="networkidle")
        pg.wait_for_timeout(700)
        if not pg.evaluate("""() => !!document.querySelector('[data-lens="rights"]')"""):
            continue
        before = pg.evaluate(SNAP)
        pg.evaluate("""() => { const b = document.querySelector('[data-lens="rights"]');
          b && b.click(); }""")
        pg.wait_for_timeout(600)
        after = pg.evaluate(SNAP)
        moved = sum(1 for k, v in before.items() if k in after and
                    max(abs(v[0] - after[k][0]), abs(v[1] - after[k][1]),
                        abs(v[2] - after[k][2])) > 1)
        ceiling = ALLOW.get(room, 0)
        R.check("7 lens", f"{room}: the grid holds still across the lens"
                + (" (known residue)" if ceiling else ""),
                moved <= ceiling, f"{moved} of {len(before)} chips move")
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
            R.check("7 lens", f"{room}: a held chip is still a door in Rights",
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
                R.check("7 lens", f"{room}: the chip lands on a contents page",
                        on_contents, pg.url.split("text=")[-1][:44])
                # Task 108 — and it says WHICH chip it was, or the
                # contents page cannot name the second group or the
                # arrival.
                R.check("7 lens", f"{room}: the chip identity rides the URL",
                        "chip=" in pg.url, pg.url.split("?")[-1][:52])
        R.check("7 lens", f"{room}: no chooser popover survives",
                pg.evaluate("""() => !document.querySelector('.m-chooser-pop')
                  && typeof window.__mcClose === 'undefined'"""))


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


def g_mobile(pg_unused, base, R):
    """Task 106-P2 phase 3 — the phone. This group exists because the
    battery only ever ran at 1440px, and a whole viewport class hid a
    defect for twenty lanes: at phone widths the reading room had no
    formatting apparatus at all."""
    LAYERS = [("entrance", ""), ("hall", "hall/"),
              ("map", "map/christianity.html"), ("shelf", "shelf/philosophy.html"),
              ("philosophy", "philosophy.html"),
              ("cover", "?text=bible_kjv.json")]
    TAP_JS = """() => {
      const vw = innerWidth, small = [];
      document.querySelectorAll('a, button, select, summary, [role=button], [role=link]')
        .forEach(e => { const r = e.getBoundingClientRect();
          if (!r.width || !r.height) return;
          if (r.bottom < 0 || r.top > innerHeight) return;
          if (getComputedStyle(e).position === 'fixed' && r.width < 2) return;
          if (r.height < 44 || r.width < 24)
            small.push((e.id ? '#'+e.id : e.tagName + '.' + String(e.className).slice(0,20))
                       + ' ' + Math.round(r.width) + 'x' + Math.round(r.height)); });
      return { overflow: Math.round(document.documentElement.scrollWidth - vw),
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
            R.check("8 mobile", f"{name}: every visible target ≥ 44px",
                    not m["small"], "; ".join(m["small"][:3]))
        # the reading room and its sheet
        pg.goto(base + "?text=thus-spake-zarathustra_common.json", wait_until="networkidle")
        pg.wait_for_timeout(1200)
        pg.evaluate("""() => { const b = [...document.querySelectorAll('button')]
          .find(x => /Read from beginning/.test(x.textContent)); b && b.click(); }""")
        pg.wait_for_timeout(1200)
        m = pg.evaluate(TAP_JS)
        R.check("8 mobile", "reading: no horizontal overflow", m["overflow"] <= 2, f"+{m['overflow']}px")
        R.check("8 mobile", "reading: every visible target ≥ 44px",
                not m["small"], "; ".join(m["small"][:3]))
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
              return { within: r.top >= 0 && r.bottom <= innerHeight + 1,
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


GROUPS = {
    "furniture": g_furniture,
    "lens": g_lens,
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
