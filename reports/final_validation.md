# Final Corpus Validation Report

## Health Score

| Metric | Value |
|---|---:|
| Total texts | 1091 |
| Fully clean (0 dups, low leakage) | 666 (61.0%) |
| Acceptable (minor issues) | 109 |
| Needs manual work | 316 (29.0%) |
| Texts with residual dups | 39 |
| Total residual dup passages | 12756 |
| Quality flags raised | 551 |

## Highest Risk Texts

| Text | Dups | Leaks | Status |
|---|---:|---:|---|
| ambrose-select-works | 2093 | 11 | needs_work |
| eusebius-church-history | 1881 | 195 | needs_work |
| aquinas-summa-theologica | 0 | 1449 | needs_work |
| augustine-confessions-enchiridion-ccel | 1092 | 49 | needs_work |
| anf01-early-fathers | 730 | 395 | needs_work |

## Cleanest Texts (largest clean corpora)

| Text | Passages | L1 segments |
|---|---:|---:|
| bible | 31,086 | 66 |
| tanakh | 23,143 | 39 |
| theravada-vinaya | 16,696 | 390 |
| linked-discourses-sujato | 11,416 | 53 |
| numbered-discourses-sujato | 9,963 | 11 |

## Residual Duplicates

| Text | Remaining | Cause | Action |
|---|---:|---|---|
| ambrose-select-works | 2093 | structural_ambiguity | Manual inspection needed — complex nesting |
| eusebius-church-history | 1881 | structural_ambiguity | Manual inspection needed — complex nesting |
| augustine-confessions-enchiridion-ccel | 1092 | structural_ambiguity | Manual inspection needed — complex nesting |
| jerome-letters-works | 1002 | structural_ambiguity | Manual inspection needed — complex nesting |
| athanasius-select-works | 909 | structural_ambiguity | Manual inspection needed — complex nesting |
| cyril-nazianzus-select-works | 820 | structural_ambiguity | Manual inspection needed — complex nesting |
| buddha-life-herold | 775 | structural_ambiguity | Manual inspection needed — complex nesting |
| anf01-early-fathers | 730 | structural_ambiguity | Manual inspection needed — complex nesting |
| manual-of-hadith | 542 | structural_ambiguity | Manual inspection needed — complex nesting |
| chrysostom-homilies-matthew | 465 | structural_ambiguity | Manual inspection needed — complex nesting |
| basil-letters-works | 364 | structural_ambiguity | Manual inspection needed — complex nesting |
| plato-republic | 318 | missed_parent_variant | Check for parent heading variants in the concentra |
| anf04-tertullian-cyprian | 306 | structural_ambiguity | Manual inspection needed — complex nesting |
| josephus-antiquities | 249 | structural_ambiguity | Manual inspection needed — complex nesting |
| gregory-nyssa-select-works | 240 | structural_ambiguity | Manual inspection needed — complex nesting |
| upanishads | 196 | structural_ambiguity | Manual inspection needed — complex nesting |
| luther-good-works | 134 | structural_ambiguity | Manual inspection needed — complex nesting |
| pirke-avot | 123 | missed_parent_variant | Check for parent heading variants in the concentra |
| genealogy-of-morals | 97 | structural_ambiguity | Manual inspection needed — complex nesting |
| tertullian-volume-1 | 95 | structural_ambiguity | Manual inspection needed — complex nesting |

## Quality Flags

| Text | Flag | Severity | Reason |
|---|---|---|---|
| a-very-pleasaunt-fruitful-diologe-called-the-epicur-erasmus | many_short_passages | medium | 18% of passages are ≤15 chars |
| a-wanderer-in-the-sprit-lands-franchezzo-1896 | high_heading_leakage | high | 27 heading-like lines in body |
| abrahams-hebraic-bookland | uneven_segments | medium | Segment size CV = 3.39 (very uneven) |
| abrahams-jewish-literature | uneven_segments | medium | Segment size CV = 3.62 (very uneven) |
| ahiman-rezon | high_heading_leakage | high | 25 heading-like lines in body |
| ambrose-select-works | high_heading_leakage | high | 11 heading-like lines in body |
| analects-legge-1893 | many_short_passages | medium | 44% of passages are ≤15 chars |
| ancient-egypt-george-rawlinson-art | many_short_passages | medium | 15% of passages are ≤15 chars |
| ancient-egyptian-legends | many_short_passages | medium | 24% of passages are ≤15 chars |
| ancient-jewish-proverbs | high_heading_leakage | high | 24 heading-like lines in body |
| anf01-early-fathers | high_heading_leakage | high | 395 heading-like lines in body |
| anf04-tertullian-cyprian | high_heading_leakage | high | 70 heading-like lines in body |
| aquarian-gospel | high_heading_leakage | high | 21 heading-like lines in body |
| aquinas-summa-theologica | high_heading_leakage | high | 1449 heading-like lines in body |
| arabian-poetry-clouston | uneven_segments | medium | Segment size CV = 2.48 (very uneven) |
| aradia-gospel-witches-leland | high_heading_leakage | high | 49 heading-like lines in body |
| aradia-gospel-witches-leland | uneven_segments | medium | Segment size CV = 2.93 (very uneven) |
| aradia-gospel-witches-leland | many_short_passages | medium | 16% of passages are ≤15 chars |
| arnold-roman-stoicism | high_heading_leakage | high | 19 heading-like lines in body |
| arnold-roman-stoicism | uneven_segments | medium | Segment size CV = 2.21 (very uneven) |
