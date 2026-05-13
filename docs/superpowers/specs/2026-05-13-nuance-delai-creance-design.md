---
title: Nuancer le délai de 30 jours pour les déclarations de créance
date: 2026-05-13
status: draft
---

# Spec — Nuancer le délai de 30 jours pour les déclarations de créance

## Contexte

Le site infofaillite.be présente, à plusieurs endroits, le délai de 30
jours pour la déclaration de créance comme une **échéance stricte** :
« passé un an, votre créance est définitivement perdue ». Cette
formulation est juridiquement incorrecte. En pratique :

- Les 30 jours fixent la fenêtre pour participer aux **répartitions
  provisoires** (qui sont rares — moins de 15 % des dossiers).
- Une déclaration arrivée **après** les 30 jours reste recevable tant que
  le **troisième procès-verbal de vérification** (PV définitif, déposé
  environ douze mois après le jugement) n'a pas été déposé. Le curateur
  l'inclura dans le 2ᵉ ou le 3ᵉ PV.
- Forclusion réelle = **dépôt du 3ᵉ PV**, pas « 1 an calendaire ».

La cartographie du site révèle une **incohérence verticale** : les pages
d'entrée (homepage, intro créancier) sont strictes ; les pages profondes
(`delais.md`, `creanciers/faq.md`, `creanciers/declarer-creance.md`,
`comprendre/deroulement-phase-1-3.md`) sont déjà nuancées mais avec la
mauvaise borne (« 1 an » au lieu de « 3ᵉ PV »).

## Objectif

Aligner toutes les mentions du délai de 30 jours sur une **formulation
type unique** :

> « Le délai de trente jours fixe la fenêtre pour participer aux
> éventuelles répartitions provisoires. Une déclaration tardive reste
> recevable tant que le curateur n'a pas déposé le **troisième
> procès-verbal de vérification** (en pratique environ douze mois après
> le jugement). Au-delà, la créance est forclose. »

Avec deux principes éditoriaux :

1. **Garder l'urgence** sur les 30 jours en intro (« visez les 30 jours,
   c'est votre meilleure protection »).
2. **Nommer le 3ᵉ PV** comme verrou pratique partout où on parlait de
   « 1 an » comme couperet absolu.

## Non-objectifs

- Pas de refonte des autres délais (recours, contestation, etc.) : ils
  *sont* stricts, on les laisse tels quels.
- Pas de modification de la déchéance des cautions (3 mois) : c'est une
  vraie déchéance.
- Pas de changement structurel des pages (ordre, sections) : passes
  chirurgicales sur les passages concernés.

## Formulation type — variantes selon le contexte

Selon que la page s'adresse au grand public ou au créancier averti :

**Variante longue (intro de page, admonition `danger`)** :

> Le délai de trente jours court dès la publication du jugement de
> faillite au Moniteur belge — et non à partir du moment où vous en
> prenez connaissance. Une déclaration tardive reste recevable tant que
> le curateur n'a pas déposé le troisième procès-verbal de vérification
> (environ douze mois après le jugement), mais vous perdez le droit aux
> éventuelles répartitions provisoires. Au-delà du troisième
> procès-verbal, la créance est forclose.

**Variante courte (en cours de paragraphe)** :

> Une déclaration tardive reste recevable jusqu'au dépôt du troisième
> procès-verbal de vérification (environ douze mois après le jugement),
> au prix de l'exclusion des répartitions provisoires.

**Variante glossaire / référence (sec, juridique)** :

> Forclusion pour les déclarations de créance : dépôt du 3ᵉ
> procès-verbal de vérification.

## Composants — changements par fichier

### Composant 1 — `docs/README.md` (admonition lignes 29–32)

Actuel :

> Le délai de trente jours court dès la publication du jugement de
> faillite au Moniteur belge — et non à partir du moment où vous en
> prenez connaissance. Passé un an, votre créance est définitivement
> perdue.

Cible : **variante longue** (voir ci-dessus).

### Composant 2 — `docs/creanciers/README.md` (bloc « Priorité absolue » lignes 11–13)

Actuel : « Priorité absolue : déclarez votre créance dans les 30 jours.
[…] Passé ce délai, vous ne participez plus aux répartitions
provisoires. Passé un an, votre droit est définitivement éteint. »

Cible : conserver le titre « Priorité absolue » (l'urgence est légitime
opérationnellement), conserver la première phrase ; remplacer la
deuxième mention « passé un an » par la **variante longue**.

### Composant 3 — `docs/delais.md`

Deux passages.

**Lignes 12–13 (intro générale)** : la phrase « Les délais en droit de
la faillite sont des délais de forclusion : […] Il n'existe pas de
prolongation, pas de régularisation, pas de bonne volonté qui compense
un retard. » est trop absolue. Cible : la garder mais ajouter une note
« Une exception notable : le délai de déclaration de créance, qui
dispose d'une tolérance pratique jusqu'au dépôt du 3ᵉ procès-verbal de
vérification. Voir le tableau ci-dessous. » avec un lien interne.

**Ligne 33 (passage spécifique au délai de déclaration)** : déjà
nuancé mais utilise « 1 an ». Cible : remplacer
« Une déclaration tardive reste possible jusqu'à un an après le
jugement » par « Une déclaration tardive reste recevable jusqu'au
dépôt du **troisième procès-verbal de vérification** (environ douze
mois après le jugement, voir [verification-contestation.md])
[creanciers/verification-contestation.md] ». Et la phrase « Au-delà
d'un an, la créance est définitivement perdue. » devient « Au-delà
du 3ᵉ procès-verbal, la créance est forclose. »

