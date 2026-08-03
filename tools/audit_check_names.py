#!/usr/bin/env python3
"""audit_check_names.py — the §8.1d sweep.

THE EIGHTH COSTUME. 8.1b asks whether a check examined anything. 8.1c
asks whether its subject set can be empty. Neither asks the question
this tool asks:

    DOES THE PREDICATE TEST THE VALUE THE NAME PROMISES?

A check can fire, examine a full real population, and report green while
measuring a weaker rule than its own label states. Nothing downstream can
tell, because the report carries the NAME — and the name is what a STATUS
quotes and the next lane trusts.

The worked example this tool exists for: the battery's mobile group
asserted `"every visible target ≥ 44px"` over the predicate
`r.height < 44 || r.width < 24`. The ruled floor is 44x44. A 30x44 star
and a 24x44 shelf link passed a check whose name says they cannot. Task
122's vacuity audit read that line, fixed its vacuity, and never saw the
`< 24` beside the `< 44` it had just written about.

Two rules, both mechanical:

  1  NUMBERS. Every number in a check's name must appear in the code that
     decides it. A name saying 44 whose predicate only knows 24 is the
     costume exactly.
  2  SCOPE. A name saying "every" / "all" / "no" must not sit over a
     predicate carrying a scope filter the name never mentions — an
     early `return` on off-screen elements, a slice, a head-limit.

Exit 0 = every name matches its predicate. Exit 1 = a name overstates.
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent

# The batteries. Task 122 item 3 named them; this is that list plus the
# two batteries written since.
BATTERIES = [
    "test_surface.py",
    "test_mobile_inhabitation.py",
    "check_reachability.py",
    "crawl_links.py",
    "inventory_grammar.py",
    "audit_vacuity.py",
    "prepush_guard.py",
    "check_shelves_drift.py",
]

# numbers that are never a ruled threshold: version tags, indices, the
# slice bounds in a detail string, percentages of a ratio already named.
NOISE = {"0", "1", "2", "100"}

# Constants inside a formula are not thresholds. These are the sRGB
# linearisation terms in the WCAG relative-luminance function; a contrast
# check that names 4.5 is not "also enforcing 0.03928".
NOISE |= {"0.03928", "0.055", "1.055", "2.4", "12.92", "0.2126", "0.7152",
          "0.0722", "255"}

# Nor is a SANITY BOUND a threshold. 21 is the maximum contrast ratio that
# can exist (pure black on pure white) and 255 the maximum channel; a probe
# that refuses values outside them is checking ITSELF, not the page. Doctrine
# 8.1f asks probes to do exactly that, so the sweep must not read the guard
# it mandated as a second floor beside the named one.
NOISE |= {"21"}

# A SCOPE defect excludes elements from EXAMINATION. A `.slice(0, N)` on
# the offenders being *reported* is not one — the predicate still scanned
# everything and only the printout is capped. Flagging those was this
# tool's own first draft and it produced 25 false positives against 0 real
# ones, which is the costume in the instrument built to find the costume.
# So: only filters that decide what gets LOOKED AT.
# The filter must actually EXCLUDE. After Task 126-R the same viewport
# test survives in TAP_JS as `if (...) offscreen++;` — it counts what is
# below the fold and examines it anyway, which is the opposite of the
# defect. A pattern that flagged the condition alone reported the fixed
# code as broken, so the `return` is part of the pattern.
SCOPE_PATTERNS = [
    (r"\.bottom\s*<\s*0\s*\|\|[^;{]*\.top\s*>\s*innerHeight\s*\)\s*return",
     "an off-screen early return (elements below the fold are never examined)"),
    (r"\.top\s*>\s*innerHeight\s*\)\s*return",
     "an off-screen early return (elements below the fold are never examined)"),
    (r"\bhead_limit\s*=\s*\d+", "a head limit on the examined set"),
]

UNIVERSAL = re.compile(r"\b(every|all|no|never|none|any)\b", re.I)

# "≥ 44px", "at least 44" — a name that PROMISES a threshold. A bare
# "38px" or "at 390px" states a context, not a floor, and flagging those
# produced four false positives in this tool's first run.
THRESHOLD = re.compile(
    r"(?:[≥≤><]=?\s*|at least\s+|at most\s+|no less than\s+|min(?:imum)?\s+)"
    r"(\d+(?:\.\d+)?)", re.I)

# a comparison against a constant, in JS or python
COMPARISON = re.compile(r"[<>]=?\s*(\d+(?:\.\d+)?)")


def js_blocks(src: str) -> str:
    """Everything inside triple-quoted JS, where the predicates live."""
    return "\n".join(m.group(0) for m in
                     re.finditer(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', src))


def numbers(text: str) -> set[str]:
    return {n for n in re.findall(r"\b\d+(?:\.\d+)?\b", text)}


def scan(path: Path):
    src = path.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [], [f"{path.name}: unparseable ({e})"]

    lines = src.splitlines()
    js = js_blocks(src)
    findings, seen = [], 0

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = getattr(fn, "attr", None) or getattr(fn, "id", None)
        if name != "check" or not node.args:
            continue
        # R.check(group, what, ok, detail=...)  — `what` is arg 1
        what_node = node.args[1] if len(node.args) > 1 else None
        if not isinstance(what_node, (ast.Constant, ast.JoinedStr)):
            continue
        if isinstance(what_node, ast.Constant):
            what = str(what_node.value)
        else:
            what = "".join(v.value for v in what_node.values
                           if isinstance(v, ast.Constant))
        if not what:
            continue
        seen += 1

        # the predicate: the `ok` expression, plus the surrounding window
        # (predicates are usually computed a few lines above the call)
        lo = max(0, node.lineno - 26)
        hi = min(len(lines), node.end_lineno + 2)
        window = "\n".join(lines[lo:hi])
        ok_src = ast.get_source_segment(src, node.args[2]) if len(node.args) > 2 else ""
        # the JS the window pulls from, by variable name
        pool = window + "\n" + (ok_src or "")
        for m in re.findall(r"\b([A-Z_]{3,})\b", pool):
            for jm in re.finditer(r"(%s\s*=\s*\"\"\"[\s\S]*?\"\"\")" % re.escape(m), src):
                pool += "\n" + jm.group(1)
        # NOT: `pool += js`. Dumping every module-level JS block into every
        # check's pool made the contrast helper's 0.03928 and the mobile
        # group's 24 visible to unrelated checks, and produced four false
        # THRESHOLD reports in this tool's first run. Only the JS constants
        # this check actually names are resolved, above.

        # ── rule 1a: numbers in the name must appear in the predicate ──
        want = numbers(what) - NOISE
        have = numbers(pool)
        missing = sorted(want - have)
        if missing:
            findings.append({
                "file": path.name, "line": node.lineno, "what": what,
                "kind": "NUMBER", "detail":
                    "name states %s; predicate never mentions %s"
                    % (", ".join(sorted(want)), ", ".join(missing))})

        # ── rule 1b: ONE named threshold, TWO enforced constants ──
        # The founding case. `"every visible target ≥ 44px"` over
        # `r.height < 44 || r.width < 24` passes 1a — 44 IS in the
        # predicate. The defect is that the name promises a single floor
        # and the code enforces two different ones. So: when a name states
        # a threshold, every comparison constant in its predicate must be
        # that threshold.
        named = {m.group(1) or m.group(2) for m in THRESHOLD.finditer(what)}
        named -= NOISE
        if named and not missing:
            # A LENGTH TEST IS NOT A THRESHOLD. `m.length > 3` asks whether
            # a colour string carried an alpha channel; it says nothing
            # about the value being asserted. Leaving it in made the
            # contrast checks read as "promises 4.5, also enforces 3" —
            # the sweep crying wolf on structural arithmetic, which is
            # how a checker trains its reader to skip it.
            pool_cmp = re.sub(r"\.length\s*[<>]=?\s*\d+", " ", pool)
            cmps = {c for c in COMPARISON.findall(pool_cmp)} - NOISE
            stray = sorted(cmps - named)
            if stray:
                findings.append({
                    "file": path.name, "line": node.lineno, "what": what,
                    "kind": "THRESHOLD", "detail":
                        "name promises the single floor %s; the predicate also "
                        "compares against %s — one named value, %d enforced"
                        % ("/".join(sorted(named)), ", ".join(stray),
                           len(cmps))})

        # ── rule 2: a universal name over a scoped predicate ──
        if UNIVERSAL.search(what):
            for pat, label in SCOPE_PATTERNS:
                if re.search(pat, pool):
                    findings.append({
                        "file": path.name, "line": node.lineno, "what": what,
                        "kind": "SCOPE", "detail":
                            "name is universal but the predicate carries %s" % label})
                    break

    return findings, [], seen


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true",
                    help="sweep every .py in tools/, not just the batteries")
    a = ap.parse_args()

    targets = sorted(TOOLS.glob("*.py")) if a.all else \
        [TOOLS / b for b in BATTERIES]

    print("audit_check_names — the §8.1d sweep")
    print("  does each check's PREDICATE test the value its NAME promises?\n")

    all_findings, total_checks, files_read = [], 0, 0
    for t in targets:
        if not t.exists():
            print("  (absent) %s" % t.name)
            continue
        files_read += 1
        found, errs, seen = scan(t)
        total_checks += seen
        for e in errs:
            print("  " + e)
        if seen:
            mark = "FAIL" if found else "ok  "
            print("  %s %-30s %3d checks, %d mismatch(es)"
                  % (mark, t.name, seen, len(found)))
        all_findings += found

    # §8.1b applied to this tool itself: a sweep that examined no checks
    # is not a clean sweep, it is a sweep that did not run.
    if total_checks == 0:
        print("\nSTOP: examined 0 checks across %d file(s). A name/predicate "
              "sweep that found no checks is not evidence that names match "
              "— it is evidence this tool is not reading the batteries."
              % files_read)
        return 1

    print("\n  swept %d checks across %d batteries" % (total_checks, files_read))

    if not all_findings:
        print("  OK — every check name is matched by its predicate.")
        return 0

    print("\n  %d NAME/PREDICATE MISMATCH(ES):\n" % len(all_findings))
    for f in all_findings:
        print("    %s:%d  [%s]" % (f["file"], f["line"], f["kind"]))
        print("      name: %s" % f["what"])
        print("      %s\n" % f["detail"])
    return 1


if __name__ == "__main__":
    sys.exit(main())
