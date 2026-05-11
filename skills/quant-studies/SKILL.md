---
name: quant-studies
description: Design and iterate on cross-sectional equity backtests using the qstudy Study pipeline. Use when the user wants to build, explore, or improve a long/short or long-only factor study on equities.
---

# quant-studies

## Overview

`qstudy` is a library for doing unconstrainted backtesting. The `Study` class provides a chainable pipeline that handles data alignment, signal generation, filtering, position construction, PnL computation, and metrics — the researcher writes only the signal logic and any custom filters.

```python
import qstudy as qs
from qstudy import Study
from qstudy.constants import SP500
```

---

## Workflow: Starting a New Study

When the user invokes this skill, **ask the following questions before writing any code**. Do not guess — wait for answers.

### Required questions (ask all at once)

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
   - Each iteration writes a new script and prints metrics
   - The agent improves signal, filters, or position sizing based on prior results
   - Suggested range: 2–5; more is fine but slower

6. **Output mode** — single exploratory study or multi-version experiment?
   - **Single study**: one-off script, output to `~/.qstudy/<study-name>/`
   - **Experiment**: `common.py` + numbered `v0.py`–`vN.py` + `run_all.py` + `LOG.md` under `experiments/<study-name>/`
   - Default if unspecified: ask the user — do not guess
   - Use the experiment structure whenever the goal is systematic iteration with a CSV results table

### Output location

**Single study** — each iteration is a new file under `~/.qstudy/<study-name>/`:

```
~/.qstudy/
  residual_mr_sp500/
    v1_baseline.py
    v2_vol_filter.py
    v3_corr_regime.py
    ...
```

Create the folder before writing the first script:
```python
import os
os.makedirs(os.path.expanduser("~/.qstudy/<study-name>"), exist_ok=True)
```

