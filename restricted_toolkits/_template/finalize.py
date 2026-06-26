# -*- coding: utf-8 -*-
"""TEMPLATE finalize.py — write validated output to the gitignored local tree ONLY.
Refuses unless validation passed; never touches public data/. Copy & implement."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_shared'))
import io_paths  # noqa: E402

MANIFEST = json.load(open(os.path.join(HERE, 'manifest.json'), encoding='utf-8'))


def main():
    raise SystemExit('STUB: implement finalize.py for %r (copy of _template).' % MANIFEST['id'])


if __name__ == '__main__':
    main()
