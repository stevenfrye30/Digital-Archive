"""Add AO · 012 — The House Filled With Glory (The Layered Sanctuary).

The twelfth Codex Object class — sacred-space. Materially distinct
from the prior eleven:

  AO · 001  cosmological-motif      diagram + ANE parallels.
  AO · 002  translation-tradition   manuscript witness slips.
  AO · 003  genealogical-lineage    descent register + stemma.
  AO · 004  sacred-time             sevenfold rhythm.
  AO · 005  symbolic-motif          vertical axis-mundi.
  AO · 006  covenant-formula        bipartite recurrence.
  AO · 007  wisdom-saying           sparse aphorisms + compression.
  AO · 008  revelatory-vision       threshold → unveiled pairs.
  AO · 009  lament-structure        dotted axis of address.
  AO · 010  incarnational-presence  compressed intimate dwellings.
  AO · 011  resurrection-renewal    rupture-then-return pairings.
  AO · 012  sacred-space            five concentrically narrowing
                                    enclosures — outer gate, court,
                                    holy place, holy of holies, and
                                    at the centre, the glory.

The chamber's form is the form of sacred approach: progressive
inward compression, threshold rubrics between layers, and at
the centre — without a threshold — the indwelling glory. The
reader does not read about temples. They walk inward through
the codex itself.

The codex has already learned how to behave at thresholds
(v51), how to narrow inward and admit gradually (v52); this
chamber lands in an environment that already knows sacred
approach.

Idempotent. Updates both bible_kjv.json and bible_kjv.json.gz.
"""
import gzip
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "bible_kjv.json"
DATA_GZ = ROOT / "data" / "bible_kjv.json.gz"

RECORD_ID = "exo40-sanctuary-glory"


# Five layered enclosures, each a successively inward depth.
# Depth 1 is the outer gate; depth 5 is the indwelling glory.
# Each carries: a name, a Hebrew or Greek term, transliteration,
# a brief gloss, a canonical witness verse, and an optional
# threshold rubric naming what is passed through to enter THIS
# layer. The fifth layer carries no inward threshold — one
# does not pass into the glory; the glory enters the room.
APPROACH_LAYERS = [
    {
        "depth": 1,
        "name": "The Outer Gate",
        "hebrew": "שַׁעַר",
        "translit": "shaʿar",
        "gloss": "the gate, the threshold from common ground",
        "witness": (
            "Enter into his gates with thanksgiving, and into his "
            "courts with praise: be thankful unto him, and bless "
            "his name."
        ),
        "witness_ref": "Psalm 100:4",
        "threshold": "the common ground crossed",
    },
    {
        "depth": 2,
        "name": "The Court",
        "hebrew": "חָצֵר",
        "translit": "ḥatzer",
        "gloss": "the enclosure of the altar",
        "witness": (
            "For a day in thy courts is better than a thousand. I "
            "had rather be a doorkeeper in the house of my God, "
            "than to dwell in the tents of wickedness."
        ),
        "witness_ref": "Psalm 84:10",
        "threshold": "and into his courts",
    },
    {
        "depth": 3,
        "name": "The Holy Place",
        "hebrew": "הַקֹּדֶשׁ",
        "translit": "ha-qodesh",
        "gloss": "the sanctuary — set apart unto the LORD",
        "witness": (
            "For there was a tabernacle made; the first, wherein "
            "was the candlestick, and the table, and the shewbread; "
            "which is called the sanctuary."
        ),
        "witness_ref": "Hebrews 9:2",
        "threshold": "past the first veil",
    },
    {
        "depth": 4,
        "name": "The Holy of Holies",
        "hebrew": "קֹדֶשׁ הַקֳּדָשִׁים",
        "translit": "qodesh ha-qodashim",
        "gloss": "the holiest of all — entered once a year, with blood",
        "witness": (
            "And after the second veil, the tabernacle which is "
            "called the Holiest of all; which had the golden censer, "
            "and the ark of the covenant overlaid round about with "
            "gold, wherein was the golden pot that had manna, and "
            "Aaron’s rod that budded, and the tables of the covenant."
        ),
        "witness_ref": "Hebrews 9:3–4",
        "threshold": "past the second veil",
    },
    {
        "depth": 5,
        "name": "The Glory",
        "hebrew": "כָּבוֹד",
        "translit": "kavod",
        "gloss": "the weight of presence — the indwelling itself",
        "witness": (
            "Then a cloud covered the tent of the congregation, and "
            "the glory of the LORD filled the tabernacle. And Moses "
            "was not able to enter into the tent of the congregation, "
            "because the cloud abode thereon, and the glory of the "
            "LORD filled the tabernacle."
        ),
        "witness_ref": "Exodus 40:34–35",
        "threshold": None,
        "indwelling": True,
    },
]


