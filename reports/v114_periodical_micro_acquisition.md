# v114 — Periodical / micro-acquisition pass (acquisition-needed)

The v114 pass searched all 71 unaudited Hindu texts already in the
archive plus the authoritative 1921 Hume bibliography for any
pre-1929 public-domain English translation of the 53 Upanishads
currently missing from both `MUKTIKA_108` and `MUKTIKA_108_AIYAR`.

**Outcome**: No new missing-in-both Upanishads could be safely
added in this pass. The pre-1929 PD English landscape for the
minor Upanishads beyond Aiyar 1914's *Thirty Minor* and Sastri
1920's *Dakshinamurti Stotra* (added v113) is **structurally
empty** — confirmed by Hume's own bibliography. v114 produces a
rigorous acquisition-needed report and ships zero new routes.

## 1. Summary

| Field | Value |
|---|---|
| Build before v114 | `v113-dual-canon-acquisition-batch` |
| Build after v114 | **`v114-periodical-acquisition-needed`** |
| Primary `MUKTIKA_108` active | 43 / 108 (unchanged) |
| Aiyar `MUKTIKA_108_AIYAR` active | 43 / 108 (unchanged) |
| Missing in primary | 65 (unchanged) |
| Missing in Aiyar | 65 (unchanged) |
| Missing in BOTH | 53 (unchanged) |
| byUpanishad routes | 44 (unchanged) |
| New texts ingested | **0** |
| New parser scripts created | **0** |
| New data files created | **0** |
| New `data/index.json` entries | **0** |
| Restricted text committed | none |
| Public routes to restricted text | none |
| Files touched | `index.html` (build marker only), `reports/v114_…md` (new), `05_scripts/v113_dual_missing_intersection.py` (reused from v113) |

## 2. Missing-in-both search set (53 entries after v113)

The missing-in-both intersection is unchanged from v113 §2 of
`reports/v113_dual_canon_acquisition_priority.md`. By class:

| Class | Count | Status |
|---|---:|---|
| Sannyāsa (S) | 12 | None routed |
| Shaiva (Sh) | 7 | Dakṣiṇāmūrti was routed in v113; 7 remain |
| Shakta (Sk) | 9 | None routed |
| sāmānya Vedānta (V) | 10 | None routed |
| Yoga (Y) | 6 | None routed |
| Vaishnava (Vs) | 5 | None routed |
| Sub-classed or other (?) | 4 | edge cases |
| **Total** | **53** | |

## 3. Local search results

### 3.1 Scope

* `data/index.json` — 1203 catalog entries, 83 Hindu texts.
* 71 unaudited Hindu sources (the 12 sources already audited in
  v109-v113 — Müller complete, Müller Parts 1-2, Aiyar, Johnston,
  Hume 1921, Sastri Dakshinamurti, both Vedanta-Sutras commentaries
  — were skipped).
* `02_raw_sources/Library_/` — InternetArchive, SacredTexts.com,
  Gutenberg.org, openlibrary.org caches.
* Text-content search across passages of all 71 unaudited Hindu
  files for the 12 most-distinctive missing-in-both target names.

### 3.2 Catalog-level hits inspected

The following non-routed Hindu sources were promising candidates
and were inspected in detail:

