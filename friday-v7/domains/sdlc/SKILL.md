# Domain: SDLC

Agile delivery. **Load:** `kernel/runtime.md` → this file → **one** `modes/*.md`.

**Every mode:** vault writes → `kernel/io/write.md` + `schema/write-gate.md` (same as every other domain). Chat ≠ delivery.

Surfaces: `/fr-sdlc` `/fr-design` `/fr-implement` `/fr-fix` `/fr-review` `/fr-test` `/fr-ship` `/fr-publish` `/fr-panel` `/fr-pipe`. Other old `/fr-*` names are aliases in `ROUTING.md`.

## Tiers

| Tier | Artifacts |
|---|---|
| S | Feature List row, lightweight Intent, work-item if queued |
| M | + Design card; queue when tracked; ADR if needed |
| L | + queue; Review/Ship when in scope |

## Modes

| Mode | File | How |
|---|---|---|
| orient | `modes/orient.md` | `/fr-sdlc` default; workspace map |
| summary | `modes/summary.md` | Feature + Design card, read-only |
| arch | `modes/arch.md` | `/fr-sdlc` |
| design | `modes/design.md` | `/fr-design` |
| feature-consolidate | `modes/feature-consolidate.md` | `/fr-sdlc` |
| decision | `modes/decision.md` | `/fr-sdlc` |
| implement | `modes/implement.md` | `/fr-implement` |
| publish | `modes/publish.md` | `/fr-publish` |
| timeline | `modes/timeline.md` | `/fr-sdlc` or `/fr-write` |
| fix | `modes/fix.md` | `/fr-fix` (review follow-up, runbook) |
| sync | `modes/sync.md` | `/fr-sdlc` · scope feature \| project |
| review | `modes/review.md` | `/fr-review` (incl. PR) |
| test | `modes/test.md` | `/fr-test` (incl. init, perf) |
| audit-struct | `modes/audit-struct.md` | `/fr-sdlc` |
| ship | `modes/ship.md` | `/fr-ship` |
| init-agent | `modes/init-agent.md` | `/fr-sdlc` |
| panel | `modes/panel.md` | `/fr-panel` (opt-in, no write) |
| pipe | `modes/pipe.md` | `/fr-pipe` (recipe runner, no write) |

No `design-slice`. Reports use `quality-report`.

## On demand

`standards/feature-identity.md` · `execution.md` · `code.md` · `deps.md` · `data.md` · `review.md`(+`.deep`) · `test.md`(+`.deep`) · `perf.md` · `audit.md` · `gates/ready.md` · `gates/done.md` · `gates/ship.md`

## Done

Cite artifact paths. Caps pass.
