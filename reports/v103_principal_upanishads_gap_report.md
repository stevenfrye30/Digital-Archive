# v103 — Principal Upanishads gap report

Phase 1 audit of the principal Upanishads target list, with one
new safe witness recovered (Maitri via Müller Part 2) and an
acquisition plan for the remaining gap (Mandukya).

## 1. Principal Upanishads target list & status

Target = the conservative 10 + commonly-added principal Upanishads.

| # | Upanishad | Status | Veda (curated) | Source witness | Route quality | textId | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Isha           | **active** | Shukla Yajurveda  | Müller, complete (1879) | safe                          | `upanishads`              | L1 slug = `isha` |
| 2 | Kena           | **active** | Samaveda          | Müller, complete (1879) | safe                          | `upanishads`              | L1 slug = `kena` |
| 3 | Katha          | **active** | Krishna Yajurveda | Müller, complete (1884) | safe                          | `upanishads`              | L1 slug = `katha` |
| 4 | Prasna         | **active** | Atharvaveda       | Müller, complete (1884) | safe                          | `upanishads`              | L1 slug = `prasna` |
| 5 | Mundaka        | **active** | Atharvaveda       | Müller, complete (1884) | safe                          | `upanishads`              | L1 slug = `mundaka` |
| 6 | **Mandukya**   | **missing** | Atharvaveda     | — none —                | n/a                           | —                         | Acquisition needed |
| 7 | Taittiriya     | **active** | Krishna Yajurveda | Müller, complete (1884) | safe                          | `upanishads`              | L1 slug = `taittiriya` |
| 8 | Aitareya       | **active** (v102) | Rigveda     | Müller Part 1 (1879)    | safe-start (pid='11.51')      | `upanishads-muller-part1` | Opens at AITAREYA-ARANYAKA header; Upanishad proper sits within second Aranyaka |
| 9 | Chandogya      | **active** | Samaveda          | Müller, complete (1879) | safe                          | `upanishads`              | L1 slug = `chandogya` |
|10 | Brihadaranyaka | **active** | Shukla Yajurveda  | Müller, complete (1884) | safe                          | `upanishads`              | L1 slug = `brihadaranyaka` |
|11 | Svetasvatara   | **active** | Krishna Yajurveda | Müller, complete (1884) | safe                          | `upanishads`              | L1 slug = `svetasvatara` |
|12 | Kaushitaki     | **active** | Rigveda           | Müller, complete (1879) | safe                          | `upanishads`              | L1 slug = `kaushitaki` |
|13 | **Maitri** (Maitrayaniya / Maitrayani) | **active** (v103 ✦) | Krishna Yajurveda | Müller Part 2 (1884)    | safe-start (pid='6.348')      | `upanishads-muller-part2` | Opens at MAITRAYANA-BRAHMANA-UPANISHAD section header; Upanishad continues across 7 Prapathakas |

**Result:** 12 of 13 principal Upanishads are now active. Mandukya
is the single remaining gap.

## 2. Missing / incomplete

### Mandukya (the gap)

A repo-wide v103 audit searched **all** data files (not only the
Upanishads family files) for "mandukya" / "māṇḍūkya" / "mandookya"
in passage text bodies. Total hits and their nature:

| File | Hits | Nature |
|------|----:|---|
| `brahma-knowledge-barnett`                   | 2 | List mention ("Mandukya" in the "List of the Chief Upanishads" appendix, id='24.40') + a footnote reference |
| `dakshinamurti-stotra`                       | 2 | Commentary mentions |
| `history-sanskrit-literature-macdonell`      | 7 | MacDonell's history *describes* Mandukya ("a very short prose Upanishad") — does not translate it |
| `the-yoga-vasishtha-maharamayana...vol-1`    | 1 | Allusion |
| `thrice-greatest-hermes-vol-3`               | 1 | Allusion |
| `thrice-greatest-hermes-vol3`                | 1 | Allusion (different translator/edition) |
| `upanishads-30-minor-aiyar`                  | 2 | Editor mentions in introduction (id='2.11', '2.17') quoting the Muktikā Upanishad's list of names |
| `upanishads-muller-part1`                    | 2 | Editor's bibliography ("E. Roer translated... Mandukya"); editor's list of Upanishads studied in Bengal |
| `upanishads-muller-part2`                    | 1 | Editor's discussion of Sankara's commentaries |
| `yoga-vasishtha-mitra-vol1`                  | 1 | Allusion |

**No translation passages exist** in the current archive. Every
hit is editorial commentary, a list mention, or an allusion in
another text.

### Maitri / Maitrayaniya / Maitrayani — recovered ✦

