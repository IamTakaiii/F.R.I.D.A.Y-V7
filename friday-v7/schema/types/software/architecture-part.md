---
type: architecture-part
id: "{{project_slug}}.arch.{{part_kind}}"
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
part_kind: stack
---
<!-- fill: Version pins · omit: Links if none · part_kind: stack only -->
# Architecture part — {{part_kind}}

## Version pins

| Package | Version | Upgrade |
|---|---|---|
| {{name}} | {{ver}} | {{policy}} |

## Risks

{{compat · lock-in}}

## Links

- Architecture: [[01 - Architecture]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
