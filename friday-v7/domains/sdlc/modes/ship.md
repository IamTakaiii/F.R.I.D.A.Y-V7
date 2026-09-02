# SDLC — ship

Go / no-go before a release claim. Verdict from `../gates/ship.md`.

## Read

Named commits/tags/queue ids. Design in scope. Latest `/fr-test` (or verify) result. `06 - Ship/` checklist if it exists. High-risk: latest code review PASS.

## Card (≤80)

What ships. Failed must-gates. Conditions the user must own in writing. Rollback + smoke (named, not pasted secrets).

## Persist

Checklist → `ship-checklist` at `06 - Ship/YYYY-MM-DD - Ship.md`. After a real ship (user/env did it): `release-notes` at `06 - Ship/YYYY-MM-DD - Release Notes.md`.

## Verdict

`go` · `go_with_conditions` · `no-go`. Never claim deployed without user/env action.
