"""Inject Git-derived 'updated' dates into Markdown front matter.

Workflow:
    python scripts/inject_git_dates.py [--check]

Pour chaque fichier ``docs/**/*.md`` :
    1. récupère la date du dernier commit Git qui l'a modifié,
    2. fallback sur mtime si le fichier n'est pas dans l'historique,
    3. met à jour la clé ``updated`` du front matter YAML,
    4. ne réécrit le fichier que si la valeur change.
"""
from __future__ import annotations

import argparse
import io
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml


def git_last_modified_date(file: Path, repo_root: Path) -> str:
    """Retourne la date ISO (YYYY-MM-DD) du dernier commit touchant `file`.

    Fallback sur le mtime du filesystem si le fichier n'a pas d'historique Git
    (untracked ou repo en shallow clone sans le commit pertinent).
    """
    relative = file.relative_to(repo_root)
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cI", "--", str(relative)],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = result.stdout.strip()
    if result.returncode == 0 and stdout:
        return stdout[:10]  # garde uniquement YYYY-MM-DD
    # Fallback : mtime
    mtime = datetime.fromtimestamp(file.stat().st_mtime, tz=timezone.utc)
    return mtime.date().isoformat()


_FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)


def update_front_matter(content: str, updated: str) -> tuple[str, bool]:
    """Retourne (nouveau_contenu, a_change).

    - Si le bloc front matter existe et contient déjà ``updated == updated``,
      renvoie le contenu inchangé et ``False``.
    - Sinon, met à jour ou ajoute la clé ``updated`` et renvoie ``True``.
    - Si aucun front matter n'existe, en crée un minimal.
    """
    match = _FRONT_MATTER_RE.match(content)
    if match:
        yaml_block = match.group(1)
        body = content[match.end():]
        data = yaml.safe_load(yaml_block) or {}
        if not isinstance(data, dict):
            raise ValueError(
                "Front matter YAML doit être un mapping, "
                f"trouvé : {type(data).__name__}"
            )
        if data.get("updated") == updated:
            return content, False
        data["updated"] = updated
        new_yaml = _dump_yaml(data)
        return f"---\n{new_yaml}---\n{body}", True
    else:
        data = {"updated": updated}
        new_yaml = _dump_yaml(data)
        return f"---\n{new_yaml}---\n\n{content.lstrip()}", True


def _dump_yaml(data: dict) -> str:
    buffer = io.StringIO()
    yaml.safe_dump(
        data,
        buffer,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )
    return buffer.getvalue()


def process_file(file: Path, repo_root: Path) -> bool:
    """Met à jour le front matter d'un fichier Markdown si nécessaire.

    Retourne True si le fichier a été réécrit, False sinon.
    """
    updated = git_last_modified_date(file, repo_root=repo_root)
    original = file.read_text(encoding="utf-8")
    new_content, changed = update_front_matter(original, updated)
    if changed:
        file.write_text(new_content, encoding="utf-8")
    return changed


def _iter_markdown(docs_root: Path):
    yield from sorted(docs_root.rglob("*.md"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Injecte la date Git du dernier commit dans "
        "le front matter des fichiers Markdown sous docs/."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Ne pas écrire ; exit 1 si au moins un fichier nécessiterait "
        "une mise à jour, 0 sinon.",
    )
    args = parser.parse_args(argv)

    repo_root = Path.cwd()
    docs_root = repo_root / "docs"
    if not docs_root.is_dir():
        print(f"Aucun dossier docs/ trouvé sous {repo_root}", file=sys.stderr)
        return 2

    changed = 0
    unchanged = 0
    for md in _iter_markdown(docs_root):
        if args.check:
            updated = git_last_modified_date(md, repo_root=repo_root)
            _, would_change = update_front_matter(
                md.read_text(encoding="utf-8"), updated
            )
            if would_change:
                print(f"À mettre à jour : {md.relative_to(repo_root)}")
                changed += 1
            else:
                unchanged += 1
        else:
            if process_file(md, repo_root=repo_root):
                changed += 1
            else:
                unchanged += 1

    print(f"{changed} fichier(s) mis à jour, {unchanged} inchangé(s).")
    if args.check and changed > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
