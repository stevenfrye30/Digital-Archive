# v102 — Upanishads Veda views + further extraction

The Upanishads family page now supports three viewing modes
(By Veda · By text · Traditional order), and the audit recovered
three additional Upanishads (Aitareya, Narada-Parivrajaka, Sandilya)
that v101 had marked uncertain or absent. No source files merged,
rewritten, or deleted.

## 1. Summary

| Metric | Before (v101) | After (v102) |
|---|---:|---:|
| Total active Upanishads | 31 | **34** |
| Principal active | 10 | **11** (+ Aitareya) |
| Minor active | 21 | **23** (+ Narada-Parivrajaka, Sandilya) |
| Safe (clean L1 = whole Upanishad) | 20 | 20 |
| Safe-start (start L1 + content forward) | 11 | **13** |
| Pid-route (sub-L1 entry point) | 0 | **1** (Aitareya) |
| Uncertain / inactive | 3 | 2 |

Mandukya: not found in any archive source (v102 deep search across
all six files; only editorial-list mentions, never a translation).
Confirmed honestly inactive.

Aitareya: recovered. Müller Part 1 has the section header at
`id='11.51'` ("AITAREYA-ARANYAKA."). v102 routes the witness via
`pendingPid='11.51'` — a pid-level route that lands at the
Aitareya-Aranyaka section header inside the merged Part 1 L1.

Upadeśā I-IX: classified as ONE Upanishad — the **Narada-Parivrajaka
Upanishad** of the Atharvaveda (Aiyar labelled its nine teachings
"Upadeśā I-IX" rather than the Upanishad name). Now active.

Aiyar L1=51-53: classified as the **Sandilya Upanishad** of the
Atharvaveda (Sandilya / Atharvan dialogue on the eight angas of
yoga; Aiyar labelled its three chapters as plain "Chapter I-III").
Now active.

## 2. Veda metadata table

Veda source: `source heading` = read directly from Aiyar's
chapter_titles ("of X-Yajurveda"). `curated traditional metadata` =
Muktikā assignment (no source field in the file).

### Principal Upanishads

| order | Upanishad | Veda | source | route |
|---:|---|---|---|---|
| 10  | Isha           | Shukla Yajurveda  | curated traditional | safe (Müller complete) |
| 20  | Kena           | Samaveda          | curated traditional | safe (Müller complete) |
| 30  | Katha          | Krishna Yajurveda | curated traditional | safe (Müller complete) |
| 40  | Prasna         | Atharvaveda       | curated traditional | safe (Müller complete) |
| 50  | Mundaka        | Atharvaveda       | curated traditional | safe (Müller complete) |
| 70  | Taittiriya     | Krishna Yajurveda | curated traditional | safe (Müller complete) |
| 80  | **Aitareya** (v102) | Rigveda      | curated traditional | safe-start, pid='11.51' (Müller Part 1) |
| 90  | Chandogya      | Samaveda          | curated traditional | safe (Müller complete) |
| 100 | Brihadaranyaka | Shukla Yajurveda  | curated traditional | safe (Müller complete) |
| 110 | Svetasvatara   | Krishna Yajurveda | curated traditional | safe (Müller complete) |
| 120 | Kaushitaki     | Rigveda           | curated traditional | safe (Müller complete) |

### Minor Upanishads

| order | Upanishad | Veda | source | route (Aiyar L1) |
|---:|---|---|---|---|
| 210 | Maitreya       | Samaveda          | source heading | safe-start (6) |
| 220 | Sarvasara      | Krishna Yajurveda | source heading | safe (4) |
| 230 | Niralamba      | Shukla Yajurveda  | source heading | safe (5) |
| 240 | Kaivalya       | Krishna Yajurveda | source heading | safe-start (9) |
| 250 | Amrtabindu     | Krishna Yajurveda | source heading | safe-start (10) |
| 260 | Atmabodha      | Rigveda           | source heading | safe-start (11) |
| 270 | Skanda         | Krishna Yajurveda | source heading | safe-start (12) |
| 280 | Adhyatma       | Shukla Yajurveda  | source heading | safe (17) |
| 290 | Brahmopanishad | Krishna Yajurveda | source heading | safe-start (34) |
| 300 | Vajrasuchi     | Samaveda          | source heading | safe (35) |
| 310 | S'Ariraka      | Krishna Yajurveda | source heading | safe-start (36) |
| 320 | Garbha         | Krishna Yajurveda | source heading | safe (37) |
| 330 | Tarasara       | Shukla Yajurveda  | source heading | safe (38) |
| 340 | Narayana       | Krishna Yajurveda | source heading | safe-start (39) |
| 350 | Kalisantarana  | Krishna Yajurveda | source heading | safe-start (40) |
| 360 | Bhikshuka      | Shukla Yajurveda  | source heading | safe-start (41) |
| 370 | Yogatattva     | Krishna Yajurveda | source heading | safe (55) |
| 380 | Dhyanabindu    | Samaveda          | source heading | safe (56) |
| 390 | Hamsa          | Shukla Yajurveda  | source heading | safe (57) |
| 400 | Amrtanada      | Krishna Yajurveda | source heading | safe-start (58) |
| 405 | **Narada-Parivrajaka** (v102) | Atharvaveda | curated traditional | safe-start (42, spans L1=42-50) |
| 410 | Nadabindu      | Rigveda           | source heading | safe (68) |
| 415 | **Sandilya** (v102) | Atharvaveda  | source heading | safe-start (51, spans L1=51-53) |

