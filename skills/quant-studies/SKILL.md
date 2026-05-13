---
name: quant-studies
description: Design and iterate on cross-sectional equity backtests using the qstudy Study pipeline. Use when the user wants to build, explore, or improve a long/short or long-only factor study on equities.
---

# quant-studies

## Overview

`qstudy` is a library for doing unconstrainted backtesting. The `Study` class provides a chainable pipeline that handles data alignment, signal generation, filtering, position construction, PnL computation, and metrics.

The preferred workflow is now the first-party `qstudy` CLI. Use the CLI to create and manage experiment folders, then implement study logic inside the generated scaffold. Do not default to ad hoc `common.py` / `run_all.py` structures when the CLI already provides the correct experiment layout.

---

## Workflow: Starting a New Study

When the user invokes this skill to start or iterate on a study, prefer the CLI workflow:

1. Resolve the studies root from `.qstudy.toml` or the current working directory.
2. Create the experiment with `uv run qstudy create <name>` if it does not exist yet.
3. Put reusable loaders and helpers in `shared.py`. New scaffolds already cache `load_universe()` and `load_benchmark()`.
4. Implement the baseline in `v0.py`.
5. Create each next iteration with `uv run qstudy iterate <study-name> <version-name>`.
6. Run the experiment with `uv run qstudy run <study-name>`.
   - To run exactly one iteration, use `uv run qstudy run <study-name> --version <version-stem>`.
7. Review results with `uv run qstudy show-results <name>` or examine the `results.json` directly

### Study Checklist

Ask the following questions before choosing parameters or writing study logic. Ask them all at once.

1. **Universe** — what assets to trade?
   - Common answers: `SP500`, `SECTOR_ETFS`, a custom list of tickers
   - Default if unspecified: `SP500`
2. **Benchmark** — what to compare against?
   - Common answers: `SPY`, `QQQ`, `None`
   - Used for benchmark metrics and (optionally) residualization
   - Default if unspecified: `SPY`
3. **Signal type** — what drives the trade?
   - Mean reversion, momentum, residual mean reversion (factor-stripped), or custom
   - If residual: ask which factors to strip (e.g. `["SPY", "XLK"]`)
4. **Date range** — start and end dates
   - Default if unspecified: `"2015-01-01"` to `"2023-12-31"`
5. **Iterations** — how many versions should the agent attempt to improve?
   - Each iteration should be created with `qstudy iterate`
   - The agent improves signal, filters, or position sizing based on prior results
   - Suggested range: 2–5; more is fine but slower
6. **Experiment name** — what should the CLI create or reuse?
   - This becomes the folder name passed to `qstudy create <name>`
   - Use a short kebab-case name when possible
7. **Studies root** — Always use the `studies_dir` in `.qstudy.toml` if configured otherwise ask the user.

### CLI-first experiment layout

`qstudy create <name>` generates:

```
<studies_root>/<study-name>/
  shared.py
  v0.py
  run.py
  iteration_index.json
  results.json
  results.csv
  log.md
  readme.md
```

Use this layout as the source of truth. Do not replace it with `common.py` or `run_all.py` unless the user explicitly asks for a nonstandard structure.
Treat `qstudy run` as the primary runner for this layout rather than invoking per-experiment runner scripts directly.

### Command sequence

```bash
uv run qstudy create <study-name>
uv run qstudy iterate <study-name> <version-name>
uv run qstudy run <study-name>
uv run qstudy run <study-name> --version <version-stem>
uv run qstudy show-results <study-name>
```

If the studies root is repo-local, run these commands from the directory containing the relevant `.qstudy.toml`.

---

## Study Pipeline Reference

Keep the skill at the workflow level. When implementing actual study logic:

- Put shared download helpers, constants, and reusable functions in `shared.py`.
- Keep each version file focused on one change axis.
- Return `study.metrics_dict()` from `run_study()`.
- Prefer one position construction path per version.
- Prefer one interpretable iteration change at a time.

---

## Iteration Strategy

For each iteration after the baseline, improve along **one axis at a time** so the effect is interpretable. Suggested progression:

| Iteration | Focus |
|-----------|-------|
| v1 | Baseline: raw signal + liquidity filter only |
| v2 | Add conditioning filters (vol, volume z-score, momentum context) |
| v3 | Add residualization (strip market/sector beta) |
| v4 | Add a regime scaler (equity curve, correlation spike, or VIX) |
| v5 | Tune position sizing, rebalance frequency, or weighting scheme |

After each iteration, note changes in Sharpe, ann_return, max_drawdown, and information_ratio. Only carry forward improvements.

---

## CLI Experiment Structure

Use the CLI-generated structure whenever you are running a systematic, multi-version experiment where results should be aggregated and compared in a results table.

### Directory layout

```
<studies_root>/<study-name>/
  shared.py       # shared loaders, constants, and helper functions
  v0.py           # baseline study with run_study() -> dict
  v1_name.py      # first CLI-created iteration
  ...
  vN_name.py      # Nth CLI-created iteration
  run.py          # local wrapper around the shared experiment runner
  iteration_index.json
  log.md          # per-version rationale and outcome notes
  readme.md       # local experiment notes
  results.json    # generated by qstudy run — source of truth for results
  results.csv     # generated by qstudy run — flat table
```

### `shared.py`

`shared.py` should hold everything every version script reuses: data loaders, constants, and helper signal/filter/scaler functions.

### `v0.py`

`v0.py` should define `run_study() -> dict` and return `study.metrics_dict()`.

### Iteration files

Create each new iteration with `uv run qstudy iterate <study-name> <version-name>`. Each copied file should still define `run_study() -> dict`, import shared helpers from `shared.py`, change one axis at a time, and return metrics for aggregation by the shared `qstudy run` execution path.

### `run.py`

`run.py` is generated by the CLI and should usually be left alone. It is only a local wrapper around the same shared runner used by `qstudy run`, not the primary interface the agent should choose.

### `iteration_index.json`

`iteration_index.json` is append-only metadata for CLI-created iterations. It is useful for lineage and tooling, but the shared runner still treats top-level `v*.py` discovery as the execution source of truth.

Primary execution path:

```bash
uv run qstudy run <study-name>
```

Single-version execution:

```bash
uv run qstudy run <study-name> --version <version-stem>
```

Use `python run.py` only when you are already working inside the experiment directory and specifically want the local wrapper script path.

### `log.md`

Record the per-version rationale and outcome in a compact changelog-style format. End with a short summary of what worked, what did not, and the final recommended version.

---

## Key Rules

- **NaN = excluded, 0 = signal.** In filters, use `signal.where(mask)` to NaN-out ineligible assets. Never set signal to 0 — zero is a valid signal value that will be ranked and potentially traded.
- **Use the CLI layout first.** Start with `qstudy create`, edit the generated files, run `qstudy run`, inspect with `qstudy show-results`.
- **Filtered runs overwrite results artifacts.** `qstudy run --version ...` rewrites `results.json` and `results.csv` with only the selected version.
- **One version = one `run_study()` module.** Each `vN.py` should be runnable through the shared `qstudy run` execution path.
- **1-day execution lag** is baked into `engine.run()` via `positions.shift(1)`. Do not shift signals manually.
- **Download once, reuse** — `qs.download()` hits yfinance. Put shared loaders in `shared.py` and reuse across `vN.py` files.
- **residualize_returns() requires** either `factors=` or `benchmark=` in the `Study` constructor.
