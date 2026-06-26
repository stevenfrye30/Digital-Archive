# -*- coding: utf-8 -*-
"""Archive passage-schema validation for restricted_toolkits.

A parsed text is a list of passages: {id:str, path:list, order:int, text:str}.
Optional top-level `front_matter`: list of {kind, label, body} (appendix material).
These helpers check STRUCTURE only and never print passage text.
"""
import re

TAG_RE = re.compile(r'\\[a-zA-Z]+\*?|<[a-zA-Z/][^>]*>')


def validate_passages(passages):
    """Return a list of structural problems (empty list == clean). No text printed."""
    problems = []
    if not isinstance(passages, list) or not passages:
        return ['passages must be a non-empty list']
    seen = set()
    for i, p in enumerate(passages):
        for k in ('id', 'path', 'order', 'text'):
            if k not in p:
                problems.append('passage #%d missing key %r' % (i, k))
        pid = p.get('id')
        if pid in seen:
            problems.append('duplicate id %r' % pid)
        seen.add(pid)
        if not str(p.get('text', '')).strip():
            problems.append('empty text at %r' % pid)
        if '�' in p.get('text', ''):
            problems.append('U+FFFD at %r' % pid)
        if TAG_RE.search(p.get('text', '')):
            problems.append('residual markup/tag at %r' % pid)
    orders = [p.get('order') for p in passages]
    if orders != list(range(len(passages))):
        problems.append('order field is not a 0..N-1 sequence')
    return problems
