# SDLC — summary (brief)

Read-only news card for **one** software feature + its Design. No vault write unless the user asks `/fr-write`.

## Read

`intent.md` + `design.md` only. If Design is missing, say so and stop (or route `/fr-design`). Do not invent from chat.

## Card (≤80)

```
## Feature
What users can do · what they get · why it exists
## Design
How it works (1–3 lines) · important limits · open risks
## Status
intent / design / queue / shipped — from files only
```

Use `Not stated in Design` instead of guessing. Cite vault paths. Not a scored review (`/fr-review`). Not a four-view timeline (`/fr-sdlc` + timeline).
