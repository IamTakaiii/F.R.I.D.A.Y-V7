# SDLC — design twice

First idea is unlikely to be the best (Ousterhout). Run at **Decide**, after the grill closes.

Tier L, irreversible shape, or the user asked → offer it. Tier M → only on request. Tier S → never.

## Frame first

One short block to the user before spawning: constraints any interface must satisfy · dependency category (in-process · local-substitutable · remote-but-owned · true-external) · one rough sketch that makes the constraints concrete — **a sketch, not a proposal**.

Then proceed immediately. The user reads while the agents work.

## Spawn

3–4 parallel subagents (`kernel/extras/subagent.md`, design-twice exception). Each gets a technical brief — paths, coupling, dependency category, what sits behind the seam, project glossary terms — and **one different constraint**:

| Agent | Constraint |
|---|---|
| A | Minimize the interface — 1–3 entry points, maximum leverage each |
| B | Maximize flexibility — many use cases, room to extend |
| C | Optimize the common caller — the default case is trivial |
| D | Ports and adapters — only if a seam crosses a process or network |

Each returns: interface (types · invariants · ordering · error modes) · a caller usage example · what stays hidden behind the seam · dependency and adapter strategy · trade-offs, including where leverage is thin.

## Compare

Present them one at a time, then contrast in prose on **depth** (behaviour per unit of interface a caller must learn), **locality** (where change concentrates), and **seam placement**.

Then recommend one and mean it. Combine designs into a hybrid if the pieces fit. A menu with no pick is a failed run.

Output feeds Decide. Design twice does not lock.
