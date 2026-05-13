"""Tests du script inject_git_dates."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from scripts.inject_git_dates import git_last_modified_date
from scripts.inject_git_dates import update_front_matter
from scripts.inject_git_dates import process_file
from scripts.inject_git_dates import main


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


def test_process_file_updates_markdown_with_git_date(
    git_repo: Path, run_git
) -> None:
    md = git_repo / "page.md"
    md.write_text("---\ntitle: Page\n---\n\n# Hello\n", encoding="utf-8")
    run_git("add", "page.md")
    run_git(
        "commit",
        "-m",
        "init",
        "--date=2025-03-15T10:00:00",
        env={"GIT_COMMITTER_DATE": "2025-03-15T10:00:00"},
    )

    changed = process_file(md, repo_root=git_repo)

    assert changed is True
    content = md.read_text(encoding="utf-8")
    assert "updated: '2025-03-15'" in content or "updated: 2025-03-15" in content


def test_process_file_is_idempotent_on_second_run(
    git_repo: Path, run_git
) -> None:
    md = git_repo / "page.md"
    md.write_text("---\ntitle: Page\n---\n\n# Hello\n", encoding="utf-8")
    run_git("add", "page.md")
    run_git(
        "commit",
        "-m",
        "init",
        "--date=2025-03-15T10:00:00",
        env={"GIT_COMMITTER_DATE": "2025-03-15T10:00:00"},
    )

    process_file(md, repo_root=git_repo)
    changed = process_file(md, repo_root=git_repo)

    assert changed is False


def test_main_processes_all_markdown_files_under_docs(
    git_repo: Path, run_git, monkeypatch, capsys
) -> None:
    docs = git_repo / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("---\ntitle: A\n---\n\n# A\n", encoding="utf-8")
    (docs / "sub").mkdir()
    (docs / "sub" / "b.md").write_text(
        "---\ntitle: B\n---\n\n# B\n", encoding="utf-8"
    )
    run_git("add", "docs")
    run_git(
        "commit",
        "-m",
        "init",
        "--date=2025-03-15T10:00:00",
        env={"GIT_COMMITTER_DATE": "2025-03-15T10:00:00"},
    )

    monkeypatch.chdir(git_repo)
    exit_code = main([])

    assert exit_code == 0
    captured = capsys.readouterr().out
    assert "2 fichier" in captured  # log "2 fichiers mis à jour"
    assert "updated:" in (docs / "a.md").read_text(encoding="utf-8")
    assert "updated:" in (docs / "sub" / "b.md").read_text(encoding="utf-8")


def test_main_check_mode_returns_1_when_changes_needed(
    git_repo: Path, run_git, monkeypatch
) -> None:
    docs = git_repo / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("---\ntitle: A\n---\n\n# A\n", encoding="utf-8")
    run_git("add", "docs")
    run_git(
        "commit",
        "-m",
        "init",
        "--date=2025-03-15T10:00:00",
        env={"GIT_COMMITTER_DATE": "2025-03-15T10:00:00"},
    )

    monkeypatch.chdir(git_repo)
    exit_code = main(["--check"])

    assert exit_code == 1
    # En mode --check on n'écrit pas
    assert "updated:" not in (docs / "a.md").read_text(encoding="utf-8")


def test_main_check_mode_returns_0_when_nothing_to_do(
    git_repo: Path, run_git, monkeypatch
) -> None:
    docs = git_repo / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("---\ntitle: A\n---\n\n# A\n", encoding="utf-8")
    run_git("add", "docs")
    run_git(
        "commit",
        "-m",
        "init",
        "--date=2025-03-15T10:00:00",
        env={"GIT_COMMITTER_DATE": "2025-03-15T10:00:00"},
    )

    monkeypatch.chdir(git_repo)
    main([])  # premier run : applique les modifs
    run_git("add", "docs")
    run_git(
        "commit",
        "-m",
        "dates",
        env={"GIT_COMMITTER_DATE": "2025-03-15T10:00:00"},
    )

    exit_code = main(["--check"])
    assert exit_code == 0


def test_update_front_matter_is_idempotent_with_unquoted_date() -> None:
    """Garantit l'idempotence quand la date existante est non-quotée dans le YAML
    (PyYAML la parse alors comme un datetime.date au lieu d'une str)."""
    content = "---\ntitle: Page\nupdated: 2025-03-15\n---\n\n# Hello\n"
    new_content, changed = update_front_matter(content, "2025-03-15")
    assert changed is False
    assert new_content == content
