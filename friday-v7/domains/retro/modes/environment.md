# Retro — environment

Improve the **agent environment** after a named session; do not merely summarize feelings. Default to this conversation. Read primary session evidence only — no invented history. Never auto-run or silently promote Memory.

## Hunt

| Candidate | Signal | Prefer |
|---|---|---|
| Navigation | Time lost finding truth; hidden file relationship | Small pointer to the owning doc |
| Automated check | Agent mistake was mechanically detectable | Lint, type, test, schema, filesystem check |
| Review standard | Reviewer missed a consequential mistake | Rule in reviewer-loaded standards |
| Global steering | AGENTS instructions are long or specialized | Keep only pointers globally; move detail to standards/skills |
| Tool economy | Expensive calls, large output, repeated lookup | Narrow command, helper, cache, or better adapter |
| No-op rule | Instruction did not change observed behavior | Clarify, automate, or delete |
| Information access | Crucial logs/service facts unavailable | Read-only access, captured artifact, tee logs |

Also record: went well (1–3) · hurt/slow (1–3) · wrong assumptions · failed gates · missing verification.

## Ownership

Implementation bears exploration, edits, and debugging, so its context pressure is highest. Review receives a diff and has more room. Put enforceable coding standards on review unless implementation needs the rule to avoid irreversible harm. Prefer automated checks over prose whenever possible.

## Output

Rank candidates by consequence. Each: evidence from the session · recurrence risk · smallest environment change · verification that proves improvement · owner.

Recommend **one** next change; do not silently edit steering, standards, hooks, or tools. Optional save: `note` at the governed retro path. `memory-lesson` only when the user explicitly promotes it.
