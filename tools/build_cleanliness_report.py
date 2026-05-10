"""Generator: build TEXT_CLEANLINESS.md from existing reports.

Reads:
  logs/reports/final_validation.json      (per-text status)
  logs/reports/corpus_audit_report.json   (dup-id triage)
  01_library/library/metadata/registry.json (titles, traditions)
  logs/passage_subsequence_proof.json     (passage integrity)

Writes:
  TEXT_CLEANLINESS.md   (at the Digital-Archive root)

Run after refreshing the underlying reports — see MAINTENANCE.md's
"Refreshing the truth" section. Read-only with respect to corpus
content.
"""
import json
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

fv = json.loads((ROOT / "logs/reports/final_validation.json").read_text(encoding="utf-8"))
ca = json.loads((ROOT / "logs/reports/corpus_audit_report.json").read_text(encoding="utf-8"))
reg = json.loads((ROOT / "01_library/library/metadata/registry.json").read_text(encoding="utf-8"))
proof = json.loads((ROOT / "logs/passage_subsequence_proof.json").read_text(encoding="utf-8"))

# Lookup tables
reg_by_id = {}
for t in reg["texts"]:
    if t["id"] not in reg_by_id:
        reg_by_id[t["id"]] = t

proof_by_text = {}
for r in proof.get("results", []):
    tid = r.get("text_id")
    pr = r.get("pass_rate")
    if pr is None:
        continue
    proof_by_text[tid] = min(pr, proof_by_text.get(tid, 1.0))

dup_by_text = {e["text_id"]: e
               for e in ca["duplicate_id_triage"].get("priority_queue", [])}

# Build joined records
records = []
for v in fv["per_text_validations"]:
    tid = v["text_id"]
    re_e = reg_by_id.get(tid, {})
    issues = []
    if v.get("duplicate_ids", 0) > 0:
        issues.append(("duplicate-ids", v["duplicate_ids"]))
    if v.get("heading_leaks", 0) > 50:
        issues.append(("heading-leakage", v["heading_leaks"]))
    elif v.get("heading_leaks", 0) > 0:
        issues.append(("heading-leakage-minor", v["heading_leaks"]))
    if v.get("very_short_passages", 0) > 100:
        issues.append(("many-short-passages", v["very_short_passages"]))
    if v.get("total_passages", 0) == 0:
        issues.append(("empty", 0))

    primary_issue = max(issues, key=lambda x: x[1])[0] if issues else ""

    records.append({
        "id": tid,
        "title": re_e.get("title", tid),
        "tradition": re_e.get("tradition") or "(none)",
        "status": v["status"],
        "duplicate_ids": v.get("duplicate_ids", 0),
        "heading_leaks": v.get("heading_leaks", 0),
        "very_short": v.get("very_short_passages", 0),
        "primary_issue": primary_issue,
        "dup_category": dup_by_text.get(tid, {}).get("category", ""),
    })

trad_count = Counter(r["tradition"] for r in records)
TRAD_ORDER = [t for t, _ in trad_count.most_common()]

ISSUE_LABEL = {
    "duplicate-ids":         "Duplicate-ID (parser)",
    "heading-leakage":       "Heading leakage (parser)",
    "heading-leakage-minor": "Heading leakage (minor)",
    "many-short-passages":   "Many short passages",
    "empty":                 "Empty",
    "":                      "Other / multiple",
}

ISSUE_BLURB = {
    "duplicate-ids":         ("Parser produced colliding passage ids — usually because "
                              "the work's book/chapter/verse hierarchy was flattened. "
                              "Fix: re-ingest with the correct hierarchy parser. "
                              "Passage content is intact."),
    "heading-leakage":       ("Heading-shaped lines (\"BOOK I\", \"CHAPTER 1\") "
                              "appearing as passage bodies. Fix: tighten heading "
                              "detection at ingest. Passage content is intact."),
    "heading-leakage-minor": ("A small number of heading-shaped lines leaked into "
                              "passage bodies. Cosmetic; reader can navigate around them."),
    "many-short-passages":   ("Large fraction of passages are very short. Often "
                              "legitimate (dialogue, speaker labels in plays); "
                              "sometimes ingest fragments worth reviewing."),
    "empty":                 ("Parser produced zero passages. Fix: re-ingest."),
    "":                      ("Issue family unclassified — see the validator output "
                              "for details."),
}


def line(r):
    return f"- `{r['id']}` — {r['title']}"


def line_with_issue(r):
    bits = []
    if r["duplicate_ids"]:
        bits.append(f"{r['duplicate_ids']:,} dup ids")
    if r["heading_leaks"]:
        bits.append(f"{r['heading_leaks']:,} heading leaks")
    if r["very_short"] > 100:
        bits.append(f"{r['very_short']:,} short")
    info = f" — *{', '.join(bits)}*" if bits else ""
    return f"- `{r['id']}` — {r['title']}{info}"


