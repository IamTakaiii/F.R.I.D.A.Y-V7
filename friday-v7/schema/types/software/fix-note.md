---
type: fix-note
id: "{{project_slug}}.feat.{{feature_id}}.fix.{{slug}}"
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
<!-- fill: Symptom, Root cause, Fix, Verification · omit: Links if none -->
# Fix — {{title}}

## Symptom

{{what the user saw}}

## Root cause

{{path + why}}

## Fix

{{what changed}}

## Verification

{{command + result}}

## Regression guard

{{test or "none — typo"}}

## Links

- Intent: [[../intent]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
