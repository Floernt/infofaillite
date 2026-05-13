---
title: Requête en refus d'effacement (acte du parquet) — page pilier effacement.md
date: 2026-05-13
status: draft
---

# Spec — Requête en refus d'effacement du parquet

## Contexte

La requête en refus d'effacement déposée par le **procureur du Roi**
(parquet) est l'arme procédurale centrale du ministère public dans une
faillite de personne physique. Elle vise à empêcher le bénéfice de
l'effacement automatique des dettes lorsque le failli a commis des
fautes graves et caractérisées ayant contribué à la faillite.

État actuel de la documentation :

- [docs/faillis/effacement.md](../../faillis/effacement.md) ligne 71
  liste les quatre demandeurs possibles (curateur, parquet, créancier
  impayé, tribunal d'office) et donne deux délais (4 ans préventif /
  3 mois tierce opposition), mais **ne décrit aucune mécanique
  procédurale**.
- [docs/comprendre/acteurs-secondaires.md](../../comprendre/acteurs-secondaires.md)
  lignes 36–46 présente le procureur du Roi et sa demande
  d'interdiction de gérer, **mais rien sur le refus d'effacement** alors
  que c'est l'autre arme principale du parquet.
- [docs/comprendre/cloture.md](../../comprendre/cloture.md) ligne 46
  contient une mention secondaire cohérente, à laisser telle quelle.
- Aucune page n'explique au lecteur **comment** une requête en refus
  d'effacement est introduite, devant quelle juridiction, sous quelle
  forme, ni quelle audience s'ensuit.

## Objectif

Faire de [effacement.md](../../faillis/effacement.md) la **page pilier**
sur le refus d'effacement, en y détaillant la mécanique procédurale
(qui dépose, comment, quand, audience, défense, recours). Et compléter
[acteurs-secondaires.md](../../comprendre/acteurs-secondaires.md) avec
un paragraphe sur la requête côté procureur du Roi, qui renvoie à la
page pilier.

Principes éditoriaux :

1. Pas d'article du Code de droit économique cité dans la nouvelle
   sous-section (le reste de la page mentionne déjà XX.173 ; pas la
   peine de réincanter).
2. La sous-section enrichie reste accessible (pas un manuel de
   procédure), mais nomme explicitement les actes : *requête*,
   *audience contradictoire*, *tierce opposition*.
3. Le lecteur arrivant sur la page d'effacement doit être averti
   **deux fois** que le refus est possible : une mention courte en
   intro pour ne pas créer un faux sentiment de sécurité, et un
   encadré plus détaillé en fin de section « Quelles dettes sont
   effacées ? » avec un lien interne vers la sous-section
   procédurale.

## Non-objectifs

- Pas de page dédiée `docs/faillis/refus-effacement.md` (rejetée : pas
  besoin de fragmenter ; effacement.md devient le pilier).
- Pas de détail sur la stratégie de défense (mémoires, expertise
  comptable contradictoire, etc.) — c'est du conseil d'avocat, pas
  un guide grand public.
- Pas de modification de la phrase ligne 71 actuelle d'effacement.md :
  elle reste utile comme synthèse, la sous-section enrichie vient
  juste après.

## Composants

### Composant 1 — `docs/faillis/effacement.md`

Trois modifications, dans cet ordre.

**Modification 1.1 — mention courte dans l'intro de page** (après la
section d'intro existante, dans le paragraphe ligne 16).

Ajouter en fin de l'intro existante (paragraphe qui se termine par
« les revenus futurs ne peuvent plus être saisis au titre de ces
anciennes dettes ») la phrase :

```markdown
Ce bénéfice n'est cependant pas automatiquement garanti : le tribunal peut le refuser à la demande du procureur du Roi, du curateur, d'un créancier impayé ou d'office, en cas de fautes graves et caractérisées ayant contribué à la faillite. Voir plus bas : [Quand l'effacement peut-il être refusé ?](#quand-leffacement-peut-il-etre-refuse).
```

**Modification 1.2 — encadré renvoi en fin de section « Quelles dettes
sont effacées ? »** (juste avant le séparateur `---` ligne 46).

Insérer un encadré `!!! note` :

```markdown
!!! note "Le refus d'effacement est possible"
    Même quand vos dettes entrent dans le périmètre ci-dessus, l'effacement n'est pas garanti. Si vous avez commis des fautes graves et caractérisées ayant contribué à la faillite, le tribunal peut le refuser à la demande du curateur, du procureur du Roi, d'un créancier impayé ou d'office. Voir plus bas : [Quand l'effacement peut-il être refusé ?](#quand-leffacement-peut-il-etre-refuse).
```

**Modification 1.3 — sous-section enrichie « La requête en refus
d'effacement »** dans la section « Quand l'effacement peut-il être
refusé ? ». Insérer juste avant le séparateur `---` qui clôt cette
section (entre la phrase actuelle ligne 71 et le `---` ligne 73).

Contenu exact :

