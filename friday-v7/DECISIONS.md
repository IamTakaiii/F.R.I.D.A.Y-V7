# Friday v7 — Locked decisions

| ID | Topic | Decision |
|---|---|---|
| D1 | Surfaces | `/fr-*` prefix; thin stubs from `plugin.json`; no fat surfaces |
| D2 | Brain | Resolve via `kernel/brain/port.md` only. Default backend `local` at `~/.local/share/friday/` (create on first approved write). Obsidian is opt-in: explicit `brain.backend: obsidian` + vault path, or a resolved root that contains `.obsidian/`. Same `schema/vault.md` layout either way |
| D3 | Plugins | Manifest + hooks. Claude/Codex: `hosts/runtime.py`. No pack shell scripts |
| D4 | SDLC artifacts | Feature List row + Intent always. Design for M/L or durable technical decision. Work-item evidence for every implemented queue row. No `00 - Index.md`. No Threads folder |
| D5 | Headings | English always; body follows confirmed project language |
| D6 | vs v6 | Separate skill tree; parallel install; no auto vault migrate |
| D7 | Shape | Harness, not a framework. No SDK / marketplace |
| D8 | Artifact SoT | `schema/` only. Card + registered parts + hard line caps. One frontmatter schema |
| D9 | Load SoT | `kernel/runtime.md` only. Parent SKILL does not duplicate the upgrade table |
| D10 | Folders | Companion folders created with first file only |
| D11 | Vault numbers | Fixed: Data=`04`, Labs=`05` (opt-in), Ship=`06`, Operations=`07`. Feature inner files are unnumbered names |
| D12 | Types retired | `design-slice`, `policy-cost-spike`, vault types `lab`/`guide`/`httpyac`, aliases `brief`/`todo`/`work-log`, field `load_profile` |
| D13 | Collapse set | 18 surfaces. Folded names only in `ROUTING.md`. Merged types: `quality-report`, `brief`, `note`, architecture `stack` part. Surface and mode counts are derived from `domains/*/plugin.json` — never asserted anywhere else. |
| D14 | Vault consistency | Every durable vault write uses the same gate (`schema/write-gate.md`): type + placement + template + cap. Command/domain must not define a second shape. |
| D15 | Allow | Mode may write only types in `schema/allow.md`. |
| D16 | Vault check | `evals/check_vault.py` against `FRIDAY_BRAIN_ROOT` when set; templates checked by `check_schema.py`. |
| D17 | Feature List SoT | New `intent.md` / `design.md` without a Feature List SoT is a failed write. |
| D18 | Kernel | No project names or language defaults in `kernel/io/write.md`. |
| D19 | User docs | `docs/USER-GUIDE.md` is the only how-to. History stays in this file. |
| D20 | Split | Compress first. Registered parts only (`design/*`, `stack`, `work/`). Never `stem - Heading.md`. Doc history stays on the card (last 5 rows). Still over = failed write. |
| D21 | Nav | Click = `[[wikilink]]` only. Never `[[.]]`. `## Parts` is click SoT. `intent.md` is the feature hub; other feature files link Intent only. `## Links` last before history, one `- Kind: [[path]]` per target. No Index file. |
| D22 | Cap | `max_lines: 200`. Count body only (exclude YAML, Links, history). `0` = unlimited for `timeline-log`, `memory-lesson`, and `90 - Log/`. Still over → compress or registered parts; never heading siblings. |
| D23 | Review-lock | `a` turns on review-lock after the write. Next work needs `r <hook>` or `aa`. `aa` bypasses lock and unlocks writes. Dumb hooks (`ok` `lgtm` `ดูแล้ว` …) rejected. `/fr-review` is not next work. |
| D24 | Pipe | `/fr-pipe` is a coordinator. Recipes in `pipelines.md`. Spawn a new host session per beat. Never fuse review/fix/test. Never a ship beat. |
| D25 | Review scoring | Dim scale `0 4 6 8 10`; `10` needs a cite and zero findings; ★ must be 10. `score_pct` divides by `10 × Σweights` — a plain weighted sum is not a percentage. One bar for every run; `เข้มงวด`/`strict` changes who hunts, never the bar. |
| D26 | Determinism | Scope lock before reading · ledger row per lens/dim (`clean` · finding · `N/A`+reason; missing row = FAIL) · severity by consequence for all three tracks · tier and risk chosen by stated triggers · scored output names its profile. Re-runs are compared on the ledger, never on `%`. **Exception:** the Friday skill tree is not a vault project, so a review or audit of it is chat-only. Its ledger dies with the session — say so, and never claim cross-run comparability for those runs. |
| D27 | Freshness | `superseded`/`archived` is never truth. A card quoted without opening its source is `Unverified(<updated>)`. Source wins for current behavior, card wins for intent; conflicts are reported, never merged. |
| D28 | TDD | Red→green is mode `sdlc.tdd` under `/fr-implement` — an alias, not a 20th surface (D13 holds). No test at a seam the user has not confirmed; no correct seam is an architecture finding, never a shallow test. **Refactoring is not in the loop** — it belongs to `/fr-review`. Test *quality* is owned by `standards/tdd.md` only; `standards/test.md` keeps coverage evidence. A tautological test is `major` on C5: false green regardless of coverage. |
| D29 | Routing evidence | `routing/registry.json` carries signals only; examples live in `evals/routing-examples.json` and must route **by score** — no exact-match shortcut, ever. A `negative` names the sibling's canonical phrase, never a generic word. Contrast examples need ≥2 positive hits on the intent half plus a negative on the rival. `check_tree.py` is the only green light and runs every sibling eval. |

## SDLC tiers

Locked: tier drives which artifacts and which gate rows apply. Selection triggers and the artifact table live in `domains/sdlc/SKILL.md` — one owner, do not copy them back here.

## Prose

Durable docs: specific enough to act, short enough to scan (`kernel/thinking/prose.md`). Over cap → compress, then registered parts, else fail.
