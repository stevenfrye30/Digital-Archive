"""Add AO · 007 — The Fear of the LORD (Wisdom's Beginning).

The seventh Codex Object class — wisdom-saying. Materially
distinct from the prior six:

  AO · 001  cosmological-motif      diagram + ANE parallels.
  AO · 002  translation-tradition   manuscript witness slips.
  AO · 003  genealogical-lineage    descent register + stemma.
  AO · 004  sacred-time             sevenfold rhythm.
  AO · 005  symbolic-motif          vertical axis-mundi.
  AO · 006  covenant-formula        bipartite recurrence.
  AO · 007  wisdom-saying           sparse centered sayings with
                                    meditative whitespace between
                                    and a compression layer that
                                    surfaces the depth of the
                                    Hebrew phrase yir'at YHWH.

The chamber's form is the form of wisdom: short sentences,
generous silence between, the central phrase left to ramify
rather than be solved.

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

RECORD_ID = "prov1-wisdom-fear"


# Six wisdom sayings — the same insight returning across the
# canon. Each saying is compressed; the chamber leaves them
# alone and surrounds them with silence.
WISDOM_SAYINGS = [
    {
        "numeral": "i",
        "text": "The fear of the LORD is the beginning of knowledge: but fools despise wisdom and instruction.",
        "ref": "Proverbs 1:7",
        "book": "Proverbs",
    },
    {
        "numeral": "ii",
        "text": "Behold, the fear of the Lord, that is wisdom; and to depart from evil is understanding.",
        "ref": "Job 28:28",
        "book": "Job",
    },
    {
        "numeral": "iii",
        "text": "The fear of the LORD is the beginning of wisdom: a good understanding have all they that do his commandments.",
        "ref": "Psalm 111:10",
        "book": "Psalms",
    },
    {
        "numeral": "iv",
        "text": "The fear of the LORD is the beginning of wisdom: and the knowledge of the holy is understanding.",
        "ref": "Proverbs 9:10",
        "book": "Proverbs",
    },
    {
        "numeral": "v",
        "text": "Let us hear the conclusion of the whole matter: Fear God, and keep his commandments: for this is the whole duty of man.",
        "ref": "Ecclesiastes 12:13",
        "book": "Ecclesiastes",
    },
    {
        "numeral": "vi",
        "text": "But the wisdom that is from above is first pure, then peaceable, gentle, and easy to be intreated, full of mercy and good fruits.",
        "ref": "James 3:17",
        "book": "James",
    },
]


# The compressed phrase — yir'at YHWH. Surfaced not to be solved
# but to be inhabited: a few short lexical and translation notes
# that show what the short Hebrew construction holds.
COMPRESSION = {
    "phrase_he": "יִרְאַת יְהוָה",
    "translit": "yirʾat YHWH",
    "english": "the fear of the LORD",
    "notes": [
        {
            "head": "yirʾah — fear, awe, reverence",
            "body": (
                "The noun yirʾah does not split cleanly into 'terror' and "
                "'reverence' in Biblical Hebrew. Its semantic range gathers "
                "both — the gravity of standing in a presence that is not "
                "one's own."
            ),
        },
        {
            "head": "yirʾat YHWH — a construct binding",
            "body": (
                "The construct chain yirʾat-YHWH binds the noun to the "
                "divine name itself. The wisdom literature uses the phrase "
                "not as an emotion but as a posture: oriented attention "
                "toward the LORD as the condition of seeing rightly."
            ),
        },
        {
            "head": "the beginning — rēʾshîth",
            "body": (
                "Hebrew rēʾshîth means 'beginning' but also 'first-fruits', "
                "'best portion', 'principal thing'. The fear of the LORD is "
                "wisdom's first-fruit; not its prerequisite only, but its "
                "abiding centre."
            ),
        },
    ],
    "lxx": "φόβος Κυρίου — phobos Kyriou",
    "vulgate": "timor Domini",
    "trail": (
        "The Septuagint phobos Kyriou and the Vulgate timor Domini "
        "preserve the compression; later scholastic tradition glosses "
        "it as filial fear — the gravity of a child before a parent, "
        "not a slave before a master."
    ),
}


ARCHIVE_COMMENTARY = (
    "Wisdom in the Hebrew tradition is not a body of knowledge "
    "to be acquired but a posture to be returned to. The same "
    "short sentence — 'the fear of the LORD is the beginning of "
    "wisdom' — recurs through Proverbs, Job, the Psalms, "
    "Ecclesiastes, and reaches its echo in the New Testament. "
    "Each return is the same insight, slightly differently "
    "angled. The sayings are short because their object is depth, "
    "not breadth: the more attention pressed into them, the more "
    "they hold. To consult this object is to consult the "
    "archive's commitment that some forms of knowledge are not "
    "statements but inhabitations — that wisdom, properly "
    "speaking, is entered, not solved."
)


ATLAS_OBJECT = {
    "id": "atlas:object:wisdom:fear-of-the-lord",
    "class": "wisdom-saying",
    "siglum": "AO · 007",
    "civilizations": [
        "Hebrew Bible (wisdom tradition)",
        "Second-Temple Judaism",
        "Apostolic Christian wisdom",
    ],
    "traditions": [
        "Proverbs sapiential corpus",
        "Joban wisdom",
        "Psalmic instruction",
        "Qoheleth (Ecclesiastes)",
        "New Testament wisdom (James)",
    ],
    "anchorings": [
        {
            "ref": "Proverbs 1:7",
            "citation": "bible::kjv::pro.1.7",
            "note": "the beginning of knowledge",
        },
        {
            "ref": "Proverbs 9:10",
            "citation": "bible::kjv::pro.9.10",
            "note": "the beginning of wisdom",
        },
        {
            "ref": "Job 28:28",
            "citation": "bible::kjv::job.28.28",
            "note": "behold, the fear of the Lord, that is wisdom",
        },
        {
            "ref": "Psalm 111:10",
            "citation": "bible::kjv::psa.111.10",
            "note": "a good understanding have all they that do his commandments",
        },
        {
            "ref": "Ecclesiastes 12:13",
            "citation": "bible::kjv::ecc.12.13",
            "note": "the conclusion of the whole matter",
        },
        {
            "ref": "James 3:17",
            "citation": "bible::kjv::jas.3.17",
            "note": "the wisdom that is from above",
        },
    ],
    "linked": [
        "atlas:object:cosmology:ane-three-tier",
        "atlas:object:translation:firmament",
        "atlas:object:lineage:antediluvian",
        "atlas:object:ritual:sabbath-pattern",
        "atlas:object:symbol:sacred-mountain",
        "atlas:object:covenant:formula",
    ],
}


RECORD = {
    "id": RECORD_ID,
    "kind": "wisdom-saying",
    "title": "The Fear of the LORD — Wisdom's Beginning",
    "body": (
        "A single sentence returns across the wisdom literature, "
        "slightly differently angled each time: the fear of the "
        "LORD is the beginning of wisdom. The chamber surrounds "
        "the sayings with silence — wisdom is entered rather "
        "than explained."
    ),
    "authority": "tertiary",
    "tradition": "Hebrew Bible — sapiential / wisdom tradition",
    "source_basis": (
        "Proverbs 1:7 & 9:10; Job 28:28; Psalm 111:10; "
        "Ecclesiastes 12:13; James 3:17 (KJV)"
    ),
    "confidence": "Archive contemplative synthesis",
    "anchors": [
        {"target": "archive:passage:bible::kjv::pro.1.7"},
        {"target": "archive:passage:bible::kjv::job.28.28"},
        {"target": "archive:passage:bible::kjv::ecc.12.13"},
        {"target": "archive:passage:bible::kjv::jas.3.17"},
    ],
    "wisdom_sayings": WISDOM_SAYINGS,
    "compression": COMPRESSION,
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
    print(f"  wisdom sayings: {len(WISDOM_SAYINGS)}")
    for s in WISDOM_SAYINGS:
        print(f"    {s['numeral']:>4} · {s['book']:<12} {s['ref']}")
    print(f"  compression notes: {len(COMPRESSION['notes'])}")
    print(f"  declared anchorings: {len(ATLAS_OBJECT['anchorings'])}")

    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with gzip.open(DATA_GZ, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"\nwrote {DATA.name} + {DATA_GZ.name}")


if __name__ == "__main__":
    main()
