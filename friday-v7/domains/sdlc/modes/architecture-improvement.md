# SDLC — architecture improvement

Find high-value opportunities to concentrate behavior behind small interfaces. Writes: `audit-plan`; does not refactor.

## Aim

Optimize for **leverage** (behavior per interface fact callers learn), **locality** (change concentrates), and testability through one seam. Vocabulary: module · interface · implementation · seam · adapter.

## Scope before scan

Use the user's target. Otherwise inspect commit history for recurring hot paths; recent repeated change earns priority. Scattered history may widen the scope. Read project glossary and applicable ADRs first.

Hunt friction:

- One concept requires bouncing through many shallow modules.
- Interface complexity approaches implementation complexity.
- Extracted helpers test easily while orchestration bugs remain uncovered.
- Coupled modules leak knowledge across seams.
- Important behavior cannot be tested through the current interface.

Apply the deletion test: if deleting a module removes complexity, it was a pass-through; if complexity reappears across callers, the module was earning its keep.

## Report

For each candidate: paths · friction · proposed concentration (not the final interface) · leverage/locality/test benefit · before/after diagram · `Strong | Worth exploring | Speculative` · ADR conflict if any.

Put the top recommendation first. An optional self-contained HTML report goes to `$TMPDIR`, never the repo; include visual before/after cards and open it for the user.

Do not propose interfaces yet. User picks one → `/fr-design`; use Design Twice if alternatives matter. A rejected candidate gets an ADR only when its load-bearing reason prevents a future review from re-suggesting it.
