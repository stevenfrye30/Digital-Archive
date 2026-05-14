# APPARATUS_PROPAGATION_REPAIR_2026

**Date:** 2026-05-14.
**Scope:** A narrow constitutional repair of the apparatus pipeline
between canonical archive and public Reading Room.
**Trigger:** The May 2026 Reading Room constitutional audit identified
that the deployed reader rendered `[*N]` apparatus markers as
clickable affordances but carried no apparatus bodies in deploy. Clicks
failed silently.
**Result:** Apparatus now propagates from canonical to deploy when it
exists. When it does not, the reader fails honestly with a visible
diagnostic instead of silent inaction.

This is a repair, not a redesign. It restores integrity between the
canonical archive and the public reader for a single, localized
concern: textual apparatus. No commentary engine was built. No
framework migrated. No Reading Room rewritten.

---

## 1. Root cause

The full causal chain, in five steps.

1. The Reading Room's renderer treats `[*N]` markers in passage text as
   clickable apparatus references. On click, it consults
   `currentData.apparatus_page_boundaries[]` and `currentData.apparatus[]`
   to resolve the marker to a footnote body. (See
   `03_web_app/index.html`, function `findApparatusForPassage`.)

2. The canonical archive carries structured apparatus in sibling files
   named `apparatus_<translation_id>.json`, with explicit
   `page_boundaries[]` and `apparatus[]` arrays containing per-entry
   `id`, `page`, `index`, `body`, `anchors[]`, and `source` metadata.
   This format is well-shaped, byte-faithful, and constitutionally
   sound — it is precisely the standoff anchor pattern that
   COMMENTARY_ATTACHMENT_MODEL.md prescribes.

3. The export pipeline at `05_scripts/export_reader_data.py` merges
   `text.json` + `passages_<tr_id>.json` into a single deploy file for
   the reader. It does **not** look for or propagate
   `apparatus_<tr_id>.json`. Apparatus is dropped at export.

4. Separately, the ingestion pipeline preserved verbatim `[*N]` markers
   from raw witnesses (mostly SacredTexts.com HTML, where footnote
   anchors arrived as inline bracketed numerals) as plain text in
   passage records. This was correct ingestion: verbatim preservation
   of the source. But ingestion did not auto-extract those marker
   references into structured apparatus.

5. The result, before this repair: 168 deployed texts carried `[*N]`
   markers in passage text. One text (Upaniṣads Part 2, Müller 1879)
   had canonical apparatus that was silently dropped at export.
   The remaining 167 texts had no canonical apparatus to drop — their
   markers were inherited from raw sources but no apparatus
   restoration had ever been performed.

The audit framed this as a single pipeline bug. It is in fact two
distinct constitutional shapes:

- **Propagation breach (1 text):** Apparatus exists canonically;
  export drops it. Honest-by-omission failure.
- **Orphan markers (167 texts):** Apparatus has never existed
  canonically. The markers are unresolvable not because the pipeline
  loses them but because the work of recovering the bodies has not
  yet been done. The reader has no truthful way to resolve them.

Both shapes produced the same surface symptom — clickable apparatus
markers that yielded nothing on click — but the constitutional remedy
is different for each.

---

## 2. The repair

Three changes, all minimal.

### 2.1 Export pipeline propagation

`05_scripts/export_reader_data.py` now looks for
`text_dir / f"apparatus_{tr_id}.json"` alongside each translation's
passages file. When found, it propagates two arrays into the deploy:

- `apparatus_page_boundaries` ← canonical `page_boundaries`
- `apparatus` ← canonical `apparatus`

It also propagates an `apparatus_meta` object carrying
`page_keying`, `page_keying_note`, and `restoration_note`. This object
is consulted by the renderer for the apparatus-entry byline (the
"Müller — page X, footnote N" line is now data-driven, not hard-coded
to one name).

The export remains byte-stable for texts without apparatus: when the
file does not exist, no apparatus keys are written.

The key rename (`page_boundaries` → `apparatus_page_boundaries`) is
deliberate. The deploy is a flat per-text JSON; the prefix
disambiguates from any future, non-apparatus page-keyed metadata. The
canonical files retain their original key name.

