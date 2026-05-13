---
updated: '2026-05-13'
---

# Nuancer le délai de 30 jours pour les déclarations de créance — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Aligner toutes les mentions du délai de 30 jours pour la déclaration de créance sur une formulation type unique qui nomme explicitement le **3ᵉ procès-verbal de vérification** comme verrou pratique de forclusion, au lieu de l'imprécis « passé un an ».

**Architecture:** Une passe éditoriale chirurgicale sur 8 fichiers Markdown sous `docs/`. Pas de code, pas de tests automatisés. Un grep de contrôle final + un build Zensical de vérification. Un commit par fichier modifié pour traçabilité, plus un commit final pour `log.md`.

**Tech Stack:** Markdown, Zensical (pour le build de contrôle), `grep` (pour la vérification de cohérence).

**Spec :** [docs/superpowers/specs/2026-05-13-nuance-delai-creance-design.md](../specs/2026-05-13-nuance-delai-creance-design.md)

**Formulation type de référence** (à réutiliser, en variantes longue/courte selon le contexte) :

> Une déclaration tardive reste recevable tant que le curateur n'a pas déposé le **troisième procès-verbal de vérification** (en pratique environ douze mois après le jugement), mais vous perdez le droit aux éventuelles répartitions provisoires. Au-delà du troisième procès-verbal, la créance est forclose.

---

## File structure

