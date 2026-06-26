# -*- coding: utf-8 -*-
"""Path resolution for restricted_toolkits.

CONTRACT: toolkit output, sources, and local indexes may ONLY live under the
gitignored `data/_restricted/` tree. Every write path is validated here; any
attempt to resolve a path outside `_restricted/` raises. No toolkit may write
into the public `data/` body files or `index.json`.
"""
import os

# .../03_web_app/restricted_toolkits/_shared/io_paths.py  -> deploy root = parents[2]
DEPLOY_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RESTRICTED_ROOT = os.path.join(DEPLOY_ROOT, 'data', '_restricted')

SOURCES_DIR = os.path.join(RESTRICTED_ROOT, 'sources')
GENERATED_DIR = os.path.join(RESTRICTED_ROOT, 'generated')
LOCAL_INDEX = os.path.join(RESTRICTED_ROOT, 'restricted_index.local.json')


def _under_restricted(path):
    p = os.path.abspath(path)
    root = os.path.abspath(RESTRICTED_ROOT)
    return p == root or p.startswith(root + os.sep)


def assert_local_only(path):
    """Raise unless `path` is inside the gitignored data/_restricted/ tree."""
    if not _under_restricted(path):
        raise PermissionError(
            "REFUSED: %r is outside data/_restricted/. Toolkits may never write "
            "to public data/ or index.json." % path)
    return os.path.abspath(path)


def source_path(text_id, ext='src'):
    return assert_local_only(os.path.join(SOURCES_DIR, '%s.%s' % (text_id, ext)))


def output_path(text_id):
    return assert_local_only(os.path.join(GENERATED_DIR, '%s.local.json' % text_id))


def local_index_path():
    return assert_local_only(LOCAL_INDEX)


def ensure_dirs():
    for d in (SOURCES_DIR, GENERATED_DIR):
        os.makedirs(d, exist_ok=True)
