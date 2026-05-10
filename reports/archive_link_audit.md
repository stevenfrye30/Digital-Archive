# Archive link audit

Read-only verification of Reading Room ↔ canonical links.
Run with `python 05_scripts/validate_archive_links.py`.

## Summary

- Reading Room entries on disk: **205**
- Entries with `library_id`: 204
- Entries referenced from `index.md` / `shelves.md`: 57
- Entries reachable from the graph map: 8
- Canonical ids in registry: 1086

## Findings

### Broken `library_id` pointers (0)

*All `library_id` values resolve to a canonical text.*

### Broken `entity.html?id=` references (0)

*Every shelf reference resolves to an existing entry.*

### Entries without a `library_id` (1)

- `sappho-fragment-31`

### Deep-archive entries (not on any shelf, not in graph map) (144)

- `aitareya-aranyaka-book-2`
- `aitareya-aranyaka-book-3`
- `bhagavad-gita-chapter-10`
- `bhagavad-gita-chapter-11`
- `bhagavad-gita-chapter-12`
- `bhagavad-gita-chapter-13`
- `bhagavad-gita-chapter-14`
- `bhagavad-gita-chapter-15`
- `bhagavad-gita-chapter-16`
- `bhagavad-gita-chapter-17`
- `bhagavad-gita-chapter-18`
- `bhagavad-gita-chapter-2`
- `bhagavad-gita-chapter-3`
- `bhagavad-gita-chapter-4`
- `bhagavad-gita-chapter-5`
- `bhagavad-gita-chapter-6`
- `bhagavad-gita-chapter-7`
- `bhagavad-gita-chapter-8`
- `bhagavad-gita-chapter-9`
- `brihadaranyaka-upanishad-book-1-part-3`
- `brihadaranyaka-upanishad-book-1-part-4`
- `brihadaranyaka-upanishad-book-1-part-5`
- `brihadaranyaka-upanishad-book-1-part-6`
- `brihadaranyaka-upanishad-book-2-part-1`
- `brihadaranyaka-upanishad-book-2-part-2`
- `brihadaranyaka-upanishad-book-2-part-3`
- `brihadaranyaka-upanishad-book-2-part-4`
- `brihadaranyaka-upanishad-book-2-part-5`
- `brihadaranyaka-upanishad-book-2-part-6`
- `brihadaranyaka-upanishad-book-3-part-1`
- *… and 114 more*

