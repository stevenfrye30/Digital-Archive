"""Add AO · 011 — Bones Clothed With Breath (Resurrection and Renewal).

The eleventh Atlas Object class — resurrection-renewal. Materially
distinct from the prior ten:

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
  AO · 011  resurrection-renewal    rupture-then-return pairings
                                    held by a hairline scar mark —
                                    the dimmed "before" remains
                                    visible above the restored
                                    "after"; the wounds remain.

The chamber's form is the form of resurrection itself: renewal
that preserves the marks of rupture. The "before" — the silence,
the corruption, the dying — is not erased; it is kept legible,
dimmed, above the return. The reader sees life come back through
typography itself: faded text breathes into restored text.

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

RECORD_ID = "eze37-bones-breath"


# Six canonical return-through-rupture moments. Each carries a
# numbered head, a paired "before" (the rupture / silence /
# corruption state — kept dim) and "after" (the return / renewal
# / restored breath — at full intensity), and an optional
# footnote (Hebrew / Greek root). The John 20 moment carries an
# additional "wound mark" — the chamber's structural claim made
# explicit for the moment where it is also the theological text.
RETURN_MOMENTS = [
    {
        "numeral": "i",
        "ref": "Ezekiel 37:11 → 37:10",
        "tradition": "Exilic vision — the valley of dry bones",
        "before": (
            "Our bones are dried, and our hope is lost: "
            "we are cut off for our parts."
        ),
        "after": (
            "And the breath came into them, and they lived, "
            "and stood up upon their feet, an exceeding great "
            "army."
        ),
        "footnote": "רוּחַ (ruach) — breath, wind, spirit; the same word that hovers in Genesis 1:2.",
    },
    {
        "numeral": "ii",
        "ref": "Jonah 2:6 (a → b)",
        "tradition": "Prophetic — brought up from the pit",
        "before": (
            "I went down to the bottoms of the mountains; "
            "the earth with her bars was about me for ever."
        ),
        "after": (
            "Yet hast thou brought up my life from corruption, "
            "O LORD my God."
        ),
    },
    {
        "numeral": "iii",
        "ref": "Hosea 6:1 → 6:2",
        "tradition": "Prophetic — on the third day",
        "before": (
            "Come, and let us return unto the LORD: for he hath "
            "torn, and he will heal us; he hath smitten, and he "
            "will bind us up."
        ),
        "after": (
            "After two days will he revive us: in the third day "
            "he will raise us up, and we shall live in his sight."
        ),
    },
    {
        "numeral": "iv",
        "ref": "John 20:25 → 20:27",
        "tradition": "Apostolic — the wounded risen body",
        "before": (
            "Except I shall see in his hands the print of the "
            "nails, and put my finger into the print of the nails, "
            "and thrust my hand into his side, I will not believe."
        ),
        "after": (
            "Reach hither thy finger, and behold my hands; and "
            "reach hither thy hand, and thrust it into my side: "
            "and be not faithless, but believing."
        ),
        "wound_mark": True,
        "footnote": "the risen body is recognized by its wounds; resurrection preserves the marks.",
    },
    {
        "numeral": "v",
        "ref": "1 Corinthians 15:42 (a → b–43)",
        "tradition": "Apostolic — sown and raised",
        "before": (
            "It is sown in corruption; it is sown in dishonour; "
            "it is sown in weakness; it is sown a natural body."
        ),
        "after": (
            "It is raised in incorruption: it is raised in glory: "
            "it is raised in power: it is raised a spiritual body."
        ),
        "footnote": "ἐγείρω (egeirō) — to raise up; the verb of resurrection.",
    },
    {
        "numeral": "vi",
        "ref": "Revelation 21:4 → 21:5",
        "tradition": "Apocalyptic — all things new",
        "before": (
            "And there shall be no more death, neither sorrow, "
            "nor crying, neither shall there be any more pain: "
            "for the former things are passed away."
        ),
        "after": (
            "And he that sat upon the throne said, Behold, "
            "I make all things new."
        ),
        "consummation": True,
    },
]


# Breath vocabulary — Hebrew and Greek words for breath / spirit
# / rising that travel across the testaments. The ruach that
# breathes life into the dry bones is the same word as the
# pneuma the risen Christ breathes into his disciples (John
# 20:22); the verb anistēmi / egeirō becomes the noun anastasis,
# the New Testament's term for resurrection itself.
BREATH_VOCABULARY = [
    {
        "script": "רוּחַ",
        "lang": "he",
        "translit": "ruach",
        "gloss": "breath, wind, spirit",
        "note": "the breath that hovers over the waters in Genesis 1:2; the breath that animates the dry bones in Ezekiel 37; the breath returning.",
    },
    {
        "script": "נְשָׁמָה",
        "lang": "he",
        "translit": "neshamah",
        "gloss": "breath of life",
        "note": "the breath breathed into the man's nostrils in Genesis 2:7; what is given returns.",
    },
    {
        "script": "πνεῦμα",
        "lang": "el",
        "translit": "pneuma",
        "gloss": "breath, wind, spirit",
        "note": "the Greek equivalent of ruach; what the risen Christ breathes on his disciples in John 20:22 — the same act, the same word, returning.",
    },
    {
        "script": "ἀνάστασις",
        "lang": "el",
        "translit": "anastasis",
        "gloss": "resurrection — literally, “a standing-up-again”",
        "note": "the New Testament's primary term for the resurrection of the body; the rising back to one's feet.",
    },
    {
        "script": "ἐγείρω",
        "lang": "el",
        "translit": "egeirō",
        "gloss": "to raise up, to awaken",
        "note": "the verb behind the noun anastasis; used through the gospels and Paul for what the LORD does with the dead.",
    },
]


ARCHIVE_COMMENTARY = (
    "Resurrection in the biblical tradition is not the erasure "
    "of death but its transformation. The risen body in John 20 "
    "bears the wounds of the cross; the dry bones of Ezekiel "
    "are clothed with breath but remain bones; Paul speaks not "
    "of escape from corruption but of corruption raised in "
    "incorruption — the same body, the same flesh, the same "
    "person, now transfigured. The Hebrew ruach that breathes "
    "wind back into Israel is the same word as the pneuma the "
    "risen Christ breathes into his disciples. What returns is "
    "recognizable. What returns is altered. Renewal in this "
    "archive preserves what passed through death; the wounds "
    "remain."
)


ATLAS_OBJECT = {
    "id": "atlas:object:resurrection:bones-and-breath",
    "class": "resurrection-renewal",
    "siglum": "AO · 011",
    "civilizations": [
        "Hebrew Bible — exilic and prophetic restoration",
        "Wisdom-tradition emergence motifs",
        "Apostolic resurrection witness",
        "Pauline transformation theology",
        "Apocalyptic consummation",
    ],
    "traditions": [
        "Ezekielian valley of bones",
        "Jonah / Hosean prophetic emergence",
        "Gospel resurrection narrative",
        "Pauline sown-and-raised body",
        "Eschatological making-new",
    ],
    "anchorings": [
        {
            "ref": "Ezekiel 37:5–10",
            "citation": "bible::kjv::eze.37.10",
            "note": "the breath came into them, and they lived",
        },
        {
            "ref": "Jonah 2:6",
            "citation": "bible::kjv::jon.2.6",
            "note": "yet hast thou brought up my life from corruption",
        },
        {
            "ref": "Hosea 6:2",
            "citation": "bible::kjv::hos.6.2",
            "note": "in the third day he will raise us up",
        },
        {
            "ref": "John 20:25–27",
            "citation": "bible::kjv::jhn.20.27",
            "note": "behold my hands… thrust it into my side",
        },
        {
            "ref": "1 Corinthians 15:42–44",
            "citation": "bible::kjv::1co.15.42",
            "note": "it is sown in corruption; it is raised in incorruption",
        },
        {
            "ref": "Revelation 21:5",
            "citation": "bible::kjv::rev.21.5",
            "note": "behold, I make all things new",
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
    ],
}


RECORD = {
    "id": RECORD_ID,
    "kind": "resurrection-renewal",
    "title": "Bones Clothed With Breath — Resurrection and Renewal",
    "body": (
        "Six returns through rupture. In each, the silence is "
        "kept legible above the renewed text — dimmed, not "
        "erased. The wounds remain. The breath that hovered in "
        "Genesis 1 is the breath that animates the dry bones, "
        "and the breath that the risen Christ breathes on his "
        "disciples."
    ),
    "authority": "tertiary",
    "tradition": "Hebrew Bible & New Testament — resurrection / renewal tradition",
    "source_basis": (
        "Ezekiel 37; Jonah 2; Hosea 6; John 20; "
        "1 Corinthians 15; Revelation 21 (KJV)"
    ),
    "confidence": "Archive resurrection synthesis",
    "anchors": [
        {"target": "archive:passage:bible::kjv::eze.37.10"},
        {"target": "archive:passage:bible::kjv::jhn.20.27"},
        {"target": "archive:passage:bible::kjv::1co.15.42"},
        {"target": "archive:passage:bible::kjv::rev.21.5"},
    ],
    "return_moments": RETURN_MOMENTS,
    "breath_vocabulary": BREATH_VOCABULARY,
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
    print(f"  return moments: {len(RETURN_MOMENTS)}")
    for m in RETURN_MOMENTS:
        tag = []
        if m.get("wound_mark"):   tag.append("WOUND")
        if m.get("consummation"): tag.append("CONSUMMATION")
        tagstr = " · " + " · ".join(tag) if tag else ""
        print(f"    {m['numeral']:>4} · {m['ref']:<28} {m['tradition']}{tagstr}")
    print(f"  breath vocabulary terms: {len(BREATH_VOCABULARY)}")
    print(f"  declared anchorings:     {len(ATLAS_OBJECT['anchorings'])}")

    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with gzip.open(DATA_GZ, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"\nwrote {DATA.name} + {DATA_GZ.name}")


if __name__ == "__main__":
    main()
