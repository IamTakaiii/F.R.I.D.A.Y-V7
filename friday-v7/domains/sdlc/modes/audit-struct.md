# SDLC — audit-struct

Structure audit of the **vault project**. Plan-first. Persist only in the vault.

## Read

Folder numbers vs `schema/placement.md`. Feature folders: `intent.md` / `design.md` / `queue.md`. Overview + Arch + Decisions present?

## Ledger

Scope rule: `kernel/runtime.md`. Every item in Read returns one row — `clean` + cited path, or a finding. Silent item = not checked.
Severity: the `artifact` column of `../standards/review.md`. Do not invent a second scale.
Re-run: read the newest prior `audit-plan` for this scope first. New finding needs a reason · gone finding needs `fixed` or `withdrawn`.

## Card (≤80)

Findings (path + what’s wrong + severity). Keep vs merge vs move. Order of work (smallest first).

## Persist

Type `audit-plan` → project `00 - Overview/` or `{F}/plans/` (`schema/placement.md`). Record scope + profile + the ledger. **Never** write `{agent_root}/docs/` or skill-tree docs.

## Next

User accepts plan → `/fr-write` or `/fr-design` / consolidate. This mode does not move files unless asked in a follow-up.
