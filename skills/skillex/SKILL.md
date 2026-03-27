---
name: skillex
description: Manage shared skills with the skillex CLI
---

# Skillex

Use `skillex` to manage versioned skills for Codex from a central repository.

## Locations

- Central repository: `~/.skillex/skills/`
- Codex skills: `/Users/jplatta/repos/skillex/.codex/skills`
- Lockfile: `/Users/jplatta/repos/skillex/.codex/skills/.skillex.lock`

## Core Commands

List available skills:

```bash
skillex list
```

Install a skill into Codex:

```bash
skillex pull <skill-name>
```

Update an installed skill:

```bash
skillex update <skill-name>
```

Push changes back to the central repository:

```bash
skillex push <skill-name> \
  --type feat \
  --summary "brief description of the change"
```

Initialize another provider:

```bash
skillex init claude
skillex init codex
skillex init gemini
```

## Recommended Workflow

1. Pull before editing:

```bash
skillex pull
```

2. Edit the installed skill in `/Users/jplatta/repos/skillex/.codex/skills/<skill-name>/`.

3. Push with a structured commit:

```bash
skillex push <skill-name> \
  --type docs \
  --summary "describe the change" \
  --changes "specific thing that changed" \
  --reason "why the change was needed"
```

## Commit Types

- `feat`: new capability
- `fix`: bug fix
- `refactor`: no behavior change
- `docs`: documentation or metadata only
- `test`: test changes
- `chore`: maintenance work

## Version Bumps

- `--bump patch`: bugfix or small update
- `--bump minor`: new capability
- `--bump major`: breaking change

## Notes

- Skillex syncs the full `~/.skillex` repository, not individual skills.
- If push is rejected because the repository is behind remote, run `skillex pull` and retry.
- If a provider install drifts from the recorded hash, skillex will treat it as a local modification.

See `references/commands.md` for a compact command summary.
