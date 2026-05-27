# v109 — Restricted-source protocol

Concurrent with the v109 Hume second-witness ingestion, this pass
establishes the archive's explicit protocol for **copyrighted or
public-domain-uncertain sources**. The goal is to make it
operationally impossible to accidentally ship restricted text to
GitHub Pages while still allowing private research use.

## 1. The risk model

The archive is a public GitHub-Pages site. Anything committed to
`03_web_app/data/` ships to the public internet. Source texts fall
into three categories:

| Category | Examples | Public publication safety |
|---|---|---|
| **PD-safe** | Pre-1929 US-published works (Hume 1921, Müller 1879/1884, Aiyar 1914) | Safe to publish |
| **PD-uncertain** | Indian works pre-1929 with US URAA restoration; 20th-century works whose translator died < 95 years ago; Adyar Library English series 1929–1977 | Defer ingestion; verify or skip |
| **Copyrighted** | Modern translations (Ramanathan 1978, Aiyar Yoga Upanishads 1938 still URAA-restored till 2034, Mahā-Nārāyaṇa modern editions, Marabathina 2024) | Never publish |

Categories 2 and 3 are collectively **restricted**.

## 2. The folder protocol

```
Digital-Archive/
├── 01_library/_restricted/        ← personal copies of restricted works
│   ├── copyrighted/
│   ├── sacred/
│   ├── backups/
│   └── wishlist/
│
├── 02_raw_sources/_restricted/    ← OCR / PDF caches of restricted works
│   ├── README.md
│   └── notes/                     ← per-work copyright-analysis notes
│
└── 03_web_app/data/_restricted/   ← (if used) local-only ingested JSON
                                   ← never registered in index.json
```

Every `_restricted/` folder is excluded by the top-level `.gitignore`.
A user can hold restricted PDFs, OCR caches, and even ingested JSON
copies locally for personal study, while remaining certain that none
of it can ship publicly.

## 3. The `.gitignore` (new at repo root)

```
01_library/_restricted/
02_raw_sources/_restricted/
03_web_app/data/_restricted/
06_workspace/
logs/
.server.pid
```

Workspace-hub deploy scripts (which copy `03_web_app/` into
`workspace-hub/Digital-Archive/`) should be **audited** to confirm
they skip `_restricted/` subfolders. If a deploy script blindly
mirrors `03_web_app/data/`, the `_restricted/` directory would still
not be present in git but would be present on disk; a safe-by-default
deploy explicitly excludes any path containing `_restricted/`.

Recommended deploy filter (pseudocode):

```python
def is_publishable(path: str) -> bool:
    return '_restricted/' not in path and '_restricted\\' not in path
```

## 4. The ingestion-script protocol

Any script in `05_scripts/` that produces a data file from a
restricted source **must**:

1. Read the source from `02_raw_sources/_restricted/…`, not the
   public `02_raw_sources/Library_/…` cache.
2. Write the output to `03_web_app/data/_restricted/…`, not the
   public `data/` root.
3. Skip catalog registration in `data/index.json`. If a local-only
   shadow catalog is useful, register in
   `data/_restricted/index.json` (also gitignored).
4. Emit a one-line warning at script start:
   `WARNING: restricted source — output is local-only, do not commit`.
5. Be referenced in the corresponding `reports/vN_…_report.md` with
   the field `restricted: yes`.

## 5. The witness-routing protocol

The `TEXT_FAMILIES.upanishads.byUpanishad` (and equivalent family
configs) **must not** carry witness entries pointing to restricted
textIds. The witness picker only ever offers PD-safe routes to the
reading room.

If a restricted source is partially valuable (e.g., a 1938 Adyar
Yoga Upanishad edition that contains both Sanskrit and 20th-century
English commentary), the family config may list the work in
`principalMissing` or a similar "known but not active" structure
**with explicit restricted: true flag**, so future contributors know
the work has been considered and consciously deferred — not missed.

## 6. The acquisition-audit protocol

When v105-style acquisition plans surface a candidate source, the
audit must produce a copyright determination **before** any
ingestion work:

| Question | Decision |
|---|---|
| Was the work first published in the US before 1929? | → PD-safe, may publish |
| Was the work first published outside US, in PD in its source country on 1996-01-01? | → PD-safe in US (no URAA restoration) |
| Was the work first published outside US, NOT in PD in its source country on 1996-01-01? | → URAA-restored; US PD = 95 years from publication |
| Is the work post-1977? | → Restricted unless explicit license |
| Is the work between 1929–1977, US-published, with renewed copyright? | → Restricted till 95 years from publication |
| Is the work between 1929–1977, US-published, without renewal? | → PD-safe (verify via Catalog of Copyright Entries) |

The determination is recorded in
`02_raw_sources/_restricted/notes/<work>_copyright_analysis.md` for
restricted works, or in the corresponding `reports/` file for
PD-safe ones.

## 7. Existing restricted works (as of v109)

The following acquisition candidates surfaced through v105–v108 are
restricted under this protocol and remain **not active** in the
archive:

| Work | Reason |
|---|---|
| Ramanathan 1978 Samnyāsa Upanishads (Adyar) | 1978; copyright till 2073 |
| Ayyangar 1938 Yoga Upanishads (Adyar) | 1938 + URAA-restored till 2034 |
| Ayyangar 1935 Saiva Upanishads (Adyar) | 1935 + URAA-restored till 2031 |
| Marabathina 2024 *108 Upanishads* | 2024; copyright till 2119 |
| Modern Mahā-Nārāyaṇa English editions | Various post-1929; case-by-case |
| Most "Theosophical Society" reprints post-1929 | Case-by-case |

None of these works have been ingested. If any of them is acquired
in the future for personal study, the file goes to
`01_library/_restricted/sacred/` and (if OCR'd) to
`02_raw_sources/_restricted/`. The witness-routing config does NOT
get a route to them.

## 8. Hume 1921 — explicitly NOT restricted

The v109 Hume ingestion (this same pass) is **PD-safe**:

- Published by Oxford University Press in the United States in 1921.
- Pre-1929 → US public domain regardless of URAA.
- Hume (1877–1948) died in 1948; even life+70 jurisdictions placed
  the work in PD by 2018.

The full Hume cache lives in the public `02_raw_sources/Library_/`
directory, not `_restricted/`. The ingested JSON lives in the
public `03_web_app/data/` directory and is registered in
`data/index.json`. This is the correct, well-behaved path that the
restricted protocol exists to keep clean of bad neighbours.

## 9. Build marker

This protocol document is part of the `v109-hume-principal-witnesses`
build. The accompanying ingestion report is at
`reports/v109_hume_principal_witnesses.md`.
