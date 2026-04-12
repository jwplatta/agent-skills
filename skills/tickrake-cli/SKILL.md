---
name: tickrake-cli
description: Use the installed tickrake CLI for one-off and background candle/options collection, stored-data queries, log inspection, and operational troubleshooting. Activate when the user wants to run Tickrake rather than modify Tickrake internals.
---

# Tickrake CLI Skill

Use this skill when the task should be completed through the installed `tickrake` command.

## When to use

- The user wants to run Tickrake commands directly
- The user wants to start, inspect, or stop Tickrake background jobs
- The user wants to inspect Tickrake logs
- The user wants to inspect stored data with `tickrake query`
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

Run one-off collection:

```bash
tickrake run options --provider schwab --verbose
tickrake run candles --provider ibkr-paper --verbose
tickrake run candles --provider ibkr-paper --from-config-start --verbose
```

Manage background jobs:

```bash
tickrake start options --provider schwab
tickrake start candles --provider ibkr-paper
tickrake status
tickrake stop options
tickrake stop candles
tickrake stop all
```

Inspect logs:

```bash
tickrake logs cli
tickrake logs options --tail 100
tickrake logs candles --tail 100
```

Query stored data:

```bash
tickrake query --provider ibkr-paper
tickrake query --type candles --provider ibkr-paper --ticker SPY
tickrake query --type candles --provider ibkr-paper --ticker '$SPX' --frequency 30min
tickrake query --type options --provider schwab --ticker '$SPX'
tickrake query --type candles --provider ibkr-paper --ticker SPY --format json
```

Query rules:

- At least one of `--provider` or `--ticker` is required
- `--frequency` only applies to candle queries
- `--format` supports `text` and `json`
- Query output summarizes available data and never prints raw rows
- Provider filtering uses the configured provider namespace, not just the adapter type

## Provider-aware operation

Tickrake uses named providers from `~/.tickrake/tickrake.yml`:

```yaml
default_provider: schwab
providers:
  schwab:
    adapter: schwab
    settings: {}
  ibkr-paper:
    adapter: ibkr
    settings:
      host: 127.0.0.1
      port: 4002
      client_id: 1001
```

Current provider status:

- `schwab` supports candles and options
- `ibkr` currently supports candles only

If the user runs `tickrake run options` with an `ibkr` provider, expect an error and redirect them to a Schwab provider entry instead.

## Storage model

- Tickrake config: `~/.tickrake/tickrake.yml`
- Tickrake SQLite metadata: `~/.tickrake/tickrake.sqlite3`
- Tickrake CLI log: `~/.tickrake/cli.log`
- Tickrake options log: `~/.tickrake/options.log`
- Tickrake candles log: `~/.tickrake/candles.log`
- Tickrake job state: `~/.tickrake/jobs/*.json`
- Tickrake lockfiles: `~/.tickrake/*.lock`
- Candle payloads: `~/.tickrake/data/history/<provider>`
- Option payloads: `~/.tickrake/data/options/<provider>`

Tickrake also caches query summary metadata in the SQLite database. The schema is migrated additively at startup; the CLI does not recreate or overwrite the existing DB.

## Operating guidance

- Use `tickrake start ...` / `status` / `stop ...` for long-running jobs.
- Use `--verbose` for one-off runs when the user wants live console output in addition to the file logs.
- Use `--from-config-start` for candles only when the user explicitly wants to force a backfill from the configured `start_date`.
- For data-availability questions, prefer `tickrake query` instead of reading CSV rows directly.
- Tickrake depends on a working `schwab_rb` installation and valid Schwab credentials/token for Schwab workflows.
- Tickrake depends on a working TWS or IB Gateway session plus `ib-api` for IBKR candle workflows.

## Common checks

1. Verify the CLI is installed:

```bash
tickrake --help
```

2. Validate config:

```bash
tickrake validate-config
```

3. Confirm required environment variables exist when Schwab auth/data commands fail:
- `SCHWAB_API_KEY`
- `SCHWAB_APP_SECRET`
- `SCHWAB_APP_CALLBACK_URL` when auth/login is needed

4. Check the Schwab token if auth errors appear:
- `~/.schwab_rb/token.json`

5. Check recent Tickrake logs:

```bash
tickrake logs cli --tail 100
tickrake logs options --tail 100
tickrake logs candles --tail 100
```

6. Validate that named providers exist and are spelled correctly in config if a command fails with an unknown provider error.

7. For stored-data queries, remember that text output is human-oriented and grouped by provider, type, and ticker, while JSON output is better for agent consumption.
