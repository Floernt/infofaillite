"""Garde-fou : toute page de docs/ est soit dans le menu, soit hors menu à dessein."""
from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Pages publiées volontairement hors du menu (accueil, pied de page).
OFF_NAV = {
    "README.md",
    "a-propos.md",
    "contact.md",
    "delais.md",
    "glossaire.md",
    "ressources.md",
}
# Les notes d'actualité sont atteintes par la liste, la page par thème et les renvois.
OFF_NAV_PREFIX = "actualites/20"


def _nav_files(items) -> set[str]:
    files: set[str] = set()
    for item in items:
        if isinstance(item, str):
            files.add(item)
        elif isinstance(item, dict):
            for value in item.values():
                files |= _nav_files([value] if isinstance(value, str) else value)
    return files


def _config() -> dict:
    return tomllib.loads((ROOT / "zensical.toml").read_text(encoding="utf-8"))


def test_every_page_is_in_nav_or_explicitly_off_nav() -> None:
    nav = _nav_files(_config()["project"]["nav"])
    pages = {p.relative_to(ROOT / "docs").as_posix() for p in (ROOT / "docs").rglob("*.md")}
    orphans = sorted(
        p for p in pages - nav - OFF_NAV if not p.startswith(OFF_NAV_PREFIX)
    )
    assert orphans == [], f"Pages absentes du menu (zensical.toml) : {orphans}"


def test_every_nav_entry_points_to_an_existing_page() -> None:
    nav = _nav_files(_config()["project"]["nav"])
    missing = sorted(p for p in nav if not (ROOT / "docs" / p).is_file())
    assert missing == [], f"Entrées du menu sans fichier : {missing}"


def test_top_level_nav_has_the_four_sections() -> None:
    titles = [next(iter(item)) for item in _config()["project"]["nav"]]
    assert titles == [
        "Je suis en faillite",
        "Je suis créancier",
        "Comprendre la procédure",
        "Actualités",
    ]
