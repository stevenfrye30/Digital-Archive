#!/usr/bin/env python3
"""check_reachability.py — Task 27 closer 1 (2026-07-29): every public index
entry must be reachable from at least one surface.

Surfaces, in the archive's own order of preference:
  A. STRUCTURE PLACEMENT — the df rides a lit chip on some map
     (maps/*/bindings.json read routes);
  B. ROOM LISTING — the df appears on a deployed room page (placed basket
     or the reception/Browse-Held fallback block);
  C. THE READER CATALOG — the reader's own listing (index.json), which
     today still lists everything. Rows reachable ONLY here are recorded
     in tools/reachability_ledger.json — the dated, deliberately-maintained
     ledger this check enforces. ROADMAP phases 2 and 5 exist to burn that
     ledger down (the Religion shelf retiring behind Map/Hall; the
     Philosophy/Literature/Esoteric surfaces).

The invariant that gates every push (guard check 6): NO public row may be
reader-only unless it is in the ledger. New texts must land on a surface,
or their reader-only state must be a recorded decision:

    python tools/check_reachability.py                 # check (guard mode)
    python tools/check_reachability.py --write-ledger  # deliberate re-baseline

Ledger SHRINKAGE is progress and never fails; silent GROWTH fails closed.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INDEX = REPO / "data" / "_generated" / "index.json"
LEDGER = REPO / "tools" / "reachability_ledger.json"


def surfaces():
    ix = json.loads(INDEX.read_text(encoding="utf-8"))["texts"]
    pub = [e for e in ix if not e.get("restricted") and e.get("data_file")]
    # Task 37 (one page per tradition): the surfaces are the Map's —
    # structure routes (bindings read[], which is also the held-editions
    # overlay's derivation) and the map pages' own content (the
    # reception overlays live in the page files). The rooms are
    # permanent redirect stubs and no longer a surface.
    mapped = set()
    for f in sorted((REPO / "maps").glob("*/bindings.json")):
        for c in json.loads(f.read_text(encoding="utf-8"))["chips"]:
            for r in (c.get("read") or []):
                mapped.add(r["df"])
    map_html = "".join(f.read_text(encoding="utf-8")
                       for f in sorted((REPO / "map").glob("*.html")))
    # Task 65 Lane C — the three shelf pages are surfaces too (the
    # phase-5 front doors; the reader-only ledger burns down here).
    map_html += "".join(f.read_text(encoding="utf-8")
                        for f in sorted((REPO / "shelf").glob("*.html")))
    roomed = {e["data_file"] for e in pub if e["data_file"] in map_html}
    reader_only = sorted(e["data_file"] for e in pub
                         if e["data_file"] not in mapped and e["data_file"] not in roomed)
    return pub, mapped, roomed, reader_only


def surface_cross_links() -> list[str]:
    """Task 34: the Hall and the Map must link each other — asserted, not
    assumed, so neither entrance surface loses reachability when the other
    takes the front door. (Guard check 6 protects the texts; this protects
    the surfaces.)"""
    probs = []
    hall = REPO / "hall" / "index.html"
    if not hall.is_file():
        probs.append("hall/index.html is missing — the Religion front door is gone")
    else:
        # Task 40b: the Hall IS the all-traditions view (map/index.html
        # is a redirect stub back to it) — every tradition page must be
        # one door away.
        h = hall.read_text(encoding="utf-8")
        # Task 45: the Abrahamic door split into three
        for slug in ("hindu", "buddhist", "judaism", "christianity", "islam",
                     "eastasian", "zoroastrian", "sikh", "jain", "shinto",
                     "bahai", "ancient", "gnostic", "indigenous", "modern"):
            if f"map/{slug}.html" not in h:
                probs.append(f"hall/index.html carries no door to map/{slug}.html "
                             "(rebuild via 05_scripts/deploy_hall.py)")
    for f in sorted((REPO / "map").glob("*.html")):
        if "hall" not in f.read_text(encoding="utf-8"):
            probs.append(f"map/{f.name} carries no Hall link — the Hall is "
                         "unreachable from that map page")
    return probs


def problems() -> list[str]:
    if not LEDGER.exists():
        return ["tools/reachability_ledger.json is missing — the reachability "
                "baseline was never recorded"]
    ledger = set(json.loads(LEDGER.read_text(encoding="utf-8"))["reader_only"])
    _, _, _, reader_only = surfaces()
    new = [df for df in reader_only if df not in ledger]
    return [f"UNREACHABLE from every structural surface and not in the ledger: {df} "
            "(bind it, place it on a map surface, or record the decision with "
            "tools/check_reachability.py --write-ledger)" for df in new] \
        + surface_cross_links()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-ledger", action="store_true")
    a = ap.parse_args()
    pub, mapped, roomed, reader_only = surfaces()
    on = len({e["data_file"] for e in pub} & (mapped | roomed))
    print(f"public {len(pub)} · map-bound {len(mapped & {e['data_file'] for e in pub})} "
          f"· map-page-listed {len(roomed)} · on a structural surface {on} "
          f"· reader-only {len(reader_only)}")
    if a.write_ledger:
        LEDGER.write_text(json.dumps(
            {"note": "Dated reachability baseline — rows reachable ONLY via the reader "
                     "catalog. Maintained deliberately; ROADMAP phases 2 and 5 burn it "
                     "down. Guard check 6 fails on any public row that is reader-only "
                     "and absent from this list.",
             "generated": "2026-07-29 (Task 27 closer; regenerate with --write-ledger)",
             "count": len(reader_only), "reader_only": reader_only},
            ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        print(f"ledger written: {len(reader_only)} reader-only rows")
        return 0
    probs = problems()
    for p in probs:
        print("FAIL", p)
    ledger = set(json.loads(LEDGER.read_text(encoding="utf-8"))["reader_only"])
    healed = len([df for df in ledger if df not in set(reader_only)])
    if healed:
        print(f"note: {healed} ledger rows have since reached a surface "
              "(shrinkage — rebaseline when convenient)")
    print("REACHABILITY OK" if not probs else f"{len(probs)} unreachable")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
