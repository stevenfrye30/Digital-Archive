"""Retrofit the 22 Genesis 1 calibration records with provenance
fields: authority / tradition / source_basis / confidence.

Honest classification — most chamber bodies are archive editorial
synthesis (tertiary). Only direct artifacts, manuscript texts,
canonical citations, and direct liturgical/cultural recordings
are primary. Scholarly theses being represented in summary are
secondary.

Idempotent: re-running overwrites the four fields.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "bible_kjv.json"


# Map record id → (authority, tradition, source_basis, confidence)
PROV = {
    # ── PRIMARY — direct artifacts / canonical texts ──
    "dore-creation-of-light": (
        "primary",
        "19th-century French biblical illustration",
        "Gustave Doré, La Sainte Bible (Mame, Tours, 1866)",
        "Direct artifact — engraving reproduction",
    ),
    "gen1-manuscript-opening": (
        "primary",
        "Textual criticism — major manuscript traditions",
        "Masoretic (BHS); Septuagint (Rahlfs); Samaritan Pentateuch; Vulgate",
        "Direct textual evidence — manuscript readings",
    ),
    "gen1-xref-nt-creation": (
        "primary",
        "Canonical intertextuality",
        "John 1:1-3; Hebrews 11:3; Colossians 1:15-17 (KJV)",
        "Direct canonical citations",
    ),
    "gen1-ritual-maariv-aravim": (
        "primary",
        "Jewish liturgical tradition (Siddur)",
        "Standard Ashkenazic/Sephardic siddur — Ma'ariv ʿarāḇîm blessing",
        "Direct liturgical text",
    ),
    "gen1-audio-cantillation": (
        "primary",
        "Jewish cantillation tradition (teʿāmîm)",
        "Ashkenazic / Sephardic Torah trope traditions",
        "Direct cultural recording — placeholder pending audio asset",
    ),

    # ── SECONDARY — scholarly theses / reconstructions ──
    "gen1-architecture-cosmic-temple": (
        "secondary",
        "Cosmic-temple thesis (modern OT scholarship)",
        "Walton, J., The Lost World of Genesis One; Levenson, J., Creation and the Persistence of Evil",
        "Interpretive model — represents a major scholarly proposal",
    ),
    "gen1-map-ane-constellations": (
        "secondary",
        "Ancient astronomy / biblical Hebrew lexicography",
        "MUL.APIN tablets (c. 1000 BCE); Hartmann, Wright on biblical constellation names",
        "Scholarly reconstruction of ancient Near Eastern sky",
    ),
    "gen1-artifact-tanninim": (
        "secondary",
        "Comparative ANE mythology",
        "Tiamat (Enuma Elish); Lotan (Ugaritic Baal Cycle); Apep (Egyptian)",
        "Comparative-religion interpretation",
    ),
    "gen1-reconstruction-priestly": (
        "secondary",
        "Source criticism — Documentary Hypothesis",
        "Wellhausen, Prolegomena (1883); modern P-source scholarship",
        "Scholarly reconstruction — working hypothesis",
    ),
}


# ── TERTIARY — archive editorial synthesis ──
TERTIARY_RECORDS = {
    "cain-seth-divergence": (
        "Hebrew Bible genealogy — Cain and Seth lines",
        "Genesis 4-5; standard genealogical tradition",
        "Archive editorial synthesis",
    ),
    "shem-to-terah": (
        "Hebrew Bible genealogy — Shem to Terah",
        "Genesis 11:10-26; standard genealogical tradition",
        "Archive editorial synthesis",
    ),
    "noah-sons": (
        "Hebrew Bible genealogy — Sons of Noah",
        "Genesis 6:10; 10:1",
        "Archive editorial synthesis",
    ),
    "terah-abram": (
        "Hebrew Bible genealogy — Terah's house",
        "Genesis 11:27-32",
        "Archive editorial synthesis",
    ),
    "lot-moab-ammon": (
        "Hebrew Bible genealogy — Moab and Ammon descent",
        "Genesis 19:30-38",
        "Archive editorial synthesis",
    ),
    "isaac-ishmael": (
        "Hebrew Bible genealogy — Isaac and Ishmael",
        "Genesis 16, 21, 25",
        "Archive editorial synthesis",
    ),
    "nahor-house": (
        "Hebrew Bible genealogy — Nahor's house",
        "Genesis 22:20-24",
        "Archive editorial synthesis",
    ),
    "jacob-esau": (
        "Hebrew Bible genealogy — Jacob and Esau",
        "Genesis 25-27",
        "Archive editorial synthesis",
    ),
    "jacob-sons-by-mother": (
        "Hebrew Bible genealogy — Jacob's twelve sons by mother",
        "Genesis 29-30, 35",
        "Archive editorial synthesis",
    ),
    "esau-edom": (
        "Hebrew Bible genealogy — Edom",
        "Genesis 36",
        "Archive editorial synthesis",
    ),
    "ephraim-manasseh-adopted": (
        "Hebrew Bible genealogy — Ephraim and Manasseh adopted",
        "Genesis 48",
        "Archive editorial synthesis",
    ),
    # Other Genesis 1 records that are archive editorial synthesis
    "gen1-cosmology-ane": (
        "Ancient Near Eastern cosmology — synthesis",
        "Drawn from Enuma Elish, Egyptian cosmologies, biblical text",
        "Interpretive archive synthesis — reconstructed worldview",
    ),
    "gen1-linguistic-bereshit": (
        "Biblical Hebrew lexicography and Rashi's reading",
        "BDB lexicon; Rashi on Genesis 1:1; modern translations (KJV, NJPS, NRSV)",
        "Archive synthesis of grammatical and exegetical positions",
    ),
    "gen1-commentary-augustine": (
        "Western patristic theological tradition",
        "Augustine of Hippo, Confessions XI; City of God XI",
        "Archive editorial summary of primary text",
    ),
    "gen1-linguistic-tohu": (
        "Biblical Hebrew lexicography; comparative ANE",
        "BDB lexicon on tōhû / bōhû; Babylonian Tiamat tradition",
        "Archive synthesis of lexical and comparative positions",
    ),
    "gen1-reception-ruach": (
        "Cross-traditional reception (Christian / critical / Jewish mystical)",
        "Patristic readings; modern critical scholarship; Kabbalistic tradition",
        "Archive survey across traditions",
    ),
    "gen1-cosmology-light-before-luminaries": (
        "Rabbinic / patristic / critical scholarship",
        "Genesis Rabbah 3:6; Basil's Hexaemeron; Augustine; modern source criticism",
        "Archive survey of competing readings",
    ),
    "gen1-cosmology-firmament": (
        "Ancient Hebrew cosmology",
        "Biblical Hebrew lexicography on rāqîaʿ; ANE three-tier cosmos studies",
        "Archive synthesis — reconstructed cosmological model",
    ),
    "gen1-commentary-philo": (
        "Hellenistic Jewish philosophy / Platonism",
        "Philo of Alexandria, De Opificio Mundi (c. 1st cent CE)",
        "Archive editorial summary of primary text",
    ),
    "gen1-timeline-calendar": (
        "Historical-critical scholarship on the Priestly source",
        "Standard source-critical dating (6th century BCE Priestly source)",
        "Archive historical-contextual note",
    ),
    "gen1-commentary-aquinas": (
        "Scholastic theology / Thomistic synthesis",
        "Aquinas, Summa Theologiae I.q.69 (c. 1265-1273)",
        "Archive editorial summary of primary text",
    ),
    "gen1-linguistic-naaseh-adam": (
        "Biblical Hebrew grammar; Jewish and Christian exegetical traditions",
        "BDB on cohortative plural; Rashi; Christian Trinitarian readings; modern critical",
        "Archive survey of competing readings",
    ),
    "gen1-commentary-barth-imago": (
        "20th-century systematic theology (Reformed)",
        "Karl Barth, Church Dogmatics III/1 §41 (1945)",
        "Archive editorial summary of primary text",
    ),
    "gen1-reception-imago-history": (
        "Cross-traditional reception of imago Dei",
        "Irenaeus, Augustine, Aquinas, Reformation, modern critical, feminist, liberation",
        "Archive survey across 2,000 years of reception",
    ),
}


def main():
    with DATA.open(encoding="utf-8") as f:
        data = json.load(f)
    records = data.get("genealogy", [])

    updated = 0

    for r in records:
        rid = r["id"]
        if rid in PROV:
            authority, tradition, source_basis, confidence = PROV[rid]
            r["authority"] = authority
            r["tradition"] = tradition
            r["source_basis"] = source_basis
            r["confidence"] = confidence
            updated += 1
        elif rid in TERTIARY_RECORDS:
            tr, sb, conf = TERTIARY_RECORDS[rid]
            r["authority"] = "tertiary"
            r["tradition"] = tr
            r["source_basis"] = sb
            r["confidence"] = conf
            updated += 1
        else:
            # Records outside the classified set — default to tertiary
            # archive synthesis (our own authored summaries).
            r["authority"] = "tertiary"
            r["tradition"] = "Archive editorial layer"
            r["source_basis"] = "Multiple sources — see record body"
            r["confidence"] = "Archive editorial synthesis"
            updated += 1

    data["genealogy"] = records
    with DATA.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated provenance on {updated} records.")

    # Summary by authority
    from collections import Counter
    auth_counts = Counter(r.get("authority", "?") for r in records)
    gen1_auth = Counter(
        r.get("authority", "?") for r in records
        if any(a.get("target", "").split("::").pop().startswith("gen.1.")
               for a in r.get("anchors", []))
    )
    print(f"\nAll records by authority: {dict(auth_counts)}")
    print(f"Genesis 1 by authority:    {dict(gen1_auth)}")


if __name__ == "__main__":
    main()
