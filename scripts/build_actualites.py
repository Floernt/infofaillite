"""Génère la section Actualités et ses renvois croisés avec le guide.

Workflow:
    python scripts/build_actualites.py [--check]

À partir des notes ``docs/actualites/AAAA-MM-JJ-slug.md`` et de la taxonomie
``data/themes.yml`` :
    1. valide le front matter de chaque note (champs, type, thèmes connus),
    2. régénère la liste des notes dans ``docs/actualites/README.md``,
    3. régénère ``docs/actualites/themes.md`` (une section par thème),
    4. ajoute en fin de note les renvois vers les pages du guide,
    5. ajoute en fin de chaque page du guide concernée un bloc
       « Actualités liées » (et le retire quand il n'y a plus de note),
    6. met à jour l'encart « Dernières actualités » de l'accueil.

Le script n'écrit qu'entre les marqueurs START / END et ne réécrit un fichier
que si son contenu change.
"""
from __future__ import annotations

import argparse
import posixpath
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml


START = "<!-- actualites:auto:start -->"
END = "<!-- actualites:auto:end -->"

NOTES_DIR = "actualites"
GENERATED_PAGES = {"README.md", "themes.md"}
TYPES = {
    "jurisprudence": "Jurisprudence",
    "doctrine": "Doctrine",
    "legislation": "Législation",
}
REQUIRED_FIELDS = ("title", "date", "type", "themes", "resume")
MAX_RELATED_ON_PAGE = 5
MAX_SAME_THEME = 3
MAX_HOME = 3

_FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)
_ISO_DATE_RE = re.compile(r"\A\d{4}-\d{2}-\d{2}\Z")
_MOIS = [
    "janvier", "février", "mars", "avril", "mai", "juin", "juillet",
    "août", "septembre", "octobre", "novembre", "décembre",
]


@dataclass
class Theme:
    slug: str
    label: str
    pages: list[str]


@dataclass
class Note:
    rel: str  # chemin relatif à docs/, en notation POSIX
    title: str
    date: str  # YYYY-MM-DD
    type: str
    themes: list[str]
    resume: str
    source: dict = field(default_factory=dict)


# --- utilitaires -----------------------------------------------------------


def split_front_matter(content: str) -> tuple[dict, str]:
    match = _FRONT_MATTER_RE.match(content)
    if not match:
        return {}, content
    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        raise ValueError("front matter YAML : un mapping est attendu")
    return data, content[match.end():]


def iso(value) -> str | None:
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str) and _ISO_DATE_RE.match(value):
        return value
    return None


def date_fr(value: str) -> str:
    year, month, day = value.split("-")
    return f"{int(day)} {_MOIS[int(month) - 1]} {year}"


def zensical_problems(value, path: str = "") -> list[str]:
    """Valeurs de front matter sur lesquelles Zensical échoue au build.

    Zensical 0.0.24 refuse toute valeur YAML nulle et toute date non quotée
    (« failed to extract field Markdown.meta », sans nom de fichier).
    """
    if value is None:
        return [f"valeur vide pour « {path} » : écrire \"\" ou supprimer la ligne"]
    if isinstance(value, date):
        return [f"date non quotée pour « {path} » : écrire '{value.isoformat()}'"]
    if isinstance(value, dict):
        return [
            p for k, v in value.items()
            for p in zensical_problems(v, f"{path}.{k}" if path else str(k))
        ]
    if isinstance(value, list):
        return [p for i, v in enumerate(value) for p in zensical_problems(v, f"{path}[{i}]")]
    return []


def link(source_rel: str, target_rel: str) -> str:
    """Lien relatif de la page source vers la cible (chemins relatifs à docs/)."""
    start = posixpath.dirname(source_rel) or "."
    return posixpath.relpath(target_rel, start=start)


def md_text(text: str) -> str:
    """Échappe les crochets pour un texte de lien Markdown."""
    return text.replace("[", r"\[").replace("]", r"\]")


