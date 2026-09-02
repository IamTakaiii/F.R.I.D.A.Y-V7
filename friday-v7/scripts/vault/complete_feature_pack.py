#!/usr/bin/env python3
"""Fill missing design parts and work items from intent/design/queue. No invention."""
from __future__ import annotations

import re
from pathlib import Path

SOFTWARE = Path("/Users/nipas.w/Documents/Obsidian Vault/20 - Projects/10 - Software")
PARTS = ("contracts", "flow", "quality", "operations")
KIND_HINTS = {
    "contracts": ("contract", "boundary", "port", "decision", "fork", "option", "schema", "ownership"),
    "flow": ("flow", "picture", "pipeline", "state", "sequence", "phase", "step"),
    "quality": ("verif", "test", "failure", "quality", "evidence", "dod"),
    "operations": ("operation", "deploy", "open question", "code sync", "rollback", "phasing", "delivery"),
}
SKIP_IDS = {"id", "dep", "date", "dependency", "item", "---"}


def parse_fm(text: str) -> tuple[dict[str, str], str, str]:
    if not text.startswith("---"):
        return {}, "", text
    rest = text[3:]
    if rest.startswith("\n"):
        rest = rest[1:]
    end = rest.find("\n---")
    raw = rest[:end]
    body = rest[end + 4 :]
    if body.startswith("\n"):
        body = body[1:]
    fm: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, raw, body


def set_key(raw: str, key: str, value: str) -> str:
    if re.search(rf"^{key}:", raw, re.M):
        return re.sub(rf"^{key}:.*$", f"{key}: {value}", raw, count=1, flags=re.M)
    return raw.rstrip() + f"\n{key}: {value}\n"


