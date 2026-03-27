# Skillex Commands

## Basic

```bash
skillex list
skillex pull --agent claude
skillex pull <skill-name> --agent claude
skillex update <skill-name> --agent claude
skillex delete <skill-name>
```

## Push

```bash
skillex push <skill-name> \
  --agent claude|codex|gemini \
  --type feat|fix|refactor|docs|test|chore \
  --summary "brief summary" \
  --changes "what changed" \
  --reason "why it changed" \
  --bump patch|minor|major
```

## Provider Setup

```bash
skillex init claude
skillex init codex
skillex init gemini
```

## Config

```bash
skillex config show
skillex config get-remote
skillex config set-remote <repo-url>
```