**Tableau des PV (lignes ~104–110)** : déjà correct. Ajouter une
colonne ou une note finale : « Le 3ᵉ PV est aussi la **date limite
pratique** pour qu'une déclaration de créance tardive soit examinée. »

### Composant 4 — `docs/creanciers/declarer-creance.md`

Deux passages.

**Lignes 20–21 (intro section délai)** : déjà nuancé. Aligner sur la
formulation type ; remplacer « jusqu'à un an » par
« jusqu'au dépôt du 3ᵉ procès-verbal de vérification (environ douze
mois après le jugement) ».

**Ligne 102 (FAQ-style « J'ai dépassé le délai ») :** déjà bien
formulé. Aligner sur le 3ᵉ PV. Garder le ton rassurant
(« Pas nécessairement. »).

### Composant 5 — `docs/creanciers/faq.md`

**Question « Puis-je encore déclarer après 30 jours ? » (ligne 16)** :
déjà nuancé. Aligner sur la nouvelle formulation : « jusqu'au dépôt
du 3ᵉ procès-verbal de vérification (environ douze mois après le
jugement) », et reformuler la phrase « Passé ce délai d'un an, c'est
la forclusion absolue » en « Une fois le 3ᵉ procès-verbal déposé,
c'est la forclusion. »

### Composant 6 — `docs/comprendre/deroulement-phase-1-3.md` (lignes 76–77)

Déjà nuancé. Une seule modification mineure : remplacer
« jusqu'à un an après le jugement » par « jusqu'au dépôt du 3ᵉ
procès-verbal de vérification (environ douze mois après le jugement) ».

### Composant 7 — `docs/creanciers/verification-contestation.md` (sections 2ᵉ et 3ᵉ PV)

**2ᵉ PV (ligne 26)** : enrichir « créances déclarées tardivement —
entre la clôture du premier et la clôture du deuxième procès-verbal »
en « créances déclarées tardivement entre la clôture du premier et la
clôture du deuxième procès-verbal (les déclarations parvenues entre le
2ᵉ et le 3ᵉ PV sont examinées au 3ᵉ) ».

**3ᵉ PV (ligne 30)** : ajouter une phrase finale :
« C'est aussi la **date limite pratique pour qu'une déclaration de
créance tardive soit recevable** : une déclaration parvenue au curateur
après le dépôt du 3ᵉ procès-verbal n'est plus traitée. »

### Composant 8 — `docs/glossaire.md` (entrée « Forclusion », ligne 88)

Actuel : « Perte définitive et irréversible d'un droit en raison du
dépassement d'un délai légal impératif. La forclusion ne peut pas être
régularisée après coup. »

Cible : garder la définition générique ; ajouter une seconde phrase :
« Pour la déclaration de créance dans une faillite, la forclusion
intervient au dépôt du 3ᵉ procès-verbal de vérification (voir
[la vérification des créances][creanciers/verification-contestation.md]). »

### Composant 9 — `log.md`

Une entrée datée 2026-05-13, type `edit`, qui synthétise la passe.

## Plan de test (manuel)

1. **Grep de contrôle** après modifications :
   - `grep -ri "passé un an\|passe un an\|jusqu'à un an" docs/` → doit
     ne plus rien ressortir dans le contexte des créances (mais peut
     ressortir pour d'autres délais).
   - `grep -ri "définitivement perdue\|définitivement éteint" docs/` →
     idem.
   - `grep -ri "3e procès-verbal\|3ᵉ procès-verbal\|troisième
     procès-verbal" docs/` → ressortir partout où on a injecté la
     nuance.
2. **Cohérence des liens internes** : chaque mention du 3ᵉ PV doit
   pouvoir être suivie d'un lien vers `verification-contestation.md`
   (au moins une fois par page).
3. **Lecture comparée** : ouvrir `README.md` puis suivre le chemin
   « Vous êtes créancier » jusqu'à `declarer-creance.md` et `faq.md`.
   Vérifier qu'il n'y a pas de contradiction entre les niveaux.
4. **Build Zensical** : `zensical build` doit passer sans erreur (pas
   de lien cassé après réécriture).

## Gestion des erreurs / risques

- **R1 — Affaiblir trop l'urgence des 30 jours.** Un lecteur qui lit
  trop vite peut se dire « ah, j'ai un an de tolérance, pas besoin de
  me presser ». Mitigation : conserver le format `admonition danger`
  partout où il existait, et garder la première phrase de chaque bloc
  centrée sur « visez les 30 jours ». La nuance vient après, jamais
  avant.
- **R2 — Glissement de date du 3ᵉ PV.** En théorie, le 3ᵉ PV est fixé
  par ordonnance du juge-commissaire ; il peut être plus tôt ou plus
  tard que 12 mois. Mitigation : formulation systématique
  « environ douze mois après le jugement » plutôt que « 12 mois ».
- **R3 — Désynchronisation lors d'évolutions futures.** Si plus tard
  on doit ré-éditer un de ces passages, on risque de re-introduire
  une formulation stricte. Mitigation : pas de mécanisme automatique
  ici, mais la formulation type est consignée dans ce spec ; on peut
  y revenir.
- **R4 — Cohérence avec `droits-specifiques.md` ligne 102.** Cette
  phrase générique « délais stricts sans exception » reste en place
  (décision assumée : elle vaut pour les autres délais). Risque que
  des lecteurs y voient une contradiction. Mitigation : si le retour
  utilisateur va dans ce sens, on nuancera cette phrase aussi dans
  une passe ultérieure.

## Hors scope

- JSON-LD `dateModified` (autre follow-up déjà identifié).
- Réécriture stylistique des autres passages des mêmes pages.
- Ajout d'un encadré « 3ᵉ PV » réutilisable type partial Jinja
  (overkill pour ~8 passages).
