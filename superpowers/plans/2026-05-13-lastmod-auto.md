---
updated: '2026-05-13'
---

# `lastmod` automatique dérivé de Git — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Faire émerger automatiquement, pour chaque page du site infofaillite.be, une date de dernière modification dérivée du dernier commit Git, exposée à la fois dans `sitemap.xml` (`<lastmod>`) et dans le pied de page côté lecteur.

**Architecture:** Un script Python pré-build (`scripts/inject_git_dates.py`) lit `git log` et écrit `updated: YYYY-MM-DD` dans le front matter de chaque `.md`. Deux templates Jinja sont overridés sous `overrides/` : le `sitemap.xml` (pour ajouter `<lastmod>`) et le partial `partials/source-file.html` (pour afficher la date au lecteur). Zensical 0.0.24 n'a pas de système de hooks Python exposé ; le script s'exécute manuellement ou via CI avant `zensical build`.

**Tech Stack:** Python 3.x, PyYAML (déjà inclus via Zensical), `git` CLI, Jinja2 (via Zensical), pytest (à installer pour les tests du script).

**Spec :** [docs/superpowers/specs/2026-05-13-lastmod-auto-design.md](../specs/2026-05-13-lastmod-auto-design.md)

---

## File structure

À créer :
- `scripts/inject_git_dates.py` — script pré-build, parse les `.md`, lit `git log`, met à jour le front matter.
- `tests/test_inject_git_dates.py` — tests unitaires du script (sandbox Git temporaire).
- `tests/__init__.py` — vide, marqueur de package.
- `overrides/sitemap.xml` — override du template Zensical pour ajouter `<lastmod>`.
- `overrides/partials/source-file.html` — override du partial pour afficher « Dernière mise à jour ».

À modifier :
- `requirements.txt` — ajouter `pytest` en dev (optionnel mais utile).
- `CLAUDE.md` — mentionner le script dans la section Workflow.
- `log.md` — entrée datée 2026-05-13.

Tous les fichiers `.md` sous `docs/` seront touchés au premier run du script (ajout/mise à jour de la clé `updated:`) — c'est attendu, on commit en bloc.

---

### Task 1: Bootstrap des dossiers et `pytest`

**Files:**
- Create: `scripts/__init__.py` (vide)
- Create: `tests/__init__.py` (vide)
- Create: `tests/conftest.py`
- Modify: `requirements.txt`

- [ ] **Step 1: Créer les dossiers et fichiers vides**

```bash
mkdir -p scripts tests
type nul > scripts/__init__.py
type nul > tests/__init__.py
```

(Sous PowerShell, `type nul` peut être remplacé par `New-Item -ItemType File scripts/__init__.py` ; sous bash, `touch scripts/__init__.py tests/__init__.py`.)

- [ ] **Step 2: Créer `tests/conftest.py` avec une fixture de repo Git temporaire**

Le contenu :

```python
"""Fixtures pytest partagées."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


def _run_git(repo: Path, *args: str) -> str:
    """Exécute git dans repo et retourne stdout strippé."""
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
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

    def _runner(*args: str) -> str:
        return _run_git(git_repo, *args)

    return _runner
```

- [ ] **Step 3: Ajouter pytest aux dépendances**

Modifier `requirements.txt` pour qu'il devienne :

```
zensical==0.0.24
pytest>=8.0
PyYAML>=6.0
```

