---
type: trip-plan
id: "{{project_slug}}.personal.trip.{{slug}}"
project: "{{project}}"
created: "{{date}}"
updated: "{{date}}"
status: current
rev: 1
lifecycle: personal
tags: []
standard: 7
max_lines: 200
parts: []
---
<!-- fill: Trip brief, Itinerary, Bookings, Before departure, Budget snapshot, Risks and backup · never invent booking refs/prices/times · omit: Links if none -->
# Trip plan — {{title}}

## Trip brief

| Travelers | Dates | Destination / bases | Purpose and pace |
|---|---|---|---|
| {{}} | {{start → end}} | {{}} | {{}} |

**Locked constraints:** {{budget cap · leave/return windows · accessibility · non-negotiables}}

## Itinerary

| Day / date | Base | Plan | Transit | Reservation / decision |
|---|---|---|---|---|
| {{}} | {{}} | {{}} | {{duration · buffer}} | {{confirmed · option · open}} |

## Bookings

| Item | Status | Deadline | Owner | Reference |
|---|---|---|---|---|
| {{flight · stay · ticket · insurance}} | {{open · held · confirmed · cancelled}} | {{date}} | {{}} | {{real ref or —}} |

## Before departure

- [ ] {{task}} — due {{date}} · owner {{}}

## Budget snapshot

| Currency | Cap | Estimated | Confirmed spend | Remaining |
|---|---|---|---|---|
| {{}} | {{}} | {{Assumed or cited}} | {{}} | {{}} |

Detailed transactions belong in `personal-budget`; this table is the current trip-level snapshot.

## Risks and backup

| Trigger | Impact | Prevention | Backup / decision deadline |
|---|---|---|---|
| {{weather · delay · closure · health · document}} | {{}} | {{}} | {{}} |

## Links

- Brief: [[../00 - Overview/01 - Brief]]
- Tasks: [[../02 - Tasks/{{slug}}]]
- Budget: [[../30 - Budget/{{slug}}]]
- Risk: [[../05 - Risk/{{slug}}]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