def page_title(docs_root: Path, rel: str) -> str:
    meta, body = split_front_matter((docs_root / rel).read_text(encoding="utf-8"))
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return str(meta.get("title") or Path(rel).stem)


def sync_block(content: str, block: str | None, append: bool) -> str:
    """Remplace le contenu entre START et END.

    - ``block is None`` : retire marqueurs et bloc (avec la ligne vide qui précède) ;
    - marqueurs absents : ajoute le bloc en fin de fichier si ``append``, sinon
      laisse le contenu intact.
    """
    start = content.find(START)
    end = content.find(END, start + 1) if start >= 0 else -1
    if start < 0 or end < 0:
        if block is None or not append:
            return content
        return f"{content.rstrip(chr(10))}\n\n{START}\n{block}\n{END}\n"
    after = content[end + len(END):]
    if block is None:
        before = content[:start].rstrip("\n")
        return f"{before}\n{after.lstrip(chr(10))}" if after.strip() else f"{before}\n"
    inner = f"\n{block}\n" if block else "\n"
    return f"{content[:start]}{START}{inner}{END}{after}"


# --- chargement --------------------------------------------------------------


def load_themes(path: Path, docs_root: Path) -> dict[str, Theme]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    themes: dict[str, Theme] = {}
    errors: list[str] = []
    for slug, entry in data.items():
        entry = entry or {}
        if not entry.get("label"):
            errors.append(f"{path}: thème « {slug} » sans label")
        pages = list(entry.get("pages") or [])
        for page in pages:
            if not (docs_root / page).is_file():
                errors.append(f"{path}: thème « {slug} » : page introuvable {page}")
        themes[slug] = Theme(slug, str(entry.get("label", slug)), pages)
    if errors:
        raise ValueError("\n".join(errors))
    return themes


def load_notes(docs_root: Path, themes: dict[str, Theme]) -> list[Note]:
    notes: list[Note] = []
    errors: list[str] = []
    for path in sorted((docs_root / NOTES_DIR).glob("*.md")):
        if path.name in GENERATED_PAGES:
            continue
        rel = path.relative_to(docs_root).as_posix()
        try:
            meta, _ = split_front_matter(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path}: {exc}")
            continue
        problems = zensical_problems(meta)
        problems += [f"champ manquant : {f}" for f in REQUIRED_FIELDS if not meta.get(f)]
        if meta.get("type") and meta["type"] not in TYPES:
            problems.append(
                f"type inconnu « {meta['type']} » (attendu : {', '.join(TYPES)})"
            )
        if meta.get("date") and not iso(meta["date"]):
            problems.append(f"date invalide « {meta['date']} » (attendu : AAAA-MM-JJ)")
        note_themes = meta.get("themes") or []
        if not isinstance(note_themes, list):
            problems.append("themes doit être une liste")
            note_themes = []
        for slug in note_themes:
            if slug not in themes:
                problems.append(f"thème inconnu « {slug} » (voir data/themes.yml)")
        if problems:
            errors.extend(f"{path}: {p}" for p in problems)
            continue
        notes.append(
            Note(
                rel=rel,
                title=str(meta["title"]),
                date=iso(meta["date"]),
                type=meta["type"],
                themes=list(note_themes),
                resume=" ".join(str(meta["resume"]).split()),
                source=meta.get("source") or {},
            )
        )
    if errors:
        raise ValueError("\n".join(errors))
    notes.sort(key=lambda n: (n.date, n.rel), reverse=True)
    return notes


# --- rendu ---------------------------------------------------------------------


def source_line(note: Note) -> str:
    src = note.source
    origin = src.get("juridiction") or src.get("auteur") or src.get("publication")
    parts = [str(origin)] if origin else []
    if iso(src.get("date")):
        parts.append(date_fr(iso(src["date"])))
    return ", ".join(parts)


def date_court(value: str) -> str:
    year, month, day = value.split("-")
    return f"{day}.{month}.{year}"


def display_date(note: Note) -> str:
    """Date affichée dans les cartes : celle du texte commenté, sinon la publication."""
    return iso(note.source.get("date")) or note.date