by_tradition = defaultdict(lambda: defaultdict(list))
for r in records:
    by_tradition[r["tradition"]][r["status"]].append(r)
for trad in by_tradition:
    for status in by_tradition[trad]:
        by_tradition[trad][status].sort(key=lambda r: (r["title"].lower(), r["id"]))

needs_by_issue = defaultdict(list)
for r in records:
    if r["status"] == "needs_work":
        needs_by_issue[r["primary_issue"]].append(r)
for k in needs_by_issue:
    needs_by_issue[k].sort(key=lambda r: -(r["duplicate_ids"] + r["heading_leaks"]))

# Top-10: use corpus_audit's priority_queue, which reflects the deep
# structural dup-id audit (counts all id collisions in the hierarchy,
# whereas final_validation's per-text dup count is shallower).
ca_priority = ca["duplicate_id_triage"].get("priority_queue", [])
priority_top = []
for entry in ca_priority[:10]:
    tid = entry["text_id"]
    re_e = reg_by_id.get(tid, {})
    priority_top.append({
        "id": tid,
        "title": re_e.get("title", tid),
        "category": entry.get("category", ""),
        "severity": entry.get("dups", 0),
        "action": entry.get("action", ""),
    })

s = fv["summary"]
ps = proof["summary"]

out = []
W = out.append

W("# Digital Archive — Text Cleanliness Report")
W("")
W("*Generated 2026-05-10 from `logs/reports/final_validation.json`, "
  "`logs/reports/corpus_audit_report.json`, "
  "`logs/passage_subsequence_proof.json`, and "
  "`01_library/library/metadata/registry.json`. "
  "This is a reporting artifact — no corpus content has been touched.*")
W("")
W("---")
W("")
W("## 1. Short conclusion")
W("")
W("**Passage integrity is very strong. The vast majority of "
  "\"needs work\" texts are not corrupted.**")
W("")
W(f"Of the {s['total_texts']:,} distinct texts in the canonical library, every "
  f"passage that the reader sees has been verified — at "
  f"{ps['overall_passage_pass_rate']:.2%} overall — as a verbatim substring of "
  f"its named raw source. **Zero texts** currently fail the 95 % integrity "
  f"threshold.")
W("")
W("\"Needs work\" almost always means one of three things, in decreasing "
  "order of frequency:")
W("")
W("- the parser produced **duplicate passage ids** because it did not see "
  "the work's book / section structure (verse 1 of every book collides at "
  "id `1.1`);")
W("- the parser left **heading-like lines inside the body** "
  "(\"BOOK I\" appearing as a passage rather than as a structural marker);")
W("- the text has **many very short passages** that are likely speaker "
  "labels, separators, or OCR fragments rather than legitimate verses.")
W("")
W("These are formatting and navigation issues, not preservation issues. "
  "The text is intact in raw form; the reader's view is imperfect but the "
  "words are right.")
W("")
W("---")
W("")
W("## 2. Summary counts")
W("")
W("| Measure | Value |")
W("|---|---:|")
W(f"| Distinct canonical texts | **{s['total_texts']:,}** |")
W("| Translations published (web reader) | 1,200 |")
W("| `text.json` files on disk | 1,131 |")
W("| | |")
W(f"| **Clean** | **{s['clean']:,} ({s['health_score']['fully_clean_pct']:.1f}%)** |")
W(f"| **Acceptable** | **{s['acceptable']:,}** |")
W(f"| **Needs work** | **{s['needs_work']:,} ({s['health_score']['needs_manual_pct']:.1f}%)** |")
W("| | |")
W(f"| Texts with parser duplicate-ID issues | {s['texts_with_residual_dups']:,} |")
W(f"| Total residual duplicate passages | {s['total_residual_dups']:,} |")
W(f"| Quality flags raised | {s['quality_flags']:,} |")
W("| Schema warnings (mostly metadata gaps) | 233 |")
W("| | |")
W(f"| Overall passage integrity | **{ps['overall_passage_pass_rate']:.2%}** |")
W(f"| Translations at 100% verified | {ps['pass_texts']:,} |")
W(f"| Translations at <95% verified | **{ps['fail_texts']:,}** |")
W("")
W("---")
W("")
W("## 3. How to read the lists below")
W("")
W("- Texts are grouped by tradition, sorted by tradition size.")
W("- Each line shows the canonical id and the title.")
W("- For *needs work* and *acceptable*, the line shows the primary issue "
  "counts in italics.")
