# Anti-spam de l'adresse contact — Plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remplacer le `mailto:` en clair de [docs/contact.md](../../docs/contact.md) par un bloc HTML+JS inline qui n'expose aucune adresse e-mail scrapable, tout en restant cliquable pour les visiteurs avec JS et lisible pour ceux sans JS.

**Architecture:** Le bloc vit entièrement dans `contact.md`. Un `<span>` porte les morceaux de l'adresse encodés en base64 dans des attributs `data-u` (local-part) et `data-d` (domaine). Un `<noscript>` affiche une phrase lisible mais non-scrapable. Un script inline IIFE décode les deux morceaux au `DOMContentLoaded`, reconstruit l'adresse et remplace le span par un `<a href="mailto:…">` cliquable. Aucune variable, aucun partial, aucun fichier `extra_css` ni JS séparé — tout reste dans un seul fichier pour qu'un changement futur d'adresse soit une édition unique.

**Tech Stack:** Markdown (Zensical 0.0.24, dérivé MkDocs Material), HTML5 inline, JavaScript vanilla (atob, dataset, replaceWith). Aucune dépendance nouvelle.

**Spec de référence:** [superpowers/specs/2026-05-12-anti-spam-contact-email-design.md](../specs/2026-05-12-anti-spam-contact-email-design.md)

---

## File Structure

- **Modifier** : [docs/contact.md](../../docs/contact.md) — remplacer la ligne 14 (`**Courriel** : [florian@avroy.be](mailto:florian@avroy.be)`) par le bloc HTML+JS.
- **Modifier** : [log.md](../../log.md) — ajouter une entrée datée.

Aucun autre fichier touché.

---

## Task 1 : Remplacer le mailto par le bloc obfusqué

**Files:**
- Modify: `docs/contact.md` (ligne 14)

- [ ] **Step 1 : Vérifier que les valeurs base64 sont correctes**

Sur Windows PowerShell, lancer :

```powershell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("florian"))
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("avroy.be"))
```

Sortie attendue :

```
Zmxvcmlhbg==
YXZyb3kuYmU=
```

Si la sortie diffère, utiliser les valeurs obtenues à la place dans Step 2.

- [ ] **Step 2 : Remplacer la ligne 14 de `docs/contact.md`**

Remplacer exactement cette ligne :

```markdown
**Courriel** : [florian@avroy.be](mailto:florian@avroy.be)
```

Par ce bloc :

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

Notes :
- Le `<span>` et le `<noscript>` sont sur la même ligne que `**Courriel** :` pour préserver le flux du paragraphe Markdown.
- Le `<script>` est séparé par une ligne blanche pour que MkDocs/Zensical ne tente pas de le mélanger au paragraphe précédent.
- Ne pas indenter le `<script>` : Markdown traiterait quatre espaces de tête comme un bloc de code.

- [ ] **Step 3 : Vérifier que `mailto:` n'apparaît plus dans le fichier**

Run:

```powershell
Select-String -Path docs/contact.md -Pattern "mailto:|florian@|@avroy"
```

Expected: aucune ligne retournée (le fichier ne contient plus aucune mention en clair).

- [ ] **Step 4 : Vérifier que le bloc obfusqué est bien présent**

Run:

```powershell
Select-String -Path docs/contact.md -Pattern "contact-email|Zmxvcmlhbg=="
```

