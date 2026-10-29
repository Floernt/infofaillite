"""Génère le JSON-LD FAQPage de la page « Questions fréquentes ».

Workflow:
    python scripts/build_faq.py [--check]

Lit les questions de ``docs/faq/README.md`` (blocs
``<details class="ifa-faq" id="..."> <summary>Question</summary> ... </details>``)
et écrit, entre les marqueurs START / END de la même page, un bloc
``<script type="application/ld+json">`` de type FAQPage : question et réponse
en texte brut, pour les moteurs de recherche et les moteurs génératifs.

Le contenu de la page reste la source unique : on ne modifie que le bloc
entre marqueurs, et seulement s'il change. Appelé par ``inject_git_dates.py``.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FAQ_PAGE = Path("docs") / "faq" / "README.md"
START = "<!-- faq:jsonld:start -->"
END = "<!-- faq:jsonld:end -->"

_DETAILS_RE = re.compile(
    r'<details class="ifa-faq"[^>]*\bid="(?P<id>[^"]+)"[^>]*>\s*'
    r"<summary>(?P<question>.*?)</summary>(?P<body>.*?)</details>",
    re.DOTALL,
)
_MORE_LINE_RE = re.compile(r"^\s*\[[^\]]*\]\([^)]*\)\{\s*\.ifa-more\s*\}\s*$", re.MULTILINE)
_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)(\{[^}]*\})?")
_ATTR_RE = re.compile(r"\{\s*[.#][^}]*\}")


def plain_text(markdown: str) -> str:
    """Texte brut d'une réponse : sans liens « Pour aller plus loin », ni balisage."""
    text = _MORE_LINE_RE.sub("", markdown)
    text = _LINK_RE.sub(r"\1", text)
    text = _ATTR_RE.sub("", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"(\*\*|__|\*|_)(\S[^*_]*?\S|\S)\1", r"\2", text)
    lines = [re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", l).strip() for l in text.splitlines()]
    return " ".join(l for l in lines if l)


def parse_questions(content: str) -> list[dict]:
    seen: set[str] = set()
    questions = []
    for m in _DETAILS_RE.finditer(content):
        qid = m.group("id")
        if qid in seen:
            raise ValueError(f"identifiant de question en double : {qid}")
        seen.add(qid)
        questions.append({
            "id": qid,
            "question": plain_text(m.group("question")),
            "answer": plain_text(m.group("body")),
        })
    return questions


def render_block(questions: list[dict], page_url: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": "fr-BE",
        "url": page_url,
        "mainEntity": [
            {
                "@type": "Question",
                "@id": f"{page_url}#{q['id']}",
                "name": q["question"],
                "acceptedAnswer": {"@type": "Answer", "text": q["answer"]},
            }
            for q in questions
        ],
    }
    payload = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'{START}\n<script type="application/ld+json">\n{payload}\n</script>\n{END}'


def sync(content: str, block: str) -> str:
    if START in content and END in content:
        before, rest = content.split(START, 1)
        _, after = rest.split(END, 1)
        return before + block + after
    return content.rstrip("\n") + "\n\n" + block + "\n"


def site_url(repo_root: Path) -> str:
    match = re.search(r'^site_url\s*=\s*"([^"]+)"', (repo_root / "zensical.toml").read_text(encoding="utf-8"), re.M)
    return (match.group(1) if match else "https://infofaillite.be/").rstrip("/") + "/"


def main(argv: list[str] | None = None, repo_root: Path | None = None) -> int:
    parser = argparse.ArgumentParser(description="Génère le JSON-LD de la FAQ.")
    parser.add_argument("--check", action="store_true", help="Ne pas écrire ; exit 1 si désynchronisé.")
    args = parser.parse_args(argv)

    repo_root = repo_root or Path.cwd()
    page = repo_root / FAQ_PAGE
    if not page.is_file():
        print("Pas de page FAQ : rien à générer.")
        return 0
    content = page.read_text(encoding="utf-8")
    try:
        questions = parse_questions(content)
    except ValueError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 2
    updated = sync(content, render_block(questions, site_url(repo_root) + "faq/"))
    if updated == content:
        print(f"FAQ à jour ({len(questions)} questions).")
        return 0
    if args.check:
        print("FAQ à régénérer : docs/faq/README.md", file=sys.stderr)
        return 1
    page.write_text(updated, encoding="utf-8")
    print(f"JSON-LD de la FAQ régénéré ({len(questions)} questions).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
