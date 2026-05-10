# Corpus Audit Report

## 1. Duplicate-ID Structural Triage

**Texts affected:** 48
**Total excess duplicates:** 184,634

### Category Distribution

| Category | Texts |
|---|---:|
| missing_book_level | 33 |
| front_matter_absorbed | 7 |
| unknown | 5 |
| missing_section_level | 2 |
| regex_partial_detection | 1 |

### Priority Queue (top 10)

| Rank | Text | Dups | Category | Action |
|---:|---|---:|---|---|
| 1 | quran | 158,458 | missing_book_level | Switch to book_chapter parser; detect BOOK/PART/bi... |
| 2 | jataka | 8,895 | missing_book_level | Switch to book_chapter parser; detect BOOK/PART/bi... |
| 3 | ambrose-select-works | 2,093 | unknown | Manual inspection required — no clear structural p... |
| 4 | eusebius-church-history | 1,881 | front_matter_absorbed | Move prefatory passages to front_matter; start bod... |
| 5 | expositor-bible | 1,720 | regex_partial_detection | Expand chapter regex to catch variant formatting (... |
| 6 | augustine-confessions-enchiridion-ccel | 1,092 | front_matter_absorbed | Move prefatory passages to front_matter; start bod... |
| 7 | calvin-letters | 1,022 | missing_book_level | Switch to book_chapter parser; detect BOOK/PART/bi... |
| 8 | jerome-letters-works | 1,002 | unknown | Manual inspection required — no clear structural p... |
| 9 | athanasius-select-works | 909 | missing_book_level | Switch to book_chapter parser; detect BOOK/PART/bi... |
| 10 | cyril-nazianzus-select-works | 820 | missing_book_level | Switch to book_chapter parser; detect BOOK/PART/bi... |

## 2. Front-Matter Recovery

**Texts with missing FM:** 43

### FM Types Found

| Type | Count |
|---|---:|
| contents | 24 |
| introduction | 23 |
| preface | 15 |
| uncertain | 10 |
| editorial_prefatory | 2 |
| dedication | 2 |
| argument_summary | 1 |

## 3. Short-Stub Classification

**Total stubs:** 163,632

### Global Recommendations

| Action | Count |
|---|---:|
| keep | 72,683 |
| review | 47,779 |
| drop | 43,170 |

### Category Distribution

| Category | Count |
|---|---:|
| legitimate_dialogue | 72,683 |
| uncertain | 22,101 |
| roman_numeral_marker | 18,464 |
| heading_fragment | 17,178 |
| residual_artifact | 9,432 |
| structural_label | 7,933 |
| ocr_noise | 6,355 |
| speaker_label | 5,249 |
| separator_divider | 4,237 |
