"""Add AO · 006 — The Covenant Formula (I Will Be Your God).

The sixth Codex Object class — covenant-formula. Materially
distinct from the prior five:

  AO · 001  cosmological-motif      diagram + ANE parallels.
  AO · 002  translation-tradition   manuscript witness slips.
  AO · 003  genealogical-lineage    descent register + stemma.
  AO · 004  sacred-time             sevenfold rhythm.
  AO · 005  symbolic-motif          vertical axis-mundi.
  AO · 006  covenant-formula        bipartite recurrence column —
                                    declaration · pivot · response,
                                    repeating across the canon.

The chamber's form is the form of the covenant itself: a
reciprocal call-and-response that repeats across the canon. The
reader does not read about the covenant; they hear it spoken
into the room.

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

RECORD_ID = "gen17-covenant-formula"


# Seven canonical occurrences of the covenant formula, in
# canonical sequence. Each occurrence is a bipartite pivot:
# the LORD's side (declaration) and the people's side
# (covenantal response / obligation). The "full_quote" is the
# verse text from which the formula is drawn (KJV).
FORMULA_OCCURRENCES = [
    {
        "numeral": "i",
        "ref": "Genesis 17:7–9",
        "era": "Abrahamic Covenant",
        "god_side": "to be a God unto thee, and to thy seed after thee",
        "people_side": "thou shalt keep my covenant, thou, and thy seed after thee",
        "full_quote": (
            "And I will establish my covenant between me and thee "
            "and thy seed after thee in their generations for an "
            "everlasting covenant, to be a God unto thee, and to "
            "thy seed after thee."
        ),
    },
    {
        "numeral": "ii",
        "ref": "Exodus 6:7",
        "era": "Mosaic — the deliverance promise",
        "god_side": "I will be to you a God",
        "people_side": "I will take you to me for a people",
        "full_quote": (
            "And I will take you to me for a people, and I will be "
            "to you a God: and ye shall know that I am the LORD your "
            "God, which bringeth you out from under the burdens of "
            "the Egyptians."
        ),
    },
    {
        "numeral": "iii",
        "ref": "Leviticus 26:12",
        "era": "Priestly — the indwelling",
        "god_side": "I will walk among you, and will be your God",
        "people_side": "ye shall be my people",
        "full_quote": (
            "And I will walk among you, and will be your God, and "
            "ye shall be my people."
        ),
    },
    {
        "numeral": "iv",
        "ref": "Deuteronomy 29:12–13",
        "era": "Deuteronomic — the covenant renewed",
        "god_side": "that he may be unto thee a God",
        "people_side": "that he may establish thee to day for a people unto himself",
        "full_quote": (
            "That thou shouldest enter into covenant with the LORD "
            "thy God… that he may establish thee to day for a people "
            "unto himself, and that he may be unto thee a God."
        ),
    },
    {
        "numeral": "v",
        "ref": "Jeremiah 31:33",
        "era": "Prophetic — the new covenant",
        "god_side": "I will be their God",
        "people_side": "they shall be my people",
        "full_quote": (
            "But this shall be the covenant that I will make with "
            "the house of Israel; After those days, saith the LORD, "
            "I will put my law in their inward parts, and write it "
            "in their hearts; and will be their God, and they shall "
            "be my people."
        ),
    },
    {
        "numeral": "vi",
        "ref": "Ezekiel 36:28",
        "era": "Prophetic — the restoration",
        "god_side": "I will be your God",
        "people_side": "ye shall be my people",
        "full_quote": (
            "And ye shall dwell in the land that I gave to your "
            "fathers; and ye shall be my people, and I will be your "
            "God."
        ),
    },
    {
        "numeral": "vii",
        "ref": "Revelation 21:3",
        "era": "Apocalyptic — the consummation",
        "god_side": "God himself shall be with them, and be their God",
        "people_side": "they shall be his people",
        "full_quote": (
            "Behold, the tabernacle of God is with men, and he will "
            "dwell with them, and they shall be his people, and God "
            "himself shall be with them, and be their God."
        ),
        "consummation": True,
    },
]


# Witness and seal — short formal clauses that surround the
# covenant in scripture. The covenant is not declared in private;
# it is sealed before heaven and earth, before the people, in
# writing, in the answering of one voice.
WITNESS_CLAUSES = [
    {
        "text": "These are the words of the covenant, which the LORD commanded Moses to make with the children of Israel.",
        "ref": "Deuteronomy 29:1",
    },
    {
        "text": "And he wrote upon the tables the words of the covenant, the ten commandments.",
        "ref": "Exodus 34:28",
    },
    {
        "text": "And all the people answered with one voice, and said, All the words which the LORD hath said will we do.",
        "ref": "Exodus 24:3",
    },
    {
        "text": "I call heaven and earth to record this day against you, that I have set before you life and death, blessing and cursing.",
        "ref": "Deuteronomy 30:19",
    },
    {
        "text": "Behold the blood of the covenant, which the LORD hath made with you concerning all these words.",
        "ref": "Exodus 24:8",
    },
]


ARCHIVE_COMMENTARY = (
    "Covenant in the Hebrew canon is not legal obligation set "
    "against communal life — it is communal life, formally "
    "declared. The same reciprocal formula recurs from Abraham's "
    "tents through the Sinai theophany, the priestly walking, the "
    "prophets of exile, and into the apocalyptic vision of a city "
    "whose name is the covenant fulfilled. Each renewal is the "
    "same declaration: a people and a God, formally bound. What "
    "is binding here is not a law but a relationship under the "
    "form of law — identity inscribed by formal speech, witnessed "
    "before heaven and earth, sealed in the speaking itself."
)


ATLAS_OBJECT = {
    "id": "atlas:object:covenant:formula",
    "class": "covenant-formula",
    "siglum": "AO · 006",
    "civilizations": [
        "Hebrew Bible (patriarchal, Mosaic, prophetic)",
        "Second-Temple Judaism",
        "Apostolic Christian witness",
        "Apocalyptic tradition",
    ],
    "traditions": [
        "Abrahamic covenant",
        "Sinai covenant",
        "Priestly covenant",
        "Deuteronomic renewal",
        "New covenant (Jeremianic)",
        "Restoration covenant (Ezekielian)",
        "Eschatological consummation",
    ],
    "anchorings": [
        {
            "ref": "Genesis 17:7–9",
            "citation": "bible::kjv::gen.17.7",
            "note": "the everlasting covenant with Abraham",
        },
        {
            "ref": "Exodus 6:7",
            "citation": "bible::kjv::exo.6.7",
            "note": "I will take you to me for a people",
        },
        {
            "ref": "Leviticus 26:12",
            "citation": "bible::kjv::lev.26.12",
            "note": "I will walk among you",
        },
        {
            "ref": "Deuteronomy 29:12–13",
            "citation": "bible::kjv::deu.29.12",
            "note": "the covenant renewed in Moab",
        },
        {
            "ref": "Jeremiah 31:33",
            "citation": "bible::kjv::jer.31.33",
            "note": "the new covenant — written on the heart",
        },
        {
            "ref": "Ezekiel 36:28",
            "citation": "bible::kjv::eze.36.28",
            "note": "the restoration covenant",
        },
        {
            "ref": "Revelation 21:3",
            "citation": "bible::kjv::rev.21.3",
            "note": "the tabernacle of God is with men",
        },
    ],
    "linked": [
        "atlas:object:cosmology:ane-three-tier",
        "atlas:object:translation:firmament",
        "atlas:object:lineage:antediluvian",
        "atlas:object:ritual:sabbath-pattern",
        "atlas:object:symbol:sacred-mountain",
    ],
}


RECORD = {
    "id": RECORD_ID,
    "kind": "covenant-formula",
    "title": "The Covenant Formula — I Will Be Your God",
    "body": (
        "Across the canon a single reciprocal sentence recurs — "
        "I will be your God; you shall be my people — under "
        "successive covenants and through every renewal. The "
        "formula is the form: a people and a God, formally bound."
    ),
    "authority": "tertiary",
    "tradition": "Hebrew Bible — covenant-formula tradition",
    "source_basis": (
        "Genesis 17; Exodus 6 & 24 & 34; Leviticus 26; "
        "Deuteronomy 29 & 30; Jeremiah 31; Ezekiel 36; "
        "Revelation 21 (KJV)"
    ),
    "confidence": "Archive covenantal synthesis",
    "anchors": [
        {"target": "archive:passage:bible::kjv::gen.17.7"},
        {"target": "archive:passage:bible::kjv::exo.6.7"},
        {"target": "archive:passage:bible::kjv::jer.31.33"},
        {"target": "archive:passage:bible::kjv::rev.21.3"},
    ],
    "formula_occurrences": FORMULA_OCCURRENCES,
    "witness_clauses": WITNESS_CLAUSES,
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
    print(f"  formula occurrences: {len(FORMULA_OCCURRENCES)}")
    for f in FORMULA_OCCURRENCES:
        tag = " · CONSUMMATION" if f.get("consummation") else ""
        print(f"    {f['numeral']:>4} · {f['era']:<40} {f['ref']}{tag}")
    print(f"  witness clauses: {len(WITNESS_CLAUSES)}")
    print(f"  declared anchorings: {len(ATLAS_OBJECT['anchorings'])}")

    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with gzip.open(DATA_GZ, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"\nwrote {DATA.name} + {DATA_GZ.name}")


if __name__ == "__main__":
    main()
