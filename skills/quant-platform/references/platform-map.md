# Quant platform map

This is a starting map for discovery. Verify paths, remotes, branches, and
current component documentation before relying on any entry.

| Component | Local checkout | GitHub | Owns | First context to read |
| --- | --- | --- | --- | --- |
| quant-infra | `/Users/jplatta/repos/quant-infra` | `https://github.com/jwplatta/quant-infra` | Docker runtime, Compose profiles, monitoring, environment wiring | `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `Makefile`, `services/`, `deploy/` |
| Tickrake | `/Users/jplatta/repos/tickrake` | `https://github.com/jwplatta/tickrake` | Market-data ingestion, scheduling, storage, publication contracts | `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `lib/`, `spec/`, config and job definitions |
| schwab_rb | `/Users/jplatta/repos/schwab_rb` | `https://github.com/jwplatta/schwab_rb` | Schwab authentication, REST API, and streaming-client library behavior | `README.md`, `AGENTS.md`, `CHANGELOG.md`, `lib/`, `spec/`, gem configuration |
| Tractatus | `/Users/jplatta/repos/tractatus` | `https://github.com/jwplatta/tractatus` | Research-facing configuration and access to published data | `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `src/` or package modules, tests |
| Options Monitor | `/Users/jplatta/repos/options-monitor` | `https://github.com/jwplatta/options-monitor` | User-facing intraday dashboard and consumer behavior | `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, application source, tests |

## Quant-infra runtime discovery

The Makefile combines base Compose definitions under `services/` with
environment overlays in `deploy/dev.yml` and `deploy/prod.yml`. Inspect the
actual Makefile target before any operation; profiles determine the service
set. `services/tickrake/compose.yml` identifies runtime services, while
`services/tickrake/jobs/{prod,dev}/` identifies the selected job files and
`services/tickrake/config/{prod,dev}/` contains versioned configuration and
universes.

Use current Compose configuration, running-service status, and mounted paths
to understand a deployed service. A healthy container does not prove that its
data path or external stream is healthy.

## Data-flow orientation

The normal direction is:

```text
market/broker sources -> Tickrake -> local and archive/published data
                       -> Tractatus and research consumers
                       -> Options Monitor and operational views

quant-infra supplies runtime services, storage, and observability around the flow.
```

Treat published data/indexes/manifests as consumer contracts. Do not make a
consumer depend on Tickrake's private SQLite database or unversioned internal
filesystem layout without an explicit, current contract.

## Refresh checklist

When working across components, check:

- Git remote and current branch in every affected checkout.
- `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, and `AGENTS.md` where they
  exist.
- Existing plans, notes, backlog items, and open local worktree changes.
- Producer schema and live consumer assumptions for data-contract changes.
- Effective Compose configuration and exact target services for runtime work.
