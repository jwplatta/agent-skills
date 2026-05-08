---
name: qstudy-backtests
description: Write cross-sectional equity backtests using the qstudy library. Use when building or reviewing long/short SP500 factor studies, signal research, or parameter grid searches in trade_lab notebooks.
---

# qstudy Backtests

## Overview

`qstudy` is a lightweight cross-sectional equity backtesting library in `src/qstudy/`. It handles all boilerplate — data loading, liquidity filtering, position construction, PnL engine, and metrics. The researcher writes only the signal formula.

```python
import qstudy as qs
from qstudy.constants import SP500
```

## Workflow

1. **Download** — single API call returns close, volume, returns, log_returns
2. **Signal** — write the formula inline (this is the only unique code)
3. **Filter** — optionally apply vol, volume, or momentum context filters
4. **Liquidity mask** — keep top N assets by rolling dollar volume
5. **Positions** — rank signal cross-sectionally, select longs and shorts
6. **Rebalance** — optional; default is daily (no rebalancing)
7. **Run** — apply 1-day execution lag, sum weighted returns
8. **Metrics / Charts** — `summary()` + `summary_plot()`

## Core Patterns

### Minimal Backtest

```python
import qstudy as qs
from qstudy.constants import SP500

d = qs.download(SP500, start="2015-01-01", end="2023-12-31")
close_df, volume_df, returns_df = d["close"], d["volume"], d["returns"]

# Signal — mean reversion (write inline, this is the research)
signal = -returns_df.rolling(5).mean().shift(1)

# Liquidity filter (always apply before build_positions)
liq_mask = qs.liquidity_filter(close_df, volume_df, top_n=250)
signal = signal.where(liq_mask)
ret_filtered = returns_df.where(liq_mask)

# Portfolio and backtest
positions = qs.build_positions(signal, n_long=25, n_short=25)
port_ret = qs.run(positions, ret_filtered)

print(qs.metrics.summary(port_ret, positions))
qs.summary_plot(port_ret)
```

### VIX Contango Filter (Regime Gate)

```python
from qstudy.constants import VOL_INDEXES

d_vix = qs.download(VOL_INDEXES, start="2015-01-01", end="2023-12-31")
signal = qs.vix_contango_filter(signal, d_vix["close"])
# Zeros out all positions on dates where VIX1D < VIX9D < VIX is violated
```

### Residual Mean Reversion (Factor-Stripped Signal)

```python
d_factors = qs.download(["SPY", "XLK"], start="2015-01-01", end="2023-12-31")
residuals, factor_params, factor_rsq = qs.residualize(returns_df, d_factors["returns"])

signal = -residuals.rolling(5).mean().shift(1)
signal = signal.sub(signal.mean(axis=1), axis=0)  # cross-sectional demean
```

### Adding Filters (chain with `.where()`)

```python
# Keep low-vol assets (cross-sectional — below quantile on each date)
signal = qs.vol_filter(signal, returns_df, vol_window=40, quantile=0.75, keep="low")

# Keep assets with above-average recent volume activity
signal = qs.volume_zscore_filter(signal, volume_df, window=10, min_zscore_quantile=0.65)

# Keep assets with weak medium-term momentum (context for mean reversion)
signal = qs.momentum_context_filter(signal, returns_df, window=15, max_abs_quantile=0.75)

# Apply liquidity mask last
signal = signal.where(liq_mask)
```

### Rebalancing (hold positions N days)

```python
positions = qs.build_positions(signal, n_long=25, n_short=25)
positions = qs.rebalance(positions, every=5)   # weekly
positions = qs.rebalance(positions, every=21)  # monthly
# every=1 is a no-op (daily rebalance, the default)
```

### Benchmark Comparison

```python
d_bm = qs.download("SPY", start="2015-01-01", end="2023-12-31")
bm_returns = d_bm["returns"]  # single-ticker download returns a 1-col DataFrame; squeeze handled internally

print(qs.metrics.summary(port_ret, positions, benchmark=bm_returns))
# Adds: benchmark_ann_return, benchmark_sharpe, benchmark_corr, information_ratio
```

### Parameter Grid Search

