---
name: skillex
description: Manage shared skills with the skillex CLI
---

# Skillex

Use `skillex` to manage versioned skills from a central repository shared across Claude, Codex, and Gemini.

## Locations

- Central repository: `~/.skillex/skills/`
- Provider installs:
  - Claude: `.claude/skills`
  - Codex: `.codex/skills`
  - Gemini: `.gemini/skills`
- Each provider keeps its own `.skillex.lock` file in its skills directory.

## Core Commands

List available skills:

```bash
skillex list
```

Install a skill for a specific agent:

```bash
skillex pull <skill-name> --agent claude
skillex pull <skill-name> --agent codex
skillex pull <skill-name> --agent gemini
```

Update an installed skill:

```bash
skillex update <skill-name> --agent claude
```

Push changes back to the central repository:

```bash
skillex push <skill-name> \
  --agent claude \
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
skillex pull --agent claude
```

2. Edit the installed skill in the matching agent directory, for example:
   - `.claude/skills/<skill-name>/`
   - `.codex/skills/<skill-name>/`
   - `.gemini/skills/<skill-name>/`

3. Push with a structured commit:

```bash
skillex push <skill-name> \
  --agent claude \
  --type docs \
  --summary "describe the change" \
  --changes "what changed" \
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
- Use `--agent` when pulling, pushing, or updating so the CLI knows which local skills directory to use.
- If push is rejected because the repository is behind remote, run `skillex pull` and retry.
- If an installed skill drifts from the recorded hash, skillex will treat it as a local modification.

See `references/commands.md` for a compact command summary.
