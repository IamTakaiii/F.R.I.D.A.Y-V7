# Type registry

One file per type. That file **is** the vault template. `<!-- fill: -->` is agent-only — write-gate strips comments and `>` lines. Do not invent types. Path lives in `placement.md`, not in the template body.

| Folder | Use |
|---|---|
| `types/software/` | Software delivery + shared `brief` |
| `types/personal/` | Personal-only types |
| `types/shared/` | Notes, lessons, glossary, timeline logs |

## Software

| Type | File |
|---|---|
| brief | `types/software/brief.md` |
| feature-list | `types/software/feature-list.md` |
| intent | `types/software/intent.md` |
| design | `types/software/design.md` |
| design-part | `types/software/design-part.md` |
| queue | `types/software/queue.md` |
| work-item | `types/software/work-item.md` |
| api | `types/software/api.md` |
| adr | `types/software/adr.md` |
| architecture | `types/software/architecture.md` |
| architecture-part | `types/software/architecture-part.md` |
| data-model | `types/software/data-model.md` |
| data-dict | `types/software/data-dict.md` |
| quality-report | `types/software/quality-report.md` |
| fix-note | `types/software/fix-note.md` |
| ship-checklist | `types/software/ship-checklist.md` |
| runbook | `types/software/runbook.md` |
| release-notes | `types/software/release-notes.md` |
| feature-plan | `types/software/feature-plan.md` |
| audit-plan | `types/software/audit-plan.md` |
| decision-map | `types/software/decision-map.md` |
| decision-ticket | `types/software/decision-ticket.md` |
| questionnaire | `types/software/questionnaire.md` |

## Personal

| Type | File |
|---|---|
| personal-goals | `types/personal/personal-goals.md` |
| personal-plan | `types/personal/personal-plan.md` |
| trip-plan | `types/personal/trip-plan.md` |
| personal-tasks | `types/personal/personal-tasks.md` |
| personal-decision | `types/personal/personal-decision.md` |
| personal-research | `types/personal/personal-research.md` |
| personal-budget | `types/personal/personal-budget.md` |
| personal-risk | `types/personal/personal-risk.md` |
| personal-outcome | `types/personal/personal-outcome.md` |

Personal overview uses `brief` + `project_kind: personal`. Personal log uses `note`.

## Shared

| Type | File |
|---|---|
| note | `types/shared/note.md` |
| memory-lesson | `types/shared/memory-lesson.md` |
| glossary | `types/shared/glossary.md` |
| timeline-log | `types/shared/timeline-log.md` |
