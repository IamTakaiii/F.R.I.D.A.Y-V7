# Friday v7 — Memory

Load only on: session close extract · recall trigger · explicit remember.

```
extract → propose → commit(approve) → store
                 recall → budgeted inject
```

Default propose-only. No silent lesson/knowledge/skill. `handoff-auto` may write handoff only.

| Layer | Store | Gate |
|---|---|---|
| `handoff` | `{agent_root}/index.md` | propose · optional auto |
| `lesson` | `type: memory-lesson` | approve |
| `knowledge` | `30 - Knowledge/` | approve |
| `skill` | `docs/skill-drafts/` | approve |

Candidates need: `id` · `layer` · `claim` · `evidence` · `scope` · `confidence` · `suggested_path`.  
Reject: no evidence · secrets · non-actionable.

Recall inject stays inside runtime budget.
