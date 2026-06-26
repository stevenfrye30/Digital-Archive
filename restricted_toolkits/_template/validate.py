# -*- coding: utf-8 -*-
"""TEMPLATE validate.py — compare parsed output to SIGNATURES.json (structural only).
Never prints passage text. Copy this package and wire it to your output path."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_shared'))
import io_paths, schema, signatures  # noqa: E402

MANIFEST = json.load(open(os.path.join(HERE, 'manifest.json'), encoding='utf-8'))
SIG = json.load(open(os.path.join(HERE, MANIFEST['signatures_file']), encoding='utf-8'))


def main():
    raise SystemExit('STUB: implement validate.py for %r (copy of _template).' % MANIFEST['id'])


if __name__ == '__main__':
    main()
