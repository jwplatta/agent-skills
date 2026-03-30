---
name: skillex
description: Manage shared skills with the skillex CLI
---

# Skillex

Use `skillex` to manage versioned skills from a shared repository.

## First Steps

1. Configure the shared skills repo:

```bash
skillex config set-remote <repo-url>
```

2. Pull or push skills with an explicit agent:

```bash
skillex pull <skill-name> --agent claude
skillex remove <skill-name>
skillex push <skill-name> --agent codex --type docs --summary "describe the change"
```

## Notes

- The shared source of truth lives in `~/.skillex`.
- Installed copies live in agent-specific skills directories.
- Use `skillex list` to inspect the shared repository contents.

See `references/commands.md` for a compact command summary.
