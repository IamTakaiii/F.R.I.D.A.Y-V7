#!/usr/bin/env python3
"""Host-neutral Friday lifecycle runtime for Claude Code and Codex."""
from __future__ import annotations

import json
import os
import re
import sqlite3
import subprocess
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WRITE_TOOLS = {
    "write", "edit", "applypatch", "strreplace", "multiedit", "searchreplace",
    "createfile", "replaceallstringinfile", "notebookedit",
}
READ_TOOLS = {"read", "readfile"}
PROPOSE_MARKERS = ("## Memory propose", "## Session complete", "Approve memory (am)")
CLOSE_SIGNAL = re.compile(
    r"^(?:/)?fr-close\b|^(?:please\s+)?close\s+session\b|\bmemory\s+propose\s+now\b|"
    r"^(?:จบ|ปิด)\s*session\b|^ปิดงานนี้\b|^extract\s+memory\b",
    re.I,
)
SURFACE = re.compile(r"(?:^|[\s/`])(/?fr(?:iday)?(?:-[\w-]+)?)", re.I)
NEXT_WORK = re.compile(
    r"(?:^|[\s/`])(/fr-(?:implement|fix|design|test|ship|publish)\b)|"
    r"^(?:ทำต่อ|ต่อไป|next(?:\s+item)?\b|implement\b|ลงมือ)",
    re.I,
)
DUMB_HOOKS = frozenset(
    {"ok", "lgtm", "yes", "y", "ดูแล้ว", "แล้ว", ".", "1", "reviewed", "done", "next", "ต่อ", "ทำต่อ", "r"}
)
NO_SAVE_ON = re.compile(r"^(?:nosave|no-save|no save|ไม่บันทึก|ไม่ต้องบันทึก)\b", re.I)
NO_SAVE_OFF = re.compile(r"^(?:save on|savemode on|บันทึกได้|บันทึกได้แล้ว)\b", re.I)
VAULT_TOP = re.compile(r"^(?:00 - Meta|10 - Inbox|20 - Projects|30 - Knowledge|40 - Writing|90 - Archive)$")
SECRET_PATH = re.compile(
    r"(^|[\\/])(\.env(?:\.|$)|.*\.(?:pem|p12|pfx|key)$|id_rsa|id_ed25519|"
    r"credentials|service-account|secrets?[\\/]|[\\/]\.ssh[\\/]|auth\.json$|token\.json$)",
    re.I,
)


def flag_on(name: str, fallback: bool = True) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    if not raw:
        return fallback
    if raw in {"off", "0", "false", "no"}:
        return False
    if raw in {"on", "1", "true", "yes"}:
        return True
    return fallback


