---
type: decision-ticket
id: "{{project_slug}}.feat.{{feature_id}}.decision.{{decision_id}}"
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
decision_id: "{{decision_id}}"
decision_kind: "{{research|experiment|discussion|prerequisite}}"
decision_state: "{{open|claimed|resolved|out-of-scope}}"
---
<!-- fill: Question; Resolution only when closed · one ticket fits one fresh context -->
# DEC-{{decision_id}} — {{title}}

## Question

{{one precise decision or investigation}}

## Resolution

{{answer · evidence · consequence; omit while open}}

## Links

- Map: [[../../{{map}}]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
