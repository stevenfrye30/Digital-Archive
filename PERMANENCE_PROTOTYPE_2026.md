# PERMANENCE_PROTOTYPE_2026

**Status:** Prototype.
**Scope:** One tale (Apannaka-jātaka, Jātaka 1), one translation
(`chalmers-vol1`), one set of synthetic test fixtures, fifteen test
citations.
**Result:** 15 of 15 test citations behave as the constitutional documents
say they must, with substantive supporting evidence in the resolver
response — not silent agreement.
**Date:** 2026-05-14.

This document is the operational counterpart to the constitutional
permanence architecture established earlier in May 2026
(CITATION_PERMANENCE.md, COMMENTARY_LIFECYCLE.md, COMMENTARY_VERSIONING.md,
COMMENTARY_MIGRATION.md, COMMENTARY_REPAIR_PROTOCOLS.md). It records what
happened when the architecture's claims were exercised against actual
code.

The prototype is intentionally small. Its purpose is not to be a
production resolver. Its purpose is to confirm that the constitutional
permanence commitments survive contact with operational behavior — and to
surface, honestly, the places where they almost did not.

---

## 1. What was built

Two scripts and four fixture files.

- **`05_scripts/resolve_urn.py`** — A read-only URN resolver supporting
  the eight kinds enumerated in the URN scheme (`text`, `tale`,
  `translation`, `chapter`, `passage`, `range`, `commentary`, `apparatus`),
  with alias-chain traversal, sub-locator evaluation, lifecycle-state
  surfacing, frozen-policy preservation, AI quarantine preservation, and
  explicit failure modes (`malformed`, `missing`, `retired`, `ambiguous`).
- **`05_scripts/verify_permanence.py`** — A verification harness that
  loads the test-citation fixture and runs each URN through the resolver,
  comparing the response to the expected outcome. Produces both a
  machine-readable JSON audit and a human-readable Markdown audit.
- **`01_library/library/permanence/aliases.json`** — The real
  (production-bound, currently empty) alias table.
- **`01_library/library/permanence/test_fixtures/aliases.json`** — Three
  synthetic test aliases (re-keyed, retired, id-corrected).
- **`01_library/library/permanence/test_fixtures/commentary_test.json`** —
  Five synthetic commentary records demonstrating withdrawn, superseded,
  successor, frozen, and orphaned states.
- **`01_library/library/permanence/test_fixtures/test_citations.json`** —
  Fifteen test citations T01–T15.

The artifacts of the verification run are at
`03_web_app/reports/permanence_audit.json` and
`03_web_app/reports/permanence_audit.md`.

---

## 2. What worked

The constitutional architecture was load-bearing under operational
pressure — to a surprising degree. Several decisions made on paper turned
out to be exactly right when implementing.

### 2.1 Kind-aware URN parsing

The decision in COMMENTARY_PROTOTYPE_2026.md §7.2 to use a dictionary of
kind-keyed regexes rather than a single unified regex was vindicated
again here. A single regex cannot disambiguate
`archive:tale:jataka::1` (kind=tale, text=jataka, id=1) from
`archive:passage:jataka::trans::1` (kind=passage, text=jataka,
trans=trans, id=1) because the `::` separator carries no positional
information. The kind-keyed approach makes parsing explicit and
unambiguous, and it left room to add `text`, `translation`,
`commentary`, `apparatus` kinds cleanly.

### 2.2 Honest failure statuses

The status taxonomy in CITATION_PERMANENCE.md (resolved, alias_redirected,
retired, missing, malformed, ambiguous) plus the lifecycle-derived
statuses (withdrawn, superseded, orphaned, frozen) was sufficient to
cover every test case without resorting to a generic `error` status. Each
failure mode names exactly which constitutional breach occurred. This is
the fail-honestly discipline operationalized.

### 2.3 Aliases as canonical objects

The alias table itself is an append-only canonical object — same schema
discipline as commentary records. This sounded over-engineered at design
time. In practice, having an alias entry carry `event`, `date`, `reason`,
`restoration_id` meant that the verification audit could surface the
*reason* a URN was retired, not just the fact. T08's resolver response
includes the retirement reason verbatim in the diagnostics. A citation
to 1.998 in a 2126 dissertation will still know why.

### 2.4 Sub-locator verbatim discipline

