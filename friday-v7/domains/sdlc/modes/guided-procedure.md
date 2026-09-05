# SDLC — guided procedure

Generate an interactive script for manual steps only a human can perform: credentials, third-party dashboards, provisioning, one-off migration, or cutover. Agent-doable steps stay with the agent.

## Scope

Read first. Setup: env examples, README, compose/framework config, workflows and every secret/variable reference. Transition: current state, target state, irreversible edges.

Show ordered stages. Every captured value must name:

- where the human obtains it,
- where it lands (`.env`, CI secret/variable, both, or nowhere),
- whether it is secret,
- which later stage consumes it.

Map the real click/command journey. Unknown current UI → check primary docs or ask; never invent a dashboard path.

## Script UX

- One focused stage per screen; show progress `n/total`.
- Open the relevant URL before requesting a value.
- Secret input is hidden and never printed.
- Idempotent env upsert; CI names exactly match workflow references.
- Confirm before irreversible action; retries resume safely.
- Final summary names completed stages and where values landed, never their secret values.

Use the repo task runner when appropriate. Scratch by default; commit only for repeatable team setup. Durable operational knowledge belongs in `runbook`, not comments inside an ephemeral script.

Verify `bash -n`; run `shellcheck` if available; static-trace every value. Do not run end-to-end when it opens browsers or blocks on human input.
