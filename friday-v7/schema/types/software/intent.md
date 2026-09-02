---
type: intent
id: "{{project_slug}}.feat.{{feature_id}}.intent"
project: "{{project}}"
created: "{{date}}"
updated: "{{date}}"
status: current
rev: 1
lifecycle: delivery
tags: []
standard: 7
max_lines: 200
parts: []
feature: "{{feature}}"
feature_id: "{{feature_id}}"
depends_on: []
---
<!-- fill: Outcome, Current state, Success criteria · omit: Non-goals, Constraints, Links if none -->
# Intent — {{feature}}

## Outcome

{{one checkable change — no API paths}}

## Current state

- Status: {{mapped|planned|building|stable|blocked}}
- Now: {{what is true}}
- Next: [[queue]]

## Non-goals

{{what this feature will not do}}

## Constraints

{{hard limits}}

## Success criteria

- [ ] {{observable}}

## Links

- Design: [[design]]
- Queue: [[queue]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
