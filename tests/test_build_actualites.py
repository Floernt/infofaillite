"""Tests du générateur de la section Actualités."""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.build_actualites import START, END
from scripts.build_actualites import load_themes
from scripts.build_actualites import load_notes
from scripts.build_actualites import sync_block
from scripts.build_actualites import main


THEMES_YML = """\
effacement:
  label: Effacement des dettes
  pages: [faillis/effacement.md, comprendre/cloture.md]
caution:
  label: Cautions
  pages: [creanciers/suretes-cautions.md, faillis/effacement.md]
curateur:
  label: Le curateur
  pages: [comprendre/acteurs.md]
"""

NOTE_A = """\
---
title: "Effacement : la caution du conjoint reste tenue"
date: '2026-10-15'
type: jurisprudence
source:
  juridiction: Cour de cassation
  date: '2026-03-12'
  reference: C.25.0001.F
themes: [effacement, caution]
resume: La Cour précise la portée de l'effacement.
---
Corps de la note A.
"""

NOTE_B = """\
---
title: Le refus d'effacement, premier bilan
date: '2026-09-20'
type: doctrine
themes: [effacement]
resume: Panorama des refus d'effacement.
---
Corps de la note B.
"""

INDEX = f"""\
---
title: Actualités
---
# Actualités

Intro rédigée à la main.

{START}
{END}
"""

THEMES_PAGE = f"""\
---
title: Par thème
---
# Les actualités par thème

{START}
{END}
"""

HOME = f"""\
# Accueil

Texte d'accueil.

{START}
{END}

Suite de l'accueil.
"""


@pytest.fixture
def site(tmp_path: Path) -> Path:
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "themes.yml").write_text(THEMES_YML, encoding="utf-8")
    docs = tmp_path / "docs"
    pages = {
        "README.md": HOME,
        "faillis/effacement.md": "---\nupdated: '2026-01-01'\n---\n# L'effacement des dettes\n\nTexte.\n",
        "comprendre/cloture.md": "# La clôture\n\nTexte.\n",
        "comprendre/acteurs.md": "# Les acteurs\n\nTexte.\n",
        "creanciers/suretes-cautions.md": "# Les sûretés et cautions\n\nTexte.\n",
        "actualites/README.md": INDEX,
        "actualites/themes.md": THEMES_PAGE,
        "actualites/2026-10-15-caution-conjoint.md": NOTE_A,
        "actualites/2026-09-20-refus-effacement.md": NOTE_B,
    }
    for rel, content in pages.items():
        path = docs / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return tmp_path


def read(site: Path, rel: str) -> str:
    return (site / "docs" / rel).read_text(encoding="utf-8")


# --- sync_block ---------------------------------------------------------


def test_sync_block_replaces_content_between_markers() -> None:
    content = f"avant\n{START}\nancien\n{END}\naprès\n"
    result = sync_block(content, "nouveau", append=False)
    assert result == f"avant\n{START}\nnouveau\n{END}\naprès\n"


def test_sync_block_appends_when_markers_missing_and_append_true() -> None:
    result = sync_block("# Page\n\nTexte.\n", "bloc", append=True)
    assert result == f"# Page\n\nTexte.\n\n{START}\nbloc\n{END}\n"


def test_sync_block_leaves_content_alone_when_markers_missing_and_append_false() -> None:
    assert sync_block("# Page\n", "bloc", append=False) == "# Page\n"


def test_sync_block_removes_block_when_none() -> None:
    content = f"# Page\n\nTexte.\n\n{START}\nbloc\n{END}\n"
    assert sync_block(content, None, append=True) == "# Page\n\nTexte.\n"


def test_sync_block_none_without_markers_is_noop() -> None:
    assert sync_block("# Page\n", None, append=True) == "# Page\n"


# --- chargement et validation ---------------------------------------------