| Source | Year | Translator | Verdict |
|---|---:|---|---|
| `brahma-knowledge-barnett` *Brahma Knowledge* | 1907 | L.D. Barnett | **Anthology of excerpts only** — 16 thematic chapters with selections from Brihadaranyaka, Chandogya, Aitareya, Mundaka; no full minor Upanishads. Per principle "do not count incomplete excerpts as full texts," no routes added. |
| `shankara-select-works` *Select Works of Sri Sankaracharya* | 1911 | S. Venkataramanan | **Sankara's own treatises and hymns** (Atmabodha-treatise, Vivekachudamani, Aparokshanubhuti, Dakshinamurti-stotra), not Upanishads. The Atmabodha-treatise is Sankara's own composition, not the Atmabodha-Upanishad (which is already active via Aiyar L1=11). |
| `besant-yoga` *An Introduction to Yoga* | 1908 | Annie Besant | **Yoga philosophy lectures**, not Upanishad translations. |
| `tamil-saivite-hymns` | 1921 | F. Kingsbury, G.E. Phillips | **Tamil Saivite devotional hymns** (Tevaram + Tiruvasakam), not Sanskrit Upanishads. |
| `arnold-hindu-literature` *Hindu Literature* | 1899 | Edwin Arnold | Hitopadesa fables + Mahabharata excerpts + Ramayana — no Upanishad content. |
| `arnold-indian-poetry` *Indian Poetry* | 1881 | Edwin Arnold | Gita Govinda + Mahabharata excerpts — no Upanishad content. |
| `garuda-purana` 1911 | 1911 | Ernest Wood, S.V. Subrahmanyam | Garuda Purana mentions Paramahaṃsa as a *type of renunciate*, not the Paramahaṃsa Upanishad. |
| `dasgupta-indian-philosophy` Vol 1 | 1922 | Surendranath Dasgupta | **Scholarly survey** of Indian philosophy; discusses Upanishads thematically and quotes from them but is not itself a translation source. |
| `tagore-sadhana` *Sadhana: The Realisation of Life* | 1913 | Rabindranath Tagore | Philosophical lectures, not Upanishad translations. |
| `vivekananda-jnana-yoga` *Jñāna Yoga* Part 2 | 1915 | Swami Vivekananda | Lecture series on Vedanta themes, not Upanishad text. |
| `yajur-veda-keith` *The Yajur Veda (Taittiriya Saṃhitā)* | 1914 | Arthur Berriedale Keith | Taittiriya Saṃhitā mantras, not Upanishad text — the embedded Maha-Narayana Upanishad is NOT present in Keith's translation. |
| `vivekananda-karma-yoga` *Karma-Yoga* | 1896 | Swami Vivekananda | Lectures on karma yoga, not Upanishads. |
| Yoga-Vasishtha volumes (Mitra 1891 + 1900) | 1891-1900 | Mitra | Yoga-Vasishtha epic narrative; mentions "kshurika" in unrelated context (trapper weapons). |

### 3.3 Text-content search for top targets

A text-content search across all 71 unaudited Hindu sources for
the 12 most-distinctive missing-in-both name terms produced:

| Target | Hits | Verdict |
|---|---:|---|
| paramahamsa | 20 hits in 8 files | All MENTIONS of paramahaṃsa as a renunciate type, not the Paramahaṃsa Upanishad |
| kshurika | 2 hits | Unrelated Yoga-Vasishtha word usage |
| mahanarayana | 4 hits | Barnett's TOC + Macdonell's history (discussion only) |
| atharvasiras | 4 hits | Mahabharata mentions only |
| nirvana, turiyatita, kalagnirudra, mahavakya, pranagnihotra, brahmavidya, rudrahridaya, panchabrahma | **0 hits** | No mention in any unaudited Hindu source |

**Conclusion**: No local Hindu source contains the full English
text of any missing-in-both Upanishad.

## 4. External / bibliographic source-family survey

### 4.1 Hume 1921 authoritative bibliography mining

`02_raw_sources/Library_/InternetArchive/Hume-1921-Thirteen-Principal-Upanishads.txt`
contains Hume's comprehensive bibliography (lines 28545–33500) of
all known Upanishad editions and translations through 1921. The
bibliography organises entries by Upanishad. Every section header
found:

```
Brihad-Aranyaka, Chandogya, Aitareya, Kaushitaki, Kena, Katha,
Mundaka, Svetasvatara, Mandukya, Taittiriya, Prasna, Maitri
```

= **the 13 principal Upanishads only.** No section in Hume's
bibliography is headed by any of the 53 missing-in-both names
(Nirvana, Paramahamsa, Atharvasiras, Atharvasikha, Brihajjabala,
Kalagnirudra, Daksinamurti, Rudrahridaya, Pancabrahma,
Brahmavidya, Yogasikha, Yogachudamani, Mahanarayana, Nrsimha-
tapani, Tripura, Devi, etc.).

This is **definitive evidence** that pre-1929 English translation
work focused almost exclusively on the principal canon. The
13-principal scholarly tradition (Müller → Tattvabhushan →
Sitaram Sastri+Jha → Vasu → Hume) treated the minor Upanishads
as secondary; they were left for the post-1929 Adyar Library
English Series.

### 4.2 Pre-1929 PD English sources Hume catalogues — all PRINCIPAL Upanishads

