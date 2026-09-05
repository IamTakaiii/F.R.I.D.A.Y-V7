# Friday v7 — Phase boundary

A **phase** is one chunk of work inside a session — the grill, the capture, the implementation, the QA. It ends when "that's done with".

Decide continuity **only at the boundary**. Mid-phase there is no decision: continue, or split what is left. Cutting context mid-phase loses the thread.

## First yes wins

| # | Ask | Then |
|---|---|---|
| 1 | Does the next phase need this one as a **primary source**, or does it still fit the budget? | **Continue.** Costs nothing, loses nothing. Grill → Decide → Capture → Implement is the standard yes: implementation wants the reasoning verbatim, not a summary of it. |
| 2 | Is everything here — exploration, dead ends, decisions — disposable? | **`/new`.** Cheapest move on the board; the old session stays resumable. |
| 3 | Is anything **travelling** — new harness, new repo, a colleague, or a side task found mid-phase? | **Handoff** (`extras/agent-root.md`). Portability is the only thing it buys. |
| 4 | Can the rest run with the user away from the keyboard, no steering? | **Subagent** (`extras/subagent.md`). |
| 5 | Otherwise | **Compact**, with an instruction naming the next phase. |

## Cost

Every move except Continue turns a primary source into a secondary one — less noise and more room, but lossy. Pay that only when staying costs more than it saves.

Clearing a **relevant** context is one-way. Reading the diff back never returns the *why*.

Compact is the default landing spot, not the first reach: the four questions above it are cheaper or more precise. The failure mode of starting at compact is a fresh session confidently wrong about a decision the summary flattened.
