# Routing Policy (v7)

## Precedence

1. Explicit `/fr-*` (or a folded alias below)
2. Clear natural-language domain outcome
3. Ambiguous / multi-domain → `/fr`
4. Greeting / thanks / simple math → no skill

One request → one primary surface. Secondary = explicit handoff.

## Surfaces (keep)

| Intent | Surface |
|---|---|
| triage, “Friday”, unclear, session retro | `/fr` |
| hub: orient, arch, ADR, consolidate, audit, sync/drift, timeline, init-agent, workspace | `/fr-sdlc` |
| feature Design | `/fr-design` |
| implement one work-item | `/fr-implement` |
| bug / incident / runbook / fix from review | `/fr-fix` |
| scored review / PR | `/fr-review` |
| tests, coverage, bench/load, test tooling | `/fr-test` |
| ship gate | `/fr-ship` |
| polished docs, stakeholder brief, release notes | `/fr-write` |
| teach, path | `/fr-learn` |
| citations, compare sources | `/fr-research` |
| inbox, MOC, capture, vault health | `/fr-brain` |
| life / personal project (including init) | `/fr-life` |
| TickTick | `/fr-ticktick` |
| internal tool | `/fr-tool` |
| publish docs to Git | `/fr-publish` |
| explicit `.http` / httpyac | `/fr-httpyac` |
| opt-in brainstorm panel, 2–5 roles | `/fr-panel` |
| named pipeline / วนจนผ่าน | `/fr-pipe` |

## Folded aliases (no surface folder)

| Old / signal | Use |
|---|---|
| `/fr-pr` | `/fr-review` |
| `/fr-fix-from-review` | `/fr-fix` |
| `/fr-runbook` | `/fr-fix` (incident) |
| `/fr-test-init` `/fr-perf` `/fr-perf-init` | `/fr-test` |
| `/fr-orient` `/fr-workspace` `/fr-arch` `/fr-decision` `/fr-consolidate` `/fr-audit` `/fr-sync` `/fr-drift` `/fr-timeline` `/fr-init-agent` `/fr-brief` | `/fr-sdlc` (pick mode) |
| Feature Design summary | `/fr-sdlc` summary or `/fr-write` |
| `/fr-retro` | `/fr` |
| `วนจนผ่าน` | `/fr-pipe` (recipe `quality`) |

## Disambiguation

| Signal | Prefer |
|---|---|
| bug / outage | `/fr-fix` |
| docs ≠ code | `/fr-sdlc` sync (scope: feature or project) |
| PR / scored review | `/fr-review` |
| run / init tests or load | `/fr-test` |
| generate `.http` | `/fr-httpyac` |
| teach | `/fr-learn` |
| sources | `/fr-research` |
| stakeholder brief / release notes | `/fr-write` |
| personal trip/home/health / new personal project | `/fr-life` |
| vault inbox | `/fr-brain` |
| brainstorm / ขอมุมชน / panel | `/fr-panel` — not `/fr-brain` |
| pipeline / วนจนผ่าน | `/fr-pipe` — not fused `/fr-review` |
| TickTick | `/fr-ticktick` |
| tool grows into product | `/fr-design` |

## Rules

- Outcome over keyword.
- Don't route v7 into friday-v6 or v5.
- Don't invent vault paths. SoT: `schema/vault.md`.
