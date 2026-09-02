# SDLC — design deep

Load at Capture. Earlier if HTTP/data/async/security/scale/deploy · `ละเอียด`.

Mark each lens `required` or `N/A + evidence`. **Required + missing must → no lock.** N/A skips that table (do not fake Build/Prepare/Defer).

## Lenses

| Lens | Resolve |
|---|---|
| Behavior | actors · pre/post · empty/error/replay |
| Contracts | API/events/ports · validation · errors · version |
| Boundaries | policy → ports inward |
| Data | SoT · keys · lifecycle · migrate — then **Data must** |
| Concurrency | order · idempotency · retry · partial fail |
| Security | authz · trust · sensitive · abuse |
| Reliability | bounds · degrade |
| Scale | then **Scale must** |
| Compat | consumers · evolution · flags |
| Deploy/ops | then **Deploy must** |

## Scale must (lens required)

Fail any blank. Units on every number. `Assumed` needs owner + date. User target is a requirement — current metrics are not a veto.

| # | Must |
|---|---|
| S1 | Launch target + future target + horizon |
| S2 | Each figure labeled Measured / User target / Forecast / Assumed |
| S3 | First bottleneck + hard bound (conn/lock/queue/quota/hot key) |
| S4 | Scale unit/mode (or explicit single-instance limit) |
| S5 | Build / Prepare / Defer — ≤1 line each. Prepare = seams only |
| S6 | Defer trigger = metric + threshold + window + owner — not a calendar alone |

Cost/cardinality if fan-out, retention, or third-party is unbounded. Project-wide scale → Architecture; this card only records deltas.

## Deploy must (lens required)

Sequence, not a final command. Zero-downtime claim without mixed-version proof → no lock.

| # | Must |
|---|---|
| D1 | Artifact + order (config/schema → code → traffic) |
| D2 | Compat window (old/new code × schema/API) or named downtime |
| D3 | Health: signal · threshold · window · owner |
| D4 | Rollback boundary + irreversible data line |
| D5 | No secret values in the vault |

## Data must (lens required)

Both `data-model` + `data-dict` (`standards/data.md`). ORM/migration wins if they diverge.

| # | Must |
|---|---|
| M1 | Owner feature + tenancy/keys |
| M2 | Delete/orphan rule |
| M3 | Migrate/backfill/recovery or “no schema change” |

## HTTP (any HTTP surface)

Design = index only (method · path · link · auth). One `api/` page per resource (fields · errors · auth). No invent. No HTTP → no folder.

## Deps

`standards/deps.md`. `mapped` ≠ shipped.

## Before lock

Attack applicable cases (invalid, empty, replay, concurrent, timeout, partial, unauth, burst, mixed-version, migrate, rollback, blind). Weakness → change Design, own the trade-off, or **block**.
