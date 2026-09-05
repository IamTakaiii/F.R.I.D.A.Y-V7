# Friday v7 — Subagent

**Default: do not spawn.** Parent uses Grep/Glob/Read.

Spawn only when all hold: XL scope (≥2 distant trees) · read-only or write-disjoint · user asked or XL justification · concurrent ≤ prefs (default 0).

Panel beat (`thinking/brainstorm.md`) is separate: user opted (`/fr-panel` or accepted offer) · N 2–5 · not XL explore.
Pipe beat (`domains/sdlc/modes/pipe.md`) is separate: user issued `/fr-pipe` · host sessions per beat · not XL explore.

## Named exceptions

| Beat | Allowed |
|---|---|
| Grill fact-find (`domains/sdlc/modes/design.grill.md`) | ≤2 concurrent, **including `lean`**. Read-only fact lookup. Never carries a question to the user. Frontier keeps moving while it runs. |
| Design twice (`domains/sdlc/modes/design.twice.md`) | 3–4 concurrent. Tier L, irreversible, or user asked. Read-only; output is proposals, not writes. |
| Review hunts (`domains/sdlc/modes/review.md` T2) | Exactly 2 — standards and spec — on the same locked scope. Read-only, ≤400 words each, separate contexts on purpose. They hunt; the parent scores. |

Both report to the parent. Neither locks anything.
