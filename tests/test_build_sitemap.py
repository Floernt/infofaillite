"""Tests du générateur de sitemap statique."""
from __future__ import annotations

from pathlib import Path

from scripts.build_sitemap import page_url, render_sitemap, main


def _site(tmp_path: Path) -> Path:
    (tmp_path / "zensical.toml").write_text(
        '[project]\nsite_url = "https://example.be/"\n', encoding="utf-8"
    )
    (tmp_path / "overrides").mkdir()
    pages = {
        "README.md": "---\nupdated: '2026-10-01'\n---\n# Accueil\n",
        "delais.md": "# Délais\n",
        "faillis/README.md": "---\nupdated: '2026-09-02'\n---\n# Faillis\n",
        "faillis/effacement.md": "---\nupdated: '2026-10-28'\n---\n# Effacement\n",
    }
    for rel, content in pages.items():
        path = tmp_path / "docs" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return tmp_path


def test_page_url_maps_readme_to_directory() -> None:
    base = "https://example.be/"
    assert page_url(base, "README.md") == "https://example.be/"
    assert page_url(base, "faillis/README.md") == "https://example.be/faillis/"
    assert page_url(base, "faillis/effacement.md") == "https://example.be/faillis/effacement/"
    assert page_url(base, "delais.md") == "https://example.be/delais/"


def test_render_lists_every_page_with_lastmod_when_known(tmp_path: Path) -> None:
    site = _site(tmp_path)
    xml = render_sitemap(site)
    assert xml.count("<url>") == 4
    assert "<loc>https://example.be/faillis/effacement/</loc>\n    <lastmod>2026-10-28</lastmod>" in xml
    assert "<loc>https://example.be/delais/</loc>\n  </url>" in xml  # pas de date connue


def test_main_writes_then_check_passes(tmp_path: Path, capsys) -> None:
    site = _site(tmp_path)
    assert main(["--check"], repo_root=site) == 1
    assert main([], repo_root=site) == 0
    assert (site / "overrides" / "sitemap.xml").read_text(encoding="utf-8").startswith("{#-")
    assert main(["--check"], repo_root=site) == 0