def card_meta(note: Note) -> str:
    """Étiquette de type + date courte (+ origine du texte commenté)."""
    origin = (
        note.source.get("juridiction")
        or note.source.get("auteur")
        or note.source.get("publication")
    )
    date = date_court(display_date(note))
    if origin:
        date += f" · {origin}"
    return (
        f'<span class="ifa-type ifa-type--{note.type}">{TYPES[note.type]}</span> '
        f'<span class="ifa-date">{date}</span>'
    )


def note_item(source_rel: str, note: Note) -> str:
    return (
        f"- [{md_text(note.title)}]({link(source_rel, note.rel)}) — "
        f"{TYPES[note.type].lower()}, {date_fr(note.date)}"
    )


def render_index(notes: list[Note], themes: dict[str, Theme]) -> str:
    rel = f"{NOTES_DIR}/README.md"
    if not notes:
        return "*Aucune note publiée pour l'instant.*"
    lines: list[str] = []
    year = None
    for note in notes:
        if note.date[:4] != year:
            year = note.date[:4]
            lines += [f"## {year}", ""]
        meta = f"Publiée le {date_fr(note.date)}"
        if source_line(note):
            meta += f" · {source_line(note)}"
        tags = " ".join(
            f"[{md_text(themes[s].label)}]({link(rel, f'{NOTES_DIR}/themes.md')}#{s}){{ .ifa-tag }}"
            for s in note.themes
        )
        lines += [
            f'<div class="ifa-note" data-type="{note.type}" '
            f'data-themes="{" ".join(note.themes)}" markdown>',
            "",
            f'<span class="ifa-type ifa-type--{note.type}">{TYPES[note.type]}</span> '
            f'<span class="ifa-note__meta">{meta}</span>',
            "",
            f"### [{md_text(note.title)}]({link(rel, note.rel)})",
            "",
            note.resume,
            "",
            tags,
            "",
            "</div>",
            "",
        ]
    return "\n".join(lines).rstrip()


def render_themes_page(
    notes: list[Note], themes: dict[str, Theme], titles: dict[str, str]
) -> str:
    rel = f"{NOTES_DIR}/themes.md"
    sections: list[str] = []
    for theme in themes.values():
        related = [n for n in notes if theme.slug in n.themes]
        if not related:
            continue
        guide = " · ".join(
            f"[{md_text(titles[p])}]({link(rel, p)})" for p in theme.pages
        )
        body = [f"## {theme.label} {{ #{theme.slug} }}", ""]
        if guide:
            body += [f"Dans le guide : {guide}", ""]
        body += [note_item(rel, n) for n in related]
        sections.append("\n".join(body))
    if not sections:
        return "*Aucune note publiée pour l'instant.*"
    return "\n\n".join(sections)


def render_note_block(
    note: Note, notes: list[Note], themes: dict[str, Theme], titles: dict[str, str]
) -> str:
    themes_rel = f"{NOTES_DIR}/themes.md"
    tags = " · ".join(
        f"[{md_text(themes[s].label)}]({link(note.rel, themes_rel)}#{s})"
        for s in note.themes
    )
    pages: list[str] = []
    for slug in note.themes:
        for page in themes[slug].pages:
            if page not in pages:
                pages.append(page)
    lines = ["---", "", f"**Thèmes :** {tags}"]
    if pages:
        lines += ["", "## Pour approfondir sur infofaillite.be", ""]
        lines += [f"- [{md_text(titles[p])}]({link(note.rel, p)})" for p in pages]
    same = [
        n for n in notes
        if n is not note and set(n.themes) & set(note.themes)
    ][:MAX_SAME_THEME]
    if same:
        lines += ["", "## Sur le même thème", ""]
        lines += [note_item(note.rel, n) for n in same]
    return "\n".join(lines)