The same repo-wide search for Maitri/Maitrayani text found 21
hits in `upanishads-muller-part2`. Investigation of fm markers in
that file revealed:

  · id='2.280' (fm) = "MAITRAYANA-BRAHMANA-UPANISHAD." — Müller's
    introductory section for the Maitri.
  · id='6.348' (non-fm) = "Maitrayana-Brahmana-Upanishad" — the
    actual translation's section header.
  · id='6.349' (fm) = "FIRST PRAPATHAKA." — first chapter.
  · Through id='6.566' (fm) = "SEVENTH PRAPATHAKA." — seventh
    and final chapter.

**Routable.** v103 adds Maitri as a principal Upanishad with a
safe-start pid-route to id='6.348' in Müller Part 2. The reader
lands at the section header and reads forward through all seven
Prapathakas.

## 3. Source acquisition candidates (for Mandukya)

The Mandukya is short (12 verses / approximately 2 pages of
English text), so a clean ingestion is small in scope. Candidate
public-domain sources:

  1. **Nikhilananda's translation of the Mandukya Upanishad with
     Gaudapada's Karika** (1949) — most complete public-domain
     English Mandukya. Includes the Karika commentary, which
     is itself important. *Caution:* the Karika alone is not the
     Upanishad text; the Mandukya proper must be ingested as a
     distinct unit.
  2. **Robert Ernest Hume — "The Thirteen Principal Upanishads"**
     (Oxford, 1921). Contains a Mandukya translation. Public
     domain.
  3. **Sacred Books of the East** — Müller did NOT include
     Mandukya in either SBE Vol. I or Vol. XV (confirmed by the
     audit above — Müller's own preface lists which Upanishads
     he excluded, and Mandukya is one). So SBE is not a source.
  4. **Swami Sharvananda — "Māndukya Upanishad with the Karika of
     Gaudapada"** (Ramakrishna Math, 1922-ish). Public domain.

Recommendation order: Hume's Thirteen Principal Upanishads
(broadest, well-edited) → Nikhilananda (most popular). Either
fits the archive's translator-credited standards.

Acquisition workflow: place the source TXT in
`02_raw_sources/Library_/<source>/` and run the existing ingestion
pipeline (mirrors the workflow that produced `upanishads_muller.json`).

## 4. Inactive / uncertain table (post-v103)

| Entry | Status | Repair needed |
|---|---|---|
| Mandukya | Honestly absent from current archive — only editor / commentary mentions. | Acquire one of the candidate sources (see §3) and ingest. |
| Aiyar L1=18–33 (Khanda I–XVI and Chapter I–VI) | Sub-section headings without identifiable Upanishad title. Likely covers Tejobindu / Yogashikha / similar minor texts. | Parser repair to recover Upanishad-boundary metadata from the source TXT. (Phase 2.) |

## 5. View-mode integration

- **By Veda view** — Atharvaveda group now shows: Prasna, Mundaka,
  Narada-Parivrajaka, Sandilya (active cards) + a quiet
  non-clickable status card for Mandukya marked "not yet in
  archive" with the acquisition note inline.
- **Traditional order view** — Mandukya appears at the end of the
  Principal Upanishads block as a non-clickable status card.
- **By text view** — unchanged. Maitri is reachable as a
  source-volume route through Müller Part 2.

## 6. Future Phase 3 — Traditional 108 target

Phase 1 closes the principal / major Upanishads gap save for the
single Mandukya acquisition.

Current active count: **35** (12 principal + 23 minor).

The traditional **Muktikā canon** lists 108 Upanishads (including
the principal 10 plus many minor / specialised Upanishads from
the four Vedas plus the Sannyasa, Yoga, and Vaishnava / Saiva /
Shakta subclasses). Phase 3 — when undertaken — would target
that 108 list, classified by:

  · subject class (Samanya, Sannyasa, Yoga, Vaishnava, Saiva, Shakta)
  · Veda affiliation (already present in v102 metadata)
  · current archive availability (status per Upanishad)
  · ingestion priority

That phase is explicitly out of scope for v103. This pass closes
the principal gap honestly; the 108 target remains a future
project.

## What was NOT touched

- No JSON files merged, rewritten, or deleted.
- No source-text passages, fm flags, or chapter_titles modified.
- v100 TEXT_CONTENTS_OVERRIDES preserved.
- All non-Upanishads flows preserved (Bible, Tao, Gita, Iliad,
  Odyssey, etc.).
- Page-type doctrine (shelf scrolls, contents leaf static,
  reading room scrolls) preserved.
- Atlas Object / Folio architecture untouched.
