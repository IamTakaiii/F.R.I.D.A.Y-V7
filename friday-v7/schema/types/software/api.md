---
type: api
id: "{{project_slug}}.feat.{{feature_id}}.api.{{resource}}"
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
resource: "{{resource}}"
---
<!-- fill: Surface, Request, Response, Errors · omit: Behavior and limits, Examples if none · omit: Links if none -->
# API — {{resource}}

## Surface

{{METHOD}} {{/path}} · auth: {{scheme}}

## Request

| Field | Rule |
|---|---|
| {{name}} | {{required · type · limit}} |

## Response

{{success shape}}

## Errors

| Code | When |
|---|---|
| {{4xx/5xx}} | {{condition}} |

## Behavior and limits

{{idempotency · pagination · rate — omit heading if none}}

## Examples

{{one happy · one error — omit heading if none}}

## Links

- Intent: [[../intent]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