def render_page_block(
    page_rel: str, notes: list[Note], themes: dict[str, Theme]
) -> str | None:
    # Les thèmes dont la page est le rattachement principal passent en tête
    slugs = sorted(
        (t.slug for t in themes.values() if page_rel in t.pages),
        key=lambda s: themes[s].pages.index(page_rel),
    )
    related = [n for n in notes if set(n.themes) & set(slugs)]
    if not related:
        return None
    used = [s for s in slugs if any(s in n.themes for n in related)]
    themes_link = link(page_rel, f"{NOTES_DIR}/themes.md")
    lines = ['<div class="ifa-related" markdown>', "", "## Actualités liées", ""]
    lines += ['<div class="ifa-relcards" markdown>']
    for note in related[:MAX_RELATED_ON_PAGE]:
        lines += [
            '<div class="ifa-relcard" markdown>',
            card_meta(note),
            "",
            f"[{md_text(note.title)}]({link(page_rel, note.rel)})",
            "</div>",
        ]
    lines += [
        "</div>",
        "",
        "Toutes les notes sur : "
        + " · ".join(f"[{md_text(themes[s].label)}]({themes_link}#{s})" for s in used),
        "",
        "</div>",
    ]
    return "\n".join(lines)


def render_home_block(notes: list[Note]) -> str:
    """Colonne « À la une » de l'accueil (overrides/home.html)."""
    if not notes:
        return ""
    rel = "README.md"
    lines: list[str] = []
    for note in notes[:MAX_HOME]:
        target = link(rel, note.rel)
        lines += [
            '<div class="ifa-feat" markdown>',
            card_meta(note),
            "",
            f"### [{md_text(note.title)}]({target})",
            "",
            f"[Lire la note]({target}){{ .ifa-more }}",
            "</div>",
        ]
    lines += ["", f"[Toutes les actualités]({NOTES_DIR}/README.md){{ .ifa-more }}"]
    return "\n".join(lines)


# --- orchestration -----------------------------------------------------------


def build(docs_root: Path, themes_path: Path) -> dict[Path, str]:
    """Retourne {fichier: nouveau contenu} pour tous les fichiers concernés."""
    themes = load_themes(themes_path, docs_root)
    notes = load_notes(docs_root, themes)
    titles = {p: page_title(docs_root, p) for t in themes.values() for p in t.pages}

    outputs: dict[Path, str] = {}

    def plan(rel: str, block: str | None, append: bool) -> None:
        path = docs_root / rel
        if not path.is_file():
            return
        content = outputs.get(path, path.read_text(encoding="utf-8"))
        outputs[path] = sync_block(content, block, append)

    plan(f"{NOTES_DIR}/README.md", render_index(notes, themes), append=False)
    plan(f"{NOTES_DIR}/themes.md", render_themes_page(notes, themes, titles), append=False)
    plan("README.md", render_home_block(notes), append=False)
    for note in notes:
        plan(note.rel, render_note_block(note, notes, themes, titles), append=True)
    for path in sorted(docs_root.rglob("*.md")):
        rel = path.relative_to(docs_root).as_posix()
        if rel == "README.md" or rel.startswith(f"{NOTES_DIR}/"):
            continue
        plan(rel, render_page_block(rel, notes, themes), append=True)
    return outputs


def main(argv: list[str] | None = None, repo_root: Path | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Génère la section Actualités et les renvois vers le guide."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Ne pas écrire ; exit 1 si au moins un fichier est désynchronisé.",
    )
    args = parser.parse_args(argv)

    repo_root = repo_root or Path.cwd()
    docs_root = repo_root / "docs"
    try:
        outputs = build(docs_root, repo_root / "data" / "themes.yml")
    except ValueError as exc:
        print(f"Erreur de validation :\n{exc}", file=sys.stderr)
        return 2

    changed = 0
    for path, content in outputs.items():
        if path.read_text(encoding="utf-8") == content:
            continue
        changed += 1
        if args.check:
            print(f"À régénérer : {path.relative_to(repo_root).as_posix()}")
        else:
            path.write_text(content, encoding="utf-8")

    print(f"{changed} fichier(s) mis à jour, {len(outputs) - changed} inchangé(s).")
    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
