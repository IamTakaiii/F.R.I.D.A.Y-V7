# Artifact contract

A file is compliant only when type, path, frontmatter, required sections, cap, and history pass. Procedure: `write-gate.md`.

## Frontmatter

```yaml
type: <registered>
id: <stable>
project: <name>
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft|current|superseded|archived
rev: <int>
lifecycle: delivery|decision|lab|ship|note|personal
tags: []
standard: 7
max_lines: 200
parts: []
```

Also: feature files → `feature`, `feature_id`, `depends_on`. API → `resource`. quality-report → `kind` + `result`. brief → `project_kind`. work-item → `todo_id` + `delivery`.

No `TBD` in YAML. No `doc_status`. No `load_profile`. Headings English.

`parts[]` may stay `[]`. If `## Parts` exists, YAML `parts[]` must match that table. Click SoT is `## Parts`, not YAML.

## Card + parts + links

Card = current answer.

**Lazy-load:** Design parts `contracts` · `flow` · `quality` · `operations`. Architecture part `stack` only. No other type has parts. Never `stem - Heading.md`.

**Flow part:** bound + numbered ` ```text` ` sequence + ` ```mermaid` ` (sequenceDiagram or flowchart) + fail/next. Both text and diagram required.

**Click:** `[[wikilink]]` only. Never `[[.]]`. Never mid-dot lists.

| Heading | Role |
|---|---|
| `## Parts` | Wikilink table matching `parts[]`. Omit if none. |
| `## Links` | Last body section, immediately before `Doc history`. One `- Kind: [[path]]` per target. |

**Hub:** `intent.md` lists the feature package. Other feature files link `Intent` only. Design parts also link `Design`. Project hub is `01 - Brief.md`. No `00 - Index.md`.

## Caps

`max_lines: 200` default. `max_lines: 0` = unlimited — `timeline-log`, `memory-lesson`, and any file under `90 - Log/`.

Count **body only**: after YAML, excluding `## Links` and `## Doc history`. Skip the count when `max_lines` is `0`. Runtime read slice (lean ≤80) is not a write cap.

Over = failed write unless a registered split applies.

## Split

When over cap, in order:

1. Cut filler (`thinking/prose.md`). Omit empty optional sections.
2. Registered parts only: design → `design/{contracts,flow,quality,operations}.md`; architecture → `stack.md`; queue row detail → `work/`.
3. Keep `Doc history` on the card (last 5 rows). Do not split history.
4. Still over → failed write. Rewrite denser. Do not invent siblings.

## Read

Frontmatter + first required section. Follow `## Parts` / `parts[]` only as needed. Skip Links and history unless navigating.

Read `status` and `updated` before using the content, every time:

| Found | Do |
|---|---|
| `status: superseded` or `archived` | Not truth. Find the successor, or ask. Never quote it as current |
| `status: draft` | Usable as intent only, never as a contract |
| `status: current`, code not opened | Quote as `Unverified(<updated>)` |
| `status: current`, code opened, agrees | Use it. Cite both |
| `status: current`, code opened, disagrees | Conflict. Code = current behavior · artifact = intended behavior. Report it; `/fr-sdlc` sync owns the repair |

Age alone never makes a card wrong, and a recent `updated` never makes it right — only checking against code does.

## Retired

`design-slice` · `policy-cost-spike` · `todo` · `work-log` · `slice-log` · `lab` · `guide` · vault `httpyac` · `load_profile` · `project-brief` · `personal-brief` · `personal-note` · `review` · `test-report` · `perf-report` · `stack`
