# Duplicate text ids — what counts as a duplicate

The corpus uses two unrelated kinds of "duplicate id." Conflating them
has caused confusion in past audits, so this document records the
distinction once.

---

## Type A — directory-level shared `id`

The canonical library has **13 `id` values that appear in more than one
`text.json`**. Most are legitimate; a small number are worth a careful
editorial look.

These are detected by `build_registry.py` (which records each text.json
as its own registry entry, regardless of duplicate `id`). The registry
size — 1,131 entries — accordingly exceeds the 1,086 distinct ids by
exactly 45 extras.

### Translation families

A single canonical work with many parallel translations, each in its
own directory. The shared `id` is the work; each directory is one
translation. This is by design.

| Shared id | Directories | Note |
|---|---:|---|
| `bible` | 24 | The KJV/ASV/BBE/Brenton/Darby/Douay/Geneva/LXX/Peshitta/Vulgate/Wycliffe family. Plus tanakh sources. |
| `jataka` | 7 | Five volumes of the Cowell-edition Jataka, plus Babbit's children's selection and Rhys Davids vol. 1. |
| `quran` | 4 | A combined-translations directory plus Rodwell, Yusuf Ali, and Yusuf Ali / Pickthall / Shakir editions. |

### Volume splits

A single multi-volume work where each volume has its own directory but
all share the work's `id`. Volume disambiguation lives in directory
name and in `volume_label`.

| Shared id | Directories |
|---|---:|
| `augustine-city-of-god` | 2 (Dods vol. 1, vol. 2) |
| `calvin-institutes` | 2 (Allen vol. 1, vol. 2) |
| `calvin-letters` | 2 (Bonnet vol. 1, vol. 2) |
| `hippolytus-philosophumena` | 2 (Macmahon vol. 1, vol. 2) |
| `origen-writings` | 2 (Crombie vol. 1, vol. 2) |

### Multi-text in one series, sharing a series id

| Shared id | Directories | Note |
|---|---:|---|
| `expositor-bible` | 4 | Four books in the Expositor's Bible series — Job, Judges & Ruth, Numbers, Revelation. Each is a different book. They legitimately share the series id. |
| `bhagavad-gita` | 2 | Main Gita directory (Gita Society + Arnold) and a separate Arnold-only directory. |
| `mahabharata` | 2 | Ganguli and Dutt translations. |

### Worth a careful look

Two cases where the duplicate id is plausibly an editorial choice but
might be re-examined as the corpus matures. **Do not change these
without a deliberate decision.**

- **`newman-essays` (3 directories).** *Development of Christian
  Doctrine*, *Grammar of Assent*, and *The Idea of a University* —
  three substantively different works by Newman. Sharing the
  `newman-essays` id is convenient for grouping but obscures the
  distinct works. If the corpus ever expects "fetch the work for id
  X," each should likely have its own id.
- **`seneca-minor-dialogues` (2 directories).** Identical translation
  (`stewart`) under both `other/greek-philosophy/` and
  `other/roman-philosophy/`. The translation id matches; this looks
  like a true duplicate left over from a categorization change. Worth
  resolving by deciding which tradition is correct and removing the
  other directory — but **only after confirming nothing references
  the removed path**.

---

## Type B — passage-level dup ids inside one text

A different kind of duplicate. Reported by
`05_scripts/corpus_audit.py` and shown in
`logs/reports/corpus_audit_report.md`. These are passages within a
single `passages_*.json` file that share a structural id (e.g. two
passages both keyed `1.1`). They are parser problems, not
editorial decisions.

The current top affected texts (counts from the most recent run):

| Text | Excess passage dups |
|---|---:|
| `quran` | 158,458 |
| `jataka` | 8,895 |
| `ambrose-select-works` | 2,093 |
| `eusebius-church-history` | 1,881 |
| `expositor-bible` | 1,720 |
| `augustine-confessions-enchiridion-ccel` | 1,092 |
| `calvin-letters` | 1,022 |
| `jerome-letters-works` | 1,002 |
| `athanasius-select-works` | 909 |
| `cyril-nazianzus-select-works` | 820 |

These cluster on texts with multi-book structure where the parser
keyed by `chapter.verse` instead of `book.chapter.verse`, so verse 1
of every book collides. The fix is per-text parser work — a separate,
slow project. They do not affect passage integrity (the
`passage_subsequence_proof` still passes); they affect navigability.

---

## How to read counts

When in doubt, read the current state from the actual files rather
than from any single header number.

- **"How many texts on disk?"** — count `text.json` files. (1,131 today.)
- **"How many distinct works?"** — count distinct `id`s in
  `registry.json`. (1,086 today.)
- **"How many translations exposed to readers?"** — count entries in
  `03_web_app/data/index.json`. (1,200 today.)
- **"How many texts had duplicate-passage-id parser issues?"** — read
  `logs/reports/corpus_audit_report.md`. (48 texts today.)

These are different numbers because they measure different things.
