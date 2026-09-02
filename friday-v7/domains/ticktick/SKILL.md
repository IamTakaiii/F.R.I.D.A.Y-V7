# Domain: TickTick

TickTick execution queue with controlled Vault sync.

**Load:** `kernel/runtime.md` → this file → **one** `modes/*.md`.
Writes to vault: `kernel/io/write.md` + `schema/write-gate.md` — same type/path/template as every other domain.
Writes: `kernel/io/write.md`. Vault: `kernel/brain/port.md` + `schema/`.

## Modes
| Mode | File |
|---|---|
| init | `modes/init.md` |
| setup | `modes/setup.md` |
| manage | `modes/manage.md` |
| sync | `modes/sync.md` |
| review | `modes/review.md` |
| describe | `modes/describe.md` |
| schedule | `modes/schedule.md` |

Vault owns roadmap; TickTick owns dates/reminders. Titles stay natural language.



## Done
Cite paths for durable work. Artifact caps apply when writing vault types.
