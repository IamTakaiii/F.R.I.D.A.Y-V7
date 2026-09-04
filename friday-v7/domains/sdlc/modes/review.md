# SDLC — review

Pair review. `/fr-pr` = this + `git log`/`diff` (do not invent the range).
Bar lives in `../standards/review.md`. **Score only after hunt. Deep always when scoring.**
`deep` / `เข้มงวด` = specialist spawn only; same bar.

Do not implement. After must-fix → `/fr-fix`. Do not load ship.

## Pulse

```
T0  Track (from named paths only) + deep? → user restates 1 line
T1  Scope lock (≤6 paths) + prior report for that scope
T2  Hunt vs Intent/Design/DoD → ledger. Ask only if clash or ambiguous bug → restate 1 line
T3  review.deep.md → score that track
T4  One verdict block (scope · ledger · findings)
T5  quality-report if they want a file
```

**Panel:** offer once at T2. Accepted → `modes/panel.md` before T3. Panel findings still get scored here; panel never scores.
- default: `skip` or N (2–5)
- deep: `skip` · `3` · `5` only — do not offer generic N
Roles = first N of the review catalog (`kernel/thinking/brainstorm.md`).

## Scope lock

Scope rule: `kernel/runtime.md`. PR → the `git diff` range, never invent.
Re-review of the same target: read the newest `reports/` for that scope first. New finding needs a reason · dropped finding needs `fixed` or `withdrawn`. Scope or profile changed → say so; runs are not comparable.

## Ledger

Every lens (code) or dim (artifact, general) emits one row before scoring: `clean` + cited path, or finding ids.
Silent row = unread scope = FAIL. Ledger is what re-runs are compared on — not the %.

Whole folder = two sessions (code, then artifact). Challenge: hold / withdraw / refine — then rescore that track.
