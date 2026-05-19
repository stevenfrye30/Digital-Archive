"""Add AO · 004 — The Sabbath Pattern (Consecrated Time).

The fourth Atlas Object class — ritual / sacred-time. Materially
distinct from the prior three:

  AO · 001  cosmological-motif        diagram + ANE parallels.
  AO · 002  translation-tradition     manuscript witness slips.
  AO · 003  genealogical-lineage      descent register + stemma.
  AO · 004  sacred-time               sevenfold rhythm + tradition
                                      recurrence fragments.

The chamber's form is the form of the Sabbath in scripture
itself: six identical movements followed by a seventh that
breaks the cadence and is set apart. Atlas does not explain
this — it inhabits it.

Idempotent: re-running replaces the AO · 004 record in place.
Updates both bible_kjv.json and bible_kjv.json.gz.
"""
import gzip
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "bible_kjv.json"
DATA_GZ = ROOT / "data" / "bible_kjv.json.gz"

RECORD_ID = "gen2-sabbath-pattern"


# Six creation acts + the seventh consecrated day. Each "act"
# is a single short clause distilled from Genesis 1. The refrain
# follows the canonical "and the evening and the morning were
# the Nth day". On day seven the formula is broken — there is no
# refrain; in its place sits the consecration rubric.
SEVENFOLD_RHYTHM = [
    {
        "numeral": "i",
        "act": "Let there be light.",
        "refrain": "And the evening and the morning were the first day.",
        "ref": "Genesis 1:3–5",
    },
    {
        "numeral": "ii",
        "act": "Let there be a firmament in the midst of the waters.",
        "refrain": "And the evening and the morning were the second day.",
        "ref": "Genesis 1:6–8",
    },
    {
        "numeral": "iii",
        "act": "Let the dry land appear; let the earth bring forth grass.",
        "refrain": "And the evening and the morning were the third day.",
        "ref": "Genesis 1:9–13",
    },
    {
        "numeral": "iv",
        "act": "Let there be lights in the firmament of the heaven.",
        "refrain": "And the evening and the morning were the fourth day.",
        "ref": "Genesis 1:14–19",
    },
    {
        "numeral": "v",
        "act": "Let the waters bring forth abundantly the moving creature; let fowl fly above the earth.",
        "refrain": "And the evening and the morning were the fifth day.",
        "ref": "Genesis 1:20–23",
    },
    {
        "numeral": "vi",
        "act": "Let the earth bring forth the living creature; let us make man in our image.",
        "refrain": "And the evening and the morning were the sixth day.",
        "ref": "Genesis 1:24–31",
    },
    {
        "numeral": "vii",
        "consecrated": True,
        "act": "God ended his work; God rested from all his work.",
        "consecration": (
            "And God blessed the seventh day, and sanctified it: "
            "because that in it he had rested from all his work "
            "which God created and made."
        ),
        "ref": "Genesis 2:1–3",
    },
]


# The Sabbath pattern recurring through later traditions. Six
# short witness fragments showing the same ritual interval re-
# anchored in successive texts. Quoted from the KJV; ordered
# chronologically so the reader senses the pattern propagating
# forward through the canon.
RECURRENCE_FRAGMENTS = [
    {
        "ref": "Exodus 20:8–11",
        "tradition": "The Decalogue · Sinai",
        "quote": (
            "Remember the sabbath day, to keep it holy. Six days "
            "shalt thou labour, and do all thy work: but the seventh "
            "day is the sabbath of the LORD thy God… For in six days "
            "the LORD made heaven and earth, the sea, and all that "
            "in them is, and rested the seventh day: wherefore the "
            "LORD blessed the sabbath day, and hallowed it."
        ),
    },
    {
        "ref": "Exodus 31:12–17",
        "tradition": "The Sign · Perpetual Covenant",
        "quote": (
            "Verily my sabbaths ye shall keep: for it is a sign "
            "between me and you throughout your generations… It is "
            "a sign between me and the children of Israel for ever."
        ),
    },
    {
        "ref": "Leviticus 23:3",
        "tradition": "The Priestly Ordering",
        "quote": (
            "Six days shall work be done: but the seventh day is "
            "the sabbath of rest, an holy convocation; ye shall do "
            "no work therein: it is the sabbath of the LORD in all "
            "your dwellings."
        ),
    },
    {
        "ref": "Isaiah 58:13–14",
        "tradition": "The Prophetic Call",
        "quote": (
            "If thou turn away thy foot from the sabbath, from doing "
            "thy pleasure on my holy day; and call the sabbath a "
            "delight, the holy of the LORD, honourable… then shalt "
            "thou delight thyself in the LORD."
        ),
    },
    {
        "ref": "Hebrews 4:9–10",
        "tradition": "The Eschatological Echo",
        "quote": (
            "There remaineth therefore a rest to the people of "
            "God. For he that is entered into his rest, he also "
            "hath ceased from his own works, as God did from his."
        ),
    },
]


