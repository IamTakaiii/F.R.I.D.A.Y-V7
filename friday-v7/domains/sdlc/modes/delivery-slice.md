# SDLC — delivery slice

Turn a locked Design into agent-sized, end-to-end work. Writes: `queue` + `work-item`. This is not a layer checklist.

## Slice

Each item is a **tracer bullet**:

- One narrow but complete path through every applicable layer — data, contract, behavior, UI, verification.
- Demoable or independently verifiable when done.
- Fits one fresh agent context.
- Uses project glossary terms; respects ADRs.
- Declares every blocker; no blocker means `ready`.

Look for a small prefactor first: make the change easy, then make the easy change. Prefactor is its own item only when it stays green and independently verifiable.

## Wide change exception

A mechanical change whose blast radius cannot land as a vertical slice uses **expand → migrate → contract**:

1. Expand: add the new form beside the old; keep callers green.
2. Migrate: batches by package/directory, each blocked by expand and independently green.
3. Contract: remove the old form; blocked by every migration batch.

If batches cannot stay green alone, use a named integration branch and a final integrate-and-verify item. Do not pretend each batch shipped safely.

## Dependency graph

Put blockers in `work-item.depends_on`; queue order is blocker-first. The live frontier is every `ready` item whose blockers are done. `next`/`ready` remains ≤5 — later items stay in the plan, not a fake active queue.

## Lock

Show numbered items: Title · Blocked by · End-to-end outcome · DoD. Ask whether granularity and edges are right; merge/split until the user names the lock.

Then write one `work-item` per approved slice and update `queue`. Specific file paths belong in implementation Plan Lock, not in the slice.
