# -*- coding: utf-8 -*-
"""TEMPLATE parse.py — source -> archive passage schema. Deterministic, no network,
no embedded text. Copy this package and implement the transform for your text."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_shared'))
import io_paths, schema  # noqa: E402

MANIFEST = json.load(open(os.path.join(HERE, 'manifest.json'), encoding='utf-8'))


def main():
    raise SystemExit('STUB: implement parse.py for %r (copy of _template).' % MANIFEST['id'])


if __name__ == '__main__':
    main()
