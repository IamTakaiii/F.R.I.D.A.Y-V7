#!/usr/bin/env python3
"""Mechanical v6 → v7 vault migrate. Default is dry-run. Wikilinks updated in-place."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FILE_RENAMES = {
    "01 - Intent.md": "intent.md",
    "02 - Design.md": "design.md",
    "03 - TODO.md": "queue.md",
    "01 - Project Brief.md": "01 - Brief.md",
    "01 - System.md": "01 - Architecture.md",
    "02 - Stack.md": "stack.md",
}
DIR_RENAMES = {
    "01 - API": "api",
    "02 - Work": "work",
    "03 - Fixes": "fixes",
    "04 - Reports": "reports",
    "06 - Plans": "plans",
    "99 - Notes": "89-Notes",
}
# project-level only (direct child of NN - Project)
PROJECT_DIR_RENAMES = {
    "05 - Ship": "06 - Ship",
    "06 - Operations": "07 - Operations",
}
TYPE_MAP = {
    "project-brief": "brief",
    "personal-brief": "brief",
    "todo-board": "queue",
    "todo-item": "work-item",
    "todo": "work-item",
    "design-slice": "design-part",
    "stack": "architecture-part",
    "review": "quality-report",
    "review-report": "quality-report",
    "test-report": "quality-report",
    "perf-report": "quality-report",
    "timeline": "timeline-log",
    "guide": "note",
}
LINK_RE = [
    (re.compile(r"\[\[([^\]|#]*?)01 - Intent(\|[^\]]*)?\]\]"), r"[[\1intent\2]]"),
    (re.compile(r"\[\[([^\]|#]*?)02 - Design(\|[^\]]*)?\]\]"), r"[[\1design\2]]"),
    (re.compile(r"\[\[([^\]|#]*?)03 - TODO(\|[^\]]*)?\]\]"), r"[[\1queue\2]]"),
    (re.compile(r"01 - API/"), "api/"),
    (re.compile(r"02 - Work/"), "work/"),
    (re.compile(r"03 - Fixes/"), "fixes/"),
    (re.compile(r"04 - Reports/"), "reports/"),
    (re.compile(r"06 - Plans/"), "plans/"),
]


def is_project_root(path: Path, projects: Path) -> bool:
    try:
        rel = path.relative_to(projects)
    except ValueError:
        return False
    parts = rel.parts
    return len(parts) == 3 and parts[0] in {"10 - Software", "20 - Personal"}


def plan_renames(projects: Path) -> list[tuple[Path, Path]]:
    moves: list[tuple[Path, Path]] = []
    for src_name, dst_name in DIR_RENAMES.items():
        for src in projects.rglob(src_name):
            if src.is_dir():
                moves.append((src, src.with_name(dst_name)))
    for src_name, dst_name in PROJECT_DIR_RENAMES.items():
        for src in projects.rglob(src_name):
            if src.is_dir() and is_project_root(src, projects):
                dest = src.with_name(dst_name)
                if dest.exists() and dest.resolve() != src.resolve():
                    continue
                moves.append((src, dest))
    for src_name, dst_name in FILE_RENAMES.items():
        for src in projects.rglob(src_name):
            if src.is_file():
                moves.append((src, src.with_name(dst_name)))
    # deepest first
    moves.sort(key=lambda x: len(x[0].parts), reverse=True)
    return moves


def patch_frontmatter(text: str) -> tuple[str, bool]:
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return text, False
    fm = m.group(1)
    rest = text[m.end() :]
    changed = False

    def sub_type(mo: re.Match[str]) -> str:
        nonlocal changed
        old = mo.group(1)
        new = TYPE_MAP.get(old, old)
        if new != old:
            changed = True
        return f"type: {new}"

    fm2 = re.sub(r"^type:\s*(\S+)", sub_type, fm, flags=re.M)
    if re.search(r"^type:\s*brief\s*$", fm2, re.M) and not re.search(
        r"^project_kind:", fm2, re.M
    ):
        fm2 += "\nproject_kind: software"
        changed = True
    if re.search(r"^type:\s*architecture-part\s*$", fm2, re.M) and not re.search(
        r"^part_kind:", fm2, re.M
    ):
        fm2 += "\npart_kind: stack"
        changed = True
    if re.search(r"^type:\s*quality-report\s*$", fm2, re.M) and not re.search(
        r"^kind:", fm2, re.M
    ):
        fm2 += "\nkind: review"
        changed = True
    for key in ("load_profile", "doc_status"):
        nfm, n = re.subn(rf"^{key}:.*\n?", "", fm2, flags=re.M)
        if n:
            fm2 = nfm
            changed = True
    if not re.search(r"^standard:", fm2, re.M):
        fm2 += "\nstandard: 7"
        changed = True
    if not re.search(r"^max_lines:", fm2, re.M):
        fm2 += "\nmax_lines: 80"
        changed = True
    if fm2 != fm:
        changed = True
    if not changed:
        return text, False
    return f"---\n{fm2.strip()}\n---\n{rest}", True


def patch_links(text: str) -> tuple[str, bool]:
    out = text
    changed = False
    for rx, repl in LINK_RE:
        nout, n = rx.subn(repl, out)
        if n:
            out = nout
            changed = True
    return out, changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    vault = Path(args.vault).expanduser()
    projects = vault / "20 - Projects"
    if not projects.is_dir():
        print("FAIL no 20 - Projects under", vault, file=sys.stderr)
        return 1

    moves = plan_renames(projects)
    print(f"{'APPLY' if args.apply else 'DRY-RUN'} {len(moves)} renames")
    for src, dst in moves:
        print(f"  mv {src.relative_to(vault)} → {dst.relative_to(vault)}")
        if args.apply:
            dst.parent.mkdir(parents=True, exist_ok=True)
            src.rename(dst)

    patched = 0
    for path in projects.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        text, a = patch_frontmatter(text)
        text, b = patch_links(text)
        if a or b:
            patched += 1
            if args.apply:
                path.write_text(text, encoding="utf-8")
    print(f"{'patched' if args.apply else 'would patch'} {patched} markdown files")
    if not args.apply:
        print("Re-run with --apply to write.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
