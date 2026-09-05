---
type: work-item
id: "{{project_slug}}.feat.{{feature_id}}.todo.{{todo_id}}"
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
todo_id: "{{todo_id}}"
delivery: todo
---
<!-- fill: Outcome and DoD, Verification · omit: Blocked by if none · omit: Plan lock unless Full · omit: What shipped / Evidence until Done · omit: Links if none -->
# TODO-{{todo_id}} — {{title}}

## Outcome and DoD

- Outcome: {{what changes}}
- Done when: {{checkable}}
- Invariant: {{Design cite or omit this bullet}}

## Blocked by

- {{work-item id and why it genuinely gates this item}}

## What shipped

{{when Done: what was built, in order — not a restatement of Outcome}}

## Plan lock

{{touch set · sequence · stop — Full path only}}

## Verification

| DoD / risk | Evidence | Result |
|---|---|---|
| {{item}} | {{cmd or path}} | {{pass\|fail\|not-run}} |

## Evidence

**Done · Where · Verify · Left**

{{paths · leftover stubs}}

## Links

- Intent: [[../intent]]

## Doc history

| Date | Rev | Change | Why |
|---|---|---|---|
| {{date}} | 1 | Initial | |