```markdown
### La requête en refus d'effacement

Le refus n'est jamais prononcé automatiquement par le tribunal : il faut qu'une partie en fasse la demande, ou que le tribunal s'en saisisse d'office. **Quatre voies** mènent à un examen du refus.

Le **procureur du Roi** (le parquet) est l'acteur central. Il peut déposer une **requête en refus d'effacement** devant le tribunal de l'entreprise lorsqu'il estime qu'une faute grave et caractérisée a contribué à la faillite. Cette requête peut être déposée à tout moment de la procédure, jusqu'à quatre ans après le jugement déclaratif. Elle est généralement motivée par les éléments transmis au parquet par le curateur dans son rapport sur les causes de la faillite, ou par une plainte qui aboutit à un signalement.

Le **curateur** peut lui aussi former une demande, dans le cadre de son rapport au juge-commissaire ; il agit en représentant des intérêts de la masse des créanciers.

Un **créancier impayé** peut former une demande individuelle s'il dispose d'éléments concrets démontrant une faute grave. Cette voie reste rare en pratique parce qu'elle suppose une connaissance approfondie du dossier.

Enfin, le **tribunal de l'entreprise** peut soulever la question d'office, sur la base des éléments versés au dossier.

Dans tous les cas, le tribunal organise une **audience contradictoire** à laquelle vous êtes convoqué. La représentation par un avocat n'est pas obligatoire mais est fortement recommandée — c'est votre statut futur de débiteur libéré qui est en jeu. L'audience porte exclusivement sur la matérialité des fautes invoquées et leur lien causal avec la faillite. Si le tribunal écarte la requête, votre droit à l'effacement est confirmé ; s'il l'accueille, le refus peut être total ou partiel selon la gravité.

Après le jugement de clôture, le seul recours subsiste est la **tierce opposition** dans les trois mois suivant la publication. Au-delà, l'effacement est définitif.
```

### Composant 2 — `docs/comprendre/acteurs-secondaires.md`

**Modification 2.1 — sous-section dédiée au refus d'effacement** dans
la section « Le procureur du Roi », à insérer **après** la sous-section
« La demande d'interdiction de gérer » (lignes 40–42) et **avant**
l'admonition `!!! danger "Collaborez pour éviter les poursuites
pénales"` (ligne 44).

Contenu exact :

```markdown
### La requête en refus d'effacement

Le procureur du Roi peut également déposer une requête en refus d'effacement des dettes lorsqu'un failli personne physique a commis des fautes graves et caractérisées ayant contribué à la faillite. Cette requête est l'arme procédurale principale du parquet pour empêcher la « seconde chance » dans les dossiers qui ne le méritent pas. Voir [l'effacement des dettes](../faillis/effacement.md#la-requete-en-refus-deffacement) pour le détail de la mécanique.
```

### Composant 3 — `log.md`

Une entrée datée 2026-05-13, type `edit`, qui synthétise.

## Considérations d'ancres Markdown

Les ancres générées par Zensical à partir des titres :

- `### La requête en refus d'effacement` →
  `#la-requete-en-refus-deffacement` (sans accent, sans apostrophe).
- `## Quand l'effacement peut-il être refusé ?` →
  `#quand-leffacement-peut-il-etre-refuse` (sans accent, sans
  apostrophe, sans point d'interrogation).

Ces deux ancres sont utilisées trois fois dans les modifications. À
**vérifier au build** : ouvrir
`site/faillis/effacement/index.html` et confirmer que ces deux IDs
existent bien sur les éléments correspondants.

## Plan de test

1. **Build Zensical** : `zensical build` doit passer sans erreur de
   lien interne ni warning d'ancre manquante.
2. **Vérification visuelle ancres** : grep dans
   `site/faillis/effacement/index.html` pour confirmer la présence des
   IDs `la-requete-en-refus-deffacement` et
   `quand-leffacement-peut-il-etre-refuse` (à ajuster si Zensical
   utilise une autre slugification — fallback : utiliser une syntaxe
   d'ancre explicite Markdown `{ #ancre-personnalisee }`).
3. **Lecture comparée** : ouvrir `effacement.md` rendu, vérifier que
   les deux renvois (intro + encadré ligne 46) cliquent bien sur la
   sous-section enrichie. Ouvrir `acteurs-secondaires.md` rendu,
   vérifier que le lien vers effacement.md atterrit sur la
   sous-section.
4. **Grep de contrôle** :

   ```bash
   grep -c "parquet\|procureur du Roi" docs/faillis/effacement.md
   ```

   Résultat attendu : ≥ 4 (avant : 1).
5. **Build** : pas de régression sur les autres pages (vérifier que la
   suite de tests pytest des dates `inject_git_dates.py` reste 13/13).

## Gestion des erreurs / risques

- **R1 — Ancres Markdown différentes en sortie Zensical.** Si Zensical
  slugifie autrement (par exemple en gardant les accents codés en
  pourcent-encoding), les liens internes peuvent casser silencieusement.
  Mitigation : vérifier au build (test #2 ci-dessus). Si KO, ajouter
  une ancre explicite : `### La requête en refus d'effacement { #la-requete-en-refus-deffacement }`
  selon la syntaxe MkDocs-Material que Zensical hérite.
- **R2 — Effet de répétition entre l'intro et l'encadré ligne 46.**
  Le lecteur croise deux fois la même information. Mitigation
  acceptée : intentionnel (vue côté spec — il faut prévenir tôt).
- **R3 — Le paragraphe court d'`acteurs-secondaires.md` peut donner
  l'impression que le procureur du Roi est forcément hostile.**
  Mitigation : tournure neutre (« peut également déposer »), pas
  d'adjectif évaluatif.

## Hors scope

- Création de `docs/faillis/refus-effacement.md` (rejetée).
- Réorganisation structurelle de [effacement.md](../../faillis/effacement.md)
  (sections, titres) — passe chirurgicale uniquement.
- Mise à jour de [docs/comprendre/cloture.md](../../comprendre/cloture.md)
  (mention secondaire déjà cohérente).
- Mise à jour de [docs/faillis/obligations.md](../../faillis/obligations.md)
  (mention ligne 69 reste cohérente).
