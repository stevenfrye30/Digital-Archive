# Commentary Schema — Reference Sketch

*v1 · 2026-05-14 · illustrative only; not adopted, not implemented.*

This document is **not** part of the constitutional set. The four
adopted architectural documents are:

- `COMMENTARY_CONSTITUTION.md`
- `COMMENTARY_ONTOLOGY.md`
- `COMMENTARY_ATTACHMENT_MODEL.md`
- `PROVENANCE_LAYERS.md`
- `INTERPRETIVE_BOUNDARIES.md`

This file is a sketch of what an implementation that obeyed all four
*might* look like. It exists to ground the architecture in something
concrete enough to argue with. It is the **most likely to change**
of the documents in this constitutional set; it should be the
**least cited** by any other.

When commentary implementation begins, the schema may differ from
this sketch. The constitution will not.

---

## 1. File layout

A commentary record set lives in a sibling family of files to the
existing `apparatus_*.json`, under the canonical text's directory:

```
01_library/library/texts/sacred/buddhist/jataka-vol6/
├── text.json
├── passages_cowell-rouse-vol6.json
├── apparatus_cowell-rouse-vol6.json     # existing pattern
├── commentary_editorial.json            # Layer 5 — archive editorial notes
├── commentary_scholarship.json          # Layer 4 — modern scholarship
├── commentary_ai.json                   # Layer 6 — AI suggestions
└── commentary_ai/                       # if Layer-6 records grow large
    ├── 2026-05-14_motif-tagging.json
    └── ...
```

The naming pattern `commentary_<layer>.json` separates layers at
the filesystem level, as `PROVENANCE_LAYERS.md §9` requires.

Layer 3 (traditional commentary) is **not** in this sibling family.
A traditional commentary is its own primary text in another
directory; only the *attachment* records — the bridges between
that commentary's passages and this text's passages — live in a
separate file:

```
01_library/library/texts/sacred/buddhist/jataka-vol6/
└── attachments_traditional.json          # Layer 3 — anchored references to other primary texts
```

Layer 7 (private annotations) does not live in the canonical
record set at all. The reader's storage holds it.

---

## 2. Record shape

A commentary record carries the structure:

```json
{
  "version": 1,
  "id": "<stable record id>",
  "provenance": {
    "layer": "editorial | scholarship | ai | traditional",
    "author": "<named author or model>",
    "date": "2026-05-14",
    "source": { ... }
  },
  "body": "<verbatim text of the comment>",
  "body_language": "en",
  "categories": ["philological", "cross-civilizational"],
  "category_vocab_version": 1,
  "anchors": [
    { "target": "archive:passage:jataka::cowell-rouse-vol6::10.1" },
    { "target": "archive:passage:jataka::cowell-rouse-vol6::10.1",
      "sub_locator": { "type": "phrase", "value": "Ten boons", "nth": 1 } }
  ],
  "reference_text": "Jātaka VI.10.1 (Cowell & Rouse, Vessantara opening)",
  "stewardship_log": [
    { "date": "2026-05-14", "action": "created", "by": "archive:steward:steve" }
  ]
}
```

Field-by-field:

| Field | Required? | Notes |
|---|---|---|
| `version` | yes | Schema version. v1 today. |
| `id` | yes | Stable record id. Format: layer-prefix + timestamp + slug, e.g., `editorial-2026-05-14-vessantara-opening`. |
| `provenance.layer` | yes | One of the seven layer names; see `PROVENANCE_LAYERS.md`. |
| `provenance.author` | yes | Named author. `archive:steward:<name>`, `archive:ai:<model>`, `scholar:<id>`, etc. Never anonymous. |
| `provenance.date` | yes | ISO date of authorship. |
| `provenance.source` | conditional | For scholarship: journal/book citation. For AI: prompt context. For editorial: usually empty (the steward is the source). |
| `body` | yes | Verbatim claim text. Discipline of `SCHEMA.md`'s apparatus rule extends here. |
| `body_language` | yes | ISO language code. |
| `categories` | optional | Zero, one, or many; from `COMMENTARY_ONTOLOGY.md §4`. |
| `category_vocab_version` | conditional | Required when categories are non-empty. |
| `anchors` | yes | At least one. Each anchor follows `COMMENTARY_ATTACHMENT_MODEL.md §1`. |
| `reference_text` | optional | Human-readable citation for display. |
| `stewardship_log` | yes | Append-only history of actions on this record. |

