# Friday v7 — Locked decisions

| ID | Topic | Decision |
|---|---|---|
| D1 | Surfaces | `/fr-*` prefix; thin stubs from `plugin.json`; no fat surfaces |
| D2 | Brain | Resolve via `kernel/brain/port.md` only. Prefer configured Obsidian vault; fallback `~/.local/share/friday/` (`local`) on first approved write |
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
| D13 | Collapse set | 17 surfaces. Folded names only in `ROUTING.md`. Merged types: `quality-report`, `brief`, `note`, architecture `stack` part. |
| D14 | Vault consistency | Every durable vault write uses the same gate (`schema/write-gate.md`): type + placement + template + cap. Command/domain must not define a second shape. |
| D15 | Allow | Mode may write only types in `schema/allow.md`. |
| D16 | Vault check | `evals/check_vault.py` against `FRIDAY_BRAIN_ROOT` when set; templates checked by `check_schema.py`. |
| D17 | Feature List SoT | New `intent.md` / `design.md` without a Feature List SoT is a failed write. |
| D18 | Kernel | No project names or language defaults in `kernel/io/write.md`. |
| D19 | User docs | `docs/USER-GUIDE.md` is the only how-to. History stays in this file. |
| D20 | Split | Compress first. Registered parts only (`design/*`, `stack`, `work/`). Never `stem - Heading.md`. Doc history stays on the card (last 5 rows). Still over = failed write. |
| D21 | Nav | Click = `[[wikilink]]` only. Never `[[.]]`. `## Parts` is click SoT. `intent.md` is the feature hub; other feature files link Intent only. `## Links` last before history, one `- Kind: [[path]]` per target. No Index file. |
| D22 | Cap | `max_lines: 200`. Count body only (exclude YAML, Links, history). `0` = unlimited for `timeline-log`, `memory-lesson`, and `90 - Log/`. Still over → compress or registered parts; never heading siblings. |

## SDLC tiers

| Tier | Required artifacts |
|---|---|
| S | Feature List row + lightweight Intent; work-item if implemented as a queue row |
| M | + one Design card; queue/work-items when tracked; ADR if irreversible |
| L | + queue; Review/Ship when in scope |

## Prose

Durable docs: specific enough to act, short enough to scan (`kernel/thinking/prose.md`). Over cap → compress, then registered parts, else fail.
