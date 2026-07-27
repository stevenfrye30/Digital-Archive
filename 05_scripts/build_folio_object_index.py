"""Build BIBLE_FOLIO_OBJECT_INDEX.md — a human-readable index of
all folio/Codex objects currently anchored to the Bible, organized
by canonical order.

Pulls from data/bible_kjv.json. For each chapter that carries
records, lists the records with title, anchor verse, authority,
kind, optional Codex Object siglum, and a short role line.

Not a feature. An editorial-planning reference document.
"""
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "bible_kjv.json"
OUT = ROOT / "BIBLE_FOLIO_OBJECT_INDEX.md"

# Canonical book order — Protestant Bible (Hebrew Bible + NT).
CANON = [
    ("gen", "Genesis"),       ("exo", "Exodus"),
    ("lev", "Leviticus"),     ("num", "Numbers"),
    ("deu", "Deuteronomy"),   ("jos", "Joshua"),
    ("jdg", "Judges"),        ("rut", "Ruth"),
    ("1sa", "1 Samuel"),      ("2sa", "2 Samuel"),
    ("1ki", "1 Kings"),       ("2ki", "2 Kings"),
    ("1ch", "1 Chronicles"),  ("2ch", "2 Chronicles"),
    ("ezr", "Ezra"),          ("neh", "Nehemiah"),
    ("est", "Esther"),        ("job", "Job"),
    ("psa", "Psalms"),        ("pro", "Proverbs"),
    ("ecc", "Ecclesiastes"),  ("sng", "Song of Songs"),
    ("isa", "Isaiah"),        ("jer", "Jeremiah"),
    ("lam", "Lamentations"),  ("eze", "Ezekiel"),
    ("dan", "Daniel"),        ("hos", "Hosea"),
    ("joe", "Joel"),          ("amo", "Amos"),
    ("oba", "Obadiah"),       ("jon", "Jonah"),
    ("mic", "Micah"),         ("nah", "Nahum"),
    ("hab", "Habakkuk"),      ("zep", "Zephaniah"),
    ("hag", "Haggai"),        ("zec", "Zechariah"),
    ("mal", "Malachi"),       ("mat", "Matthew"),
    ("mrk", "Mark"),          ("luk", "Luke"),
    ("jhn", "John"),          ("act", "Acts"),
    ("rom", "Romans"),        ("1co", "1 Corinthians"),
    ("2co", "2 Corinthians"), ("gal", "Galatians"),
    ("eph", "Ephesians"),     ("php", "Philippians"),
    ("col", "Colossians"),    ("1th", "1 Thessalonians"),
    ("2th", "2 Thessalonians"),("1ti", "1 Timothy"),
    ("2ti", "2 Timothy"),     ("tit", "Titus"),
    ("phm", "Philemon"),      ("heb", "Hebrews"),
    ("jas", "James"),         ("1pe", "1 Peter"),
    ("2pe", "2 Peter"),       ("1jo", "1 John"),
    ("2jo", "2 John"),        ("3jo", "3 John"),
    ("jud", "Jude"),          ("rev", "Revelation"),
]
BOOK_ORDER = {abbr: i for i, (abbr, _) in enumerate(CANON)}
BOOK_NAMES = {abbr: name for abbr, name in CANON}

# A short editorial role line per record — what role the record
# plays in the codex, in the manuscript editor's own voice. Kept
# brief because the index is for planning, not exegesis.
ROLES = {
    # Codex Objects
    "gen1-cosmology-firmament":
        "AO·001 cosmology — Firmament chamber; the ANE three-tier cosmos.",
    "gen1-firmament-translation-tradition":
        "AO·002 translation tradition — manuscript-witness chamber across Hebrew/Greek/Latin/English.",
    "gen5-antediluvian-line":
        "AO·003 genealogy — Adam → Noah Sethite line; the canon's first lineage chamber.",
    "gen2-sabbath-pattern":
        "AO·004 sacred time — sevenfold rhythm; Sabbath through the canon.",
    "gen2-sacred-mountain":
        "AO·005 symbolic motif — vertical mountain stack from Eden to the eschatological summit.",
    "gen17-covenant-formula":
        "AO·006 covenant formula — 'I will be your God; you shall be my people' across the testaments.",
    "prov1-wisdom-fear":
        "AO·007 wisdom saying — 'fear of the LORD' as the wisdom corpus's gathering phrase.",
    "isa6-opened-heavens":
        "AO·008 revelatory vision — throne disclosure tradition (Isa 6 / Eze 1 / Dan 7 / Rev 4).",
    "psa13-lament-cry":
        "AO·009 lament structure — 'how long, O LORD?' lament-shape.",
    "joh1-incarnation-dwelling":
        "AO·010 incarnational presence — tent, temple, flesh.",
    "eze37-bones-breath":
        "AO·011 resurrection-renewal — valley of bones; emergence; resurrection body.",
    "exo40-sanctuary-glory":
        "AO·012 sacred space — layered sanctuary; tabernacle / temple / heavenly sanctuary.",
}

# Authority symbols for visual density.
AUTH_GLYPH = {
    "primary":   "●",
    "secondary": "◐",
    "tertiary":  "○",
}