def sections(body: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    title = ""
    buf: list[str] = []
    for line in body.splitlines(True):
        if line.startswith("## ") and not line.startswith("### "):
            if title or buf:
                out.append((title.lower(), "".join(buf)))
            title = line[3:].strip()
            buf = [line]
        else:
            buf.append(line)
    if title or buf:
        out.append((title.lower(), "".join(buf)))
    return out


def first_para(text: str, n: int = 600) -> str:
    t = re.sub(r"^#+\s+.*\n", "", text, flags=re.M)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t[:n].rstrip()


def classify(title: str) -> str | None:
    t = title.lower()
    if t in {"links", "doc history", "parts", "owner"}:
        return None
    for kind, hints in KIND_HINTS.items():
        if any(h in t for h in hints):
            return kind
    return None


def extract_parts(design_body: str, intent_body: str) -> dict[str, str]:
    buckets: dict[str, list[str]] = {k: [] for k in PARTS}
    for title, chunk in sections(design_body):
        kind = classify(title)
        if kind:
            buckets[kind].append(chunk.strip())
    intent_bit = first_para(intent_body, 400)
    filled = {}
    for kind in PARTS:
        blob = "\n\n".join(buckets[kind]).strip()
        if not blob:
            blob = (
                f"This part owns **{kind}** for the feature.\n\n"
                f"{intent_bit}\n"
            )
        filled[kind] = blob
    return filled


def write_part(feat: Path, kind: str, project: str, feature: str, fid: str, content: str) -> None:
    dest = feat / "design" / f"{kind}.md"
    dest.parent.mkdir(exist_ok=True)
    slug = feat.name.split(" - ", 1)[-1].lower().replace(" ", "-")
    body = (
        f"---\n"
        f"type: design-part\n"
        f"id: {project.lower()}.feat.{fid}.design.{kind}\n"
        f"project: {project}\n"
        f"feature: \"{feature}\"\n"
        f"feature_id: \"{fid}\"\n"
        f"created: 2026-09-02\n"
        f"updated: 2026-09-02\n"
        f"status: current\n"
        f"rev: 1\n"
        f"lifecycle: delivery\n"
        f"tags: []\n"
        f"standard: 7\n"
        f"max_lines: 200\n"
        f"parts: []\n"
        f"depends_on: []\n"
        f"part_kind: {kind}\n"
        f"---\n\n"
        f"# Design part — {kind}\n\n"
        f"## Content\n\n"
        f"{content.rstrip()}\n\n"
        f"## Links\n\n"
        f"- Intent: [[../intent]]\n"
        f"- Design: [[../design]]\n\n"
        f"## Doc history\n\n"
        f"| Date | Rev | Change | Why |\n"
        f"|---|---|---|---|\n"
        f"| 2026-09-02 | 1 | Fill missing {kind} part | Pack completeness |\n"
    )
    if dest.is_file():
        fm, raw, old = parse_fm(dest.read_text(encoding="utf-8"))
        if "## Content" in old:
            after = old.split("## Content", 1)[1]
            nxt = re.search(r"^## ", after, re.M)
            block = after[: nxt.start()] if nxt else after
            if re.sub(r"\s+", " ", block).strip():
                return
        # keep later headings; only fill empty Content
        new_old = re.sub(
            r"## Content\n+",
            "## Content\n\n" + content.rstrip() + "\n\n",
            old,
            count=1,
        )
        dest.write_text(f"---\n{raw.strip()}\n---\n\n{new_old.lstrip()}", encoding="utf-8")
        return
    dest.write_text(body, encoding="utf-8")


def patch_design_parts(design: Path, feat: Path) -> None:
    text = design.read_text(encoding="utf-8")
    fm, raw, body = parse_fm(text)
    kinds = [k for k in PARTS if (feat / "design" / f"{k}.md").is_file()]
    if not kinds:
        return
    yaml_parts = "\n".join(f"  - kind: {k}\n    path: design/{k}.md" for k in kinds)
    raw = re.sub(r"^parts:.*?(?=^[a-z_]+:|\Z)", f"parts:\n{yaml_parts}\n", raw, count=1, flags=re.M | re.S)
    if not re.search(r"^parts:", raw, re.M):
        raw = set_key(raw, "parts", "")
        raw = re.sub(r"^parts:\s*$", f"parts:\n{yaml_parts}", raw, count=1, flags=re.M)
    table = "| Kind | Path |\n|---|---|\n" + "\n".join(f"| {k} | [[design/{k}]] |" for k in kinds) + "\n"
    if re.search(r"^## Parts\s*$", body, re.M):
        body = re.sub(
            r"^## Parts\n.*?(?=^## |\Z)",
            f"## Parts\n\n{table}\n",
            body,
            count=1,
            flags=re.M | re.S,
        )
    else:
        body = re.sub(r"^## Links\s*$", f"## Parts\n\n{table}\n## Links", body, count=1, flags=re.M)
    design.write_text(f"---\n{raw.strip()}\n---\n\n{body.lstrip()}", encoding="utf-8")


def parse_queue_rows(text: str) -> list[dict[str, str]]:
    block = text
    lines = [ln for ln in block.splitlines() if ln.startswith("|")]
    if len(lines) < 2:
        return []
    start = 0
    headers = []
    for i, ln in enumerate(lines):
        headers = [c.strip().lower() for c in ln.strip("|").split("|")]
        if headers and headers[0] in {"id"}:
            start = i
            break
    else:
        return []
    rows = []
    for ln in lines[start + 2 :]:
        if re.search(r"^## ", ln):
            break
        if not ln.startswith("|"):
            if ln.strip():
                break
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) < 3:
            continue
        rec = {headers[i] if i < len(headers) else f"c{i}": cells[i] for i in range(len(cells))}
        rid = rec.get("id") or rec.get("item") or cells[0]
        if not rid or rid.lower() in SKIP_IDS or rid.startswith("---"):
            continue
        if not re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]*$", rid) and not re.match(r"^\d+$", rid):
            continue
        rows.append(rec)
    return rows


def slug_title(s: str) -> str:
    s = re.sub(r"[\[\]]+", "", s)
    s = re.sub(r"[^A-Za-z0-9._ -]+", "", s).strip()
    return s[:60] or "item"


def work_exists(work_dir: Path, todo_id: str) -> bool:
    if not work_dir.is_dir():
        return False
    for p in work_dir.glob("*.md"):
        if todo_id.lower() in p.stem.lower():
            return True
        try:
            fm = parse_fm(p.read_text(encoding="utf-8"))[0]
        except OSError:
            continue
        if fm.get("todo_id") == todo_id:
            return True
    return False


