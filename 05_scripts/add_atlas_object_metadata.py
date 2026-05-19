"""Stamp the gen1-cosmology-firmament record with Atlas Object
metadata — the first record promoted from "annotation" to "Atlas
Object encountered through this verse."

Adds the following block to that one record:

  atlas_object: {
    id:            canonical object identifier (atlas:object: ns)
    class:         object class (cosmological-motif, etc.)
    siglum:        manuscript-style short code shown in the chamber
    civilizations: civilizational contexts the object spans
    traditions:    traditions through which it has been transmitted
    anchorings:    other passages where this object may be met
    linked:        related Atlas Object ids (future)
  }

This is a data-only stamp. The chamber renderer (in index.html)
reads the block and quietly surfaces the siglum and anchorings.

Idempotent — re-running overwrites the block in place. Updates
both bible_kjv.json and bible_kjv.json.gz so live deployments
read the new fields.
"""
import gzip
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "bible_kjv.json"
DATA_GZ = ROOT / "data" / "bible_kjv.json.gz"


# ── The cosmology object's Atlas-side identity ──────────────────
# The same object — Ancient ANE three-tier cosmos — is encountered
# in Genesis 1 here, but also in Psalms, Job, Ezekiel, and in
# explicit comparative parallel through Enūma Eliš. The data
# captures that breadth even though the chamber renders only a
# quiet list of anchorings.
COSMOLOGY_OBJECT = {
    "id": "atlas:object:cosmology:ane-three-tier",
    "class": "cosmological-motif",
    "siglum": "AO · 001",
    "civilizations": [
        "Israel (Iron Age)",
        "Babylonia",
        "Egypt",
    ],
    "traditions": [
        "Ancient Hebrew",
        "Mesopotamian",
        "Egyptian",
    ],
    # Other passages where the same Atlas Object may be encountered.
    # External refs (non-canonical, e.g. Mesopotamian texts) carry
    # external: true and no internal citation.
    "anchorings": [
        {
            "ref": "Genesis 1:6–10",
            "citation": "bible::kjv::gen.1.6",
            "note": "the firmament installed; waters divided",
        },
        {
            "ref": "Psalms 104:5–9",
            "citation": "bible::kjv::psa.104.5",
            "note": "the earth fixed on its foundations; waters bounded",
        },
        {
            "ref": "Job 38:4–11",
            "citation": "bible::kjv::job.38.4",
            "note": "the sea's prescribed bound — the deep addressed by YHWH",
        },
        {
            "ref": "Ezekiel 1:22",
            "citation": "bible::kjv::eze.1.22",
            "note": "a firmament above the living creatures",
        },
        {
            "ref": "Enūma Eliš IV.135 – V.62",
            "external": True,
            "note": "Marduk splits Tiāmat; upper and lower waters formed",
        },
    ],
    # Related Atlas Objects — placeholders for future objects.
    # Listed by id so the architecture supports cross-linking
    # before any of these objects exist as full chambers.
    "linked": [
        "atlas:object:cosmology:flood-cosmos",
        "atlas:object:cosmology:temple-mountain",
        "atlas:object:cosmology:divine-council",
    ],
}


def main():
    with DATA.open(encoding="utf-8") as f:
        data = json.load(f)
    target = None
    for r in data.get("genealogy", []):
        if r.get("id") == "gen1-cosmology-firmament":
            target = r
            break
    if not target:
        raise SystemExit("gen1-cosmology-firmament record not found")
    target["atlas_object"] = COSMOLOGY_OBJECT

    # Multi-anchor: the Atlas Object recurs across the canon, so the
    # record now carries anchorings on Psalm 104:5 and Job 38:4 in
    # addition to the canonical Genesis 1:6 anchoring. The folio
    # render iterates all anchors, so a single record contributes
    # markers wherever it is encountered.
    target["anchors"] = [
        {"target": "archive:passage:bible::kjv::gen.1.6"},
        {"target": "archive:passage:bible::kjv::psa.104.5"},
        {"target": "archive:passage:bible::kjv::job.38.4"},
    ]
    print("stamped atlas_object onto gen1-cosmology-firmament")
    print(f"  siglum: {COSMOLOGY_OBJECT['siglum']}")
    print(f"  class:  {COSMOLOGY_OBJECT['class']}")
    print(f"  anchors (canon recurrence): {len(target['anchors'])}")
    for a in target["anchors"]:
        print(f"    - {a['target']}")
    print(f"  anchorings (declared, may be wider): {len(COSMOLOGY_OBJECT['anchorings'])}")
    print(f"  linked Atlas Objects:               {len(COSMOLOGY_OBJECT['linked'])}")

    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with gzip.open(DATA_GZ, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"\nwrote {DATA.name} + {DATA_GZ.name}")


if __name__ == "__main__":
    main()
