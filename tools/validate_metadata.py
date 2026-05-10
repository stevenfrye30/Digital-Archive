#!/usr/bin/env python3
"""
validate_metadata.py — Validate all text.json metadata before export.

Checks every text.json in the canonical library against the schema contract.
Reports errors (must fix) and warnings (should fix) per text.

Run before export or large-scale ingestion:
    python 05_scripts/validate_metadata.py
"""

import json
import sys
from pathlib import Path

from issue_logger import log_issue as _log_issue

ROOT      = Path(__file__).parent.parent
TEXTS_DIR = ROOT / "01_library" / "library" / "texts"

# ── Closed value sets ────────────────────────────────────────────────────────

VALID_COLLECTIONS = {"sacred", "other"}

VALID_TRADITIONS = {
    # Religious / spiritual
    "Buddhist", "Christian", "Hindu", "Islam", "Jewish",
    "Sikh", "Jain", "Zoroastrian", "Taoist", "Confucian", "Shinto",
    # Cross-tradition / broader philosophical
    "Mohist", "Legalist", "Greek Philosophy", "Stoic", "Greek Literature", "Political Philosophy", "Modern Philosophy", "Chinese Strategy", "Persian Literature", "Japanese Philosophy", "Roman Philosophy", "Comparative Religion",
    # Syncretic / cross-tradition
    "Gnostic", "Hermetic", "Bahai", "Mandaean", "Theosophy", "Rastafari",
    "Tibetan Buddhist",
    # Mythological / folk
    "Greek", "Norse", "Egyptian", "Mesopotamian", "Celtic", "Finnish", "Mesoamerican",
    "Slavic", "Witchcraft / Folk Religion",
    # Null for secular
    None,
}

VALID_CATEGORIES = {
    "Scripture", "Philosophy", "Ethics", "Literature",
    "History", "Theology", "Mythology", "Commentary", "Law",
    "Poetry", "Science", "Folklore",
    # Added after metadata audit — legitimate categories used in the corpus
    "Folk Literature", "Scholarship", "Biography", "Treatise",
    "Scripture / Hagiography", "Scripture / Folklore", "Folk Religion",
    "Hagiography", "Education", "Travel Narrative", "Travel / Memoir",
    "Rhetoric", "Mysticism", "Epic Poetry", "Autobiography", "Anthology",
    "Apologetic",
    # Added 2026-05-10 — single legitimate use in `prayers-middle-ages`
    "Devotional",
}

VALID_SOURCE_QUALITY = {"clean", "acceptable", "provisional", "poor"}

# Publisher strings or URL domains that map to known sources.
# The export pipeline resolves these to source IDs.
KNOWN_PUBLISHERS = {
    "eBible.org", "Project Gutenberg", "SacredTexts.com",
    "Suttacentral", "Tanzil.net", "Peshitta.org",
    "Internet Archive", "openlibrary.org", "ctext.org",
    # Added 2026-05-10 — Christian Classics Ethereal Library, used by ~18 texts
    "CCEL",
    # Added 2026-05-10 — small Gnostic / early-Christian sources, 1–2 texts each
    "Nag Hammadi Library", "Early Christian Writings", "gnosis.org",
}

KNOWN_URL_DOMAINS = {
    "ebible.org", "gutenberg.org", "sacred-texts.com",
    "suttacentral.net", "tanzil.net", "archive.org", "openlibrary.org",
    "ctext.org",
    "ccel.org",
}


# ── Validation ───────────────────────────────────────────────────────────────

