# httpyac — run

Do not claim green without execute.

Need: `.http` · env vars · `httpyac` on PATH (`npm i -g httpyac` if missing).

```bash
httpyac send --all "{{http_file}}" --env dev
```

After: pass/fail per named step. On failure show status/body excerpt — do not rewrite asserts to green.

Optional durable record: type `note` at the feature project `89-Notes/Notes/YYYY-MM-DD - httpyac - <journey>.md` via write-gate. Only on ask — a run is not a document.
