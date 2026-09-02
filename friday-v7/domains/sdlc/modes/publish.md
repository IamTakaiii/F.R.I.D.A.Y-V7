# SDLC — publish

Publish **approved** vault knowledge to Git. Never publish without an exact file preview the user accepts.

## Scope

User names files or “this feature”. Default: that feature’s `intent.md` / `design.md` / `queue.md` plus linked ADRs. Not the whole vault. Not `.agent/` unless asked.

## Preview (required)

Table: path · action (add/update) · why. Secrets/PII scan — strip or refuse. Language/headings already English-stable.

## After approve

Stage only listed paths. Commit message = why (1–2 sentences). Do not `git push` unless the user said push. Do not open a PR unless they asked.

## Done

Commit hash (or “user skipped”) + file list.
