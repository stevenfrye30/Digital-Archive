"""Add AO · 002 — The Firmament Translation Tradition.

A textual witness / translation tradition object. Materially
distinct from AO · 001 (Ancient Hebrew Cosmology):

  AO · 001 — comparative cosmological reconstruction; diagram
             and Hebrew terminology and ANE parallels.

  AO · 002 — manuscriptal witness encounter; aligned excerpts
             from the Masoretic Hebrew, Septuagint Greek,
             Vulgate Latin, and KJV English, with a brief
             philological lineage from rāqîaʿ to firmament.

The two objects anchor on the same passage (Genesis 1:6) but
offer different intellectual textures. Their coexistence is the
point: Atlas can support distinct object ontologies inside one
codex atmosphere.

This script is idempotent: re-running replaces the AO · 002
record in place.

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


RECORD_ID = "gen1-firmament-translation-tradition"


WITNESS_FRAGMENTS = [
    {
        "tradition": "Hebrew · Masoretic Text",
        "witness": "BHS, Codex Leningradensis B19A",
        "date": "consonantal tradition pre-100 CE; pointed c. 1008 CE",
        "lang": "he",
        "script": "וַיֹּאמֶר אֱלֹהִים יְהִי רָקִיעַ בְּתוֹךְ הַמָּיִם",
        "term": "רָקִיעַ",
        "translit": "rāqîaʿ",
        "gloss": "And God said: Let there be a rāqîaʿ in the midst of the waters.",
    },
    {
        "tradition": "Greek · Septuagint (LXX)",
        "witness": "Rahlfs, Vaticanus B; Alexandrinus A",
        "date": "translated 3rd – 2nd c. BCE, Alexandria",
        "lang": "el",
        "script": "καὶ εἶπεν ὁ Θεός Γενηθήτω στερέωμα ἐν μέσῳ τοῦ ὕδατος",
        "term": "στερέωμα",
        "translit": "stereōma",
        "gloss": "And God said: Let a stereōma (solid frame) come to be in the midst of the water.",
    },
    {
        "tradition": "Latin · Vulgate",
        "witness": "Stuttgartensia (Weber – Gryson)",
        "date": "translated by Jerome, c. 405 CE",
        "lang": "la",
        "script": "dixit quoque Deus fiat firmamentum in medio aquarum",
        "term": "firmamentum",
        "translit": "firmamentum",
        "gloss": "And God also said: Let firmamentum (a firm support) come to be in the midst of the waters.",
    },
    {
        "tradition": "English · King James Bible",
        "witness": "1611 edition, Robert Barker, London",
        "date": "1611",
        "lang": "en",
        "script": "And God said, Let there be a firmament in the midst of the waters.",
        "term": "firmament",
        "translit": "firmament",
        "gloss": "the Latin word inherited, anglicised.",
    },
]


SEMANTIC_SHIFT_NOTES = [
    {
        "head": "rāqîaʿ — the hammered surface",
        "body": (
            "The Hebrew verbal root r-q-ʿ describes the action of "
            "beating metal flat. The noun rāqîaʿ designates the "
            "resulting hammered surface. The lexical center of "
            "gravity is the act of forming, not the substance formed."
        ),
    },
    {
        "head": "στερέωμα — the solid structure",
        "body": (
            "The Septuagint translators reach for στερέωμα, a noun "
            "from στερεός (solid, firm). The verb of hammering is "
            "set aside; the noun of solidity takes its place. "
            "Hellenistic medical writers use στερέωμα for a body's "
            "solid frame."
        ),
    },
    {
        "head": "firmamentum — a firm support",
        "body": (
            "Jerome renders the Greek with firmamentum, from firmus, "
            "preserving the substantive emphasis. In classical Latin, "
            "firmamentum is a pillar or stay — a thing that holds."
        ),
    },
    {
        "head": "firmament — the Latin word inherited",
        "body": (
            "Wycliffe (1380s) carries firmamentum into English as "
            "firmament. The word travels through Tyndale (1530) and "
            "the Geneva Bible (1560) to the KJV (1611), increasingly "
            "detached from any living lexical root. Modern translations "
            "diverge: ‘expanse’ (NIV, NASB, ESV), ‘vault’ (NRSV), "
            "‘dome’ (NJPS) — each chooses to soften or preserve the "
            "older solidity."
        ),
    },
]


LINEAGE_STOPS = [
    {
        "tradition": "Hebrew (Masoretic)",
        "term": "רָקִיעַ",
        "translit": "rāqîaʿ",
        "date": "consonantal: pre-100 CE",
        "lang": "he",
    },
    {
        "tradition": "Greek (LXX)",
        "term": "στερέωμα",
        "translit": "stereōma",
        "date": "c. 3rd – 2nd c. BCE",
        "lang": "el",
    },
    {
        "tradition": "Latin (Vulgate)",
        "term": "firmamentum",
        "translit": "firmamentum",
        "date": "c. 405 CE",
        "lang": "la",
    },
    {
        "tradition": "English (KJV)",
        "term": "firmament",
        "translit": "firmament",
        "date": "1611",
        "lang": "en",
    },
]


LINEAGE_TRANSITIONS = [
    "Alexandrian Jewish translators · 3rd – 2nd c. BCE",
    "Jerome, working from Hebrew and Greek · c. 405 CE",
    "Wycliffe (1380s) → Tyndale (1530) → Geneva (1560) → KJV (1611)",
]


ARCHIVE_COMMENTARY = (
    "The arc from rāqîaʿ to firmament is not loss but lineage. A "
    "Hebrew verbal noun describing a process — hammering — became a "
    "Greek noun denoting a substance — solidity — and the Latin and "
    "English traditions inherited that substantive emphasis. The "
    "cosmological picture remains roughly the same across the chain; "
    "what shifts is the semantic centre of gravity, from action to "
    "architecture. Translation choices, repeated over centuries, "
    "shape the later cosmological imagination as quietly and "
    "decisively as any theological decision."
)


ATLAS_OBJECT = {
    "id": "atlas:object:translation:firmament",
    "class": "translation-tradition",
    "siglum": "AO · 002",
    "civilizations": [
        "Second-Temple Judaism",
        "Hellenistic Mediterranean",
        "Latin Christendom",
        "Reformation England",
    ],
    "traditions": [
        "Masoretic Hebrew transmission",
        "Septuagint translation",
        "Vulgate translation",
        "English Reformation translation",
    ],
    "anchorings": [
        {
            "ref": "Genesis 1:6",
            "citation": "bible::kjv::gen.1.6",
            "note": "first installation of the firmament",
        },
        {
            "ref": "Genesis 1:7",
            "citation": "bible::kjv::gen.1.7",
            "note": "the waters divided by the firmament",
        },
        {
            "ref": "Genesis 1:8",
            "citation": "bible::kjv::gen.1.8",
            "note": "the firmament named — heavens",
        },
        {
            "ref": "Ezekiel 1:22",
            "citation": "bible::kjv::eze.1.22",
            "note": "a firmament above the heads of the living creatures",
        },
        {
            "ref": "Psalm 148:4",
            "citation": "bible::kjv::psa.148.4",
            "note": "ye waters that be above the heavens — praise",
        },
    ],
    "linked": [
        "atlas:object:cosmology:ane-three-tier",
    ],
}


RECORD = {
    "id": RECORD_ID,
    "kind": "translation-tradition",
    "title": "The Firmament Translation Tradition",
    "body": (
        "From the Hebrew rāqîaʿ to the English firmament, a single "
        "passage carries a textual lineage four traditions long. The "
        "witnesses below stand alongside one another so the lineage "
        "may be read as itself."
    ),
    "authority": "tertiary",
    "tradition": "Philological — textual witness collation",
    "source_basis": (
        "Masoretic Text (BHS, Leningradensis); Septuagint (Rahlfs, "
        "Vaticanus and Alexandrinus); Vulgate (Stuttgartensia, "
        "Weber – Gryson); KJV 1611"
    ),
    "confidence": "Archive philological synthesis",
    "anchors": [
        {"target": "archive:passage:bible::kjv::gen.1.6"},
        {"target": "archive:passage:bible::kjv::eze.1.22"},
        {"target": "archive:passage:bible::kjv::psa.148.4"},
    ],
    "witness_fragments": WITNESS_FRAGMENTS,
    "semantic_shift": SEMANTIC_SHIFT_NOTES,
    "lineage_stops": LINEAGE_STOPS,
    "lineage_transitions": LINEAGE_TRANSITIONS,
    "archive_commentary": ARCHIVE_COMMENTARY,
    "atlas_object": ATLAS_OBJECT,
}


def main():
    with DATA.open(encoding="utf-8") as f:
        data = json.load(f)
    records = data.get("genealogy", [])
    # Idempotent: replace in place if present, otherwise append.
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
    print(f"  siglum:   {ATLAS_OBJECT['siglum']}")
    print(f"  class:    {ATLAS_OBJECT['class']}")
    print(f"  anchors:  {len(RECORD['anchors'])}")
    for a in RECORD["anchors"]:
        print(f"    - {a['target']}")
    print(f"  witnesses:           {len(WITNESS_FRAGMENTS)}")
    print(f"  semantic-shift notes:{len(SEMANTIC_SHIFT_NOTES)}")
    print(f"  lineage stops:       {len(LINEAGE_STOPS)}")

    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with gzip.open(DATA_GZ, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"\nwrote {DATA.name} + {DATA_GZ.name}")


if __name__ == "__main__":
    main()