# Vocabulary of nearness — Hebrew (and one Greek) terms that
# carry the architecture of sacred approach. Each is a word the
# canon uses to name what cannot be diagrammed.
SACRED_VOCABULARY = [
    {
        "script": "קֹדֶשׁ",
        "lang": "he",
        "translit": "qodesh",
        "gloss": "holy — that which is set apart unto the LORD",
        "note": "the root of all sacred-space vocabulary; the noun for holy, the adjective qadosh for the holy one, and the substantive qodashim for the holies.",
    },
    {
        "script": "פָּרֹכֶת",
        "lang": "he",
        "translit": "parocheth",
        "gloss": "the veil before the holiest of all",
        "note": "Exodus 26:33 — “the vail shall divide unto you between the holy place and the most holy.” Torn at the moment of the crucifixion (Matthew 27:51).",
    },
    {
        "script": "כָּבוֹד",
        "lang": "he",
        "translit": "kavod",
        "gloss": "glory — literally, weight",
        "note": "the same root as the Hebrew verb “to be heavy.” Glory in this archive is not radiance but weight — the substantial gravity of the indwelling.",
    },
    {
        "script": "כְּרֻבִים",
        "lang": "he",
        "translit": "keruvim",
        "gloss": "cherubim — the guardians of the inner sanctum",
        "note": "their outstretched wings overshadow the mercy seat (Exodus 25:20); the LORD is said to dwell between the cherubim (Psalm 80:1).",
    },
    {
        "script": "δόξα",
        "lang": "el",
        "translit": "doxa",
        "gloss": "glory — the Septuagint's rendering of kavod",
        "note": "carried through the New Testament; when John says “we beheld his glory” (John 1:14), the same word stands.",
    },
]


ARCHIVE_COMMENTARY = (
    "Sacred space in the biblical tradition is not a building "
    "but a structure of approach. The tabernacle in the "
    "wilderness, the temple in Jerusalem, Ezekiel's restored "
    "sanctuary, the sanctuary opened by the torn veil, and the "
    "eschatological city whose temple is no longer needed "
    "because God himself is its temple — these are not separate "
    "buildings. They are successive answers to the same "
    "question: how shall God dwell among a people, and how shall "
    "the people approach? The form of the answer is graded "
    "nearness: outer gate, court, holy place, holy of holies, "
    "and at the centre, the glory that fills the house. To enter "
    "is to be admitted layer by layer. To read this chamber is "
    "to walk closer to the centre of the room without crossing "
    "a single literal threshold. The codex remembers the "
    "structure even where the buildings are gone."
)


