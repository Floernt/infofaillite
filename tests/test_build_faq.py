"""Tests du générateur de JSON-LD de la FAQ."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from scripts.build_faq import END, START, main, parse_questions, plain_text

PAGE = """\
---
description: FAQ
---
# Questions fréquentes

## Avant la faillite { #avant-la-faillite }

<details class="ifa-faq" id="chambre" data-profils="dirigeant" markdown>
<summary>Le tribunal surveille-t-il les entreprises ?</summary>

Oui. La **chambre** des entreprises en difficulté (article XX.21) examine les [signaux](../glossaire.md).

- arriérés ONSS ;
- jugements par défaut.

[Pour aller plus loin : les acteurs](../comprendre/acteurs-secondaires.md){ .ifa-more }

</details>

<details class="ifa-faq" id="aveu" data-profils="independant dirigeant" markdown>
<summary>Comment faire aveu ?</summary>

Sur Regsol, dans le mois.

</details>
"""


def _site(tmp_path: Path, page: str = PAGE) -> Path:
    (tmp_path / "zensical.toml").write_text('[project]\nsite_url = "https://example.be/"\n', encoding="utf-8")
    faq = tmp_path / "docs" / "faq" / "README.md"
    faq.parent.mkdir(parents=True)
    faq.write_text(page, encoding="utf-8")
    return tmp_path


def _jsonld(site: Path) -> dict:
    content = (site / "docs" / "faq" / "README.md").read_text(encoding="utf-8")
    block = content.split(START, 1)[1].split(END, 1)[0]
    return json.loads(re.search(r"<script[^>]*>(.*)</script>", block, re.S).group(1))


def test_plain_text_drops_more_links_and_markup() -> None:
    text = plain_text("Oui. La **chambre** voit les [signaux](x.md).\n\n- un ;\n- deux.\n\n[Plus](y.md){ .ifa-more }\n")
    assert text == "Oui. La chambre voit les signaux. un ; deux."


def test_parse_questions_reads_id_question_and_answer() -> None:
    qs = parse_questions(PAGE)
    assert [q["id"] for q in qs] == ["chambre", "aveu"]
    assert qs[0]["question"] == "Le tribunal surveille-t-il les entreprises ?"
    assert "Pour aller plus loin" not in qs[0]["answer"]


def test_duplicate_ids_are_rejected() -> None:
    with pytest.raises(ValueError):
        parse_questions(PAGE + PAGE)


def test_main_writes_jsonld_then_is_idempotent(tmp_path: Path) -> None:
    site = _site(tmp_path)
    assert main(["--check"], repo_root=site) == 1
    assert main([], repo_root=site) == 0
    data = _jsonld(site)
    assert data["@type"] == "FAQPage"
    assert len(data["mainEntity"]) == 2
    assert data["mainEntity"][1]["@id"] == "https://example.be/faq/#aveu"
    assert main(["--check"], repo_root=site) == 0
    first = (site / "docs" / "faq" / "README.md").read_text(encoding="utf-8")
    main([], repo_root=site)
    assert (site / "docs" / "faq" / "README.md").read_text(encoding="utf-8") == first


def test_block_follows_edits(tmp_path: Path) -> None:
    site = _site(tmp_path)
    main([], repo_root=site)
    page = site / "docs" / "faq" / "README.md"
    page.write_text(page.read_text(encoding="utf-8").replace("dans le mois", "dans le mois de la cessation", 1), encoding="utf-8")
    assert main(["--check"], repo_root=site) == 1
    main([], repo_root=site)
    assert "cessation" in _jsonld(site)["mainEntity"][1]["acceptedAnswer"]["text"]
