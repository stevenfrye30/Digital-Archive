# -*- coding: utf-8 -*-
"""scan_no_text.py — block text / source / output / fixtures from entering the
restricted_toolkits tree. Run on a list of paths (e.g. staged files from the
pre-commit hook) or, with no args, on the whole restricted_toolkits/ tree.

Flags (any -> non-zero exit):
  1. forbidden paths     (fixtures/sources/generated/output, *.txt/.epub/.pdf/.usfm/.local.json)
  2. non-Latin script run (>=15 consecutive Greek/Hebrew/Arabic/CJK letters anywhere)
  3. prose dump          (non-.md file whose word-dense string content exceeds a budget)
  4. oversized file      (.py>50KB, .json>64KB [SIGNATURES.json exempt], .md>40KB)
  5. known restricted data_file names
This is a guard, not a proof: reviewers must still ensure .md files carry no excerpts.
"""
import os, sys, re, json

TOOLKITS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FORBIDDEN_PATH = re.compile(
    r'(^|/)(fixtures|sources|generated|output)(/|$)|'
    r'\.(txt|epub|pdf|usfm|local\.json|restricted\.json)$', re.I)
NONLATIN_RUN = re.compile(r'[Ͱ-Ͽ֐-׿؀-ۿ一-鿿]{15,}')
SIZE_BUDGET = {'.py': 50_000, '.json': 64_000, '.md': 40_000}
RESTRICTED_NAMES = ('dead-sea-scrolls', 'hesse-siddhartha', 'gospel-ramakrishna',
                    'think-grow-rich', 'apocryphon-of-john', 'gospel-of-thomas',
                    'conference-of-the-birds', 'greek-popular-religion', 'huna-theory',
                    'kierkegaard-sickness', 'leibniz-theodicy', 'kitab-i-aqdas')


def word_dense(s):
    if len(s) < 60:
        return False
    letters = sum(ch.isalpha() for ch in s)
    spaces = s.count(' ')
    return letters >= 0.7 * len(s.replace(' ', '')) and spaces >= 12


def prose_chars(text):
    total = 0
    for lit in re.findall(r'"((?:[^"\\]|\\.){40,})"', text):
        if word_dense(lit):
            total += len(lit)
    return total


def scan_file(path):
    rel = os.path.relpath(path, TOOLKITS).replace('\\', '/')
    probs = []
    if FORBIDDEN_PATH.search(rel):
        probs.append('forbidden path/extension (text/source/output/fixture): %s' % rel)
        return probs  # don't even read it
    for n in RESTRICTED_NAMES:
        if n in rel.lower():
            probs.append('restricted data_file name in path: %s' % rel)
    ext = os.path.splitext(path)[1].lower()
    try:
        data = open(path, encoding='utf-8', errors='replace').read()
    except Exception as e:
        return probs + ['unreadable: %s (%s)' % (rel, e)]
    size = len(data.encode('utf-8'))
    base = os.path.basename(path)
    if base != 'SIGNATURES.json' and ext in SIZE_BUDGET and size > SIZE_BUDGET[ext]:
        probs.append('oversized %s: %d bytes > %d' % (rel, size, SIZE_BUDGET[ext]))
    m = NONLATIN_RUN.search(data)
    if m:
        probs.append('non-Latin script run (>=15) in %s (possible pasted text)' % rel)
    if ext != '.md' and prose_chars(data) > 2000:
        probs.append('prose dump in %s (word-dense string content > 2000 chars)' % rel)
    return probs


def iter_paths(args):
    if args:
        for a in args:
            if os.path.isfile(a) and os.path.abspath(a).startswith(TOOLKITS):
                yield os.path.abspath(a)
    else:
        for root, _, files in os.walk(TOOLKITS):
            for f in files:
                yield os.path.join(root, f)


def main(argv):
    all_probs = []
    for p in iter_paths(argv):
        all_probs += scan_file(p)
    if all_probs:
        print('scan_no_text: BLOCKED — %d issue(s):' % len(all_probs))
        for x in all_probs:
            print('  -', x)
        return 1
    print('scan_no_text: OK — no text/source/output/fixtures detected.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
