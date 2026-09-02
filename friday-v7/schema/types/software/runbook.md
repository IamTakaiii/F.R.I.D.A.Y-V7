---
type: runbook
id: "{{project_slug}}.ops.{{slug}}"
project: "{{project}}"
created: "{{date}}"
updated: "{{date}}"
status: current
rev: 1
lifecycle: ship
tags: []
standard: 7
max_lines: 200
parts: []
---
<!-- fill: Trigger and scope, Steps, Recovery, Validation · omit: Comms, Prevention if none · omit: Links if none -->
# Runbook — {{title}}

## Trigger and scope

{{when to open · severity}}

## Steps

1. {{action}}

## Recovery

{{rollback / mitigate}}

## Validation

{{how we know it is over}}

## Escalation

{{who · when}}

## Links

- Brief: [[../00 - Overview/01 - Brief]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