| Source | Year | Translator | Coverage | Status |
|---|---:|---|---|---|
| Sastri & Jha *The Upanishads and Sri Sankara's Commentary* (5 vols) | 1898–1901 | S. Sitarama Sastri, Ganganath Jha | Isa, Kena, Mundaka, Katha, Prasna, Chandogya 1-8, Aitareya, Taittiriya | **PD-safe**, NOT in archive. Would provide second/third witnesses for principals (similar role to Hume 1921). v115 candidate. |
| Tattvabhushan *The Upanishads* (3 vols) | 1900–1904 | Sitanath Tattvabhushan | All 12 of the 13 principals (missing Maitri) | **PD-safe**, NOT in archive. Same role as above. |
| Vasu *Sacred Books of the Hindus* — Vol 1 *Six Upanishads* | 1911 | Srisa Chandra Vasu | Isa, Kena, Katha, Prasna, Mundaka, Manduka | **PD-safe**, NOT in archive. Same role. |
| Vasu *Sacred Books of the Hindus* — Vol 3 *Chandogya* | 1909–10 (rpt 1917) | Vasu | Chandogya | **PD-safe**, NOT in archive. |
| Vasu *Sacred Books of the Hindus* — Vol 14 *Brihadaranyaka* | 1913 | Vasu | Brihadaranyaka | **PD-safe**, NOT in archive. |
| Bhagavata *The Aitareya Upanishad* | 1898 | Rajaram Ramkrishna Bhagavata | Aitareya | **PD-safe**, NOT in archive. |
| A. Mahadeva Sastri *The Taittiriya Upanishad* | 1903 | A. Mahadeva Sastri | Taittiriya | **PD-safe**, NOT in archive. |

**None of these covers any of the missing-in-both 53 minor
Upanishads.** They are all principal-Upanishad sources. Adding
them as new family members would enrich the principal witness
picker but not advance Muktikā coverage.

### 4.3 Sanskrit-only and German sources Hume catalogues

| Source | Year | Notes |
|---|---:|---|
| Bohtlingk *Drei … Upanishaden* | 1891 | German, Katha+Aitareya+Prasna |
| Bohtlingk *Brhadaranjakopanishad* | 1889 | German, Brihadaranyaka |
| Bohtlingk *Khandogjopanishad* | 1889 | German, Chandogya |
| Venkatesvara Press *Sanskrit Upanishad-Vol* including Nrisimhatapanlya | 1890 | Sanskrit Devanagari only |
| Various Bibliotheca Indica volumes | 1840s–1860s | Edward Röer's editions — mostly Sanskrit with English notes; English translations cover principals only |

**Rejected as English reading witnesses** per the v109 protocol
(Sanskrit-only or non-English sources do not become English
reading witnesses).

### 4.4 Periodical search attempts

| Periodical | Years | Outcome |
|---|---|---|
| *The Theosophist* | 1879–1928 (PD) | Not surveyed directly — no local cache. WebFetch on Internet Archive search returned no actionable item listings (the search page is JavaScript-rendered and not parseable). v115 candidate. |
| *The Theosophical Quarterly* | 1904–1938 | Same. Charles Johnston published Upanishad translations here, but the archive already has his consolidated 1899 *From the Upanishads* covering Katha/Kena/Chandogya principals. |
| *Indian Antiquary* | 1872–1933 (pre-1929 PD) | Not surveyed directly. |
| *Journal of the Royal Asiatic Society* | 1834+ (pre-1929 PD) | Not surveyed directly. |
| *Adyar Library Bulletin* | 1937+ | Post-1929; URAA-restricted. |

The four PD periodicals above (Theosophist, Theosophical
Quarterly, Indian Antiquary, JRAS) collectively are the **only
remaining plausible PD English source family** for the missing-in-
both 53. A v115 acquisition pass requires either:
1. A local cache of those periodicals (none currently exists), or
2. External web-fetching capability to traverse IA listings (the
   WebFetch tool exists but the IA search interface is JS-rendered
   and not directly scrapable; specific item URLs would need to
   be supplied or guessed), or
3. Manual user direction toward specific known PD candidate
   identifiers on IA.

### 4.5 Other PD English candidates not in Hume's bibliography (post-1921)