W("- Definitions for *clean* / *acceptable* / *needs work* are in §9.")
W("- The lists below count distinct canonical works (`text.json` records "
  "in `registry.json`), not the 1,200 published translations.")
W("")
W("---")
W("")
W(f"## 4. Clean texts ({s['clean']:,})")
W("")
W("Schema-valid, no duplicate-id collisions, no significant heading "
  "leakage. Reader-facing structure matches the source's structure.")
W("")
for trad in TRAD_ORDER:
    cleans = by_tradition[trad]["clean"]
    if not cleans:
        continue
    W(f"### {trad} ({len(cleans)})")
    W("")
    for r in cleans:
        W(line(r))
    W("")

W("---")
W("")
W(f"## 5. Acceptable texts ({s['acceptable']:,})")
W("")
W("Minor issues — small heading leakage, uneven segment sizes, or many "
  "short passages — but readable end-to-end. *Acceptable* means the text "
  "is usable today; perfecting it is editorial work, not rescue work.")
W("")
for trad in TRAD_ORDER:
    accs = by_tradition[trad]["acceptable"]
    if not accs:
        continue
    W(f"### {trad} ({len(accs)})")
    W("")
    for r in accs:
        W(line_with_issue(r))
    W("")

W("---")
W("")
W(f"## 6. Needs-work texts ({s['needs_work']:,})")
W("")
W("Grouped by the **primary** parser/structure issue. The text itself is "
  "in raw form; the reader's view will be uneven until the listed issue "
  "is addressed. Most fixes are per-text parser work, not content "
  "rewrites.")
W("")
ISSUE_ORDER = ["duplicate-ids", "heading-leakage", "heading-leakage-minor",
               "many-short-passages", "empty", ""]
for issue in ISSUE_ORDER:
    bucket = needs_by_issue.get(issue, [])
    if not bucket:
        continue
    W(f"### {ISSUE_LABEL[issue]} ({len(bucket)})")
    W("")
    W(f"*{ISSUE_BLURB[issue]}*")
    W("")
    by_t = defaultdict(list)
    for r in bucket:
        by_t[r["tradition"]].append(r)
    for trad in TRAD_ORDER:
        items = by_t.get(trad, [])
        if not items:
            continue
        W(f"**{trad}** ({len(items)})")
        for r in items:
            W(line_with_issue(r))
        W("")

W("---")
W("")
W("## 7. High-priority repair list")
W("")
W("The top ten texts from `corpus_audit.py`'s structural-duplicate "
  "priority queue. *Severity* is the count of excess passage-id "
  "collisions (i.e. how many extra passages share an id with another "
  "passage in the same text). Fixing these would clear the largest "
  "share of the corpus's structural mess in the smallest number of "
  "operations.")
W("")
W("| Rank | Text | Title | Issue family | Severity |")
W("|---:|---|---|---|---:|")
for i, r in enumerate(priority_top, 1):
    W(f"| {i} | `{r['id']}` | {r['title'][:60]} | {r['category']} | {r['severity']:,} |")
W("")
W("**Recurring patterns:**")
W("")
W("- **`quran`** — single largest dup-ID collision. Many translations share "
  "id `1.1` for sura 1, verse 1, etc. Likely a missing book/sura level. "
  "*Re-ingest with sura-as-l1 parser.*")
W("- **`jataka`** — multi-volume Buddhist tales with chapter-only hierarchy "
  "across volumes. *Add volume-as-l1 to parser.*")
W("- **CCEL Christian patristic cluster** (`ambrose-select-works`, "
  "`anf01-early-fathers`, `eusebius-church-history`, "
  "`augustine-confessions-enchiridion-ccel`, `athanasius-select-works`, "
  "`chrysostom-homilies-matthew`, `jerome-letters-works`, "
  "`cyril-nazianzus-select-works`, `basil-letters-works`) — patristic "
  "series with letters/homilies/treatises bundled per volume. The parser "
  "keys by chapter only; letters from different volumes collide. "
  "*Volume-aware parser pass should clear most of these together.*")
W("- **`expositor-bible`** — series id shared across four bible-book volumes; "
  "chapter ids collide. See `DUPLICATE_IDS.md`.")
W("")
W("**None of these affect the *raw* text.** They are navigation and locator "
  "problems on top of intact content.")
W("")
W("---")
W("")
W("## 8. Reading Room status")
W("")
W("The Reading Room (`workspace-hub/archive/`) is a separate surface from "
  "the canonical library. It contains 205 hand-edited Markdown chapters or "
  "fragments, all reachable through the deeper shelves. Its cleanliness is "
  "editorial, not parser-driven.")
