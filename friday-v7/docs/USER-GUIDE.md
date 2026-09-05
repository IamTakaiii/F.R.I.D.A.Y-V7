# Friday v7

Install: `./scripts/install.sh`. Load friday-v7 only.

## Map — read in this order

```
SKILL.md                 identity only (not the rulebook)
kernel/runtime.md        cold path SoT
docs/USER-GUIDE.md       this file
DECISIONS.md             locked calls
ROUTING.md               routing behavior and confidence contract
routing/registry.json    route evidence + aliases + examples (SoT)
hosts/opencode/commands/ OpenCode slash stubs → matching surface
schema/                  write contract (order below)
domains/<name>/SKILL.md  → one modes/<job>.md
surfaces/fr-*/SKILL.md   thin stubs only
```

Do not cold-load the whole vault or `schema/`. Every mode must resolve the configured brain and perform a bounded lookup before claiming relevant context is absent; load `schema/` only when the mode writes or migrates an artifact.

## Rule owners

One concern → one file. Copying a procedure into a second file is drift.

| Concern | Owner |
|---|---|
| Identity | `SKILL.md` |
| Always-on / cold path | `kernel/runtime.md` |
| Write / approve / review-lock | `kernel/io/write.md` |
| Verify commands | `kernel/io/verify.md` |
| Vault shape + cap | `schema/write-gate.md` |
| Routing behavior | `ROUTING.md` |
| Route targets, evidence, aliases, examples | `routing/registry.json` |
| Locked product calls | `DECISIONS.md` |
| How-to | this file |
| OpenCode slash stubs | `hosts/opencode/commands/` |
| OpenCode host pointer | `~/.config/opencode/AGENTS.md` |

## One Front Door

Use `/fr <outcome in normal language>`. A high-confidence route continues into the owning mode in the same turn; never repeat the command. Medium confidence asks one contrast question. Low confidence shows six outcome groups, not 67 modes.

OpenCode convenience aliases under `hosts/opencode/commands/` are real commands. Claude/Codex use `/fr <outcome>` or one of the registered surfaces.

## Brain (Obsidian optional)

Durable docs live in a brain folder. Obsidian is not required.

| Backend | When |
|---|---|
| `local` | Default. No config, or `brain.backend: local` / `local-fs` / `fs` |
| `obsidian` | Opt-in: `brain.backend: obsidian` + vault path, or the resolved root has `.obsidian/` |

Set **one** of: env `FRIDAY_BRAIN_ROOT` (optional `FRIDAY_BRAIN_BACKEND`) · `{agent_root}/preferences.md` · host AGENTS `brain.backend` + `brain.root`. Default root: `~/.local/share/friday/`. Layout is always `schema/vault.md`.

## Vault write (every command)

1. Type allowed — `schema/allow.md`
2. Path — `schema/placement.md`
3. Copy type file — `schema/types/` — strip `<!-- -->` and `>` lines
4. Shape + cap — `schema/artifact.md` · `schema/write-gate.md`
5. Layout — `schema/vault.md`

Never `stem - Heading.md`. Chat is not the artifact. Intent/Design without a Feature List SoT is a failed write.

## Approve

Default supervised. `a` = this file, then review-lock. Next work needs `r <section|symbol|finding>` — not `r` / `r ok` / `r lgtm` / `r ดูแล้ว`. `aa` = session bypass, no review-lock. `/fr-review` is not next work.

## Existing feature (change or add)

Do not open a new feature folder. Patch the same package.

| What happened | Command | Touch |
|---|---|---|
| Code moved, docs lag | `/fr-sdlc` sync | Only the wrong file |
| Contract change (flow, owner, API, data) | `/fr-design` | `design.md` + matching part · HTTP → `api/` · irreversible → ADR |
| Several dependent slices | `/fr-slice` | Vertical `work-item`s + blocker graph; wide change uses expand → migrate → contract |
| One queue item | `/fr-implement` | One `queue.md` row + `work/TODO-…` · Intent/Design only if scope changes |
| One queue item, test-first | `/fr-tdd` | Confirm seams → red → green per vertical slice · same `work/TODO-…` · refactor deferred to `/fr-review` |
| Hard bug / performance regression | `/fr-debug` | Red-capable loop → minimal repro → falsifiable hypotheses → regression seam → `fix-note` |
| Incident / review follow-up | `/fr-fix` | `runbook`, `fix-note`, or `work` · Design if intended behavior changed |
| New review | `/fr-review` [`เข้มงวด`/`strict`] | New `reports/YYYY-MM-DD - …`. Strict offers a skip/3/5 specialist panel; the bar is the same either way |

## Focused SDLC Modes

Aliases route into `/fr-sdlc`; they do not create extra surfaces.

| Signal / alias | Mode | Outcome |
|---|---|---|
| `/fr-experiment` | `design-experiment` | Disposable evidence for one logic/UI decision |
| `/fr-plan-large` | `decision-map` | Destination + decision frontier + fog across sessions |
| `/fr-architecture-review` | `architecture-improvement` | Ranked deep-module opportunities; no refactor yet |
| `/fr-triage` | `work-intake` | Verified issue/PR routed to agent, human, info, or wontfix |
| `/fr-questionnaire` | `stakeholder-questions` | Questions for the person who owns missing knowledge |
| `/fr-wizard` | `guided-procedure` | Safe interactive script for human-only setup/cutover |
| `/fr-retro` | `environment` | One evidence-backed improvement to agent navigation/checks/tools |

Travel planning through `/fr-life logistics` writes one canonical `trip-plan` with itinerary, booking state, departure checklist, budget snapshot, and backups. Detailed tasks, transactions, and heavy risks stay in linked personal artifacts.

Patch: same type and heading order · `Doc history` row · `rev++` only for contract or data-shape · hub Links stay on `intent.md`. No `flow-2.md` / Design v2.

## Check

```bash
python3 evals/check_tree.py      # runs everything below; the only command you need
```

It chains `check_schema` (one frontmatter contract) · `check_allow` (every type allowed somewhere) · `check_routing` (every example routes by evidence) · `check_rubric` (review scale, bands, weights) · `check_vault` (skipped unless `FRIDAY_BRAIN_ROOT` is set). Run one of them alone only to read its output in isolation — never to decide the tree is green.

## Scripts

| Path | Use |
|---|---|
| `scripts/install.sh` | Symlink this clone into host skill folders |
| `scripts/vault/` | One-off vault heal / migrate — not on the cold path |
| `scripts/retired/` | Do not run |

## Words

| Term | Meaning |
|---|---|
| card | Canonical file |
| part | Registered companion (`design/` or `stack`) |
| vault / brain | Configured root (local folder or Obsidian vault). Same layout |
| Links | Hub = `intent.md`. Others: Intent only. Last before history. Never `[[.]]` |
| Cap | 200 body lines; YAML / Links / history do not count. Logs = unlimited (`max_lines: 0`) |
| Flow | Bound + ` ```text` ` sequence + ` ```mermaid` ` + fail/next |
| queue | Feature work index |
| work-item | What shipped + Evidence (paths + verify). Not a copy of the queue row. |
| domain | Was v6 pack |

## v6 → v7 names (no auto-migrate)

| v6 | v7 |
|---|---|
| `01 - Intent.md` | `intent.md` |
| `02 - Design.md` | `design.md` |
| `03 - TODO.md` | `queue.md` |
| `02 - Work/` | `work/` |
| Data `03`/`04` | `04 - Data/` |
| Ship `04`/`05` | `06 - Ship/` |
| `review` / test-report / perf-report | `quality-report` + `kind` |
| `project-brief` / `personal-brief` | `brief` + `project_kind` |
