#!/usr/bin/env python3
"""Merge the full Friday lifecycle runtime into Claude Code and Codex."""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "hosts" / "hook.py"
COMMON_EVENTS = (
    "SessionStart",
    "UserPromptSubmit",
    "PreToolUse",
    "PostToolUse",
    "Stop",
    "SessionEnd",
)
HOST_EVENTS = {
    "claude": (*COMMON_EVENTS, "PostToolUseFailure"),
    "codex": COMMON_EVENTS,
}


def friday_group(host: str) -> dict:
    return {
        "hooks": [
            {
                "type": "command",
                "command": f'python3 "{HOOK}" --host {host}',
                "timeout": 10,
            }
        ]
    }


def is_friday(group: dict) -> bool:
    for h in group.get("hooks") or []:
        if isinstance(h, dict) and "hosts/hook.py" in str(h.get("command") or ""):
            return True
    return False


def merge_event(hooks: dict, event: str, host: str) -> None:
    groups = hooks.setdefault(event, [])
    if not isinstance(groups, list):
        hooks[event] = [friday_group(host)]
        return
    for index, group in enumerate(groups):
        if isinstance(group, dict) and is_friday(group):
            groups[index] = friday_group(host)
            return
    groups.append(friday_group(host))


def merge_file(path: Path, host: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data: dict = {}
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
    if not isinstance(data, dict):
        data = {}
    hooks = data.setdefault("hooks", {})
    if not isinstance(data.get("hooks"), dict):
        data["hooks"] = {}
        hooks = data["hooks"]
    for event in HOST_EVENTS[host]:
        merge_event(hooks, event, host)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"hooks: {path}")


def main() -> int:
    if os.environ.get("FRIDAY_HOST_HOOKS", "").strip().lower() in {"off", "0", "false", "no"}:
        print("skip host hooks (FRIDAY_HOST_HOOKS=off)")
        return 0
    HOOK.chmod(HOOK.stat().st_mode | 0o111)
    home = Path.home()
    merge_file(home / ".claude" / "settings.json", "claude")
    merge_file(home / ".codex" / "hooks.json", "codex")
    print("Codex: open /hooks and trust the Friday command once.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
