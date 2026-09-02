# Vault layout (v7)

Numbers are **fixed**. Do not shift Ship because Labs exists. Do not invent folders.

```
00 - Meta/
10 - Inbox/
20 - Projects/
  10 - Software/
    NN - <Project>/
      00 - Overview/          # brief, feature-list, timeline logs
      01 - Architecture/      # architecture + stack part
      02 - Decisions/         # adr only
      03 - Features/
        NN - <slug>/
          intent.md
          design.md
          design/             # registered parts only
          queue.md
          api/
          work/
          fixes/
          reports/
          plans/
      04 - Data/
        01 - Model/
        02 - Dictionary/
      05 - Labs/              # create only when used
      06 - Ship/
      07 - Operations/
      89-Notes/Notes/         # project-local notes
      90 - Log/               # memory-lesson
  20 - Personal/
    NN - <Project>/
      00 - Overview/          # 01 - Brief.md · 02 - Goals.md
      01 - Plan/
      02 - Tasks/
      03 - Decisions/
      04 - Research/
      05 - Risk/
      06 - Outcomes/
      30 - Budget/
      90 - Log/               # note
30 - Knowledge/
40 - Writing/                 # dated `note` only — not a second Design
90 - Archive/
```

## Rules

- No `00 - Index.md`. No Threads folder.
- Companion folders (`api/`, `work/`, `fixes/`, `reports/`, `plans/`, `design/`, `05 - Labs/`) are created **with the first file only**.
- Feature files use unnumbered names so they do not collide with `api/` / `work/`.
- Project-specific notes: `<project>/89-Notes/Notes/`. Cross-project knowledge: `30 - Knowledge/`.
- Software vs personal: kind is the folder. Personal projects do not use Feature/Design/Ship unless the user adds a software track.
- Exact filenames: `schema/placement.md`. Tree here is the folder map only.


## Timeline files (Overview, registered names)

| File | Role |
|---|---|
| `04 - production feature log.md` | shipped feature timeline |
| `05 - development feature log.md` | in-progress feature timeline |
| `06 - production change log.md` | shipped change timeline |
| `07 - development change log.md` | in-progress change timeline |

Type: `timeline-log`. Do not invent a floating `timeline` type.
