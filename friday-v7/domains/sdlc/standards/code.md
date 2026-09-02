# Code standard

How Friday writes code. Not audit, not Design capacity, not review scores.
Load on implement/fix **full path** before the first edit. S uses Ready-light boxes only.

## Fit

Match neighbors (naming, layer, errors, tests). Absorb/extend — no new pattern the repo lacks. No drive-by.

## Maintain

One job at the **existing** seam. Blast radius = Plan Lock touch set. Names from domain/Design; no `Util` dump. Names must not hide I/O/mutate/enqueue. New state lives with the current owner. Comments = why or Design cite.

## Test

Logic callable without the whole app. Inject I/O, clock, random, clients. Cover DoD + dominant risk. Untestable seam → split first.

## Scale / cost

No cache/queue/shard/pool unless Design locked it. No hidden single-writer globals. Policy does not import infra — use existing ports. No I/O in a loop unless Design locked batching. Expensive calls stay visible.

## Not Uncle Bob as SoT

Borrow visible side effects and the dependency rule. No function line cap, no mandatory Clean Architecture rings.

## Self-check

Fits neighbors · no new god unit · honest names · why-comments only · test seam for the risk · no policy→infra · no I/O-in-loop · no unlocked scale infra · no drive-by.
Any fail → fix the diff before Done.
