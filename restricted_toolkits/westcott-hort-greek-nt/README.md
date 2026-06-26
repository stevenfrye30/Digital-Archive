# Westcott-Hort Greek NT — build toolkit (public-domain proof of concept)

This package proves the restricted-toolkit pipeline on a **public-domain** text. It runs
the full **acquire → parse → validate → finalize** flow, writing output only to the
gitignored `data/_restricted/generated/` tree — exactly the path a real restricted text
would use, but with zero legal exposure.

## Source you supply
A directory of byztxt **`textonly`** per-book files (unaccented beta-code), named
`MT.WH, MR.WH, LU.WH, JOH.WH, … RE.WH` (27 files). These are public domain
("Copy freely"); the default path expects *your* copy.

## Run (local only)
```
python acquire.py  --input /path/to/textonly        # normalizes 27 .WH files into _restricted/sources/
python parse.py                                      # beta-code -> unaccented Unicode, archive schema
python validate.py                                   # compares output to SIGNATURES.json (structural only)
python finalize.py                                   # writes _restricted/generated/westcott-hort-greek-nt.local.json
```
`acquire.py --fetch` is permitted here only because the source is public domain.

## Expected result
**7,941 verses**, `mat.1.1` … `rev.22.21`, 27 NT books, unaccented Greek; matches
`SIGNATURES.json` exactly (the beta-code transform is deterministic).

## Notes
- `parse.py` contains the documented beta-code→Unicode map (code, not text).
- Output never re-enters the public tree; it is read only by the app's local mode, which
  is hard-blocked on `github.io`.
- This is a stand-in. **No in-copyright/restricted package exists in this repo.**
