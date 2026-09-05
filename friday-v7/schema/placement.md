# Placement (only legal vault paths)

Do not invent a folder or filename. Type → one pattern. If it does not fit, pick another registered type or do not write.

`{P}` = `20 - Projects/10 - Software/NN - <Project>`
`{F}` = `{P}/03 - Features/NN - <slug>`
`{L}` = `20 - Projects/20 - Personal/NN - <Project>`

## Software

| Type | Path |
|---|---|
| brief | `{P}/00 - Overview/01 - Brief.md` |
| feature-list | `{P}/00 - Overview/02 - Feature List.md` |
| glossary | `{P}/00 - Overview/03 - Glossary.md` |
| timeline-log | `{P}/00 - Overview/{04\|05\|06\|07} - {production\|development} {feature\|change} log.md` |
| architecture | `{P}/01 - Architecture/01 - Architecture.md` |
| architecture-part | `{P}/01 - Architecture/stack.md` (`part_kind: stack` only) |
| adr | `{P}/02 - Decisions/ADR-NN - <title>.md` |
| intent | `{F}/intent.md` |
| design | `{F}/design.md` |
| design-part | `{F}/design/{contracts\|flow\|quality\|operations}.md` |
| queue | `{F}/queue.md` |
| api | `{F}/api/NN - <resource>.md` |
| work-item | `{F}/work/TODO-XX - <title>.md` |
| fix-note | `{F}/fixes/YYYY-MM-DD - <title>.md` |
| quality-report | `{F}/reports/YYYY-MM-DD - {Code Review\|Artifact Review\|Deep Review\|Test Report\|Perf Report}.md` |
| feature-plan | `{F}/plans/<slug>.md` |
| audit-plan | `{P}/00 - Overview/` or `{F}/plans/` — never `{agent_root}` |
| decision-map | `{F}/plans/decision-map-<slug>.md` |
| decision-ticket | `{F}/plans/<map>/decisions/DEC-NN - <title>.md` |
| questionnaire | `{F}/plans/questions/<slug>.md` |
| data-model | `{P}/04 - Data/01 - Model/<slug>.md` |
| data-dict | `{P}/04 - Data/02 - Dictionary/<slug>.md` |
| ship-checklist | `{P}/06 - Ship/YYYY-MM-DD - Ship.md` |
| release-notes | `{P}/06 - Ship/YYYY-MM-DD - Release Notes.md` |
| runbook | `{P}/07 - Operations/<slug>.md` |
| memory-lesson | `{P}/90 - Log/YYYY-MM-DD - <title>.md` |
| note | `{P}/89-Notes/Notes/YYYY-MM-DD - <title>.md` or `30 - Knowledge/20 - Notes/YYYY-MM-DD - <title>.md` or `30 - Knowledge/10 - MOCs/NN - <topic>.md` or `40 - Writing/…/YYYY-MM-DD - <title>.md` |

`quality-report.kind` must match the filename: review→Code/Artifact/Deep Review, test→Test Report, perf→Perf Report.

## Personal

| Type | Path |
|---|---|
| brief | `{L}/00 - Overview/01 - Brief.md` (`project_kind: personal`) |
| personal-goals | `{L}/00 - Overview/02 - Goals.md` |
| personal-plan | `{L}/01 - Plan/<slug>.md` |
| trip-plan | `{L}/01 - Plan/Trip - <slug>.md` |
| personal-tasks | `{L}/02 - Tasks/<slug>.md` |
| personal-decision | `{L}/03 - Decisions/<slug>.md` |
| personal-research | `{L}/04 - Research/<slug>.md` |
| personal-risk | `{L}/05 - Risk/<slug>.md` |
| personal-outcome | `{L}/06 - Outcomes/<slug>.md` |
| personal-budget | `{L}/30 - Budget/<slug>.md` |
| note | `{L}/90 - Log/YYYY-MM-DD - <title>.md` |

## Not governed

`10 - Inbox/` captures are raw until **promoted**: rewrite as a registered type at its path above. Do not leave durable decisions in Inbox.
