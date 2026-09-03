# SDLC — pipe

Named recipe runner. Rows live in `pipelines.md` — do not restate them here.
Writes: none (`allow.md`). Coordinator does not review, fix, or test.

## Run

| Step | Do |
|---|---|
| Name | Arg or alias. Bare → list names, stop. Unknown → list, stop |
| Confirm | One line: name · scope · N · 3 sequential roles. Stop until user confirms (not bare `ok`) |
| Spawn | Host **new session** per beat. Not kernel subagent. No spawn tool → stop, do not run the beat here |
| Loop | Follow the row. Skip `/fr-fix` if no must-fix. Max N. User halt anytime |
| Report | Halt round only: spawn `/fr-review` and `/fr-test` with report yes |
| Done | Verdict + session ids + report paths. Not `/fr-ship` |

Child prompt: target `/fr-*` · pipe name · iter i/N · scope · report yes/no · return that mode’s verdict block only.
