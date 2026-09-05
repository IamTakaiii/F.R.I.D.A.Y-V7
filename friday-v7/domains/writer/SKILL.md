# Domain: Writer

Clear shareable documents. Headings English. Types live in `schema/` — no writer-owned release-notes twin.

**Load:** `kernel/runtime.md` → this file → **one** `modes/*.md`.
Writes to vault: `kernel/io/write.md` + `schema/write-gate.md` — same type/path/template as every other domain.
Writes: `kernel/io/write.md`. Vault: `kernel/brain/port.md` + `schema/`.

## Modes
| Mode | File |
|---|---|
| note | `modes/note.md` |
| brief | `modes/brief.md` |
| spec | `modes/spec.md` |
| present | `modes/present.md` |
| polish | `modes/polish.md` |
| release-notes | `modes/release-notes.md` |

Destination defaults: Knowledge notes · `40 - Writing/` for briefs/specs/presentations · Ship for release notes.

## Before the mode

Name outcome · audience (self · teammate · stakeholder · external · class) · sources (vault path, paste, or chat-only) · sink (chat vs `schema/placement.md`) · length (card ≤80 unless the type cap is higher). At most one blocking question.
Which mode is the router's job (`ROUTING.md`) — this domain keeps no second classification table.
Not here: software ADR → `/fr-sdlc` decision · feature news card → `/fr-sdlc` summary · personal decision → `/fr-life`.

## Done
Cite paths for durable work. Artifact caps apply when writing vault types.
