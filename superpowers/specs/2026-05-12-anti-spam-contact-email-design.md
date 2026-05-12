# Protection anti-spam de l'adresse contact

**Date** : 2026-05-12
**Statut** : spec validé, prêt pour plan d'implémentation
**Périmètre** : [docs/contact.md](../../docs/contact.md) uniquement

---

## Context

Le pilote de CTA léger ajouté sur [docs/faillis/checklist-premiere-semaine.md](../../docs/faillis/checklist-premiere-semaine.md) renvoie vers [docs/contact.md](../../docs/contact.md), qui contient aujourd'hui l'adresse `florian@avroy.be` en clair dans un lien `mailto:`. La généralisation prévue (CTA sur ~20 pages éditoriales) va décupler la visibilité de cette page contact et, par ricochet, l'exposition de l'adresse aux moissonneurs.

Deux contraintes ont été énoncées :

1. **Anti-spam d'abord** : l'adresse ne doit jamais apparaître en clair dans le HTML servi (priorité confirmée par l'utilisateur).
2. **Changement futur facile** : pouvoir basculer l'adresse (ex. `infofaillite@avroy.be`) en éditant un seul fichier.

Étant donné que (a) tous les CTA pointent vers une seule page intermédiaire `/contact`, la centralisation est déjà acquise par la structure — aucune variable ni partial n'est nécessaire. Le travail se réduit donc à protéger l'unique occurrence de l'adresse sur `contact.md`.

Résultat attendu : un scraper HTML statique ne trouve aucune chaîne ressemblant à une adresse e-mail valide sur le site ; un visiteur humain avec JS voit un lien cliquable normal ; sans JS, il voit une indication lisible mais non-scrapable.

---

## Architecture

Tout le mécanisme vit dans [docs/contact.md](../../docs/contact.md) sous forme d'un bloc HTML inline. Trois composants :

### 1. Marqueur HTML inerte

Un `<span id="contact-email">` portant deux `data-*` attributs avec les morceaux de l'adresse encodés en **base64**, séparément pour le local-part et le domaine :

```html
<span id="contact-email" data-u="Zmxvcmlhbg==" data-d="YXZyb3kuYmU="></span>
```

Aucune chaîne ressemblant à `florian`, `avroy`, ou à une adresse complète n'apparaît dans le HTML servi. Le scraper qui lit le HTML statique voit deux blobs base64 indépendants — il faudrait spécifiquement décoder les deux *et* les concaténer avec `@` pour reconstruire l'adresse.

### 2. Fallback `<noscript>` lisible humainement

Phrase en clair pour visiteurs sans JS, sans `mailto:`, sans `@` ni `.` littéraux à proximité immédiate des morceaux d'adresse :

```html
<noscript>Écrivez à <strong>florian</strong> [arobase] <strong>avroy</strong> [point] be.</noscript>
```

Un scraper qui matche `\b[\w.+-]+@[\w.-]+\.\w+\b` ne trouve rien. Un humain lit sans friction.

### 3. Script inline de reconstruction

À la fin du bloc, ~15 lignes de JS qui décodent les `data-*` et remplacent le `<span>` par un `<a href="mailto:…">` cliquable au `DOMContentLoaded` :

```html
<script>
  (function () {
    var el = document.getElementById('contact-email');
    if (!el) return;
    var addr = atob(el.dataset.u) + '@' + atob(el.dataset.d);
    var a = document.createElement('a');
    a.href = 'mailto:' + addr;
    a.textContent = addr;
    el.replaceWith(a);
  })();
</script>
```

Choix techniques :

- **Inline plutôt que fichier séparé** : la promesse « un seul fichier à éditer » serait diluée si le décodage vivait dans `docs/javascripts/`. Inline = tout est dans `contact.md`.
- **IIFE** : pas de pollution du scope global, pas de dépendance à `defer`/`async` puisque le script s'exécute après le `<span>` dans le flux du document.
- **`replaceWith`** : remplace le span par le `<a>`, plus net que `innerHTML` (pas de risque d'injection même si l'adresse était modifiée par erreur).
- **`try/catch` autour de la reconstruction** : ajouté lors de la revue de code de Task 1. Le raisonnement initial du spec — « si `atob` échoue, l'utilisateur voit le `<noscript>` indirectement » — était incorrect : `<noscript>` est supprimé par le navigateur dès que JS est actif, donc un échec silencieux laisserait un visiteur avec JS sans aucune indication. Le `try/catch` remplit `el.textContent` avec la phrase obfusquée du `<noscript>` en cas d'échec d'`atob`, garantissant une dégradation visible.

---

## Localisation dans `contact.md`

Le bloc remplace cette ligne actuelle (ligne 13 environ) :

```markdown
**Courriel** : [florian@avroy.be](mailto:florian@avroy.be)
```

Par :

```markdown
**Courriel** : <span id="contact-email" data-u="Zmxvcmlhbg==" data-d="YXZyb3kuYmU="></span><noscript>Écrivez à <strong>florian</strong> [arobase] <strong>avroy</strong> [point] be.</noscript>

<script>
  (function () {
    var el = document.getElementById('contact-email');
    if (!el) return;
    var addr = atob(el.dataset.u) + '@' + atob(el.dataset.d);
    var a = document.createElement('a');
    a.href = 'mailto:' + addr;
    a.textContent = addr;
    el.replaceWith(a);
  })();
</script>
```

Aucune autre modification de la page n'est nécessaire. Le disclaimer juridique et les renvois externes restent inchangés.

---

## Changement futur d'adresse

Pour basculer vers, par exemple, `infofaillite@avroy.be` :

1. Encoder `infofaillite` en base64 → `aW5mb2ZhaWxsaXRl`, mettre dans `data-u`.
2. Si le domaine change aussi, encoder en base64, mettre dans `data-d`. Sinon laisser.
3. Mettre à jour le `<noscript>` : remplacer `<strong>florian</strong>` par `<strong>infofaillite</strong>`.

Trois modifications, un seul fichier, aucune autre partie du site n'est touchée. Commandes pour encoder en PowerShell :

```powershell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("infofaillite"))
```

---

## Hors périmètre

- **Formulaire de contact tiers** (Formspree, Netlify Forms) : écarté. Introduit une dépendance externe, un captcha, et complexifie une page qui doit rester sobre.
- **Obfuscation par entités HTML** sur les pages éditoriales : inutile puisque les CTA pointent vers `/contact` en lien interne Markdown, sans jamais contenir d'adresse.
- **CSS `::before` / `direction: rtl`** : écarté pour cause d'accessibilité dégradée (lecteurs d'écran).
- **Stockage de l'adresse dans une variable Zensical / partial `overrides/`** : écarté — la centralisation est déjà acquise par la structure (une seule page-cible).
- **Généralisation du CTA aux autres pages** : objet d'un futur cycle de travail séparé. Le présent spec se limite à la protection de l'adresse.

