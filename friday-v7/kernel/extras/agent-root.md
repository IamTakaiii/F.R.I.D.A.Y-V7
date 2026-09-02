# Friday v7 — Agent root (`.agent/`)

Optional. Missing is normal — do not nag.

| Concern | Where |
|---|---|
| Resume handoff | `{agent_root}/index.md` — Focus/Done/Next/Blocked |
| Prefs | `{agent_root}/preferences.md` |
| httpyac | `{agent_root}/httpyac/<feature-slug>/` |
| Product docs | vault only — never `.agent` as Design store |

If inject `FRIDAY_AGENT_ROOT` is present, use it. Do not re-search.

Resolve: cwd `.agent` → walk up ≤12 → home scan ≤2 → optional `~/` workspace map → one level down → else `none`.
