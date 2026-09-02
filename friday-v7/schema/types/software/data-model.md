---
type: data-model
id: "{{project_slug}}.data.model.{{slug}}"
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
---
<!-- fill: Purpose and ownership, Entities, Invariants · columns live in data-dict -->
# Data model — {{name}}

## Purpose and ownership

{{cluster · owning feature}}

## Entities

| Entity | Keys | Tenancy | Delete/orphan |
|---|---|---|---|
| {{}} | {{}} | {{}} | {{}} |

## Invariants

| Rule | Owner |
|---|---|
| {{always-true}} | {{feature}} |

## Lifecycle

{{create → retain → delete}}

## Links

- Brief: [[../00 - Overview/01 - Brief]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
