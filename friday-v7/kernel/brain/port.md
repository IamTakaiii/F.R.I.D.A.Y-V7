# Friday v7 — Brain Port

Storage-agnostic API. **This file is the only brain-default SoT.**

## Resolve (first hit wins)

1. Env `FRIDAY_BRAIN_ROOT` if the directory exists → root; backend from prefs, else `local` unless the path looks like an Obsidian vault
2. Project `{agent_root}/preferences.md` if already resolved
3. Skill / AGENTS (`brain.backend` + `brain.root`; alias `obsidian_vault`)
4. Fallback `~/.local/share/friday/` with `brain.backend: local` — create only on first approved durable write

Prefer `obsidian` when configured and the vault exists.

| `brain.backend` | Adapter |
|---|---|
| `obsidian` | `adapters/obsidian.md` |
| `local` / `local-fs` / `fs` | `adapters/local-fs.md` |

Expand `~/` and `$HOME`. Load **one** adapter. Do not require `.agent` to open the brain.

## Operations

`resolve_root` · `read_slice` · `write` · `patch` · `list` · `link`

## Rules

- Domains never `if obsidian` — only port + adapter.
- Slice reads (runtime budget). Artifacts: frontmatter + card first, then `parts[]` (`schema/artifact.md`).
- New folder → no `00 - Index.md`.
- Layout SoT: `schema/vault.md`.
