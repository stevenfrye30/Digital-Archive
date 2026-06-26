# Restricted-Text Build Toolkits

This directory distributes **reproducible build toolkits — never the texts themselves.**

The public Digital Archive ships only public-domain / open-license finalized texts.
For texts that cannot be redistributed, this folder ships a *recipe*: code, metadata,
lawful-source instructions, and structural signatures that let a person who has
**lawfully obtained their own source** reconstruct a local copy on their own machine.

## The one rule

> **No copyrighted bytes ever live here.** No text, no excerpts, no fixtures, no
> golden outputs, no cached downloads. Only code, metadata, instructions, and
> one-way structural fingerprints (counts / hashes / lengths).

A toolkit's *output* never re-enters the public tree. It is written only to the
gitignored `data/_restricted/generated/` and read only by the app's **local mode**,
which is hard-blocked on `github.io` and never activates on the public deploy.

## Data flow (one-directional)

```
PUBLIC (committed)            restricted_toolkits/<id>/   (code + metadata + signatures)
                                      |  user runs locally, supplies own lawful source
                                      v
LOCAL (gitignored)            data/_restricted/sources/<id>.*      (user's lawful input)
                              data/_restricted/generated/<id>.local.json   (toolkit output)
                                      v
READER                        local mode only (github.io hard-blocked)
```

## A package (`<id>/`)

| file | role |
|---|---|
| `manifest.json` | id, edition, rights, source options, output path, signatures pointer |
| `README.md` | what it is, why it's not distributed, the exact lawful source to supply, run steps |
| `RIGHTS.md` | rightsholder, status, why restricted, what counts as lawful access |
| `SIGNATURES.json` | structural fingerprints only (counts, ordered-id hash, per-unit length/tokens) |
| `acquire.py` | resolve a source (default: `--input <user file>`); refuses DRM/paywall/scraping |
| `parse.py` | source → archive passage schema `{id,path,order,text}` (+ optional `front_matter`) |
| `validate.py` | compare output to `SIGNATURES.json` — structural only, never prints text |
| `finalize.py` | write to gitignored `data/_restricted/generated/` + local index |

Shared helpers live in `_shared/`. New packages start from `_template/`.

## Proof of concept

`westcott-hort-greek-nt/` is a **public-domain** package used to prove the pipeline and
the guardrails end-to-end with zero legal exposure. It runs the full
acquire → parse → validate → finalize flow on a PD source, writing only to the
gitignored local tree. No restricted-text package exists yet.

## Guards

Two git hooks enforce the boundary:
- **pre-commit** → `tools/scan_no_text.py` — blocks any commit that would introduce
  text/source/output/fixtures or oversized/prose-like files into this tree.
- **pre-push** → `05_scripts/check_restricted_invariants.py` — **fails closed**: blocks a
  push if any restricted text would ship publicly (restricted entry tracked, a shipped
  body mapping to a restricted entry, or `data/_restricted/` not gitignored).

`core.hooksPath` is local git config (not committed), so install the hooks **once per clone**:

```
bash restricted_toolkits/tools/install-hooks.sh
# (equivalently: git config core.hooksPath restricted_toolkits/tools/hooks)
```

See `CONVENTIONS.md` for the full package contract.
