# CLAUDE.md — infofaillite

Notes de contexte pour Claude. À mettre à jour quand le projet évolue.

## Projet

Site documentaire **Guide de la faillite en Belgique** (infofaillite.be), basé sur le Livre XX du Code de droit économique. Public visé : faillis/dirigeants, créanciers, curieux du droit de l'insolvabilité belge.

- Stack : **Zensical** (statique, dérivé de MkDocs Material). Config dans [zensical.toml](zensical.toml).
- Sources Markdown : [docs/](docs/).
- Dépendances Python : [requirements.txt](requirements.txt), venv local dans `.venv/`.
- **Branche de travail effective : `gh-pages`** (malgré son nom, c'est elle qui contient les sources à jour ; `main` est très en retard et n'est plus utilisée pour le développement). Commiter directement sur `gh-pages`, qui est déployée automatiquement par GitHub Actions.

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
- **Ancres internes** : Zensical slugifie les titres en ASCII (accents et apostrophes supprimés). Exemple : `## Quand l'effacement peut-il être refusé ?` → `#quand-leffacement-peut-il-etre-refuse`. Vérifier au build avec un grep `id="..."` dans `site/<page>/index.html` ; si KO, utiliser l'ancre explicite `## Titre { #ancre-personnalisee }`.
- **Admonitions** : syntaxe MkDocs (`!!! danger`, `!!! note`, `!!! warning`, etc.) — utilisée notamment pour les délais critiques.
- **Front matter YAML** : `description` + `keywords` en tête de chaque page SEO-sensible.
- **Pas d'emojis** dans les pages éditoriales sauf demande explicite.

## Workflow

- Modifier les sources dans `docs/`, vérifier au besoin avec un build local Zensical.
- Les commits récents montrent un style de message court et descriptif en français (« Refonte éditoriale complète… », « SEO & GEO », « analytics »). Suivre ce style.
- **Toujours journaliser** les modifications de fond (ingest, refonte, passe SEO, lint, etc.) dans [log.md](log.md) avec le préfixe `## [YYYY-MM-DD] <type> | <titre>`.
- **Avant chaque build** (ou avant de commiter une modification de contenu) : lancer `python scripts/inject_git_dates.py` pour rafraîchir la clé `updated:` dans le front matter. Cette date alimente `<lastmod>` du sitemap et le pied de page « Dernière mise à jour » côté lecteur. Le script est idempotent et ne touche que les fichiers dont la date a changé. Mode `--check` disponible pour CI (exit 1 si des fichiers nécessiteraient une mise à jour).

## Passes éditoriales (relecture / enrichissement)

Pour toute modification du corps de texte du site (relecture, nuance, ajout de section, correction factuelle) déclenchée par une instruction de l'utilisateur :

- **Pas de spec, pas de plan, pas de skill brainstorming.** Modifier directement les fichiers Markdown concernés sur la base des éléments donnés, en tenant compte du contexte (Livre XX, public, ligne éditoriale).
- Si une demande est vraiment ambiguë (risque d'erreur factuelle, choix éditorial structurant qui touche plusieurs pages), poser **une question ciblée** avant d'écrire. Sinon, exécuter.
- Un commit court par modification cohérente, message en français suivant le style du projet.
- Après une passe qui touche plusieurs fichiers : `python scripts/inject_git_dates.py` puis entrée dans [log.md](log.md), commités ensemble.
- Le workflow spec→plan→exécution (skills `brainstorming` / `writing-plans` / `subagent-driven-development`) reste réservé aux **chantiers techniques** : code, scripts, configuration, automatisations CI, refontes architecturales.

### Procédure de clôture de session de relecture

Lorsque l'utilisateur annonce qu'il clôture la session (« je termine », « clôture », « on arrête »), dérouler les étapes suivantes — l'ordre importe car le script de dates lit le dernier commit Git :

1. **Inventaire** : `git status` + `git diff --stat` pour identifier toutes les pages modifiées (y compris celles modifiées hors session via l'éditeur).
2. **Vérifier les diffs non vus** : `git diff <fichier>` pour chaque page modifiée qui n'a pas été éditée explicitement dans la session.
3. **Commits éditoriaux** : un commit court par page (ou groupe cohérent), en français, style du projet. Pas encore le log.
4. **Bump des dates** : `.venv/Scripts/python.exe scripts/inject_git_dates.py` — le script ne touche que les pages dont la date Git a changé. Mode `--check` disponible pour vérifier sans écrire.
5. **Entrée [log.md](log.md)** : `## [YYYY-MM-DD] edit | <titre synthétique>` en tête du journal, avec une puce par page touchée et un renvoi explicite si une correction factuelle importante a été faite.
6. **Commit final** groupant le bump des dates et l'entrée du log : message type `log + lastmod : relecture du <date>`.
7. **Confirmation** : `git log --oneline -10` pour vérifier la chaîne de commits ; ne pas pousser sauf demande explicite.

Si une page a été modifiée mais que le script ne la bumpe pas, c'est qu'elle n'a pas encore été commitée : repasser à l'étape 3 d'abord.

## Historique récent

- La refonte éditoriale globale (`aad0a0f`) a restructuré l'ensemble de la documentation ; voir [log.md](log.md) pour la chronologie détaillée des évolutions ultérieures.
- Le dossier [infofaillite/](infofaillite/) à la racine est apparu récemment (untracked) — vérifier son rôle avant d'y toucher.
