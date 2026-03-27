# Skillex Commands

## Basic

```bash
skillex list
skillex pull
skillex pull <skill-name>
skillex update <skill-name>
skillex delete <skill-name>
```

## Push

```bash
skillex push <skill-name> \
  --type feat|fix|refactor|docs|test|chore \
  --summary "brief summary" \
  --changes "specific change" \
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
