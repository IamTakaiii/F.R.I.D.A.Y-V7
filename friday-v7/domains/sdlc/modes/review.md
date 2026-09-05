# SDLC — review

Pair review. `/fr-pr` = this + `git log`/`diff` (do not invent the range).
Bar lives in `../standards/review.md`; lenses in `../standards/lens.md`. **Score only after hunt; load `review.deep.md` whenever you score.**
Arg `เข้มงวด` / `strict` (users may type `deep`) = offer the specialist panel. It changes who hunts, never the bar.

Do not implement. After must-fix → `/fr-fix`. Do not load ship.

## Pulse

```
T0  Track (from named paths only) + strict? → user restates 1 line
T1  Pre-flight → scope lock (≤6 paths) + spec source + prior report for that scope
T2  Two hunts in parallel → merged ledger. Ask only if clash or ambiguous bug → restate 1 line
T3  review.deep.md → score that track
T4  One verdict block (scope · ledger · findings)
T5  quality-report if they want a file
```

## T1 pre-flight

Diff review (`/fr-pr`, "review since X") resolves the range **before** anything else runs:

1. Fixed point is whatever the user named — SHA, branch, tag, `main`, `HEAD~5`. Not named → ask. Never invent.
2. `git rev-parse <point>` must resolve · `git diff <point>...HEAD` (three-dot = against the merge-base) must be non-empty · `git log <point>..HEAD --oneline` for the commit list.
3. Bad ref or empty diff **fails here** — not inside a hunt, and never as a guess.

**Spec source**, first hit wins: resolve the brain root through `kernel/brain/port.md` + one adapter (`local` default; Obsidian only if configured), then use the repo project name/remote and changed paths or branch to select one feature from that project's Feature List and read only that feature pack's `intent.md`, `design.md`, `queue.md`, and linked `plans/`/`work/` slices → Intent/Design already in context → issue refs in the commit messages → a path the user passed → a spec under `docs/` `specs/` `.scratch/` matching the branch → ask. A resolved brain is a valid spec source, not an optional afterthought.

Vault lookup is bounded: do not scan the whole brain. If project/feature matching yields zero or multiple candidates, report the candidates and ask before scoring; do not silently downgrade a known brain spec to `no spec`.

None of those → state `no spec` plainly. It is a recorded state, not unread scope: the spec hunt reports `no spec available`, spec findings are impossible, and **C2 cannot reach 10** because nothing is cited to prove intent.

## T2 two hunts

Split the **context**, not the score. An agent that just filled its window with repo conventions judges intent worse.

Two read-only subagents in parallel (`kernel/extras/subagent.md`), same locked scope, neither sees the other's context:

| Hunt | Carries | Reports |
|---|---|---|
| **standards** | `lens.md` incl. the smell baseline · repo convention docs · neighbor files | per file/hunk: documented-standard breaches (cite the rule) · `possible <smell>` with the hunk quoted |
| **spec** | Intent/Design/DoD or the resolved spec source · the diff | requirements missing or partial · behaviour nobody asked for (`creep`) · requirements implemented wrong — quote the requirement line for each |

Each returns ledger rows + findings, ≤400 words. No spec source → that hunt returns `no spec available` and the ledger says so.

The parent merges: every lens still owes its row, findings map to dims, **one track, one %**. Show both hunt blocks separately above the verdict — do not rerank one hunt's findings against the other before mapping. Scoring is the parent's job alone; hunts never score.

Hunts are unavailable or the scope is one small file → run both passes in this context, sequentially, and say so in the verdict. Cheaper is fine; silent merging is not.

**Panel:** offer once at T2. Accepted → `modes/panel.md` before T3. Panel findings still get scored here; panel never scores.
- default: `skip` or N (2–5)
- strict: `skip` · `3` · `5` only — do not offer generic N
Roles = first N of the review catalog (`kernel/thinking/brainstorm.md`).

## Scope lock

Scope rule: `kernel/runtime.md`. PR → the `git diff` range, never invent.
Re-review of the same target: read the newest `reports/` for that scope first. New finding needs a reason · dropped finding needs `fixed` or `withdrawn`. Scope or profile changed → say so; runs are not comparable.

## Ledger

Every lens (code) or dim (artifact, general) emits one row before scoring: `clean` + cited path · finding ids · or `N/A` + reason.
`N/A` is a row, not an absence — a dim you skip silently is unread scope = FAIL. All rows `clean` → collapse to one line.
Ledger is what re-runs are compared on — not the %.

Target is the Friday skill tree itself → chat-only; no `quality-report`, no vault path. Say plainly that this ledger dies with the session and the next run has nothing to diff (D26).

Whole folder = two sessions (code, then artifact). Challenge: hold / withdraw / refine — then rescore that track.