Expected: au moins deux lignes retournées (l'attribut `id` et la valeur `data-u`).

---

## Task 2 : Build local et vérification anti-scraper

**Files:** aucun (vérification uniquement)

- [ ] **Step 1 : Lancer le serveur Zensical local**

Run (PowerShell, depuis la racine du projet) :

```powershell
.venv\Scripts\Activate.ps1
zensical serve
```

Expected : serveur en écoute sur `http://127.0.0.1:8000` (ou port équivalent indiqué par Zensical). Pas d'erreur de build.

Si la commande `zensical serve` n'existe pas, essayer `zensical build` puis servir le dossier de sortie avec `python -m http.server` depuis ce dossier.

- [ ] **Step 2 : Vérifier le HTML rendu**

Dans un navigateur, ouvrir `http://127.0.0.1:8000/contact/`. Puis `Ctrl+U` (View Source) ou DevTools > Elements pour inspecter le HTML servi.

Expected dans le HTML statique :
- Présence : `<span id="contact-email" data-u="Zmxvcmlhbg==" data-d="YXZyb3kuYmU="></span>` et le `<noscript>` et le `<script>`.
- Absence : aucune occurrence de `florian@`, `@avroy`, ou `mailto:florian` dans le HTML *avant* exécution du JS.

- [ ] **Step 3 : Grep anti-regex e-mail sur le HTML statique**

Identifier le chemin du HTML généré (typiquement `site/contact/index.html` ou `site/contact.html` selon la config Zensical). Puis :

```powershell
Select-String -Path "site/contact/index.html" -Pattern "[\w.+-]+@[\w.-]+\.\w+" -AllMatches
```

Expected : zéro résultat. Si une occurrence apparaît, identifier sa provenance (autre contenu de la page ? template Zensical ? footer ?) et reporter.

- [ ] **Step 4 : Tester avec JS activé**

Dans le navigateur, sur `/contact/`, vérifier que le span est remplacé par un lien `florian@avroy.be` cliquable. Cliquer dessus : doit déclencher le client mail système avec `mailto:florian@avroy.be`.

Expected : lien visible, hover affiche `mailto:florian@avroy.be` dans la barre de statut, clic ouvre le client mail.

- [ ] **Step 5 : Tester avec JS désactivé**

DevTools > Settings (F1) > Debugger > « Disable JavaScript ». Recharger la page.

Expected : la phrase « Écrivez à **florian** [arobase] **avroy** [point] be. » s'affiche à la place du span. Pas de lien cliquable. Pas d'erreur visible.

Réactiver JavaScript après le test.

- [ ] **Step 6 : Régression sur la page pilote**

Dans le navigateur, ouvrir `/faillis/checklist-premiere-semaine/`. Scroller en bas. Cliquer sur le lien « florian@avroy.be » du CTA.

Expected : navigation vers `/contact/`. Une fois sur place, le lien obfusqué fonctionne comme dans Step 4.

Note : le CTA actuel dans `checklist-premiere-semaine.md` (ligne 125) affiche le texte `florian@avroy.be` mais pointe vers `../contact.md`. Le texte du CTA est cosmétique (le lien Markdown va vers la page contact, pas vers `mailto:`), donc il reste tel quel. Le texte affiché n'est pas un piège pour scrapers parce qu'il est aussi présent en clair dans le HTML du CTA — c'est un compromis hors scope de ce plan (objet de la généralisation future).

---

## Task 3 : Journaliser et committer

**Files:**
- Modify: `log.md`

- [ ] **Step 1 : Ajouter une entrée au log**

À la fin de `log.md`, ajouter :

```markdown

## [2026-05-12] edit | Anti-spam adresse contact

Remplacement du `mailto:` en clair de [docs/contact.md](docs/contact.md) par un bloc HTML+JS inline. L'adresse n'apparaît plus dans le HTML statique servi : les morceaux (`florian`, `avroy.be`) sont stockés en base64 dans des attributs `data-*` d'un `<span>`, reconstruits par un script inline au chargement, et remplacés par un `<a href="mailto:…">` cliquable. Fallback `<noscript>` lisible humainement mais non-scrapable pour visiteurs sans JS.

Changement futur d'adresse : éditer les valeurs `data-u`, `data-d` et le `<noscript>` dans le même fichier. Aucune variable ni JS séparé.

Spec : [superpowers/specs/2026-05-12-anti-spam-contact-email-design.md](superpowers/specs/2026-05-12-anti-spam-contact-email-design.md).
```

- [ ] **Step 2 : Vérifier le statut git**

Run:

```powershell
git status
```

Expected : `docs/contact.md` et `log.md` modifiés. Le dossier `superpowers/` peut apparaître en untracked s'il ne l'était pas déjà — c'est attendu (spec + plan).

- [ ] **Step 3 : Stager et committer**

Run:

```powershell
git add docs/contact.md log.md superpowers/specs/2026-05-12-anti-spam-contact-email-design.md superpowers/plans/2026-05-12-anti-spam-contact-email.md
git commit -m @'
Protéger l'adresse contact des scrapers

Bloc HTML+JS inline dans docs/contact.md : base64 dans data-*,
reconstruction au DOMContentLoaded, fallback <noscript> lisible.
Aucune dépendance ajoutée. Changement futur = éditer un seul fichier.
'@
```

Expected : commit créé. Vérifier avec `git log -1 --stat`.

---

## Self-review

**Spec coverage :**
- §Architecture / Marqueur HTML inerte → Task 1 Step 2 (span + data-u/data-d en base64).
- §Architecture / Fallback `<noscript>` → Task 1 Step 2 (phrase obfusquée).
- §Architecture / Script inline → Task 1 Step 2 (IIFE, replaceWith).
- §Localisation dans `contact.md` → Task 1 Step 2 (remplace bien la ligne 14, qui correspond au `**Courriel** :` actuel après l'évolution du fichier).
- §Changement futur d'adresse → couvert dans l'entrée du log (Task 3 Step 1) ; pas de tâche dédiée car ce n'est pas un livrable de cette implémentation, c'est une propriété du design.
- §Hors périmètre → aucune tâche ne tente d'aller au-delà.
- §Verification → Task 2 (build + grep + JS on/off + régression pilote).
- §Fichiers touchés → uniquement `docs/contact.md` et `log.md`, exactement comme prévu.

**Placeholder scan :** aucun TBD, aucun « add error handling », aucun « similar to ». Toutes les commandes et tous les blocs de code sont complets.

**Type consistency :** `data-u` / `data-d` apparaissent dans le HTML, le JS, le grep et la note de changement futur — cohérents partout. `contact-email` est l'unique `id` utilisé. `atob` / `dataset` / `replaceWith` ne changent pas de nom entre tâches.

**Note d'écart vs spec :** le spec décrivait la ligne 14 comme `**Courriel** : [florian@avroy.be](mailto:florian@avroy.be)` — c'est encore exact dans le fichier actuel. Si entre maintenant et l'exécution la ligne bouge, l'exécutant doit chercher la ligne contenant `mailto:florian@avroy.be` et la remplacer en préservant le préfixe `**Courriel** :`.
