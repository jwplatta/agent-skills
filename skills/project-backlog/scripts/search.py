#!/usr/bin/env python3
"""Search and filter project backlog items by frontmatter fields."""

import argparse
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def parse_frontmatter(path: Path):
    """Return (frontmatter_dict, body_text) for a markdown file with YAML frontmatter."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, parts[2].strip()


def fuzzy_match(query: str, fm: dict) -> bool:
    """Return True if query string appears (case-insensitive) in title or description."""
    q = query.lower()
    title = str(fm.get("title", "")).lower()
    desc = str(fm.get("description", "")).lower()
    return q in title or q in desc


def format_result(path: Path, fm: dict, body: str, full: bool) -> str:
    priority = fm.get("priority", "?")
    title = fm.get("title") or path.stem
    item_type = fm.get("type", "?")
    status = fm.get("status", "?")
    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]

    header = f"[{priority}] {path.name} — {title} ({item_type}) [{status}]"
    tag_line = f"       tags: {', '.join(tags)}" if tags else ""

    lines = [header]
    if tag_line:
        lines.append(tag_line)
    if full:
        lines.append("")
        lines.append(body)
        lines.append("-" * 60)
    return "\n".join(lines)


def load_items(directory: Path):
    """Yield (path, frontmatter, body) for every .md file except template.md."""
    for p in sorted(directory.glob("*.md")):
        if p.name == "template.md":
            continue
        fm, body = parse_frontmatter(p)
        yield p, fm, body


def main():
    parser = argparse.ArgumentParser(description="Search project backlog items")
    parser.add_argument("--dir", default="docs/backlog", help="Path to backlog directory")
    parser.add_argument("--type", dest="item_type", help="Filter by type: feature|bug|chore|documentation")
    parser.add_argument("--status", help="Filter by status: not-started|in-progress|complete|blocked")
    parser.add_argument("--priority", help="Filter by priority: low|medium|high|critical")
    parser.add_argument("--tag", help="Filter by tag (exact match)")
    parser.add_argument("--query", help="Fuzzy match against title and description")
    parser.add_argument("--full", action="store_true", help="Print full file body in results")
    parser.add_argument("--sort-priority", action="store_true", default=True,
                        help="Sort results by priority (default: on)")
    args = parser.parse_args()

    backlog_dir = Path(args.dir)
    if not backlog_dir.exists():
        print(f"Backlog directory not found: {backlog_dir}", file=sys.stderr)
        sys.exit(1)

    results = []
    for path, fm, body in load_items(backlog_dir):
        if args.item_type and fm.get("type") != args.item_type:
            continue
        if args.status and fm.get("status") != args.status:
            continue
        if args.priority and fm.get("priority") != args.priority:
            continue
        if args.tag:
            tags = fm.get("tags") or []
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",")]
            if args.tag not in tags:
                continue
        if args.query and not fuzzy_match(args.query, fm):
            continue
        results.append((path, fm, body))

    if args.sort_priority:
        results.sort(key=lambda x: PRIORITY_ORDER.get(x[1].get("priority", "medium"), 2))

    if not results:
        print("No matching backlog items.")
        return

    for path, fm, body in results:
        print(format_result(path, fm, body, args.full))
        if not args.full:
            print()


if __name__ == "__main__":
    main()
