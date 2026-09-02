# SDLC — init-agent

**Opt-in.** Create `.agent` for handoff / prefs / httpyac home. Most work does not need it.

## Steps

1. Confirm repo root and that the user wants `.agent` here.
2. Existing? Report vs v7 shape; repair only with approval.
3. Primary checkout: `index.md` + `preferences.md` from `hosts/cursor/agent-templates/`. Keep `memory.*` at `propose`, not auto-handoff.
4. Linked git worktree: reuse primary `.agent`; do not copy handoff focus into primary.
5. Git handling — ask: `local-ignore` (`.git/info/exclude`) or `track`. Never silently rewrite `.gitignore`.
6. Link `brain_project` if known.

## Done

Primary has a usable config root. State the Git choice. Ops only — not a Design store.
