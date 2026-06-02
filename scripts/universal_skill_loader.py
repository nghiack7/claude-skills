from __future__ import annotations

import argparse
import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


DOC_CANDIDATES = ("SKILL.md", "skill.md")
MANAGED_BEGIN = "<!-- shared-skill-loader:begin -->"
MANAGED_END = "<!-- shared-skill-loader:end -->"
WORKPLACE_VAR = "WORKPLACE"


@dataclass(frozen=True)
class SkillEntry:
    name: str
    directory: Path
    doc_path: Path
    asset_paths: tuple[Path, ...]


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_always_load_path() -> Path:
    return repo_root() / "always-load.json"


def default_workplace_root() -> Path:
    return repo_root().parents[1]


def display_path(path: Path) -> str:
    resolved_path = path.expanduser().resolve()
    workplace_root = Path(os.environ.get(WORKPLACE_VAR, default_workplace_root())).expanduser().resolve()
    try:
        return f"${WORKPLACE_VAR}/{resolved_path.relative_to(workplace_root).as_posix()}"
    except ValueError:
        return str(path)


def discover_skills(source_dir: Path) -> list[SkillEntry]:
    skills: list[SkillEntry] = []
    for entry in sorted(source_dir.iterdir(), key=lambda item: item.name):
        if not entry.is_dir() or entry.name.startswith("."):
            continue

        children = {child.name: child for child in entry.iterdir()}
        doc_path = next((children[name] for name in DOC_CANDIDATES if name in children and children[name].is_file()), None)
        if doc_path is None:
            continue

        assets = tuple(
            sorted(
                (
                    child
                    for child in entry.iterdir()
                    if child.name not in DOC_CANDIDATES and not child.name.startswith(".")
                ),
                key=lambda child: child.name,
            )
        )
        skills.append(
            SkillEntry(
                name=entry.name,
                directory=entry,
                doc_path=doc_path,
                asset_paths=assets,
            )
        )
    return skills


def build_adapters(source_dir: Path, output_dir: Path, always_load_path: Path | None = None) -> list[SkillEntry]:
    skills = discover_skills(source_dir)
    resolved_source_dir = source_dir.resolve()
    if always_load_path is not None:
        resolved_always_load_path = always_load_path
    elif resolved_source_dir == (repo_root() / "skills").resolve():
        resolved_always_load_path = default_always_load_path()
    else:
        resolved_always_load_path = None

    always_load_skills = _resolve_always_load_skills(
        skills=skills,
        always_load_path=resolved_always_load_path,
    )

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "source_dir": display_path(source_dir),
        "skill_count": len(skills),
        "skills": [
            {
                "name": skill.name,
                "source_dir": display_path(skill.directory),
                "doc_path": display_path(skill.doc_path),
                "assets": [display_path(asset) for asset in skill.asset_paths],
            }
            for skill in skills
        ],
    }

    for tool in ("claude", "codex"):
        _build_skill_mirror(skills, output_dir / tool / "skills")
        _write_text(
            output_dir / tool / ("CLAUDE.md" if tool == "claude" else "AGENTS.md"),
            _render_tool_loader_doc(
                tool=tool,
                source_dir=source_dir,
                skills_dir=output_dir / tool / "skills",
                always_load_skills=always_load_skills,
            ),
        )

    _build_cursor_loader(skills, always_load_skills, source_dir, output_dir / "cursor")
    _write_text(output_dir / "manifest.json", json.dumps(manifest, indent=2) + "\n")
    return skills


def install(
    source_dir: Path,
    output_dir: Path,
    claude_home: Path,
    codex_home: Path,
    cursor_home: Path,
    always_load_path: Path,
    cursor_repos: Iterable[Path] = (),
) -> list[SkillEntry]:
    skills = build_adapters(source_dir, output_dir, always_load_path=always_load_path)
    backup_root = output_dir / "backups" / datetime.now().strftime("%Y%m%d-%H%M%S")

    _install_tool_skills(
        tool="claude",
        target_home=claude_home,
        generated_root=output_dir / "claude",
        backup_root=backup_root / "claude",
    )
    _install_tool_skills(
        tool="codex",
        target_home=codex_home,
        generated_root=output_dir / "codex",
        backup_root=backup_root / "codex",
    )
    _install_cursor_home(cursor_home, output_dir / "cursor")
    for repo in cursor_repos:
        _install_cursor_repo(repo, output_dir / "cursor")
    return skills


