"""Add AO · 009 — How Long, O LORD? (Lament Before Heaven).

The ninth Atlas Object class — lament-structure. Materially
distinct from the prior eight:

  AO · 001  cosmological-motif      diagram + ANE parallels.
  AO · 002  translation-tradition   manuscript witness slips.
  AO · 003  genealogical-lineage    descent register + stemma.
  AO · 004  sacred-time             sevenfold rhythm.
  AO · 005  symbolic-motif          vertical axis-mundi.
  AO · 006  covenant-formula        bipartite recurrence.
  AO · 007  wisdom-saying           sparse aphorisms + compression.
  AO · 008  revelatory-vision       threshold → unveiled pairs.
  AO · 009  lament-structure        cry sequence held by a broken
                                    vertical axis of address; the
                                    Lamentations acrostic carrying
                                    structural endurance under
                                    rupture; refrains that recur
                                    because resolution has not yet
                                    come.

The chamber's form is the form of lament itself: structured
endurance under rupture. The cries return because they have
not been answered.

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

RECORD_ID = "psa13-lament-cry"


# Six canonical lament cries, in canonical sequence. Each carries
# a numeral, a reference, a tradition label, the cry text quoted
# from the KJV, and (for Lamentations 3) the triadic acrostic
# structure preserved as three Hebrew-letter triplets.
LAMENT_CRIES = [
    {
        "numeral": "i",
        "ref": "Psalm 13:1–2",
        "tradition": "Davidic — the cry of How long",
        "text": (
            "How long wilt thou forget me, O LORD? for ever? "
            "how long wilt thou hide thy face from me? "
            "How long shall I take counsel in my soul, having "
            "sorrow in my heart daily?"
        ),
    },
    {
        "numeral": "ii",
        "ref": "Psalm 22:1–2",
        "tradition": "Davidic — the cry of abandonment",
        "text": (
            "My God, my God, why hast thou forsaken me? why art "
            "thou so far from helping me, and from the words of "
            "my roaring? O my God, I cry in the daytime, but "
            "thou hearest not; and in the night season, and am "
            "not silent."
        ),
    },
    {
        "numeral": "iii",
        "ref": "Psalm 88:13, 18",
        "tradition": "Korahite — the psalm that does not turn",
        "text": (
            "But unto thee have I cried, O LORD; and in the "
            "morning shall my prayer prevent thee… Lover and "
            "friend hast thou put far from me, and mine "
            "acquaintance into darkness."
        ),
        "unresolved_note": "the only psalm of lament that does not turn — the form holds without closing.",
    },
    {
        "numeral": "iv",
        "ref": "Lamentations 3:1–9",
        "tradition": "Exilic lament — the acrostic that holds",
        "acrostic": [
            {
                "letter_he": "א",
                "letter_translit": "ʾaleph",
                "lines": [
                    "I am the man that hath seen affliction by the rod of his wrath.",
                    "He hath led me, and brought me into darkness, but not into light.",
                    "Surely against me is he turned; he turneth his hand against me all the day.",
                ],
            },
            {
                "letter_he": "ב",
                "letter_translit": "bet",
                "lines": [
                    "My flesh and my skin hath he made old; he hath broken my bones.",
                    "He hath builded against me, and compassed me with gall and travail.",
                    "He hath set me in dark places, as they that be dead of old.",
                ],
            },
            {
                "letter_he": "ג",
                "letter_translit": "gimel",
                "lines": [
                    "He hath hedged me about, that I cannot get out: he hath made my chain heavy.",
                    "Also when I cry and shout, he shutteth out my prayer.",
                    "He hath enclosed my ways with hewn stone, he hath made my crooked paths.",
                ],
            },
        ],
        "acrostic_note": "the alphabet itself is the form holding what would otherwise dissolve.",
    },
    {
        "numeral": "v",
        "ref": "Job 3:3, 11",
        "tradition": "Wisdom lament — the curse on the day",
        "text": (
            "Let the day perish wherein I was born, and the "
            "night in which it was said, There is a man child "
            "conceived… Why died I not from the womb? why did I "
            "not give up the ghost when I came out of the belly?"
        ),
    },
    {
        "numeral": "vi",
        "ref": "Habakkuk 1:2–4",
        "tradition": "Prophetic lament — the cry not heard",
        "text": (
            "O LORD, how long shall I cry, and thou wilt not "
            "hear! even cry out unto thee of violence, and thou "
            "wilt not save! Why dost thou shew me iniquity, and "
            "cause me to behold grievance?… Therefore the law is "
            "slacked, and judgment doth never go forth."
        ),
    },
]


# Echo refrains — short recurring phrases that travel across
# the canon's lament register. The voice persists.
ECHO_REFRAINS = [
    {
        "text": "How long, O LORD?",
        "ref": "Psalm 13:1 · Psalm 6:3 · Habakkuk 1:2",
    },
    {
        "text": "My God, my God, why hast thou forsaken me?",
        "ref": "Psalm 22:1 · Matthew 27:46",
    },
    {
        "text": "Out of the depths have I cried unto thee, O LORD.",
        "ref": "Psalm 130:1",
    },
    {
        "text": "My tears have been my meat day and night.",
        "ref": "Psalm 42:3",
    },
    {
        "text": "Remember, O LORD, what is come upon us.",
        "ref": "Lamentations 5:1",
    },
    {
        "text": "Though he slay me, yet will I trust in him.",
        "ref": "Job 13:15",
    },
]


ARCHIVE_COMMENTARY = (
    "Lament in the biblical tradition is not the absence of "
    "address but its persistence under rupture. The psalmist "
    "who cries How long, O LORD? has not stopped speaking to "
    "the LORD — the cry itself is the address. The "
    "Lamentations acrostic is the form's argument with itself: "
    "the alphabet structure carries the grief that would "
    "dissolve it, holding the cry across twenty-two letters of "
    "ordered speech. Psalm 88 ends in darkness without turning. "
    "Job curses the day of his birth. Habakkuk asks why his cry "
    "is not heard. These speeches are not the failure of "
    "covenant but the form covenant takes when the world does "
    "not yet match the promise. Lament is what fidelity sounds "
    "like under pressure."
)


ATLAS_OBJECT = {
    "id": "atlas:object:lament:how-long",
    "class": "lament-structure",
    "siglum": "AO · 009",
    "civilizations": [
        "Hebrew Bible — psalmic lament tradition",
        "Exilic lament (Lamentations)",
        "Wisdom-tradition lament (Job)",
        "Prophetic lament (Habakkuk, Jeremiah)",
        "Gospel passion echoes",
    ],
    "traditions": [
        "Davidic psalmody",
        "Korahite psalmody",
        "Exilic acrostic lament",
        "Joban wisdom-lament",
        "Prophetic complaint",
    ],
    "anchorings": [
        {
            "ref": "Psalm 13:1–2",
            "citation": "bible::kjv::psa.13.1",
            "note": "how long, O LORD",
        },
        {
            "ref": "Psalm 22:1",
            "citation": "bible::kjv::psa.22.1",
            "note": "why hast thou forsaken me",
        },
        {
            "ref": "Psalm 88:18",
            "citation": "bible::kjv::psa.88.18",
            "note": "lover and friend hast thou put far from me",
        },
        {
            "ref": "Lamentations 3:1–9",
            "citation": "bible::kjv::lam.3.1",
            "note": "I am the man that hath seen affliction",
        },
        {
            "ref": "Job 3:3",
            "citation": "bible::kjv::job.3.3",
            "note": "let the day perish wherein I was born",
        },
        {
            "ref": "Habakkuk 1:2",
            "citation": "bible::kjv::hab.1.2",
            "note": "O LORD, how long shall I cry, and thou wilt not hear",
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
    ],
}


RECORD = {
    "id": RECORD_ID,
    "kind": "lament-structure",
    "title": "How Long, O LORD? — Lament Before Heaven",
    "body": (
        "Six cries return across the canon. Each one is the same "
        "address under different ruptures. The Lamentations "
        "acrostic carries the grief through the alphabet itself; "
        "Psalm 88 ends in darkness without turning. The chamber "
        "does not solve the cries — it holds them."
    ),
    "authority": "tertiary",
    "tradition": "Hebrew Bible — lament tradition",
    "source_basis": (
        "Psalm 13; Psalm 22; Psalm 88; Lamentations 3; "
        "Job 3; Habakkuk 1 (KJV)"
    ),
    "confidence": "Archive lament synthesis",
    "anchors": [
        {"target": "archive:passage:bible::kjv::psa.13.1"},
        {"target": "archive:passage:bible::kjv::psa.22.1"},
        {"target": "archive:passage:bible::kjv::lam.3.1"},
        {"target": "archive:passage:bible::kjv::job.3.3"},
    ],
    "lament_cries": LAMENT_CRIES,
    "echo_refrains": ECHO_REFRAINS,
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
    print(f"  lament cries: {len(LAMENT_CRIES)}")
    for c in LAMENT_CRIES:
        ac = " · ACROSTIC" if c.get("acrostic") else ""
        un = " · UNRESOLVED" if c.get("unresolved_note") else ""
        print(f"    {c['numeral']:>4} · {c['ref']:<24} {c['tradition']}{ac}{un}")
    print(f"  echo refrains: {len(ECHO_REFRAINS)}")
    print(f"  declared anchorings: {len(ATLAS_OBJECT['anchorings'])}")

    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with gzip.open(DATA_GZ, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"\nwrote {DATA.name} + {DATA_GZ.name}")


if __name__ == "__main__":
    main()
