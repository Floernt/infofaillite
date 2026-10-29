"""Génère un sitemap statique couvrant toutes les pages de docs/.

Workflow:
    python scripts/build_sitemap.py [--check]

Avec un `nav` explicite, la variable `pages` du gabarit sitemap de Zensical
ne contient que les pages du menu : les notes d'actualité et les pages du
pied de page en sortiraient. Ce script écrit donc ``overrides/sitemap.xml``
en dur, à partir de tous les fichiers ``docs/**/*.md`` :
    - URL construite depuis ``site_url`` (zensical.toml) ;
    - ``<lastmod>`` repris de la clé ``updated`` du front matter ;
    - notes d'actualité programmées (``date`` future) exclues.

Appelé automatiquement à la fin de ``inject_git_dates.py``.
"""
from __future__ import annotations

import argparse
import re
import sys
import tomllib
from datetime import date
from pathlib import Path

import yaml

_FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)
NOTES_PREFIX = "actualites/20"

HEADER = """{#-
  Fichier généré par scripts/build_sitemap.py : ne pas éditer à la main.
  Couvre toutes les pages de docs/, y compris celles hors du menu.
-#}
"""


def page_url(base: str, rel: str) -> str:
    path = rel[: -len(".md")]
    if path == "README" or path.endswith("/README"):
        path = path[: -len("README")]
    elif path:
        path += "/"
    return base.rstrip("/") + "/" + path


def front_value(file: Path, key: str) -> str | None:
    match = _FRONT_MATTER_RE.match(file.read_text(encoding="utf-8"))
    if not match:
        return None
    value = (yaml.safe_load(match.group(1)) or {}).get(key)
    return value.isoformat() if hasattr(value, "isoformat") else (str(value) if value else None)


def updated(file: Path) -> str | None:
    return front_value(file, "updated")


def is_scheduled(rel: str, file: Path, today: str) -> bool:
    """Note d'actualité dont la date de publication n'est pas encore atteinte."""
    if not rel.startswith(NOTES_PREFIX):
        return False
    published = front_value(file, "date")
    return bool(published) and published > today


def render_sitemap(repo_root: Path, today: str | None = None) -> str:
    today = today or date.today().isoformat()
    config = tomllib.loads((repo_root / "zensical.toml").read_text(encoding="utf-8"))
    base = config["project"]["site_url"]
    docs = repo_root / "docs"
    lines = [
        HEADER + '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for file in sorted(docs.rglob("*.md")):
        rel = file.relative_to(docs).as_posix()
        if is_scheduled(rel, file, today):
            continue
        lines.append("  <url>")
        lines.append(f"    <loc>{page_url(base, rel)}</loc>")
        lastmod = updated(file)
        if lastmod:
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None, repo_root: Path | None = None) -> int:
    parser = argparse.ArgumentParser(description="Génère overrides/sitemap.xml.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Ne pas écrire ; exit 1 si le sitemap est désynchronisé.",
    )
    parser.add_argument(
        "--today",
        metavar="AAAA-MM-JJ",
        help="Date de référence pour exclure les notes programmées (défaut : aujourd'hui).",
    )
    args = parser.parse_args(argv)

    repo_root = repo_root or Path.cwd()
    target = repo_root / "overrides" / "sitemap.xml"
    content = render_sitemap(repo_root, args.today)
    current = target.read_text(encoding="utf-8") if target.exists() else None
    if current == content:
        print("Sitemap à jour.")
        return 0
    if args.check:
        print("Sitemap à régénérer : overrides/sitemap.xml", file=sys.stderr)
        return 1
    target.write_text(content, encoding="utf-8")
    print("Sitemap régénéré : overrides/sitemap.xml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