---

## Verification

À effectuer après implémentation :

1. **Build local** Zensical (`zensical serve` ou équivalent du projet). Servir le site sur `localhost`.
2. **Page contact servie** : ouvrir `view-source:` (ou Ctrl+U) sur `/contact/`. Vérifier qu'aucune occurrence de `florian` ni `avroy` n'apparaît en clair (en dehors du `<noscript>`, où ils sont séparés par `[arobase]`/`[point]`). Le HTML doit contenir uniquement les blobs base64 dans les `data-*`.
3. **Grep anti-regex e-mail** dans le HTML statique généré : `grep -E '[\w.+-]+@[\w.-]+\.\w+' site/contact/index.html` (chemin à adapter) — doit retourner zéro résultat.
4. **Visiteur avec JS** : ouvrir la page dans Chrome/Firefox. Vérifier que le lien cliquable `florian@avroy.be` apparaît à la place du span, et que `mailto:` se déclenche au clic.
5. **Visiteur sans JS** : désactiver JavaScript dans le navigateur (DevTools > Settings > Disable JavaScript). Recharger. Vérifier que la phrase « Écrivez à **florian** [arobase] **avroy** [point] be. » s'affiche et reste lisible.
6. **Lecteur d'écran** (best-effort, NVDA ou VoiceOver si disponible) : confirmer que le lien reconstruit est lu comme une adresse normale.
7. **Régression CTA pilote** : depuis [docs/faillis/checklist-premiere-semaine.md](../../docs/faillis/checklist-premiere-semaine.md), cliquer le lien du paragraphe CTA, vérifier qu'on arrive sur la page contact et que le `mailto:` y fonctionne.

---

## Fichiers touchés

- [docs/contact.md](../../docs/contact.md) — un bloc remplace la ligne `mailto:` actuelle.
- [log.md](../../log.md) — ajouter une entrée `## [2026-05-12] edit | Anti-spam page contact`.

Aucun autre fichier du projet n'est modifié.
