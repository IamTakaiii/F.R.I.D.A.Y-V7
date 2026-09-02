# Friday v7 — Verify

Never invent test commands. SoT order:

1. Injected `recipe=` path
2. Same file Dev commands table if root exists
3. Repo manifests read this session
4. User-stated command
5. Neighbor README if already opened

If none → `Verify: not run — no command`. Missing `.agent` is not a failure.

Use the repository's declared runner. Do not default to httpyac. Do not install a framework.

HTTP/API: prefer the repo e2e suite. Use `.http` only when the repo already owns it or the user asks.