ARCHIVE_COMMENTARY = (
    "What is consecrated here is neither a place nor a person "
    "but an interval. Six identical movements pass through the "
    "creation week; the seventh breaks the formula and is set "
    "apart. The text does not argue for the Sabbath. It enacts "
    "it: the form of the passage is the form of the rite. Across "
    "later tradition the same interval re-anchors — at Sinai as "
    "commandment, in the wilderness as sign, in the priestly "
    "order as convocation, in the prophets as delight, in the "
    "letter to the Hebrews as eschatological rest still kept "
    "open. Sacred time, in this archive, is the form that "
    "civilizational memory takes when it must return."
)


ATLAS_OBJECT = {
    "id": "atlas:object:ritual:sabbath-pattern",
    "class": "sacred-time",
    "siglum": "AO · 004",
    "civilizations": [
        "Hebrew Bible (Priestly tradition)",
        "Second-Temple Judaism",
        "Apostolic Christian liturgy",
    ],
    "traditions": [
        "Genesis creation week",
        "Sinai commandment",
        "Priestly Sabbath",
        "Prophetic call to delight",
        "Christian eschatological rest",
    ],
    "anchorings": [
        {
            "ref": "Genesis 2:1–3",
            "citation": "bible::kjv::gen.2.1",
            "note": "the seventh day blessed and sanctified",
        },
        {
            "ref": "Exodus 20:8–11",
            "citation": "bible::kjv::exo.20.8",
            "note": "the fourth commandment — the sabbath remembered",
        },
        {
            "ref": "Exodus 31:12–17",
            "citation": "bible::kjv::exo.31.13",
            "note": "the sabbath as sign — a perpetual covenant",
        },
        {
            "ref": "Leviticus 23:3",
            "citation": "bible::kjv::lev.23.3",
            "note": "the sabbath of rest — an holy convocation",
        },
        {
            "ref": "Isaiah 58:13–14",
            "citation": "bible::kjv::isa.58.13",
            "note": "call the sabbath a delight",
        },
        {
            "ref": "Hebrews 4:9–10",
            "citation": "bible::kjv::heb.4.9",
            "note": "there remaineth a rest to the people of God",
        },
    ],
    "linked": [
        "atlas:object:cosmology:ane-three-tier",
        "atlas:object:translation:firmament",
        "atlas:object:lineage:antediluvian",
    ],
}


RECORD = {
    "id": RECORD_ID,
    "kind": "ritual",
    "title": "The Sabbath Pattern — Consecrated Time",
    "body": (
        "What is consecrated at the end of the creation week is "
        "neither a place nor a person but an interval. The "
        "sevenfold cadence — six movements and a seventh set "
        "apart — recurs through scripture as the form of sacred "
        "time itself."
    ),
    "authority": "tertiary",
    "tradition": "Hebrew Bible — Sabbath / sacred-time tradition",
    "source_basis": (
        "Genesis 2:1–3 (KJV); Exodus 20:8–11; Exodus 31:12–17; "
        "Leviticus 23:3; Isaiah 58:13–14; Hebrews 4:9–10"
    ),
    "confidence": "Archive sacred-time synthesis",
    "anchors": [
        {"target": "archive:passage:bible::kjv::gen.2.1"},
        {"target": "archive:passage:bible::kjv::exo.20.8"},
        {"target": "archive:passage:bible::kjv::exo.31.13"},
        {"target": "archive:passage:bible::kjv::heb.4.9"},
    ],
    "sevenfold_rhythm": SEVENFOLD_RHYTHM,
    "recurrence_fragments": RECURRENCE_FRAGMENTS,
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
    print(f"  anchors: {[a['target'].split('::').pop() for a in RECORD['anchors']]}")
    print(f"  sevenfold rhythm: {len(SEVENFOLD_RHYTHM)} movements")
    for m in SEVENFOLD_RHYTHM:
        marker = " · CONSECRATED" if m.get("consecrated") else ""
        print(f"    {m['numeral']:>4} — {m['act'][:60]}{marker}")
    print(f"  recurrence fragments: {len(RECURRENCE_FRAGMENTS)}")
    for fr in RECURRENCE_FRAGMENTS:
        print(f"    · {fr['ref']:<20} {fr['tradition']}")

    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with gzip.open(DATA_GZ, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"\nwrote {DATA.name} + {DATA_GZ.name}")


if __name__ == "__main__":
    main()