Phrase sub-locators use verbatim case-sensitive string find. No
normalization, no Unicode folding, no whitespace collapsing. This means
the sub-locator behavior is reproducible to the byte. The test citation
T04 asks for `phrase=Truth:nth=1` in passage 1.1; the resolver reports
character offset 31 with occurrence_count 1. A reader in 2126 can verify
this against the canonical passage text byte-equally.

### 2.5 Orphan self-verification

The orphan resolution path makes a recursive resolver call to confirm
that the orphaned record's anchor target genuinely does not resolve. T12
demonstrates this: the resolver returned the orphaned record alongside
`orphan_evidence: {broken_anchor: ..., anchor_resolution_status:
"missing"}`. The resolver verifies its own claims.

### 2.6 Layer-6 quarantine preservation

The AI record (T06) resolved with `quarantined: true` and the full
`model_identity` block (model_id, model_date, prompt_context). This is
the AI_STEWARDSHIP_POLICY.md dual-authorship pattern made operational:
the body's author is the AI, and that fact is preserved permanently in
the resolver response, never silently bleached.

---

## 3. Where the architecture is fragile

These are not failures. The tests pass. These are places where, while
implementing, I noticed the architecture is held up by thinner threads
than the constitutional documents acknowledge.

### 3.1 The `parsed` block reflects the resolved target, not the input

When an alias redirects (T07), the resolver's response is honest at the
top level — `input_urn` retains the original, `aliases_traversed[0]`
retains the alias entry — but the `parsed` block reflects the *target*
URN, because the recursive resolution re-parses the new URN. A casual
reader of the JSON might see `parsed.id: "1.62"` and miss that the
original citation was to `1.999`.

This is not wrong, but it is a transparency cost. A future resolver
should probably carry both `parsed_input` and `parsed_resolved` to make
the redirection fully legible at every level of the response.

### 3.2 The "tale" URN is genuinely virtual

There is no `tale.json` in the archive. A tale URN
(`archive:tale:jataka::1`) names a concept that spans multiple
translations and may map to different chapter ranges per translation.
The current schema records chapter titles per translation but does not
carry the cross-translation `tale_offset` metadata that
COMMENTARY_ATTACHMENT_MODEL.md §3 acknowledged was needed.

The prototype handles this honestly: T02 resolves to a symbolic tale
object with a `note` field explaining that per-translation chapter
mapping is not yet populated, and the renderer is responsible for
finding the chapter in each translation. This is acceptable for the
single-tale prototype but does not generalize. Real cross-translation
tale resolution requires the tale_offset schema work to be done, and the
constitutional documents underestimated how much of the resolver's
intelligence depends on metadata that does not yet exist.

### 3.3 Commentary discovery is a full-tree walk

The resolver loads all `commentary_*.json` and `attachments_*.json` files
under the texts directory at startup. At one tale's scale this is
trivial. At ten thousand tales' scale it is unacceptable. The
permanence promise (resolution in 2126) implicitly requires that, by
2126, there is an *index* — a single file listing every commentary id
and its source path — that the resolver loads instead of walking the
tree.

The constitutional documents did not specify this index. They should.
The honest version of the resolver contract is: "The resolver guarantees
resolution; the implementation may keep an index for performance, and
that index is itself an append-only canonical object."

### 3.4 Schema-version pinning is not exercised

The frozen-record test (T11) confirms that `migration_policy: "frozen"`
is surfaced. But the resolver does not yet refuse to apply a migration
to a frozen record because the resolver does not perform migrations at
all. Schema-version pinning — the part of the promise that says "a
record pinned to schema v1 will still be readable when v17 is current"
— is asserted but not tested. A V2 of this prototype should write a
synthetic record at "schema v1" with a deliberately old field name, run
it through a synthetic migration that changes that field name, and
verify that the frozen record is left untouched while non-frozen
records are migrated.

### 3.5 The alias chain depth is not formally bounded

CITATION_PERMANENCE.md §4.3 prefers single-hop aliases. The resolver
allows chains up to depth 5 and refuses to recurse further (returning
`alias_chain_too_long`). This is a defensive bound, not a constitutional
one. No test exercises it. If a poorly disciplined sequence of
restorations builds a long alias chain, the resolver will follow it
silently up to depth 5 without flagging the chain length anywhere a
human would naturally read. Future versions should emit a diagnostic
whenever the chain exceeds depth 1, regardless of whether it terminates
cleanly.

### 3.6 Body-by-value, not by-reference

Every commentary record returned by the resolver carries its full body
inline. The AI record (T06) is roughly a thousand-character paragraph.
For a single CLI invocation this is fine; for a network-served resolver
returning a thousand commentary records per page, this is wasteful.

