---
type: design-part
id: "{{project_slug}}.feat.{{feature_id}}.design.{{part_kind}}"
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
part_kind: contracts
---
<!-- fill: Content · omit: Links if none · part_kind: contracts|flow|quality|operations -->
# Design part — {{part_kind}}

## Content

{{contracts/quality/operations: this kind only · HTTP fields live in api/}}

{{flow only — all four, in order:
1. one-line bound (does / does not)
2. numbered ```text``` sequence
3. ```mermaid``` sequenceDiagram or flowchart (≥3 hops)
4. one-line fail + who runs next
No ## Picture. No "this part owns".}}

## Links

- Intent: [[../intent]]
- Design: [[../design]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