---

## 3. An editorial example (Layer 5)

```json
{
  "version": 1,
  "id": "editorial-2026-05-14-mtjga-pakkha-ocr",
  "provenance": {
    "layer": "editorial",
    "author": "archive:steward:steve",
    "date": "2026-05-14"
  },
  "body": "The tale title preserved here as MtJGA-PAKKHA-JATAKA is an OCR misread of the canonical Pāli MŪGA-PAKKHA-JĀTAKA — the 'tale of the silent prince', jātaka 538. The 'tJ' was the scanner mistaking M + Ū for M + t + J. The misread is preserved verbatim in the canonical record per the verbatim discipline (SCHEMA.md, COMMENTARY_CONSTITUTION.md §7). This editorial note records the correct reading without modifying the source. A future OCR-cleanup restoration pass may correct the title with confidence; until then, both readings are recorded.",
  "body_language": "en",
  "categories": ["editorial", "philological", "restoration"],
  "category_vocab_version": 1,
  "anchors": [
    {
      "target": "archive:chapter:jataka::cowell-rouse-vol6::1"
    },
    {
      "target": "archive:passage:jataka::cowell-rouse-vol6::1.1",
      "sub_locator": { "type": "phrase", "value": "MtJGA-PAKKHA", "nth": 1 }
    }
  ],
  "reference_text": "Jātaka Vol 6, ch. 1, title and passage 1.1",
  "stewardship_log": [
    { "date": "2026-05-14", "action": "created", "by": "archive:steward:steve",
      "note": "Per Jātaka Vol 6 acquisition restoration; OCR drift recorded as found, correction noted in commentary layer." }
  ]
}
```

---

## 4. A scholarship example (Layer 4)

```json
{
  "version": 1,
  "id": "scholarship-2026-05-14-vessantara-dana-paramita",
  "provenance": {
    "layer": "scholarship",
    "author": "scholar:steven-collins",
    "date": "1998",
    "source": {
      "title": "Nirvana and Other Buddhist Felicities",
      "publisher": "Cambridge University Press",
      "year": 1998,
      "isbn": "978-0521570541",
      "page_range": "497-554"
    }
  },
  "body": "Vessantara's gift of his own children, the moment which has most disturbed Western readers of the Jātaka, has within the Theravada commentarial tradition been read not as a violation of paternal duty but as the highest expression of dāna-pāramitā — the perfection of giving. The Jātakaṭṭhakathā's treatment of this episode is itself a study in how the canon negotiates between household ethics and the bodhisatta's distinct moral logic.",
  "body_language": "en",
  "categories": ["doctrinal", "narrative-motif"],
  "category_vocab_version": 1,
  "anchors": [
    {
      "target": "archive:tale:jataka::547"
    }
  ],
  "reference_text": "Vessantara-jātaka (Jātaka 547)",
  "stewardship_log": [
    { "date": "2026-05-14", "action": "created", "by": "archive:steward:steve",
      "note": "Citing Collins (1998) as a representative modern scholarly reading. Other readings exist and would attach to the same tale anchor in parallel." }
  ]
}
```

---

## 5. An AI example (Layer 6)

```json
{
  "version": 1,
  "id": "ai-2026-05-14-vessantara-bible-parallel",
  "provenance": {
    "layer": "ai",
    "author": "archive:ai:claude-opus-4-7",
    "date": "2026-05-14",
    "source": {
      "model_id": "claude-opus-4-7",
      "model_date": "2026-01",
      "prompt_summary": "Suggest cross-civilizational parallels for the Vessantara-jātaka's narrative of total renunciation."
    }
  },
  "body": "The Vessantara-jātaka and the Akedah (Genesis 22) share a structural feature: the saint or patriarch is asked to give up their child as an extreme test of religious commitment. The two narratives differ in trajectory — Vessantara's children are restored to him through the tale's later events; Isaac is restored by divine intervention; and the moral framings differ across Theravada Buddhism and rabbinic Judaism — but the narrative shape, of the parent's willingness to surrender the child, is structurally analogous.",
  "body_language": "en",
  "categories": ["cross-civilizational", "narrative-motif"],
  "category_vocab_version": 1,
  "anchors": [
    { "target": "archive:tale:jataka::547" },
    { "target": "archive:passage:tanakh::leeser::genesis-22" }
  ],
  "reference_text": "Vessantara-jātaka (Jātaka 547) ↔ Akedah (Genesis 22)",
  "stewardship_log": [
    { "date": "2026-05-14", "action": "created", "by": "archive:ai:claude-opus-4-7",
      "note": "Layer-6 suggestion. Not endorsed by a steward. Off by default in reader views." }
  ]
}
```

