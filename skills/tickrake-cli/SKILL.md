---
name: tickrake-cli
description: Use the installed tickrake CLI for one-off data collection, background job control, log inspection, and basic troubleshooting. Activate when the user wants to run Tickrake rather than modify Tickrake internals.
---

# Tickrake CLI Skill

Use this skill when the task should be completed through the installed `tickrake` command.

## When to use

- The user wants to run Tickrake commands directly
- The user wants to start, inspect, or stop Tickrake background jobs
- The user wants to inspect Tickrake logs
- The user wants help verifying that Tickrake is installed and usable on the machine
- The user wants operational help, not code changes inside Tickrake

## Execution rule

Prefer the globally installed `tickrake` executable from `PATH`.

Do **not** use `bundle exec exe/tickrake` from the repo checkout unless the user explicitly asks to run Tickrake from source for development or debugging.

If `tickrake` is not available in `PATH`:
- stop and tell the user the CLI is not installed globally
- ask whether they want it installed on the machine
- do not silently substitute repo-local execution

## Core commands

Initialize and validate:

```bash
tickrake init
tickrake validate-config
```

Run one-off scrapes:

```bash
tickrake run options --verbose
tickrake run candles --verbose
tickrake run candles --from-config-start --verbose
```

Manage background jobs:

```bash
tickrake start options
tickrake start candles
tickrake status
tickrake stop options
tickrake stop candles
tickrake stop all
```

Inspect logs:

```bash
tickrake logs
tickrake logs --tail 100
```

## Storage model

- Tickrake config: `~/.tickrake/tickrake.yml`
- Tickrake SQLite metadata: `~/.tickrake/tickrake.sqlite3`
- Tickrake logs: `~/.tickrake/tickrake.log`
- Tickrake job state: `~/.tickrake/jobs/*.json`
- Tickrake lockfiles: `~/.tickrake/*.lock`
- Candle payloads: `~/.schwab_rb/data/history`
- Option payloads: `~/.schwab_rb/data/options`

## Operating guidance

- Use `tickrake start ...` / `status` / `stop ...` for long-running jobs.
- Use `--verbose` for one-off runs when the user wants live console output in addition to the file log.
- Use `--from-config-start` for candles only when the user explicitly wants to force a backfill from the configured `start_date`.
- Tickrake depends on a working `schwab_rb` installation and valid Schwab credentials/token.

## Common checks

1. Verify the CLI is installed:

```bash
tickrake --help
```

2. Validate config:

```bash
tickrake validate-config
```

3. Confirm required environment variables exist when auth/data commands fail:
- `SCHWAB_API_KEY`
- `SCHWAB_APP_SECRET`
- `SCHWAB_APP_CALLBACK_URL` when auth/login is needed

4. Check the token if auth errors appear:
- `~/.schwab_rb/token.json`

5. Check recent Tickrake logs:

```bash
tickrake logs --tail 100
```

## References

- For concrete command examples and troubleshooting steps, read [references/cli_examples.md](references/cli_examples.md).
