#!/usr/bin/env bash
# Install the restricted_toolkits git hooks for THIS (deploy) repo.
# Run once per clone, from the deploy repo root (03_web_app):
#
#     bash restricted_toolkits/tools/install-hooks.sh
#
# Or run the one line it wraps:
#
#     git config core.hooksPath restricted_toolkits/tools/hooks
#
# core.hooksPath is LOCAL git config (not committed), so every fresh clone must
# run this once. It activates:
#   pre-commit -> scan_no_text.py        (block text/source/output/fixtures in toolkits)
#   pre-push   -> check_restricted_invariants.py  (block a restricted leak before push)
set -e
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "Not in a git repo."; exit 1; }
git config core.hooksPath restricted_toolkits/tools/hooks
chmod +x restricted_toolkits/tools/hooks/pre-commit restricted_toolkits/tools/hooks/pre-push 2>/dev/null || true
echo "Installed: core.hooksPath = $(git config core.hooksPath)"
echo "  pre-commit -> scan_no_text.py"
echo "  pre-push   -> check_restricted_invariants.py (fails closed)"
