# SDLC — sync

Docs ↔ code. **scope:** `feature` (default) or `project` (former drift-radar).

## Feature scope

Read `design.md` + matching code. List: in Design not in code · in code not in Design · both but different. Each row: path · severity `info|drift` · suggested fix (docs or code — do not silently patch both).

## Project scope

Scan Feature List vs folders vs Overview. Flag orphan Design, missing intent, queue without feature, Arch/ADR stubs. Same severity model. Not a scored review.

## Persist

Persist only if asked: type `note` at `89-Notes/Notes/YYYY-MM-DD - Drift.md`. Chat table is enough for a small feature sync.

## Next

Docs wrong → `/fr-write` or `/fr-design`. Code wrong → `/fr-implement` or `/fr-fix`. Do not implement in this mode.