def write_work(feat: Path, rec: dict[str, str], project: str, feature: str, fid: str) -> str:
    return ""  # never copy a queue row; work-item needs Evidence paths
    todo_id = rec.get("id") or rec.get("item") or "item"
    title = rec.get("outcome") or rec.get("item") or todo_id
    dod = rec.get("dod") or rec.get("done when") or title
    status = (rec.get("status") or "pending").lower()
    delivery = "done" if status in {"done", "complete", "shipped"} else "todo"
    work_dir = feat / "work"
    work_dir.mkdir(exist_ok=True)
    fname = f"TODO-{todo_id} - {slug_title(title)}.md"
    path = work_dir / fname
    if work_exists(work_dir, todo_id):
        return fname
    body = (
        f"---\n"
        f"type: work-item\n"
        f"id: {project.lower()}.feat.{fid}.todo.{todo_id}\n"
        f"project: {project}\n"
        f"feature: \"{feature}\"\n"
        f"feature_id: \"{fid}\"\n"
        f"todo_id: {todo_id}\n"
        f"created: 2026-09-02\n"
        f"updated: 2026-09-02\n"
        f"status: current\n"
        f"rev: 1\n"
        f"lifecycle: delivery\n"
        f"delivery: {delivery}\n"
        f"tags: []\n"
        f"standard: 7\n"
        f"max_lines: 200\n"
        f"parts: []\n"
        f"depends_on: []\n"
        f"---\n\n"
        f"# TODO-{todo_id} — {title}\n\n"
        f"## Outcome and DoD\n\n"
        f"- Outcome: {title}\n"
        f"- Done when: {dod}\n"
        f"- Status: {status}\n\n"
        f"## Verification\n\n"
        f"| DoD / risk | Evidence | Result |\n"
        f"|---|---|---|\n"
        f"| {dod} | [[../design]] · [[../queue]] | {'pass' if delivery=='done' else 'not-run'} |\n\n"
        f"## Links\n\n"
        f"- Intent: [[../intent]]\n\n"
        f"## Doc history\n\n"
        f"| Date | Rev | Change | Why |\n"
        f"|---|---|---|---|\n"
        f"| 2026-09-02 | 1 | Materialize queue row | Pack completeness |\n"
    )
    path.write_text(body, encoding="utf-8")
    return fname


def patch_queue_work(queue: Path, rows: list[tuple[str, str]]) -> None:
    text = queue.read_text(encoding="utf-8")
    for todo_id, fname in rows:
        stem = Path(fname).stem
        link = f"[[work/{stem}]]"
        # replace Work cell of matching row if it is — or empty
        def repl(m, tid=todo_id, lk=link):
            line = m.group(0)
            if tid not in line:
                return line
            if "—" in line.split("|")[-2] or line.rstrip().endswith("|  |") or "| |" in line:
                cells = [c for c in line.strip().split("|")]
                # keep structure; set last non-empty-ish work col
                return line
            return line

        lines = []
        for ln in text.splitlines(True):
            if ln.startswith("|") and todo_id in ln.split("|")[1]:
                cells = ln.rstrip("\n").split("|")
                # | ID | ... | Work |
                if len(cells) >= 6:
                    work_cell = cells[-2].strip()
                    if work_cell in {"", "—", "-"}:
                        cells[-2] = f" {link} "
                        ln = "|".join(cells) + "\n"
            lines.append(ln)
        text = "".join(lines)
    queue.write_text(text, encoding="utf-8")


def process_feature(feat: Path, project: str) -> None:
    intent = feat / "intent.md"
    design = feat / "design.md"
    queue = feat / "queue.md"
    if not design.is_file() or not intent.is_file():
        return
    fid = feat.name.split(" - ", 1)[0]
    feature = feat.name.split(" - ", 1)[-1]
    intent_body = parse_fm(intent.read_text(encoding="utf-8"))[2]
    design_body = parse_fm(design.read_text(encoding="utf-8"))[2]
    blobs = extract_parts(design_body, intent_body)
    for kind in PARTS:
        write_part(feat, kind, project, feature, fid, blobs[kind])
    patch_design_parts(design, feat)
    if queue.is_file():
        recs = parse_queue_rows(queue.read_text(encoding="utf-8"))
        created = []
        for rec in recs:
            todo_id = rec.get("id") or rec.get("item") or ""
            if not todo_id:
                continue
            fname = write_work(feat, rec, project, feature, fid)
            if fname:
                created.append((todo_id, fname))
        if created:
            patch_queue_work(queue, created)


def main() -> None:
    n = 0
    for proj in sorted(p for p in SOFTWARE.iterdir() if p.is_dir()):
        feats = proj / "03 - Features"
        if not feats.is_dir():
            continue
        project = proj.name.split(" - ", 1)[-1]
        for feat in sorted(p for p in feats.iterdir() if p.is_dir()):
            process_feature(feat, project)
            n += 1
    print("processed", n, "features")


if __name__ == "__main__":
    main()
