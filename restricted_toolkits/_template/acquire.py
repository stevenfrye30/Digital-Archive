# -*- coding: utf-8 -*-
"""TEMPLATE acquire.py — resolve a lawful source into data/_restricted/sources/.
Copy this package, then implement source normalization for your text."""
import os, sys, json, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_shared'))
import io_paths, rights  # noqa: E402

MANIFEST = json.load(open(os.path.join(HERE, 'manifest.json'), encoding='utf-8'))


def main():
    ap = argparse.ArgumentParser(description='Acquire a lawful source (default: --input).')
    ap.add_argument('--input', help='path to YOUR lawfully obtained source file')
    ap.add_argument('--fetch', action='store_true', help='only valid if an allowed PD source exists')
    args = ap.parse_args()
    rights.refuse_unless_user_file(args.input, MANIFEST)
    print(rights.LAWFUL_SOURCE_NOTICE)
    raise SystemExit('STUB: implement acquire.py for %r (copy of _template).' % MANIFEST['id'])


if __name__ == '__main__':
    main()
