---
updated: '2026-05-13'
---

# Requête en refus d'effacement — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Faire de [docs/faillis/effacement.md](../../faillis/effacement.md) la page pilier sur le refus d'effacement, en y intégrant une sous-section dédiée à la **requête en refus d'effacement** déposée par le parquet (et les autres demandeurs), et compléter [docs/comprendre/acteurs-secondaires.md](../../comprendre/acteurs-secondaires.md) avec un paragraphe correspondant côté procureur du Roi.

**Architecture:** Passe éditoriale chirurgicale sur 2 fichiers Markdown. Un seul commit par fichier. Build Zensical de vérification + check des ancres générées. Un commit final pour `log.md` et rafraîchissement des dates `updated:`.

**Tech Stack:** Markdown, Zensical (build), `inject_git_dates.py` (rafraîchissement front matter).

**Spec :** [docs/superpowers/specs/2026-05-13-requete-refus-effacement-design.md](../specs/2026-05-13-requete-refus-effacement-design.md)

---

## File structure

À modifier (ordre d'édition) :

1. `docs/faillis/effacement.md` — 3 éditions (mention intro section « Le principe », encadré fin section « Quelles dettes », sous-section enrichie « La requête en refus d'effacement »).
2. `docs/comprendre/acteurs-secondaires.md` — 1 édition (paragraphe « La requête en refus d'effacement » dans la section « Le procureur du Roi »).
3. `log.md` — entrée du jour + rafraîchissement automatique des dates `updated:` via le script.

Aucun fichier à créer. Aucun test pytest à écrire (édition Markdown).

---

### Task 1 : `docs/faillis/effacement.md` — 3 éditions, 1 commit

Trois éditions dans le même fichier, regroupées en un seul commit.

**Files:**
- Modify: `docs/faillis/effacement.md` (paragraphe ligne 16, fin section ligne 46, fin section ligne 71)

#### Édition 1.1 — mention courte dans la section « Le principe »

- [ ] **Step 1 : Édit 1.1**

Utiliser l'outil Edit avec :

`old_string` :
```
L'effacement intervient au moment du jugement de clôture. Vous n'avez aucune procédure à lancer, aucun formulaire à remplir, aucun frais à payer. Dès que le tribunal prononce la clôture, vous êtes libéré de toutes les dettes concernées. Les créanciers ne peuvent plus vous poursuivre pour les montants effacés, et vos revenus futurs ne peuvent plus être saisis au titre de ces anciennes dettes.
```

`new_string` :
```
L'effacement intervient au moment du jugement de clôture. Vous n'avez aucune procédure à lancer, aucun formulaire à remplir, aucun frais à payer. Dès que le tribunal prononce la clôture, vous êtes libéré de toutes les dettes concernées. Les créanciers ne peuvent plus vous poursuivre pour les montants effacés, et vos revenus futurs ne peuvent plus être saisis au titre de ces anciennes dettes.

Ce bénéfice n'est cependant pas automatiquement garanti : le tribunal peut le refuser à la demande du procureur du Roi, du curateur, d'un créancier impayé ou d'office, en cas de fautes graves et caractérisées ayant contribué à la faillite. Voir plus bas : [Quand l'effacement peut-il être refusé ?](#quand-leffacement-peut-il-etre-refuse).
```

#### Édition 1.2 — encadré renvoi en fin de section « Quelles dettes sont effacées ? »

- [ ] **Step 2 : Édit 1.2**

`old_string` :
```
!!! warning "Attention aux dettes nées après le jugement"
    Tous les engagements que vous prenez après la date du jugement déclaratif — achats, abonnements, crédits — restent entièrement à votre charge personnelle. L'effacement ne concerne que les dettes antérieures à ce jugement.

---

## Votre conjoint ou cohabitant en bénéficie aussi
```

`new_string` :
```
!!! warning "Attention aux dettes nées après le jugement"
    Tous les engagements que vous prenez après la date du jugement déclaratif — achats, abonnements, crédits — restent entièrement à votre charge personnelle. L'effacement ne concerne que les dettes antérieures à ce jugement.

!!! note "Le refus d'effacement est possible"
    Même quand vos dettes entrent dans le périmètre ci-dessus, l'effacement n'est pas garanti. Si vous avez commis des fautes graves et caractérisées ayant contribué à la faillite, le tribunal peut le refuser à la demande du curateur, du procureur du Roi, d'un créancier impayé ou d'office. Voir plus bas : [Quand l'effacement peut-il être refusé ?](#quand-leffacement-peut-il-etre-refuse).

---

## Votre conjoint ou cohabitant en bénéficie aussi
```

#### Édition 1.3 — sous-section enrichie « La requête en refus d'effacement »

- [ ] **Step 3 : Édit 1.3**

`old_string` :
```
Le refus peut être total (toutes vos dettes restent dues) ou partiel (seule une catégorie ou un montant spécifique reste dû). La demande de refus peut être formulée par le curateur, le procureur du Roi, un créancier impayé, ou soulevée d'office par le tribunal. Le délai pour une demande préventive est de quatre ans après le jugement déclaratif ; après la publication du jugement de clôture, le délai pour former une tierce opposition est de trois mois.

---

## Comment préserver votre droit à l'effacement ?
```

`new_string` :
```
Le refus peut être total (toutes vos dettes restent dues) ou partiel (seule une catégorie ou un montant spécifique reste dû). La demande de refus peut être formulée par le curateur, le procureur du Roi, un créancier impayé, ou soulevée d'office par le tribunal. Le délai pour une demande préventive est de quatre ans après le jugement déclaratif ; après la publication du jugement de clôture, le délai pour former une tierce opposition est de trois mois.

### La requête en refus d'effacement

Le refus n'est jamais prononcé automatiquement par le tribunal : il faut qu'une partie en fasse la demande, ou que le tribunal s'en saisisse d'office. **Quatre voies** mènent à un examen du refus.

Le **procureur du Roi** (le parquet) est l'acteur central. Il peut déposer une **requête en refus d'effacement** devant le tribunal de l'entreprise lorsqu'il estime qu'une faute grave et caractérisée a contribué à la faillite. Cette requête peut être déposée à tout moment de la procédure, jusqu'à quatre ans après le jugement déclaratif. Elle est généralement motivée par les éléments transmis au parquet par le curateur dans son rapport sur les causes de la faillite, ou par une plainte qui aboutit à un signalement.

Le **curateur** peut lui aussi former une demande, dans le cadre de son rapport au juge-commissaire ; il agit en représentant des intérêts de la masse des créanciers.

Un **créancier impayé** peut former une demande individuelle s'il dispose d'éléments concrets démontrant une faute grave. Cette voie reste rare en pratique parce qu'elle suppose une connaissance approfondie du dossier.

Enfin, le **tribunal de l'entreprise** peut soulever la question d'office, sur la base des éléments versés au dossier.

Dans tous les cas, le tribunal organise une **audience contradictoire** à laquelle vous êtes convoqué. La représentation par un avocat n'est pas obligatoire mais est fortement recommandée — c'est votre statut futur de débiteur libéré qui est en jeu. L'audience porte exclusivement sur la matérialité des fautes invoquées et leur lien causal avec la faillite. Si le tribunal écarte la requête, votre droit à l'effacement est confirmé ; s'il l'accueille, le refus peut être total ou partiel selon la gravité.

Après le jugement de clôture, le seul recours subsiste est la **tierce opposition** dans les trois mois suivant la publication. Au-delà, l'effacement est définitif.

---

## Comment préserver votre droit à l'effacement ?
```

#### Commit Task 1

- [ ] **Step 4 : Commit**

```bash
git add docs/faillis/effacement.md
git commit -m "Refus d'effacement : page pilier (intro, encadré, sous-section requête)"
```

Message exact : `Refus d'effacement : page pilier (intro, encadré, sous-section requête)`

---

### Task 2 : `docs/comprendre/acteurs-secondaires.md` — 1 édition, 1 commit

**Files:**
- Modify: `docs/comprendre/acteurs-secondaires.md` (entre lignes 42 et 44)

- [ ] **Step 1 : Édition**

`old_string` :
```
### La demande d'interdiction de gérer

Indépendamment de toute poursuite pénale, le procureur peut demander au tribunal de prononcer une interdiction de gérer à l'encontre d'un dirigeant si des fautes graves ont été commises de manière répétée, si le dirigeant a été impliqué dans plusieurs faillites successives, ou si son comportement témoigne d'une malhonnêteté manifeste.

!!! danger "Collaborez pour éviter les poursuites pénales"
```

`new_string` :
```
### La demande d'interdiction de gérer

Indépendamment de toute poursuite pénale, le procureur peut demander au tribunal de prononcer une interdiction de gérer à l'encontre d'un dirigeant si des fautes graves ont été commises de manière répétée, si le dirigeant a été impliqué dans plusieurs faillites successives, ou si son comportement témoigne d'une malhonnêteté manifeste.

### La requête en refus d'effacement

Le procureur du Roi peut également déposer une requête en refus d'effacement des dettes lorsqu'un failli personne physique a commis des fautes graves et caractérisées ayant contribué à la faillite. Cette requête est l'arme procédurale principale du parquet pour empêcher la « seconde chance » dans les dossiers qui ne le méritent pas. Voir [l'effacement des dettes](../faillis/effacement.md#la-requete-en-refus-deffacement) pour le détail de la mécanique.

!!! danger "Collaborez pour éviter les poursuites pénales"
```

- [ ] **Step 2 : Commit**

```bash
git add docs/comprendre/acteurs-secondaires.md
git commit -m "Refus d'effacement : paragraphe procureur du Roi"
```

Message exact : `Refus d'effacement : paragraphe procureur du Roi`

---

### Task 3 : Build Zensical et vérification des ancres

**Files:** aucun à modifier.

- [ ] **Step 1 : Build**

```bash
.venv/Scripts/zensical build
```

Résultat attendu : `Build finished in <N>s`, sans erreur Jinja, sans warning d'ancre interne.

- [ ] **Step 2 : Vérifier que les ancres internes existent dans le HTML produit**

```bash
.venv/Scripts/python -c "
import re
html = open('site/faillis/effacement/index.html', encoding='utf-8').read()
ancres_attendues = ['quand-leffacement-peut-il-etre-refuse', 'la-requete-en-refus-deffacement']
for a in ancres_attendues:
    found = re.search(rf'id=\"{a}\"', html) is not None
    print(f'#{a} -> {\"OK\" if found else \"MANQUANT\"}')"
```

Résultat attendu : `#quand-leffacement-peut-il-etre-refuse -> OK` et `#la-requete-en-refus-deffacement -> OK`.

Si l'une des deux est `MANQUANT`, ouvrir le HTML rendu pour voir quel slug Zensical a généré (probablement avec un autre encodage des accents), puis adapter en utilisant la syntaxe d'ancre explicite Markdown supportée par Zensical (MkDocs `attr_list`) :

```markdown
## Quand l'effacement peut-il être refusé ? { #quand-leffacement-peut-il-etre-refuse }
### La requête en refus d'effacement { #la-requete-en-refus-deffacement }
```

Édition correctrice à faire dans `docs/faillis/effacement.md` aux titres concernés, et rebuild + recheck.

- [ ] **Step 3 : Vérifier que le lien cross-document depuis acteurs-secondaires.md fonctionne**

```bash
.venv/Scripts/python -c "
import re
html = open('site/comprendre/acteurs-secondaires/index.html', encoding='utf-8').read()
m = re.search(r'href=\"[^\"]*effacement[^\"]*la-requete[^\"]*\"', html)
print('lien cross-doc:', 'OK' if m else 'MANQUANT', '|', m.group(0)[:100] if m else '')"
```

Résultat attendu : `lien cross-doc: OK` avec un href qui contient `effacement` et `la-requete`.

- [ ] **Step 4 : Pas de commit pour cette task** (vérification uniquement).

---

### Task 4 : Grep de contrôle

**Files:** aucun à modifier.

- [ ] **Step 1 : Vérifier la densité de mentions du parquet sur la page pilier**

```bash
grep -c "parquet\|procureur du Roi" docs/faillis/effacement.md
```

Résultat attendu : **≥ 4** (avant le refactor : 1).

- [ ] **Step 2 : Vérifier que la sous-section enrichie est bien présente**

```bash
grep -c "requête en refus d'effacement\|audience contradictoire\|tierce opposition" docs/faillis/effacement.md
```

Résultat attendu : **≥ 3**.

- [ ] **Step 3 : Vérifier la cohérence côté acteurs-secondaires.md**

```bash
grep -c "requête en refus d'effacement" docs/comprendre/acteurs-secondaires.md
```

Résultat attendu : **≥ 1**.

- [ ] **Step 4 : Pas de commit** (vérification uniquement).

---

### Task 5 : Rafraîchir les dates `updated:` + entrée `log.md`

**Files:**
- Modify: `docs/faillis/effacement.md`, `docs/comprendre/acteurs-secondaires.md` (front matter `updated:` rafraîchi automatiquement)
- Modify: `log.md`

- [ ] **Step 1 : Rafraîchir les dates updated**

```bash
.venv/Scripts/python scripts/inject_git_dates.py
```

Résultat attendu : `N fichier(s) mis à jour, M inchangé(s).` avec N ≥ 2 (les 2 fichiers édités).

- [ ] **Step 2 : Ajouter une entrée dans `log.md`**

Utiliser Edit, juste après le séparateur `---` (ligne 7) et avant la première entrée existante.

`old_string` :
```
---

## [2026-05-13] edit | Nuancer le délai de 30 jours (déclarations de créance)
```

`new_string` :
```
---

## [2026-05-13] edit | Requête en refus d'effacement : page pilier

Enrichi [docs/faillis/effacement.md](docs/faillis/effacement.md) avec une sous-section dédiée à la **requête en refus d'effacement** déposée par le parquet (et les autres demandeurs : curateur, créancier impayé, tribunal d'office). Détaille la procédure : juridiction (tribunal de l'entreprise), audience contradictoire, défense, tierce opposition après clôture. Ajout d'un paragraphe correspondant dans [docs/comprendre/acteurs-secondaires.md](docs/comprendre/acteurs-secondaires.md) côté procureur du Roi, qui pointe vers la page pilier. Spec et plan dans [docs/superpowers/](docs/superpowers/).

## [2026-05-13] edit | Nuancer le délai de 30 jours (déclarations de créance)
```

- [ ] **Step 3 : Commit groupé**

```bash
git add docs/ log.md
git commit -m "log + rafraîchissement updated : requête en refus d'effacement"
```

Message exact : `log + rafraîchissement updated : requête en refus d'effacement`

- [ ] **Step 4 : Vérification finale**

```bash
.venv/Scripts/pytest tests/ -q
```

Résultat attendu : `13 passed`. Aucune régression dans les tests du script `inject_git_dates`.

```bash
.venv/Scripts/python scripts/inject_git_dates.py --check
```

Résultat attendu : exit 1 (artefact de bootstrap déjà connu — les fichiers viennent d'être commités donc leur dernier commit Git est postérieur à la date `updated:` qu'ils contiennent ; pas d'action requise).
