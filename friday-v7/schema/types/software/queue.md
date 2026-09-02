---
type: queue
id: "{{project_slug}}.feat.{{feature_id}}.queue"
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
<!-- fill: Items · next/ready ≤5 · omit: Dependencies if none · omit: Links if none -->
# Queue — {{feature}}

## Items

| ID | Outcome | Status | DoD | Work |
|---|---|---|---|---|
| TODO-{{nn}} | {{one line}} | {{next\|ready\|doing\|done\|blocked}} | {{checkable}} | [[work/TODO-{{nn}} - {{title}}]] |

## Dependencies

| Dep | Status | Strategy | Replace |
|---|---|---|---|
| {{feature}} | {{mapped\|…}} | {{stub\|flag\|port\|block\|narrow}} | {{queue id}} |

## Links

- Intent: [[intent]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
