"""Add AO · 003 — The Antediluvian Line (Adam → Noah).

The third Codex Object class — genealogical / lineage. Materially
distinct from AO · 001 (comparative cosmology) and AO · 002
(textual witness / transmission):

  AO · 001  Cosmological-motif        diagram + terminology +
                                      ANE parallels + synthesis.
  AO · 002  Translation-tradition     manuscript-witness slips
                                      with semantic lineage.
  AO · 003  Genealogical-lineage      descent register + temporal
                                      continuity strip + sacred
                                      interruption (Enoch).

The chamber rhythm is recursive and generational, not essay-like.
The reader consults a sacred descent record rather than reading
about one.

This script is idempotent: re-running replaces the AO · 003
record in place. Updates both bible_kjv.json and bible_kjv.json.gz.
"""
import gzip
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "bible_kjv.json"
DATA_GZ = ROOT / "data" / "bible_kjv.json.gz"


RECORD_ID = "gen5-antediluvian-line"


# Ten generations of the Sethite descent, Genesis 5. Hebrew forms
# follow the MT pointing; transliterations follow the SBL Hebrew
# convention. Ages preserved as the canonical numbers.
GENERATIONS_RAW = [
    {
        "name_en": "Adam",   "name_he": "אָדָם",       "translit": "ʾĀdām",
        "age_at_begat": 130, "lifespan": 930,
        "witness_ref": "Genesis 5:3–5",
        "special": None,
        "note": None,
    },
    {
        "name_en": "Seth",   "name_he": "שֵׁת",        "translit": "Shēt",
        "age_at_begat": 105, "lifespan": 912,
        "witness_ref": "Genesis 5:6–8",
        "special": None,
        "note": None,
    },
    {
        "name_en": "Enosh",  "name_he": "אֱנוֹשׁ",     "translit": "ʾĚnôsh",
        "age_at_begat": 90,  "lifespan": 905,
        "witness_ref": "Genesis 5:9–11",
        "special": None,
        "note": "Then began men to call upon the name of the LORD. (Gen 4:26)",
    },
    {
        "name_en": "Kenan",  "name_he": "קֵינָן",      "translit": "Qênān",
        "age_at_begat": 70,  "lifespan": 910,
        "witness_ref": "Genesis 5:12–14",
        "special": None,
        "note": None,
    },
    {
        "name_en": "Mahalalel", "name_he": "מַהֲלַלְאֵל", "translit": "Mahălalʾēl",
        "age_at_begat": 65,  "lifespan": 895,
        "witness_ref": "Genesis 5:15–17",
        "special": None,
        "note": None,
    },
    {
        "name_en": "Jared",  "name_he": "יֶרֶד",        "translit": "Yered",
        "age_at_begat": 162, "lifespan": 962,
        "witness_ref": "Genesis 5:18–20",
        "special": None,
        "note": None,
    },
    {
        "name_en": "Enoch",  "name_he": "חֲנוֹךְ",      "translit": "Ḥănôk",
        "age_at_begat": 65,  "lifespan": 365,
        "witness_ref": "Genesis 5:21–24",
        "special": "interruption",
        "note": "And Enoch walked with God: and he was not; for God took him.",
    },
    {
        "name_en": "Methuselah", "name_he": "מְתוּשֶׁלַח", "translit": "Mětûshelaḥ",
        "age_at_begat": 187, "lifespan": 969,
        "witness_ref": "Genesis 5:25–27",
        "special": None,
        "note": None,
    },
    {
        "name_en": "Lamech", "name_he": "לֶמֶךְ",       "translit": "Lemek",
        "age_at_begat": 182, "lifespan": 777,
        "witness_ref": "Genesis 5:28–31",
        "special": None,
        "note": "He shall comfort us concerning our work and toil of our hands. (Gen 5:29)",
    },
    {
        "name_en": "Noah",   "name_he": "נֹחַ",         "translit": "Nōaḥ",
        "age_at_begat": 500, "lifespan": 950,
        "witness_ref": "Genesis 5:32; 9:29",
        "special": None,
        "note": None,
    },
]