### 2.2 Renderer honest-gap rendering

`03_web_app/index.html`, function `toggleApparatusBody`, previously
returned silently when no apparatus body was found. It now invokes a
new helper, `_toggleApparatusGap`, which renders a visible diagnostic
block in the apparatus register (warm tan, with a dashed border to
distinguish from a resolved body).

The diagnostic distinguishes two gap shapes by inspecting whether the
deploy carries any apparatus arrays at all:

- **No apparatus arrays present.** "The marker is preserved verbatim
  from the source text. The corresponding footnote body has not yet
  been extracted into the canonical apparatus for this translation.
  This is a known gap; see APPARATUS_PROPAGATION_REPAIR_2026.md."
- **Apparatus arrays present, but no entry resolves.** "The apparatus
  for this translation is present in this deploy, but no entry was
  recovered at the requested page/index for passage X. The marker is
  preserved verbatim from the source; the corresponding footnote body
  was not recovered during apparatus restoration."

In neither case is the marker hidden. In neither case is content
fabricated.

A small CSS class — `.apparatus-body.gap` — was added: dashed border,
italic system font, slightly muted text color. Visually distinct from
a resolved apparatus body without being alarming.

The byline in resolved apparatus bodies was generalized from the
hard-coded "Müller — page X, footnote N" to a data-driven form:
`<page_keying> — page X, footnote N`. For Müller this resolves to
`muller-print-1884 — page 27, footnote 1`. For future apparatus
restorations of other texts, the page-keying string surfaces the
authorial context automatically.

### 2.3 Validation check

A new read-only check, `05_scripts/validate_apparatus.py`, audits the
apparatus pipeline end-to-end:

- Propagation: for every canonical `apparatus_*.json`, confirm the
  corresponding deploy carries the apparatus arrays.
- Anchor integrity: every anchor and page-boundary entry must
  reference a passage that exists in the passages file.
- Orphan markers: every deploy with `[*N]` markers but no canonical
  apparatus is reported as a long-term restoration backlog item.

The check exits non-zero only on propagation breaches. Orphan markers
are reported but not treated as pipeline failures, because they
represent missing canonical work, not lost canonical work.

The check writes two artifacts:

- `logs/reports/apparatus_audit.md` (human-readable)
- `logs/reports/apparatus_audit.json` (machine-readable)

Both are regenerated each run.

---

## 3. Affected files

### 3.1 Edits

- `05_scripts/export_reader_data.py` — apparatus propagation block.
- `03_web_app/index.html` — `_toggleApparatusGap` helper; `.apparatus-body.gap` CSS; data-driven byline.

### 3.2 New

- `05_scripts/validate_apparatus.py` — apparatus integrity audit.
- `logs/reports/apparatus_audit.{md,json}` — audit output.
- `APPARATUS_PROPAGATION_REPAIR_2026.md` — this document.

### 3.3 Regenerated deploy artifacts

Re-running `export_reader_data.py` followed by `gzip_web_data.py`
rebuilt all 1185 deploy `.json` and `.json.gz` files. The
constitutionally relevant change appears in exactly one of them:

- `03_web_app/data/upanishads-muller-part2_muller-part2.json[.gz]` —
  now carries 42 apparatus entries, 16 page boundaries, and the
  apparatus_meta block. Smoke-tested: passage 5.80's `[*1]` marker
  resolves to the Müller footnote on page 27 ("The change between
  Atharva and Atharvan...").

All other deploy files are unchanged in their constitutional content;
the rebuild merely refreshes their modification timestamps and ensures
their gzipped variants are current.

---

## 4. What assumptions were wrong

Three assumptions in the prior pipeline turned out to be incorrect.

### 4.1 "The export pipeline knows the canonical schema."

It did not. The export merge had been written assuming the only files
under a text directory worth caring about were `text.json` and
`passages_<tr_id>.json`. When apparatus restoration introduced a third
canonical file shape — `apparatus_<tr_id>.json` — no one updated the
export to learn about it. This is the most ordinary kind of pipeline
drift: a new canonical idiom outpacing the consumer that needs to see
it.

The corollary: **every new canonical file shape must be paired, at
the same commit, with the export-side learner that propagates it.**
This is now a discipline, not a procedural option.

### 4.2 "Markers in passage text imply apparatus exists."

The audit's first framing was that 168 texts had apparatus that was
being dropped. In fact only one of those 168 had canonical apparatus
at all. The other 167 had markers preserved verbatim from raw sources
where no archive-side restoration had ever been performed.

This is a more uncomfortable fact than the audit acknowledged. It
means most apparatus content currently *visible* in the public reader,
in the sense of "the reader can see there is meant to be a footnote
here," remains genuinely unrecovered. The brackets are not vestigial;
they are an honest record of what the raw witness contained. But
without the body, they are also a citation pointing at a void.

### 4.3 "Silent failure is honest failure."

It is not. Before this repair, clicking an unresolvable apparatus
marker produced no visual change. The constitutional commitment is to
narrated honesty: name the failure, name the cause, name what would
make it remediable. Silent failure leaves the reader in the
epistemically worst place — unable to tell whether the click was
registered, whether the apparatus did not exist, whether the data
was malformed, or whether the browser ate the event. After this
repair, clicking always yields a visible response, even when (in fact
especially when) the response is "this body is not present in the
archive."

---

## 5. Were prior deployments constitutionally misleading?

Yes, in a precise and small way.

For one text — Upaniṣads Part 2, Müller 1879 — the canonical archive
contained 42 apparatus entries and 16 page boundaries that had been
recovered byte-faithfully from the raw witness during a deliberate
restoration pass. The public reader rendered the passages with the
`[*N]` markers preserved, encouraging the reader to click them.
Clicking produced no result. A scholar reading the deployed Upaniṣads
between the moment the apparatus restoration completed and the moment
of this repair could not have known that the apparatus bodies existed
in the archive at all. The marker said something existed. The
behavior said nothing did. The deploy lied by omission.

For the other 167 texts, the deploy did not lie. The markers were
preserved from raw, and no canonical apparatus had ever been claimed.
The silent click was still epistemically poor — the reader could not
tell whether the apparatus was missing for pipeline reasons or for
restoration reasons — but no canonical fact was being suppressed.
These 167 texts have always been honestly incomplete; they have only
recently come to *say so visibly*.

The 1-text constitutional breach was small but real. It is now
repaired. The 167-text restoration backlog is now visible in the
audit and surfaced honestly to readers.

---

## 6. Lessons for future commentary infrastructure

Five lessons that should travel with any future commentary work.

### 6.1 Every canonical schema addition pairs with an export addition.

If the canonical archive grows a new sibling file under a text
directory (`commentary_*.json`, `attachments_*.json`,
`apparatus_*.json`, future `frozen_*.json`), the export script must
gain a propagation block in the same commit. The pipeline-drift
problem this repair addressed is general; commentary is more
vulnerable to it than apparatus, because commentary has multiple
provenance layers and each is a separate file shape.

### 6.2 Renderer affordances imply data shapes.

Clickable markers imply resolvable targets. Layer toggles imply layer
metadata. Provenance bylines imply provenance fields. The Reading
Room's renderer has historically been written ahead of the data
pipeline that would justify its affordances. This is the silent-failure
posture made worse over time. The discipline: a UI affordance ships at
the same commit as the data shape it consumes, never earlier.

### 6.3 Honest-gap rendering is itself part of the constitution.

The May 2026 audit observed that the Reading Room's failure was
"honest by omission, not honest by design." This repair makes the
failure design-honest for apparatus. The same pattern will be needed
for every future overlay class: commentary, attachment, AI quarantine,
withdrawn-record display, frozen-generation display. None of these can
be allowed to fail silently when their backing data is absent.

The reusable pattern, stated abstractly: every renderer affordance that
expects to resolve a reference must have a fallback path that
**(a)** preserves the marker visibly, **(b)** names the failure mode in
plain language, **(c)** distinguishes "data structure absent" from
"data structure present but entry missing," and **(d)** does not
fabricate content.

### 6.4 The data-driven byline is the right shape.

The original apparatus byline hard-coded "Müller" as the author's
name. This was fine when only one text had apparatus, awkward when a
second is added, and constitutionally wrong once seven provenance
layers each have their own apparatus, scholarship, and editorial
voices. The byline is now derived from `apparatus_meta.page_keying`.
For commentary records, the analogous derivation will draw from
`provenance.{layer, author, date, lifecycle_state}`. The pattern —
metadata flows from canonical to deploy to renderer to byline — is
the same.

### 6.5 The orphan-marker backlog is itself an archival object.

167 deployed texts carry approximately 46,630 inline `[*N]` markers
that have no canonical apparatus. This is a *visible map* of the
restoration work the archive has not yet done. The audit report at
`logs/reports/apparatus_audit.md` is itself the right artifact to
carry that backlog forward: a permanent honest accounting of where
the archive's apparatus restoration is incomplete.

The backlog is not a defect to be fixed at once; it is a working list
spanning years. Some entries (Kojiki's 2,385 markers; Vishnu Purana's
1,574) will likely require dedicated restoration passes comparable in
scope to the Quran or Jātaka work. Others (single-marker entries like
Common Sense) may be a few hours' work each. The audit makes this
landscape navigable.

---

## 7. Constitutional compatibility checks

The user-facing test surface, with results.

| Check | Method | Result |
|---|---|---|
| Bare-canon reading still works | Render `passages[*].text` through `textContent` is unchanged. | OK |
| Apparatus does not mutate passages | Apparatus body lives in `currentData.apparatus[]`; passage records are unchanged. | OK |
| Markers resolve correctly when apparatus exists | Smoke test: Upaniṣads 5.80 `[*1]` resolves to page-27 footnote 1 body. | OK |
| Apparatus provenance remains visible | Byline now renders `page_keying — page X, footnote N`, derived from canonical `apparatus_meta`. | OK |
| Renderer fails honestly when apparatus absent | Click on `[*N]` in any of the 167 orphan-marker texts now opens a visible diagnostic block in the warm-tan register, distinct from a resolved body, naming the gap. | OK |
| Markers preserved verbatim | The `flatText` pipeline still splits on `[\*?\d+]` and renders the bracketed marker text as the anchor's `textContent`. No marker is hidden, deleted, or rewritten. | OK |
| Exported data remains audit-friendly | `validate_apparatus.py` cross-checks canonical apparatus against deploy artifacts; reports propagation breaches, orphan markers, and anchor problems. | OK |

---

## 8. Verification

To rerun this audit and confirm continued integrity:

```
python 05_scripts/export_reader_data.py
python 05_scripts/gzip_web_data.py
python 05_scripts/validate_apparatus.py
```

Expected output at the time of this writing:

```
Apparatus status: 1 ok, 0 propagation breaches, 167 texts with orphan markers, 0 with anchor integrity problems.
```

The numbers may evolve: a new canonical apparatus restoration will
move a text from "orphan markers" to "ok." A regression in the export
pipeline will move it back. Both directions are visible.

---

## 9. What this repair did not do

Per the repair brief:

- No Reading Room rewrite.
- No SPA migration.
- No commentary engine.
- No semantic overlays.
- No inline annotation system.
- No apparatus auto-generation.
- No hidden suppression of unresolved markers.
- No fabricated apparatus bodies.
- No framework expansion.

The renderer's existing CSS register vocabulary, marker-parsing logic,
and click handlers were preserved unchanged except for the one
fail-silently → fail-honestly call site.

---

## 10. Reading order for future stewards

1. This document.
2. `READING_ROOM_CONSTITUTIONAL_AUDIT_2026.md` (parent audit).
3. `01_library/library/texts/sacred/hindu/upanishads-muller-part2/apparatus_muller-part2.json` (the exemplar canonical apparatus).
4. `05_scripts/export_reader_data.py` (the propagation block, search "apparatus_path").
5. `03_web_app/index.html`, function `_toggleApparatusGap` (the honest-gap renderer).
6. `05_scripts/validate_apparatus.py` (the integrity audit).
7. `logs/reports/apparatus_audit.md` (the current state of the world).

That is enough to understand the apparatus pipeline end-to-end, what
this repair fixed, and what work remains in the orphan-marker backlog.
