# -*- coding: utf-8 -*-
"""WH validate.py — compare the generated output to SIGNATURES.json. Structural only:
ids / counts / hashes. NEVER prints passage text. Non-zero exit on mismatch."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_shared'))
import io_paths, schema, signatures  # noqa: E402

MANIFEST = json.load(open(os.path.join(HERE, 'manifest.json'), encoding='utf-8'))
SIG = json.load(open(os.path.join(HERE, MANIFEST['signatures_file']), encoding='utf-8'))
TEXT_ID = MANIFEST['id']


def load_output():
    op = io_paths.output_path(TEXT_ID)
    if not os.path.exists(op):
        raise SystemExit('No output at %s — run parse.py first.' % op)
    return json.load(open(op, encoding='utf-8'))['passages']


def main():
    passages = load_output()
    sp = schema.validate_passages(passages)
    if sp:
        print('SCHEMA problems:', sp[:5]); raise SystemExit(2)
    ok, problems = signatures.compare(passages, SIG)
    if ok:
        print('VALIDATE PASS: %d units, %s..%s, ordered-id + per-unit signatures match.' % (
            len(passages), passages[0]['id'], passages[-1]['id']))
        return
    print('VALIDATE FAIL (structural):')
    for p in problems:
        print('  -', p)
    print('Your source is likely a different edition than %r.' % MANIFEST['edition'])
    raise SystemExit(1)


if __name__ == '__main__':
    main()
