# Mode → type (only legal writes)

If the type is not in this row, **do not write it**. Pick another mode or do not write.
`none` = chat / git / `.agent` / repo code only. `promote` = Inbox → any registered type at a `placement.md` path. `patch` = keep the file’s existing type.

## SDLC

| Mode | Surface | Types |
|---|---|---|
| orient | `/fr-sdlc` | none |
| summary | `/fr-sdlc` | none |
| arch | `/fr-sdlc` | architecture, architecture-part |
| architecture-improvement | `/fr-sdlc` | audit-plan |
| design | `/fr-design` | intent, design, design-part, api, queue, feature-list, data-model, data-dict |
| design-experiment | `/fr-sdlc` | none |
| decision-map | `/fr-sdlc` | decision-map, decision-ticket |
| delivery-slice | `/fr-sdlc` | queue, work-item |
| feature-consolidate | `/fr-sdlc` | intent, design, queue, feature-list |
| decision | `/fr-sdlc` | adr |
| implement | `/fr-implement` | work-item, queue |
| tdd | `/fr-implement` | work-item, queue |
| publish | `/fr-publish` | none |
| timeline | `/fr-sdlc` | timeline-log |
| fix | `/fr-fix` | fix-note, runbook, design, work-item, queue |
| debug | `/fr-fix` | fix-note |
| work-intake | `/fr-sdlc` | none |
| stakeholder-questions | `/fr-sdlc` | questionnaire |
| guided-procedure | `/fr-sdlc` | runbook |
| sync | `/fr-sdlc` | note |
| review | `/fr-review` | quality-report |
| test | `/fr-test` | quality-report |
| audit-struct | `/fr-sdlc` | audit-plan |
| ship | `/fr-ship` | ship-checklist, release-notes |
| init-agent | `/fr-sdlc` | none |
| panel | `/fr-panel` | none |
| pipe | `/fr-pipe` | none |

`design` on `/fr-fix` only when intended behavior was wrong.

## Other domains

| Mode | Surface | Types |
|---|---|---|
| route | `/fr` | none |
| environment | `/fr` | note, memory-lesson |
| capture | `/fr-brain` | none |
| inbox | `/fr-brain` | promote |
| link | `/fr-brain` | patch |
| moc | `/fr-brain` | note |
| health | `/fr-brain` | none |
| research | `/fr-research` | note, personal-research |
| teach | `/fr-learn` | note |
| path | `/fr-learn` | note |
| distill | `/fr-learn` | note |
| note | `/fr-write` | note, glossary |
| brief | `/fr-write` | note |
| spec | `/fr-write` | note |
| present | `/fr-write` | note |
| polish | `/fr-write` | patch |
| release-notes | `/fr-write` | release-notes, note |
| init | `/fr-life` | brief, personal-goals |
| plan | `/fr-life` | personal-plan |
| budget | `/fr-life` | personal-budget |
| weekly | `/fr-life` | note, personal-outcome |
| logistics | `/fr-life` | trip-plan, personal-tasks, personal-budget, personal-risk, personal-decision, note |
| orient | `/fr-tool` | none |
| shape | `/fr-tool` | none |
| build | `/fr-tool` | none |
| harden | `/fr-tool` | none |
| orient | `/fr-httpyac` | none |
| write | `/fr-httpyac` | none |
| from-design | `/fr-httpyac` | none |
| run | `/fr-httpyac` | none |
| feature-plan | `/fr-sdlc` | feature-plan |
| brief | `/fr-sdlc` | brief |

`brief` (software Overview) is `/fr-sdlc` or first software project create — not Writer `brief` (that is `note`).