def _build_skill_mirror(skills: list[SkillEntry], destination_root: Path) -> None:
    destination_root.mkdir(parents=True, exist_ok=True)
    for skill in skills:
        skill_dir = destination_root / skill.name
        skill_dir.mkdir(parents=True, exist_ok=True)
        _symlink_or_copy(skill.doc_path, skill_dir / "SKILL.md")
        for asset in skill.asset_paths:
            _symlink_or_copy(asset, skill_dir / asset.name)


def _build_cursor_loader(
    skills: list[SkillEntry],
    always_load_skills: list[SkillEntry],
    source_dir: Path,
    cursor_root: Path,
) -> None:
    rule_dir = cursor_root / ".cursor" / "rules"
    rule_dir.mkdir(parents=True, exist_ok=True)
    catalog_path = cursor_root / "skill-catalog.md"
    _write_text(catalog_path, _render_cursor_catalog(skills))
    _write_text(
        rule_dir / "00-universal-skill-loader.mdc",
        _render_cursor_rule(
            source_dir=source_dir,
            catalog_path=catalog_path,
            skills=skills,
            always_load_skills=always_load_skills,
        ),
    )


def _render_tool_loader_doc(
    tool: str,
    source_dir: Path,
    skills_dir: Path,
    always_load_skills: list[SkillEntry],
) -> str:
    title = "Claude" if tool == "claude" else "Codex"
    text = (
        f"# Shared Skill Loader\n\n"
        f"This file is generated. The canonical skill source lives at:\n"
        f"`{display_path(source_dir)}`\n\n"
        f"Normalized {title} skill mirror:\n"
        f"`{display_path(skills_dir)}`\n\n"
        "Do not edit generated mirrors directly. Update the source skill directory and rerun the loader.\n"
    )
    if always_load_skills:
        text += "\n## Always-Load Skills\n\n"
        text += "The following shared skills are trusted defaults and should be treated as active guidance in every session.\n\n"
        for skill in always_load_skills:
            text += f"### {skill.name}\n\n"
            text += skill.doc_path.read_text(encoding="utf-8").strip() + "\n\n"
    return text


def _render_cursor_catalog(skills: list[SkillEntry]) -> str:
    lines = [
        "# Shared Skill Catalog",
        "",
        "Canonical source for all skills. Resolve a skill by name and read its source markdown file.",
        "",
    ]
    for skill in skills:
        lines.append(f"- `{skill.name}`: `{display_path(skill.doc_path)}`")
    lines.append("")
    return "\n".join(lines)


def _render_cursor_rule(
    source_dir: Path,
    catalog_path: Path,
    skills: list[SkillEntry],
    always_load_skills: list[SkillEntry],
) -> str:
    skill_names = ", ".join(skill.name for skill in skills)
    text = (
        "---\n"
        "description: Load shared skills from the central skill repository\n"
        "globs:\n"
        "alwaysApply: true\n"
        "---\n\n"
        "# Shared Skill Loader\n\n"
        f"Canonical shared skill source: `{display_path(source_dir)}`\n\n"
        f"Catalog of skills: `{display_path(catalog_path)}`\n\n"
        "When a task matches or names a skill, open the matching source file from the shared repository instead of inventing a local copy.\n\n"
        f"Available shared skills: {skill_names}\n"
    )
    if always_load_skills:
        text += "\n## Always-Load Skills\n\n"
        text += "These trusted shared skills are part of the default operating rules for every session:\n\n"
        for skill in always_load_skills:
            text += f"### {skill.name}\n\n"
            text += skill.doc_path.read_text(encoding="utf-8").strip() + "\n\n"
    return text


def _resolve_always_load_skills(skills: list[SkillEntry], always_load_path: Path | None) -> list[SkillEntry]:
    if always_load_path is None or not always_load_path.exists():
        return []

    names = json.loads(always_load_path.read_text(encoding="utf-8"))
    skill_map = {skill.name: skill for skill in skills}
    missing = [name for name in names if name not in skill_map]
    if missing:
        missing_list = ", ".join(missing)
        raise ValueError(f"always-load skill not found: {missing_list}")
    return [skill_map[name] for name in names]


