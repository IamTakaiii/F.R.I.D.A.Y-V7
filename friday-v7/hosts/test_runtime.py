from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from install_hooks import HOST_EVENTS, merge_file
from runtime import find_agent_prefs, git_linked_primary, handle


class RuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.env = patch.dict(
            os.environ,
            {
                "FRIDAY_STATE_DIR": self.temp.name,
                "FRIDAY_SUPERVISED": "on",
                "FRIDAY_EDIT_BYPASS": "off",
                "FRIDAY_COST_LOG": "off",
            },
            clear=False,
        )
        self.env.start()

    def tearDown(self) -> None:
        self.env.stop()
        self.temp.cleanup()

    def event(self, host: str, session: str, name: str, **extra):
        return handle(host, {"session_id": session, "hook_event_name": name, "cwd": self.temp.name, **extra})

    def test_session_start_injects_host_and_agent_root(self) -> None:
        root = Path(self.temp.name) / ".agent"
        root.mkdir()
        (root / "index.md").write_text("project: test\n", encoding="utf-8")

        output = self.event("claude", "one", "SessionStart")

        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("host=claude", context)
        self.assertIn(str(root), context)

    def test_pack_enter_is_injected_once(self) -> None:
        first = self.event("codex", "pack", "UserPromptSubmit", prompt="/fr-design search")
        second = self.event("codex", "pack", "UserPromptSubmit", prompt="/fr-design again")

        self.assertIn("pack=domain.sdlc", first["hookSpecificOutput"]["additionalContext"])
        self.assertIsNone(second)

    def test_folded_alias_enters_owning_pack(self) -> None:
        output = self.event("codex", "alias", "UserPromptSubmit", prompt="/fr-debug intermittent failure")

        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("pack=domain.sdlc", context)
        self.assertIn("surface=fr-fix", context)

    def test_supervised_write_requires_a_then_allows_exact_path(self) -> None:
        denied = self.event(
            "claude", "write", "PreToolUse", tool_name="Write", tool_input={"file_path": "note.md"}
        )
        self.event("claude", "write", "UserPromptSubmit", prompt="a")
        allowed = self.event(
            "claude", "write", "PreToolUse", tool_name="Write", tool_input={"file_path": "note.md"}
        )

        self.assertEqual("deny", denied["hookSpecificOutput"]["permissionDecision"])
        self.assertIsNone(allowed)

    def test_a_write_locks_next_work_until_r_hook(self) -> None:
        self.event("claude", "lock", "UserPromptSubmit", prompt="a")
        self.event(
            "claude", "lock", "PreToolUse", tool_name="Write", tool_input={"file_path": "note.md"}
        )
        post = self.event(
            "claude", "lock", "PostToolUse", tool_name="Write", tool_input={"file_path": "note.md"}
        )
        nxt = self.event("claude", "lock", "UserPromptSubmit", prompt="/fr-implement next")
        dumb = self.event("claude", "lock", "UserPromptSubmit", prompt="r lgtm")
        ok = self.event("claude", "lock", "UserPromptSubmit", prompt="r Review-lock")
        after = self.event("claude", "lock", "UserPromptSubmit", prompt="/fr-implement next")

        self.assertIn("FRIDAY_REVIEW_LOCK: on", post["hookSpecificOutput"]["additionalContext"])
        self.assertIn("refuse next work", nxt["hookSpecificOutput"]["additionalContext"])
        self.assertIn("need r <section|symbol|finding>", dumb["hookSpecificOutput"]["additionalContext"])
        self.assertIn("cleared", ok["hookSpecificOutput"]["additionalContext"])
        self.assertIsNone(after)

    def test_aa_skips_review_lock(self) -> None:
        self.event("claude", "bypass", "UserPromptSubmit", prompt="aa")
        self.event(
            "claude",
            "bypass",
            "PostToolUse",
            tool_name="Write",
            tool_input={"file_path": "note.md"},
        )
        nxt = self.event("claude", "bypass", "UserPromptSubmit", prompt="/fr-implement next")
        ctx = (nxt or {}).get("hookSpecificOutput", {}).get("additionalContext", "")

        self.assertNotIn("FRIDAY_REVIEW_LOCK", ctx)

    def test_aa_unlocks_writes_for_each_host_without_sharing_state(self) -> None:
        self.event("codex", "same", "UserPromptSubmit", prompt="aa")
        codex = self.event(
            "codex", "same", "PreToolUse", tool_name="apply_patch", tool_input={"file_path": "a.md"}
        )
        claude = self.event(
            "claude", "same", "PreToolUse", tool_name="Write", tool_input={"file_path": "a.md"}
        )

        self.assertIsNone(codex)
        self.assertEqual("deny", claude["hookSpecificOutput"]["permissionDecision"])

    def test_memory_path_requires_explicit_memory_approval(self) -> None:
        self.event("claude", "memory", "UserPromptSubmit", prompt="a")
        denied = self.event(
            "claude",
            "memory",
            "PreToolUse",
            tool_name="Write",
            tool_input={"file_path": "docs/skill-drafts/new.md"},
        )
        self.event("claude", "memory", "UserPromptSubmit", prompt="am")
        allowed = self.event(
            "claude",
            "memory",
            "PreToolUse",
            tool_name="Write",
            tool_input={"file_path": "docs/skill-drafts/new.md"},
        )

        self.assertIn("FRIDAY_WRITE_GUARD", denied["hookSpecificOutput"]["permissionDecisionReason"])
        self.assertIsNone(allowed)

    def test_nosave_blocks_vault_docs_but_not_repo_code(self) -> None:
        vault = str(Path(self.temp.name) / "20 - Projects" / "10 - Software" / "01 - X" / "design.md")
        self.event("claude", "nosave", "UserPromptSubmit", prompt="aa")
        on = self.event("claude", "nosave", "UserPromptSubmit", prompt="nosave")
        denied = self.event(
            "claude", "nosave", "PreToolUse", tool_name="Write", tool_input={"file_path": vault}
        )
        code = self.event(
            "claude", "nosave", "PreToolUse", tool_name="Write", tool_input={"file_path": "src/app.py"}
        )
        self.event("claude", "nosave", "UserPromptSubmit", prompt="save on")
        restored = self.event(
            "claude", "nosave", "PreToolUse", tool_name="Write", tool_input={"file_path": vault}
        )

        self.assertIn("FRIDAY_NO_SAVE: on", on["hookSpecificOutput"]["additionalContext"])
        self.assertEqual("deny", denied["hookSpecificOutput"]["permissionDecision"])
        self.assertIn("FRIDAY_NO_SAVE", denied["hookSpecificOutput"]["permissionDecisionReason"])
        self.assertIsNone(code)
        self.assertIsNone(restored)

    def test_nosave_uses_brain_root_when_set(self) -> None:
        root = Path(self.temp.name) / "MyVault"
        (root / "notes").mkdir(parents=True)
        target = str(root / "notes" / "x.md")
        with patch.dict(os.environ, {"FRIDAY_BRAIN_ROOT": str(root)}, clear=False):
            self.event("claude", "root", "UserPromptSubmit", prompt="aa")
            self.event("claude", "root", "UserPromptSubmit", prompt="ไม่บันทึก")
            denied = self.event(
                "claude", "root", "PreToolUse", tool_name="Write", tool_input={"file_path": target}
            )

        self.assertEqual("deny", denied["hookSpecificOutput"]["permissionDecision"])

    def test_secret_and_subagent_guards(self) -> None:
        self.event("claude", "guards", "UserPromptSubmit", prompt="/fr-design")
        subagent = self.event("claude", "guards", "PreToolUse", tool_name="Task", tool_input={})
        with patch.dict(os.environ, {"FRIDAY_SECRETS": "on"}, clear=False):
            secret = self.event(
                "claude", "guards", "PreToolUse", tool_name="Read", tool_input={"file_path": ".env"}
            )

        self.assertIn("FRIDAY_SUBAGENT", subagent["hookSpecificOutput"]["permissionDecisionReason"])
        self.assertIn("FRIDAY_SECRETS", secret["hookSpecificOutput"]["permissionDecisionReason"])

    def test_close_blocks_stop_until_proposal_is_emitted(self) -> None:
        self.event("codex", "close", "UserPromptSubmit", prompt="aa")
        self.event(
            "codex", "close", "PostToolUse", tool_name="apply_patch", tool_input={"file_path": "done.md"}
        )
        self.event("codex", "close", "UserPromptSubmit", prompt="/fr-close")
        blocked = self.event("codex", "close", "Stop", last_assistant_message="Not closed")
        complete = self.event("codex", "close", "Stop", last_assistant_message="## Session complete")

        self.assertEqual("block", blocked["decision"])
        self.assertIsNone(complete)