| Source | Year | Translator | Status |
|---|---:|---|---|
| Swami Paramananda *The Mundaka Upanishad* | 1911 | Paramananda (Vedanta Society of America) | **PD-safe**, NOT in archive. Mundaka is already routed via Müller; adding Paramananda would be a second witness. |
| Swami Paramananda *The Maitrayana Brahmana Upanishad* | 1912 | Paramananda | **PD-safe**, NOT in archive. Maitri already routed via Müller Part 2 + Hume; second witness candidate. |
| Swami Paramananda *Self-Knowledge: Atma-Bodha* | 1911 | Paramananda | **PD-safe**, NOT in archive. Sankara's Atma-bodha treatise, similar to Shankara Select Works' Atma-bodha. |
| Annie Besant & Bhagavan Das *Sanatana Dharma* | 1903 | Besant + Das | **PD-safe**, NOT in archive. Excerpts only. |
| Annie Besant *Wisdom of the Upanishats* | 1907 | Annie Besant | **PD-safe**, NOT in archive. Anthology/synthesis, not direct translation. |
| Edward Carpenter *Light from the East* | 1927 | Carpenter | **PD-safe**, NOT in archive. Devotional anthology with Upanishad excerpts. |

**None of these covers a missing-in-both Upanishad** that isn't
also covered by Müller / Hume / Aiyar / Sastri 1920 (already in
the archive).

## 5. Ingestion summary

**Zero new texts ingested.**

* No new source files added to `02_raw_sources/`.
* No new parser scripts created in `05_scripts/`.
* No new data JSON / .gz files created in `03_web_app/data/`.
* No new catalog entry in `data/index.json`.
* No new `byUpanishad` entries added.
* No `MUKTIKA_108` keys changed.
* No `MUKTIKA_108_AIYAR` keys changed.
* No `members[]` additions.

The only change in `index.html` is the build marker line.

## 6. Deferred leads (for v115+ acquisition planning)

### 6.1 High-priority (PD-safe but principal-only — would not advance missing-in-both)

1. **Sastri & Jha 1898–1901** *The Upanishads and Sri Sankara's
   Commentary* (5 vols) — covers Isa, Kena, Mundaka, Katha, Prasna,
   Chandogya, Aitareya, Taittiriya as Sankara-commentary English
   translation. Would add scholar-grade second/third witnesses.
2. **Tattvabhushan 1900–1904** *The Upanishads* (3 vols) — covers
   12 of 13 principals.
3. **Vasu 1909–1917** *Sacred Books of the Hindus* series (vols
   1, 3, 14) — covers principals.
4. **Paramananda's individual Vedanta Society of America
   volumes** (1911–1916) — Mundaka, Maitrayana-Brahmana,
   Atma-bodha treatise.
5. **A. Mahadeva Sastri 1903** *Taittiriya Upanishad* with
   Sankara/Suresvara/Sayana commentaries — same translator as
   v113's Dakshinamurti Stotra source; potentially other minor
   Upanishads with embedded Sankara commentary may exist as
   separate Sastri volumes (e.g., *Saiva-Bhushyam*?). Verification
   needed.

### 6.2 Medium-priority (might surface minor Upanishads)

6. **Theosophist back-issues 1879–1928** — *The Theosophist*
   journal published in Adyar, edited by Olcott then Besant. Full
   PD up to 1928 (cutoff for US PD via URAA expiry on the editorial
   matter; individual translations PD by date of publication).
   May contain individual minor Upanishad translations by Olcott,
   Sinnett, Judge, Chatterji, Sitaram Sastri, etc. **Requires direct
   IA browsing or a local cache.**
7. **Indian Antiquary 1872–1928** — published by Royal Asiatic
   Society of Bengal. Similar profile.
8. **K.K. Mitra and Sitanath Datta translations** (Calcutta-based
   Theosophists, 1890s–1910s) — Hume's bibliography mentions
   "Sitanath Datta, the annotator of the Upanishadas" (line 31239).

### 6.3 Low-priority (rights-blocked but eventual PD-entry)

9. **Adyar Library Saiva Upanishads (Ayyangar 1935)** — URAA-
   restricted; enters US PD 2031-01-01. Would close 7 of the 8
   missing-in-both Shaiva entries in a single ingestion.
10. **Adyar Library Yoga Upanishads (Ayyangar 1938)** — enters US
    PD 2034-01-01. Would close 5–6 missing-in-both Yoga entries.
