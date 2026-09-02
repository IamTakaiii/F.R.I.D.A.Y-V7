---
type: ship-checklist
id: "{{project_slug}}.ship.{{slug}}"
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
<!-- fill: What ships, Gates, Verdict · one row per must from gates/ship.md · omit: Links if none -->
# Ship — {{release}}

## What ships

{{commits / tags / queue ids}}

## Gates

| # | Gate | Result |
|---|---|---|
| S0 | Named scope | {{pass\|fail}} |
| S2 | Verify green | {{}} |
| S4 | Rollback named | {{}} |
| S5 | Smoke named | {{}} |
| S9 | Code review PASS (if L/high-risk) | {{pass\|n/a}} |

## Verdict

**{{go\|go_with_conditions\|no-go}}** · {{conditions the user owns}}

## Links

- Brief: [[../00 - Overview/01 - Brief]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
