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

ROOMS = sorted(
    f[:-5] for f in os.listdir(MAP)
    if f.endswith(".html")
    and "Task 111 " in io.open(os.path.join(MAP, f), encoding="utf-8").read()
)

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

    print("\n\nOUTLIERS — element classes NOT universal across the 16 rooms")
    for label, n, missing in sorted(outliers, key=lambda x: x[1]):
        print("  %-18s %2d/16   absent: %s" % (label, n, ", ".join(missing)))

    out = os.path.join(HERE, "room_grammar_inventory.json")
    io.open(out, "w", encoding="utf-8", newline="\n").write(
        json.dumps(grid, indent=1, ensure_ascii=False))
    print("\nwrote " + out)


if __name__ == "__main__":
    main()
