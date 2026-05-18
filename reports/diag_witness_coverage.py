"""Audit folio witness coverage for the KJV Bible."""
import json
from collections import defaultdict

with open("data/bible_kjv.json", encoding="utf-8") as f:
    data = json.load(f)

by_chapter = defaultdict(list)
for rec in data.get("genealogy", []):
    for a in rec.get("anchors", []):
        pid = (a.get("target") or "").split("::").pop()  # e.g. "gen.4.25"
        parts = pid.split(".")
        if len(parts) < 2:
            continue
        ch = f"{parts[0]}.{parts[1]}"
        by_chapter[ch].append(
            {"kind": rec.get("kind"), "title": rec.get("title"), "anchor": pid, "id": rec.get("id")}
        )

print(f"Total witness records: {len(data.get('genealogy', []))}")
print(f"Chapters with witnesses: {len(by_chapter)}\n")
for ch in sorted(by_chapter.keys()):
    print(f"  {ch}:")
    for w in by_chapter[ch]:
        marker = "[PLATE]" if w["kind"] == "plate" else "[gene] "
        print(f"    {marker} @{w['anchor']:<12}  {w['title']}")
