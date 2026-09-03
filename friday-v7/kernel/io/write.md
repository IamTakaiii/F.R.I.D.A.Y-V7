# Friday v7 — Write & Approval

## Autonomy

- `supervised` (default): approve every file before write.
- `bounded`: one declared work package; writes inside need no repeat prompt.
- `autonomous`: announce package, then routine reversible writes.

Runtime: Claude/Codex `hosts/runtime.py` (`FRIDAY_SUPERVISED=on` default).

| Reply | Effect |
|---|---|
| `a` | approve proposed / next file; then **review-lock** |
| `r <hook>` | opened cited path; hook = section, symbol, or one finding |
| `s` | skip |
| `aa` / `bypass` | session unlock **and** skip review-lock |
| `supervised` | back to file-by-file |

Never Write/Edit until `a` or `aa` in chat (unless autonomy already unlocked).

## Session no-save

Session switch, not a mode. Any `/fr-*` still runs; only vault documents are refused.

| Reply | Effect |
|---|---|
| `nosave` · `ไม่บันทึก` | this session writes no vault document |
| `save on` · `บันทึกได้` | restore normal vault writes |

Scope: vault only. Repo code, tests, and `{agent_root}/` are unaffected.
While on: run the mode, deliver in chat, and name what would have been written (type + path). Do not write it. Durable work is not Done.

## Artifact language

Before the first durable write, ask body language (`ไทย` · `English` · `สองภาษา`).
If the project Brief already states a language, propose that; otherwise propose English.
Headings stay English. Record the choice for the work package. Do not hard-code project names here.

## Ask

```
[n/Total] TYPE: path - one-line description
Approve (a) / Skip (s) / Abort (x)? After write: r <hook> or aa
```

## Review-lock

`a` writes that file, then lock is on. Cite the path. Do not start the next work command.

Next work (`/fr-implement` `/fr-fix` `/fr-design` `/fr-test` `/fr-ship` `/fr-publish` `/fr-pipe`, ทำต่อ, next) → refuse until:

- `r <hook>` — section, symbol, or finding from the cited file
- `aa` — bypass lock + session unlock

Reject bare `r` and hooks `ok` `lgtm` `yes` `y` `ดูแล้ว` `แล้ว` `reviewed` `done`. `/fr-review` is not next work.

## Destinations

| Write type | Destination |
|---|---|
| Any durable document | vault via `brain/port.md` + **write-gate** |
| Application code / tests / migrations | code repo |
| Handoff / prefs / httpyac | `{agent_root}/` |
| Repo README | thin pointer; not Design |

Unsure markdown = vault.

## Vault documents

Command does not change the shape. Load `schema/write-gate.md` and follow it. Skip only for raw `10 - Inbox/`; promote later through the same gate.

## Always human-gated

Delete, deploy, overwrite large, secrets, irreversible migration, vault-wide restructure.

## Memory writes

Separate propose batch: `am` / `e` / `sm`. Never mix into ordinary `aa`.

## After durable writes

Close via `session/session.md`. Write-gate + line cap must pass before Done.
