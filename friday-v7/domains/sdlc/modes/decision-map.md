# SDLC — decision map

Plan work too large or uncertain for one session as a map of **decisions**, not premature implementation tasks. Writes: `decision-map` + `decision-ticket`.

## Concepts

| Term | Meaning |
|---|---|
| Destination | The spec, decision, or state that means navigation is finished. Fixes scope. |
| Decision ticket | One precise question resolvable within one fresh context. |
| Frontier | Open, unblocked, unclaimed tickets that can be worked now. |
| Fog | In-scope territory known to matter but not yet precise enough to phrase as a ticket. |
| Out of scope | Beyond the destination; never graduates unless the destination changes. |

**Fog or ticket:** can the question be stated precisely now? Ability to answer it is irrelevant.

## Chart

1. Grill to name the Destination first.
2. Map breadth-first: current frontier, blockers, and fog. No fog and fits one session → stop; use Design instead.
3. Write one map as the index; decisions live only in tickets. Never duplicate their bodies into the map.
4. Create tickets, then wire blocker IDs in a second pass.
5. Classify each: `research` (AFK fact) · `experiment` (HITL concrete artifact) · `discussion` (HITL decision) · `prerequisite` (work that only unlocks a decision).

## Work the map

One non-research ticket per session.

1. Read the low-resolution map, not every ticket.
2. Pick the first frontier ticket unless the user names one; claim before work.
3. Resolve with research, design experiment, or grill as its type requires. HITL questions are never answered by the agent.
4. Record the answer on the ticket, close it, add one linked gist under Decisions so far.
5. Recompute: create newly-visible tickets, graduate sharpened fog, remove invalidated tickets, and move beyond-destination work to Out of scope.

Map is done when the frontier and fog are empty and the Destination can be handed to delivery planning.
