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

import subprocess
from datetime import date, datetime, timezone
from pathlib import Path


def git_last_modified_date(file: Path, repo_root: Path) -> str:
    """Retourne la date ISO (YYYY-MM-DD) du dernier commit touchant `file`.

    Fallback sur le mtime du filesystem si le fichier n'a pas d'historique Git
    (untracked ou repo en shallow clone sans le commit pertinent).
    """
    relative = file.relative_to(repo_root)
    result = subprocess.run(
        ["git", "log", "-1", "--format=%aI", "--", str(relative)],
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
