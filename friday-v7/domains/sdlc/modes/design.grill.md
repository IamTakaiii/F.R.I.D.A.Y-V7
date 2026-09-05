# SDLC — design grill

Load at Discover on **every** `/fr-design`. Interrogate until the design tree has no unvisited branch, then design.

Grill owns the **problem space and the decision tree**. `design.deep.md` owns the solution lenses — do not ask its must-checks here.

## Design tree

Every answer branches into the decisions that hang off it.

**Frontier** = every decision whose prerequisites are already settled — what can be asked *now* without guessing at answers not yet heard. Ask the **whole frontier in one round**, then wait. A question whose answer depends on another question still open this round belongs to a **later** round.

Each round: answers settle branches → the frontier pushes outward → recompute → next round.

## Round format

```
❓ **Q1 — <title>**
<what turns on this · 2–4 concrete choices>
➡️ <the answer you'd bet on, and why in one line>
```

Numbering runs across the whole grill (Q1…Qn, never restart). The user may answer by number. Cap ~6 per round — more than that means the frontier is wrong, split it.

## Facts vs decisions

| Kind | Whose job |
|---|---|
| **Facts** — what the code, vault, config, or dependency already does | **Yours.** Never ask. Find it, then state it as one confirmed line. |
| **Decisions** — what should be true | **The user's.** Always ask. Never assume-and-continue. |

A missing fact blocks only its own branch: dispatch fact-finding (`kernel/extras/subagent.md`, grill exception — allowed in `lean`) and **keep going**. Ask the rest of the frontier now; mark the waiting ones `pending fact`.

Asking for something you could have looked up = the grill failed.

## Rules

| # | Rule |
|---|---|
| R1 | Recommend, never survey. Every question carries the answer you'd bet on. |
| R2 | Vague answer → **one** narrowing follow-up (ask for a number, a name, or a case), then `Assumed` + owner. Never move on quietly. |
| R3 | Restate each answer as one concrete claim. An unconfirmed restatement is not recorded. |
| R4 | No design during grill — no options, no architecture, no file names. That is Decide. |
| R5 | Contradiction with a card, the code, or an earlier answer → surface it now, name both sides, never merge. |
| R6 | Nothing silently assumed. Every `Assumed` carries an owner and a date. |

## Coverage floor

Seeds the tree; it is **not** the exit — the empty frontier is.

| # | Item | Closed when |
|---|---|---|
| G1 | Problem | who hurts · what breaks · why now · cost of doing nothing |
| G2 | Outcome | one checkable change, in the user's words |
| G3 | Actors | who triggers · who is affected · permission tiers |
| G4 | Non-goals | what is tempting and still out, named |
| G5 | Current state | what exists today, cited (code or card) · reuse vs new |
| G6 | Happy path | end-to-end story, one pass, no branches |
| G7 | Wrong path | what *should* happen on invalid/empty/late/duplicate — business answer |
| G8 | Constraints | deadline · budget · team · stack · compliance · legacy that cannot move |
| G9 | Real-world shape | how many · how often · how big · how fast — numbers with units |
| G10 | Consumers | who else depends on this · what breaks if it changes |
| G11 | Evidence | how we see it worked · what signal would make us roll back |
| G12 | Appetite | what may be traded — speed, cost, consistency, polish |

`เร็ว` / `quick`: G1–G4 + G11 stay mandatory; the rest may close as `Assumed` **with an owner**.

## Language

Sharpen the domain model while grilling — glossary type `Term | Meaning | Not`.

- Term clashes with the project glossary → say so in the round. Never translate it silently.
- Fuzzy or overloaded term → propose the canonical one **and** the lookalike it is not.
- User states how something works and the code disagrees → that is R5, not a question.
- Term resolves → capture it then, not batched. Vault write goes through the write-gate.

ADR only when all three hold: hard to reverse · surprising without context · a real trade-off with named alternatives → `modes/decision.md`. Any one missing → no ADR.

## With a doc

Given a spec, ticket, thread, or existing card: read it fully first, then grill only **gaps and contradictions**. Every question cites the line it came from. Contradictions are listed as blockers, not questions.

## Ledger

**Open** (one line): scope · what was read · which floor rows the source already closes · fact-finds running.
**Close** (before Decide): Outcome · Non-goals · Constraints · `Assumed` + owner · Open risks · frontier empty.

The close card must be echoed or amended by the user. Bare `โอเค` is not acceptance.

## Blockers

An open branch that would change contract, data shape, ownership, or blast radius → **no lock**, no Capture. Escalate to counsel, ADR, or research instead of guessing.
