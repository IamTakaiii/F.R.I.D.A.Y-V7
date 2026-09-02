---
type: data-dict
id: "{{project_slug}}.data.dict.{{slug}}"
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
<!-- fill: Fields · meaning ≠ column name · ORM wins if they diverge -->
# Data dictionary — {{name}}

## Fields

| Name | Type | Null | Key | Meaning |
|---|---|---|---|---|
| {{col}} | {{}} | {{yes\|no}} | {{PK\|FK\|—}} | {{product meaning · units}} |

## Constraints

{{unique / checks — omit heading if none}}

## Links

- Brief: [[../00 - Overview/01 - Brief]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
