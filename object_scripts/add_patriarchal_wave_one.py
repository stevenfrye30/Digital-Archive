"""Wave One — Patriarchal Genesis atmosphere layer.

Adds six records to bible_kjv.json, exactly as specified in
GENESIS_WAVE_ONE_PLAN.md. No new Codex Objects, no new chamber
classes, no new metadata fields. Each record uses the existing
generic fallback renderer (provenance header + verse + title +
body).

Editorial discipline:
  · Tertiary architecture records: 2-3 paragraphs, inscription-
    shaped, place-centred.
  · Secondary commentary records: 3-5 paragraphs, narrative-
    shaped, restrained.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "bible_kjv.json"

DATE = "2026-05-20"
AUTHOR = "archive:steward:steve"
LAYER = "editorial"
LIFECYCLE = "provisional"


def record(
    *,
    id_,
    kind,
    title,
    verse,
    body,
    authority,
    tradition,
    source_basis,
    confidence,
):
    return {
        "id": id_,
        "kind": kind,
        "title": title,
        "anchors": [
            {"target": f"archive:passage:bible::kjv::{verse}"}
        ],
        "body": body,
        "provenance": {
            "layer": LAYER,
            "author": AUTHOR,
            "date": DATE,
            "lifecycle_state": LIFECYCLE,
        },
        "authority": authority,
        "tradition": tradition,
        "source_basis": source_basis,
        "confidence": confidence,
    }


# ── Tertiary architecture: the three sacred-site origins ────

altar_at_shechem = record(
    id_="gen12-altar-at-shechem",
    kind="architecture",
    title="Altar at Shechem — the first patriarchal stone",
    verse="gen.12.7",
    body=(
        "Abram, newly arrived in the land promised to him, "
        "builds the first patriarchal altar beside the oak of "
        "Moreh in Shechem. The Hebrew מִזְבֵּחַ (mizbeach, "
        "'place of slaughter / place of sacrifice') is named "
        "here for the first time in scripture.\n\n"
        "The act establishes a rhythm. A patriarch enters a "
        "place, the LORD appears or speaks, an altar is "
        "raised, and the journey continues. Shechem will be "
        "revisited by Jacob (Gen 33:18-20), and the same "
        "ground will hold Joseph's bones at the close of "
        "Joshua (24:32). The altar is built and abandoned; "
        "the place is named and remembered.\n\n"
        "The first stone in the patriarchal landscape."
    ),
    authority="tertiary",
    tradition="Patriarchal sacred-site rhythm — Hebrew Bible",
    source_basis="Gen 12:6-7; cf. Gen 33:18-20; Josh 24:32",
    confidence="Archive editorial summary of primary text",
)

beersheba_well_oath = record(
    id_="gen21-beersheba-well-oath",
    kind="architecture",
    title="The well at Beersheba — water and oath",
    verse="gen.21.31",
    body=(
        "Abraham and Abimelech swear an oath; seven ewe lambs "
        "are set apart as witness; and the place is named "
        "Beʾer Sheva — בְּאֵר שֶׁבַע, 'well of oath / well of "
        "seven'. The Hebrew preserves both senses, because "
        "the oath is the seven.\n\n"
        "Water and oath bind together here. The patriarchs "
        "claim ground not by conquest but by treaty at a "
        "well: the well that is dug and the word that is "
        "sworn become a single act of inhabitation. Isaac "
        "will re-dig his father's wells at this same site "
        "(Gen 26:18-33); centuries later the southern "
        "boundary of Israel is still named from Dan to "
        "Beersheba.\n\n"
        "A well, an oath, a name. The patriarchal memory-"
        "site begins here."
    ),
    authority="tertiary",
    tradition="Patriarchal sacred-site rhythm — Hebrew Bible",
    source_basis="Gen 21:22-34; cf. Gen 26:18-33; Judg 20:1",
    confidence="Archive editorial summary of primary text",
)

bethel_pillar = record(
    id_="gen28-bethel-pillar",
    kind="architecture",
    title="The pillar at Bethel — the first standing-stone",
    verse="gen.28.18",
    body=(
        "Jacob, waking from the ladder-dream, takes the stone "
        "he had set under his head and sets it up as a "
        "maṣṣebah (מַצֵּבָה, 'standing-stone / pillar'), "
        "pouring oil upon its top. The place he had called "
        "Luz he renames Bethel — 'house of God'.\n\n"
        "The pillar is a different kind of mark than an "
        "altar. An altar is for sacrifice; a pillar is for "
        "memory. Jacob does not slaughter here; he raises a "
        "stone and continues his journey. Decades later he "
        "returns to this same place (Gen 35:1-7), and the "
        "pillar still stands.\n\n"
        "The first patriarchal pillar; the first "
        "sanctification of an ordinary stone."
    ),
    authority="tertiary",
    tradition="Patriarchal sacred-site rhythm — Hebrew Bible",
    source_basis="Gen 28:10-22; cf. Gen 35:1-15",
    confidence="Archive editorial summary of primary text",
)


# ── Secondary commentary: the narrative-arc bookends + the vision

lekh_lekha_call = record(
    id_="gen12-lekh-lekha-call",
    kind="commentary",
    title="Lekh lekha — the call to go",
    verse="gen.12.1",
    body=(
        "The first word spoken to Abram is a command of "
        "departure: lekh lekha (לֶךְ לְךָ) — 'go for yourself', "
        "'go to yourself', 'go from yourself'. The Hebrew "
        "doubles the verb upon its own pronoun and resists a "
        "single English equivalent. The going is also a "
        "turning toward; the leaving is also a finding.\n\n"
        "What follows is a three-fold promise — land, seed, "
        "blessing — given before any altar, before any "
        "covenant ceremony, before any sign. Abram is called "
        "by name; the call is purely verbal; the response, "
        "when it comes, is only motion. He leaves Haran "
        "without speaking.\n\n"
        "Eleven chapters of primeval history end with a city "
        "being dispersed (Babel) and a genealogy crossing "
        "into Mesopotamia (Terah's house). In the twelfth "
        "chapter, the narrative narrows to a single household "
        "and a single voice. From this point on, Genesis is "
        "the story of a family moving across named ground.\n\n"
        "The going-out begun here will recur — Israel out of "
        "Egypt, Israel out of Babylon, the Son out from the "
        "Father — and the codex will encounter the shape of "
        "lekh lekha many times again. Here it is first "
        "spoken."
    ),
    authority="secondary",
    tradition="Patriarchal narrative — Hebrew Bible",
    source_basis="Gen 12:1-3; cf. Heb 11:8; Acts 7:2-4",
    confidence="Archive editorial narrative-theological gloss",
)

jacob_ladder = record(
    id_="gen28-jacob-ladder",
    kind="commentary",
    title="Jacob's ladder — the patriarchal vision",
    verse="gen.28.12",
    body=(
        "Fleeing from his brother, Jacob lies down in 'a "
        "certain place' — the Hebrew is deliberately "
        "unspecified — and dreams a sullam (סֻלָּם, 'ladder' "
        "or 'ramp / stairway') set up on the earth with its "
        "top reaching to heaven. Angels of God ascend and "
        "descend upon it; the LORD stands above it and "
        "renews to Jacob the promise made to Abraham.\n\n"
        "The patriarchal vision differs from the cosmic "
        "visionary disclosures later given to Isaiah, "
        "Ezekiel, Daniel, John. There is no enthroned "
        "figure, no rotating wheels, no harvest of seals. "
        "There is only a stairway and the moving of angels "
        "— and the One who speaks is heard, not seen.\n\n"
        "The dream is embodied at a place. Jacob wakes and "
        "names the ground beneath him: 'this is none other "
        "than the house of God, and this is the gate of "
        "heaven'. The vision does not lift him into another "
        "world; it discloses that the ground he is already "
        "standing on is sacred. The patriarchal register of "
        "vision is precisely this — heaven touched in "
        "passing, at a particular stone, in a particular "
        "night, by a particular man on a journey.\n\n"
        "The next morning Jacob raises a pillar there and "
        "continues his flight. The vision has not ended his "
        "travelling; it has named one place along it."
    ),
    authority="secondary",
    tradition="Patriarchal narrative — Hebrew Bible",
    source_basis="Gen 28:10-22; cf. John 1:51",
    confidence="Archive editorial narrative-theological gloss",
)

descent_into_egypt = record(
    id_="gen46-descent-into-egypt",
    kind="commentary",
    title="The going-down into Egypt",
    verse="gen.46.3",
    body=(
        "On the road to Egypt, at Beersheba — the same well "
        "where Abraham had sworn and Isaac had dug — Jacob "
        "receives a night vision and is told: I will go down "
        "with thee into Egypt. The verb yarad (יָרַד, 'to go "
        "down / descend') is one of the most theologically "
        "loaded movements in the Hebrew Bible.\n\n"
        "Genesis has been a long going-out. Abram was called "
        "out of Haran; Isaac was sent to the land; Jacob "
        "travelled to Paddan-aram and back. The going-down "
        "into Egypt reverses that motion. The seventy souls "
        "of the house of Jacob yarad — they descend — and "
        "Joseph, who had already been brought down by his "
        "brothers, is the one waiting to receive them.\n\n"
        "The descent is not punitive. It is preservation. "
        "The land of promise will not feed them; the foreign "
        "land will. But the shape of yarad has been "
        "inscribed, and its inverse — the going-up, the "
        "aliyah — is already implicit. Joseph at his death "
        "will swear his brothers to carry his bones up out "
        "of Egypt (Gen 50:25).\n\n"
        "The patriarchal narrative's closing geography: a "
        "journey that began as lekh lekha (go forth) ends "
        "as yarad (go down). Genesis closes with a family "
        "safe but displaced; the codex marks the "
        "displacement here and lets the silence carry the "
        "rest."
    ),
    authority="secondary",
    tradition="Patriarchal narrative — Hebrew Bible",
    source_basis="Gen 46:1-7; cf. Gen 50:24-25; Exod 1:1-7",
    confidence="Archive editorial narrative-theological gloss",
)


WAVE_ONE = [
    altar_at_shechem,        # gen.12.7   tertiary architecture
    beersheba_well_oath,     # gen.21.31  tertiary architecture
    bethel_pillar,           # gen.28.18  tertiary architecture
    lekh_lekha_call,         # gen.12.1   secondary commentary
    jacob_ladder,            # gen.28.12  secondary commentary
    descent_into_egypt,      # gen.46.3   secondary commentary
]


def main():
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {r["id"] for r in data["genealogy"]}
    added = []
    for rec in WAVE_ONE:
        if rec["id"] in existing_ids:
            print(f"SKIP (already present): {rec['id']}")
            continue
        data["genealogy"].append(rec)
        added.append(rec["id"])
        print(f"ADD: {rec['id']:<32} → {rec['anchors'][0]['target'].split('::')[-1]}")

    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print()
    print(f"Total records in genealogy: {len(data['genealogy'])}")
    print(f"Added this run: {len(added)}")
    if added:
        for a in added:
            print(f"  · {a}")


if __name__ == "__main__":
    main()
