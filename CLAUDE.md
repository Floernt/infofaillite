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
- [docs/faillis/](docs/faillis/) — deux parcours : **indépendant en nom propre** (effacement des dettes) et **dirigeant de société** ([societe-en-faillite.md](docs/faillis/societe-en-faillite.md), [responsabilite-dirigeant.md](docs/faillis/responsabilite-dirigeant.md)), plus des pages communes (obligations, droits, checklist, reprise d'activité, interdiction). Clé de front matter `public: [independant, dirigeant]` : affichée dans le bandeau (« Cette page concerne »).
- [docs/faq/README.md](docs/faq/README.md) — FAQ unique (5e onglet) : questions en `<details class="ifa-faq" id="…" data-profils="independant dirigeant creancier travailleur" markdown>` sous des H2 de thème à ancre explicite ; filtres dans [docs/javascripts/faq.js](docs/javascripts/faq.js) (`#profil=…&theme=…&q=…` ; recherche par mots avec racines, classement par pertinence et surlignage). Le JSON-LD `FAQPage` est généré par [scripts/build_faq.py](scripts/build_faq.py) (appelé par `inject_git_dates.py`, mode `--check`). Les anciennes `faillis/faq.md` et `creanciers/faq.md` sont des renvois hors menu.
- [docs/creanciers/](docs/creanciers/) — déclaration de créance, sûretés/cautions, vérification, dividendes, droits, catégories, FAQ.
- [docs/glossaire.md](docs/glossaire.md), [docs/delais.md](docs/delais.md), [docs/ressources.md](docs/ressources.md), [docs/a-propos.md](docs/a-propos.md).
- [docs/actualites/](docs/actualites/) — notes d'actualité (jurisprudence, doctrine, législation), une par fichier `AAAA-MM-JJ-slug.md`. `README.md` (liste) et `themes.md` (par thème) sont générés entre marqueurs.
- [data/themes.yml](data/themes.yml) — taxonomie des thèmes et rattachement de chaque thème aux pages du guide (hors `docs/`, non publiée).
- [docs/javascripts/](docs/javascripts/) — analytics (clicky), JSON-LD (schema.js), filtres de la liste des actualités (actualites.js).
- [overrides/main.html](overrides/main.html) — gabarit commun : bandeau de page (fil d'Ariane, rubrique, H1 repris du Markdown, date de mise à jour), JSON-LD `BreadcrumbList` côté serveur, et pour les notes le cartouche de la source et le JSON-LD `Article`.
- [overrides/home.html](overrides/home.html) — gabarit de l'accueil (`template: home.html` dans [docs/README.md](docs/README.md)) : ouverture, tuiles et bandeau écrits en Markdown avec les classes `ifa-*`.
- [overrides/partials/header.html](overrides/partials/header.html) et [footer.html](overrides/partials/footer.html) — en-tête avec les quatre rubriques intégrées, pied de page en colonnes (seul accès aux pages hors menu : délais, glossaire, ressources, à propos, contact).
- [docs/stylesheets/extra.css](docs/stylesheets/extra.css) — identité visuelle : palette Yale Blue `#2e4057`, Carrot Orange `#f18f01`, Bondi Blue `#048ba8`, Yellow Green `#99c24d`, Graphite `#2f2d2e` (variantes assombries pour le petit texte) ; police Albert Sans (`[project.theme.font]`).

## Navigation

- Le menu est **explicite** : `nav` dans [zensical.toml](zensical.toml), cinq rubriques (Je suis en faillite, Je suis créancier, Comprendre la procédure, Actualités, Questions fréquentes) avec des libellés courts. Le H1 de chaque page reste celui du Markdown.
- **Toute nouvelle page de fond doit être ajoutée au `nav`**. [tests/test_nav.py](tests/test_nav.py) échoue sinon. Seules exceptions : l'accueil, les pages du pied de page et les notes d'actualité.
- Le **sitemap est statique**, généré par [scripts/build_sitemap.py](scripts/build_sitemap.py) dans [overrides/sitemap.xml](overrides/sitemap.xml) : avec un menu explicite, celui de Zensical ne listerait que les pages du menu. Il est régénéré automatiquement par `inject_git_dates.py`.
- Les pages d'entrée de rubrique ouvrent sur une grille `ifa-subtiles` (liens numérotés dans l'ordre du menu) : la tenir à jour quand une page est ajoutée à la rubrique.

## Actualités : publier une note

1. `python scripts/new_actualite.py "Titre" --type jurisprudence|doctrine|legislation|pratique --themes slug1,slug2 [--date AAAA-MM-JJ]` crée le squelette ; les slugs viennent de [data/themes.yml](data/themes.yml).
2. Rédiger la note. Remplir ou supprimer les champs vides du front matter.
3. `python scripts/build_actualites.py` : valide les notes, régénère la liste, la page par thème, l'encart de l'accueil, les renvois en fin de note et le bloc « Actualités liées » en fin de chaque page du guide concernée. `--check` pour vérifier sans écrire.
4. Commit éditorial, puis `inject_git_dates.py` et commit `lastmod` (procédure habituelle).

Règles :

- **Ne jamais éditer à la main** le contenu entre `<!-- actualites:auto:start -->` et `<!-- actualites:auto:end -->` : il est écrasé à chaque génération.
- **Front matter compatible Zensical** : dates toujours entre guillemets (`'2026-10-15'`) et aucune valeur vide (`""` ou ligne supprimée). Sinon le build échoue avec « failed to extract field Markdown.meta », sans nommer le fichier. Le script de génération détecte ces deux cas et indique le fichier en cause.
- Ajouter un thème ou rattacher une page à un thème : éditer seulement [data/themes.yml](data/themes.yml), puis relancer la génération.
- **Publication programmée** : une note dont la `date` est future n'apparaît nulle part (liste, thèmes, accueil, pages du guide, sitemap) tant que la date n'est pas atteinte. Le workflow [deploy.yml](.github/workflows/deploy.yml) reconstruit le site chaque matin (05:00 UTC) et lance `build_actualites.py --drop-future` pour retirer les fichiers des notes futures avant le build : elles ne sont pas accessibles par URL avant leur date. Le cron ne tourne que sur `main` : une note programmée paraît seule, à condition d'avoir été fusionnée dans `main`. En local, `--check` peut signaler un écart après le passage d'une date : relancer la génération. `--today AAAA-MM-JJ` simule une autre date.
- Calendrier et points à vérifier des notes programmées : [superpowers/revue-actualites.md](superpowers/revue-actualites.md) (non publié).

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
- **Avant chaque build** (ou avant de commiter une modification de contenu) : lancer `python scripts/inject_git_dates.py` pour rafraîchir la clé `updated:` dans le front matter. Cette date alimente `<lastmod>` du sitemap (régénéré dans la foulée) et la mention « Mise à jour le … » du bandeau de page. Le script est idempotent et ne touche que les fichiers dont la date a changé. Mode `--check` disponible pour CI (exit 1 si des fichiers nécessiteraient une mise à jour).

## Passes éditoriales (relecture / enrichissement)

Pour toute modification du corps de texte du site (relecture, nuance, ajout de section, correction factuelle) déclenchée par une instruction de l'utilisateur :

- **Pas de spec, pas de plan, pas de skill brainstorming.** Modifier directement les fichiers Markdown concernés sur la base des éléments donnés, en tenant compte du contexte (Livre XX, public, ligne éditoriale).
- Si une demande est vraiment ambiguë (risque d'erreur factuelle, choix éditorial structurant qui touche plusieurs pages), poser **une question ciblée** avant d'écrire. Sinon, exécuter.
- Un commit court par modification cohérente, message en français suivant le style du projet.
- Après une passe qui touche plusieurs fichiers : `python scripts/inject_git_dates.py` puis entrée dans [log.md](log.md), commités ensemble.
- Le workflow spec→plan→exécution (skills `brainstorming` / `writing-plans` / `subagent-driven-development`) reste réservé aux **chantiers techniques** : code, scripts, configuration, automatisations CI, refontes architecturales.
- **Emplacement des specs et plans** : toujours à la racine du repo, dans [superpowers/specs/](superpowers/specs/) et [superpowers/plans/](superpowers/plans/). **Jamais sous `docs/`** : tout fichier `.md` placé dans `docs/` est publié sur infofaillite.be et indexé dans le sitemap. Les specs et plans sont des artefacts internes au workflow et ne doivent pas être servis.

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