**Experiment** — use the structure described in [Experiment Structure](#experiment-structure) below. Files live under `experiments/<study-name>/` in the repo.

---

## Study Pipeline Reference

### Basic shape

```python
study = (
    Study(universe=universe_data, benchmark=benchmark_data, factors=factors_data)
    # [optional] strip factor exposure before signal
    .residualize_returns()
    # signal source — exactly one
    .mean_reversion(window=20)     # or .momentum(window=60) or .base_signal(fn)
    # filters — zero or more, applied in order
    .add_liquidity_filter(top_n=250)
    .add_vol_filter(vol_window=40, quantile=0.75, keep="low")
    .add_volume_zscore_filter(window=30, min_zscore_quantile=0.8)
    .add_momentum_context_filter(window=60, max_abs_quantile=0.7)
    # position builder — exactly one
    .build_long_short(n_long=25, n_short=25)   # or .build_long_only(n=50)
    # position scalers — zero or more
    .scale_returns(my_regime_scaler)
    # optional weighting (default = equal dollar)
    .weight_equal_vol(vol_window=60)
    .run()
)

study.report()   # prints metrics + 3-panel chart
```

### Data loading

```python
# Returns a StudyData object with fields: tickers, close, volume, returns, log_returns
universe_data  = qs.download(SP500,           "2015-01-01", "2023-12-31")
benchmark_data = qs.download(["SPY"],         "2015-01-01", "2023-12-31")
factors_data   = qs.download(["SPY", "XLK"], "2015-01-01", "2023-12-31")
```

Download **once** at the top of each script, then reuse across iterations in the same session.

### Built-in signal methods

| Method | Signal formula |
|--------|---------------|
| `.mean_reversion(window=20)` | `-residuals.rolling(window).mean()` — recent losers rank highest |
| `.momentum(window=60)` | `residuals.rolling(window).mean()` — recent winners rank highest |
| `.base_signal(fn)` | `fn(**cache) -> pd.DataFrame` — fully custom |

When `.residualize_returns()` is called, `_active_returns` is set to `residual_returns`; otherwise it's `returns`. Built-in methods use `_active_returns` automatically.

### Built-in filters

| Method | What it does |
|--------|-------------|
| `.add_liquidity_filter(top_n=250)` | Keep only top N by rolling dollar volume; also masks returns in the engine |
| `.add_vol_filter(vol_window=40, quantile=0.75, keep="low")` | Remove high-vol assets cross-sectionally |
| `.add_volume_zscore_filter(window=30, min_zscore_quantile=0.8)` | Remove assets with below-average recent volume |
| `.add_momentum_context_filter(window=60, max_abs_quantile=0.7)` | Remove strongly trending assets (for mean reversion) |

When `residualize_returns()` was called, `add_vol_filter` and `add_momentum_context_filter` automatically use `residual_returns` instead of raw returns.

### Custom signal filter

```python
def my_filter(signal, **cache):
    # cache keys: returns, close, volume, residual_returns, _active_returns, benchmark, ...
    returns = cache["returns"]
    mask = ...   # bool DataFrame, same shape as signal
    return signal.where(mask)   # NaN to exclude, never 0

study.add_filter(my_filter)
```

### Custom position scaler

```python
def my_scaler(positions, **cache):
    returns = cache["returns"]
    liq_mask = cache.get("_liquidity_mask")
    if liq_mask is not None:
        returns = returns.where(liq_mask)
    # compute scale: pd.Series indexed by date
    scale = ...
    return positions.mul(scale.shift(1), axis=0)

study.scale_returns(my_scaler)
```

### Weighting schemes

```python
study.weight_equal()                        # default, no-op
study.weight_equal_vol(vol_window=60)       # inverse realized vol
study.weight_equal_sharpe(window=126)       # proportional to rolling Sharpe
study.weight_optimal(window=126, gamma=1.0) # mean-variance (slow for large universes)
```

### Save and reload

```python
study.save("~/.qstudy/my_study/v1.pkl")
study2 = Study.from_cache("~/.qstudy/my_study/v1.pkl")
study2.report()
```

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

## Experiment Structure

Use this structure whenever you are running a systematic, multi-version experiment where results should be aggregated and compared in a CSV table.

### Directory layout

```
experiments/<study-name>/
  common.py       # shared loaders, signal builders, scalers, build_study()
  v0.py           # baseline — all logic inline, no imports from common
  v1.py           # first iteration — delegates to build_study() with one change
  ...
  vN.py           # Nth iteration
  run_all.py      # loads every version, aggregates metrics → results.csv
  LOG.md          # per-version rationale and outcome notes
  results.csv     # generated by run_all.py — do not hand-edit
```

### `common.py` template

`common.py` holds everything that every version script reuses: data loaders, reusable signal/filter/scaler functions, the `build_study()` factory, and `emit_metrics()`.

```python
import json
from functools import cache

import numpy as np
import pandas as pd

import qstudy as qs
from qstudy import Study
from qstudy.constants import SP500

START_DATE = "2015-01-01"
END_DATE   = "2023-12-31"


# ── Data loaders (cached so each version reuses the same objects) ────────────

@cache
def load_universe():
    return qs.download(SP500, START_DATE, END_DATE)

@cache
def load_benchmark():
    return qs.download("SPY", START_DATE, END_DATE)

@cache
def load_baseline_factors():
    return qs.download(["SPY", "XLK"], START_DATE, END_DATE)


# ── Reusable signal / scaler / filter functions ──────────────────────────────

def demean_signal(signal, **cache):
    return signal.sub(signal.mean(axis=1), axis=0)

def proportional_positions(signal, **cache):
    signal_z = signal.sub(signal.mean(axis=1), axis=0)
    signal_z = signal_z.div(signal_z.std(axis=1), axis=0).clip(-3, 3)
    signal_z = signal_z.sub(signal_z.mean(axis=1), axis=0)
    gross = signal_z.abs().sum(axis=1).replace(0.0, np.nan)
    return signal_z.div(gross, axis=0)

def equity_curve_regime_scale(lookback=20, defensive_scale=0.25):
    def scaler(positions, **cache):
        returns = cache["returns"]
        mask = cache.get("_tradeable_mask") or cache.get("_liquidity_mask")
        if mask is not None:
            returns = returns.where(mask)
        raw_ret = (positions.shift(1) * returns).sum(axis=1)
        equity  = (1 + raw_ret).cumprod()
        equity_ma = equity.rolling(lookback).mean()
        scale = pd.Series(
            np.where(equity > equity_ma, 1.0, defensive_scale),
            index=equity.index,
        )
        return positions.mul(scale.shift(1), axis=0)
    scaler.__name__ = f"equity_curve_regime_scale_{lookback}_{defensive_scale}"
    return scaler


# ── Study factory ─────────────────────────────────────────────────────────────

def build_study(
    *,
    name,
    factors_loader=load_baseline_factors,
    signal_window=5,
    signal_shift=1,
    vol_window=5,
    vol_quantile=0.6,
    volume_window=30,
    volume_quantile=0.8,
    momentum_window=60,
    momentum_quantile=0.7,
    liquidity_top_n=250,
    liquidity_window=60,
    extra_filters=None,
    rebalance_every=1,
    risk_scalers=None,
):
    def mr_signal(**cache):
        sig = -cache["residual_returns"].rolling(signal_window).mean()
        if signal_shift:
            sig = sig.shift(signal_shift)
        return sig

    study = (
        Study(
            universe=load_universe(),
            benchmark=load_benchmark(),
            factors=factors_loader(),
            name=name,
        )
        .residualize_returns()
        .base_signal(mr_signal)
        .transform_signal(demean_signal)
        .add_vol_filter(vol_window=vol_window, quantile=vol_quantile)
        .add_volume_zscore_filter(window=volume_window, min_zscore_quantile=volume_quantile)
        .add_momentum_context_filter(window=momentum_window, max_abs_quantile=momentum_quantile)
    )

    for fn in extra_filters or []:
        study = study.add_filter(fn)

    study = study.add_tradeable_constraint(
        qs.liquidity(top_n=liquidity_top_n, window=liquidity_window)
    )
    study = study.build_positions(proportional_positions).rebalance(every=rebalance_every)

    for fn in risk_scalers or []:
        study = study.scale_risk(fn)

    return study.run()


def baseline_study(name="baseline"):
    return build_study(name=name, risk_scalers=[equity_curve_regime_scale()])


# ── Output helper ─────────────────────────────────────────────────────────────

def emit_metrics(study):
    print(json.dumps(study.metrics_dict(), default=str, sort_keys=True))
```

### `v0.py` — baseline (fully inline)

v0 should be entirely self-contained — no imports from `common.py`. Write all signal, filter, and scaler logic inline so the baseline is readable without any shared context.

```python
"""Baseline study — all logic explicit, no imports from common."""
import json
import numpy as np
import pandas as pd
import qstudy as qs
from qstudy import Study
from qstudy.constants import SP500

START_DATE, END_DATE = "2015-01-01", "2023-12-31"

universe  = qs.download(SP500,           START_DATE, END_DATE)
factors   = qs.download(["SPY", "XLK"], START_DATE, END_DATE)
benchmark = qs.download("SPY",           START_DATE, END_DATE)

def demean_signal(signal, **cache):
    return signal.sub(signal.mean(axis=1), axis=0)

def proportional_positions(signal, **cache):
    z = signal.sub(signal.mean(axis=1), axis=0)
    z = z.div(z.std(axis=1), axis=0).clip(-3, 3)
    z = z.sub(z.mean(axis=1), axis=0)
    return z.div(z.abs().sum(axis=1).replace(0.0, np.nan), axis=0)

def equity_curve_regime_scale(positions, **cache):
    returns = cache["returns"]
    mask = cache.get("_liquidity_mask")
    if mask is not None:
        returns = returns.where(mask)
    raw_ret = (positions.shift(1) * returns).sum(axis=1)
    equity  = (1 + raw_ret).cumprod()
    scale   = pd.Series(np.where(equity > equity.rolling(20).mean(), 1.0, 0.25), index=equity.index)
    return positions.mul(scale.shift(1), axis=0)

def mr_signal(**cache):
    return -cache["residual_returns"].rolling(5).mean().shift(1)

study = (
    Study(universe=universe, benchmark=benchmark, factors=factors, name="v0_baseline")
    .residualize_returns()
    .base_signal(mr_signal)
    .transform_signal(demean_signal)
    .add_vol_filter(vol_window=5, quantile=0.6)
    .add_volume_zscore_filter(window=30, min_zscore_quantile=0.8)
    .add_momentum_context_filter(window=60, max_abs_quantile=0.7)
    .add_tradeable_constraint(qs.liquidity(top_n=250, window=60))
    .build_positions(proportional_positions)
    .rebalance(every=1)
    .scale_risk(equity_curve_regime_scale)
    .run()
)

if __name__ == "__main__":
    print(json.dumps(study.metrics_dict(), default=str, sort_keys=True))
```

### `v1.py`–`vN.py` — iteration scripts

Each iteration imports from `common` and calls `build_study()` with exactly the parameters that differ from the baseline. Change **one axis per version** so the effect is interpretable.

```python
"""v1 — <one-line description of the change>."""
from common import build_study, emit_metrics, equity_curve_regime_scale

study = build_study(
    name="v1_<change_label>",
    # override exactly the parameters that differ from baseline:
    risk_scalers=[equity_curve_regime_scale()],
)

if __name__ == "__main__":
    emit_metrics(study)
```

### `run_all.py` template

```python
import importlib.util
import json
from pathlib import Path

import pandas as pd

HERE     = Path(__file__).resolve().parent
CSV_PATH = HERE / "results.csv"

PREFERRED_COLS = [
    "sharpe", "ann_return", "ann_vol", "max_drawdown",
    "max_drawdown_duration", "avg_daily_turnover",
    "benchmark_corr", "information_ratio",
]


def load_study(version):
    path = HERE / f"{version}.py"
    spec = importlib.util.spec_from_file_location(version, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.study


def main():
    versions = ["v0", *[f"v{i}" for i in range(1, N + 1)]]  # set N to your last version
    rows = []
    for version in versions:
        metrics = load_study(version).metrics_dict()
        metrics["version"] = version
        rows.append(metrics)

    df = pd.DataFrame(rows).set_index("version")
    df.transpose().to_csv(CSV_PATH)

    existing = [c for c in PREFERRED_COLS if c in df.columns]
    print(df[existing].sort_index().round(4).to_string())
    print(f"\nWrote: {CSV_PATH}")
    print("\nJSON:")
    print(json.dumps(rows, default=str, indent=2))


if __name__ == "__main__":
    main()
```

Run with: `uv run python experiments/<study-name>/run_all.py`

### `LOG.md` convention

```markdown
# <Study Title>

Brief description of the study goal and the metric being optimized.

## Baseline

### `v0`
- Setup: universe, factors, signal, filters, scalers used
- Result: Sharpe `X.XX`, max drawdown `-X.XX%`, duration `NNN`, turnover `X.XX`

## Iterations

### `v1`
- Change: <one-line description of what was changed vs. v0>
- Result: <key metric deltas>; keep / reject

### `v2`
...

## Summary
- What worked, what didn't, and why
- Final recommended version and its metrics
```

---

## Key Rules

- **NaN = excluded, 0 = signal.** In filters, use `signal.where(mask)` to NaN-out ineligible assets. Never set signal to 0 — zero is a valid signal value that will be ranked and potentially traded.
- **Liquidity filter last** among signal filters — it NaN-outs everything outside the liquid universe, so filters applied after operate on a smaller set.
- **1-day execution lag** is baked into `engine.run()` via `positions.shift(1)`. Do not shift signals manually.
- **Download once, reuse** — `qs.download()` hits yfinance. Do it once per session and pass `StudyData` objects to `Study`.
- **residualize_returns() requires** either `factors=` or `benchmark=` in the `Study` constructor.

---

## Cache Keys in Custom Functions

| Key | Type | Notes |
|-----|------|-------|
| `"returns"` | `pd.DataFrame` | always available |
| `"close"` | `pd.DataFrame` | always available |
| `"volume"` | `pd.DataFrame` | always available |
| `"benchmark"` | `pd.Series` | if benchmark provided |
| `"factor_returns"` | `pd.DataFrame` | if factors provided |
| `"_active_returns"` | `pd.DataFrame` | residuals if residualized, else returns |
| `"residual_returns"` | `pd.DataFrame` | after `residualize_returns()` |
| `"signal"` | `pd.DataFrame` | current signal state (in filters) |
| `"positions"` | `pd.DataFrame` | current positions (in scalers) |
| `"_liquidity_mask"` | `pd.DataFrame` | after `add_liquidity_filter()` runs |

---

## Full API Reference

**Constants**
```python
from qstudy.constants import SP500         # ~500 S&P 500 tickers
from qstudy.constants import SECTOR_ETFS  # XLC XLY XLP XLE XLF XLV XLI XLK XLB XLRE XLU
from qstudy.constants import MAJOR_INDEXES # SPY QQQ DIA IWM
```

**Data**
- `qs.download(tickers, start, end) -> StudyData`

**Filters (functional API — use inside custom functions)**
- `qs.vol_filter(signal, returns, vol_window, quantile, keep) -> pd.DataFrame`
- `qs.volume_zscore_filter(signal, volume, window, min_zscore_quantile) -> pd.DataFrame`
- `qs.momentum_context_filter(signal, returns, window, max_abs_quantile) -> pd.DataFrame`
- `qs.vix_contango_filter(signal, vix_close, window) -> pd.DataFrame`
- `qs.residualize(returns, factor_returns) -> (residuals_df, params_df, rsquared_s)`

**Portfolio Construction**
- `qs.liquidity_filter(close, volume, top_n=250, window=60) -> pd.DataFrame`
- `qs.build_long_short_positions(signal, n_long=25, n_short=25) -> pd.DataFrame`
- `qs.build_long_only(signal, n=10) -> pd.DataFrame`
- `qs.rebalance(positions, every=5) -> pd.DataFrame`

**Backtest Engine**
- `qs.run(positions, returns) -> pd.Series` — 1-day lag applied

**Metrics**
- `qs.metrics.summary(returns, positions=None, benchmark=None) -> pd.Series`
- `qs.metrics.sharpe(returns) -> float`
- `qs.metrics.annualized_return(returns) -> float`
- `qs.metrics.max_drawdown(returns) -> float`
- `qs.metrics.information_ratio(returns, benchmark) -> float`

**Charts**
- `qs.summary_plot(returns, figsize=(14, 8))` — equity / drawdown / rolling Sharpe
- `qs.param_heatmap(results_df, row_param, col_param, metric="metric")`

**Grid Search**
- `qs.param_grid(param_dict, backtest_fn, metric_fn=None) -> pd.DataFrame`