def validate_text(meta, path):
    """Validate a single text.json. Returns (errors, warnings)."""
    errors   = []
    warnings = []
    rel = path.relative_to(ROOT)

    def err(msg):  errors.append(f"  ERROR  {rel}: {msg}")
    def warn(msg): warnings.append(f"  WARN   {rel}: {msg}")

    # ── Required top-level fields ────────────────────────────────────────

    for field in ("id", "collection", "title", "description", "hierarchy"):
        if field not in meta or meta[field] is None:
            err(f"missing required field '{field}'")

    # id: must be lowercase slug
    text_id = meta.get("id", "")
    if text_id and text_id != text_id.lower():
        err(f"id '{text_id}' must be lowercase")
    if text_id and " " in text_id:
        err(f"id '{text_id}' must not contain spaces (use hyphens)")

    # collection: closed set
    col = meta.get("collection")
    if col and col not in VALID_COLLECTIONS:
        err(f"collection '{col}' not in {VALID_COLLECTIONS}")

    # tradition: closed set
    tradition = meta.get("tradition")
    if tradition is not None and tradition not in VALID_TRADITIONS:
        err(f"tradition '{tradition}' not in allowed set — add to VALID_TRADITIONS if legitimate")

    # category
    cat = meta.get("category")
    if not cat:
        warn("missing category")
    elif cat not in VALID_CATEGORIES:
        warn(f"category '{cat}' not in standard set — add to VALID_CATEGORIES if legitimate")

    # author: must be array, never null
    author = meta.get("author")
    if author is None:
        err("author must be [] (empty array), not null or missing")
    elif not isinstance(author, list):
        err(f"author must be array, got {type(author).__name__}")

    # hierarchy: array of 1-4 strings (1 = flat text with no group structure)
    hier = meta.get("hierarchy", [])
    if not isinstance(hier, list) or len(hier) < 1 or len(hier) > 4:
        err(f"hierarchy must be array of 1-4 strings, got {hier}")

    # ── Translations ─────────────────────────────────────────────────────

    translations = meta.get("translations", [])
    if not translations:
        err("no translations defined")

    seen_tr_ids = set()
    for i, tr in enumerate(translations):
        tr_label = f"translations[{i}]"

        # id
        tr_id = tr.get("id")
        if not tr_id:
            err(f"{tr_label}: missing id")
        elif tr_id in seen_tr_ids:
            err(f"{tr_label}: duplicate translation id '{tr_id}'")
        else:
            seen_tr_ids.add(tr_id)

        # language
        lang = tr.get("language")
        if not lang:
            err(f"{tr_label}: missing language")
        elif len(lang) > 5 and "+" not in lang:
            warn(f"{tr_label}: language '{lang}' looks non-standard (expected ISO 639)")

        # translator
        translator = tr.get("translator")
        if translator is None or (isinstance(translator, list) and len(translator) == 0):
            warn(f"{tr_label}: empty translator — provide group/committee name if no individual")
        elif not isinstance(translator, list):
            err(f"{tr_label}: translator must be array, got {type(translator).__name__}")

        # source object
        src = tr.get("source", {})
        if not src:
            err(f"{tr_label}: missing source object")
            continue

        publisher = src.get("publisher")
        url       = src.get("url", "")

        if not publisher:
            err(f"{tr_label}: missing source.publisher")
        else:
            # Check if publisher or URL maps to a known source
            pub_known = publisher in KNOWN_PUBLISHERS
            url_known = any(d in url for d in KNOWN_URL_DOMAINS) if url else False
            if not pub_known and not url_known:
                warn(f"{tr_label}: publisher '{publisher}' not in known set — "
                     "export will generate a fallback source ID")

        if not url:
            warn(f"{tr_label}: missing source.url")

        # year
        year = src.get("year")
        if year is not None and not isinstance(year, int):
            err(f"{tr_label}: source.year must be int or null, got {type(year).__name__}")

        # passages_file
        pf = tr.get("passages_file")
        if not pf:
            err(f"{tr_label}: missing passages_file")

    # ── Optional field quality checks ────────────────────────────────────

    if not meta.get("date"):
        warn("missing date")

    # Distinguish missing key from explicit null — explicit null means
    # "verified unknown," missing means "nobody thought about it."
    if "original_title" not in meta and col == "sacred":
        warn("sacred text missing original_title — set to null explicitly if truly unknown")

    # source_quality: optional classification
    sq = meta.get("source_quality")
    if sq is not None and sq not in VALID_SOURCE_QUALITY:
        err(f"source_quality '{sq}' not in {VALID_SOURCE_QUALITY}")
    if sq is None:
        warn("missing source_quality — classify as clean/acceptable/provisional/poor")

    # source_notes: optional string
    sn = meta.get("source_notes")
    if sn is not None and not isinstance(sn, str):
        err(f"source_notes must be string, got {type(sn).__name__}")

    return errors, warnings


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    total_errors   = 0
    total_warnings = 0
    texts_checked  = 0

    for text_json in sorted(TEXTS_DIR.rglob("text.json")):
        try:
            meta = json.loads(text_json.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ERROR  {text_json.relative_to(ROOT)}: cannot parse JSON: {e}")
            total_errors += 1
            continue

        texts_checked += 1
        errors, warnings = validate_text(meta, text_json)
        total_errors   += len(errors)
        total_warnings += len(warnings)

        rel = str(text_json.relative_to(ROOT))
        for msg in errors:
            print(msg)
            _log_issue("error", "validation", rel,
                       text_id=meta.get("id"), issue_type="schema_error",
                       message=msg.strip())
        for msg in warnings:
            print(msg)
            _log_issue("warning", "validation", rel,
                       text_id=meta.get("id"), issue_type="schema_warning",
                       message=msg.strip())

    print()
    print(f"Checked {texts_checked} texts")
    print(f"  {total_errors} errors (must fix before export)")
    print(f"  {total_warnings} warnings (should fix)")

    if total_errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