À modifier (chronologie d'édition) :

1. `docs/README.md` — admonition homepage
2. `docs/creanciers/README.md` — admonition intro créancier
3. `docs/delais.md` — intro générique + section déclaration + tableaux
4. `docs/creanciers/declarer-creance.md` — admonition + FAQ inline
5. `docs/creanciers/faq.md` — Q/R délai
6. `docs/comprendre/deroulement-phase-1-3.md` — admonition phase 1-3
7. `docs/creanciers/verification-contestation.md` — sections 2ᵉ et 3ᵉ PV
8. `docs/glossaire.md` — entrée Forclusion
9. `log.md` — entrée du jour

Tous les fichiers existent déjà. Aucun nouveau fichier à créer.

---

### Task 1 : `docs/README.md` — admonition homepage

**Files:**
- Modify: `docs/README.md` (lignes 32–33)

- [ ] **Step 1 : Édition**

Utiliser l'outil Edit avec :

`old_string` :
```
!!! danger "Délai de 30 jours pour déclarer votre créance"
    Le délai de trente jours court dès la publication du jugement de faillite au Moniteur belge — et non à partir du moment où vous en prenez connaissance. Passé un an, votre créance est définitivement perdue.
```

`new_string` :
```
!!! danger "Délai de 30 jours pour déclarer votre créance"
    Le délai de trente jours court dès la publication du jugement de faillite au Moniteur belge — et non à partir du moment où vous en prenez connaissance. Une déclaration tardive reste recevable tant que le curateur n'a pas déposé le troisième procès-verbal de vérification (en pratique environ douze mois après le jugement), mais vous perdez le droit aux éventuelles répartitions provisoires. Au-delà, la créance est forclose.
```

- [ ] **Step 2 : Commit**

```bash
git add docs/README.md
git commit -m "Nuance délai créance — README"
```

Message de commit exact : `Nuance délai créance — README`

---

### Task 2 : `docs/creanciers/README.md` — admonition intro créancier

**Files:**
- Modify: `docs/creanciers/README.md` (lignes 12–13)

- [ ] **Step 1 : Édition**

`old_string` :
```
!!! danger "Priorité absolue : déclarez votre créance dans les 30 jours"
    Vous avez trente jours à compter de la publication du jugement au Moniteur belge pour déclarer votre créance auprès du curateur. Passé ce délai, vous ne participez plus aux répartitions provisoires. Passé un an, votre droit est définitivement éteint. Commencez par [déclarer votre créance dans les trente jours](declarer-creance.md).
```

`new_string` :
```
!!! danger "Priorité absolue : déclarez votre créance dans les 30 jours"
    Vous avez trente jours à compter de la publication du jugement au Moniteur belge pour déclarer votre créance auprès du curateur. Passé ce délai, vous ne participez plus aux répartitions provisoires. Une déclaration tardive reste cependant recevable tant que le curateur n'a pas déposé le troisième procès-verbal de vérification (en pratique environ douze mois après le jugement) ; au-delà, votre droit est forclos. Commencez par [déclarer votre créance dans les trente jours](declarer-creance.md).
```

- [ ] **Step 2 : Commit**

```bash
git add docs/creanciers/README.md
git commit -m "Nuance délai créance — intro créancier"
```

Message exact : `Nuance délai créance — intro créancier`

---

### Task 3 : `docs/delais.md` — trois passages

Trois éditions dans le même fichier, regroupées en un seul commit.

**Files:**
- Modify: `docs/delais.md` (lignes 12–13, 21, 33, 39–40, 108–112)

- [ ] **Step 1 : Édition 1 — admonition d'intro (lignes 12–13)**

`old_string` :
```
!!! danger "Des délais de forclusion sans tolérance"
    Les délais en droit de la faillite sont des délais de forclusion : une fois écoulés, le droit correspondant est perdu définitivement. Il n'existe pas de prolongation, pas de régularisation, pas de bonne volonté qui compense un retard. Notez chaque délai dans votre agenda dès que vous en avez connaissance, avec une alarme plusieurs jours avant l'échéance.
```

`new_string` :
```
!!! danger "Des délais de forclusion sans tolérance"
    Les délais en droit de la faillite sont des délais de forclusion : une fois écoulés, le droit correspondant est perdu définitivement. Il n'existe pas de prolongation, pas de régularisation, pas de bonne volonté qui compense un retard. Notez chaque délai dans votre agenda dès que vous en avez connaissance, avec une alarme plusieurs jours avant l'échéance.

    Une exception notable concerne la **déclaration de créance** : passé le délai de trente jours, une déclaration tardive reste recevable jusqu'au dépôt du troisième procès-verbal de vérification (environ douze mois après le jugement). Voir le détail dans la section [Déclaration de créance](#déclaration-de-créance) plus bas.
```

- [ ] **Step 2 : Édition 2 — tableau des cinq délais critiques (ligne 21)**

`old_string` :
```
| **30 jours** | Déclarer sa créance | Créanciers | Exclusion des répartitions provisoires ; forclusion totale après 1 an |
```

`new_string` :
```
| **30 jours** | Déclarer sa créance | Créanciers | Exclusion des répartitions provisoires ; forclusion au dépôt du 3ᵉ PV (≈ 12 mois) |
```

- [ ] **Step 3 : Édition 3 — section Déclaration de créance (ligne 33)**

`old_string` :
```
Le délai de trente jours court à compter de la publication du jugement déclaratif au Moniteur belge — et non à compter du moment où vous en prenez connaissance. Une déclaration tardive reste possible jusqu'à un an après le jugement, mais exclut la participation aux éventuelles répartitions provisoires. Au-delà d'un an, la créance est définitivement perdue.
```

`new_string` :
```
Le délai de trente jours court à compter de la publication du jugement déclaratif au Moniteur belge — et non à compter du moment où vous en prenez connaissance. Une déclaration tardive reste recevable jusqu'au dépôt du **troisième procès-verbal de vérification** (environ douze mois après le jugement, voir [la vérification des créances et les procès-verbaux](creanciers/verification-contestation.md)) ; elle est alors examinée au 2ᵉ ou au 3ᵉ procès-verbal. Vous perdez en revanche le droit aux éventuelles répartitions provisoires. Au-delà du 3ᵉ procès-verbal, la créance est forclose.
```

- [ ] **Step 4 : Édition 4 — tableau des délais créanciers (lignes 39–40)**

`old_string` :
```
| 30 jours | Jugement de faillite | Déclarer la créance | Exclusion des répartitions provisoires |
| 1 an | Jugement de faillite | Délai absolu de déclaration | Forclusion totale |
```

`new_string` :
```
| 30 jours | Jugement de faillite | Déclarer la créance | Exclusion des répartitions provisoires |
| Dépôt du 3ᵉ PV (≈ 12 mois) | Jugement de faillite | Délai pratique de déclaration | Forclusion |
```

- [ ] **Step 5 : Édition 5 — tableau des trois PV (lignes 108–112)**

`old_string` :
```
| PV | Délai depuis le jugement | Caractère |
|---|---|---|
| 1er PV | J+35 à J+60 (après expiration du délai de 30 jours) | Provisoire |
| 2e PV | 6 mois | Provisoire |
| 3e PV | 12 mois | Définitif |

Pour comprendre le déroulement des procès-verbaux, consultez [la vérification des créances et les procès-verbaux](creanciers/verification-contestation.md).
```

`new_string` :
```
| PV | Délai depuis le jugement | Caractère |
|---|---|---|
| 1er PV | J+35 à J+60 (après expiration du délai de 30 jours) | Provisoire |
| 2e PV | 6 mois | Provisoire |
| 3e PV | 12 mois | Définitif — c'est aussi la date limite pratique pour qu'une déclaration de créance tardive soit examinée |

Pour comprendre le déroulement des procès-verbaux, consultez [la vérification des créances et les procès-verbaux](creanciers/verification-contestation.md).
```

- [ ] **Step 6 : Commit**

```bash
git add docs/delais.md
git commit -m "Nuance délai créance — délais (intro, tableaux, section dédiée)"
```

Message exact : `Nuance délai créance — délais (intro, tableaux, section dédiée)`

---

### Task 4 : `docs/creanciers/declarer-creance.md` — admonition + FAQ inline

**Files:**
- Modify: `docs/creanciers/declarer-creance.md` (lignes 20–21, 102)

- [ ] **Step 1 : Édition 1 — admonition (lignes 20–21)**

`old_string` :
```
!!! danger "Ne manquez pas le délai de trente jours"
    Une déclaration effectuée après le trentième jour peut encore être acceptée, mais vous serez exclu de toutes les répartitions provisoires. Passé un an depuis le jugement, toute déclaration est définitivement irrecevable. La date limite est indiquée clairement dans l'onglet "Délais" de votre dossier sur REGSOL.
```

`new_string` :
```
!!! danger "Ne manquez pas le délai de trente jours"
    Une déclaration effectuée après le trentième jour peut encore être acceptée, mais vous serez exclu de toutes les répartitions provisoires. La déclaration tardive reste recevable jusqu'au dépôt du troisième procès-verbal de vérification (environ douze mois après le jugement) ; au-delà, elle est irrecevable. La date limite des trente jours est indiquée clairement dans l'onglet "Délais" de votre dossier sur REGSOL.
```

- [ ] **Step 2 : Édition 2 — FAQ inline (ligne 102)**

`old_string` :
```
**J'ai dépassé le délai de trente jours. Est-il trop tard ?** Pas nécessairement. Une déclaration tardive reste recevable jusqu'à l'assemblée générale des créanciers (généralement un an ou plus après le jugement), mais vous ne participerez pas aux répartitions provisoires éventuelles. Au-delà d'un an, la forclusion est totale.
```

`new_string` :
```
**J'ai dépassé le délai de trente jours. Est-il trop tard ?** Pas nécessairement. Une déclaration tardive reste recevable jusqu'au dépôt du troisième procès-verbal de vérification (environ douze mois après le jugement), mais vous ne participerez pas aux répartitions provisoires éventuelles. Une fois le 3ᵉ procès-verbal déposé, la forclusion est acquise. Voir [la vérification des créances et les procès-verbaux](verification-contestation.md) pour le détail.
```

- [ ] **Step 3 : Commit**

```bash
git add docs/creanciers/declarer-creance.md
git commit -m "Nuance délai créance — declarer-creance"
```

Message exact : `Nuance délai créance — declarer-creance`

---

### Task 5 : `docs/creanciers/faq.md` — Q/R sur le délai

**Files:**
- Modify: `docs/creanciers/faq.md` (ligne 16)

- [ ] **Step 1 : Édition**

`old_string` :
```
Oui, vous pouvez encore déclarer votre créance après l'expiration du délai de 30 jours. La loi vous autorise à le faire jusqu'à un an après le jugement de faillite, mais cette déclaration tardive a une conséquence concrète : vous ne participez pas aux éventuelles répartitions provisoires déjà effectuées avant votre déclaration. Passé ce délai d'un an, c'est la forclusion absolue — votre créance est définitivement perdue.
```

`new_string` :
```
Oui, vous pouvez encore déclarer votre créance après l'expiration du délai de 30 jours. Une déclaration tardive reste recevable jusqu'au dépôt du **troisième procès-verbal de vérification** par le curateur (en pratique environ douze mois après le jugement). Elle a cependant une conséquence concrète : vous ne participez pas aux éventuelles répartitions provisoires déjà effectuées avant votre déclaration. Une fois le 3ᵉ procès-verbal déposé, c'est la forclusion — votre créance est définitivement perdue. Voir [la vérification des créances et les procès-verbaux](verification-contestation.md) pour le déroulement complet.
```

- [ ] **Step 2 : Commit**

```bash
git add docs/creanciers/faq.md
git commit -m "Nuance délai créance — FAQ créancier"
```

Message exact : `Nuance délai créance — FAQ créancier`

---

### Task 6 : `docs/comprendre/deroulement-phase-1-3.md` — admonition phase 1-3

**Files:**
- Modify: `docs/comprendre/deroulement-phase-1-3.md` (lignes 76–77)

- [ ] **Step 1 : Édition**

`old_string` :
```
!!! danger "Le délai de trente jours est impératif pour les créanciers"
    Une créance non déclarée dans les trente jours ne peut pas bénéficier des répartitions provisoires. Les déclarations tardives restent acceptées jusqu'à un an après le jugement, mais vous perdez le droit aux dividendes intermédiaires. La déclaration via REGSOL est le moyen le plus rapide et le plus sûr.
```

`new_string` :
```
!!! danger "Le délai de trente jours est impératif pour les créanciers"
    Une créance non déclarée dans les trente jours ne peut pas bénéficier des répartitions provisoires. Les déclarations tardives restent acceptées jusqu'au dépôt du troisième procès-verbal de vérification (en pratique environ douze mois après le jugement), mais vous perdez le droit aux dividendes intermédiaires. La déclaration via REGSOL est le moyen le plus rapide et le plus sûr.
```

- [ ] **Step 2 : Commit**

```bash
git add docs/comprendre/deroulement-phase-1-3.md
git commit -m "Nuance délai créance — déroulement phase 1-3"
```

Message exact : `Nuance délai créance — déroulement phase 1-3`

---

### Task 7 : `docs/creanciers/verification-contestation.md` — sections 2ᵉ et 3ᵉ PV

Deux éditions dans le même fichier, un seul commit.

**Files:**
- Modify: `docs/creanciers/verification-contestation.md` (lignes 26, 30)

- [ ] **Step 1 : Édition 1 — 2ᵉ PV (ligne 26)**

`old_string` :
```
Le deuxième procès-verbal intervient environ six mois après le jugement. Il porte principalement sur les créances déclarées tardivement — entre la clôture du premier et la clôture du deuxième procès-verbal — ainsi que sur les créances laissées en réserve lors du premier. Les décisions restent provisoires.
```

`new_string` :
```
Le deuxième procès-verbal intervient environ six mois après le jugement. Il porte principalement sur les créances déclarées tardivement — entre la clôture du premier et la clôture du deuxième procès-verbal — ainsi que sur les créances laissées en réserve lors du premier. Les déclarations parvenues au curateur entre le 2ᵉ et le 3ᵉ procès-verbal sont, elles, examinées lors du 3ᵉ. Les décisions restent provisoires.
```

- [ ] **Step 2 : Édition 2 — 3ᵉ PV (ligne 30)**

`old_string` :
```
Le troisième procès-verbal intervient environ douze mois après le jugement. Il a un caractère définitif : les réserves doivent être levées, sauf si un litige judiciaire est encore pendant ou si une créance conditionnelle n'est pas encore réalisée. Après ce procès-verbal, les créances admises ne peuvent plus être contestées sauf en cas de fraude avérée ou d'erreur matérielle manifeste.
```

`new_string` :
```
Le troisième procès-verbal intervient environ douze mois après le jugement. Il a un caractère définitif : les réserves doivent être levées, sauf si un litige judiciaire est encore pendant ou si une créance conditionnelle n'est pas encore réalisée. Après ce procès-verbal, les créances admises ne peuvent plus être contestées sauf en cas de fraude avérée ou d'erreur matérielle manifeste.

Le dépôt du 3ᵉ procès-verbal est aussi la **date limite pratique pour qu'une déclaration de créance tardive soit recevable** : une déclaration parvenue au curateur après ce dépôt n'est plus traitée, même si elle arrive avant le délai légal d'un an.
```

- [ ] **Step 3 : Commit**

```bash
git add docs/creanciers/verification-contestation.md
git commit -m "Nuance délai créance — verification (2e/3e PV)"
```

Message exact : `Nuance délai créance — verification (2e/3e PV)`

---

### Task 8 : `docs/glossaire.md` — entrée Forclusion

**Files:**
- Modify: `docs/glossaire.md` (ligne 88)

- [ ] **Step 1 : Édition**

`old_string` :
```
**Forclusion** — Perte définitive et irréversible d'un droit en raison du dépassement d'un délai légal impératif. La forclusion ne peut pas être régularisée après coup.
```

`new_string` :
```
**Forclusion** — Perte définitive et irréversible d'un droit en raison du dépassement d'un délai légal impératif. La forclusion ne peut pas être régularisée après coup. Pour la déclaration de créance dans une faillite, la forclusion intervient au dépôt du 3ᵉ procès-verbal de vérification (voir [la vérification des créances et les procès-verbaux](creanciers/verification-contestation.md)).
```

- [ ] **Step 2 : Commit**

```bash
git add docs/glossaire.md
git commit -m "Nuance délai créance — glossaire (Forclusion)"
```

Message exact : `Nuance délai créance — glossaire (Forclusion)`

---

### Task 9 : Grep de contrôle

Vérifier qu'on n'a oublié aucune mention strict-mode et que les nouvelles formulations sont cohérentes.

**Files:** aucun à modifier (lecture seule).

- [ ] **Step 1 : Vérifier qu'il ne reste plus de « passé un an » ou « jusqu'à un an » dans le contexte des créances**

Commande :
```bash
grep -rni "passé un an\|jusqu'à un an\|au-delà d'un an\|passé ce délai d'un an" docs/ --include="*.md"
```

Résultat attendu :
- Aucune correspondance, OU
- Uniquement des correspondances qui ne concernent PAS la déclaration de créance (par exemple un autre délai juridique).

Si des matches restent dans un contexte de déclaration de créance → revenir à la task correspondante.

- [ ] **Step 2 : Vérifier que « 3ᵉ procès-verbal » ou « troisième procès-verbal » apparaît bien dans les bonnes pages**

```bash
grep -rni "troisième procès-verbal\|3ᵉ procès-verbal\|3e procès-verbal" docs/ --include="*.md"
```

Résultat attendu : au moins une mention dans chacun des fichiers modifiés (README.md, creanciers/README.md, delais.md, creanciers/declarer-creance.md, creanciers/faq.md, comprendre/deroulement-phase-1-3.md, creanciers/verification-contestation.md, glossaire.md).

- [ ] **Step 3 : Vérifier qu'il ne reste pas de « définitivement perdue » ou « définitivement éteint » dans le contexte créancier**

```bash
grep -rni "définitivement perdue\|définitivement perdu\|définitivement éteint\|définitivement irrecevable" docs/ --include="*.md"
```

Résultat attendu : pas de correspondance dans `docs/README.md`, `docs/creanciers/README.md`, `docs/delais.md` (intro et section déclaration), `docs/creanciers/declarer-creance.md`, `docs/creanciers/faq.md`, `docs/comprendre/deroulement-phase-1-3.md`. Une correspondance peut subsister dans `docs/glossaire.md` (définition générique de la forclusion : « Perte définitive et irréversible » — c'est OK, c'est la définition juridique) ou dans `docs/delais.md` ligne 13 (l'admonition d'intro générale reste avec « perdu définitivement » sur le ton générique des délais, ce qui est conservé : la nuance créance est ajoutée APRÈS, pas en remplacement).

Si une correspondance subsiste dans le contexte créance et qu'elle n'était pas listée comme conservée → revenir à la task correspondante.

- [ ] **Step 4 : Pas de commit pour cette task** (uniquement de la vérification).

---

### Task 10 : Build Zensical de vérification

**Files:** aucun à modifier.

- [ ] **Step 1 : Build**

```bash
.venv/Scripts/zensical build
```

Résultat attendu : `Build finished in <N>s` sans erreur Jinja, sans erreur de lien interne.

Si une erreur de lien interne apparaît (lien vers `verification-contestation.md` depuis un dossier qui n'avait pas ce lien avant), corriger en utilisant un chemin relatif correct.

- [ ] **Step 2 : Sanity check du sitemap et d'une page rendue**

```bash
.venv/Scripts/python -c "
import re
for path in ['site/index.html', 'site/creanciers/index.html', 'site/delais/index.html', 'site/glossaire/index.html']:
    html = open(path, encoding='utf-8').read()
    has_3e_pv = 'troisi' in html.lower() and 'proc' in html.lower()
    print(path, '-> 3e PV mentioned:', has_3e_pv)
"
```

Résultat attendu : `3e PV mentioned: True` pour les pages où on a injecté la nuance.

- [ ] **Step 3 : Pas de commit** (vérification uniquement).

---

### Task 11 : `scripts/inject_git_dates.py` + `log.md`

**Files:**
- Modify: tous les `.md` modifiés (front matter `updated:` rafraîchi automatiquement)
- Modify: `log.md`

- [ ] **Step 1 : Rafraîchir les dates updated dans le front matter**

Comme on vient de modifier 8 fichiers `.md`, leur front matter `updated:` est devenu obsolète vis-à-vis du dernier commit (qui est ceux des Tasks 1–8). Lancer :

```bash
.venv/Scripts/python scripts/inject_git_dates.py
```

Résultat attendu : `N fichier(s) mis à jour, M inchangé(s).` avec N ≥ 8 (les 8 fichiers édités).

- [ ] **Step 2 : Ajouter une entrée dans `log.md`**

Utiliser Edit, juste après le séparateur `---` (ligne 7) et avant la première entrée existante.

`old_string` :
```
---

## [2026-05-13] edit | Format date français au pied de page
```

`new_string` :
```
---

## [2026-05-13] edit | Nuancer le délai de 30 jours (déclarations de créance)

Aligné toutes les mentions du délai de 30 jours pour la déclaration de créance sur une formulation type qui nomme explicitement le **3ᵉ procès-verbal de vérification** comme verrou de forclusion (≈ 12 mois après le jugement), au lieu de l'imprécis « passé un an ». Touche 8 fichiers : [docs/README.md](docs/README.md), [docs/creanciers/README.md](docs/creanciers/README.md), [docs/delais.md](docs/delais.md), [docs/creanciers/declarer-creance.md](docs/creanciers/declarer-creance.md), [docs/creanciers/faq.md](docs/creanciers/faq.md), [docs/comprendre/deroulement-phase-1-3.md](docs/comprendre/deroulement-phase-1-3.md), [docs/creanciers/verification-contestation.md](docs/creanciers/verification-contestation.md), [docs/glossaire.md](docs/glossaire.md). Spec et plan dans [docs/superpowers/](docs/superpowers/).

## [2026-05-13] edit | Format date français au pied de page
```

- [ ] **Step 3 : Commit groupé**

```bash
git add docs/ log.md
git commit -m "log + rafraîchissement updated : nuance délai créance"
```

Message exact : `log + rafraîchissement updated : nuance délai créance`

- [ ] **Step 4 : Vérification finale**

```bash
.venv/Scripts/python scripts/inject_git_dates.py --check
```

Résultat attendu : exit 1, avec une liste de fichiers « À mettre à jour » qui correspondent aux fichiers modifiés dans le dernier commit. C'est l'artefact de bootstrap déjà documenté pour la fonctionnalité lastmod — pas d'action requise. Note-le simplement dans le rapport.

```bash
.venv/Scripts/pytest tests/ -q
```

Résultat attendu : `13 passed`. Aucune régression dans les tests du script `inject_git_dates`.
