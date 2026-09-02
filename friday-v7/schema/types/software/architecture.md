---
type: architecture
id: "{{project_slug}}.arch"
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
<!-- fill: Context, Containers, Cross-cutting rules · omit: Picture, Tech stack, Open questions if none · omit: Links if none -->
# Architecture — {{project}}

## Context

{{system boundary}}

## Picture

```mermaid
flowchart LR
  {{A}} --> {{B}}
```

## Containers

{{runtime pieces}}

## Key flows

{{2–4 hops — feature Design owns the rest}}

## Tech stack

{{short pins · overflow → architecture-part stack}}

## Cross-cutting rules

{{auth · data · errors}}

## Feature constraints

{{what every feature must obey}}

## Open questions

| Q | Owner | Decide by |
|---|---|---|
| {{}} | {{}} | {{date}} |

## Parts

| Kind | Path |
|---|---|
| stack | [[stack]] |

## Links

- Brief: [[../00 - Overview/01 - Brief]]
- Feature List: [[../00 - Overview/02 - Feature List]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