def _compute_chronology(gens):
    """Walk the descent and stamp each generation with its
    birth_year and death_year (Anno Mundi, from creation = 0).
    Returns the augmented list.
    """
    out = []
    birth = 0
    for g in gens:
        gg = dict(g)
        gg["birth_year"] = birth
        gg["death_year"] = birth + g["lifespan"]
        out.append(gg)
        # The next generation is born when this one reaches age_at_begat
        birth = birth + g["age_at_begat"]
    return out


GENERATIONS = _compute_chronology(GENERATIONS_RAW)


ARCHIVE_COMMENTARY = (
    "Genealogy in the Hebrew Bible is not a list of names attached "
    "to a story; it is the story’s structural memory. The Sethite "
    "line carries identity through ten generations, binding Adam "
    "to Noah by a single thread of named descent, then carrying "
    "Noah onward into the Table of Nations and, in later tradition, "
    "into Chronicles and the Gospel of Luke. To consult this record "
    "is to consult the archive’s commitment that a people is its "
    "own past — that covenant moves through ancestry the way a "
    "river moves through its bed. The single interruption at Enoch — "
    "‘he was not; for God took him’ — is the inscription, inside "
    "the rhythm of dying, of one man other than dying. The rhythm "
    "resumes after him without comment. The interruption is part "
    "of the form."
)


ATLAS_OBJECT = {
    "id": "atlas:object:lineage:antediluvian",
    "class": "genealogical-lineage",
    "siglum": "AO · 003",
    "civilizations": [
        "Hebrew Bible (Sethite tradition)",
        "Second-Temple Judaism",
        "Apostolic Christian genealogy",
    ],
    "traditions": [
        "Genesis Sethite line",
        "Chronicler retelling",
        "Lukan genealogy",
    ],
    "anchorings": [
        {
            "ref": "Genesis 5:1",
            "citation": "bible::kjv::gen.5.1",
            "note": "the book of the generations of Adam",
        },
        {
            "ref": "Genesis 10:1",
            "citation": "bible::kjv::gen.10.1",
            "note": "the descent continues — Noah’s sons, table of nations",
        },
        {
            "ref": "1 Chronicles 1:1–4",
            "citation": "bible::kjv::1ch.1.1",
            "note": "the lineage retold without narrative",
        },
        {
            "ref": "Luke 3:36–38",
            "citation": "bible::kjv::luk.3.38",
            "note": "the lineage as ancestry — ending ‘the son of Adam, the son of God’",
        },
    ],
    "linked": [
        "atlas:object:cosmology:ane-three-tier",
        "atlas:object:translation:firmament",
    ],
}


RECORD = {
    "id": RECORD_ID,
    "kind": "genealogy",
    "title": "The Antediluvian Line — Adam to Noah",
    "body": (
        "Ten generations between creation and the flood. The "
        "descent is sparse and exact: name, age at begetting, "
        "total years, and the closing rubric ‘and he died.’ The "
        "rhythm holds, and then once — at Enoch — it breaks."
    ),
    "authority": "tertiary",
    "tradition": "Hebrew Bible — Sethite genealogy",
    "source_basis": (
        "Genesis 5 (Masoretic Text); 1 Chronicles 1:1–4; Luke 3:36–38"
    ),
    "confidence": "Archive generational record",
    "anchors": [
        {"target": "archive:passage:bible::kjv::gen.5.1"},
        {"target": "archive:passage:bible::kjv::1ch.1.1"},
        {"target": "archive:passage:bible::kjv::luk.3.38"},
    ],
    "generations": GENERATIONS,
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
    print(f"  generations: {len(GENERATIONS)}")
    for g in GENERATIONS:
        spec = f" [{g['special']}]" if g['special'] else ""
        print(f"    {g['name_en']:<12} ({g['translit']:<12}) "
              f"AM {g['birth_year']:>4}–{g['death_year']:<4} "
              f"begat at {g['age_at_begat']:>3}, lived {g['lifespan']:>3}"
              + spec)

    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with gzip.open(DATA_GZ, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"\nwrote {DATA.name} + {DATA_GZ.name}")


if __name__ == "__main__":
    main()