def chapter_key(pid):
    parts = pid.split(".")
    if len(parts) < 2:
        return None, None, None
    try:
        ch = int(parts[1])
    except ValueError:
        return None, None, None
    try:
        v = int(parts[2]) if len(parts) >= 3 else 0
    except ValueError:
        v = 0
    return parts[0], ch, v


def main():
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)

    # Index records by (book, chapter); each record may anchor
    # multiple verses but each appearance gets its own row.
    by_chapter = defaultdict(list)
    for rec in data.get("genealogy", []):
        for anchor in (rec.get("anchors") or []):
            target = (anchor or {}).get("target", "")
            pid = target.split("::")[-1] if target else ""
            book, ch, v = chapter_key(pid)
            if not book or ch is None:
                continue
            by_chapter[(book, ch)].append((v, pid, rec))

    # Sort each chapter's records by verse, then title for stability.
    for k in by_chapter:
        by_chapter[k].sort(key=lambda x: (x[0], (x[2].get("title") or "")))

    total_records = sum(
        1 for r in data.get("genealogy", []) for _ in (r.get("anchors") or [])
    )
    distinct_records = len(data.get("genealogy", []))
    chapters_with_records = len(by_chapter)
    chapter_counts = sorted(by_chapter.keys(), key=lambda k: (BOOK_ORDER.get(k[0], 999), k[1]))

    lines = []
    push = lines.append

    push("# Bible — Folio Object Index")
    push("")
    push(
        "*Auto-generated from `data/bible_kjv.json`. "
        "Run `05_scripts/build_folio_object_index.py` to regenerate.*"
    )
    push("")
    push(
        "A human-readable register of every record currently "
        "anchored to a verse in the Bible. Codex Objects, "
        "commentary, architecture, plates, and patriarchal "
        "wave-one additions are listed together, grouped by the "
        "chapter they touch. Authority class is shown by glyph:"
    )
    push("")
    push("- ● primary — canonical anchor")
    push("- ◐ secondary — substantial scholarly witness")
    push("- ○ tertiary — quiet marginal gloss")
    push("")
    push(
        f"**Totals.** {distinct_records} distinct records · "
        f"{total_records} anchor entries (one record may anchor "
        f"multiple verses) · {chapters_with_records} chapters "
        f"touched across the Bible."
    )
    push("")
    push("---")
    push("")
    push("## Summary by book")
    push("")
    push("| Book | Chapters touched | Anchors |")
    push("|------|-----------------:|--------:|")
    book_totals = defaultdict(lambda: [0, 0])  # [chapters_with_records, anchors]
    for (book, ch), recs in by_chapter.items():
        book_totals[book][0] += 1
        book_totals[book][1] += len(recs)
    for abbr, name in CANON:
        if abbr in book_totals:
            ch_count, anchor_count = book_totals[abbr]
            push(f"| {name} | {ch_count} | {anchor_count} |")
    push("")
    push("---")
    push("")
    push("## Detailed register (by canonical order)")
    push("")

    prev_book = None
    for (book, ch) in chapter_counts:
        if book != prev_book:
            push(f"### {BOOK_NAMES.get(book, book.title())}")
            push("")
            prev_book = book
        push(f"#### {BOOK_NAMES.get(book, book.title())} {ch}")
        push("")
        for (v, pid, rec) in by_chapter[(book, ch)]:
            title = (rec.get("title") or "").strip()
            kind = (rec.get("kind") or "").strip()
            authority = (rec.get("authority") or "tertiary").strip()
            ao_block = rec.get("atlas_object") or {}
            siglum = (ao_block.get("siglum") or "").strip()
            anchor_label = f"{BOOK_NAMES.get(book, book)} {ch}:{v}" if v else f"{BOOK_NAMES.get(book, book)} {ch}"
            glyph = AUTH_GLYPH.get(authority, "·")
            siglum_part = f" · **{siglum}**" if siglum else ""
            role = ROLES.get(rec.get("id"), "")
            kind_part = f" *{kind}*" if kind else ""
            push(
                f"- {glyph} **{title}** — {anchor_label} · {authority}{kind_part}{siglum_part}"
            )
            if role:
                push(f"  - {role}")
            else:
                # Fall back to a short trim of the body's first sentence
                body = (rec.get("body") or "").strip()
                if body:
                    # First sentence (up to ~140 chars).
                    first = re.split(r"(?<=[.!?])\s+", body, maxsplit=1)[0]
                    if len(first) > 200:
                        first = first[:200].rstrip() + "..."
                    push(f"  - {first}")
        push("")

    push("---")
    push("")
    push("## Silent regions")
    push("")
    push(
        "Chapters or books without any currently anchored "
        "record. The codex's restraint here is intentional; "
        "this list is editorial context, not a worklist."
    )
    push("")
    silent_books = []
    for abbr, name in CANON:
        if abbr not in book_totals:
            silent_books.append(name)
    if silent_books:
        push("**Silent books (no anchored records):**")
        push("")
        for name in silent_books:
            push(f"- {name}")
        push("")
    push(
        "*Per-chapter silences within partially-served books "
        "are visible above: any chapter not listed under its "
        "book's section currently has no anchor.*"
    )
    push("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"  · {distinct_records} distinct records")
    print(f"  · {total_records} anchor entries")
    print(f"  · {chapters_with_records} chapters touched")
    print(f"  · {len(silent_books)} silent books")


if __name__ == "__main__":
    main()