class WorktreeAgentTest(unittest.TestCase):
    def _git(self, cwd: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)

    def test_linked_worktree_inherits_prefs_and_blocks_primary_write(self) -> None:
        import shutil
        if shutil.which("git") is None:
            self.skipTest("git not available")
        with tempfile.TemporaryDirectory() as temp:
            main = Path(temp) / "main"
            main.mkdir()
            self._git(main, "init", "-b", "main")
            self._git(main, "config", "user.email", "t@t")
            self._git(main, "config", "user.name", "t")
            (main / "README").write_text("x\n", encoding="utf-8")
            self._git(main, "add", "README")
            self._git(main, "commit", "-m", "i")
            agent = main / ".agent"
            agent.mkdir()
            (agent / "index.md").write_text("project: main\n", encoding="utf-8")
            (agent / "preferences.md").write_text("autonomy_profile: bounded\n", encoding="utf-8")
            wt = Path(temp) / "wt"
            self._git(main, "worktree", "add", str(wt), "-b", "feat")

            self.assertEqual(Path(git_linked_primary(str(wt))).resolve(), main.resolve())
            self.assertEqual(git_linked_primary(str(main)), "")
            self.assertEqual(
                Path(find_agent_prefs(str(wt), "none", str(main))).resolve(),
                (agent / "preferences.md").resolve(),
            )

            env = patch.dict(
                os.environ,
                {
                    "FRIDAY_STATE_DIR": temp,
                    "FRIDAY_SUPERVISED": "on",
                    "FRIDAY_EDIT_BYPASS": "off",
                    "FRIDAY_COST_LOG": "off",
                },
                clear=False,
            )
            env.start()
            try:
                start = handle(
                    "claude",
                    {"session_id": "wt1", "hook_event_name": "SessionStart", "cwd": str(wt)},
                )
                ctx = start["hookSpecificOutput"]["additionalContext"]
                self.assertIn("root=none", ctx)
                self.assertIn("prefs=", ctx)
                self.assertIn("never write primary .agent", ctx)

                denied = handle(
                    "claude",
                    {
                        "session_id": "wt1",
                        "hook_event_name": "PreToolUse",
                        "cwd": str(wt),
                        "tool_name": "Write",
                        "tool_input": {"file_path": str(agent / "index.md")},
                    },
                )
                self.assertEqual("deny", denied["hookSpecificOutput"]["permissionDecision"])
                self.assertIn("linked worktree", denied["hookSpecificOutput"]["permissionDecisionReason"])
            finally:
                env.stop()


class InstallerTest(unittest.TestCase):
    def test_installer_uses_supported_event_sets_and_host_argument(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            claude = Path(temp) / "claude.json"
            codex = Path(temp) / "codex.json"
            merge_file(claude, "claude")
            merge_file(codex, "codex")
            claude_data = json.loads(claude.read_text(encoding="utf-8"))
            codex_data = json.loads(codex.read_text(encoding="utf-8"))

        self.assertEqual(set(HOST_EVENTS["claude"]), set(claude_data["hooks"]))
        self.assertEqual(set(HOST_EVENTS["codex"]), set(codex_data["hooks"]))
        self.assertIn("--host claude", claude_data["hooks"]["SessionStart"][0]["hooks"][0]["command"])
        self.assertIn("--host codex", codex_data["hooks"]["SessionStart"][0]["hooks"][0]["command"])


if __name__ == "__main__":
    unittest.main()