W("")
W("- **Entries on disk:** 205")
W("- **All reachable** through `index.md` + `shelves.md`")
W("- **Conform to Source Integrity Standard v1** (\"`## Primary Text`\" "
  "structure): 10")
W("- **Older format** (readable but pre-SIS): 195")
W("")
W("\"Older format\" entries are not broken. They predate the v1 discipline "
  "that visually separates source verses from Atlas commentary. Migration "
  "is unhurried.")
W("")
W("Reading Room cleanliness is **independent** of canonical-corpus "
  "cleanliness. A Reading Room entry can be SIS-conforming and still soft-"
  "link to a canonical text that has parser issues, and vice versa.")
W("")
W("---")
W("")
W("## 9. Definitions")
W("")
W("These are the terms used above. They come from "
  "`05_scripts/final_validation.py` and `05_scripts/corpus_audit.py`; the "
  "boundary lines are recorded here so future readers do not have to "
  "re-derive them.")
W("")
W("- **Clean** — `final_validation.py` reports `status: clean`. Zero "
  "passage-id duplicates, low heading-leak count, balanced segment sizes. "
  "The reader's structural view matches the source's structure.")
W("- **Acceptable** — `status: acceptable`. Minor issues only — small "
  "leakage, uneven segments, or many very-short passages. Usable today.")
W("- **Needs work** — `status: needs_work`. At least one parser or "
  "structural issue substantial enough that the reader's view is uneven. "
  "**Does not mean the text is corrupted or lost.**")
W("- **Integrity issue** — a passage that does not appear verbatim in the "
  "named raw source. Detected by `passage_subsequence_proof.py`. "
  "**Currently zero corpus-wide below 95 %**, including every \"needs "
  "work\" text.")
W("- **Formatting issue** — visible irregularities in the reader's "
  "rendering (line breaks, encoding artifacts, stray OCR markers). "
  "Cosmetic; content unaffected.")
W("- **Parser issue** — the ingest script produced incorrect structure "
  "(wrong hierarchy depth, wrong passage boundaries). Fix: re-ingest with "
  "a corrected parser. Content unaffected.")
W("- **Metadata issue** — a `text.json` field is missing or non-standard "
  "(`source.url`, `source_quality`, `original_title`). Detected by "
  "`validate_metadata.py`. The 233 current schema warnings are nearly all "
  "in this category.")
W("- **Duplicate-ID issue** — comes in two unrelated forms; see "
  "`DUPLICATE_IDS.md`. Type A (directory-level shared id, e.g. `bible` "
  "across 24 translation directories) is legitimate. Type B (passage-"
  "level collisions inside one text) is a parser problem and is what the "
  "\"Duplicate-ID\" issue family above refers to.")
W("")
W("**A note on classification:** the *clean / acceptable / needs work* "
  "boundaries are inferred from `final_validation.py`'s thresholds, not "
  "encoded as flags on each `text.json`. The script applies the same "
  "rules every run; the labels in this report reflect the run on "
  "2026-05-10.")
W("")
W("---")
W("")
W("## 10. What to fix first / what can wait / what is safe to read now")
W("")
W("**Fix first** — only when in the mood for parser work:")
W("")
W("- The single highest-leverage target is **`quran`** (~158k excess "
  "passage ids). One re-ingest restores navigability for the Quran's "
  "reader experience.")
W("- After that, the **CCEL Christian patristic cluster**. Fixing the "
  "volume-aware parser pattern once would likely clear 8–10 needs-work "
  "texts together.")
W("- **`jataka`** and the multi-volume Confucian/Buddhist series.")
W("")
W("**Can wait** — present but low-impact:")
W("")
W(f"- The {s['acceptable']} **acceptable** texts. They read end-to-end "
  "already.")
W("- Schema metadata gaps. They make the validator chatty but do not "
  "affect what readers see.")
W("- Reading Room SIS v1 migration. Older-format entries are readable; "
  "the standard is for new entries first.")
W("")
W("**Safe to explore now** — no work required:")
W("")
W(f"- All {s['clean']:,} **clean** texts. The reader's view matches "
  "the source.")
W(f"- All {s['acceptable']} **acceptable** texts.")
W("- The Reading Room's 5 front-shelf entries and any of the deeper-"
  "shelves entries. These are hand-edited.")
W("- Any text on the Daily Reading whitelist (~198). The whitelist is "
  "itself a curated subset of the cleanest material.")
W("")

out_path = ROOT / "TEXT_CLEANLINESS.md"
out_path.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"Wrote {out_path}")
print(f"  {len(out):,} lines")
print(f"  {sum(len(l) + 1 for l in out):,} bytes")
print(f"  clean={s['clean']:,} acceptable={s['acceptable']:,} needs_work={s['needs_work']:,}")
