#!/usr/bin/env python3
"""Install the pre-push guard into .git/hooks/pre-push.

Hooks are not tracked by git, so a fresh clone (or a new machine) must
run this once: python tools/install_hooks.py
"""

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HOOK = REPO / ".git" / "hooks" / "pre-push"

SHIM = """#!/bin/sh
# Installed by tools/install_hooks.py — logic lives in tools/prepush_guard.py
exec python "$(git rev-parse --show-toplevel)/tools/prepush_guard.py"
"""


def main():
    if not HOOK.parent.is_dir():
        raise SystemExit(f"Not a git repo (missing {HOOK.parent}) — run from "
                         "inside 03_web_app.")
    HOOK.write_text(SHIM, encoding="utf-8", newline="\n")
    HOOK.chmod(0o755)
    print(f"Installed {HOOK}")


if __name__ == "__main__":
    main()
