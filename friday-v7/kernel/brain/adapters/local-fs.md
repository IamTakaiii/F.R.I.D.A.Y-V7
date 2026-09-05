# Adapter — Local FS

Default backend. No Obsidian app, vault, or MCP.

`brain.backend`: `local` / `local-fs` / `fs`. Default root: `~/.local/share/friday/`. Any existing directory is valid if set as `brain.root` or `FRIDAY_BRAIN_ROOT`.

Same folder map as `schema/vault.md`. Filesystem tools only. Create the default root only on the first approved durable write.

`[[wikilink]]` is a vault-relative path (D21). Resolve it on disk; do not require an Obsidian click-handler.
