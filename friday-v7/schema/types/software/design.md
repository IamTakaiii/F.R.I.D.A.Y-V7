---
type: design
id: "{{project_slug}}.feat.{{feature_id}}.design"
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
<!-- fill: Executive decision, Problem, Success and scope, Decision, Verification plan · omit: Parts unless parts[] is set · omit: Links if none -->
# Design — {{feature}}

## Executive decision

{{outcome · approach · why it wins · main trade-off}}

## Problem

{{who hurts · what breaks · why now}}

## Success and scope

| Success | Mechanism | Evidence |
|---|---|---|
| {{criterion}} | {{how}} | {{test or signal}} |

### Non-goals

{{omit this heading if none}}

### Constraints

{{omit this heading if none}}

## Decision

{{chosen option · Architecture fit · ports}}

## Verification plan

| Requirement / risk | Kind | Evidence |
|---|---|---|
| {{DoD or risk}} | {{happy\|error\|edge}} | {{cmd or signal}} |

## Parts

| Kind | Path |
|---|---|
| {{contracts\|flow\|quality\|operations}} | [[design/{{kind}}]] |

## Links

- Intent: [[intent]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
