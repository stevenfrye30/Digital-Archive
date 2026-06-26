# -*- coding: utf-8 -*-
"""WH finalize.py — register the validated local body in the gitignored local index.
Refuses unless validation passes. Writes ONLY under data/_restricted/. Never touches
public index.json or data/*.json(.gz)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_shared'))
import io_paths, signatures, schema  # noqa: E402

MANIFEST = json.load(open(os.path.join(HERE, 'manifest.json'), encoding='utf-8'))
SIG = json.load(open(os.path.join(HERE, MANIFEST['signatures_file']), encoding='utf-8'))
TEXT_ID = MANIFEST['id']


def main():
    op = io_paths.output_path(TEXT_ID)
    if not os.path.exists(op):
        raise SystemExit('No output at %s — run parse.py first.' % op)
    passages = json.load(open(op, encoding='utf-8'))['passages']
    if schema.validate_passages(passages):
        raise SystemExit('REFUSED: schema invalid — fix parse.py.')
    ok, problems = signatures.compare(passages, SIG)
    if not ok:
        raise SystemExit('REFUSED: signatures do not match (%d problems) — validate.py must pass first.' % len(problems))

    idx_path = io_paths.local_index_path()
    idx = {'version': 1, 'entries': {}}
    if os.path.exists(idx_path):
        idx = json.load(open(idx_path, encoding='utf-8'))
    idx.setdefault('entries', {})[TEXT_ID] = {
        'id': TEXT_ID,
        'title': MANIFEST['title'],
        'data_file': os.path.basename(op),
        'unit_count': len(passages),
        'rights_status': MANIFEST['rights']['status'],
        'local_only': True,
    }
    json.dump(idx, open(idx_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('FINALIZED (local only): registered %r (%d units) in %s' % (TEXT_ID, len(passages), idx_path))
    print('Body: %s  — both gitignored; never pushed.' % op)


if __name__ == '__main__':
    main()
