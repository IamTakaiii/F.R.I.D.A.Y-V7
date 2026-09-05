# Domain: Internal Tool

Internal CLI/script/ops helpers — not product SDLC.

**Load:** `kernel/runtime.md` → this file → **one** `modes/*.md`.
Writes to vault: `kernel/io/write.md` + `schema/write-gate.md` — same type/path/template as every other domain.
Writes: `kernel/io/write.md`. Vault: `kernel/brain/port.md` + `schema/`.

## Modes
| Mode | File |
|---|---|
| orient | `modes/orient.md` |
| shape | `modes/shape.md` |
| build | `modes/build.md` |
| harden | `modes/harden.md` |

## Catalog (optional)

Recording a finished tool is a line, not a mode: prefer a one-liner in the existing `scripts/README`, `tools/README`, or Makefile. Handoff Tools row only if `{agent_root}` exists (write-gate; never silent). Vault `note` only on ask — do not invent folder trees. No secrets. Slug exists → update in place.



## Done
Cite paths for durable work. Artifact caps apply when writing vault types.
