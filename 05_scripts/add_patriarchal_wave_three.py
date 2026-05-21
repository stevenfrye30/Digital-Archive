"""Wave Three — Patriarchal Emergence (Genesis 12-50 remembered).

Adds fourteen records across nine chapters, structured as:

  Akedah cluster (6, all at distinct verses, no chamber):
    gen.22.1   hineni                        tertiary  linguistic
    gen.22.2   mount-moriah                  tertiary  architecture
    gen.22.9   akedah-binding                secondary commentary
    gen.22.13  ram-thicket-substitute        tertiary  linguistic
    gen.22.14  yhwh-jireh                    tertiary  linguistic
    gen.22.19  reception-three-traditions    secondary reception-history

  Sacred-site rhythm (3):
    gen.13.4   bethel-altar-return           tertiary  architecture
    gen.23.19  machpelah-cave                tertiary  architecture
    gen.26.18  wells-of-isaac                tertiary  architecture

  Dream / vision thread (3, NOT AO·008 anchors):
    gen.32.24  wrestling-jabbok              secondary commentary
    gen.37.7   joseph-first-dream            secondary commentary
    gen.41.25  pharaoh-dreams                tertiary  commentary

  Abrahamic deepening (2):
    gen.18.2   three-visitors-reception      secondary reception-history
    gen.16.13  el-roi-hagar                  tertiary  linguistic

Discipline:
  · No new Atlas Object; no AO·014; no chamber class.
  · No metadata on existing AO records modified.
  · Akedah cluster is six independent witnesses, not a chamber.
  · Each Akedah record anchors at its own verse — no verse
    carries more than one Wave Three record.
  · Dream/vision records are commentary kind; the resonance
    with AO·008 is editorial (in the body) not metadata.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "bible_kjv.json"

DATE = "2026-05-21"
AUTHOR = "archive:steward:steve"
LAYER = "editorial"
LIFECYCLE = "provisional"


def record(*, id_, kind, title, verse, body, authority,
           tradition, source_basis, confidence):
    return {
        "id": id_,
        "kind": kind,
        "title": title,
        "anchors": [{"target": f"archive:passage:bible::kjv::{verse}"}],
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


# ── Sacred-site rhythm (3) ───────────────────────────────────

bethel_altar_return = record(
    id_="gen13-bethel-altar-return",
    kind="architecture",
    title="Return to the altar at Bethel",
    verse="gen.13.4",
    body=(
        "Abram returns from Egypt and retraces his own steps. "
        "The chapter takes him back to the tent location between "
        "Beth-el and Hai, and to the same altar he had raised at "
        "Gen 12:8 — the same ground, the same stones, the same "
        "calling on the name of the LORD.\n\n"
        "The patriarchal pattern is named here: the altars are "
        "not abandoned. The patriarchs return to them, calling "
        "on the name of the LORD where they have called before. "
        "Sacred sites accumulate as the land is walked again.\n\n"
        "The land remembers."
    ),
    authority="tertiary",
    tradition="Patriarchal sacred-site rhythm — Hebrew Bible",
    source_basis="Gen 13:1-4; cf. Gen 12:8",
    confidence="Archive editorial summary of primary text",
)

machpelah_cave = record(
    id_="gen23-machpelah-cave",
    kind="architecture",
    title="Machpelah — the first patriarchal grave",
    verse="gen.23.19",
    body=(
        "The cave of Machpelah, before Mamre (the same is "
        "Hebron in the land of Canaan), is the first piece of "
        "the promised land any patriarch comes to own — and he "
        "owns it because his wife has died and must be buried. "
        "The chapter's long negotiation between Abraham and "
        "Ephron the Hittite (twenty-three verses for a single "
        "transaction) makes the acquisition formally complete: "
        "field, cave, and trees in the borders round about, "
        "'made sure unto Abraham for a possession.'\n\n"
        "Sarah is buried here. Abraham will be buried here. "
        "Isaac, Rebekah, Leah, and Jacob will follow. The "
        "first piece of the patriarchal land is held as grave "
        "before it is held as inheritance.\n\n"
        "Sacred geography by burial."
    ),
    authority="tertiary",
    tradition="Patriarchal sacred-site rhythm — Hebrew Bible",
    source_basis="Gen 23:1-20; cf. Gen 25:9-10, 49:29-32",
    confidence="Archive editorial summary of primary text",
)

wells_of_isaac = record(
    id_="gen26-wells-of-isaac",
    kind="architecture",
    title="The wells re-dug — Isaac at his father's stones",
    verse="gen.26.18",
    body=(
        "Isaac retraces his father's wells. The Philistines "
        "have filled them in after Abraham's death; Isaac "
        "re-digs them — and renames them after his father's "
        "names. The pattern is the one Abram had set at Bethel: "
        "the patriarchs walk the land their fathers walked, "
        "calling sites by the names their fathers gave them.\n\n"
        "The chapter continues with new wells — Esek "
        "('contention'), Sitnah ('hostility'), Rehoboth "
        "('breadth') — but it opens with the recovery of the "
        "inherited ones. The patriarchal claim is by water and "
        "by naming, and the second patriarch's first act on "
        "the land is to remember his father's water."
    ),
    authority="tertiary",
    tradition="Patriarchal sacred-site rhythm — Hebrew Bible",
    source_basis="Gen 26:18-33; cf. Gen 21:25-31",
    confidence="Archive editorial summary of primary text",
)


# ── Abrahamic deepening (2) ──────────────────────────────────

el_roi_hagar = record(
    id_="gen16-el-roi-hagar",
    kind="linguistic",
    title="El-roi — 'the God who sees me'",
    verse="gen.16.13",
    body=(
        "Hagar, the Egyptian slave, has fled into the wilderness "
        "from Sarai's harshness. The angel of the LORD finds "
        "her at a spring on the way to Shur, speaks with her, "
        "sends her back, and promises that her son's descendants "
        "will be a multitude. After he leaves, Hagar names the "
        "LORD ʾEl-Roʾi (אֵל רֳאִי) — 'God of seeing,' or 'God "
        "who sees me' — the chapter's central wordplay turning "
        "on the verb raʾah ('to see') used three times in two "
        "verses.\n\n"
        "This is the first divine epithet given by a human in "
        "scripture, and the first given by a woman. The slave "
        "woman who has been seen by no one in her bondage "
        "names the God she has met as the one who sees. The "
        "well she met him at is also named: Beʾer-laḥai-roʾi, "
        "'the well of the living one who sees me' (16:14). "
        "The naming holds."
    ),
    authority="tertiary",
    tradition="Patriarchal narrative — Hebrew Bible",
    source_basis="Gen 16:7-14",
    confidence="Archive editorial linguistic gloss",
)

three_visitors_reception = record(
    id_="gen18-three-visitors-reception",
    kind="reception-history",
    title="The three visitors at the oaks of Mamre",
    verse="gen.18.2",
    body=(
        "The chapter opens by naming the LORD as the one "
        "appearing, and then immediately the patriarch sees "
        "three. Abraham runs from the tent door, bows to the "
        "earth, addresses them in the singular ('My Lord'), "
        "and prepares a feast of bread, butter, milk, and a "
        "tender calf. The three eat under the tree. They ask "
        "about Sarah. They give the promise of Isaac's birth. "
        "Sarah laughs from behind the tent door, and is "
        "rebuked. The chapter then turns toward Sodom.\n\n"
        "Christian patristic tradition has read this passage "
        "as one of the Old Testament's most explicit witnesses "
        "to the Trinity: the LORD appearing, three men "
        "standing, addressed and addressing in the singular. "
        "Augustine devotes a chapter of De Trinitate to the "
        "question; Andrei Rublev's icon — the three angels at "
        "the table — has been the visual heart of Eastern "
        "Orthodox prayer for six hundred years. The reading "
        "sees in three-men-and-yet-the-LORD the Old Testament's "
        "clearest figure of three-persons-and-one-God.\n\n"
        "Jewish tradition has read the chapter differently: "
        "three angels, sent for three distinct purposes — the "
        "promise to Sarah, the destruction of Sodom, the "
        "rescue of Lot — with one of them speaking as the "
        "LORD's voice. The chapter's own grammar moves between "
        "singular and plural without resolving, and the "
        "reception traditions take that grammar in different "
        "directions.\n\n"
        "The Mamre encounter has been carried by two "
        "civilizations as two related but distinct theophanies."
    ),
    authority="secondary",
    tradition="Christian Trinitarian and Jewish angelic reception",
    source_basis="Gen 18:1-15; Augustine, De Trinitate II; Rublev, Trinity Icon",
    confidence="Archive editorial reception-history gloss",
)


# ── Akedah cluster (6, all at distinct verses) ───────────────

hineni = record(
    id_="gen22-hineni",
    kind="linguistic",
    title="Hineni — here I am",
    verse="gen.22.1",
    body=(
        "At three distinct moments in the chapter, Abraham "
        "answers hineni (הִנֵּנִי). He answers it to God at "
        "the chapter's opening (22:1). He answers it to Isaac "
        "on the path up the mountain (22:7). He answers it "
        "again to the angel of the LORD at the chapter's edge "
        "(22:11), when his hand is already raised.\n\n"
        "The word is compressed Hebrew: hen ('behold') + ni "
        "('I'). Not a verb of intention or readiness, but a "
        "verb of presence — 'I am here, fully here, before "
        "the one calling.' The Akedah's whole structure rests "
        "on the three hineni answers: to the call, to the son, "
        "to the staying hand. Each is the same word; each "
        "answers a different voice."
    ),
    authority="tertiary",
    tradition="Patriarchal narrative — Hebrew Bible",
    source_basis="Gen 22:1, 22:7, 22:11",
    confidence="Archive editorial linguistic gloss",
)

mount_moriah = record(
    id_="gen22-mount-moriah",
    kind="architecture",
    title="Mount Moriah — the land that becomes the temple",
    verse="gen.22.2",
    body=(
        "'Get thee into the land of Moriah... and offer him "
        "there for a burnt offering upon one of the mountains "
        "which I will tell thee of.' (22:2) The name moriyyah "
        "(מוֹרִיָּה) is named here for the first time in "
        "scripture. Its etymology is disputed — possibly 'the "
        "LORD will provide / be seen' (the wordplay yhwh-yireh "
        "follows in the chapter), possibly 'the place of "
        "teaching' (mōreh + yah).\n\n"
        "Centuries later, the Chronicler will name the "
        "temple's hill as Moriah: 'Solomon began to build the "
        "house of the LORD at Jerusalem in mount Moriah, where "
        "the LORD appeared unto David his father' (2 Chr 3:1). "
        "The land of Abraham's offering becomes the ground of "
        "Israel's temple. The mountain where the substitute "
        "was provided becomes the mountain where substitutionary "
        "sacrifice is daily practiced.\n\n"
        "A single proper name carries that long correspondence."
    ),
    authority="tertiary",
    tradition="Patriarchal sacred-site rhythm — Hebrew Bible",
    source_basis="Gen 22:2; 2 Chr 3:1",
    confidence="Archive editorial summary of primary text",
)

akedah_binding = record(
    id_="gen22-akedah-binding",
    kind="commentary",
    title="The binding — Akedat Yitzhak",
    verse="gen.22.9",
    body=(
        "And they came to the place which God had told him of; "
        "and Abraham built an altar there, and laid the wood "
        "in order, and bound Isaac his son, and laid him on "
        "the altar upon the wood. (22:9)\n\n"
        "The chapter's drama climbs through three days of "
        "journey and ascends a mountain, and at its summit the "
        "verb is va-yaʿakod (וַיַּעֲקֹד) — and he bound. From "
        "this word the chapter takes the name by which Jewish "
        "tradition has known it for two thousand years: Akedat "
        "Yitzhak, the Binding of Isaac. The narrative does not "
        "say what passes between father and son in this moment. "
        "The father binds; the son is bound; the knife is "
        "taken up; the angel calls. The text moves through "
        "these motions in unembellished verbs, refusing every "
        "interior the reader might want.\n\n"
        "The Akedah is the canon's most contested passage. It "
        "is the foundational sacrifice that does not happen — "
        "and yet, as Jewish tradition has read it, it is the "
        "sacrifice that does happen, because the willingness "
        "is the offering. Later Christian reception will read "
        "the chapter typologically: a father willing to give "
        "an only beloved son on a mountain. Islamic tradition "
        "will read it with Ishmael in place of Isaac and the "
        "binding moved to Mecca. Three civilizations have "
        "built their religious imagination around this single "
        "chapter's choices.\n\n"
        "What the chapter itself says: God tests Abraham, "
        "Abraham binds Isaac, the angel intervenes, a ram is "
        "provided. What the chapter does not say is what the "
        "codex must also not say. The binding stands."
    ),
    authority="secondary",
    tradition="Patriarchal narrative — Hebrew Bible",
    source_basis="Gen 22:1-19; cf. Heb 11:17-19",
    confidence="Archive editorial narrative-theological gloss",
)

ram_thicket_substitute = record(
    id_="gen22-ram-thicket-substitute",
    kind="linguistic",
    title="The ram caught in the thicket",
    verse="gen.22.13",
    body=(
        "And Abraham lifted up his eyes, and looked, and "
        "behold behind him a ram caught in a thicket by his "
        "horns. (22:13)\n\n"
        "The Hebrew is sparse: ʾayil ʾaḥar neʾeḥaz ba-sevak "
        "be-qarnav (אַיִל אַחַר נֶאֱחַז בַּסְּבַךְ "
        "בְּקַרְנָיו) — a ram, behind, caught in the thicket, "
        "by its horns. The verb neʾeḥaz ('caught, held') "
        "governs the substitute's appearance: the animal is "
        "held in place for the sacrifice that is now possible. "
        "The substitute is provided — by the LORD, the "
        "chapter implies — at the precise moment when the "
        "knife is raised. This is the Bible's first explicit "
        "substitutionary offering."
    ),
    authority="tertiary",
    tradition="Patriarchal narrative — Hebrew Bible",
    source_basis="Gen 22:13",
    confidence="Archive editorial linguistic gloss",
)

yhwh_jireh = record(
    id_="gen22-yhwh-jireh",
    kind="linguistic",
    title="YHWH-yireh — the LORD will see / provide",
    verse="gen.22.14",
    body=(
        "And Abraham called the name of that place "
        "Jehovah-jireh: as it is said to this day, In the "
        "mount of the LORD it shall be seen. (22:14)\n\n"
        "The naming carries the chapter's central wordplay. "
        "yireh (יִרְאֶה) is the verb 'to see' — but in the "
        "passive-reflexive form it also yields 'to be seen' "
        "or 'to provide' (the seer arranges what is seen). "
        "The narrative uses the word three times in the "
        "chapter (22:8 'God will provide / see for himself', "
        "22:13 the ram seen, 22:14 the place named). The "
        "naming is the chapter's hinge: the mountain is named "
        "for what the LORD did at it, and the proverb that "
        "'as it is said to this day' preserves the naming as "
        "living memory."
    ),
    authority="tertiary",
    tradition="Patriarchal narrative — Hebrew Bible",
    source_basis="Gen 22:14",
    confidence="Archive editorial linguistic gloss",
)

akedah_reception = record(
    id_="gen22-reception-three-traditions",
    kind="reception-history",
    title="The Akedah in three traditions",
    verse="gen.22.19",
    body=(
        "The Binding of Isaac is one of the few biblical "
        "narratives read with sustained intensity by Jewish, "
        "Christian, and Islamic traditions, each reading the "
        "chapter through its own theological imagination.\n\n"
        "Jewish tradition reads the Akedah as the merit of "
        "the patriarchs — Abraham's willingness, Isaac's "
        "willingness, the ram's substitution — invoked on "
        "Rosh Hashanah and woven into the High Holy Day "
        "liturgy. The shofar's blast recalls the ram caught "
        "in the thicket; the central prayer of Rosh Hashanah, "
        "the Zikhronot, asks God to remember the Akedah on "
        "behalf of Isaac's descendants. Some midrashim insist "
        "that Isaac was in fact bound, slain, and brought "
        "back — a more total reading than the text allows but "
        "a reading the tradition has carried.\n\n"
        "Christian tradition reads the chapter typologically. "
        "Hebrews 11:17-19 names Isaac as 'figuratively' "
        "received back from the dead; later patristic and "
        "medieval tradition will see in Isaac carrying the "
        "wood up the mountain a figure of Christ carrying the "
        "cross, and in the ram caught in the thicket a figure "
        "of the crucifixion. The Caravaggio painting, the "
        "Rembrandt painting, the Kierkegaard meditation Fear "
        "and Trembling — Christian reception has returned to "
        "this chapter again and again, finding in it the "
        "riddle of obedience and the figure of substitutionary "
        "sacrifice.\n\n"
        "Islamic tradition relocates the binding. In the "
        "Qur'anic account (Surah 37) the sacrificed son is "
        "unnamed, and Islamic tradition has overwhelmingly "
        "identified him as Ishmael, with the binding placed "
        "not at Moriah but near Mecca. The Eid al-Adha — the "
        "feast of the sacrifice — is observed in "
        "commemoration, and the same ram of substitution is "
        "at the centre of the festival. The chapter has "
        "become the ground of three civilizations' liturgies "
        "of sacrifice."
    ),
    authority="secondary",
    tradition="Jewish midrash, Christian typology, Islamic reception",
    source_basis="Rosh Hashanah liturgy; Heb 11:17-19; Surah 37; Eid al-Adha",
    confidence="Archive editorial reception-history gloss",
)


# ── Dream / vision thread (3) ────────────────────────────────

wrestling_jabbok = record(
    id_="gen32-wrestling-jabbok",
    kind="commentary",
    title="Wrestling at Jabbok",
    verse="gen.32.24",
    body=(
        "And Jacob was left alone; and there wrestled a man "
        "with him until the breaking of the day. (32:24)\n\n"
        "The man is not named. He arrives unannounced; he "
        "wrestles all night; he asks Jacob's name and changes "
        "it; he refuses to give his own. He touches the "
        "hollow of Jacob's thigh and Jacob will limp for the "
        "rest of his life. He blesses Jacob and disappears "
        "with the dawn.\n\n"
        "The chapter that contains this scene is a fear "
        "chapter: Jacob is approaching his brother Esau after "
        "twenty years, his caravan divided into two camps so "
        "that one may survive if the other is struck, his "
        "wives and children sent ahead across the ford. He is "
        "left alone on the wrong side of the river and meets "
        "a man who is not a man. The narrative refuses to "
        "identify the wrestler explicitly. The text says only "
        "that Jacob names the place Peniel ('face of God') "
        "because 'I have seen God face to face, and my life "
        "is preserved.' The patriarchal visionary tradition "
        "has not, until this night, made the seer touch what "
        "he sees.\n\n"
        "What the chapter gives is not vision but contact. "
        "Jacob comes away renamed, wounded, and blessed. The "
        "patriarchal narrative has its highest theological "
        "moment in a body that limps for the rest of its days."
    ),
    authority="secondary",
    tradition="Patriarchal narrative — Hebrew Bible",
    source_basis="Gen 32:22-32; cf. Hos 12:3-4",
    confidence="Archive editorial narrative-theological gloss",
)

joseph_first_dream = record(
    id_="gen37-joseph-first-dream",
    kind="commentary",
    title="Joseph's first dream — the sheaves",
    verse="gen.37.7",
    body=(
        "And he said unto them, Hear, I pray you, this dream "
        "which I have dreamed: For, behold, we were binding "
        "sheaves in the field, and, lo, my sheaf arose, and "
        "also stood upright; and, behold, your sheaves stood "
        "round about, and made obeisance to my sheaf. "
        "(37:6-7)\n\n"
        "The Joseph cycle opens with two dreams in a single "
        "chapter — the sheaves at 37:7 and the sun, moon, "
        "and eleven stars at 37:9. These dreams set the "
        "cycle's whole motion: the elder brothers will bow, "
        "the father and mother will recognize the future "
        "king-figure, and the chapter ends with Joseph "
        "stripped of his coat and thrown into a pit. The "
        "dream is the cycle's fuse; everything else burns "
        "from it.\n\n"
        "The patriarchal narrative has carried visionary "
        "moments before — Jacob's ladder, Jacob's wrestling — "
        "but these were given to the patriarch alone, often "
        "at night, at a named site. Joseph's dreams are given "
        "to a boy in a field, told openly to his brothers, "
        "and provoke the action that drives him into Egypt. "
        "The form of vision shifts: from theophanic to "
        "prophetic, from solitary to communal, from sacred "
        "site to family table.\n\n"
        "The Joseph cycle is the canon's first sustained "
        "narrative built around dreams — Joseph's two, the "
        "butler and baker, Pharaoh's two. Twelve chapters of "
        "the cycle's twenty turn on what someone has dreamed. "
        "Dreams have become a way of seeing the future that "
        "the canon will continue to use through Daniel and "
        "into the apocalyptic tradition."
    ),
    authority="secondary",
    tradition="Patriarchal narrative — Hebrew Bible",
    source_basis="Gen 37:5-11; cf. Dan 2",
    confidence="Archive editorial narrative-theological gloss",
)

pharaoh_dreams = record(
    id_="gen41-pharaoh-dreams",
    kind="commentary",
    title="Pharaoh's two dreams — seven fat and seven lean",
    verse="gen.41.25",
    body=(
        "And Joseph said unto Pharaoh, The dream of Pharaoh "
        "is one: God hath shewed Pharaoh what he is about to "
        "do. (41:25)\n\n"
        "Two dreams given to a foreign king. The doubling — "
        "fat cows then thin cows, then full ears then "
        "withered ears — is interpreted as emphasis: the "
        "matter is established by God, the matter is shortly "
        "to come. Joseph's interpretation moves the cycle's "
        "pivot: from Hebrew slave to Egyptian vizier, in the "
        "same chapter, by reading two dreams.\n\n"
        "The form of vision has reached its widest scope. In "
        "the patriarchal narrative, dreams were given to the "
        "patriarchs (Jacob, Joseph) at named sites or in "
        "personal moments. By the close of Genesis, dreams "
        "are given to Pharaoh — a foreign king, the canon's "
        "first explicit non-Hebrew dream-recipient. The "
        "visionary thread that began at Jacob's stone at "
        "Bethel has reached the highest court of Egypt; the "
        "dream-interpreter is the same boy whose own dreams "
        "started the journey there."
    ),
    authority="tertiary",
    tradition="Patriarchal narrative — Hebrew Bible",
    source_basis="Gen 41:1-36; cf. Dan 2",
    confidence="Archive editorial narrative-theological gloss",
)


WAVE_THREE = [
    # Sacred-site rhythm
    bethel_altar_return,
    machpelah_cave,
    wells_of_isaac,
    # Abrahamic deepening
    el_roi_hagar,
    three_visitors_reception,
    # Akedah cluster
    hineni,
    mount_moriah,
    akedah_binding,
    ram_thicket_substitute,
    yhwh_jireh,
    akedah_reception,
    # Dream / vision thread
    wrestling_jabbok,
    joseph_first_dream,
    pharaoh_dreams,
]


def main():
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {r["id"] for r in data["genealogy"]}
    added = []
    for rec in WAVE_THREE:
        if rec["id"] in existing_ids:
            print(f"SKIP (already present): {rec['id']}")
            continue
        data["genealogy"].append(rec)
        added.append(rec["id"])
        pid = rec["anchors"][0]["target"].split("::")[-1]
        kind = rec["kind"]
        auth = rec["authority"]
        print(f"ADD: {rec['id']:<40} → {pid:<12} {auth}/{kind}")

    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print()
    print(f"Total records in genealogy: {len(data['genealogy'])}")
    print(f"Added this run: {len(added)}")


if __name__ == "__main__":
    main()