11. **Other Adyar English series** (1941, 1945, 1950) and the
    Ramanathan 1978 Samnyasa volume.

### 6.4 Rejected

| Source | Reason |
|---|---|
| Marabathina 2024 *108 Upanishads* | Active copyright till 2120 |
| Bedekar & Palsule 1980 *Sixty Upanishads of the Veda* | Active copyright till 2075 |
| Deussen 1897 *Sechzig Upanishads* | German-only |
| Adyar Sanskrit-only 1925/1929 | Sanskrit-only |

## 7. Honest assessment of the missing-in-both 53

For each missing-in-both Upanishad, the earliest plausible
ingestion year (or "never" if no clear PD path):

| Class | Count | Earliest plausible US-PD English source |
|---|---:|---|
| Sannyāsa (12) | 12 | 2074 (Ramanathan 1978) for all 12 |
| Shaiva (7) | 7 | **2031** (Ayyangar 1935) for 7 |
| Shakta (9) | 9 | **2046** (Warrier 1950) for 9 |
| sāmānya Vedānta (10) | 10 | **2037** (Adyar 1941) for 10 |
| Yoga (6) | 6 | **2034** (Ayyangar 1938) for 6 |
| Vaishnava (5) | 5 | **2041** (Adyar 1945) for 5 |
| **Total** | **49** | 2031–2074 |

(Four edge-case entries with class '?' are not counted in the
class totals above.)

**The bulk of the missing-in-both 53 cannot be safely closed
without waiting 7–53 years for the Adyar Library English Series
to enter US public domain**, OR finding individual Theosophical
journal translations that the in-archive Hume bibliography didn't
catalogue but that nonetheless exist.

## 8. Next recommendation (v115+)

### v115: Add Sastri & Jha 1898–1901 OR Tattvabhushan 1900–1904 as Müller/Hume-style second witnesses

Neither advances missing-in-both, but both:
* Add scholarly translation diversity (two more Sanskrit-commentary
  translations alongside Hume and Müller).
* Increase the witness picker's depth on the principal Upanishads.
* Are clean PD-safe acquisitions following the well-tested v109
  Hume pattern.
* Sastri & Jha's *with Sankara's Commentary* edition is
  particularly valuable as the canonical Advaita reading.

### v116: Theosophist-back-issue micro-search

Requires either (a) user direction toward specific IA item
identifiers, (b) a manual cache import, or (c) a different web-
search tool than WebFetch (which can't parse IA's JS-rendered
search). Expected yield: 0–5 entries.

### v117: Schedule 2031 Adyar Saiva trigger

The single highest-value future event for missing-in-both. Document
the precise Ayyangar 1935 *Saiva-Upanishads* IA identifier and
acquisition pipeline for automated ingestion on 2031-01-01.

### v118: Resume non-acquisition work

If the user wants to pause acquisition (which has produced
diminishing returns from v107's Muktikā discovery through v113's
Dakshinamurti to v114's empty pass), v118+ could profitably
return to:
* Cleaning up apparent duplicates in primary `MUKTIKA_108`
  (Tripurā ×4, Saubhāgya ×2, Avadhūta ×2, Devī ×2, Bhāvanā ×2)
  — see v112 §4.4.
* The optional Aiyar-canon-primary switch (v112 §8 v114
  recommendation).
* Other archive surfaces beyond the Upanishads family page.

## 9. Non-destructive guarantees

* **No JSON files merged, rewritten, or deleted.**
* **No source files added or modified.**
* **No catalog entries changed.**
* **No `MUKTIKA_108` or `MUKTIKA_108_AIYAR` keys changed.**
* **No `byUpanishad` entries added or modified.**
* **No restricted text committed.**
* **No public routes to restricted text.**
* **No UI redesign.** The only `index.html` change is the
  build-marker `content` attribute.
* **No folio / Atlas-Object work.**
* **Canon architecture unchanged.** Model C dual-canon from v112
  preserved verbatim.

## 10. Build marker

`v113-dual-canon-acquisition-batch` → **`v114-periodical-acquisition-needed`**

The marker reflects the honest outcome: a deep search was performed,
no new safe routes surfaced, and the next acquisition opportunities
are documented for v115+ (Sastri-Jha 1898–1901 second-witness
batch) and 2031 (Adyar Saiva entering US PD).