def normalize_tool(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def tool_path(data: dict[str, Any]) -> str:
    inp = data.get("tool_input") or data.get("toolInput") or {}
    if not isinstance(inp, dict):
        return ""
    for key in ("file_path", "filePath", "path", "file", "target_file", "notebook_path"):
        value = inp.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def absolute_path(value: str, cwd: str) -> str:
    path = Path(os.path.expandvars(os.path.expanduser(value)))
    if not path.is_absolute():
        path = Path(cwd) / path
    return str(path.resolve())


def guarded_memory_path(value: str) -> bool:
    path = value.replace("\\", "/")
    return bool(
        re.search(r"docs/skill-drafts/", path, re.I)
        or re.search(r"memory-(?:lesson|propose)", path, re.I)
        or ("/90 - Log/" in path and re.search(r"memory\s*lesson|mem\.", Path(path).name, re.I))
    )


def is_vault_path(value: str) -> bool:
    """Vault document path: under FRIDAY_BRAIN_ROOT, or under a vault top folder."""
    target = Path(value)
    root = os.environ.get("FRIDAY_BRAIN_ROOT", "").strip()
    if root:
        try:
            base = Path(os.path.expandvars(os.path.expanduser(root))).resolve()
            if target.resolve() == base or str(target.resolve()).startswith(str(base) + os.sep):
                return True
        except OSError:
            pass
    return any(VAULT_TOP.match(part) for part in target.parts)


def is_secret_path(value: str) -> bool:
    name = Path(value).name.lower()
    return name == ".env" or name.startswith(".env.") or bool(SECRET_PATH.search(value))


def default_state() -> dict[str, Any]:
    return {
        "paths": [],
        "tool_count": 0,
        "write_count": 0,
        "started_at": int(time.time()),
        "friday_skill": "",
        "pack_id": "",
        "pack_end": False,
        "pack_entered": False,
        "write_approved": flag_on("FRIDAY_EDIT_BYPASS", False),
        "supervised": flag_on("FRIDAY_SUPERVISED", True) and not flag_on("FRIDAY_EDIT_BYPASS", False),
        "last_blocked_path": "",
        "allowed_paths": [],
        "pending_allow_next": False,
        "review_lock_paths": [],
        "memory_approve_left": 0,
        "close_requested": False,
        "vault_write_off": False,
        "proposed": False,
        "closed_clean": False,
        "subagent_allowed": False,
        "agent_root": "",
        "agent_prefs": "",
        "agent_recipe": "",
        "worktree_primary": "",
        "kernel_reads": {},
        "nudge_sent": False,
        "cost_logged": False,
    }


class StateStore:
    """SQLite keeps parallel PostToolUse hooks from dropping state updates."""

    def __init__(self) -> None:
        base = Path(os.environ.get("FRIDAY_STATE_DIR", Path.home() / ".cache" / "friday-v7"))
        base.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(base / "host-runtime.sqlite3", timeout=10)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS sessions (key TEXT PRIMARY KEY, body TEXT NOT NULL, updated INTEGER NOT NULL)"
        )
        self.db.execute("BEGIN IMMEDIATE")

    def load(self, key: str) -> dict[str, Any]:
        row = self.db.execute("SELECT body FROM sessions WHERE key = ?", (key,)).fetchone()
        if not row:
            return default_state()
        try:
            state = json.loads(row[0])
            return state if isinstance(state, dict) else default_state()
        except json.JSONDecodeError:
            return default_state()

    def save(self, key: str, state: dict[str, Any]) -> None:
        self.db.execute(
            "INSERT INTO sessions(key, body, updated) VALUES(?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET body=excluded.body, updated=excluded.updated",
            (key, json.dumps(state, ensure_ascii=False), int(time.time())),
        )
        self.db.commit()
        self.db.close()

    def delete(self, key: str) -> None:
        self.db.execute("DELETE FROM sessions WHERE key = ?", (key,))
        self.db.commit()
        self.db.close()


