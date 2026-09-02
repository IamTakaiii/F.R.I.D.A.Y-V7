# Friday v7 — Write & Approval

## Autonomy

- `supervised` (default): approve every file before write.
- `bounded`: one declared work package; writes inside need no repeat prompt.
- `autonomous`: announce package, then routine reversible writes.

Runtime: Claude/Codex `hosts/runtime.py` (`FRIDAY_SUPERVISED=on` default).

| Reply | Effect |
|---|---|
| `a` | approve proposed / next file |
| `s` | skip |
| `aa` / `bypass` | session unlock |
| `supervised` | back to file-by-file |

Never Write/Edit until `a` or `aa` in chat (unless autonomy already unlocked).

## Artifact language

Before the first durable write, ask body language (`ไทย` · `English` · `สองภาษา`).
If the project Brief already states a language, propose that; otherwise propose English.
Headings stay English. Record the choice for the work package. Do not hard-code project names here.

## Ask

```
[n/Total] TYPE: path - one-line description
Approve (a) / Skip (s) / Abort (x)?
```

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
