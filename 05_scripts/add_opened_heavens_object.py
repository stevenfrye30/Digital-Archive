"""Add AO · 008 — The Opened Heavens (Visionary Disclosure).

The eighth Atlas Object class — revelatory-vision. Materially
distinct from the prior seven:

  AO · 001  cosmological-motif      diagram + ANE parallels.
  AO · 002  translation-tradition   manuscript witness slips.
  AO · 003  genealogical-lineage    descent register + stemma.
  AO · 004  sacred-time             sevenfold rhythm.
  AO · 005  symbolic-motif          vertical axis-mundi.
  AO · 006  covenant-formula        bipartite recurrence.
  AO · 007  wisdom-saying           sparse aphorisms + compression.
  AO · 008  revelatory-vision       threshold → unveiled paired
                                    vision blocks, each carrying a
                                    dim portico of partial sight
                                    followed by the unveiled text.

The chamber's form is the form of apocalyptic disclosure: the
veil lifted by degrees. The reader does not read about
revelation; they cross into a series of opened thresholds.

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

RECORD_ID = "isa6-opened-heavens"


# Five canonical visions of the opened heavens. Each carries
# two registers: the THRESHOLD (a brief partial-sight rubric —
# the veil before it lifts) and the UNVEILED (the canonical
# vision quoted from the KJV). The reader crosses the threshold
# into the unveiled text.
THRESHOLD_VISIONS = [
    {
        "numeral": "i",
        "ref": "Isaiah 6:1–3",
        "tradition": "Eighth-century prophet",
        "threshold": "the prophet looks up; the temple opens",
        "unveiled": (
            "In the year that king Uzziah died I saw also the LORD "
            "sitting upon a throne, high and lifted up, and his train "
            "filled the temple. Above it stood the seraphims… And one "
            "cried unto another, and said, Holy, holy, holy, is the "
            "LORD of hosts: the whole earth is full of his glory."
        ),
    },
    {
        "numeral": "ii",
        "ref": "Ezekiel 1:1, 4–10",
        "tradition": "Exilic prophet by the river Chebar",
        "threshold": "the heavens were opened",
        "unveiled": (
            "Now it came to pass… as I was among the captives by the "
            "river of Chebar, that the heavens were opened, and I saw "
            "visions of God. And I looked, and, behold, a whirlwind "
            "came out of the north, a great cloud, and a fire infolding "
            "itself… also out of the midst thereof came the likeness of "
            "four living creatures."
        ),
    },
    {
        "numeral": "iii",
        "ref": "Daniel 7:9–10",
        "tradition": "Second-Temple apocalyptic",
        "threshold": "the thrones were cast down",
        "unveiled": (
            "I beheld till the thrones were cast down, and the Ancient "
            "of days did sit, whose garment was white as snow, and the "
            "hair of his head like the pure wool: his throne was like "
            "the fiery flame, and his wheels as burning fire. A fiery "
            "stream issued and came forth from before him… the judgment "
            "was set, and the books were opened."
        ),
    },
    {
        "numeral": "iv",
        "ref": "Revelation 4:1–6",
        "tradition": "Apostolic apocalypse — Patmos",
        "threshold": "a door was opened in heaven",
        "unveiled": (
            "After this I looked, and, behold, a door was opened in "
            "heaven: and the first voice which I heard was as it were "
            "of a trumpet talking with me; which said, Come up hither, "
            "and I will shew thee things which must be hereafter… and, "
            "behold, a throne was set in heaven, and one sat on the "
            "throne… and there was a rainbow round about the throne."
        ),
    },
    {
        "numeral": "v",
        "ref": "Revelation 21:1–3",
        "tradition": "Eschatological consummation",
        "threshold": "the first things passed away",
        "unveiled": (
            "And I saw a new heaven and a new earth: for the first "
            "heaven and the first earth were passed away; and there was "
            "no more sea. And I John saw the holy city, new Jerusalem, "
            "coming down from God out of heaven, prepared as a bride "
            "adorned for her husband. And I heard a great voice out of "
            "heaven saying, Behold, the tabernacle of God is with men, "
            "and he will dwell with them."
        ),
        "consummation": True,
    },
]


# Vision fragments — short luminous phrases that are the
# revelatory register's own voice, gathered across the canon.
# Not tied to a single vision but to the act of unveiling itself.
VISION_FRAGMENTS = [
    {
        "text": "And the heavens were opened, and I saw visions of God.",
        "ref": "Ezekiel 1:1",
    },
    {
        "text": "After this I looked, and, behold, a door was opened in heaven.",
        "ref": "Revelation 4:1",
    },
    {
        "text": "Come up hither, and I will shew thee things which must be hereafter.",
        "ref": "Revelation 4:1",
    },
    {
        "text": "Holy, holy, holy, Lord God Almighty, which was, and is, and is to come.",
        "ref": "Revelation 4:8 · Isaiah 6:3",
    },
    {
        "text": "And I saw the dead, small and great, stand before God; and the books were opened.",
        "ref": "Revelation 20:12",
    },
]


ARCHIVE_COMMENTARY = (
    "Apocalypse in the Greek means uncovering — the lifting of "
    "a veil. In the biblical canon the apocalyptic register is "
    "not catastrophe but disclosure: a prophet looks up and the "
    "architecture of the heavens opens. The same architecture "
    "returns under different names — Isaiah's throne and "
    "seraphim, Ezekiel's wheels and living creatures, Daniel's "
    "Ancient of Days, John's throne in heaven, the new "
    "Jerusalem descending. What is unveiled is never wholly "
    "given; the visions stop short, the seer falls as one dead, "
    "and the throne remains itself. Revelation is what "
    "knowledge becomes when its object is more than the seer "
    "can hold."
)


ATLAS_OBJECT = {
    "id": "atlas:object:revelation:opened-heavens",
    "class": "revelatory-vision",
    "siglum": "AO · 008",
    "civilizations": [
        "Hebrew Bible — prophetic vision tradition",
        "Second-Temple apocalyptic",
        "Apostolic apocalypse",
    ],
    "traditions": [
        "Eighth-century prophetic (Isaiah)",
        "Exilic prophetic (Ezekiel)",
        "Daniel — Second-Temple apocalyptic",
        "Johannine apocalypse (Patmos)",
        "Eschatological consummation",
    ],
    "anchorings": [
        {
            "ref": "Isaiah 6:1–3",
            "citation": "bible::kjv::isa.6.1",
            "note": "the throne high and lifted up; the seraphim",
        },
        {
            "ref": "Ezekiel 1:1",
            "citation": "bible::kjv::eze.1.1",
            "note": "the heavens were opened; wheels and living creatures",
        },
        {
            "ref": "Daniel 7:9–10",
            "citation": "bible::kjv::dan.7.9",
            "note": "the Ancient of Days; the books opened",
        },
        {
            "ref": "Revelation 4:1–6",
            "citation": "bible::kjv::rev.4.1",
            "note": "a door opened in heaven; the throne and the rainbow",
        },
        {
            "ref": "Revelation 21:1–3",
            "citation": "bible::kjv::rev.21.1",
            "note": "the new heaven and the new earth; the city descending",
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
    ],
}


RECORD = {
    "id": RECORD_ID,
    "kind": "revelatory-vision",
    "title": "The Opened Heavens — Visionary Disclosure",
    "body": (
        "A door opens. A throne becomes visible. The architecture "
        "of the heavens stands disclosed by degrees, and the seer "
        "is given to see only what may be borne. The same vision "
        "returns under different names — five thresholds, one "
        "unveiling."
    ),
    "authority": "tertiary",
    "tradition": "Hebrew Bible — apocalyptic / revelatory tradition",
    "source_basis": (
        "Isaiah 6; Ezekiel 1; Daniel 7; Revelation 4; "
        "Revelation 21 (KJV)"
    ),
    "confidence": "Archive revelatory synthesis",
    "anchors": [
        {"target": "archive:passage:bible::kjv::isa.6.1"},
        {"target": "archive:passage:bible::kjv::eze.1.1"},
        {"target": "archive:passage:bible::kjv::dan.7.9"},
        {"target": "archive:passage:bible::kjv::rev.4.1"},
    ],
    "threshold_visions": THRESHOLD_VISIONS,
    "vision_fragments": VISION_FRAGMENTS,
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
    print(f"  threshold visions: {len(THRESHOLD_VISIONS)}")
    for v in THRESHOLD_VISIONS:
        tag = " · CONSUMMATION" if v.get("consummation") else ""
        print(f"    {v['numeral']:>4} · {v['ref']:<22} {v['tradition']}{tag}")
        print(f"         threshold: {v['threshold']!r}")
    print(f"  vision fragments: {len(VISION_FRAGMENTS)}")
    print(f"  declared anchorings: {len(ATLAS_OBJECT['anchorings'])}")

    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with gzip.open(DATA_GZ, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"\nwrote {DATA.name} + {DATA_GZ.name}")


if __name__ == "__main__":
    main()
