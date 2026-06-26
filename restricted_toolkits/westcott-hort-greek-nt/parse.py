# -*- coding: utf-8 -*-
"""WH parse.py — byztxt 'textonly' beta-code -> unaccented Unicode Greek, archive schema.

Deterministic, no network, no embedded text. Reads the normalized source from
data/_restricted/sources/westcott-hort-greek-nt/ (placed there by acquire.py) and writes
the passage body to data/_restricted/generated/westcott-hort-greek-nt.local.json (gitignored).
The map below is CODE (a character table), not copyrighted text.
"""
import os, sys, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_shared'))
import io_paths, schema  # noqa: E402

TEXT_ID = 'westcott-hort-greek-nt'
SRC_DIR = os.path.join(io_paths.SOURCES_DIR, TEXT_ID)

# byztxt filename -> archive book code (canonical NT order)
BOOKS = [('MT', 'mat'), ('MR', 'mrk'), ('LU', 'luk'), ('JOH', 'jhn'), ('AC', 'act'),
         ('RO', 'rom'), ('1CO', '1co'), ('2CO', '2co'), ('GA', 'gal'), ('EPH', 'eph'),
         ('PHP', 'php'), ('COL', 'col'), ('1TH', '1th'), ('2TH', '2th'), ('1TI', '1ti'),
         ('2TI', '2ti'), ('TIT', 'tit'), ('PHM', 'phm'), ('HEB', 'heb'), ('JAS', 'jas'),
         ('1PE', '1pe'), ('2PE', '2pe'), ('1JO', '1jn'), ('2JO', '2jn'), ('3JO', '3jn'),
         ('JUDE', 'jud'), ('RE', 'rev')]

# Online-Bible/byztxt beta-code -> UNACCENTED Unicode Greek (medial sigma s, final sigma v)
BETA = {'a': 'α', 'b': 'β', 'c': 'χ', 'd': 'δ', 'e': 'ε', 'f': 'φ', 'g': 'γ', 'h': 'η',
        'i': 'ι', 'k': 'κ', 'l': 'λ', 'm': 'μ', 'n': 'ν', 'o': 'ο', 'p': 'π', 'q': 'ψ',
        'r': 'ρ', 's': 'σ', 't': 'τ', 'u': 'υ', 'v': 'ς', 'w': 'ω', 'x': 'ξ', 'y': 'θ',
        'z': 'ζ'}
VERSE_RE = re.compile(r'^\s*(\d+):(\d+)\s*(.*)$')


def translit(s):
    return ''.join(BETA.get(ch, ch) for ch in s)


def parse_book(path):
    out = []
    for line in open(path, encoding='utf-8', errors='strict').read().splitlines():
        m = VERSE_RE.match(line)
        if m:
            out.append([int(m.group(1)), int(m.group(2)), m.group(3).rstrip()])
        elif out:
            out[-1][2] = (out[-1][2] + ' ' + line.strip()).strip()
    return out


def build():
    passages, order, skipped = [], 0, []
    for bc, code in BOOKS:
        path = os.path.join(SRC_DIR, '%s.WH' % bc)
        if not os.path.exists(path):
            raise SystemExit('MISSING source file: %s.WH (run acquire.py --input <textonly dir>)' % bc)
        for c, v, raw in parse_book(path):
            if not raw.strip():
                skipped.append('%s.%d.%d' % (code, c, v))  # WH-omitted verse
                continue
            passages.append({'id': '%s.%d.%d' % (code, c, v), 'path': [code, c, v],
                             'order': order, 'text': translit(raw.strip())})
            order += 1
    return passages, skipped


def main():
    passages, skipped = build()
    problems = schema.validate_passages(passages)
    if problems:
        raise SystemExit('PARSE schema problems: %s' % problems[:5])
    io_paths.ensure_dirs()
    out = {'version': 1, 'text_id': 'bible', 'translation_id': TEXT_ID, 'passages': passages}
    op = io_paths.output_path(TEXT_ID)
    json.dump(out, open(op, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('parsed %d verses (%d WH-omitted skipped) -> %s' % (len(passages), len(skipped), op))


if __name__ == '__main__':
    main()
