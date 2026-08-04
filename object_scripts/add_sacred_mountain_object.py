"""Add AO · 005 — The Sacred Mountain (Elevation and Encounter).

The fifth Codex Object class — symbolic / imaginal. Materially
distinct from the prior four:

  AO · 001  cosmological-motif      diagram + ANE parallels.
  AO · 002  translation-tradition   manuscript witness slips.
  AO · 003  genealogical-lineage    descent register + stemma.
  AO · 004  sacred-time             sevenfold rhythm + recurrence.
  AO · 005  symbolic-motif          vertical axis-mundi layer stack
                                    with ascent marks between
                                    canonical mountain encounters.

The chamber's form is the form of the motif: a vertical column
of layered sacred elevations connected by a hairline axis-mundi
rule, each layer carrying a brief encounter inscription. The
reader does not read about the Sacred Mountain — they ascend
through it.

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

RECORD_ID = "gen2-sacred-mountain"


# Seven canonical mountain encounters, in canonical sequence
# (Eden → eschatological summit). Each layer is a single
# encounter inscription, not an essay. The seventh layer points
# beyond history — the new Jerusalem set upon the great and
# high mountain.
MOUNTAIN_LAYERS = [
    {
        "numeral": "i",
        "name_en": "Eden",
        "name_he": "עֵדֶן",
        "translit": "ʿĒden",
        "epithet": "the cosmic mount — a river goes out",
        "fragment": (
            "And a river went out of Eden to water the garden; "
            "and from thence it was parted, and became into four heads."
        ),
        "ref": "Genesis 2:10–14 · Ezekiel 28:13–14",
    },
    {
        "numeral": "ii",
        "name_en": "Ararat",
        "name_he": "אֲרָרָט",
        "translit": "ʾĂrārāṭ",
        "epithet": "the ark rests — a world begins again",
        "fragment": (
            "And the ark rested in the seventh month, on the seventeenth "
            "day of the month, upon the mountains of Ararat."
        ),
        "ref": "Genesis 8:4",
    },
    {
        "numeral": "iii",
        "name_en": "Moriah",
        "name_he": "מוֹרִיָּה",
        "translit": "Môrîyâ",
        "epithet": "in the mount of the LORD it shall be seen",
        "fragment": (
            "And Abraham called the name of that place Jehovah-jireh: "
            "as it is said to this day, In the mount of the LORD it "
            "shall be seen."
        ),
        "ref": "Genesis 22:1–14",
    },
    {
        "numeral": "iv",
        "name_en": "Sinai",
        "name_he": "סִינַי",
        "translit": "Sînay",
        "epithet": "the LORD came down — the law given in cloud",
        "fragment": (
            "And the LORD came down upon mount Sinai, on the top of "
            "the mount: and the LORD called Moses up to the top of the "
            "mount; and Moses went up."
        ),
        "ref": "Exodus 19:20 · Deuteronomy 5",
    },
    {
        "numeral": "v",
        "name_en": "Zion",
        "name_he": "צִיּוֹן",
        "translit": "Ṣîyôn",
        "epithet": "his holy hill — the joy of the whole earth",
        "fragment": (
            "Beautiful for situation, the joy of the whole earth, is "
            "mount Zion, on the sides of the north, the city of the "
            "great King."
        ),
        "ref": "Psalm 2:6 · Psalm 48:1–2 · Isaiah 2:2–3",
    },
    {
        "numeral": "vi",
        "name_en": "The Mount of Transfiguration",
        "name_he": None,
        "translit": None,
        "epithet": "his face did shine as the sun",
        "fragment": (
            "And was transfigured before them: and his face did shine "
            "as the sun, and his raiment was white as the light."
        ),
        "ref": "Matthew 17:1–9 · Mark 9:2–8",
    },
    {
        "numeral": "vii",
        "name_en": "The Great and High Mountain",
        "name_he": None,
        "translit": None,
        "epithet": "the holy city descending out of heaven",
        "fragment": (
            "And he carried me away in the spirit to a great and high "
            "mountain, and shewed me that great city, the holy "
            "Jerusalem, descending out of heaven from God."
        ),
        "ref": "Revelation 21:10",
        "summit": True,
    },
]


# Short resonant phrases — the motif's own voice across the
# canon. Not tied to a single mountain, but to elevation as
# symbolic vocabulary. Quoted as italic fragments, each its own
# encounter.
ENCOUNTER_FRAGMENTS = [
    {
        "text": "I will lift up mine eyes unto the hills, from whence cometh my help.",
        "ref": "Psalm 121:1",
    },
    {
        "text": "Who shall ascend into the hill of the LORD? or who shall stand in his holy place?",
        "ref": "Psalm 24:3",
    },
    {
        "text": "The mountain of the LORD’s house shall be established in the top of the mountains, and shall be exalted above the hills.",
        "ref": "Isaiah 2:2",
    },
    {
        "text": "How beautiful upon the mountains are the feet of him that bringeth good tidings.",
        "ref": "Isaiah 52:7",
    },
    {
        "text": "His foundation is in the holy mountains.",
        "ref": "Psalm 87:1",
    },
]


ARCHIVE_COMMENTARY = (
    "The mountain in the Hebrew Bible is not a geographical "
    "accident but a structural image. Wherever heaven and earth "
    "meet — wherever the LORD comes down or the people are "
    "summoned up — there is a mountain. Eden's river goes out "
    "from a height; the ark rests on the mountains of Ararat; "
    "Abraham is sent to the place which God will tell him of; "
    "the LORD descends upon Sinai; Zion is the joy of the whole "
    "earth; the law is given anew on the Mount of Beatitudes; "
    "the new Jerusalem descends on a great and high mountain. "
    "The motif is the topography of revelation — elevation as "
    "the form that nearness takes when sacred and ordinary "
    "space must touch."
)


ATLAS_OBJECT = {
    "id": "atlas:object:symbol:sacred-mountain",
    "class": "symbolic-motif",
    "siglum": "AO · 005",
    "civilizations": [
        "Hebrew Bible",
        "Second-Temple Judaism",
        "Apostolic Christian witness",
        "Apocalyptic tradition",
    ],
    "traditions": [
        "Edenic / cosmic mountain",
        "Patriarchal encounter (Moriah)",
        "Sinai revelation",
        "Zion / Davidic temple-mount",
        "Gospel mountain encounters",
        "Apocalyptic eschatological summit",
    ],
    "anchorings": [
        {
            "ref": "Genesis 2:10–14",
            "citation": "bible::kjv::gen.2.10",
            "note": "Eden — the cosmic mount, the river going out",
        },
        {
            "ref": "Genesis 8:4",
            "citation": "bible::kjv::gen.8.4",
            "note": "Ararat — the ark rests, a world begins again",
        },
        {
            "ref": "Genesis 22:14",
            "citation": "bible::kjv::gen.22.14",
            "note": "Moriah — in the mount of the LORD it shall be seen",
        },
        {
            "ref": "Exodus 19:20",
            "citation": "bible::kjv::exo.19.20",
            "note": "Sinai — the LORD came down on the top of the mount",
        },
        {
            "ref": "Psalm 48:1–2",
            "citation": "bible::kjv::psa.48.1",
            "note": "Zion — beautiful for situation",
        },
        {
            "ref": "Psalm 121:1",
            "citation": "bible::kjv::psa.121.1",
            "note": "I will lift up mine eyes unto the hills",
        },
        {
            "ref": "Isaiah 2:2–3",
            "citation": "bible::kjv::isa.2.2",
            "note": "the mountain of the LORD's house exalted",
        },
        {
            "ref": "Matthew 5:1",
            "citation": "bible::kjv::mat.5.1",
            "note": "Sermon on the Mount — the new law",
        },
        {
            "ref": "Matthew 17:1–9",
            "citation": "bible::kjv::mat.17.1",
            "note": "Transfiguration — his face did shine as the sun",
        },
        {
            "ref": "Revelation 21:10",
            "citation": "bible::kjv::rev.21.10",
            "note": "the great and high mountain — new Jerusalem descending",
        },
    ],
    "linked": [
        "atlas:object:cosmology:ane-three-tier",
        "atlas:object:translation:firmament",
        "atlas:object:lineage:antediluvian",
        "atlas:object:ritual:sabbath-pattern",
    ],
}


RECORD = {
    "id": RECORD_ID,
    "kind": "symbolic-motif",
    "title": "The Sacred Mountain — Elevation and Encounter",
    "body": (
        "Wherever heaven and earth meet in the Hebrew canon, there is "
        "a mountain. The motif recurs through seven canonical layers "
        "— from Eden's heights to the great and high mountain of the "
        "apocalypse — as a structural image, not a geographical "
        "accident."
    ),
    "authority": "tertiary",
    "tradition": "Hebrew Bible — Sacred-mountain motif",
    "source_basis": (
        "Genesis 2:10, 8:4, 22:14; Exodus 19:20; Psalm 48 & 121; "
        "Isaiah 2; Matthew 5 & 17; Revelation 21 (KJV)"
    ),
    "confidence": "Archive symbolic synthesis",
    "anchors": [
        {"target": "archive:passage:bible::kjv::gen.2.10"},
        {"target": "archive:passage:bible::kjv::exo.19.20"},
        {"target": "archive:passage:bible::kjv::mat.5.1"},
        {"target": "archive:passage:bible::kjv::rev.21.10"},
    ],
    "mountain_layers": MOUNTAIN_LAYERS,
    "encounter_fragments": ENCOUNTER_FRAGMENTS,
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
    print(f"  mountain layers: {len(MOUNTAIN_LAYERS)}")
    for m in MOUNTAIN_LAYERS:
        summit = " · SUMMIT" if m.get("summit") else ""
        print(f"    {m['numeral']:>4} — {m['name_en']:<32} {summit}")
    print(f"  encounter fragments: {len(ENCOUNTER_FRAGMENTS)}")
    print(f"  declared anchorings: {len(ATLAS_OBJECT['anchorings'])}")

    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with gzip.open(DATA_GZ, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"\nwrote {DATA.name} + {DATA_GZ.name}")


if __name__ == "__main__":
    main()
