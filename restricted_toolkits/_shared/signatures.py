# -*- coding: utf-8 -*-
"""Structural signatures — fingerprints of a text, never the text itself.

A signature captures counts, ordered-id hashes, and per-unit (length, token-count)
or optional per-unit SHA-256. These are one-way and non-reconstructive: you cannot
rebuild any text from them, so they are safe to commit even for in-copyright works.
This module never stores or prints passage text.
"""
import hashlib
from collections import OrderedDict


def _sha(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def compute(passages, edition, mode='length+tokens', generator=''):
    ids = [p['id'] for p in passages]
    bc = OrderedDict()
    for p in passages:
        b = p['path'][0]
        bc[b] = bc.get(b, 0) + 1
    per_unit = {}
    strict = None
    for p in passages:
        t = p['text']
        per_unit[p['id']] = [len(t), len(t.split())]
    if mode == 'strict':
        strict = {p['id']: _sha(p['text']) for p in passages}
    return {
        'edition': edition,
        'unit_count': len(passages),
        'first_id': ids[0] if ids else None,
        'last_id': ids[-1] if ids else None,
        'book_unit_counts': dict(bc),
        'ordered_ids_sha256': _sha('\n'.join(ids)),
        'per_unit': {'mode': 'length+tokens', 'items': per_unit},
        'strict_hashes_sha256': strict,
        'generator': generator,
        'notes': 'length = character count; tokens = whitespace-delimited count',
    }


def compare(passages, sig):
    """Compare freshly-parsed passages to a stored signature. Returns (ok, problems).
    Diagnostics are structural only — ids/counts/hashes, never text."""
    fresh = compute(passages, sig.get('edition', ''),
                     mode='strict' if sig.get('strict_hashes_sha256') else 'length+tokens')
    problems = []
    for key in ('unit_count', 'first_id', 'last_id', 'ordered_ids_sha256'):
        if fresh[key] != sig.get(key):
            problems.append('%s mismatch: got %r expected %r' % (key, fresh[key], sig.get(key)))
    if fresh['book_unit_counts'] != sig.get('book_unit_counts'):
        gb, eb = fresh['book_unit_counts'], sig.get('book_unit_counts', {})
        diff = {k: (gb.get(k), eb.get(k)) for k in set(gb) | set(eb) if gb.get(k) != eb.get(k)}
        problems.append('book_unit_counts mismatch: %r' % diff)
    exp_items = sig.get('per_unit', {}).get('items', {})
    got_items = fresh['per_unit']['items']
    mism = [k for k in exp_items if got_items.get(k) != exp_items[k]]
    if mism:
        problems.append('per_unit length+tokens mismatch at %d ids (e.g. %s)' % (len(mism), mism[:5]))
    if sig.get('strict_hashes_sha256') is not None:
        sh = {p['id']: _sha(p['text']) for p in passages}
        bad = [k for k, v in sig['strict_hashes_sha256'].items() if sh.get(k) != v]
        if bad:
            problems.append('strict per-unit hash mismatch at %d ids (e.g. %s)' % (len(bad), bad[:5]))
    return (not problems), problems
