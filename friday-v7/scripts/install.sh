#!/usr/bin/env bash
# Symlink this clone into skill folders.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ROOT_P="$(cd "$ROOT" && pwd -P)"
LINK_NAME="${FRIDAY_SKILL_NAME:-friday-v7}"

if [[ ! -f "$ROOT/SKILL.md" ]]; then
  echo "error: SKILL.md not found under $ROOT" >&2
  exit 1
fi

same_clone() {
  local p="$1"
  [[ -d "$p" ]] || return 1
  [[ "$(cd "$p" && pwd -P)" == "$ROOT_P" ]]
}

unwrap_if_workspace_parent() {
  local dest_dir="$1"
  [[ -L "$dest_dir" ]] || return 0
  local resolved
  resolved="$(cd "$dest_dir" && pwd -P)"
  if [[ "$ROOT_P" == "$resolved" || "$ROOT_P" == "$resolved"/* ]]; then
    rm "$dest_dir"
    mkdir -p "$dest_dir"
    echo "unwrapped: $dest_dir (was $resolved)"
  fi
}

prune_stale_surfaces() {
  local dest_dir="$1"
  local label="$2"
  local st name
  for st in "$dest_dir"/fr "$dest_dir"/fr-*; do
    [[ -L "$st" ]] || continue
    name="$(basename "$st")"
    if [[ ! -f "$ROOT/surfaces/$name/SKILL.md" ]]; then
      rm -f "$st"
      echo "pruned ($label): $st"
    fi
  done
}

prune_dangling_legacy() {
  local dest_dir="$1"
  local label="$2"
  local p="$dest_dir/friday-v6"
  [[ -L "$p" && ! -e "$p" ]] || return 0
  rm -f "$p"
  echo "pruned ($label): $p (dangling)"
}

link_tree() {
  local dest_dir="$1"
  local label="$2"
  mkdir -p "$dest_dir"
  local target="$dest_dir/$LINK_NAME"
  if same_clone "$target" && [[ ! -L "$target" ]]; then
    echo "skip ($label): $target is this clone"
  elif [[ -e "$target" && ! -L "$target" ]]; then
    echo "error: $target exists and is not a symlink — move it aside first" >&2
    exit 1
  else
    ln -sfn "$ROOT" "$target"
    echo "linked ($label): $target -> $ROOT"
  fi

  if [[ "${3:-}" == "surfaces" ]]; then
    local surf
    for surf in "$ROOT"/surfaces/*; do
      [[ -d "$surf" && -f "$surf/SKILL.md" ]] || continue
      local name
      name="$(basename "$surf")"
      local st="$dest_dir/$name"
      if [[ -e "$st" && ! -L "$st" ]]; then
        echo "skip ($label): $st exists and is not a symlink"
        continue
      fi
      ln -sfn "$surf" "$st"
    done
    prune_stale_surfaces "$dest_dir" "$label"
  fi
  prune_dangling_legacy "$dest_dir" "$label"
}

link_opencode_commands() {
  local src="$ROOT/hosts/opencode/commands"
  local dest="${OPENCODE_COMMANDS_DIR:-$HOME/.config/opencode/commands}"
  mkdir -p "$dest"
  local f name
  for f in "$src"/*.md; do
    [[ -f "$f" ]] || continue
    name="$(basename "$f")"
    ln -sfn "$f" "$dest/$name"
    echo "linked (opencode commands): $dest/$name"
  done
  local st base
  for st in "$dest"/fr.md "$dest"/fr-*.md; do
    [[ -e "$st" || -L "$st" ]] || continue
    base="$(basename "$st")"
    if [[ ! -f "$src/$base" ]]; then
      rm -f "$st"
      echo "pruned (opencode commands): $st"
    fi
  done
}

OPENCODE_DIR="${OPENCODE_SKILLS_DIR:-$HOME/.config/opencode/skills}"
CLAUDE_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
CODEX_DIR="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"

unwrap_if_workspace_parent "$OPENCODE_DIR"
link_tree "$OPENCODE_DIR" "opencode"
link_opencode_commands
link_tree "$CLAUDE_DIR" "claude" surfaces
link_tree "$CODEX_DIR" "codex" surfaces

python3 "$ROOT/hosts/install_hooks.py"

echo
echo "OpenCode / Claude / Codex: restart. Codex: /hooks then trust."
echo "v7 is linked as $LINK_NAME."
echo "Brain default: local (~/.local/share/friday). Obsidian opt-in: set brain.backend + brain.root."
