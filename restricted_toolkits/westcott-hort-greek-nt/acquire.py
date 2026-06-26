# -*- coding: utf-8 -*-
"""WH acquire.py — normalize the byztxt 'textonly' .WH files into the gitignored
sources tree. Default: --input <dir of .WH files> (your PD copy). --fetch is permitted
ONLY because the byztxt source is public domain ('Copy freely')."""
import os, sys, json, argparse, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_shared'))
import io_paths, rights  # noqa: E402

MANIFEST = json.load(open(os.path.join(HERE, 'manifest.json'), encoding='utf-8'))
TEXT_ID = MANIFEST['id']
DST = os.path.join(io_paths.SOURCES_DIR, TEXT_ID)
BOOK_FILES = ['MT', 'MR', 'LU', 'JOH', 'AC', 'RO', '1CO', '2CO', 'GA', 'EPH', 'PHP', 'COL',
              '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE', '2PE', '1JO',
              '2JO', '3JO', 'JUDE', 'RE']


def from_input(input_dir):
    io_paths.ensure_dirs()
    io_paths.assert_local_only(DST)
    os.makedirs(DST, exist_ok=True)
    n = 0
    for bc in BOOK_FILES:
        src = os.path.join(input_dir, '%s.WH' % bc)
        if not os.path.exists(src):
            raise SystemExit('MISSING %s.WH in %r — need all 27 byztxt textonly files.' % (bc, input_dir))
        shutil.copyfile(src, os.path.join(DST, '%s.WH' % bc))
        n += 1
    print('normalized %d/27 .WH files -> %s' % (n, DST))


def fetch():
    opt = rights.network_fetch_allowed(MANIFEST)
    if not opt:
        raise SystemExit('REFUSED: no allowed public-domain fetch configured.')
    print(rights.LAWFUL_SOURCE_NOTICE)
    print('Allowed PD source: %s (%s)' % (opt['url'], opt['reason']))
    print('To fetch manually (public domain): git clone --depth 1 %s, then run with '
          '--input <clone>/textonly' % opt['url'])
    raise SystemExit('Conservative mode: automatic network clone is not performed. '
                     'Clone the PD repo yourself and pass --input.')


def main():
    ap = argparse.ArgumentParser(description='Acquire byztxt textonly .WH files (PD).')
    ap.add_argument('--input', help='directory of byztxt textonly .WH files (your PD copy)')
    ap.add_argument('--fetch', action='store_true', help='show the allowed PD fetch instructions')
    args = ap.parse_args()
    rights.refuse_unless_user_file(args.input, MANIFEST)
    if args.input:
        from_input(args.input)
    elif args.fetch:
        fetch()


if __name__ == '__main__':
    main()
