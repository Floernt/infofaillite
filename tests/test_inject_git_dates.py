"""Tests du script inject_git_dates."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from scripts.inject_git_dates import git_last_modified_date
from scripts.inject_git_dates import update_front_matter


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


def test_git_last_modified_date_falls_back_to_mtime_when_uncommitted(
    git_repo: Path,
) -> None:
    file = git_repo / "draft.md"
    file.write_text("# Draft\n", encoding="utf-8")
    # On ne commit pas. mtime doit être utilisé.

    result = git_last_modified_date(file, repo_root=git_repo)

    expected = date.fromtimestamp(file.stat().st_mtime).isoformat()
    assert result == expected


def test_update_front_matter_adds_updated_key_when_missing() -> None:
    content = "---\ntitle: Page\n---\n\n# Hello\n"
    new_content, changed = update_front_matter(content, "2025-03-15")
    assert changed is True
    assert "updated: '2025-03-15'" in new_content or "updated: 2025-03-15" in new_content
    assert "title: Page" in new_content
    assert "# Hello" in new_content


def test_update_front_matter_replaces_existing_updated_key() -> None:
    content = "---\ntitle: Page\nupdated: '2024-01-01'\n---\n\n# Hello\n"
    new_content, changed = update_front_matter(content, "2025-03-15")
    assert changed is True
    assert "2024-01-01" not in new_content
    assert "2025-03-15" in new_content


def test_update_front_matter_is_idempotent() -> None:
    content = "---\ntitle: Page\nupdated: '2025-03-15'\n---\n\n# Hello\n"
    new_content, changed = update_front_matter(content, "2025-03-15")
    assert changed is False
    assert new_content == content


def test_update_front_matter_creates_block_when_absent() -> None:
    content = "# Hello\n\nBody.\n"
    new_content, changed = update_front_matter(content, "2025-03-15")
    assert changed is True
    assert new_content.startswith("---\n")
    assert "updated:" in new_content
    assert "# Hello" in new_content
