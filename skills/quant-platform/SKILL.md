---
name: quant-platform
description: Coordinate work across the local quant research platform when a task spans quant-infra, Tickrake, Tractatus, Options Monitor, data contracts, or runtime operations.
---

# Quant Platform

Use this skill when a request concerns the platform as a system: ownership
boundaries, cross-repository changes, data flows, Docker runtime behavior,
production operations, or a component whose source of truth is not obvious.
Do not use it for a self-contained change within one repository unless the
platform context changes the implementation or deployment decision.

## Core model

`quant-infra` is the runtime and integration entry point. Tickrake ingests and
publishes market data; research consumers read published outputs rather than
Tickrake internals. `schwab_rb` owns the shared Schwab API and streaming-client
library used by Tickrake. Keep application code, runtime wiring, and consumer
code in their owning repositories. Do not turn a local deployment detail into
a producer or consumer contract.

The current repository map is in [references/platform-map.md](references/platform-map.md).
It is a discovery guide, not a complete inventory or an immutable source of
truth.

## Start with a freshness pass

Before making a cross-platform claim or changing another repository:

1. Identify the affected repository or repositories from the map, then verify
   their actual local paths and Git remotes with `git -C <repo> remote -v`.
2. Read each affected repository's `README.md`, `CONTRIBUTING.md`,
   `CHANGELOG.md`, and `AGENTS.md` when present. Check `git status --short`
   before editing.
3. Inspect live configuration and contracts where relevant: Compose files and
   overlays in `quant-infra`; job/config/data code in Tickrake; client and
   configuration code in Tractatus; consumer interfaces in Options Monitor.
4. Use `git log`, current configuration, and tests as stronger evidence than a
   static architecture note. Say when a conclusion is inferred rather than
   confirmed.

## Route work to the owner

- **quant-infra:** Docker Compose profiles, host/container mounts, credentials
  wiring, service orchestration, monitoring, dashboards, and operational
  runbooks.
- **Tickrake:** data collection, scheduling, raw-event handling, storage,
  publication contracts, and producer-side recovery behavior.
- **schwab_rb:** Schwab authentication, REST access, and the shared streaming
  client; library behavior and reconnect semantics used by Tickrake.
- **Tractatus:** research-facing configuration, data discovery/downloads, and
  consumer access to published Tickrake outputs.
- **Options Monitor:** user-facing intraday monitoring and consumption of
  published data contracts.

When a task crosses boundaries, identify the producer, the consumer, and the
contract between them. Change the smallest owner that can correct the issue;
coordinate a versioned contract change across every affected consumer rather
than relying on private files, SQLite internals, or filesystem enumeration.

## Runtime safety

Treat `quant-infra` production as live. Inspect the exact Compose profile,
service list, mounts, and effective configuration before operations. For
monitoring-only changes, prefer targeted commands and avoid broad `up`,
`restart`, or `down` operations. Do not restart, stop, recreate, or otherwise
interrupt Tickrake jobs without explicit user approval.

Credentials and mutable homes stay outside repositories. Do not commit or
echo credential files, and do not treat host paths as durable cross-component
contracts.

## Keep coordination current

For consequential work, create or update a concise plan in the initiating
repository's `docs/plans/` directory. Record durable discoveries and runbooks
in `docs/notes/`; create actionable follow-up items in `docs/backlog/` using
the installed `project-backlog` skill. Update the relevant changelog when a
repository's user-visible behavior changes.

Surface platform drift while working: a changed remote, missing documentation,
an incompatible producer/consumer schema, or an undocumented runtime
dependency is useful output, not background noise. Confirm the owner before
fixing it.