def _install_tool_skills(tool: str, target_home: Path, generated_root: Path, backup_root: Path) -> None:
    skills_dir = target_home / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    generated_skills_dir = generated_root / "skills"

    for generated_skill_dir in sorted(generated_skills_dir.iterdir(), key=lambda item: item.name):
        destination = skills_dir / generated_skill_dir.name
        _replace_with_symlink(destination, generated_skill_dir, backup_root / "skills")

    index_file = target_home / ("CLAUDE.md" if tool == "claude" else "AGENTS.md")
    loader_doc = generated_root / ("CLAUDE.md" if tool == "claude" else "AGENTS.md")
    loader_text = loader_doc.read_text(encoding="utf-8").strip()
    _upsert_managed_block(
        index_file,
        (
            f"{MANAGED_BEGIN}\n"
            f"{loader_text}\n"
            f"{MANAGED_END}\n"
        ),
    )


def _install_cursor_home(cursor_home: Path, generated_root: Path) -> None:
    cursor_rules_dir = cursor_home / "rules"
    cursor_rules_dir.mkdir(parents=True, exist_ok=True)
    _replace_with_symlink(
        cursor_rules_dir / "00-universal-skill-loader.mdc",
        generated_root / ".cursor" / "rules" / "00-universal-skill-loader.mdc",
        generated_root / "backups" / "cursor-home",
    )
    _replace_with_symlink(
        cursor_home / "skill-catalog.md",
        generated_root / "skill-catalog.md",
        generated_root / "backups" / "cursor-home",
    )


def _install_cursor_repo(repo_dir: Path, generated_root: Path) -> None:
    repo_rules_dir = repo_dir / ".cursor"
    repo_rules_dir.mkdir(parents=True, exist_ok=True)
    _replace_with_symlink(
        repo_rules_dir / "rules",
        generated_root / ".cursor" / "rules",
        generated_root / "backups" / "cursor-repos" / repo_dir.name,
    )


def _replace_with_symlink(destination: Path, source: Path, backup_dir: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        current = destination.resolve()
        if current == source.resolve():
            return
        destination.unlink()
    elif destination.exists():
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / destination.name
        if backup_path.exists() or backup_path.is_symlink():
            if backup_path.is_dir() and not backup_path.is_symlink():
                shutil.rmtree(backup_path)
            else:
                backup_path.unlink()
        shutil.move(str(destination), str(backup_path))

    os.symlink(source, destination)


def _symlink_or_copy(source: Path, destination: Path) -> None:
    if destination.exists() or destination.is_symlink():
        if destination.is_dir() and not destination.is_symlink():
            shutil.rmtree(destination)
        else:
            destination.unlink()

    try:
        os.symlink(source, destination)
    except OSError:
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)


def _upsert_managed_block(path: Path, block: str) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if MANAGED_BEGIN in existing and MANAGED_END in existing:
        start = existing.index(MANAGED_BEGIN)
        end = existing.index(MANAGED_END) + len(MANAGED_END)
        updated = existing[:start] + block + existing[end:]
    else:
        separator = "\n" if existing and not existing.endswith("\n") else ""
        updated = f"{existing}{separator}{block}"
    _write_text(path, updated)


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build and install shared skill adapters for multiple AI tools.")
    parser.add_argument("command", choices=("build", "install"))
    parser.add_argument("--source", type=Path, default=repo_root() / "skills")
    parser.add_argument("--output", type=Path, default=repo_root() / ".generated")
    parser.add_argument("--claude-home", type=Path, default=Path.home() / ".claude")
    parser.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
    parser.add_argument("--cursor-home", type=Path, default=Path.home() / ".cursor")
    parser.add_argument("--cursor-repo", type=Path, action="append", default=[])
    parser.add_argument("--always-load", type=Path, default=default_always_load_path())
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "build":
        build_adapters(args.source, args.output, always_load_path=args.always_load)
        return 0

    install(
        source_dir=args.source,
        output_dir=args.output,
        claude_home=args.claude_home,
        codex_home=args.codex_home,
        cursor_home=args.cursor_home,
        always_load_path=args.always_load,
        cursor_repos=args.cursor_repo,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