def test_load_themes_rejects_unknown_page(site: Path) -> None:
    (site / "data" / "themes.yml").write_text(
        "x:\n  label: X\n  pages: [inexistante.md]\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="inexistante.md"):
        load_themes(site / "data" / "themes.yml", site / "docs")


def test_load_notes_sorted_most_recent_first(site: Path) -> None:
    themes = load_themes(site / "data" / "themes.yml", site / "docs")
    notes = load_notes(site / "docs", themes)
    assert [n.rel for n in notes] == [
        "actualites/2026-10-15-caution-conjoint.md",
        "actualites/2026-09-20-refus-effacement.md",
    ]
    assert notes[0].date == "2026-10-15"


def test_load_notes_rejects_unknown_theme_and_names_file(site: Path) -> None:
    (site / "docs" / "actualites" / "2026-01-01-x.md").write_text(
        "---\ntitle: X\ndate: 2026-01-01\ntype: doctrine\nthemes: [inconnu]\n"
        "resume: R\n---\nCorps\n",
        encoding="utf-8",
    )
    themes = load_themes(site / "data" / "themes.yml", site / "docs")
    with pytest.raises(ValueError, match=r"2026-01-01-x\.md.*inconnu"):
        load_notes(site / "docs", themes)


def test_load_notes_rejects_values_that_break_zensical(site: Path) -> None:
    # Zensical échoue (« failed to extract field Markdown.meta ») sur une
    # valeur YAML nulle ou une date non quotée : le script doit l'intercepter.
    (site / "docs" / "actualites" / "2026-01-01-x.md").write_text(
        "---\ntitle: X\ndate: 2026-01-01\ntype: doctrine\nthemes: [effacement]\n"
        "resume: R\nsource:\n  date: '2026-01-01'\n  lien:\n---\n",
        encoding="utf-8",
    )
    themes = load_themes(site / "data" / "themes.yml", site / "docs")
    with pytest.raises(ValueError) as exc:
        load_notes(site / "docs", themes)
    assert "source.lien" in str(exc.value)
    assert "date non quotée" in str(exc.value)


def test_load_notes_rejects_missing_field_and_bad_type(site: Path) -> None:
    (site / "docs" / "actualites" / "2026-01-01-x.md").write_text(
        "---\ntitle: X\ndate: 2026-01-01\ntype: blog\nthemes: [effacement]\n---\n",
        encoding="utf-8",
    )
    themes = load_themes(site / "data" / "themes.yml", site / "docs")
    with pytest.raises(ValueError) as exc:
        load_notes(site / "docs", themes)
    assert "resume" in str(exc.value)
    assert "blog" in str(exc.value)


# --- génération -----------------------------------------------------------


def test_main_generates_index_themes_and_cross_links(site: Path) -> None:
    assert main([], repo_root=site) == 0

    index = read(site, "actualites/README.md")
    assert "Intro rédigée à la main." in index
    assert "[Effacement : la caution du conjoint reste tenue](2026-10-15-caution-conjoint.md)" in index
    assert index.index("caution-conjoint") < index.index("refus-effacement")
    assert "(themes.md#effacement)" in index
    assert 'data-type="jurisprudence"' in index

    themes = read(site, "actualites/themes.md")
    assert "## Effacement des dettes { #effacement }" in themes
    assert "## Cautions { #caution }" in themes
    assert "#curateur" not in themes  # aucun article : thème non affiché
    assert "[L'effacement des dettes](../faillis/effacement.md)" in themes

    page = read(site, "faillis/effacement.md")
    assert page.startswith("---\nupdated: '2026-01-01'\n---\n# L'effacement des dettes\n\nTexte.\n")
    assert '??? info "Actualités liées à cette page (2)"' in page
    assert "(../actualites/2026-10-15-caution-conjoint.md)" in page
    assert "(../actualites/themes.md#effacement)" in page
    # thème principal de la page (effacement) avant le thème secondaire (caution)
    assert page.index("themes.md#effacement") < page.index("themes.md#caution")

    assert START not in read(site, "comprendre/acteurs.md")  # pas de note sur ce thème

    note = read(site, "actualites/2026-10-15-caution-conjoint.md")
    assert note.startswith(NOTE_A)
    assert "## Pour approfondir sur infofaillite.be" in note
    assert "[L'effacement des dettes](../faillis/effacement.md)" in note
    assert note.count("../faillis/effacement.md") == 1  # dédoublonné
    assert "[Le refus d'effacement, premier bilan](2026-09-20-refus-effacement.md)" in note

    home = read(site, "README.md")
    assert "(actualites/2026-10-15-caution-conjoint.md)" in home
    assert home.endswith("Suite de l'accueil.\n")


def test_main_is_idempotent_and_check_passes_after_build(site: Path, capsys) -> None:
    main([], repo_root=site)
    capsys.readouterr()
    assert main([], repo_root=site) == 0
    assert "0 fichier(s) mis à jour" in capsys.readouterr().out
    assert main(["--check"], repo_root=site) == 0


def test_check_fails_when_out_of_sync_and_writes_nothing(site: Path) -> None:
    before = read(site, "faillis/effacement.md")
    assert main(["--check"], repo_root=site) == 1
    assert read(site, "faillis/effacement.md") == before


def test_block_removed_from_page_when_last_note_deleted(site: Path) -> None:
    main([], repo_root=site)
    (site / "docs" / "actualites" / "2026-10-15-caution-conjoint.md").unlink()
    main([], repo_root=site)
    assert START not in read(site, "creanciers/suretes-cautions.md")
    assert "(1)" in read(site, "faillis/effacement.md")


def test_main_reports_validation_errors(site: Path, capsys) -> None:
    (site / "docs" / "actualites" / "2026-01-01-x.md").write_text(
        "---\ntitle: X\ndate: 2026-01-01\ntype: doctrine\nthemes: [inconnu]\nresume: R\n---\n",
        encoding="utf-8",
    )
    assert main([], repo_root=site) == 2
    assert "inconnu" in capsys.readouterr().err


def test_empty_index_shows_placeholder(site: Path) -> None:
    for f in (site / "docs" / "actualites").glob("2026-*.md"):
        f.unlink()
    main([], repo_root=site)
    assert "Aucune note publiée pour l'instant." in read(site, "actualites/README.md")
    assert START not in read(site, "faillis/effacement.md")
