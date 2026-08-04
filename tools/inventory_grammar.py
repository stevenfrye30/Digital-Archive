# -*- coding: utf-8 -*-
"""Task 118 phase 1 — the room grammar, tabulated. SURVEY ONLY.

Every lane since 94 has had one shape: the steward walks a room, finds
it differs, and the difference gets fixed archive-wide. This asks the
question once for every element class at once.

SWEPT BY CONTENT. Each element class is located by what it DOES in the
page, and every class in every room is enumerated first, so a room that
spells something differently shows up as an outlier instead of
vanishing (the Task 114 failure: a survey that searched one class name
and read its absence as absence of the thing).

Reports presence, count and the rendered form. Changes nothing.
"""
from __future__ import print_function

import collections
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MAP = os.path.join(REPO, "map")

# Task 148 item 2 — THE ROOM SET IS DERIVED FROM WHAT A FILE IS.
#
# This used to read `"Task 111 " in <page text>`: a room was any page
# still carrying a comment from a 2026-07 lane. That is not a property of
# a room, it is a property of an editorial note, and lanes kept deleting
# them. By HEAD before this fix exactly ONE page still matched — and
# Task 146 removed the comment carrying it, taking the population to
# ZERO — while this file went on printing "OUTLIERS — element classes NOT
# universal across the 16 rooms" and writing room_grammar_inventory.json.
# The banner said sixteen; the sample was one, then none.
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
    raise SystemExit("inventory_grammar: the room set is EMPTY — refusing to "
                     "report on nothing. Check map/*.html.")

# element class -> the markup that realises it. Several alternatives per
# row on purpose: the point is to catch a room that uses a different one.
ELEMENTS = [
    ("masthead",        [r'<div class="mast"', r'<header[^>]*class="[^"]*mast']),
    # the lede wears NO class — it is a bare <p> inside the masthead. The
    # first pass here searched for class="lede" and reported 0/16, i.e.
    # "no room has a lede", which is false in all 16. Exactly the Task 114
    # failure reproduced inside the survey meant to prevent it: an absent
    # CLASS NAME is not an absent THING.
    ("lede",            [r'<header class="mast">(?:(?!</header>).)*?<p>']),
    ("stat line",       [r'<div class="stat"']),
    ("lens toggle",     [r'id="lensToggle"', r'class="lens-toggle"', r'data-lens']),
    ("legend",          [r'<span class="lg"']),
    ("legend swatch",   [r'<span class="sw"']),
    ("section heading", [r'<section class="basket"']),
    ("heading meta",    [r'<span class="h2-meta"']),
    ("heading count",   [r'<span class="ct"']),
    ("section blurb",   [r'<div class="blurb"']),
    ("family header",   [r'<details class="fam"']),
    ("family name",     [r'<span class="famname"']),
    ("family count",    [r'<span class="famct"']),
    ("family range",    [r'<span class="famr"']),
    ("family bar",      [r'<span class="fambar"']),
    ("collapse ctl",    [r'Collapse all', r'class="collapse', r'id="collapseAll"']),
    ("chip box tc",     [r'<span class="tc[ "]']),
    ("chip box a.tc",   [r'<a class="tc[ "]']),
    ("chip box chip",   [r'<span class="chip[ "]']),
    ("chip box su",     [r'<span class="su[ "]']),
    ("chip name tl",    [r'<span class="tl"']),
    ("chip name nm",    [r'<span class="nm"']),
    ("chip dot",        [r'<span class="dot"']),
    ("chip sub-line",   [r'<span class="te"']),
    ("mini bars",       [r'<i class="mg"', r'<i class="ma"', r'<i class="mr"']),
    ("rights lens rows", [r'<div class="rl-sec"', r'<div class="rl-lbl"']),
    ("empty state",     [r'class="fam-empty"', r'No per-text index']),
    ("canon note",      [r'Indexed from the catalogue']),
    ("greenline",       [r'class="greenline"', r'class="insight"', r'class="gl"']),
    ("footer",          [r'<footer']),
    ("theme button",    [r'id="arch-dark"']),
    ("star button",     [r'id="arch-fav"']),
    ("back arrow",      [r'class="tb-arrow"']),
]


def main():
    src = {r: io.open(os.path.join(MAP, r + ".html"), encoding="utf-8").read()
           for r in ROOMS}

    grid = {}
    for label, pats in ELEMENTS:
        grid[label] = {}
        for r in ROOMS:
            n = sum(len(re.findall(p, src[r], re.S)) for p in pats)
            grid[label][r] = n

    short = {r: r[:4] for r in ROOMS}
    print("TASK 118 PHASE 1 — ROOM GRAMMAR INVENTORY  (counts; . = absent)\n")
    # Task 148 — SAY WHAT IS BEING COUNTED. These are matches in the
    # per-page markup of map/*.html and nothing else. Task 126 moved a
    # large share of the shared grammar OUT of the sixteen pages and into
    # shared files, so an element can read "absent" here while being
    # present in every room on screen — `canon note` went 16/16 -> 0/16
    # and `collapse ctl` 4 -> 2 per room in that one commit (e838922e)
    # without leaving the archive at all. An "absent" below means absent
    # FROM THIS PAGE'S SOURCE; it is not a rendering claim.
    print("counting per-page markup in map/*.html only — shared-file "
          "grammar is invisible here (Task 126)\n")
    print("%-18s %s" % ("element", " ".join("%-5s" % short[r] for r in ROOMS)))
    print("%-18s %s" % ("", " ".join("%-5s" % "" for r in ROOMS)))
    outliers = []
    for label, _ in ELEMENTS:
        row = grid[label]
        present = [r for r in ROOMS if row[r]]
        cells = " ".join("%-5s" % (row[r] if row[r] else ".") for r in ROOMS)
        mark = ""
        if 0 < len(present) < len(ROOMS):
            mark = "  <-- %d/%d" % (len(present), len(ROOMS))
            missing = [r for r in ROOMS if not row[r]]
            outliers.append((label, len(present), missing))
        print("%-18s %s%s" % (label, cells, mark))

    # The count is DERIVED too. It read "the 16 rooms" and "%2d/16" while
    # the sample was one room, which is how a broken population passed for
    # several lanes without anyone reading a wrong number (§8.1d — a
    # report may not assert more than it measured).
    print("\n\nOUTLIERS — element classes NOT universal across the %d rooms "
          "surveyed" % len(ROOMS))
    for label, n, missing in sorted(outliers, key=lambda x: x[1]):
        print("  %-18s %2d/%d   absent: %s"
              % (label, n, len(ROOMS), ", ".join(missing)))

    out = os.path.join(HERE, "room_grammar_inventory.json")
    io.open(out, "w", encoding="utf-8", newline="\n").write(
        json.dumps(grid, indent=1, ensure_ascii=False))
    print("\nwrote " + out)


if __name__ == "__main__":
    main()
