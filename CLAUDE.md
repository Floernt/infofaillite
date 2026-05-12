# CLAUDE.md — infofaillite

Notes de contexte pour Claude. À mettre à jour quand le projet évolue.

## Projet

Site documentaire **Guide de la faillite en Belgique** (infofaillite.be), basé sur le Livre XX du Code de droit économique. Public visé : faillis/dirigeants, créanciers, curieux du droit de l'insolvabilité belge.

- Stack : **Zensical** (statique, dérivé de MkDocs Material). Config dans [zensical.toml](zensical.toml).
- Sources Markdown : [docs/](docs/).
- Dépendances Python : [requirements.txt](requirements.txt), venv local dans `.venv/`.
- Branche principale : `main`. La branche par défaut au démarrage de cette session est `gh-pages` (déploiement).

## Arborescence éditoriale

- [docs/README.md](docs/README.md) — page d'accueil, point d'entrée par profil (failli, créancier, comprendre).
- [docs/comprendre/](docs/comprendre/) — vue d'ensemble de la procédure : définition, acteurs, déroulement chronologique, dessaisissement, période suspecte, liquidation, clôture, procédures alternatives.
- [docs/faillis/](docs/faillis/) — obligations, droits, checklist, effacement des dettes, interdiction de gérer, reprise d'activité, FAQ.
- [docs/creanciers/](docs/creanciers/) — déclaration de créance, sûretés/cautions, vérification, dividendes, droits, catégories, FAQ.
- [docs/glossaire.md](docs/glossaire.md), [docs/delais.md](docs/delais.md), [docs/ressources.md](docs/ressources.md), [docs/a-propos.md](docs/a-propos.md).
- [docs/javascripts/](docs/javascripts/) — analytics (clicky) et JSON-LD (schema.js).

## Conventions éditoriales

- **Langue** : français de Belgique, registre clair et accessible — voir [docs/a-propos.md](docs/a-propos.md) pour la ligne éditoriale.
- **Référencement légal** : le Livre XX du Code de droit économique est la source de droit principale ; citer les articles précis quand c'est utile, sans noyer le lecteur.
- **Liens internes** : relatifs en `.md` (Zensical/MkDocs les résout au build), pas d'URL absolues vers infofaillite.be.
- **Admonitions** : syntaxe MkDocs (`!!! danger`, `!!! note`, `!!! warning`, etc.) — utilisée notamment pour les délais critiques.
- **Front matter YAML** : `description` + `keywords` en tête de chaque page SEO-sensible.
- **Pas d'emojis** dans les pages éditoriales sauf demande explicite.

## Workflow

- Modifier les sources dans `docs/`, vérifier au besoin avec un build local Zensical.
- Les commits récents montrent un style de message court et descriptif en français (« Refonte éditoriale complète… », « SEO & GEO », « analytics »). Suivre ce style.
- **Toujours journaliser** les modifications de fond (ingest, refonte, passe SEO, lint, etc.) dans [log.md](log.md) avec le préfixe `## [YYYY-MM-DD] <type> | <titre>`.

## Mémoire de travail

- Une session active porte sur la **refonte éditoriale complète de la documentation** (commit `aad0a0f`). Voir [log.md](log.md) pour la chronologie détaillée.
- Le dossier [infofaillite/](infofaillite/) à la racine est apparu récemment (untracked) — vérifier son rôle avant d'y toucher.