ATLAS_OBJECT = {
    "id": "atlas:object:sanctuary:house-of-glory",
    "class": "sacred-space",
    "siglum": "AO · 012",
    "civilizations": [
        "Hebrew Bible — tabernacle and temple tradition",
        "Second-Temple Judaism",
        "Apostolic Christian sanctuary theology",
        "Apocalyptic vision (heavenly temple)",
    ],
    "traditions": [
        "Mosaic tabernacle (Exodus)",
        "Solomonic temple (1 Kings)",
        "Isaian throne-temple vision",
        "Ezekielian restored sanctuary",
        "Hebraic sanctuary (epistle to the Hebrews)",
        "Apocalyptic temple inversion (Revelation)",
    ],
    "anchorings": [
        {
            "ref": "Exodus 40:34–35",
            "citation": "bible::kjv::exo.40.34",
            "note": "the cloud covered the tent; the glory filled the tabernacle",
        },
        {
            "ref": "1 Kings 8:10–11",
            "citation": "bible::kjv::1ki.8.10",
            "note": "the cloud filled the house of the LORD",
        },
        {
            "ref": "Psalm 84:10",
            "citation": "bible::kjv::psa.84.10",
            "note": "a doorkeeper in the house of my God",
        },
        {
            "ref": "Isaiah 6:1",
            "citation": "bible::kjv::isa.6.1",
            "note": "his train filled the temple",
        },
        {
            "ref": "Ezekiel 43:5",
            "citation": "bible::kjv::eze.43.5",
            "note": "the glory of the LORD filled the house",
        },
        {
            "ref": "Hebrews 9:2–4",
            "citation": "bible::kjv::heb.9.2",
            "note": "the first … the holiest of all",
        },
        {
            "ref": "Revelation 21:22",
            "citation": "bible::kjv::rev.21.22",
            "note": "and I saw no temple therein — the LORD God Almighty and the Lamb are the temple",
        },
    ],
    "linked": [
        "atlas:object:cosmology:ane-three-tier",
        "atlas:object:translation:firmament",
        "atlas:object:lineage:antediluvian",
        "atlas:object:ritual:sabbath-pattern",
        "atlas:object:symbol:sacred-mountain",
        "atlas:object:covenant:formula",
        "atlas:object:wisdom:fear-of-the-lord",
        "atlas:object:revelation:opened-heavens",
        "atlas:object:lament:how-long",
        "atlas:object:incarnation:dwelling-presence",
        "atlas:object:resurrection:bones-and-breath",
    ],
}


RECORD = {
    "id": RECORD_ID,
    "kind": "sacred-space",
    "title": "The House Filled With Glory — The Layered Sanctuary",
    "body": (
        "Five concentric enclosures — outer gate, court, holy "
        "place, holy of holies — and at the centre, where one "
        "does not pass but where one is admitted, the glory. The "
        "chamber walks the reader inward through the codex itself."
    ),
    "authority": "tertiary",
    "tradition": "Hebrew Bible & New Testament — sanctuary tradition",
    "source_basis": (
        "Exodus 25–40; 1 Kings 8; Psalm 84 & 100; Isaiah 6; "
        "Ezekiel 43; Hebrews 9; Revelation 21 (KJV)"
    ),
    "confidence": "Archive sanctuary synthesis",
    "anchors": [
        {"target": "archive:passage:bible::kjv::exo.40.34"},
        {"target": "archive:passage:bible::kjv::1ki.8.10"},
        {"target": "archive:passage:bible::kjv::isa.6.1"},
        {"target": "archive:passage:bible::kjv::rev.21.22"},
    ],
    "approach_layers": APPROACH_LAYERS,
    "sacred_vocabulary": SACRED_VOCABULARY,
    "archive_commentary": ARCHIVE_COMMENTARY,
    "atlas_object": ATLAS_OBJECT,
}


def main():
    with DATA.open(encoding="utf-8") as f:
        data = json.load(f)
    records = data.get("genealogy", [])
    found = False
    for i, r in enumerate(records):
        if r.get("id") == RECORD_ID:
            records[i] = RECORD
            found = True
            break
    if not found:
        records.append(RECORD)
    data["genealogy"] = records

    print(f"{'replaced' if found else 'added'} record {RECORD_ID}")
    print(f"  siglum:  {ATLAS_OBJECT['siglum']}")
    print(f"  class:   {ATLAS_OBJECT['class']}")
    print(f"  kind:    {RECORD['kind']}")
    print(f"  anchors: {[a['target'].split('::').pop() for a in RECORD['anchors']]}")
    print(f"  approach layers: {len(APPROACH_LAYERS)}")
    for L in APPROACH_LAYERS:
        tag = " · INDWELLING" if L.get("indwelling") else ""
        print(f"    depth {L['depth']} · {L['name']:<22} {L['hebrew']:<22} {L['translit']}{tag}")
    print(f"  vocabulary terms: {len(SACRED_VOCABULARY)}")
    print(f"  declared anchorings: {len(ATLAS_OBJECT['anchorings'])}")

    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with gzip.open(DATA_GZ, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"\nwrote {DATA.name} + {DATA_GZ.name}")


if __name__ == "__main__":
    main()
