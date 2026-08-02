#!/usr/bin/env python3
"""audit_vacuity.py — Task 122: does every check prove it looked?

Task 121 found the battery's FLAT fixture naming a deleted text. It
rendered an empty page, so every "flat" assertion had been PASSING BY
MATCHING NOTHING — green, for lanes. A check that passes by matching
nothing is not a weak check, it is a FALSE REPORT: it buys confidence it
has not earned. The question is not whether that one is fixed but how
many others there are.

Two failure modes, needing two different instruments:

  MODE 2 — THE CHECK NEVER FIRES. A loop over an empty set, a branch
    skipped, a `continue` that quietly excuses a room. It appears in the
    report in no form at all, which is why nobody notices. Detected by
    recording the source line of every executed check and diffing
    against every `R.check(` site in the file.

  MODE 1 — THE CHECK FIRES BUT EXAMINED NOTHING. The FLAT mode; it
    appears as a pass.

    A first attempt flagged any passing check whose detail string was
    empty, and reported 189 "findings" — nearly all false. It conflated
    three unlike things: a check that deliberately asserts ABSENCE
    (where 0 is the point), a check that simply passes no detail, and a
    check that found nothing to look at. Only the third is vacuity, and
    no text heuristic separates them.

    The honest discriminator is structural. An assertion whose PASS
    CONDITION IS AN ABSENCE passes identically whether the thing is
    correctly gone or the page never rendered — those two are
    indistinguishable from outside, which is exactly how FLAT survived.
    So the audit lists every absence-assertion and asks one question of
    each: does its function prove the subject exists first?

Run:  python tools/audit_vacuity.py            # full audit
      python tools/audit_vacuity.py --static   # source only, no browser
"""
from __future__ import annotations

import argparse
import ast
import inspect
import io
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
BATTERY = HERE / "test_surface.py"

# a function proves its subject exists if it asserts liveness somewhere
LIVENESS = re.compile(r"fixture renders a cover|renders a cover|is alive|"
                      r"__alive|found its subject|subject\(pg|found targets|"
                      r"subject exists", re.I)


def _read():
    src = io.open(BATTERY, encoding="utf-8").read()
    return src, ast.parse(src)


def static_shapes():
    """The shapes the ruling names, found in the source. CANDIDATES —
    static analysis cannot know whether a loop is empty at run time."""
    src, tree = _read()
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in ("all", "any"):
            out.append((node.lineno, "vacuous-truth",
                        f"{node.func.id}() is vacuously "
                        f"{'True' if node.func.id == 'all' else 'False'} over an empty sequence"))
        if isinstance(node, ast.For):
            if any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                   and n.func.attr == "check" for n in ast.walk(node)):
                for n in ast.walk(node):
                    if isinstance(n, ast.Continue):
                        out.append((n.lineno, "skip-excuses-subject",
                                    "continue inside an asserting loop — the skipped "
                                    "subject goes unexamined and unmentioned"))
    for i, line in enumerate(src.split("\n"), 1):
        if re.search(r"==\s*['\"]{2}|['\"]{2}\s*==", line):
            out.append((i, "empty-string-compare", line.strip()[:66]))
    return sorted(out)


def absence_assertions():
    """Every check whose pass condition is an absence, and whether its
    function proves the subject exists."""
    src, tree = _read()
    out = []
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        fn_src = ast.get_source_segment(src, fn) or ""
        guarded = bool(LIVENESS.search(fn_src))
        for node in ast.walk(fn):
            if not (isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "check" and len(node.args) >= 3):
                continue
            cond = (ast.get_source_segment(src, node.args[2]) or "").replace("\n", " ")
            what = (ast.get_source_segment(src, node.args[1]) or "").replace("\n", " ")
            if not cond:
                continue
            if (re.search(r"\bis None\b", cond)
                    or re.search(r"==\s*0\b", cond)
                    or re.match(r"\s*not\s", cond)
                    or re.search(r"\ball\(", cond)
                    or re.search(r"len\([^)]*\)\s*==\s*0", cond)
                    or re.search(r"==\s*\[\]", cond)):
                # SELF-GUARDING: a condition with a positive conjunct
                # cannot pass on an empty page — something has to be
                # truthy for it to hold, so the subject is proved by the
                # assertion itself. `x["reading"] and x["attr"] is None`
                # is not vacuity-prone; `not x["small"]` alone is.
                conjuncts = [c.strip() for c in re.split(r"\band\b", cond)]
                positive = [c for c in conjuncts
                            if c and not re.match(r"not\s", c)
                            and "is None" not in c and not re.search(r"==\s*0\b", c)
                            and not re.search(r"==\s*\[\]", c)]
                state = "self-guard" if positive else ("guarded" if guarded else "UNGUARDED")
                out.append((node.lineno, fn.name, state, what[:54], cond[:60]))
    return out


def check_sites():
    src, _ = _read()
    return {i: line.strip()[:76] for i, line in enumerate(src.split("\n"), 1)
            if re.search(r"\bR\.check\(", line)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--static", action="store_true")
    a = ap.parse_args()

    print("=" * 72)
    print("STATIC — candidate shapes (leads, not findings)")
    print("=" * 72)
    shapes = static_shapes()
    for ln, kind, why in shapes:
        print(f"  line {ln:>4}  {kind:<22} {why}")
    print(f"  {len(shapes)} candidate site(s)")

    print("\n" + "=" * 72)
    print("MODE 1 — ABSENCE-ASSERTIONS (the pass condition is a nothing)")
    print("=" * 72)
    abs_ = absence_assertions()
    for ln, fn, state, what, cond in abs_:
        print(f"  line {ln:>4}  [{state:>10}]  {fn}")
        print(f"              {what}")
        print(f"              cond: {cond}")
    unguarded = [x for x in abs_ if x[2] == "UNGUARDED"]
    print(f"  {len(abs_)} absence-assertion(s); {len(unguarded)} in a function that "
          f"never proves its subject rendered")

    if a.static:
        return 0

    import test_surface as T
    executed: dict[int, int] = {}
    orig = T.Result.check

    def traced(self, group, what, ok, detail=""):
        # sys._getframe, NOT inspect.stack(): the latter resolves the
        # full frame context on every call and, at 800+ calls, slowed the
        # run enough to fail a timing-sensitive cover check that passes
        # standalone. An instrument that changes the result is not an
        # instrument — which is the same lesson as the rest of this lane,
        # pointed at the audit itself.
        ln = sys._getframe(1).f_lineno
        executed[ln] = executed.get(ln, 0) + 1
        return orig(self, group, what, ok, detail)

    T.Result.check = traced
    sys.argv = [sys.argv[0]]
    print("\n" + "=" * 72)
    print("RUNTIME — the battery, every check instrumented")
    print("=" * 72)
    rc = T.main()

    sites = check_sites()
    never = {ln: t for ln, t in sites.items() if ln not in executed}
    print("\n" + "=" * 72)
    print("MODE 2 — CHECKS THAT NEVER FIRED (silent absence)")
    print("=" * 72)
    for ln, t in sorted(never.items()):
        print(f"  line {ln:>4}  {t}")
    print(f"  {len(never)} of {len(sites)} call sites never executed")

    print("\n" + "=" * 72)
    print(f"battery exit={rc} · {sum(executed.values())} checks executed from "
          f"{len(executed)} of {len(sites)} sites")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
