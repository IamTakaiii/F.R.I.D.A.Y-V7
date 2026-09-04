# SDLC — sync

Docs ↔ code. **scope:** `feature` (default) or `project` (former drift-radar).

## Feature scope

Read `design.md` + matching code. List: in Design not in code · in code not in Design · both but different. Each row: path · kind `info|drift` · suggested fix (docs or code — do not silently patch both).

## Project scope

Scan Feature List vs folders vs Overview. Flag orphan Design, missing intent, queue without feature, Arch/ADR stubs. Same kind model. Not a scored review.

## Ledger

Scope rule: `kernel/runtime.md`. Every checked item returns one row — `clean` + cited path, or a drift row. Silent item = not checked.
Re-run: read the newest prior record for this scope first. New row needs a reason · gone row needs `fixed` or `withdrawn`.

## Persist

Type `note` at `89-Notes/Notes/YYYY-MM-DD - Drift.md`. Record scope + profile + the ledger, not only the drift rows.
Project scope → always propose the record. Feature scope → chat table is fine, but say plainly that the next run will have nothing to diff against.

## Next

Docs wrong → `/fr-write` or `/fr-design`. Code wrong → `/fr-implement` or `/fr-fix`. Do not implement in this mode.