```python
liq_mask = qs.liquidity_filter(close_df, volume_df, top_n=250)
ret_filtered = returns_df.where(liq_mask)

def run_backtest(params):
    signal = -returns_df.rolling(params["window"]).mean().shift(1)
    signal = qs.vol_filter(signal, returns_df, vol_window=params["vol_wind"], quantile=params["qt"])
    signal = signal.where(liq_mask)
    positions = qs.build_positions(signal, n_long=25, n_short=25)
    return qs.run(positions, ret_filtered)

results = qs.param_grid(
    {"window": [5, 10, 15], "vol_wind": [20, 40], "qt": [0.6, 0.75, 0.9]},
    run_backtest,
    metric_fn=qs.metrics.sharpe,  # omit to get full summary() columns
)

qs.param_heatmap(results, row_param="qt", col_param="window", metric="metric", figsize=(12, 8))
```

## Key Rules

- **NaN → short**: `build_positions` uses `na_option='bottom'` — NaN signals rank last and land in the short bucket. Always apply `liquidity_filter` before `build_positions` to prevent illiquid assets from being unintentionally shorted.
- **Liquidity filter ordering**: Apply `liq_mask` to both the signal and the returns DataFrame used in `run()`.
- **1-day execution lag**: Positions built on day T earn the return on day T+1. This is baked into `qs.run()`.
- **Cross-sectional quantile**: `vol_filter` thresholds are computed across tickers per date (not rolling per ticker). This is intentional and matches the original notebook behavior.
- **Single-ticker download**: `qs.download("SPY", ...)["returns"]` returns a single-column DataFrame, not a Series. All qstudy functions handle this via `.squeeze()` internally.

## Available Constants

```python
from qstudy.constants import SP500        # ~500 S&P 500 tickers
from qstudy.constants import SECTOR_ETFS  # ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLK', 'XLB', 'XLRE', 'XLU']
from qstudy.constants import MAJOR_INDEXES  # ['SPY', 'QQQ', 'DIA', 'IWM']
```

## Full API Reference

**Data**
- `qs.download(tickers, start, end) -> dict` — keys: `close`, `volume`, `returns`, `log_returns`, `data`

**Signals / Filters**
- `qs.vol_filter(signal, returns, vol_window=40, quantile=0.75, keep="low") -> pd.DataFrame`
- `qs.volume_zscore_filter(signal, volume, window=10, min_zscore_quantile=0.65) -> pd.DataFrame`
- `qs.momentum_context_filter(signal, returns, window=15, max_abs_quantile=0.75) -> pd.DataFrame`
- `qs.vix_contango_filter(signal, vix_close) -> pd.DataFrame` — zeros out signal on dates where VIX1D < VIX9D < VIX is not satisfied
- `qs.residualize(returns, factor_returns) -> (residuals_df, params_df, rsquared_s)`

**Portfolio Construction**
- `qs.liquidity_filter(close, volume, top_n=250, window=60) -> pd.DataFrame` — boolean mask
- `qs.build_positions(signal, n_long=25, n_short=25) -> pd.DataFrame` — dollar-neutral weights
- `qs.rebalance(positions, every=5) -> pd.DataFrame` — stride-based, forward-fill

**Backtest Engine**
- `qs.run(positions, returns) -> pd.Series` — 1-day lag applied

**Metrics**
- `qs.metrics.sharpe(returns, periods_per_year=252) -> float`
- `qs.metrics.annualized_return(returns, periods_per_year=252) -> float`
- `qs.metrics.annualized_vol(returns, periods_per_year=252) -> float`
- `qs.metrics.max_drawdown(returns) -> float`
- `qs.metrics.max_drawdown_duration(returns) -> int`
- `qs.metrics.drawdown_series(returns) -> pd.Series`
- `qs.metrics.rolling_sharpe(returns, window=90, periods_per_year=252) -> pd.Series`
- `qs.metrics.turnover(positions) -> pd.Series`
- `qs.metrics.information_ratio(returns, benchmark, periods_per_year=252) -> float`
- `qs.metrics.summary(returns, positions=None, benchmark=None, periods_per_year=252) -> pd.Series`

**Charts** (all accept optional `ax`, return `Axes`; `summary_plot` returns `Figure`)
- `qs.equity_curve(returns, title="Equity Curve", ax=None)`
- `qs.drawdown_plot(returns, title="Drawdown", ax=None)`
- `qs.rolling_sharpe_plot(returns, window=90, ax=None)`
- `qs.summary_plot(returns, figsize=(14, 8))` — 3-panel: equity / drawdown / rolling Sharpe
- `qs.corr_heatmap(returns_matrix, title="Correlation", figsize=(10, 8))`
- `qs.param_heatmap(results_df, row_param, col_param, metric="metric", figsize=(10, 6))`

**Grid Search**
- `qs.param_grid(param_dict, backtest_fn, metric_fn=None) -> pd.DataFrame`
