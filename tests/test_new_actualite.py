"""Tests du créateur de notes d'actualité."""
from __future__ import annotations

from pathlib import Path

import yaml

from scripts.build_actualites import zensical_problems
from scripts.new_actualite import main, slugify


def _repo(tmp_path: Path) -> Path:
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "themes.yml").write_text(
        "effacement:\n  label: Effacement\n  pages: []\n", encoding="utf-8"
    )
    return tmp_path


def test_slugify_strips_accents_and_apostrophes() -> None:
    assert slugify("L'effacement : la caution du conjoint reste tenue") == (
        "l-effacement-la-caution-du-conjoint-reste-tenue"
    )


def test_main_creates_skeleton_with_valid_front_matter(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    code = main(
        ["Effacement et caution", "--type", "doctrine", "--themes", "effacement",
         "--date", "2026-10-15"],
        repo_root=repo,
    )
    assert code == 0
    path = repo / "docs" / "actualites" / "2026-10-15-effacement-et-caution.md"
    meta = yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1])
    assert meta["title"] == "Effacement et caution"
    assert meta["type"] == "doctrine"
    assert meta["themes"] == ["effacement"]
    assert "auteur" in meta["source"]
    assert zensical_problems(meta) == []  # squelette compatible avec le build


def test_main_rejects_unknown_theme_and_existing_file(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    args = ["T", "--type", "doctrine", "--date", "2026-10-15"]
    assert main(args + ["--themes", "inconnu"], repo_root=repo) == 2
    assert main(args + ["--themes", "effacement"], repo_root=repo) == 0
    assert main(args + ["--themes", "effacement"], repo_root=repo) == 1