Notice this record's display rules under `PROVENANCE_LAYERS.md §7`:
visually quarantined, off by default, never silently promoted, the
model and date preserved with the body. If a steward later decides
to endorse this parallel, they author a new Layer-5 record citing
this Layer-6 record; both remain.

---

## 6. A traditional-commentary attachment example (Layer 3)

A Layer-3 record bridges two primary texts. Here, the bridge from a
hypothetical Jātakaṭṭhakathā commentary on Vessantara back to the
Vessantara primary text:

```json
{
  "version": 1,
  "id": "traditional-jatakatthakatha-vessantara-prologue",
  "provenance": {
    "layer": "traditional",
    "author": "primary:jatakatthakatha::buddhaghosa",
    "date": "c. 5th century CE",
    "source": {
      "tradition": "Theravada",
      "note": "Bridge record from the Jātakaṭṭhakathā commentary tradition to Cowell-Rouse Jātaka VI."
    }
  },
  "body": null,
  "body_language": null,
  "body_in_other_record": "archive:passage:jatakatthakatha::primary-translation::547.0.1",
  "categories": [],
  "anchors": [
    { "target": "archive:tale:jataka::547" }
  ],
  "reference_text": "Jātakaṭṭhakathā on Vessantara",
  "stewardship_log": [
    { "date": "2026-05-14", "action": "created", "by": "archive:steward:steve",
      "note": "Bridge record; awaits acquisition of the Jātakaṭṭhakathā as a primary text." }
  ]
}
```

The `body` is `null` because Layer-3 attachments carry the
relationship, not the prose. The prose lives in the traditional
commentary's own primary record, named in `body_in_other_record`.

---

## 7. What this sketch does *not* yet decide

These remain open for the implementation phase:

- **Record-id format conventions** in detail.
- **Migration semantics** between schema versions.
- **The exact storage format** of Layer 7 (private annotations) on
  reader-controlled devices.
- **The renderer's display rules** — which layer uses which
  typography, color, position. Decisions belong to the renderer's
  own design document.
- **The query API** for finding all commentary on a passage. The
  inverse index is the renderer's responsibility (per
  `COMMENTARY_ATTACHMENT_MODEL.md §8`); how it builds and stores it
  is implementation-specific.
- **Acquisition workflow** for ingesting a large traditional
  commentary corpus (a tafsīr, a Talmud edition, the
  Jātakaṭṭhakathā). The acquisition pattern of the Cowell Jātaka
  Vol 6 (see `JATAKA_VOL6_ACQUISITION_2026.md`) is a precedent but
  not yet generalized.

These are intentionally deferred. The constitution exists so that
when these decisions arrive, they are made under known rules.

---

## 8. Versioning

This schema sketch is v1, dated 2026-05-14. When an actual schema is
adopted — by a stewardship decision, recorded with the same
discipline as any other major restoration — that adoption will
supersede this sketch. The sketch will be retained for historical
continuity, marked as such.

The constitutional documents (`COMMENTARY_CONSTITUTION.md`,
`COMMENTARY_ONTOLOGY.md`, `COMMENTARY_ATTACHMENT_MODEL.md`,
`PROVENANCE_LAYERS.md`, `INTERPRETIVE_BOUNDARIES.md`) are amendable
but are not expected to need amendment soon. The schema sketch is
expected to change considerably before adoption.

The constitution is the floor; this sketch is the first drawing on
the ground. The building will not look exactly like the drawing.
The drawing exists so the floor can be felt under it.
