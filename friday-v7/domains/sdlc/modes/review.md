# SDLC — review

Pair review. `/fr-pr` = this + `git log`/`diff` (do not invent the range).
Bar lives in `../standards/review.md`. **Score only after hunt. Deep always when scoring.**

Do not implement. After must-fix → `/fr-fix`. Do not load ship.

## Pulse

```
T0  Track (from named paths only) + chat language → user restates 1 line
T1  Read scope (≤6 paths)
T2  Hunt vs Intent/Design/DoD. Ask only if clash or ambiguous bug → restate 1 line
T3  review.deep.md → score that track
T4  One verdict block
T5  quality-report if they want a file
```

**Panel:** offer once at T2 — `skip` or N (2–5). Accepted → `modes/panel.md` before T3. Panel findings still get scored here; panel never scores.

Whole folder = two sessions (code, then artifact). Challenge: hold / withdraw / refine — then rescore that track.
