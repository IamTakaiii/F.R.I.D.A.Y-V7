# SDLC — orient

Pick **one** next `/fr-*`. Do not start design, implement, review, or test here.

## Read

Overview Brief, Feature List, named feature `intent.md`/`design.md` if a name is given. Repo tree only if needed to name the project. Workspace: one repo unless the user is mid-task across repos.

## Classify

`design` · `implement` · `fix` · `review` · `test` · `ship` · `pipe` · `write` · `research` · `learn` · `brain` · `life` · `tool` · `httpyac` · `publish` · `unclear`

## Rules

- Named feature + no `design.md` → `/fr-design`.
- Queue item Ready → `/fr-implement`. Bug/regression → `/fr-fix`.
- Score / deep review / PR → `/fr-review`. Run tests / coverage / load → `/fr-test`. Pipeline / วนจนผ่าน → `/fr-pipe`.
- Go/no-go → `/fr-ship`. Vault vs Git → `/fr-publish`.
- Docs without new behavior → `/fr-write`. Citations → `/fr-research`. Teach → `/fr-learn`.
- Inbox / MOC / vault health → `/fr-brain`. Personal → `/fr-life`.
- Internal helper → `/fr-tool`. Authored `.http` journeys → `/fr-httpyac`.
- Two equal routes → one question. Else recommend one command + why (≤3 lines).

## Workspace (only if multi-repo)

Table: name · path · role · next mode. One primary next action. Do not invent services off disk. Missing `.agent` → list path, no nag.

## Next

State the command. Stop. Do not load that mode in this turn unless the user already issued it.
