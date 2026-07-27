"""Add AO · 010 — The Word Became Flesh (Tent, Temple, Flesh).

The tenth Codex Object class — incarnational-presence. Materially
distinct from the prior nine:

  AO · 001  cosmological-motif      diagram + ANE parallels.
  AO · 002  translation-tradition   manuscript witness slips.
  AO · 003  genealogical-lineage    descent register + stemma.
  AO · 004  sacred-time             sevenfold rhythm.
  AO · 005  symbolic-motif          vertical axis-mundi.
  AO · 006  covenant-formula        bipartite recurrence.
  AO · 007  wisdom-saying           sparse aphorisms + compression.
  AO · 008  revelatory-vision       threshold → unveiled pairs.
  AO · 009  lament-structure        dotted axis of address.
  AO · 010  incarnational-presence  six compressed indwelling
                                    moments — visitation → tent →
                                    name → flesh → kenosis → tabernacle.

The chamber's form is the form of incarnation itself: compressed,
intimate, embodied. The reader does not read about divine
presence; they enter a sequence of dwellings, each closer than
the last.

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

RECORD_ID = "joh1-incarnation-dwelling"


# Six canonical moments of indwelling presence, in canonical
# sequence — and in increasing intimacy. Each carries a small
# opening rubric (where / how), the canonical text (italic), and
# a witness reference.
INDWELLING_MOMENTS = [
    {
        "numeral": "i",
        "ref": "Genesis 18:1–3",
        "rubric": "by the oaks of Mamre",
        "tradition": "Patriarchal visitation",
        "text": (
            "And the LORD appeared unto him in the plains of Mamre: "
            "and he sat in the tent door in the heat of the day; and "
            "he lift up his eyes and looked, and, lo, three men stood "
            "by him."
        ),
    },
    {
        "numeral": "ii",
        "ref": "Exodus 25:8 · Exodus 40:34",
        "rubric": "the sanctuary in the wilderness",
        "tradition": "The tabernacle inaugurated",
        "text": (
            "And let them make me a sanctuary; that I may dwell among "
            "them… Then a cloud covered the tent of the congregation, "
            "and the glory of the LORD filled the tabernacle."
        ),
    },
    {
        "numeral": "iii",
        "ref": "Isaiah 7:14",
        "rubric": "the name spoken — Immanuel",
        "tradition": "Prophetic — the promise of nearness",
        "text": (
            "Behold, a virgin shall conceive, and bear a son, and "
            "shall call his name Immanuel."
        ),
        "footnote": "ʿImmānû ʾĒl — “with us, God”.",
    },
    {
        "numeral": "iv",
        "ref": "John 1:14",
        "rubric": "the Word made flesh",
        "tradition": "Apostolic — incarnation",
        "text": (
            "And the Word was made flesh, and dwelt among us, (and we "
            "beheld his glory, the glory as of the only begotten of "
            "the Father,) full of grace and truth."
        ),
        "footnote": "καὶ ἐσκήνωσεν ἐν ἡμῖν — and he pitched his tent among us.",
    },
    {
        "numeral": "v",
        "ref": "Philippians 2:6–8",
        "rubric": "the form of a servant",
        "tradition": "Apostolic — the kenosis hymn",
        "text": (
            "Who, being in the form of God, thought it not robbery to "
            "be equal with God: But made himself of no reputation, and "
            "took upon him the form of a servant, and was made in the "
            "likeness of men: And being found in fashion as a man, he "
            "humbled himself."
        ),
    },
    {
        "numeral": "vi",
        "ref": "Revelation 21:3",
        "rubric": "the tabernacle of God with men",
        "tradition": "Apocalyptic — the dwelling restored",
        "text": (
            "Behold, the tabernacle of God is with men, and he will "
            "dwell with them, and they shall be his people, and God "
            "himself shall be with them, and be their God."
        ),
        "consummation": True,
    },
]


# Dwelling vocabulary — the Hebrew/Greek words of indwelling that
# travel across the testaments. The continuity of the lexicon
# carries the continuity of the theme. shakhan begets mishkan;
# skēnoō translates that verb when the Word "dwelt among us" in
# John 1:14 — literally "tabernacled."
DWELLING_VOCABULARY = [
    {
        "script": "שָׁכַן",
        "lang": "he",
        "translit": "shakhan",
        "gloss": "to dwell, to take up residence",
        "note": "the verb of habitation, used throughout the Hebrew Bible for divine presence settling in a place.",
    },
    {
        "script": "מִשְׁכָּן",
        "lang": "he",
        "translit": "mishkan",
        "gloss": "tabernacle — literally, “dwelling-place”",
        "note": "the noun derived from shakhan; the wilderness sanctuary IS the dwelling-place of the divine name.",
    },
    {
        "script": "עִמָּנוּ אֵל",
        "lang": "he",
        "translit": "ʿImmānû ʾĒl",
        "gloss": "“with us — God”",
        "note": "the name given by Isaiah; the construct chain binds the divine name to a preposition of nearness.",
    },
    {
        "script": "σκηνόω",
        "lang": "el",
        "translit": "skēnoō",
        "gloss": "to pitch a tent, to tabernacle",
        "note": "the verb John uses for “dwelt among us” — the same root as the Septuagint’s rendering of mishkan. The Word does not visit; he tabernacles.",
    },
    {
        "script": "σκηνή",
        "lang": "el",
        "translit": "skēnē",
        "gloss": "tent, tabernacle",
        "note": "the noun behind the verb; the same word used in Revelation 21:3 — “the σκηνή of God is with men.”",
    },
]


ARCHIVE_COMMENTARY = (
    "The biblical tradition does not narrate the divine as a "
    "remote sovereign visited at a distance. From the oaks of "
    "Mamre to the wilderness tabernacle to the named child to "
    "the Word made flesh to the eschatological dwelling, the "
    "consistent grammar is one of presence entering — drawing "
    "nearer, taking up residence, inhabiting. The Hebrew verb "
    "shakhan gives the noun mishkan; the Greek skēnoō translates "
    "that verb when John says the Word dwelt among us — the same "
    "word, traveling across testaments and languages, doing the "
    "same work. Incarnation is not a doctrine in this archive; "
    "it is a continuity. What recurs is divinity inhabiting "
    "locality, not as exception but as form."
)


ATLAS_OBJECT = {
    "id": "atlas:object:incarnation:dwelling-presence",
    "class": "incarnational-presence",
    "siglum": "AO · 010",
    "civilizations": [
        "Hebrew Bible — divine-presence tradition",
        "Second-Temple expectation",
        "Apostolic Christian incarnation",
        "Apocalyptic consummation",
    ],
    "traditions": [
        "Patriarchal theophany",
        "Mosaic tabernacle",
        "Prophetic naming (Immanuel)",
        "Apostolic incarnation (Johannine)",
        "Kenotic christology (Pauline)",
        "Eschatological dwelling",
    ],
    "anchorings": [
        {
            "ref": "Genesis 18:1–3",
            "citation": "bible::kjv::gen.18.1",
            "note": "the LORD appeared in the plains of Mamre",
        },
        {
            "ref": "Exodus 25:8",
            "citation": "bible::kjv::exo.25.8",
            "note": "that I may dwell among them",
        },
        {
            "ref": "Isaiah 7:14",
            "citation": "bible::kjv::isa.7.14",
            "note": "and shall call his name Immanuel",
        },
        {
            "ref": "John 1:14",
            "citation": "bible::kjv::jhn.1.14",
            "note": "the Word was made flesh, and dwelt among us",
        },
        {
            "ref": "Philippians 2:6–8",
            "citation": "bible::kjv::php.2.6",
            "note": "took upon him the form of a servant",
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
        "atlas:object:covenant:formula",
        "atlas:object:wisdom:fear-of-the-lord",
        "atlas:object:revelation:opened-heavens",
        "atlas:object:lament:how-long",
    ],
}


RECORD = {
    "id": RECORD_ID,
    "kind": "incarnational-presence",
    "title": "The Word Became Flesh — Tent, Temple, Flesh",
    "body": (
        "Six dwellings in sequence, each closer than the last. "
        "The Hebrew shakhan (to dwell) gives mishkan (the "
        "tabernacle); the Greek skēnoō translates the verb when "
        "John says the Word dwelt among us. The chamber does not "
        "explain incarnation. It enters it."
    ),
    "authority": "tertiary",
    "tradition": "Hebrew Bible & New Testament — divine indwelling tradition",
    "source_basis": (
        "Genesis 18; Exodus 25 & 40; Isaiah 7; John 1; "
        "Philippians 2; Revelation 21 (KJV)"
    ),
    "confidence": "Archive incarnational synthesis",
    "anchors": [
        {"target": "archive:passage:bible::kjv::exo.25.8"},
        {"target": "archive:passage:bible::kjv::isa.7.14"},
        {"target": "archive:passage:bible::kjv::jhn.1.14"},
        {"target": "archive:passage:bible::kjv::rev.21.3"},
    ],
    "indwelling_moments": INDWELLING_MOMENTS,
    "dwelling_vocabulary": DWELLING_VOCABULARY,
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
    print(f"  indwelling moments: {len(INDWELLING_MOMENTS)}")
    for m in INDWELLING_MOMENTS:
        tag = " · CONSUMMATION" if m.get("consummation") else ""
        print(f"    {m['numeral']:>4} · {m['ref']:<26} {m['tradition']}{tag}")
        print(f"         rubric: {m['rubric']!r}")
    print(f"  dwelling vocabulary terms: {len(DWELLING_VOCABULARY)}")
    print(f"  declared anchorings: {len(ATLAS_OBJECT['anchorings'])}")

    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with gzip.open(DATA_GZ, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"\nwrote {DATA.name} + {DATA_GZ.name}")


if __name__ == "__main__":
    main()