(PyYAML est déjà transitivement présent via Zensical, mais on l'ajoute explicitement parce que le script en dépend.)

- [ ] **Step 4: Installer les dépendances et vérifier que pytest tourne à vide**

```bash
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/pytest tests/ -v
```

Expected : `pytest` termine avec « no tests ran » (code 5) — pas d'erreur de collection.

- [ ] **Step 5: Commit**

```bash
git add scripts/__init__.py tests/__init__.py tests/conftest.py requirements.txt
git commit -m "Mise en place scripts/ et tests/ avec pytest"
```

---

### Task 2: Test rouge — extraction de la date Git d'un fichier

**Files:**
- Create: `tests/test_inject_git_dates.py`

- [ ] **Step 1: Écrire le test rouge**

```python
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
    run_git("commit", "-m", "init", "--date=2025-03-15T10:00:00")

    result = git_last_modified_date(file, repo_root=git_repo)

    assert result == "2025-03-15"
```

- [ ] **Step 2: Lancer le test, confirmer qu'il échoue**

```bash
.venv/Scripts/pytest tests/test_inject_git_dates.py -v
```

Expected : ModuleNotFoundError sur `scripts.inject_git_dates`.

- [ ] **Step 3: Pas de commit ici** (le test rouge se commit en même temps que la première implémentation à la Task 3).

---

### Task 3: Vert minimal — `git_last_modified_date`

**Files:**
- Create: `scripts/inject_git_dates.py`

- [ ] **Step 1: Écrire l'implémentation minimale**

```python
"""Inject Git-derived 'updated' dates into Markdown front matter.

Workflow:
    python scripts/inject_git_dates.py [--check]

Pour chaque fichier ``docs/**/*.md`` :
    1. récupère la date du dernier commit Git qui l'a modifié,
    2. fallback sur mtime si le fichier n'est pas dans l'historique,
    3. met à jour la clé ``updated`` du front matter YAML,
    4. ne réécrit le fichier que si la valeur change.
"""
from __future__ import annotations

import subprocess
from datetime import date, datetime, timezone
from pathlib import Path


def git_last_modified_date(file: Path, repo_root: Path) -> str:
    """Retourne la date ISO (YYYY-MM-DD) du dernier commit touchant `file`.

    Fallback sur le mtime du filesystem si le fichier n'a pas d'historique Git
    (untracked ou repo en shallow clone sans le commit pertinent).
    """
    relative = file.relative_to(repo_root)
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cI", "--", str(relative)],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = result.stdout.strip()
    if result.returncode == 0 and stdout:
        return stdout[:10]  # garde uniquement YYYY-MM-DD
    # Fallback : mtime
    mtime = datetime.fromtimestamp(file.stat().st_mtime, tz=timezone.utc)
    return mtime.date().isoformat()
```

- [ ] **Step 2: Lancer le test, vérifier qu'il passe**

```bash
.venv/Scripts/pytest tests/test_inject_git_dates.py::test_git_last_modified_date_returns_iso_date_of_last_commit -v
```

Expected : PASS.

- [ ] **Step 3: Commit**

```bash
git add scripts/inject_git_dates.py tests/test_inject_git_dates.py
git commit -m "git_last_modified_date : extraction date dernier commit"
```

---

### Task 4: Test rouge — fallback mtime pour fichier non commité

**Files:**
- Modify: `tests/test_inject_git_dates.py`

- [ ] **Step 1: Ajouter le test**

Ajouter en bas du fichier :

```python
def test_git_last_modified_date_falls_back_to_mtime_when_uncommitted(
    git_repo: Path,
) -> None:
    file = git_repo / "draft.md"
    file.write_text("# Draft\n", encoding="utf-8")
    # On ne commit pas. mtime doit être utilisé.

    result = git_last_modified_date(file, repo_root=git_repo)

    expected = date.fromtimestamp(file.stat().st_mtime).isoformat()
    assert result == expected
```

Ajouter `from datetime import date` en haut du fichier.

- [ ] **Step 2: Lancer le test, vérifier qu'il passe directement**

```bash
.venv/Scripts/pytest tests/test_inject_git_dates.py -v
```

Expected : PASS (le fallback est déjà implémenté en Task 3 — c'est un test de régression / spécification).

- [ ] **Step 3: Commit**

```bash
git add tests/test_inject_git_dates.py
git commit -m "Test : fallback mtime pour fichier non commité"
```

---

### Task 5: Test rouge — parse et update du front matter YAML

**Files:**
- Modify: `tests/test_inject_git_dates.py`

- [ ] **Step 1: Ajouter les tests**

Ajouter en bas du fichier :

```python
from scripts.inject_git_dates import update_front_matter


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
```

- [ ] **Step 2: Lancer les tests, vérifier qu'ils échouent**

```bash
.venv/Scripts/pytest tests/test_inject_git_dates.py -v
```

Expected : 3 nouveaux tests FAIL avec ImportError sur `update_front_matter`.

- [ ] **Step 3: Pas de commit** — implémentation en Task 6.

---

### Task 6: Vert — `update_front_matter`

**Files:**
- Modify: `scripts/inject_git_dates.py`

- [ ] **Step 1: Ajouter la fonction**

Ajouter en haut du fichier :

```python
import io
import re

import yaml
```

Ajouter à la fin du fichier :

```python
_FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)


def update_front_matter(content: str, updated: str) -> tuple[str, bool]:
    """Retourne (nouveau_contenu, a_change).

    - Si le bloc front matter existe et contient déjà ``updated == updated``
      → renvoie le contenu inchangé et ``False``.
    - Sinon, met à jour ou ajoute la clé ``updated`` et renvoie ``True``.
    - Si aucun front matter n'existe, en crée un minimal.
    """
    match = _FRONT_MATTER_RE.match(content)
    if match:
        yaml_block = match.group(1)
        body = content[match.end() :]
        data = yaml.safe_load(yaml_block) or {}
        if not isinstance(data, dict):
            raise ValueError(
                "Front matter YAML doit être un mapping, "
                f"trouvé : {type(data).__name__}"
            )
        if data.get("updated") == updated:
            return content, False
        data["updated"] = updated
    else:
        data = {"updated": updated}
        body = content

    buffer = io.StringIO()
    yaml.safe_dump(
        data,
        buffer,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )
    new_yaml = buffer.getvalue()
    return f"---\n{new_yaml}---\n\n{body.lstrip()}" if not match else f"---\n{new_yaml}---\n{body}", True
```

- [ ] **Step 2: Lancer les tests**

```bash
.venv/Scripts/pytest tests/test_inject_git_dates.py -v
```

Expected : tous PASS.

- [ ] **Step 3: Commit**

```bash
git add scripts/inject_git_dates.py tests/test_inject_git_dates.py
git commit -m "update_front_matter : injecte/met à jour la clé updated"
```

---

### Task 7: Test rouge — orchestration `process_file`

**Files:**
- Modify: `tests/test_inject_git_dates.py`

- [ ] **Step 1: Ajouter le test**

```python
from scripts.inject_git_dates import process_file


def test_process_file_updates_markdown_with_git_date(
    git_repo: Path, run_git
) -> None:
    md = git_repo / "page.md"
    md.write_text("---\ntitle: Page\n---\n\n# Hello\n", encoding="utf-8")
    run_git("add", "page.md")
    run_git("commit", "-m", "init", "--date=2025-03-15T10:00:00")

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
    run_git("commit", "-m", "init", "--date=2025-03-15T10:00:00")

    process_file(md, repo_root=git_repo)
    changed = process_file(md, repo_root=git_repo)

    assert changed is False
```

- [ ] **Step 2: Lancer, vérifier l'échec**

```bash
.venv/Scripts/pytest tests/test_inject_git_dates.py -v
```

Expected : 2 tests FAIL avec ImportError.

---

### Task 8: Vert — `process_file`

**Files:**
- Modify: `scripts/inject_git_dates.py`

- [ ] **Step 1: Ajouter la fonction**

À ajouter à la fin du fichier :

```python
def process_file(file: Path, repo_root: Path) -> bool:
    """Met à jour le front matter d'un fichier Markdown si nécessaire.

    Retourne True si le fichier a été réécrit, False sinon.
    """
    updated = git_last_modified_date(file, repo_root=repo_root)
    original = file.read_text(encoding="utf-8")
    new_content, changed = update_front_matter(original, updated)
    if changed:
        file.write_text(new_content, encoding="utf-8")
    return changed
```

- [ ] **Step 2: Lancer les tests**

```bash
.venv/Scripts/pytest tests/test_inject_git_dates.py -v
```

Expected : tous PASS.

- [ ] **Step 3: Commit**

```bash
git add scripts/inject_git_dates.py tests/test_inject_git_dates.py
git commit -m "process_file : orchestration date + front matter par fichier"
```

---

### Task 9: Test rouge — CLI `main` parcourt `docs/`

**Files:**
- Modify: `tests/test_inject_git_dates.py`

- [ ] **Step 1: Ajouter le test**

```python
from scripts.inject_git_dates import main


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
    run_git("commit", "-m", "init", "--date=2025-03-15T10:00:00")

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
    run_git("commit", "-m", "init", "--date=2025-03-15T10:00:00")

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
    run_git("commit", "-m", "init", "--date=2025-03-15T10:00:00")

    monkeypatch.chdir(git_repo)
    main([])  # premier run : applique les modifs
    run_git("add", "docs")
    run_git("commit", "-m", "dates")

    exit_code = main(["--check"])
    assert exit_code == 0
```

- [ ] **Step 2: Lancer, confirmer l'échec**

```bash
.venv/Scripts/pytest tests/test_inject_git_dates.py -v
```

Expected : 3 nouveaux tests FAIL avec ImportError sur `main`.

---

### Task 10: Vert — CLI `main`

**Files:**
- Modify: `scripts/inject_git_dates.py`

- [ ] **Step 1: Ajouter le code CLI**

À ajouter en bas du fichier :

```python
import argparse
import sys


def _iter_markdown(docs_root: Path):
    yield from sorted(docs_root.rglob("*.md"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Injecte la date Git du dernier commit dans "
        "le front matter des fichiers Markdown sous docs/."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Ne pas écrire ; exit 1 si au moins un fichier nécessiterait "
        "une mise à jour, 0 sinon.",
    )
    args = parser.parse_args(argv)

    repo_root = Path.cwd()
    docs_root = repo_root / "docs"
    if not docs_root.is_dir():
        print(f"Aucun dossier docs/ trouvé sous {repo_root}", file=sys.stderr)
        return 2

    changed = 0
    unchanged = 0
    for md in _iter_markdown(docs_root):
        if args.check:
            updated = git_last_modified_date(md, repo_root=repo_root)
            _, would_change = update_front_matter(
                md.read_text(encoding="utf-8"), updated
            )
            if would_change:
                print(f"À mettre à jour : {md.relative_to(repo_root)}")
                changed += 1
            else:
                unchanged += 1
        else:
            if process_file(md, repo_root=repo_root):
                changed += 1
            else:
                unchanged += 1

    print(f"{changed} fichier(s) mis à jour, {unchanged} inchangé(s).")
    if args.check and changed > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Lancer la suite complète**

```bash
.venv/Scripts/pytest tests/ -v
```

Expected : tous les tests PASS.

- [ ] **Step 3: Commit**

```bash
git add scripts/inject_git_dates.py tests/test_inject_git_dates.py
git commit -m "CLI main + mode --check"
```

---

### Task 11: Override du template `sitemap.xml`

**Files:**
- Create: `overrides/sitemap.xml`

- [ ] **Step 1: Créer le fichier**

Contenu :

```jinja
{#-
  Override du sitemap par défaut de Zensical.
  Ajoute <lastmod> quand page.meta.updated est défini par
  scripts/inject_git_dates.py.
-#}
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  {%- for page in pages -%}
    {%- if page.canonical_url %}
      <url>
        <loc>{{ page.canonical_url }}</loc>
        {%- if page.meta and page.meta.updated %}
        <lastmod>{{ page.meta.updated }}</lastmod>
        {%- endif %}
      </url>
    {%- endif -%}
  {%- endfor %}
</urlset>
```

- [ ] **Step 2: Vérifier que le build fonctionne toujours**

```bash
.venv/Scripts/zensical build
```

Expected : build OK, pas d'erreur Jinja. Le `sitemap.xml` produit reste valide (`<lastmod>` absent partout car aucun `.md` n'a encore `updated:` à ce stade).

- [ ] **Step 3: Inspection rapide**

Ouvrir `site/sitemap.xml`. Confirmer que la structure est inchangée par rapport à avant.

- [ ] **Step 4: Commit**

```bash
git add overrides/sitemap.xml
git commit -m "Override sitemap.xml : ajout <lastmod> conditionnel"
```

---

### Task 12: Override du partial `source-file.html`

**Files:**
- Create: `overrides/partials/source-file.html`

- [ ] **Step 1: Créer le dossier et le fichier**

```bash
mkdir -p overrides/partials
```

Créer `overrides/partials/source-file.html` avec ce contenu (copie de l'original Zensical + lecture de `page.meta.updated`) :

```jinja
{#-
  Override du partial source-file de Zensical.
  Ajoute le support de page.meta.updated (injecté par
  scripts/inject_git_dates.py) en plus de git_revision_date_localized.
-#}
{% macro render_updated(date) %}
  <span class="md-source-file__fact">
    <span class="md-icon" title="{{ lang.t('source.file.date.updated') }}">
      {% include ".icons/material/clock-edit-outline.svg" %}
    </span>
    {{ date }}
  </span>
{% endmacro %}
{% if page.meta %}
  {% if page.meta.git_revision_date_localized %}
    {% set updated = page.meta.git_revision_date_localized %}
  {% elif page.meta.updated %}
    {% set updated = page.meta.updated %}
  {% elif page.meta.revision_date %}
    {% set updated = page.meta.revision_date %}
  {% endif %}
{% endif %}
{% if updated %}
  <aside class="md-source-file">
    {{ render_updated(updated) }}
  </aside>
{% endif %}
```

(On simplifie volontairement : on supprime les branches `created`, `git_info`, `committers` qui ne sont jamais peuplées dans notre setup et qui alourdiraient inutilement le partial.)

- [ ] **Step 2: Build et inspection**

```bash
.venv/Scripts/zensical build
```

Ouvrir `site/index.html` dans un navigateur et chercher la classe `md-source-file`. Tant qu'aucune page n'a `updated:`, le bloc reste absent. C'est attendu.

- [ ] **Step 3: Commit**

```bash
git add overrides/partials/source-file.html
git commit -m "Override partial source-file : afficher updated"
```

---

### Task 13: Premier run du script — peupler tout le site

**Files:**
- Modify: tous les `docs/**/*.md` (front matter)

- [ ] **Step 1: Vérifier l'état Git**

```bash
git status
```

Expected : working tree clean (les modifs précédentes sont déjà committées).

- [ ] **Step 2: Lancer le script**

```bash
.venv/Scripts/python scripts/inject_git_dates.py
```

Expected output : « N fichier(s) mis à jour, 0 inchangé(s). » avec N = nombre total de `.md` sous `docs/`.

- [ ] **Step 3: Vérifier l'idempotence**

```bash
.venv/Scripts/python scripts/inject_git_dates.py
```

Expected output : « 0 fichier(s) mis à jour, N inchangé(s). »

- [ ] **Step 4: Inspection manuelle d'une page**

Ouvrir par exemple `docs/comprendre/acteurs.md`. Le front matter doit maintenant contenir une ligne `updated: 'YYYY-MM-DD'` correspondant à la date du dernier commit qui a touché ce fichier (vérifier avec `git log -1 --format=%cI -- docs/comprendre/acteurs.md`).

- [ ] **Step 5: Build et vérification end-to-end**

```bash
.venv/Scripts/zensical build
```

- Inspecter `site/sitemap.xml` : la grande majorité des `<url>` doivent maintenant contenir un `<lastmod>` au format ISO date.
- Ouvrir `site/comprendre/acteurs/index.html` dans un navigateur : un pied de page « Dernière mise à jour : 2026-… » doit être visible.

- [ ] **Step 6: Commit**

```bash
git add docs/
git commit -m "Injection initiale des dates updated dans le front matter"
```

---

### Task 14: Documentation projet

**Files:**
- Modify: `CLAUDE.md`
- Modify: `log.md`

- [ ] **Step 1: Mettre à jour `CLAUDE.md`**

Dans la section `## Workflow`, ajouter en fin de liste :

```markdown
- **Avant chaque build** (ou avant de commiter une modification de contenu) :
  lancer `python scripts/inject_git_dates.py` pour rafraîchir la clé
  `updated:` dans le front matter. Cette date alimente `<lastmod>` du sitemap
  et le pied de page « Dernière mise à jour » côté lecteur. Le script est
  idempotent et ne touche que les fichiers dont la date a changé.
```

- [ ] **Step 2: Ajouter une entrée à `log.md`**

Au sommet du fichier (en respectant le format `## [YYYY-MM-DD] <type> | <titre>` repéré dans le projet) :

```markdown
## [2026-05-13] feat | lastmod automatique

Ajout d'une chaîne pré-build qui injecte la date du dernier commit Git dans
le front matter de chaque page (`updated:`), avec deux templates Zensical
overridés :
- `overrides/sitemap.xml` : `<lastmod>` par URL pour signaler la fraîcheur
  aux moteurs de recherche.
- `overrides/partials/source-file.html` : pied de page « Dernière mise à
  jour » côté lecteur.
Script associé : `scripts/inject_git_dates.py` (idempotent, mode `--check`
pour CI).
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md log.md
git commit -m "Documentation : workflow lastmod automatique"
```

---

### Task 15: Vérification finale end-to-end

**Files:** aucun à modifier.

- [ ] **Step 1: Suite de tests complète**

```bash
.venv/Scripts/pytest tests/ -v
```

Expected : tous PASS.

- [ ] **Step 2: Build propre**

```bash
.venv/Scripts/zensical build
```

Expected : pas d'erreur. Inspection :

- `site/sitemap.xml` contient au moins un `<lastmod>` par page éditoriale (toutes les pages avec un front matter).
- Au moins une page HTML rendue (par ex. `site/comprendre/acteurs/index.html`) affiche « Dernière mise à jour : … » en pied.

- [ ] **Step 3: Validation du sitemap par un outil tiers**

Ouvrir https://www.xml-sitemaps.com/validate-xml-sitemap.html dans un navigateur et coller le contenu de `site/sitemap.xml` (ou pointer vers la version déployée une fois le site mis à jour). Vérifier qu'il valide sans erreur.

- [ ] **Step 4: Vérification idempotence finale**

```bash
.venv/Scripts/python scripts/inject_git_dates.py --check
```

Expected : exit 0, « 0 fichier(s) mis à jour, N inchangé(s). »

- [ ] **Step 5: Commit d'éventuels ajustements**

Si les vérifications ont nécessité de petites corrections (par ex. format de date affichée), commiter le delta. Sinon, rien à committer ici.
