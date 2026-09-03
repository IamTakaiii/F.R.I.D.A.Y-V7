# Pipelines

SoT for `/fr-pipe`. Add a row to add a recipe. Runner: `domains/sdlc/modes/pipe.md`.

| name | beats | halt | N | alias |
|---|---|---|---|---|
| quality | `/fr-review` → `/fr-fix` → `/fr-test` | review PASS (L5) + must-fix empty + test green | 3 | วนจนผ่าน |

Beats are existing surfaces only. Sequential roles, never parallel. Confirm one line before run. Reports: child modes, halt round only. `/fr-ship` is never a beat.
