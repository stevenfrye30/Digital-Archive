"""Wave Two — Abrahamic emergence arc (Genesis 12-15).

Adds four records to bible_kjv.json:

  gen.12.5   — Patriarchal journey-map (secondary, kind=map)
  gen.14.18  — Melchizedek                (secondary commentary)
  gen.15.18  — Covenant of pieces         (secondary commentary)
  gen.15.6   — Righteousness credited     (tertiary linguistic)

gen.12.1 (lekh lekha) is NOT in this script — it was added in
Wave One and the existing record satisfies the Wave Two spec.

Editorial discipline (per GENESIS_EXPANDED_COVERAGE_PLAN.md):
  · Secondary records render 3-4 paragraphs of restrained,
    narrative-shaped commentary.
  · Tertiary record renders 2 paragraphs, linguistic-shaped.
  · The map plate is a manuscript itinerary, not a UI map.
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


# ── 1. gen.12.5 — Patriarchal journey map (secondary, map) ──
#
# A manuscript itinerary, not a UI map. Body uses an ASCII-style
# arrow chain to evoke the route, followed by restrained
# commentary on what the route is and what it means.

patriarchal_journey_map = record(
    id_="gen12-patriarchal-journey-map",
    kind="map",
    title="Manuscript itinerary — the patriarchal road into the land",
    verse="gen.12.5",
    body=(
        "Ur of the Chaldeans  →  Haran  →  Shechem  →  Bethel  →"
        "\n"
        "the Negeb  →  Egypt  →  return  →  Hebron\n\n"
        "A line drawn across three peoples and two great rivers. "
        "Abram enters Mesopotamia at its upper bend (Haran), "
        "crosses to the Levantine highlands by way of Shechem, "
        "descends to Egypt under the famine, and returns to the "
        "oak of Mamre at Hebron.\n\n"
        "The land is sworn while the patriarch walks across it; "
        "the journey is itself the covenant. Distances are "
        "approximate, the road is unmarked, and the route "
        "survives only in the canon's own naming of places. The "
        "first map of the patriarchal narrative is preserved as "
        "toponyms rather than as lines."
    ),
    authority="secondary",
    tradition="Patriarchal geography — Hebrew Bible toponymy",
    source_basis="Gen 11:31; 12:4-9; 13:1-3, 18; cf. Acts 7:2-5",
    confidence="Archive editorial itinerary; toponyms canonical",
)


# ── 2. gen.14.18 — Melchizedek (secondary commentary) ──

melchizedek = record(
    id_="gen14-melchizedek",
    kind="commentary",
    title="Melchizedek — priest-king of Salem",
    verse="gen.14.18",
    body=(
        "The war narrative that fills Genesis 14 is interrupted "
        "at verse 18 by a figure who arrives without genealogy, "
        "without ancestry, and without parallel: Melchizedek, "
        "king of Salem, priest of God Most High (kohen le-El "
        "Elyon). He brings out bread and wine. He blesses Abram. "
        "Abram gives him a tithe of everything. Then he "
        "disappears from the chapter as suddenly as he "
        "entered.\n\n"
        "The episode resists every category Genesis has so far "
        "built. The patriarchal narratives are tracing a line — "
        "Abram, Isaac, Jacob — and into that line steps a "
        "priest-king from outside it, with an authority Abram "
        "acknowledges by tithe. His name is rendered 'king of "
        "righteousness' (melek + tsedeq); his city Salem is read "
        "as Jerusalem in later Jewish tradition; Psalm 110 will "
        "name a coming priesthood 'after the order of "
        "Melchizedek.'\n\n"
        "Hebrews 7 will eventually turn this episode into an "
        "entire doctrine of priesthood — without father, without "
        "mother, without genealogy, having neither beginning of "
        "days nor end of life. But all of that is yet to come. "
        "In Genesis 14, the figure simply appears, blesses, "
        "receives the tithe, and is gone. The patriarchal "
        "narrative's first priestly encounter happens with a "
        "priest not of Abram's line."
    ),
    authority="secondary",
    tradition="Priesthood tradition — Hebrew Bible, Second-Temple, Apostolic",
    source_basis="Gen 14:18-20; cf. Ps 110:4; Heb 5:6, 7:1-17",
    confidence="Archive editorial narrative-theological gloss",
)


# ── 3. gen.15.18 — Covenant of pieces (secondary commentary) ──

covenant_of_pieces = record(
    id_="gen15-covenant-of-pieces",
    kind="commentary",
    title="Covenant of pieces — the cutting of covenant",
    verse="gen.15.18",
    body=(
        "After the war narrative, Abram receives a vision in the "
        "night. The LORD takes him outside and tells him to look "
        "at the stars: so shall your descendants be. The chapter "
        "then turns to a covenant ritual unlike anything that "
        "has come before.\n\n"
        "Abram is told to bring a heifer, a goat, a ram, a "
        "turtledove, a young pigeon. He divides the animals down "
        "the middle and lays the halves opposite one another. "
        "The afternoon passes; he drives birds of prey away from "
        "the carcasses. At sunset a deep sleep (tardemah — the "
        "same word used for Adam in Gen 2:21) falls upon him, "
        "and a dread of great darkness. The LORD speaks: four "
        "hundred years of affliction, deliverance, return to "
        "this land.\n\n"
        "Then night closes and a smoking firepot (tannur ashan) "
        "and a flaming torch pass between the divided pieces. "
        "This is the cut covenant (karat berit) in its primal "
        "form: the parties of a covenant pass between the "
        "divided animals, invoking on themselves the fate of the "
        "animals should the covenant be broken. Here only one "
        "party passes — the LORD alone, in fire and smoke. The "
        "covenant is one-sided, unconditional, sworn against "
        "God's own being. The pieces of Genesis 15 prefigure the "
        "cut of every later covenant in scripture."
    ),
    authority="secondary",
    tradition="Covenant tradition — Hebrew Bible patriarchal narratives",
    source_basis="Gen 15:1-21; cf. Jer 34:18-20; Heb 6:13-18",
    confidence="Archive editorial narrative-theological gloss",
)


# ── 4. gen.15.6 — Righteousness credited (tertiary linguistic) ──
#
# Two paragraphs. The Genesis setting first, then the briefest
# nod to Paul/James reception. No Pauline theology built out.

righteousness_credited = record(
    id_="gen15-righteousness-credited",
    kind="linguistic",
    title="And he counted it to him for righteousness",
    verse="gen.15.6",
    body=(
        "'And he believed in the LORD; and he counted it to him "
        "for righteousness.' The Hebrew is compressed: ve-heʾemin "
        "ba-YHWH va-yachshe-veha lo tsedaqah (וְהֶאֱמִן בַּיהוָה "
        "וַיַּחְשְׁבֶהָ לּוֹ צְדָקָה). The verb chashav (חָשַׁב, "
        "'to reckon, account, credit') is mercantile-judicial in "
        "register — a value entered in a ledger.\n\n"
        "The verse will be carried forward by Paul (Rom 4) and "
        "James (Jas 2) into two long arguments about what the "
        "verse counts as faith and what it counts as "
        "righteousness. In Genesis itself, however, the verse "
        "passes quietly: a single sentence inside the covenant-"
        "of-pieces narrative, naming Abram's response as the "
        "basis on which the LORD reckons him righteous. The "
        "later reception is enormous; the Genesis setting is "
        "brief."
    ),
    authority="tertiary",
    tradition="Patriarchal narrative — Hebrew Bible",
    source_basis="Gen 15:6; cf. Rom 4:3-22; Jas 2:23",
    confidence="Archive editorial linguistic gloss",
)


WAVE_TWO = [
    patriarchal_journey_map,   # gen.12.5   secondary  map
    melchizedek,               # gen.14.18  secondary  commentary
    covenant_of_pieces,        # gen.15.18  secondary  commentary
    righteousness_credited,    # gen.15.6   tertiary   linguistic
]


def main():
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {r["id"] for r in data["genealogy"]}
    added = []
    for rec in WAVE_TWO:
        if rec["id"] in existing_ids:
            print(f"SKIP (already present): {rec['id']}")
            continue
        data["genealogy"].append(rec)
        added.append(rec["id"])
        pid = rec["anchors"][0]["target"].split("::")[-1]
        kind = rec["kind"]
        auth = rec["authority"]
        print(f"ADD: {rec['id']:<40} → {pid:<10}  {auth}/{kind}")

    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print()
    print(f"Total records in genealogy: {len(data['genealogy'])}")
    print(f"Added this run: {len(added)}")


if __name__ == "__main__":
    main()
