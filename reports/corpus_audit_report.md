# Corpus Audit Report

## 1. Duplicate-ID Structural Triage

**Texts affected:** 40
**Total excess duplicates:** 12,779

### Category Distribution

| Category | Texts |
|---|---:|
| missing_book_level | 27 |
| front_matter_absorbed | 7 |
| unknown | 4 |
| appendix_collapse | 1 |
| missing_section_level | 1 |

### Priority Queue (top 10)

| Rank | Text | Dups | Category | Action |
|---:|---|---:|---|---|
| 1 | ambrose-select-works | 2,093 | unknown | Manual inspection required — no clear structural p... |
| 2 | eusebius-church-history | 1,881 | front_matter_absorbed | Move prefatory passages to front_matter; start bod... |
| 3 | augustine-confessions-enchiridion-ccel | 1,092 | front_matter_absorbed | Move prefatory passages to front_matter; start bod... |
| 4 | jerome-letters-works | 1,002 | unknown | Manual inspection required — no clear structural p... |
| 5 | athanasius-select-works | 909 | missing_book_level | Switch to book_chapter parser; detect BOOK/PART/bi... |
| 6 | cyril-nazianzus-select-works | 820 | missing_book_level | Switch to book_chapter parser; detect BOOK/PART/bi... |
| 7 | buddha-life-herold | 775 | missing_book_level | Switch to book_chapter parser; detect BOOK/PART/bi... |
| 8 | anf01-early-fathers | 730 | missing_book_level | Switch to book_chapter parser; detect BOOK/PART/bi... |
| 9 | manual-of-hadith | 542 | missing_book_level | Switch to book_chapter parser; detect BOOK/PART/bi... |
| 10 | chrysostom-homilies-matthew | 465 | missing_book_level | Switch to book_chapter parser; detect BOOK/PART/bi... |

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

**Total stubs:** 163,282

### Global Recommendations

| Action | Count |
|---|---:|
| keep | 72,592 |
| review | 47,743 |
| drop | 42,947 |

### Category Distribution

| Category | Count |
|---|---:|
| legitimate_dialogue | 72,592 |
| uncertain | 22,067 |
| roman_numeral_marker | 18,464 |
| heading_fragment | 17,176 |
| residual_artifact | 9,432 |
| structural_label | 7,711 |
| ocr_noise | 6,354 |
| speaker_label | 5,249 |
| separator_divider | 4,237 |
