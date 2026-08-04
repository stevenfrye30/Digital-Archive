"""Add the 22-object Genesis 1 calibration set to bible_kjv.json.

Reads data/bible_kjv.json, appends 21 new records (the existing
Doré plate at gen.1.3 stays), writes back. Idempotent: re-running
deduplicates by id.

Per the Folio System Specification.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "bible_kjv.json"

AUTHOR = "archive:steward:steve"
DATE = "2026-05-18"
LAYER = "editorial"
STATE = "provisional"

URN = "archive:passage:bible::kjv::"


def rec(rid, kind, title, anchor_pid, body, extra=None):
    r = {
        "id": rid,
        "kind": kind,
        "title": title,
        "anchors": [{"target": URN + anchor_pid}],
        "body": body,
        "provenance": {
            "layer": LAYER,
            "author": AUTHOR,
            "date": DATE,
            "lifecycle_state": STATE,
        },
    }
    if extra:
        r.update(extra)
    return r


NEW_RECORDS = [
    # ─ Cluster at Gen 1:1 (the opening — 5 markers) ───────────
    rec(
        "gen1-cosmology-ane",
        "cosmology",
        "Ancient Near Eastern Cosmology",
        "gen.1.1",
        "The cosmos presupposed by Genesis 1 is the inherited Ancient "
        "Near Eastern model: a flat earth-disc resting on pillars over "
        "the cosmic waters of the abyss (tehôm), domed by the firmament "
        "(rāqîaʿ) — a solid sky-vault holding back the upper waters. "
        "Above the firmament: more waters; below the earth: Sheol and "
        "the deep. The Hebrew text neither argues for this cosmology "
        "nor invents it — it inherits the picture from the broader "
        "regional imagination (cf. Babylonian Enuma Elish) and bends "
        "it toward Israel's singular God.\n\n"
        "[Navigable diagram placeholder — a three-tier cosmos with "
        "waters above, firmament-dome, flat earth, waters below, and "
        "Sheol. Future: clickable layers naming each region.]",
    ),
    rec(
        "gen1-linguistic-bereshit",
        "linguistic",
        "bĕrēʾšît — \"In the beginning\"",
        "gen.1.1",
        "The opening word bĕrēʾšît has been read two ways since Rashi:\n\n"
        "  Absolute:   \"In the beginning, God created…\" (KJV, most translations)\n"
        "  Construct:  \"When God began to create…\" (Rashi, NJPS, NRSV note)\n\n"
        "The construct reading turns verse 1 into a temporal clause "
        "leading into verse 2's description of the pre-creation chaos. "
        "It removes the doctrine of creation ex nihilo from the surface "
        "of the text and aligns Genesis more closely with the Enuma "
        "Elish opening (\"When on high…\").\n\n"
        "The grammar permits either; the theology differs sharply.",
    ),
    rec(
        "gen1-manuscript-opening",
        "manuscript",
        "Manuscript witnesses to Gen 1:1",
        "gen.1.1",
        "The opening of Genesis is textually stable across the major "
        "traditions, but vocalization and punctuation carry interpretive "
        "weight.\n\n"
        "  Masoretic (BHS):     בְּרֵאשִׁית בָּרָא אֱלֹהִים\n"
        "  Septuagint (LXX):    Ἐν ἀρχῇ ἐποίησεν ὁ θεὸς\n"
        "  Samaritan Pentateuch: בראשית ברא אלהים\n"
        "  Vulgate:             In principio creavit Deus\n\n"
        "The Tiberian Masoretic pointing constrains bĕrēʾšît to an "
        "absolute reading; the consonantal text underlying all "
        "witnesses leaves the construct/absolute ambiguity intact.",
    ),
    rec(
        "gen1-commentary-augustine",
        "commentary",
        "Augustine — Confessions XI / City of God XI",
        "gen.1.1",
        "Augustine confronts the question \"What was God doing before "
        "creation?\" — and resolves it by denying the premise. Time "
        "itself, he argues, is a creature; it began with creation. "
        "There is no \"before\" for God to have occupied.\n\n"
        "\"Time itself was made along with the creation; there was no "
        "time prior to it…\" (City of God XI.6)\n\n"
        "The Augustinian reading inaugurates Western Christian "
        "metaphysics of time and creation — picked up by Aquinas, "
        "reformulated by Bonaventure, and reframed in the twentieth "
        "century by physicists and theologians considering Big Bang "
        "cosmology.",
    ),
    rec(
        "gen1-xref-nt-creation",
        "cross-reference",
        "New Testament echoes of Gen 1:1",
        "gen.1.1",
        "The Christian canon reads Genesis 1:1 through three later "
        "passages:\n\n"
        "  John 1:1   — \"In the beginning was the Word…\" The Johannine "
        "prologue maps logos onto bĕrēʾšît, identifying the agent of "
        "creation with Christ.\n\n"
        "  Hebrews 11:3 — \"By faith we understand that the worlds were "
        "framed by the word of God.\" Creation as speech-act, hearable "
        "only by faith.\n\n"
        "  Colossians 1:15-17 — \"All things were created by him, and "
        "for him… and by him all things consist.\" Christ as both "
        "agent and telos of creation.",
    ),

    # ─ Verse 1:2 (the formless deep) ─────────────────────────
    rec(
        "gen1-linguistic-tohu",
        "linguistic",
        "tōhû wā-bōhû",
        "gen.1.2",
        "The phrase tōhû wā-bōhû is rhyming and tonal — \"waste and "
        "void,\" \"formlessness and emptiness,\" \"trackless wilderness "
        "and confusion.\" Tōhû recurs in Isaiah 45:18 (\"He created it "
        "not in tōhû\") and Jeremiah 4:23, where it explicitly evokes "
        "an un-creation, a reversal back into the primordial state.\n\n"
        "The resonance with Babylonian Tiamat (the chaos-dragon "
        "defeated by Marduk) is unmistakable; Genesis declines the "
        "combat myth but preserves the chaos-imagery. There is no "
        "battle in Genesis 1 — only divine speech turning tōhû into "
        "ordered cosmos.",
    ),
    rec(
        "gen1-reception-ruach",
        "reception-history",
        "rûaḥ ʾĕlōhîm — Spirit, wind, or breath",
        "gen.1.2",
        "The phrase rûaḥ ʾĕlōhîm has carried at least three readings "
        "across 2,500 years:\n\n"
        "  Spirit of God   — the dominant Christian reading, "
        "identifying this with the Holy Spirit of the Trinitarian "
        "tradition.\n\n"
        "  Mighty wind     — modern critical scholarship, taking "
        "ʾĕlōhîm as a superlative intensifier (\"a great wind\").\n\n"
        "  Divine breath   — Jewish mystical reading, especially "
        "Kabbalistic: the divine breath hovering over the waters as a "
        "creative principle.\n\n"
        "Each reading reshapes the surrounding theology — pneumatic, "
        "naturalistic, or contemplative.",
    ),

    # ─ Verse 1:3 (existing plate + 2 new) ────────────────────
    rec(
        "gen1-cosmology-light-before-luminaries",
        "cosmology",
        "Light before luminaries",
        "gen.1.3",
        "Interpretive puzzle: light is created on day 1; sun, moon, "
        "and stars on day 4. What light, then, illuminates the first "
        "three days?\n\n"
        "Rabbinic tradition (Genesis Rabbah 3:6) speaks of a primordial "
        "light — the ʾôr ganûz, \"hidden light\" — separate from "
        "celestial luminaries, set aside for the righteous in the "
        "world to come.\n\n"
        "Patristic readings (Basil's Hexaemeron) take the day-1 light "
        "as a created luminosity that the sun later carries; Augustine "
        "treats it allegorically as intellectual light.\n\n"
        "Modern critical reading: the Priestly author structures the "
        "week as three days of separation (light/dark, waters/sky, "
        "land/sea) and three days of filling (luminaries, sea-creatures, "
        "land-creatures). Light precedes luminaries because the "
        "structure demands it.",
    ),
    rec(
        "gen1-ritual-maariv-aravim",
        "ritual",
        "Ma'ariv ʿarāḇîm — Hebrew evening blessing",
        "gen.1.3",
        "The traditional Jewish evening service opens with the blessing "
        "Ma'ariv ʿarāḇîm (\"who brings on the evenings\"), praising the "
        "God \"who at His word brings on the evening twilight, who "
        "with wisdom opens the gates of the heavens, with understanding "
        "changes the times…\"\n\n"
        "The blessing inhabits the creation-light theme liturgically: "
        "at the daily threshold between day and night, the community "
        "rehearses Genesis 1:3-5. Creation is not a past event "
        "remembered but a recurring divine act — every evening, every "
        "morning, the separation of light from darkness happens again.",
    ),

    # ─ Verses 1:6-8 (firmament) ──────────────────────────────
    rec(
        "gen1-cosmology-firmament",
        "cosmology",
        "The Firmament (rāqîaʿ)",
        "gen.1.6",
        "The rāqîaʿ is the solid hammered-out dome of the sky, holding "
        "back the cosmic waters above. The Hebrew root r-q-ʿ describes "
        "metal-beating — the firmament is conceived as physical, "
        "tangible vault-work.\n\n"
        "Above the rāqîaʿ: the upper waters, released through windows "
        "(ʾărubbôt) at the flood and during heavy rain.\n"
        "Within the rāqîaʿ: sun, moon, stars (day 4) — set into the "
        "vault itself.\n"
        "Below the rāqîaʿ: the gathered earth-waters, then dry land.\n\n"
        "Modern translations soften rāqîaʿ to \"expanse\" or \"sky.\" "
        "The Hebrew picture is more concrete and more ancient.\n\n"
        "[Navigable diagram placeholder — three-tier cosmos with "
        "ancient and modern overlay toggle.]",
    ),
    rec(
        "gen1-architecture-cosmic-temple",
        "architecture",
        "Cosmic Temple parallels",
        "gen.1.7",
        "John Walton, Jon Levenson, and others have argued that "
        "Genesis 1 is structured as a temple-building narrative. The "
        "Priestly author parallels the seven days of creation with the "
        "seven speeches by which God commissions the Tabernacle in "
        "Exodus 25-40.\n\n"
        "The cosmos is the macro-Temple; the Temple is the micro-cosmos. "
        "The firmament corresponds to the Temple veil; the heavenly "
        "lights to the menorah; the cosmic Sabbath to the Temple's "
        "completion. The creation week ends with God taking up "
        "residence (Sabbath rest) — the same verb used for divine "
        "indwelling in the Temple.\n\n"
        "[Navigable diagram placeholder — Temple plan overlaid on "
        "cosmos plan, with correspondences highlighted.]",
    ),

    # ─ Verse 1:11 (vegetation) ───────────────────────────────
    rec(
        "gen1-commentary-philo",
        "commentary",
        "Philo of Alexandria — De Opificio Mundi",
        "gen.1.11",
        "Philo (c. 20 BCE – c. 50 CE) reads Genesis 1 as a Platonic "
        "two-stage creation: first the intelligible cosmos (the "
        "perfect ideas), then the visible cosmos (instantiations of "
        "those ideas). The six days are not chronological but "
        "categorial — six as the perfect number, structuring divine "
        "thought.\n\n"
        "The Alexandrian allegorical tradition inaugurated by Philo "
        "shapes Origen, Clement, and the entire Eastern patristic "
        "reading of Genesis. It treats the literal sense as a husk "
        "around the philosophical kernel.\n\n"
        "Philo's De Opificio Mundi is the earliest extant systematic "
        "commentary on Genesis 1.",
    ),

    # ─ Verse 1:14 (lights / calendar) ────────────────────────
    rec(
        "gen1-timeline-calendar",
        "timeline",
        "Calendar-establishing verse",
        "gen.1.14",
        "\"Let them be for signs, and for seasons, and for days, and "
        "years.\" Genesis 1:14 founds the Israelite liturgical "
        "calendar: lunar months tracked by the moon, solar years by "
        "the sun, festivals (môʿădîm) keyed to both. Without this "
        "verse, no Sabbath, no Passover, no Day of Atonement.\n\n"
        "Datable horizon: the Priestly source's calendar is usually "
        "located in the Babylonian exile (6th century BCE), when the "
        "community was renegotiating its calendar against Babylonian "
        "lunar reckoning. The verse may be read as the theological "
        "claim that Israel's calendar is divinely instituted — not "
        "borrowed from Babylon.",
    ),
    rec(
        "gen1-map-ane-constellations",
        "map",
        "Constellations of the ancient Near East",
        "gen.1.14",
        "The Hebrew Bible names a small set of constellations:\n\n"
        "  Kîmâ      — the Pleiades (Job 9:9, 38:31; Amos 5:8)\n"
        "  Kĕsîl     — Orion (same verses)\n"
        "  ʿAyiš     — the Bear (Ursa Major), or perhaps a different group\n"
        "  Mazzārôt  — \"constellations\" generically; possibly the zodiac\n\n"
        "These names overlap and contrast with the Babylonian "
        "constellation tradition (MUL.APIN tablets, c. 1000 BCE), "
        "which provides our best reconstruction of the ancient Near "
        "Eastern night sky as the Genesis author would have known it.\n\n"
        "[Navigable star map placeholder — ANE sky with Hebrew "
        "constellation names and their proposed identifications.]",
    ),

    # ─ Verses 1:20-25 (creatures) ────────────────────────────
    rec(
        "gen1-artifact-tanninim",
        "artifact",
        "Tannînim — the great sea creatures",
        "gen.1.21",
        "Genesis 1:21 places God as creator of the tannînim — the "
        "great sea-monsters. The same word elsewhere names the dragon "
        "of the deep (Isaiah 27:1, Psalm 74:13), the Babylonian "
        "Tiamat-creature, the Ugaritic Lotan.\n\n"
        "In Genesis 1, the tannînim are de-mythologized: they are not "
        "rivals to God, not chaos-monsters to be defeated — they are "
        "creatures, made on day 5 like the fish and birds. The verse "
        "is theological combat by silence: the dragon of competing "
        "cosmologies is simply included in the list of God's good "
        "creations.\n\n"
        "[Comparative artifact reference — Babylonian Tiamat imagery, "
        "Ugaritic Lotan, Egyptian Apep. Future: image gallery.]",
    ),
    rec(
        "gen1-commentary-aquinas",
        "commentary",
        "Aquinas — Summa Theologiae I.q.69",
        "gen.1.24",
        "Aquinas asks whether the days of creation are to be "
        "understood successively, as Basil holds, or simultaneously, "
        "as Augustine holds. He preserves both readings as legitimate "
        "Catholic positions, distinguishing the literal six days "
        "(Basil) from the metaphysical instant in which the creature "
        "receives its form (Augustine).\n\n"
        "The Thomistic synthesis insulates Catholic theology from the "
        "later young-earth literalism: the six days are not, in "
        "Aquinas's reading, a doctrinally required chronology. The "
        "metaphysical claim — that creation is a single divine act, "
        "outside time — is the load-bearing one.",
    ),

    # ─ Verses 1:26-27 (humanity) ─────────────────────────────
    rec(
        "gen1-linguistic-naaseh-adam",
        "linguistic",
        "naʿăśeh ʾāḏām — \"Let us make humanity\"",
        "gen.1.26",
        "The plural cohortative verb naʿăśeh (\"let us make\") has "
        "puzzled exegetes for two millennia. Six readings circulate:\n\n"
        "  1. Plural of majesty — royal \"we,\" stylistic.\n"
        "  2. Divine council — God addressing a heavenly assembly "
        "(cf. 1 Kings 22:19, Job 1:6).\n"
        "  3. Self-deliberation — God reasoning with God.\n"
        "  4. Trinitarian (Christian, anachronistic for the Hebrew "
        "author): the Father addresses Son and Spirit.\n"
        "  5. Address to creation itself — calling earth to participate.\n"
        "  6. Plural of fullness — the divine plenitude.\n\n"
        "Mainstream critical reading favors the divine council; "
        "traditional Jewish and Christian readings vary by tradition.",
    ),
    rec(
        "gen1-commentary-barth-imago",
        "commentary",
        "Karl Barth on the Imago Dei",
        "gen.1.27",
        "Barth's Church Dogmatics III/1 §41 reads the imago Dei "
        "relationally rather than substantially. The verse \"male and "
        "female created He them\" is not appended to the imago claim "
        "incidentally — it constitutes it.\n\n"
        "The image of God, for Barth, is the relational form: I-Thou. "
        "Humanity images God by being-with-another. The substantive "
        "tradition (rationality, dominion, immortal soul) is set aside; "
        "the imago is the capacity for encounter, modeled after the "
        "intra-Trinitarian relation.\n\n"
        "This relational reading reshapes 20th-century theological "
        "anthropology and feminist theology.",
    ),
    rec(
        "gen1-reception-imago-history",
        "reception-history",
        "Imago Dei reception across 2,000 years",
        "gen.1.27",
        "The imago Dei has carried strikingly different meanings:\n\n"
        "  Irenaeus       — image (eikōn) vs likeness (homoiōsis): "
        "image is structural, likeness is achieved through grace.\n\n"
        "  Augustine      — image in the rational soul; tripartite "
        "(memory, understanding, will) mirroring the Trinity.\n\n"
        "  Aquinas        — image in intellect and will (faculties of "
        "knowing and loving).\n\n"
        "  Reformation    — emphasized loss of the image at the Fall; "
        "restoration through Christ.\n\n"
        "  Modern critical — focuses on the original ANE royal "
        "background: kings as images of gods. Imago dei democratizes "
        "kingship to all humans.\n\n"
        "  Feminist       — recovers the \"male and female\" reading; "
        "the imago belongs to humanity as relational, not to males "
        "alone.\n\n"
        "  Liberation     — humanity as imago grounds the dignity of "
        "the poor.\n\n"
        "[Navigable timeline placeholder — reception across periods.]",
    ),
    rec(
        "gen1-reconstruction-priestly",
        "reconstruction",
        "Behind the text — the Priestly source",
        "gen.1.27",
        "Critical scholarship since Wellhausen has located Genesis 1 "
        "in the Priestly source (P), distinguished from the Yahwist (J) "
        "creation account that begins at Genesis 2:4b. The Priestly "
        "version is dated to the Babylonian exile or shortly after "
        "(6th century BCE).\n\n"
        "Reconstructed features of the P creation account:\n"
        "  - Cosmological-temple framework (7 days = Tabernacle commission)\n"
        "  - Theological purpose: re-grounding Israelite identity after\n"
        "    Babylonian exile by claiming creation itself as Israel's\n"
        "    God's domain.\n"
        "  - Liturgical use likely: Sabbath-grounding text recited\n"
        "    weekly.\n\n"
        "The reconstruction is a working hypothesis, not a recovered "
        "manuscript. The text we have is the canonical form; the P "
        "source is a scholar's reconstruction behind it.",
    ),

    # ─ Verse 1:31 (closing) ──────────────────────────────────
    rec(
        "gen1-audio-cantillation",
        "audio",
        "Cantillation of Gen 1:31 — Friday evening trope",
        "gen.1.31",
        "Genesis 1:31 closes the work of creation: \"And God saw every "
        "thing that he had made, and, behold, it was very good. And "
        "the evening and the morning were the sixth day.\"\n\n"
        "In Jewish liturgical practice, this verse is read at the "
        "Friday evening service — the Sabbath-eve threshold — using "
        "the traditional Torah cantillation marks (teʿāmîm). The "
        "melodic line carries an exegetical function: the pauses, "
        "rises, and falls signal phrase boundaries that determine "
        "meaning.\n\n"
        "[Audio player placeholder — traditional Ashkenazic and "
        "Sephardic recordings of Gen 1:31 cantillation.]",
    ),
]


def main():
    with DATA.open(encoding="utf-8") as f:
        data = json.load(f)
    existing = data.get("genealogy", [])
    ids = {r["id"] for r in existing}
    added = 0
    for r in NEW_RECORDS:
        if r["id"] in ids:
            continue
        existing.append(r)
        added += 1
    data["genealogy"] = existing
    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Added {added} new records (skipped {len(NEW_RECORDS) - added} duplicates).")
    print(f"Total records: {len(existing)}.")


if __name__ == "__main__":
    main()