def load_packs() -> dict[str, dict[str, Any]]:
    packs: dict[str, dict[str, Any]] = {}
    for rel in ("domains", "packs", "plugins"):
        base = ROOT / rel
        if not base.is_dir():
            continue
        for directory in base.iterdir():
            manifest = directory / "plugin.json"
            if directory.name.startswith(("_", ".")) or not manifest.is_file():
                continue
            try:
                raw = json.loads(manifest.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            hooks = raw.get("hooks") or {}
            item = {
                "id": str(raw.get("id") or directory.name),
                "enter": hooks.get("on_pack_enter") is True,
                "end": hooks.get("on_session_end") is True,
                "dir": directory,
            }
            for surface in raw.get("surfaces") or []:
                if isinstance(surface, str) and surface.strip():
                    packs[surface.strip().lower().lstrip("/")] = item
    return packs


def surface_from_prompt(prompt: str) -> str:
    match = SURFACE.search(prompt)
    if not match:
        return ""
    key = match.group(1).lower().lstrip("/")
    if key in {"friday", "friday-v6", "friday-v7"}:
        return "fr"
    try:
        registry = json.loads((ROOT / "routing" / "registry.json").read_text(encoding="utf-8"))
        for route in registry["routes"]:
            for alias in route["aliases"]:
                if alias.startswith("/") and alias.split()[0].lower().lstrip("/") == key:
                    return route["surface"].lstrip("/")
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        pass
    return key


def pack_context(surface: str, state: dict[str, Any]) -> str:
    if not flag_on("FRIDAY_PACK_HOOK", True):
        return ""
    pack = load_packs().get(surface)
    if not pack or not pack["enter"] or state["pack_entered"]:
        return ""
    state["pack_id"] = pack["id"]
    state["pack_end"] = pack["end"]
    state["pack_entered"] = True
    body_path = pack["dir"] / "hooks" / "on_pack_enter.md"
    try:
        body = body_path.read_text(encoding="utf-8").strip()[:800]
    except OSError:
        body = "Pack enter - orientation only; memory.recall only if recall_on_enter."
    return f"FRIDAY_PACK_HOOK: enter pack={pack['id']} surface={surface}\n{body}"


def find_agent_root(cwd: str) -> str:
    current = Path(cwd).resolve()
    for directory in (current, *list(current.parents)[:12]):
        agent = directory / ".agent"
        if (agent / "index.md").is_file():
            return str(agent)
    return "none"


def _git_out(cwd: str, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", cwd, *args],
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if result.returncode != 0:
        return ""
    return (result.stdout or "").strip()


def git_linked_primary(cwd: str) -> str:
    """Primary checkout path when cwd is a linked worktree; else empty."""
    toplevel = _git_out(cwd, "rev-parse", "--show-toplevel")
    porcelain = _git_out(cwd, "worktree", "list", "--porcelain")
    primary = ""
    for line in porcelain.splitlines():
        if line.startswith("worktree "):
            primary = line[9:].strip()
            break
    if not toplevel or not primary:
        return ""
    if Path(toplevel).resolve() == Path(primary).resolve():
        return ""
    return primary


def find_agent_prefs(cwd: str, agent_root: str, primary: str) -> str:
    local = Path(cwd) / ".agent" / "preferences.md"
    if local.is_file():
        return str(local)
    if agent_root and agent_root != "none":
        nested = Path(agent_root) / "preferences.md"
        if nested.is_file():
            return str(nested)
    if primary:
        inherited = Path(primary) / ".agent" / "preferences.md"
        if inherited.is_file():
            return str(inherited)
    return ""


def find_agent_recipe(cwd: str, agent_root: str, primary: str) -> str:
    local = Path(cwd) / ".agent" / "index.md"
    if local.is_file():
        return str(local)
    if agent_root and agent_root != "none":
        nested = Path(agent_root) / "index.md"
        if nested.is_file():
            return str(nested)
    if primary:
        inherited = Path(primary) / ".agent" / "index.md"
        if inherited.is_file():
            return str(inherited)
    return ""


def bind_agent_paths(state: dict[str, Any], cwd: str) -> None:
    state["agent_root"] = find_agent_root(cwd) if flag_on("FRIDAY_AGENT_ROOT", True) else "none"
    state["worktree_primary"] = git_linked_primary(cwd) if flag_on("FRIDAY_AGENT_ROOT", True) else ""
    state["agent_prefs"] = find_agent_prefs(cwd, state["agent_root"], state["worktree_primary"])
    state["agent_recipe"] = find_agent_recipe(cwd, state["agent_root"], state["worktree_primary"])


def apply_preferences(state: dict[str, Any]) -> None:
    prefs = state.get("agent_prefs") or ""
    if not prefs:
        root = state.get("agent_root")
        if root and root != "none":
            prefs = str(Path(root) / "preferences.md")
    if not prefs:
        return
    try:
        body = Path(prefs).read_text(encoding="utf-8")
    except OSError:
        return
    match = re.search(r"autonomy_profile:\s*(\w+)", body, re.I)
    if match and match.group(1).lower() in {"bounded", "autonomous"}:
        state["write_approved"] = True
        state["supervised"] = False


def event_output(event: str, context: str) -> dict[str, Any]:
    return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": context}}


def hook_ok(raw: str) -> bool:
    tokens = [t.strip(".,!?:;") for t in re.split(r"\s+", raw.strip()) if t.strip(".,!?:;")]
    if not tokens:
        return False
    if all(t.lower() in DUMB_HOOKS for t in tokens):
        return False
    return any(re.search(r"[A-Za-zก-๙]", t) for t in tokens)


def review_lock_nudge(state: dict[str, Any]) -> str:
    paths = state.get("review_lock_paths") or []
    listed = "\n".join(paths[-8:]) or "cited paths"
    return (
        "FRIDAY_REVIEW_LOCK: refuse next work. Open:\n"
        f"{listed}\n"
        "Reply r <section|symbol|finding> or aa to bypass. Not r / r ok / r lgtm / r ดูแล้ว."
    )


def deny(event: str, reason: str) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": event,
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def handle_prompt(prompt: str, state: dict[str, Any]) -> str:
    if not prompt or prompt.lstrip().startswith("FRIDAY_"):
        return ""
    low = prompt.strip().lower()
    context: list[str] = []
    surface = surface_from_prompt(prompt)
    if surface:
        state["friday_skill"] = surface
        entered = pack_context(surface, state)
        if entered:
            context.append(entered)
    if CLOSE_SIGNAL.search(prompt.strip()):
        state["close_requested"] = True
        state["closed_clean"] = False
        context.append(close_context(state))
    if NO_SAVE_ON.match(low):
        state["vault_write_off"] = True
        context.append(
            "FRIDAY_NO_SAVE: on. Run the mode, deliver in chat, name type + path instead of writing. "
            "Vault writes refused; repo and .agent unaffected. Say `save on` to restore."
        )
    if NO_SAVE_OFF.match(low):
        state["vault_write_off"] = False
        context.append("FRIDAY_NO_SAVE: off. Vault writes follow the normal gate.")
    if re.match(r"^am\b", low) or low.startswith("approve memory"):
        state["memory_approve_left"] = 5
    if re.match(r"^a\b", low) or low in {"approve", "approve file"}:
        blocked = state.get("last_blocked_path", "")
        if blocked:
            state["allowed_paths"] = list({*state["allowed_paths"], blocked})
            state["last_blocked_path"] = ""
        else:
            state["pending_allow_next"] = True
        context.append("FRIDAY_SUPERVISED: one file write approved.")
    if re.match(r"^(aa|bypass)\b", low) or low.startswith(("approve all", "approve writes")):
        state["write_approved"] = True
        state["supervised"] = False
        state["memory_approve_left"] = 20
        state["last_blocked_path"] = ""
        state["review_lock_paths"] = []
        context.append("FRIDAY_SUPERVISED: session writes unlocked; say `supervised` to restore file-by-file approval.")
    if re.match(r"^supervised\b", low) or low in {"no bypass", "ask each"}:
        state["write_approved"] = False
        state["supervised"] = True
        state["allowed_paths"] = []
        state["pending_allow_next"] = False
        context.append("FRIDAY_SUPERVISED: file-by-file approval restored.")
    r_match = re.match(r"^r(?:\s+(.*))?$", prompt.strip(), re.I)
    if r_match:
        hook = (r_match.group(1) or "").strip()
        if not state.get("review_lock_paths"):
            context.append("FRIDAY_REVIEW_LOCK: none pending.")
        elif hook_ok(hook):
            state["review_lock_paths"] = []
            context.append("FRIDAY_REVIEW_LOCK: cleared. Next work allowed.")
        else:
            names = ", ".join(Path(p).name for p in state["review_lock_paths"][-5:]) or "cited paths"
            context.append(
                "FRIDAY_REVIEW_LOCK: need r <section|symbol|finding> from "
                f"{names}. Not r / r ok / r lgtm / r ดูแล้ว. Or aa to bypass."
            )
    if state.get("review_lock_paths") and NEXT_WORK.search(prompt):
        context.append(review_lock_nudge(state))
    if low in {"s", "skip file"}:
        state["last_blocked_path"] = ""
        state["pending_allow_next"] = False
    if re.match(r"^sm\b", low) or low in {"skip all", "skip memory"}:
        state["paths"] = []
        state["close_requested"] = False
        state["closed_clean"] = True
        state["memory_approve_left"] = 0
    if re.search(r"\b(subagent|sub-agent|use task tool|parallel agents?|spawn agents?|split the work|fan-?out)\b", prompt, re.I):
        state["subagent_allowed"] = True
    return "\n".join(context)


def close_context(state: dict[str, Any]) -> str:
    paths = ", ".join(state.get("paths", [])[-5:]) or "none"
    root = state.get("agent_root", "none")
    return (
        "FRIDAY_MEMORY_HOOK: close now - Session complete + Memory propose (cards). "
        f"No silent memory writes without am. agent_root={root}; paths={paths}"
    )


def append_cost_log(state: dict[str, Any], host: str) -> None:
    if state.get("cost_logged") or not flag_on("FRIDAY_COST_LOG", True):
        return
    state["cost_logged"] = True
    root = state.get("agent_root")
    if not root or root == "none":
        return
    elapsed = max(0, int(time.time()) - int(state.get("started_at", time.time())))
    line = (
        f"- {time.strftime('%Y-%m-%d %H:%M')} host={host} tools={state['tool_count']} "
        f"writes={state['write_count']} kernel={len(state['kernel_reads'])} "
        f"paths={len(state['paths'])} skill={state.get('friday_skill') or '-'} ~{elapsed}s\n"
    )
    try:
        with (Path(root) / "cost-log.md").open("a", encoding="utf-8") as stream:
            stream.write(line)
    except OSError:
        pass


def handle(host: str, data: dict[str, Any]) -> dict[str, Any] | None:
    if not flag_on("FRIDAY_HOOKS", True):
        return None
    event = str(data.get("hook_event_name") or data.get("hookEventName") or "")
    session = str(data.get("session_id") or data.get("sessionId") or data.get("thread_id") or "default")
    key = f"{host}:{session}"
    store = StateStore()
    state = store.load(key)
    cwd = str(data.get("cwd") or os.getcwd())
    output: dict[str, Any] | None = None

    if event == "SessionStart":
        bind_agent_paths(state, cwd)
        apply_preferences(state)
        extras = []
        if state.get("agent_prefs"):
            extras.append(f"prefs={state['agent_prefs']}")
        if state.get("agent_recipe") and state.get("agent_root") in {"", "none"}:
            extras.append(f"recipe={state['agent_recipe']} (read-only)")
        if state.get("worktree_primary"):
            extras.append("linked worktree — never write primary .agent")
        extra = (" " + " ".join(extras)) if extras else ""
        output = event_output(
            event,
            f"FRIDAY_HOST_RUNTIME: host={host} full lifecycle enabled. "
            f"FRIDAY_AGENT_ROOT: root={state['agent_root']}; "
            f"writes={'supervised (a/aa)' if state['supervised'] else 'unlocked'}."
            f"{extra}"
        )
    elif event == "UserPromptSubmit":
        prompt = str(data.get("prompt") or data.get("user_prompt") or "")
        context = handle_prompt(prompt, state)
        if context:
            output = event_output(event, context)
    elif event == "PreToolUse":
        tool = normalize_tool(str(data.get("tool_name") or data.get("toolName") or ""))
        path_value = tool_path(data)
        if state.get("friday_skill") and not state.get("subagent_allowed") and not flag_on("FRIDAY_SUBAGENT", False):
            if tool in {"task", "agent", "spawnagent", "createagent"}:
                output = deny(event, "FRIDAY_SUBAGENT: blocked by default. Ask the user before spawning agents.")
        if output is None and path_value:
            full_path = absolute_path(path_value, cwd)
            if flag_on("FRIDAY_SECRETS", False) and is_secret_path(full_path):
                output = deny(event, f"FRIDAY_SECRETS: blocked secret-like path: {path_value}")
            elif tool in WRITE_TOOLS and state.get("vault_write_off") and is_vault_path(full_path):
                output = deny(
                    event,
                    "FRIDAY_NO_SAVE: session is no-save. Deliver in chat and name type + path.\n"
                    f"{path_value}\nSay `save on` to allow vault writes again.",
                )
            elif tool in WRITE_TOOLS:
                primary = state.get("worktree_primary") or git_linked_primary(cwd)
                if primary:
                    primary_agent = str((Path(primary) / ".agent").resolve())
                    local_agent = str((Path(cwd) / ".agent").resolve())
                    target = str(Path(full_path).resolve())
                    under_primary = target == primary_agent or target.startswith(primary_agent + os.sep)
                    under_local = target == local_agent or target.startswith(local_agent + os.sep)
                    if under_primary and not under_local:
                        output = deny(
                            event,
                            "FRIDAY_AGENT_ROOT: linked worktree — do not write the primary checkout .agent. "
                            "init-agent here for local handoff.",
                        )
                if output is None:
                    guarded = guarded_memory_path(full_path)
                    approved = state["write_approved"] or (guarded and state["memory_approve_left"] > 0)
                    if state["supervised"] and not approved and not guarded:
                        if full_path in state["allowed_paths"]:
                            state["allowed_paths"].remove(full_path)
                        elif state["pending_allow_next"]:
                            state["pending_allow_next"] = False
                        else:
                            state["last_blocked_path"] = full_path
                            output = deny(
                                event,
                                f"FRIDAY_SUPERVISED: ask in chat first, then a/aa.\n{path_value}\n"
                                "Reply: a (this file) | aa (session bypass) | s (skip)",
                            )
                    if output is None and guarded and not approved and flag_on("FRIDAY_WRITE_GUARD", True):
                        output = deny(event, f"FRIDAY_WRITE_GUARD: propose first, then am/aa.\n{path_value}")
    elif event in {"PostToolUse", "PostToolUseFailure"}:
        tool = normalize_tool(str(data.get("tool_name") or data.get("toolName") or ""))
        path_value = tool_path(data)
        state["tool_count"] += 1
        if path_value and tool in WRITE_TOOLS and event == "PostToolUse":
            full_path = absolute_path(path_value, cwd)
            state["write_count"] += 1
            guarded = guarded_memory_path(full_path)
            if guarded and state["memory_approve_left"] > 0 and not state["write_approved"]:
                state["memory_approve_left"] -= 1
            if full_path not in state["paths"] and not guarded:
                state["paths"].append(full_path)
            if (
                not guarded
                and state.get("supervised")
                and not state.get("write_approved")
            ):
                lock = state.setdefault("review_lock_paths", [])
                if full_path not in lock:
                    lock.append(full_path)
                if output is None:
                    output = event_output(
                        event,
                        "FRIDAY_REVIEW_LOCK: on. Cite this path. Next work only after "
                        f"r <section|symbol|finding> or aa.\n{path_value}",
                    )
            state["closed_clean"] = False
            state["proposed"] = False
            state["nudge_sent"] = False
        if path_value and tool in READ_TOOLS and "/friday-v7/kernel/" in absolute_path(path_value, cwd).replace("\\", "/"):
            reads = state["kernel_reads"]
            full_path = absolute_path(path_value, cwd)
            reads[full_path] = int(reads.get(full_path, 0)) + 1
            if reads[full_path] >= 2:
                output = event_output(event, f"FRIDAY_KERNEL_BUDGET: re-read {reads[full_path]}x: {path_value}. Load once.")
    elif event == "Stop":
        text = str(data.get("last_assistant_message") or "")
        memory_mode = os.environ.get("FRIDAY_MEMORY_HOOK", "auto").strip().lower()
        pack_allows_close = not state["friday_skill"] or state["pack_end"] or state["close_requested"]
        if any(marker in text for marker in PROPOSE_MARKERS):
            state["proposed"] = True
            state["closed_clean"] = True
            state["close_requested"] = False
            append_cost_log(state, host)
        elif state["paths"] and pack_allows_close and (state["close_requested"] or memory_mode == "force"):
            output = {
                "decision": "block",
                "reason": close_context(state),
                "hookSpecificOutput": {"hookEventName": event, "additionalContext": close_context(state)},
            }
        elif state["paths"] and pack_allows_close and not state["nudge_sent"] and memory_mode != "off":
            state["nudge_sent"] = True
            output = {"systemMessage": f"Friday: {len(state['paths'])} changed path(s) pending. Use /fr-close when ready."}
    elif event == "SessionEnd":
        append_cost_log(state, host)
        store.delete(key)
        return None

    store.save(key, state)
    return output