## 3. Source extraction table

| File | Named Upanishads found | Routes created (v102) | Routes not yet created — why |
|---|---|---|---|
| `upanishads` (Müller complete) | 10 principal as L1 slugs | 10 (all safe) | — |
| `upanishads-muller-part1` | Aitareya-Aranyaka section header at id=11.51 | 1 (safe-start via pid) | Khandogya, Kena, Kaushitaki, Vagasaneyi-Samhita also present at same L1=7 — already in Müller complete with clean L1 slugs |
| `upanishads-muller-part2` | 6 principal Upanishads listed in joint title | 0 (already in Müller complete) | All six Vol. XV Upanishads collapsed under single L1=1 |
| `upanishads-30-minor-aiyar` | 21 named Upanishads | 21 (10 safe + 11 safe-start) | L1=18-33 Khanda/Chapter sub-sections — unidentified Upanishads |
| `upanishads-johnson` | Essay-themed | 0 | Thematic structure, not per-Upanishad |
| `the-upanishads-max-muller-1879` | Derivative of Part 1 + Part 2 | 0 (legacy duplicate) | Same content available via Müller complete and Parts |

## 4. Inactive / uncertain table

| Entry | Reason | Repair needed |
|---|---|---|
| Mandukya | Searched all six files in v102 — only editor-list mentions, never a translation passage. | Acquire a Mandukya source edition and ingest. |
| Aiyar L1=18-33 (Khanda I-XVI, Chapter I-VI) | Sub-section headings without identifiable Upanishad title in chapter_titles. Likely belong to one or more named minor Upanishads (possibly Tejobindu / Yogashikha / Sannyasa). | Parser repair to recover Upanishad-boundary metadata from the source TXT. |

(v101's "Aitareya" and "Upadeśā I-IX" inactive entries are now
ACTIVE.)

## 5. View-mode explanation

Three viewing modes are selectable via a segmented control near the
top of the family page. The selection is module-scoped so it
persists across re-renders. One layer only — no nested tabs.

**View 1: By Veda** (default)

Cards grouped under their associated Veda. Group order: Rigveda →
Samaveda → Shukla Yajurveda → Krishna Yajurveda → Atharvaveda →
Uncertain. Within each group, principal Upanishads first, then
minor. A small intro note clarifies the difference between
*source heading* and *curated traditional metadata* so readers
know which Veda assignments came from the source files vs from
Muktikā tradition.

**View 2: By text**

Preserves the v98/v100 bibliographic view: Primary collections,
Specialised collections, Volumes and parts, Legacy / duplicate
records. Lets readers who care about edition / translator /
source volume browse by witness instead of by Upanishad.

**View 3: Traditional order**

Labelled *Traditional order*, not *Historical order*. v102 declines
to invent chronological certainty — most principal Upanishad dates
fall in 800–200 BCE but exact ordering is scholarly contested.
The traditional order uses the Muktikā-style principal sequence
followed by Aiyar's source order for minor Upanishads.

## 6. Witness picker (v102 refinement)

Above each Upanishad's witness list, a small metadata band shows:

```
PRINCIPAL UPANISHAD · ASSOCIATED VEDA: RIGVEDA (CURATED TRADITIONAL
METADATA) · 1 ACTIVE WITNESS
```

This reinforces source transparency before the reader routes into
the reading room.

Witness cards continue to show: role label (italic small-caps) +
source title + translator + year + optional note. The note for
safe-start routes explains continuation ("enters at the Upanishad's
starting passage; content continues across following sections").

The Aitareya witness route additionally notes that it opens at the
AITAREYA-ARANYAKA section header and the Aitareya Upanishad sits
within the second Aranyaka.

## What was NOT touched

- No JSON files merged, rewritten, or deleted.
- No source-text passages, fm flags, or chapter_titles modified.
- The v100 TEXT_CONTENTS_OVERRIDES (Müller Parts source-volume
  notes, legacy reprint title override, Aiyar minor list) remain.
- Bible / Tao / Gita / Iliad / Odyssey / etc. flows untouched.
- Page-type doctrine (shelf scrolls, contents leaf static, reading
  room scrolls) preserved.
