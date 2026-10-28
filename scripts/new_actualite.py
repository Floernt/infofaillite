"""Crée le squelette d'une nouvelle note dans docs/actualites/.

Workflow:
    python scripts/new_actualite.py "Titre de la note" --type jurisprudence \
        --themes effacement,caution [--date 2026-10-15]

Le fichier ``docs/actualites/AAAA-MM-JJ-slug.md`` est créé avec un front
matter complet à remplir. Les thèmes sont vérifiés contre data/themes.yml.
Lancer ensuite ``python scripts/build_actualites.py``.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

import yaml

TYPES = ("jurisprudence", "doctrine", "legislation")

# Champ propre à chaque type pour l'origine du texte commenté
SOURCE_FIELD = {
    "jurisprudence": "juridiction",
    "doctrine": "auteur",
    "legislation": "publication",
}


def slugify(text: str, max_words: int = 8) -> str:
    ascii_text = (
        unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    )
    words = re.findall(r"[a-z0-9]+", ascii_text.lower().replace("'", " "))
    return "-".join(words[:max_words])


def skeleton(title: str, type_: str, themes: list[str], day: str) -> str:
    quoted = title.replace('"', '\\"')
    return f"""---
title: "{quoted}"
date: '{day}'
type: {type_}
source:
  {SOURCE_FIELD[type_]}: ""
  date: ""          # 'AAAA-MM-JJ', toujours entre guillemets
  reference: ""
  lien: ""
themes: [{", ".join(themes)}]
articles_cde: []
resume: >-
  Une ou deux phrases, reprises dans la liste des actualités et dans les
  renvois depuis les pages du guide.
description: ""
keywords: ""
---
Texte de la note.
"""


def main(argv: list[str] | None = None, repo_root: Path | None = None) -> int:
    parser = argparse.ArgumentParser(description="Crée une nouvelle note d'actualité.")
    parser.add_argument("title", help="Titre de la note")
    parser.add_argument("--type", required=True, choices=TYPES)
    parser.add_argument("--themes", required=True, help="Slugs séparés par des virgules")
    parser.add_argument("--date", default=date.today().isoformat(), help="AAAA-MM-JJ")
    parser.add_argument("--slug", help="Slug du fichier (déduit du titre par défaut)")
    args = parser.parse_args(argv)

    repo_root = repo_root or Path.cwd()
    known = yaml.safe_load((repo_root / "data" / "themes.yml").read_text(encoding="utf-8"))
    themes = [t.strip() for t in args.themes.split(",") if t.strip()]
    unknown = [t for t in themes if t not in known]
    if unknown:
        print(
            f"Thème(s) inconnu(s) : {', '.join(unknown)}\n"
            f"Thèmes disponibles : {', '.join(known)}",
            file=sys.stderr,
        )
        return 2
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        print(f"Date invalide : {args.date} (attendu : AAAA-MM-JJ)", file=sys.stderr)
        return 2

    path = repo_root / "docs" / "actualites" / f"{args.date}-{args.slug or slugify(args.title)}.md"
    if path.exists():
        print(f"Le fichier existe déjà : {path.relative_to(repo_root).as_posix()}", file=sys.stderr)
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(skeleton(args.title, args.type, themes, args.date), encoding="utf-8")
    print(f"Note créée : {path.relative_to(repo_root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
