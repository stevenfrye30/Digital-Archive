#!/usr/bin/env python3
"""
corpus_audit.py — Three-layer diagnostic audit for the Digital Archive.

Produces structured, JSON-serializable reports for:
  1. Duplicate-ID structural triage
  2. Front-matter recovery candidates
  3. Short-stub passage classification

This is DIAGNOSIS ONLY — no passages are modified, deleted, or rewritten.

Usage:
    python 05_scripts/corpus_audit.py                   # run all three audits
    python 05_scripts/corpus_audit.py --audit dup       # duplicate IDs only
    python 05_scripts/corpus_audit.py --audit fm        # front matter only
    python 05_scripts/corpus_audit.py --audit stub      # short stubs only
    python 05_scripts/corpus_audit.py --json            # JSON output
    python 05_scripts/corpus_audit.py --out report.json # save to file

Output structure (all three audits):
    ARCHITECTURE → CODE → EXAMPLE_INVOCATION → EXAMPLE_OUTPUTS → INTEGRATION_NOTE
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent
DATA = ROOT / "03_web_app" / "data"
RAW_DIR = ROOT / "02_raw_sources" / "Library_"
LIBRARY = ROOT / "01_library" / "library" / "texts"

# Sources we treat as clean baselines — skip in most heuristics
CLEAN_SOURCES = {"suttacentral", "ebible", "tanzil", "peshitta", "ctext"}


# ═══════════════════════════════════════════════════════════════════════════════
# SHARED SCHEMA
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Passage:
    """Minimal passage representation for audit purposes."""
    text_id: str
    passage_id: str
    l1: Any       # path[0] — book / sutta / biography
    l2: Any       # path[1] — chapter / section
    l3: Any       # path[2] — verse (if 3-level)
    l4: Any       # path[3] — (if 4-level, usually None)
    text: str
    order: int
    source: str = ""
    data_file: str = ""   # uniquely identifies the translation file


def load_corpus() -> tuple[list[Passage], dict]:
    """Load all passages from the web-data index. Returns (passages, index_data).

    Deduplicates by `(text_id, data_file)`: when several index entries
    point at the same data file (e.g. three SacredTexts/Gutenberg Quran
    variants all publishing as `quran_anonymous.json`), the file is
    loaded once. Otherwise the same passages would be counted multiple
    times in the duplicate-id audit.
    """
    with open(DATA / "index.json", encoding="utf-8") as f:
        idx = json.load(f)

    source_map = {e["id"]: e.get("source", "unknown") for e in idx["texts"]}
    all_passages: list[Passage] = []
    seen: set[tuple[str, str]] = set()

    for entry in idx["texts"]:
        key = (entry["id"], entry["data_file"])
        if key in seen:
            continue
        seen.add(key)
        fpath = DATA / entry["data_file"]
        if not fpath.exists():
            continue
        with open(fpath, encoding="utf-8") as f:
            d = json.load(f)
        src = entry.get("source", "unknown")
        for p in d.get("passages", []):
            path = p.get("path", [])
            all_passages.append(Passage(
                text_id=entry["id"],
                passage_id=p.get("id", ""),
                l1=path[0] if len(path) > 0 else None,
                l2=path[1] if len(path) > 1 else None,
                l3=path[2] if len(path) > 2 else None,
                l4=path[3] if len(path) > 3 else None,
                text=p.get("text", ""),
                order=p.get("order", 0),
                source=src,
                data_file=entry["data_file"],
            ))

    return all_passages, idx


def group_by_text(passages: list[Passage]) -> dict[str, list[Passage]]:
    groups: dict[str, list[Passage]] = defaultdict(list)
    for p in passages:
        groups[p.text_id].append(p)
    return dict(groups)


# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT 1: DUPLICATE-ID STRUCTURAL TRIAGE
# ═══════════════════════════════════════════════════════════════════════════════

# Structural failure categories
DUP_CATEGORIES = [
    "missing_book_level",          # multi-book flattened to chapter+verse
    "missing_section_level",       # sections not tracked, chapters collide
    "appendix_collapse",           # appendix/comparison/commentary shares namespace
    "front_matter_absorbed",       # preface/intro passages got body IDs
    "repeated_generic_headers",    # generic "Chapter I" under different parents
    "counter_reset_no_parent",     # verse/section counter resets without new chapter
    "regex_partial_detection",     # some headers detected, others missed
    "unknown",
]

# Heading patterns that suggest a missed structural level
_HEADING_PATTERNS = [
    (re.compile(r'^BOOK\s+[IVXLCDM\d]+', re.I), "missing_book_level"),
    (re.compile(r'^PART\s+[IVXLCDM\d]+', re.I), "missing_section_level"),
    (re.compile(r'^CHAPTER\s+[IVXLCDM\d]+', re.I), "missing_section_level"),
    (re.compile(r'^SECTION\s+[IVXLCDM\d]+', re.I), "missing_section_level"),
    (re.compile(r'^LIFE OF\b', re.I), "missing_book_level"),
    (re.compile(r'^COMPARISON OF\b', re.I), "appendix_collapse"),
    (re.compile(r'^APPENDIX\b', re.I), "appendix_collapse"),
    (re.compile(r'^INTRODUCTION\b', re.I), "front_matter_absorbed"),
    (re.compile(r'^PREFACE\b', re.I), "front_matter_absorbed"),
    (re.compile(r'^COMMENTARY\b', re.I), "appendix_collapse"),
    (re.compile(r'^CANTO\s+[IVXLCDM\d]+', re.I), "missing_book_level"),
    (re.compile(r'^HYMN\s+[IVXLCDM\d]+', re.I), "missing_book_level"),
    (re.compile(r'^DIALOGUE\s+[IVXLCDM\d]+', re.I), "missing_book_level"),
    (re.compile(r'^TREATISE\b', re.I), "missing_book_level"),
    (re.compile(r'^VOLUME\s+[IVXLCDM\d]+', re.I), "missing_book_level"),
    (re.compile(r'^[IVXLCDM]+\.\s*$'), "regex_partial_detection"),
]

# Short heading-like patterns
_SHORT_HEADING_RE = re.compile(r'^[A-Z][A-Z\s\.]{2,40}$')


def analyze_dup_ids(text_id: str, passages: list[Passage]) -> dict | None:
    """Analyze duplicate IDs for one text. Returns report dict or None if no dups."""
    id_counts = Counter(p.passage_id for p in passages)
    dup_ids = {pid: cnt for pid, cnt in id_counts.items() if cnt > 1}
    if not dup_ids:
        return None

    total_excess = sum(c - 1 for c in dup_ids.values())

    # ── Collect duplicate clusters ──────────────────────────────────────
    clusters: list[dict] = []
    for pid in sorted(dup_ids.keys(), key=lambda x: -dup_ids[x])[:20]:
        instances = [p for p in passages if p.passage_id == pid]
        cluster = {
            "id": pid,
            "count": len(instances),
            "paths": [{"l1": p.l1, "l2": p.l2, "l3": p.l3} for p in instances[:5]],
            "texts_preview": [p.text[:80] for p in instances[:5]],
        }
        clusters.append(cluster)

    # ── Heuristic scoring per category ──────────────────────────────────
    scores: dict[str, float] = {cat: 0.0 for cat in DUP_CATEGORIES}

    # Signal 1: heading-like text in passages near dup transitions
    heading_signals: list[str] = []
    for p in passages:
        if len(p.text) <= 60 and _SHORT_HEADING_RE.match(p.text.strip()):
            for pat, cat in _HEADING_PATTERNS:
                if pat.match(p.text.strip()):
                    scores[cat] += 1.0
                    heading_signals.append(f"{cat}: {p.text.strip()[:50]}")
                    break

    # Signal 2: l1 field is constant across all passages (no book level)
    l1_values = set(p.l1 for p in passages)
    if len(l1_values) == 1 and len(passages) > 100:
        scores["missing_book_level"] += 3.0

    # Signal 3: l2 counter resets multiple times
    l2_resets = 0
    prev_l2 = None
    for p in passages:
        if prev_l2 is not None and isinstance(p.l2, int) and isinstance(prev_l2, int):
            if p.l2 < prev_l2:
                l2_resets += 1
        prev_l2 = p.l2
    if l2_resets > 2:
        scores["missing_book_level"] += l2_resets * 0.5
    if l2_resets == 1:
        scores["appendix_collapse"] += 1.0

    # Signal 4: most dups are at low chapter/verse numbers (1.1, 1.2, etc.)
    low_id_dups = sum(1 for pid in dup_ids if pid.startswith("1."))
    if low_id_dups > len(dup_ids) * 0.3:
        scores["missing_book_level"] += 2.0

    # Signal 5: front matter keywords in early passages
    early = passages[:20]
    fm_keywords = sum(1 for p in early
                      if re.match(r'^(?:PREFACE|INTRODUCTION|FOREWORD|CONTENTS)', p.text, re.I))
    if fm_keywords > 0:
        scores["front_matter_absorbed"] += fm_keywords * 1.5

    # Signal 6: very few distinct l1 values relative to dup count
    if len(l1_values) < 3 and total_excess > 50:
        scores["missing_book_level"] += 2.0

    # Normalize and rank
    total_score = sum(scores.values()) or 1.0
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    top_cat = ranked[0][0] if ranked[0][1] > 0 else "unknown"
    confidence = min(1.0, ranked[0][1] / total_score) if total_score > 0 else 0.0

    # ── Recommended parser action ───────────────────────────────────────
    action_map = {
        "missing_book_level": "Switch to book_chapter parser; detect BOOK/PART/biography headers as level-1",
        "missing_section_level": "Add section-level detection for CHAPTER/SECTION headers within books",
        "appendix_collapse": "Detect appendix/comparison sections as separate book-level entries",
        "front_matter_absorbed": "Move prefatory passages to front_matter; start body after first chapter",
        "repeated_generic_headers": "Use parent context to disambiguate repeated 'Chapter I' headers",
        "counter_reset_no_parent": "Detect verse counter resets and infer missing parent boundary",
        "regex_partial_detection": "Expand chapter regex to catch variant formatting (missing periods, case)",
        "unknown": "Manual inspection required — no clear structural pattern detected",
    }

    return {
        "text_id": text_id,
        "source": passages[0].source if passages else "unknown",
        "total_passages": len(passages),
        "duplicate_id_count": total_excess,
        "unique_duplicated_ids": len(dup_ids),
        "l1_distinct_values": len(l1_values),
        "l2_resets": l2_resets,
        "top_category": top_cat,
        "confidence": round(confidence, 2),
        "category_scores": {k: round(v, 1) for k, v in ranked if v > 0},
        "heading_signals": heading_signals[:10],
        "top_clusters": clusters[:10],
        "recommended_action": action_map.get(top_cat, "Manual review"),
    }


def run_dup_id_audit(passages: list[Passage]) -> dict:
    """Run the duplicate-ID audit across all translations.

    Each translation file is audited independently. A multi-translation
    work like the Quran legitimately reuses the same `surah.ayah` ids
    across its translations; the old behaviour of grouping by `text_id`
    alone counted those reuse cases as duplicates and produced
    misleading totals (e.g. 158k for the Quran). Grouping by
    `(text_id, data_file)` makes each translation's parser audit
    independent, which is the truthful unit.

    The per-text-id report aggregates the worst translation per id, so
    the priority queue stays one-row-per-text and downstream tools
    (lint_archive, build_cleanliness_report) keep their existing shape.
    """
    by_translation: dict[tuple[str, str], list[Passage]] = defaultdict(list)
    for p in passages:
        by_translation[(p.text_id, p.data_file)].append(p)

    per_translation: list[dict] = []
    for (text_id, data_file), ps in sorted(by_translation.items()):
        if ps and ps[0].source in CLEAN_SOURCES:
            continue
        report = analyze_dup_ids(text_id, ps)
        if report:
            report["data_file"] = data_file
            per_translation.append(report)

    # Aggregate to one report per text_id by keeping the worst translation
    # (highest duplicate_id_count) and summing across all translations.
    per_text: dict[str, dict] = {}
    for r in per_translation:
        tid = r["text_id"]
        if tid not in per_text or r["duplicate_id_count"] > per_text[tid]["duplicate_id_count"]:
            # Keep the translation with the highest dup count as the representative
            per_text[tid] = dict(r)

    reports: list[dict] = list(per_text.values())

    # Sort by duplicate volume descending
    reports.sort(key=lambda r: -r["duplicate_id_count"])

    # Category summary
    cat_counts: dict[str, int] = Counter()
    cat_texts: dict[str, list[str]] = defaultdict(list)
    for r in reports:
        cat_counts[r["top_category"]] += 1
        cat_texts[r["top_category"]].append(r["text_id"])

    return {
        "audit": "duplicate_id_triage",
        "texts_affected": len(reports),
        "total_excess_duplicates": sum(r["duplicate_id_count"] for r in reports),
        "category_summary": [
            {"category": cat, "count": cnt, "texts": sorted(cat_texts[cat])}
            for cat, cnt in cat_counts.most_common()
        ],
        "priority_queue": [
            {"rank": i + 1, "text_id": r["text_id"], "dups": r["duplicate_id_count"],
             "category": r["top_category"], "confidence": r["confidence"],
             "action": r["recommended_action"]}
            for i, r in enumerate(reports[:20])
        ],
        "per_text_reports": reports,
        "review_packets": [
            {
                "text_id": r["text_id"],
                "suspected_category": r["top_category"],
                "why_flagged": f"{r['duplicate_id_count']} excess dups, "
                               f"{r['unique_duplicated_ids']} unique IDs affected, "
                               f"l1 has {r['l1_distinct_values']} distinct values, "
                               f"{r['l2_resets']} l2 resets",
                "representative_examples": [
                    {"id": c["id"], "count": c["count"],
                     "texts": c["texts_preview"][:3]}
                    for c in r["top_clusters"][:5]
                ],
                "heading_signals": r["heading_signals"][:5],
                "parser_fix_suggestion": r["recommended_action"],
            }
            for r in reports
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT 2: FRONT-MATTER RECOVERY
# ═══════════════════════════════════════════════════════════════════════════════

FM_CATEGORIES = [
    "title_page", "translator_attribution", "publication_imprint",
    "preface", "introduction", "contents", "argument_summary",
    "dedication", "prologue", "editorial_prefatory", "uncertain",
]

_FM_HEADER_RES = [
    (re.compile(r'^PREFACE', re.I), "preface"),
    (re.compile(r"^(?:AUTHOR'?S\s+)?PREFACE", re.I), "preface"),
    (re.compile(r"^(?:TRANSLATOR'?S\s+)?PREFACE", re.I), "preface"),
    (re.compile(r'^INTRODUCTION', re.I), "introduction"),
    (re.compile(r'^INTRODUCTORY', re.I), "introduction"),
    (re.compile(r'^FOREWORD', re.I), "preface"),
    (re.compile(r'^CONTENTS', re.I), "contents"),
    (re.compile(r'^TABLE OF CONTENTS', re.I), "contents"),
    (re.compile(r'^DEDICATION', re.I), "dedication"),
    (re.compile(r'^PROLOGUE', re.I), "prologue"),
    (re.compile(r'^ARGUMENT', re.I), "argument_summary"),
    (re.compile(r'^ADVERTISEMENT', re.I), "editorial_prefatory"),
    (re.compile(r"^(?:EDITOR'?S|TRANSLATOR'?S)\s+NOTE", re.I), "editorial_prefatory"),
    (re.compile(r"^TRANSCRIBER'?S\s+NOTE", re.I), "editorial_prefatory"),
    (re.compile(r'^NOTE\s*$', re.I), "editorial_prefatory"),
]

_BODY_ANCHOR_RES = [
    re.compile(r'^CHAPTER\s+[IVXLCDM\d]+', re.I),
    re.compile(r'^BOOK\s+[IVXLCDM\d]+', re.I),
    re.compile(r'^PART\s+[IVXLCDM\d]+', re.I),
    re.compile(r'^CANTO\s+[IVXLCDM\d]+', re.I),
    re.compile(r'^HYMN\s+[IVXLCDM\d]+', re.I),
    re.compile(r'^SECTION\s+[IVXLCDM\d]+', re.I),
    re.compile(r'^PSALM\s+\d+', re.I),
    re.compile(r'^[IVXLCDM]+\.\s+[A-Z]'),
    re.compile(r'^\d+\.\s+[A-Z]'),
]


def _find_raw_file(text_id: str, idx: dict) -> str | None:
    """Attempt to find the raw source file for a text via ingest.py configs."""
    # Quick approach: scan ingest.py for the text_id in a config
    ingest_path = ROOT / "05_scripts" / "ingest.py"
    if not ingest_path.exists():
        return None
    try:
        src = ingest_path.read_text(encoding="utf-8")
        # Find raw_file near the text_id
        pattern = re.compile(
            rf'"id":\s*"{re.escape(text_id)}".*?"raw_file":\s*str\(ROOT\s*/\s*"([^"]+)"\)',
            re.S
        )
        m = pattern.search(src)
        if m:
            raw_rel = m.group(1)
            raw_path = ROOT / raw_rel
            if raw_path.exists():
                return str(raw_path)
        # Try reversed order
        pattern2 = re.compile(
            rf'"raw_file":\s*str\(ROOT\s*/\s*"([^"]+)"\).*?"id":\s*"{re.escape(text_id)}"',
            re.S
        )
        m2 = pattern2.search(src)
        if m2:
            raw_rel = m2.group(1)
            raw_path = ROOT / raw_rel
            if raw_path.exists():
                return str(raw_path)
    except Exception:
        pass
    return None


def analyze_front_matter(text_id: str, passages: list[Passage],
                         idx: dict) -> dict | None:
    """Analyze one text for missing front matter. Returns report dict or None."""
    # Check if text already has FM
    for entry in idx["texts"]:
        if entry["id"] == text_id:
            fpath = DATA / entry["data_file"]
            if fpath.exists():
                with open(fpath, encoding="utf-8") as f:
                    d = json.load(f)
                if d.get("front_matter"):
                    return None  # already has FM
            break

    # Try to find raw source
    raw_path = _find_raw_file(text_id, idx)
    if not raw_path:
        return None

    try:
        with open(raw_path, encoding="utf-8") as f:
            raw_text = f.read()
    except Exception:
        return None

    raw_lines = raw_text.splitlines()

    # Find the Gutenberg START marker or beginning of file
    raw_start = 0
    for i, ln in enumerate(raw_lines):
        if 'START OF THE PROJECT GUTENBERG' in ln.upper() or \
           'START OF THIS PROJECT GUTENBERG' in ln.upper():
            raw_start = i + 1
            break

    # Find the first body anchor in the raw text
    body_anchor_line = None
    body_anchor_text = ""
    for i in range(raw_start, min(len(raw_lines), raw_start + 2000)):
        s = raw_lines[i].strip()
        if not s:
            continue
        for pat in _BODY_ANCHOR_RES:
            if pat.match(s):
                body_anchor_line = i
                body_anchor_text = s[:80]
                break
        if body_anchor_line is not None:
            break

    if body_anchor_line is None:
        return None  # can't find body start

    # Scan the pre-body region for FM headers
    fm_types_found: list[str] = []
    fm_header_lines: list[tuple[int, str, str]] = []
    for i in range(raw_start, body_anchor_line):
        s = raw_lines[i].strip()
        for pat, cat in _FM_HEADER_RES:
            if pat.match(s):
                fm_types_found.append(cat)
                fm_header_lines.append((i, cat, s[:60]))
                break

    if not fm_types_found:
        # Check if there's substantial text before body anchor
        pre_body_chars = sum(len(raw_lines[i].strip())
                             for i in range(raw_start, body_anchor_line))
        if pre_body_chars < 200:
            return None  # too little pre-body text
        fm_types_found = ["uncertain"]

    # Get the first parsed passage for alignment
    first_parsed = ""
    if passages:
        first_parsed = passages[0].text[:120]

    # Raw excerpt from FM region
    fm_start_excerpt = "\n".join(
        raw_lines[i].rstrip()
        for i in range(raw_start, min(raw_start + 15, body_anchor_line))
        if raw_lines[i].strip()
    )[:500]

    fm_end_excerpt = "\n".join(
        raw_lines[i].rstrip()
        for i in range(max(raw_start, body_anchor_line - 10), body_anchor_line)
        if raw_lines[i].strip()
    )[:500]

    # Category scores
    cat_scores: dict[str, int] = Counter(fm_types_found)

    # Keep/exclude recommendation
    meaningful_cats = {"preface", "introduction", "prologue", "dedication",
                       "argument_summary"}
    has_meaningful = any(c in meaningful_cats for c in fm_types_found)
    recommendation = "keep" if has_meaningful else "review"

    source = passages[0].source if passages else "unknown"

    return {
        "text_id": text_id,
        "source": source,
        "fm_present_in_raw": True,
        "fm_missing_from_parsed": True,
        "raw_fm_start_line": raw_start,
        "raw_body_anchor_line": body_anchor_line,
        "raw_body_anchor_text": body_anchor_text,
        "estimated_fm_lines": body_anchor_line - raw_start,
        "first_parsed_passage": first_parsed,
        "fm_types_found": sorted(set(fm_types_found)),
        "fm_header_details": [
            {"line": ln, "category": cat, "text": txt}
            for ln, cat, txt in fm_header_lines
        ],
        "category_scores": dict(cat_scores),
        "recommendation": recommendation,
        "raw_fm_start_excerpt": fm_start_excerpt,
        "raw_fm_end_excerpt": fm_end_excerpt,
        "parser_fix_suggestion": (
            f"Capture {len(fm_types_found)} FM sections "
            f"({', '.join(sorted(set(fm_types_found)))}) "
            f"before body anchor at L{body_anchor_line} "
            f"('{body_anchor_text}')"
        ),
    }


def run_fm_audit(passages: list[Passage], idx: dict) -> dict:
    """Run front-matter recovery audit across all texts."""
    by_text = group_by_text(passages)
    reports: list[dict] = []

    for text_id in sorted(by_text.keys()):
        ps = by_text[text_id]
        if ps and ps[0].source in CLEAN_SOURCES:
            continue
        report = analyze_front_matter(text_id, ps, idx)
        if report:
            reports.append(report)

    # Sort by FM line count descending (more FM = higher priority)
    reports.sort(key=lambda r: -r["estimated_fm_lines"])

    # Category summary
    cat_counts: Counter = Counter()
    for r in reports:
        for cat in r["fm_types_found"]:
            cat_counts[cat] += 1

    source_counts: Counter = Counter(r["source"] for r in reports)

    return {
        "audit": "front_matter_recovery",
        "texts_with_missing_fm": len(reports),
        "category_counts": dict(cat_counts.most_common()),
        "source_counts": dict(source_counts.most_common()),
        "priority_queue": [
            {"rank": i + 1, "text_id": r["text_id"],
             "fm_lines": r["estimated_fm_lines"],
             "types": r["fm_types_found"],
             "recommendation": r["recommendation"]}
            for i, r in enumerate(reports[:20])
        ],
        "per_text_reports": reports,
        "review_packets": [
            {
                "text_id": r["text_id"],
                "suspected_fm_types": r["fm_types_found"],
                "why_flagged": f"{r['estimated_fm_lines']} lines of pre-body text, "
                               f"body anchors at L{r['raw_body_anchor_line']} "
                               f"('{r['raw_body_anchor_text']}')",
                "raw_start_excerpt": r["raw_fm_start_excerpt"][:300],
                "raw_end_excerpt": r["raw_fm_end_excerpt"][:300],
                "first_parsed": r["first_parsed_passage"],
                "parser_fix_suggestion": r["parser_fix_suggestion"],
            }
            for r in reports
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT 3: SHORT-STUB CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

STUB_CATEGORIES = [
    "legitimate_dialogue",          # "Yes.", "Indeed.", "Quite true."
    "legitimate_refrain",           # liturgical / poetic refrain
    "roman_numeral_marker",         # "XIV", "III."
    "heading_fragment",             # "CHAPTER", "APPENDIX"
    "separator_divider",            # "* * *", "---", "==="
    "speaker_label",                # "Socrates.", "CRITO:"
    "structural_label",             # "BOOK I", "Part 2"
    "residual_artifact",            # leftover editorial junk
    "ocr_noise",                    # garbled characters
    "uncertain",
]

_ROMAN_RE = re.compile(r'^[IVXLCDM]+\.?\s*$')
_SEPARATOR_RE = re.compile(r'^[\s\*\-=_~·•]+$')
_SPEAKER_RE = re.compile(r'^[A-Z][a-z]+[:\.]$')
_STRUCTURAL_RE = re.compile(
    r'^(?:BOOK|CHAPTER|PART|SECTION|CANTO|HYMN|PSALM|ACT|SCENE)\b', re.I
)
_DIALOGUE_INDICATORS = {
    "yes.", "no.", "yes", "no", "indeed.", "quite true.", "certainly.",
    "i think so.", "of course.", "true.", "exactly.", "very true.",
    "to be sure.", "undoubtedly.", "never.", "nothing.", "none.",
    "impossible.", "allegory.", "allegory",
}


def classify_stub(passage: Passage, context_before: list[str],
                  context_after: list[str]) -> dict:
    """Classify a single short stub passage. Returns classification dict."""
    text = passage.text.strip()
    normalized = text.lower().strip('.')

    scores: dict[str, float] = {cat: 0.0 for cat in STUB_CATEGORIES}

    # ── Rule-based scoring ──────────────────────────────────────────────

    # Roman numeral
    if _ROMAN_RE.match(text):
        scores["roman_numeral_marker"] += 3.0

    # Separator / divider
    if _SEPARATOR_RE.match(text):
        scores["separator_divider"] += 3.0

    # Speaker label (e.g., "Socrates.", "CRITO:")
    if _SPEAKER_RE.match(text) or (text.isupper() and len(text) <= 12 and text.endswith('.')):
        scores["speaker_label"] += 2.0

    # Structural label
    if _STRUCTURAL_RE.match(text):
        scores["structural_label"] += 3.0

    # Known dialogue patterns
    if normalized in _DIALOGUE_INDICATORS:
        scores["legitimate_dialogue"] += 3.0

    # Dialogue context: if surrounding passages are also short, likely dialogue
    short_neighbors = sum(1 for t in context_before + context_after if len(t) <= 30)
    if short_neighbors >= 2:
        scores["legitimate_dialogue"] += 1.5

    # Heading fragment (ALL CAPS, not a known pattern)
    if text.isupper() and len(text) >= 4 and not _ROMAN_RE.match(text):
        if not _STRUCTURAL_RE.match(text):
            scores["heading_fragment"] += 2.0
        else:
            scores["structural_label"] += 1.0

    # OCR noise (unusual characters, very short non-word)
    if len(text) <= 3 and not text.isalpha() and not text.isdigit():
        scores["ocr_noise"] += 2.0

    # Pure number
    if text.isdigit():
        scores["roman_numeral_marker"] += 2.0  # page/section number

    # Residual artifact (contains brackets, footnote markers, etc.)
    if re.match(r'^\[.*\]$', text) or re.match(r'^\d+\]', text):
        scores["residual_artifact"] += 3.0

    # If nothing scored, mark uncertain
    if max(scores.values()) == 0:
        scores["uncertain"] += 1.0

    # Rank
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    top_cat = ranked[0][0]
    confidence = min(1.0, ranked[0][1] / (sum(scores.values()) or 1.0))

    # Keep/drop recommendation
    keep_cats = {"legitimate_dialogue", "legitimate_refrain"}
    drop_cats = {"separator_divider", "roman_numeral_marker", "residual_artifact",
                 "ocr_noise", "structural_label"}
    if top_cat in keep_cats:
        recommendation = "keep"
    elif top_cat in drop_cats and confidence > 0.5:
        recommendation = "drop"
    else:
        recommendation = "review"

    return {
        "text_id": passage.text_id,
        "passage_id": passage.passage_id,
        "l1": passage.l1, "l2": passage.l2, "l3": passage.l3,
        "raw_text": text,
        "normalized": normalized,
        "char_length": len(text),
        "token_count": len(text.split()),
        "context_before": context_before[-2:],
        "context_after": context_after[:2],
        "category_scores": {k: round(v, 1) for k, v in ranked if v > 0},
        "top_category": top_cat,
        "confidence": round(confidence, 2),
        "recommendation": recommendation,
        "reason": f"Matched {top_cat} with score {ranked[0][1]:.1f}",
    }


def run_stub_audit(passages: list[Passage]) -> dict:
    """Run short-stub classification audit across all texts."""
    by_text = group_by_text(passages)
    all_stubs: list[dict] = []
    per_text_summaries: list[dict] = []

    for text_id in sorted(by_text.keys()):
        ps = by_text[text_id]
        if ps and ps[0].source in CLEAN_SOURCES:
            continue

        stubs_in_text: list[dict] = []
        for i, p in enumerate(ps):
            if len(p.text.strip()) > 15:
                continue
            if not p.text.strip():
                continue
            ctx_before = [ps[j].text[:60] for j in range(max(0, i - 3), i)]
            ctx_after = [ps[j].text[:60] for j in range(i + 1, min(len(ps), i + 4))]
            stub = classify_stub(p, ctx_before, ctx_after)
            stubs_in_text.append(stub)

        if not stubs_in_text:
            continue

        all_stubs.extend(stubs_in_text)

        # Per-text summary
        cat_counts = Counter(s["top_category"] for s in stubs_in_text)
        rec_counts = Counter(s["recommendation"] for s in stubs_in_text)
        common_forms = Counter(s["normalized"] for s in stubs_in_text).most_common(10)

        per_text_summaries.append({
            "text_id": text_id,
            "source": ps[0].source if ps else "unknown",
            "total_stubs": len(stubs_in_text),
            "category_counts": dict(cat_counts.most_common()),
            "safe_drop": rec_counts.get("drop", 0),
            "safe_keep": rec_counts.get("keep", 0),
            "uncertain": rec_counts.get("review", 0),
            "most_common_forms": [{"text": t, "count": c} for t, c in common_forms],
        })

    # Sort by total stubs descending
    per_text_summaries.sort(key=lambda s: -s["total_stubs"])

    # Global summary
    global_cat = Counter(s["top_category"] for s in all_stubs)
    global_rec = Counter(s["recommendation"] for s in all_stubs)

    return {
        "audit": "short_stub_classification",
        "total_stubs": len(all_stubs),
        "global_category_counts": dict(global_cat.most_common()),
        "global_recommendations": dict(global_rec.most_common()),
        "texts_with_highest_uncertainty": [
            {"text_id": s["text_id"], "uncertain_count": s["uncertain"],
             "total": s["total_stubs"]}
            for s in sorted(per_text_summaries, key=lambda x: -x["uncertain"])[:10]
        ],
        "texts_with_highest_artifact_burden": [
            {"text_id": s["text_id"], "drop_count": s["safe_drop"],
             "total": s["total_stubs"]}
            for s in sorted(per_text_summaries, key=lambda x: -x["safe_drop"])[:10]
        ],
        "texts_with_mostly_legitimate": [
            {"text_id": s["text_id"], "keep_count": s["safe_keep"],
             "total": s["total_stubs"]}
            for s in sorted(per_text_summaries, key=lambda x: -x["safe_keep"])[:10]
        ],
        "per_text_summaries": per_text_summaries,
        "review_packets": [
            {
                "text_id": s["text_id"],
                "top_stub_patterns": s["most_common_forms"][:5],
                "category_distribution": s["category_counts"],
                "suggested_rules": _suggest_rules(s),
                "caution_warning": (
                    "This text has many legitimate short passages — "
                    "a global deletion rule would be risky"
                    if s["safe_keep"] > s["safe_drop"] else ""
                ),
            }
            for s in per_text_summaries
            if s["uncertain"] > 5 or s["safe_drop"] > 10
        ],
    }


def _suggest_rules(summary: dict) -> list[str]:
    """Generate suggested cleanup rules for a text based on its stub distribution."""
    rules = []
    cats = summary["category_counts"]
    if cats.get("separator_divider", 0) > 3:
        rules.append("Strip separator/divider lines (*, ---, ===)")
    if cats.get("roman_numeral_marker", 0) > 3:
        rules.append("Strip bare Roman numeral markers (likely page/section labels)")
    if cats.get("structural_label", 0) > 3:
        rules.append("Reclassify structural labels as hierarchy markers, not passages")
    if cats.get("heading_fragment", 0) > 3:
        rules.append("Reclassify ALL-CAPS heading fragments as section boundaries")
    if cats.get("residual_artifact", 0) > 3:
        rules.append("Strip remaining bracketed artifacts")
    return rules


# ═══════════════════════════════════════════════════════════════════════════════
# MARKDOWN SUMMARY GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

def generate_markdown(dup_report: dict | None, fm_report: dict | None,
                      stub_report: dict | None) -> str:
    """Generate a human-readable markdown summary of all audit results."""
    lines = ["# Corpus Audit Report\n"]

    if dup_report:
        lines.append("## 1. Duplicate-ID Structural Triage\n")
        lines.append(f"**Texts affected:** {dup_report['texts_affected']}")
        lines.append(f"**Total excess duplicates:** {dup_report['total_excess_duplicates']:,}\n")
        lines.append("### Category Distribution\n")
        lines.append("| Category | Texts |")
        lines.append("|---|---:|")
        for cs in dup_report["category_summary"]:
            lines.append(f"| {cs['category']} | {cs['count']} |")
        lines.append("")
        lines.append("### Priority Queue (top 10)\n")
        lines.append("| Rank | Text | Dups | Category | Action |")
        lines.append("|---:|---|---:|---|---|")
        for pq in dup_report["priority_queue"][:10]:
            lines.append(f"| {pq['rank']} | {pq['text_id']} | {pq['dups']:,} | "
                         f"{pq['category']} | {pq['action'][:50]}... |")
        lines.append("")

    if fm_report:
        lines.append("## 2. Front-Matter Recovery\n")
        lines.append(f"**Texts with missing FM:** {fm_report['texts_with_missing_fm']}\n")
        lines.append("### FM Types Found\n")
        lines.append("| Type | Count |")
        lines.append("|---|---:|")
        for cat, cnt in fm_report["category_counts"].items():
            lines.append(f"| {cat} | {cnt} |")
        lines.append("")

    if stub_report:
        lines.append("## 3. Short-Stub Classification\n")
        lines.append(f"**Total stubs:** {stub_report['total_stubs']:,}\n")
        lines.append("### Global Recommendations\n")
        lines.append("| Action | Count |")
        lines.append("|---|---:|")
        for act, cnt in stub_report["global_recommendations"].items():
            lines.append(f"| {act} | {cnt:,} |")
        lines.append("")
        lines.append("### Category Distribution\n")
        lines.append("| Category | Count |")
        lines.append("|---|---:|")
        for cat, cnt in stub_report["global_category_counts"].items():
            lines.append(f"| {cat} | {cnt:,} |")
        lines.append("")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(
        description="Corpus diagnostic audit — diagnosis only, no modifications.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--audit", choices=["dup", "fm", "stub", "all"],
                    default="all", help="which audit to run")
    ap.add_argument("--json", action="store_true",
                    help="output JSON instead of markdown")
    ap.add_argument("--out", type=str, default="",
                    help="save output to file instead of stdout")
    args = ap.parse_args()

    print("Loading corpus...", file=sys.stderr)
    passages, idx = load_corpus()
    print(f"Loaded {len(passages):,} passages from "
          f"{len(set(p.text_id for p in passages))} texts", file=sys.stderr)

    results = {}
    dup_report = fm_report = stub_report = None

    if args.audit in ("dup", "all"):
        print("Running duplicate-ID audit...", file=sys.stderr)
        dup_report = run_dup_id_audit(passages)
        results["duplicate_id_triage"] = dup_report
        print(f"  → {dup_report['texts_affected']} texts, "
              f"{dup_report['total_excess_duplicates']:,} excess dups",
              file=sys.stderr)

    if args.audit in ("fm", "all"):
        print("Running front-matter audit...", file=sys.stderr)
        fm_report = run_fm_audit(passages, idx)
        results["front_matter_recovery"] = fm_report
        print(f"  → {fm_report['texts_with_missing_fm']} texts missing FM",
              file=sys.stderr)

    if args.audit in ("stub", "all"):
        print("Running short-stub audit...", file=sys.stderr)
        stub_report = run_stub_audit(passages)
        results["short_stub_classification"] = stub_report
        print(f"  → {stub_report['total_stubs']:,} stubs classified",
              file=sys.stderr)

    if args.json:
        output = json.dumps(results, indent=2, ensure_ascii=False, default=str)
    else:
        output = generate_markdown(dup_report, fm_report, stub_report)

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Saved to {args.out}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
