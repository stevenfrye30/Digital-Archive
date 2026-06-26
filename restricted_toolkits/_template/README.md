# &lt;Title&gt; — build toolkit

> **Not distributed.** This package contains no text — only code, metadata, and
> structural signatures. To build a local copy you must supply your own lawfully
> obtained source. It grants no license and bypasses nothing.

## Why this is not distributed
&lt;one line: rightsholder / status / why restricted&gt;

## Lawful source you must supply
&lt;exact edition; what file format; where a lawful owner would have it&gt;

## How to run (local only)
```
python acquire.py  --input <your lawful source file>
python parse.py
python validate.py
python finalize.py
```
Output is written only to the gitignored `data/_restricted/generated/` and read only by
the app's local mode (never on the public deploy).

## Expected result
&lt;unit count and scope, from SIGNATURES.json&gt;

## Troubleshooting
If `validate.py` reports a mismatch, your source is a different edition/printing than the
one this toolkit targets (see `manifest.edition`). Regenerate signatures for your edition
only if you understand the difference — see `RIGHTS.md`.
