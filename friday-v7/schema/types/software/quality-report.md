---
type: quality-report
id: "{{project_slug}}.feat.{{feature_id}}.qa.{{kind}}.{{date}}"
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
kind: review
result: "{{result}}"
---
<!-- fill: Scope and verdict, Findings · kind: review|test|perf · filename must match kind · omit: Links if none -->
# {{kind}} — {{date}}

## Scope and verdict

{{locked path list or diff range}} · **{{PASS\|FAIL}}** · {{result}}

## Scores or bounds

{{review: C*/T*/G* · test: contracts hit · perf: metric / Design bound / measured}}

{{review only — ledger, one row per lens or dim}}

| Lens/Dim | Result | Cite |
|---|---|---|
| {{id}} | {{clean\|finding ids}} | {{path}} |

## Findings

| ID | Sev | Path | Why | Next |
|---|---|---|---|---|
| {{n}} | {{blocker\|major\|minor}} | {{file}} | {{hurt}} | {{fix}} |

## Must fix

{{or "none"}}

## What's solid

{{one line}}

## Links

- Intent: [[../intent]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
