"""Tests du script inject_git_dates."""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.inject_git_dates import git_last_modified_date


def test_git_last_modified_date_returns_iso_date_of_last_commit(
    git_repo: Path, run_git
) -> None:
    file = git_repo / "page.md"
    file.write_text("# Hello\n", encoding="utf-8")
    run_git("add", "page.md")
    run_git(
        "commit",
        "-m",
        "init",
        "--date=2025-03-15T10:00:00",
        env={"GIT_COMMITTER_DATE": "2025-03-15T10:00:00"},
    )

    result = git_last_modified_date(file, repo_root=git_repo)

    assert result == "2025-03-15"
