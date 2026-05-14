---
title: lastmod automatique dérivé de Git
date: 2026-05-13
status: draft
updated: '2026-05-13'
---
# Spec — `lastmod` automatique dérivé de Git

## Contexte

Le site **infofaillite.be** (Zensical 0.0.24) sert une documentation juridique
sur la faillite belge. Le SEO/GEO est central : on veut signaler aux moteurs
de recherche la fraîcheur de chaque page, surtout parce que le contenu
légal peut évoluer et qu'on veut être préféré aux pages obsolètes
concurrentes.

État actuel :

- `site/sitemap.xml` ne contient **aucun** `<lastmod>` — uniquement `<loc>`.
- Aucune page n'affiche au lecteur la date de dernière mise à jour.
- Le template Zensical `partials/source-file.html` sait déjà afficher
  `page.meta.git_revision_date_localized`, mais Zensical 0.0.24 ne peuple pas
  cette clé (pas d'équivalent du plugin MkDocs `git-revision-date-localized`).
- `overrides/` est déjà configuré dans `zensical.toml`
  (`custom_dir = "overrides"`).

## Objectif

Faire en sorte que chaque page du site déclare automatiquement une date de
dernière modification fiable, dérivée du **dernier commit Git qui a touché
le fichier source** (et non de la date de build). Cette date doit apparaître :

1. dans le **sitemap.xml** (`<lastmod>` sous chaque `<url>`) — pour les robots ;
2. dans le **pied de chaque page** sous forme « Dernière mise à jour : 13 mai 2026 » — pour le lecteur.

## Non-objectifs

- Pas de gestion `<priority>` ou `<changefreq>` dans le sitemap (Google les
  ignore en pratique).
- Pas de `dateCreated` ou de date de création affichée.
- Pas d'intégration dans le JSON-LD existant (`docs/javascripts/schema.js`)
  pour l'instant — peut venir plus tard.
- Pas de wrapper CI automatique : on documente le workflow et l'utilisateur
  ou un futur job CI l'exécute manuellement avant `zensical build`.

## Architecture

Une chaîne pré-build → build, avec deux overrides de templates Zensical.

```
┌────────────────────────────────┐
│ 1. scripts/inject_git_dates.py │   (pré-build, manuel ou via CI)
│   - parcourt docs/**/*.md      │
│   - git log -1 --format=%cI    │
│   - écrit `updated: YYYY-MM-DD`│
│     dans le front matter       │
└──────────────┬─────────────────┘
               │
               ▼
┌────────────────────────────────┐
│ 2. zensical build              │
│   - lit page.meta.updated      │
│   - rend overrides/sitemap.xml │
│   - rend overrides/partials/   │
│     source-file.html           │
└────────────────────────────────┘
```

## Composants

### Composant 1 — `scripts/inject_git_dates.py`

**Rôle.** Injecter dans le front matter de chaque fichier `.md` du dossier
`docs/` la clé `updated:` avec la date du dernier commit Git qui a modifié
le fichier.

**Entrée.** Le répertoire `docs/` (relatif à la racine du projet).
**Sortie.** Les fichiers `.md` modifiés en place (uniquement quand la date
change).

**Algorithme.**

1. Parcourir récursivement `docs/**/*.md`.
2. Pour chaque fichier :
   a. Obtenir la date du dernier commit qui le touche :
      `git log -1 --format=%cI -- <chemin>`. Si la sortie est vide (fichier
      non commité), fallback sur `os.path.getmtime`.
   b. Normaliser en `YYYY-MM-DD` (date seule, suffisante pour sitemap et
      affichage ; on jette l'heure).
   c. Charger le front matter YAML existant (si présent) avec PyYAML.
   d. Si `updated` existe déjà et vaut la même valeur → **skip** (pas de
      réécriture, pas de diff parasite).
   e. Sinon, mettre à jour `updated` (créer le front matter s'il n'existe pas).
   f. Réécrire le fichier en préservant l'ordre des autres clés du front
      matter et le corps Markdown inchangé.
3. Logger en fin de run : « N fichiers mis à jour, M fichiers inchangés. »

**Robustesse.**

- Si le repo n'a pas d'historique Git (rare, possible en CI shallow clone
  avec `fetch-depth: 1`), fallback `mtime` partout. Le script doit le détecter
  et le signaler via un avertissement.
- Si un fichier n'a pas de front matter du tout, en créer un avec uniquement
  `updated:` (et un séparateur `---`).
- Pas d'arguments CLI requis ; on accepte un argument optionnel `--check`
  qui sort en code de retour `1` si au moins un fichier aurait été modifié
  (utile pour un futur hook CI sans réécriture).

**Dépendances.** PyYAML (déjà présent dans `requirements.txt` via Zensical).
Aucune nouvelle dépendance.

### Composant 2 — `overrides/sitemap.xml`

**Rôle.** Ajouter `<lastmod>` à chaque entrée du sitemap, dérivé de
`page.meta.updated`.

**Implémentation.** Copie minimale du template Zensical d'origine
(`templates/sitemap.xml` dans la lib) avec un ajout conditionnel :

```jinja
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
```

Si `page.meta.updated` est absent (par exemple pour une page auto-générée
comme `SUMMARY` ou `404`), on omet simplement `<lastmod>` pour cette URL —
c'est conforme à la spec sitemap.org.

### Composant 3 — `overrides/partials/source-file.html`

**Rôle.** Afficher « Dernière mise à jour : <date localisée FR> » en pied
de chaque page.

**Implémentation.** Copie du partial Zensical d'origine, avec une branche
supplémentaire :

```jinja
{% if page.meta %}
  {% if page.meta.git_revision_date_localized %}
    {% set updated = page.meta.git_revision_date_localized %}
  {% elif page.meta.updated %}
    {% set updated = page.meta.updated %}
  {% elif page.meta.revision_date %}
    {% set updated = page.meta.revision_date %}
  {% endif %}
  ...
{% endif %}
```

Localisation de la date au format `13 mai 2026` : Zensical hérite du moteur
de templates Material qui dispose d'un filtre `| date` Jinja ; à défaut, on
formate côté Python dans le script (en stockant `updated` comme `13 mai 2026`
dans une clé séparée `updated_fr`, pour ne pas perdre le format ISO du
sitemap). **Choix retenu** : stocker `updated` (ISO court) pour le sitemap,
formater l'affichage côté template via filtre. À ajuster si le filtre n'est
pas dispo dans Zensical 0.0.24 — fallback : affichage ISO brut (13/05/2026
ou 2026-05-13), pas grave pour un premier jet.

### Composant 4 — Documentation projet

Ajouter dans `CLAUDE.md` une ligne dans la section **Workflow** :

> Avant un build de release, lancer `python scripts/inject_git_dates.py`
> puis commiter les éventuelles mises à jour de front matter, **puis**
> lancer `zensical build`.

Et une entrée `log.md` au moment du déploiement de la fonctionnalité.

## Flux de données

```
git history ──┬─► inject_git_dates.py ──► docs/**/*.md
              │      (updated: YYYY-MM-DD dans front matter)
              │
              └─► commit des changements
                        │
                        ▼
                  zensical build
                        │
                        ├─► overrides/sitemap.xml          ──► site/sitemap.xml (avec <lastmod>)
                        └─► overrides/partials/source-file.html ──► HTML de chaque page (avec mention en pied)
```

## Gestion des erreurs

| Scénario | Comportement attendu |
|---|---|
| Fichier non commité (untracked / nouveau) | Fallback `mtime`, log info, on continue. |
| Repo en shallow clone (CI) | Warning global, fallback `mtime` pour tous les fichiers concernés. |
| Front matter YAML mal formé | Erreur explicite avec chemin du fichier ; le script s'arrête (l'auteur doit corriger). |
| Fichier sans front matter | En créer un minimal avec uniquement `updated:`. |
| `git log` indisponible (pas un repo Git) | Erreur explicite, sortie non-zero. |
| Date déjà à jour | Skip silencieux, comptabilisé pour le log final. |

## Plan de test

- **Test 1 — Création initiale** : exécuter le script sur un repo propre,
  vérifier que tous les `.md` reçoivent un `updated:`, et que la date
  correspond bien au dernier commit Git de chaque fichier.
- **Test 2 — Idempotence** : relancer immédiatement le script, vérifier que
  zéro fichier est modifié.
- **Test 3 — Modification suivie** : modifier un fichier, commiter, relancer
  le script, vérifier que **seul** ce fichier voit sa date mise à jour.
- **Test 4 — Sitemap** : `zensical build` puis inspection de
  `site/sitemap.xml` — au moins une `<url>` doit contenir `<lastmod>`, et
  la date doit correspondre au commit.
- **Test 5 — Pied de page** : ouvrir une page HTML rendue, vérifier la
  présence visible de « Dernière mise à jour : … ».
- **Test 6 — Page sans historique** : créer un nouveau `.md` non commité,
  relancer le script, vérifier le fallback `mtime`.
- **Test 7 — `--check`** : modifier un fichier sans commiter, relancer
  `scripts/inject_git_dates.py --check`, vérifier que le code de sortie est
  `1`.

## Risques & questions ouvertes

- **R1 — Filtre `| date` dans Jinja sous Zensical 0.0.24.** À vérifier dès
  la mise en place du partial. Si absent, fallback à ISO brut sans casser
  l'implémentation.
- **R2 — Pollution du diff Git.** Si on lance le script avant chaque commit,
  un commit qui touche un seul fichier peut déclencher l'update de `updated`
  sur ce fichier — c'est désiré. Mais si on lance le script *après* avoir
  poussé un commit, on ajoute un second commit « cosmétique » pour la date.
  → Convention : lancer le script **avant** `git commit` (potentiellement
  via un hook `pre-commit`), pour que la mise à jour de `updated` aille dans
  le même commit que le contenu. Hors scope d'automatiser ce hook ici.
- **R3 — Pages sans contenu modifié mais affectées par un renommage.** Un
  `git mv` crée un commit ; la date capturera ce renommage. C'est cohérent
  (l'URL canonique a peut-être changé).
- **R4 — Pages auto-générées (`SUMMARY`, `404`).** Pas de front matter, donc
  pas de `<lastmod>` dans le sitemap. Acceptable.

## Décisions de design

- **Stocker dans le front matter plutôt qu'en JSON externe** : permet à
  Zensical de l'exposer naturellement via `page.meta`, sans bricolage côté
  templates.
- **Date seule (`YYYY-MM-DD`) plutôt que datetime complet** : suffisant pour
  sitemap.org, plus simple à afficher, et évite des diffs Git à chaque build
  par modification de l'heure.
- **Idempotence stricte** : c'est ce qui rend l'outil utilisable dans un
  workflow standard sans polluer l'historique.
- **Pas de wrapper de build automatique** : Zensical 0.0.24 n'a pas de
  système de plugins exposé ; un script externe est le contrat le plus
  simple et le moins fragile. Si une future version de Zensical expose un
  hook `on_pre_build`, on pourra migrer.
