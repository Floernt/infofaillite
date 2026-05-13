"""Fixtures pytest partagées."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest


def _run_git(repo: Path, *args: str, env: dict[str, str] | None = None) -> str:
    """Exécute git dans repo et retourne stdout strippé."""
    full_env = {**os.environ, **(env or {})}
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
        env=full_env,
    )
    return result.stdout.strip()


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    """Crée un repo Git temporaire isolé, prêt à recevoir des commits."""
    _run_git(tmp_path, "init", "-q")
    _run_git(tmp_path, "config", "user.email", "test@example.com")
    _run_git(tmp_path, "config", "user.name", "Test")
    _run_git(tmp_path, "config", "commit.gpgsign", "false")
    return tmp_path


@pytest.fixture
def run_git(git_repo):
    """Helper pour exécuter des commandes git dans git_repo."""

    def _runner(*args: str, env: dict[str, str] | None = None) -> str:
        return _run_git(git_repo, *args, env=env)

    return _runner