The resolver contract should grow a `body_in_other_record` indirection
(already present in some commentary records, ignored by the prototype),
or a `body_summary` projection mode. Neither was needed at this scale.
Both will be needed before this resolver can serve the public reader.

---

## 4. What should not scale

Three things in this prototype are correct for a single-tale,
single-translation, fifteen-citation test surface and would be wrong at
production scale.

### 4.1 Tree-walk discovery

See §3.3. At production scale, an index.

### 4.2 In-memory dictionary of every commentary record

The prototype holds every commentary record in `self._commentary`. At a
hundred thousand records, this is two hundred megabytes of resident
memory just for the index. A real resolver should hold an id-to-path
index and load record bodies lazily.

### 4.3 Synthetic alias entries colocated with real alias entries

The test-fixture alias file lives alongside the real alias file at
`01_library/library/permanence/test_fixtures/aliases.json`. The
`load_test_fixtures` flag controls inclusion. This is fine for the
prototype but the same discipline must not extend to commentary records.
The test commentary fixtures already live in a separate file
(`commentary_test.json`) marked `test_fixture: true` at the wrapper
level. The real commentary records do not commingle. This separation
must remain inviolate.

---

## 5. What the prototype confirms about the constitutional architecture

The architecture is sound, in the specific sense that every
constitutional commitment that could be tested *was* tested, and the
constitutional commitments survived.

- Bare-canon access: confirmed (T03 — passage 1.1 byte-equal).
- Alias redirection: confirmed (T07).
- Retired URN honesty: confirmed (T08).
- Withdrawn-but-preserved bodies: confirmed (T09).
- Supersession chains visible: confirmed (T10).
- Frozen-policy surfacing: confirmed (T11).
- Orphan honesty: confirmed (T12).
- Missing-target honesty: confirmed (T13, T14).
- Malformed-input honesty: confirmed (T15).
- AI quarantine preservation: confirmed (T06).
- Editorial commentary layer separation: confirmed (T05).
- Sub-locator verbatim discipline: confirmed (T04).
- Tale-as-virtual handling: confirmed with caveat (T02 — see §3.2).
- Text-level resolution against the registry: confirmed (T01).

The prototype is also small enough to read in full in one sitting. That
matters. The constitutional documents are several thousand words; the
resolver script is roughly five hundred lines. A future steward who
needs to understand what "permanence" *operationally* means in this
archive can read the resolver in an afternoon and the audit JSON in
five minutes.

---

## 6. What this is not

This is not a production resolver.
This is not a network service.
This is not an HTTP API.
This is not a permalink endpoint.
This is not the public reader.

It is a small, honest demonstration that the constitutional permanence
commitments correspond to operational behavior that can actually be run.

The decision about whether to grow this into a real service belongs to
later stewardship. The constitutional documents and this prototype are
sufficient for that future decision to be informed. They do not force
the decision.

---

## 7. Next reasonable steps (not commitments)

The following are honest next-step candidates. None is required to
consider Phase 15 complete.

- Add schema-version pinning test (§3.4).
- Add commentary index file generator (§3.3) — `build_commentary_index.py`.
- Add `body_in_other_record` indirection support (§3.6).
- Add `parsed_input` vs `parsed_resolved` distinction (§3.1).
- Populate `tale_offset` metadata for at least one multi-translation text
  (§3.2). The Quran (Yusuf Ali vs Pickthall) is the obvious candidate.
- Add a long-alias-chain test (§3.5).
- Expand the test surface to a second tale (e.g., Vessantara, Jātaka
  547) to confirm the patterns hold at the corpus edge as well as the
  corpus opening.

These are listed in the order of probably-cheapest-first. None should be
attempted without an explicit next phase.

---

## 8. Reading order

If a future steward arrives here cold:

1. Read this document.
2. Read `03_web_app/reports/permanence_audit.md`.
3. Read `01_library/library/permanence/test_fixtures/test_citations.json`.
4. Read `05_scripts/resolve_urn.py`.
5. Run `python 05_scripts/verify_permanence.py` and confirm the result
   matches the audit artifact.

If the audit changes, that is itself a finding worth recording. The
audit is a permanent artifact of the May 2026 prototype state; it should
not be silently overwritten. Future runs should be written to dated
files (`permanence_audit_2027-XX-XX.json`) and this 2026 baseline
preserved.
