#!/usr/bin/env python3
"""Initialize a project backlog folder with a template file."""

import argparse
import shutil
import sys
from pathlib import Path

TEMPLATE = """\
---
type: feature|bug|chore|documentation
tags: []
title:
description:
date:
status: not-started
priority: medium
source:
---

# Summary

<!-- One paragraph describing the request, bug, or task. Be specific about what is expected vs. what exists. -->

## Requirements

<!-- For features/chores: what must be true when this is done.
     For bugs: reproduction steps, expected behavior, actual behavior. -->

## Dependencies & Resources

<!-- Links to related backlog items (by filename), external docs, PRs, or code paths.
     Use tags to group related items into a project or multi-step body of work. -->
"""

GITKEEP = ""


def main():
    parser = argparse.ArgumentParser(description="Initialize a project backlog directory")
    parser.add_argument(
        "--dir",
        default="docs/backlog",
        help="Path to create the backlog directory (default: docs/backlog)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite template.md even if it already exists",
    )
    args = parser.parse_args()

    backlog_dir = Path(args.dir)

    if backlog_dir.exists() and not backlog_dir.is_dir():
        print(f"Error: {backlog_dir} exists and is not a directory.", file=sys.stderr)
        sys.exit(1)

    backlog_dir.mkdir(parents=True, exist_ok=True)
    print(f"Backlog directory ready: {backlog_dir}")

    template_path = backlog_dir / "template.md"
    if template_path.exists() and not args.force:
        print(f"template.md already exists — skipping (use --force to overwrite).")
    else:
        template_path.write_text(TEMPLATE, encoding="utf-8")
        print(f"Created: {template_path}")

    gitkeep = backlog_dir / ".gitkeep"
    if not any(backlog_dir.iterdir()):
        gitkeep.write_text(GITKEEP)

    print()
    print("Next steps:")
    print(f"  1. Commit {backlog_dir}/template.md to your repo.")
    print(f"  2. Copy template.md to create new backlog items.")
    print(f"  3. Search items with: python3 <skill>/scripts/search.py --dir {backlog_dir}")


if __name__ == "__main__":
    main()
