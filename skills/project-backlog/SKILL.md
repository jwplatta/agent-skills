---
name: project-backlog
description: Create, search, and manage project backlog items across any project
---

# Project Backlog Skill

Manage a file-based project backlog using markdown files with YAML frontmatter. Each backlog item is a single `.md` file in the project's `backlog/` folder.

## When to Activate

- User asks to add, log, or record a bug, feature request, chore, or documentation task
- User asks to search, find, or list backlog items
- User asks what work is pending, in-progress, blocked, or highest priority
- User asks about work grouped by tag or type

## Backlog Item Format

Each backlog item is a markdown file in `docs/backlog/`. Use `docs/backlog/template.md` as the starting point. Name the file descriptively using snake_case, e.g. `add_s3_upload_command.md` or `fix_tracker_nil_crash.md`.

**Frontmatter fields:**

```yaml
---
type: feature        # feature | bug | chore | documentation
tags: [s3, upload]   # free-form; use tags to group related items into a project
title: Add S3 upload command
description: One-line summary shown in search results
date: 2026-09-21     # ISO date the item was created
status: not-started  # not-started | in-progress | complete | blocked
priority: high       # low | medium | high | critical
source: claude/tickrake  # agent-name/project-name that wrote the item
---
```

**Tags as project grouping:** When a body of work spans multiple backlog items, give them all a shared tag (e.g. `s3-archive`). Searching by that tag gives a project-level view.

## Creating a Backlog Item

1. Copy `docs/backlog/template.md` to a new descriptively named file in `docs/backlog/`.
2. Fill in all frontmatter fields. Use today's date. Set `source` to `claude/<project>` (or the agent writing it).
3. Write a clear Summary, Requirements, and Dependencies & Resources section.
4. Do not leave the file as a stub — complete the content before saving.

## Searching the Backlog

Use the scripts in this skill to query backlog items. All scripts accept a `--dir` flag defaulting to `docs/backlog`.

### List by priority

```bash
python3 .codex/skills/project-backlog/scripts/search.py --priority high
python3 .codex/skills/project-backlog/scripts/search.py --priority critical --status not-started
```

### List by type

```bash
python3 .codex/skills/project-backlog/scripts/search.py --type bug
python3 .codex/skills/project-backlog/scripts/search.py --type feature --status in-progress
```

### List by tag (project view)

```bash
python3 .codex/skills/project-backlog/scripts/search.py --tag s3-archive
```

### List by status

```bash
python3 .codex/skills/project-backlog/scripts/search.py --status blocked
python3 .codex/skills/project-backlog/scripts/search.py --status not-started
```

### Fuzzy search on title or description

```bash
python3 .codex/skills/project-backlog/scripts/search.py --query "upload artifact"
```

### Combined filters

```bash
python3 .codex/skills/project-backlog/scripts/search.py --type bug --status not-started --priority high
```

### Full output (show body, not just frontmatter summary)

```bash
python3 .codex/skills/project-backlog/scripts/search.py --tag s3-archive --full
```

## Output Format

By default, each result is printed as:

```
[high] fix_tracker_nil_crash.md — Fix nil crash in tracker on first run (bug) [not-started]
       tags: tracker, crash
```

With `--full`, the entire markdown file is printed after the header line.

## Updating a Backlog Item

Edit the file directly. When status changes (e.g. work starts, completes, or gets blocked), update the `status` field in the frontmatter.

## Notes

- The backlog folder is committed to the repo — backlog items are persistent shared state, not ephemeral notes.
- Do not create vague or placeholder items. Every item should have enough detail that someone else could act on it.
- `docs/FEATURE_REQUESTS.md` (if present) is the old format — migrate items to `docs/backlog/` on sight.
