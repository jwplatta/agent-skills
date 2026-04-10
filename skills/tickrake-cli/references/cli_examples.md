# Tickrake CLI Examples

## Initialization

```bash
tickrake init
tickrake validate-config
```

## One-off runs

```bash
tickrake run options --verbose
tickrake run candles --verbose
tickrake run candles --from-config-start --verbose
```

## Background jobs

```bash
tickrake start options
tickrake start candles
tickrake status
tickrake stop options
tickrake stop candles
tickrake stop all
```

## Logs

```bash
tickrake logs
tickrake logs --tail 100
```

## Troubleshooting

If `tickrake` is missing from `PATH`, do not fall back to `bundle exec exe/tickrake`.
Ask the user whether they want to install Tickrake globally on the machine.

If data collection fails:

1. Check `tickrake logs --tail 100`
2. Check `~/.tickrake/tickrake.yml`
3. Check `~/.schwab_rb/token.json`
4. Check exported `SCHWAB_*` environment variables
