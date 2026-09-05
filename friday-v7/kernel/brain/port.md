# Friday v7 — Brain Port

Storage-agnostic API. **This file is the only brain-default SoT.** Obsidian is optional.

## Resolve (first hit wins)

1. Env `FRIDAY_BRAIN_ROOT` if the directory exists → root. Backend: `FRIDAY_BRAIN_BACKEND` if set, else prefs/`brain.backend`, else `obsidian` only when `<root>/.obsidian/` exists, else `local`
2. Project `{agent_root}/preferences.md` if already resolved (`brain.backend` + `brain.root`)
3. Skill / AGENTS (`brain.backend` + `brain.root`; alias `obsidian_vault` is Obsidian-only)
4. Fallback `~/.local/share/friday/` with `brain.backend: local` — create only on first approved durable write

No config and no `.obsidian/` → `local`. Never infer Obsidian from a markdown folder alone. Never override an explicit `local` because a vault exists elsewhere.

| `brain.backend` | Adapter |
|---|---|
| `local` / `local-fs` / `fs` | `adapters/local-fs.md` |
| `obsidian` | `adapters/obsidian.md` |

Expand `~/` and `$HOME`. Load **one** adapter. Do not require `.agent` to open the brain. Do not require the Obsidian app.

## Operations

`resolve_root` · `read_slice` · `write` · `patch` · `list` · `link`

## Rules

- Domains never `if obsidian` — only port + adapter.
- Reads are first-class: every mode may use the configured brain for relevant context. Resolve the root before declaring a source, fact, intent, or prior artifact absent; bounded lookup is required, whole-vault enumeration is not.
- Slice reads (runtime budget). Artifacts: frontmatter + card first, then `parts[]` (`schema/artifact.md`).
- New folder → no `00 - Index.md`.
- Layout SoT: `schema/vault.md`. Same map for every backend.
