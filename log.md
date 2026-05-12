# Log — infofaillite

Journal chronologique, append-only. Chaque entrée commence par `## [YYYY-MM-DD] <type> | <titre>` pour rester parsable (`grep "^## \[" log.md | tail -5`).

**Types courants** : `ingest` (nouvelle source ajoutée), `edit` (révision éditoriale), `refonte` (réécriture profonde), `seo` (passe SEO/GEO), `lint` (corrections de forme), `build` (build/déploiement), `config` (changement de config), `note` (observation hors modification).

---

## [2026-05-12] config | Création de CLAUDE.md et log.md

Mise en place de [CLAUDE.md](CLAUDE.md) (contexte projet pour les futures sessions) et de ce journal. Aucune modification du contenu éditorial.

## [2026-05-12] edit | CTA léger — page pilote checklist-premiere-semaine

Mise en place d'un CTA léger en fin de page sur [docs/faillis/checklist-premiere-semaine.md](docs/faillis/checklist-premiere-semaine.md) : un paragraphe court après « Pour aller plus loin » invitant à signaler une étape floue ou un manque, avec lien vers une nouvelle page contact (mailto `florian@avroy.be`).

Création de la page [docs/contact.md](docs/contact.md), ajoutée au [SUMMARY.md](docs/SUMMARY.md) après « À propos ». La page rappelle explicitement que l'écriture ne constitue pas une demande de conseil juridique et renvoie vers curateur / avocat / juge-commissaire pour les situations personnelles.

Forme retenue : paragraphe étendu (pas d'admonition ni de bouton). Périmètre : pilote unique avant généralisation.

## [2026-05-12] edit | Anti-spam adresse contact

Remplacement du `mailto:` en clair de [docs/contact.md](docs/contact.md) par un bloc HTML+JS inline. L'adresse n'apparaît plus dans le HTML statique servi : les morceaux (`florian`, `avroy.be`) sont stockés en base64 dans des attributs `data-*` d'un `<span>`, reconstruits par un script inline au chargement (avec `try/catch` de sécurité), et remplacés par un `<a href="mailto:…">` cliquable. Fallback `<noscript>` lisible humainement mais non-scrapable pour visiteurs sans JS.

Correction collatérale du CTA pilote sur [docs/faillis/checklist-premiere-semaine.md](docs/faillis/checklist-premiere-semaine.md) : le texte du lien (qui contenait encore l'adresse en clair, scrapable dans le HTML servi et dans `site/search.json`) est devenu « Posez votre question via la page de contact ». Plus aucune occurrence de l'adresse dans le site généré.

Changement futur d'adresse : éditer les valeurs `data-u`, `data-d` et le `<noscript>` dans [docs/contact.md](docs/contact.md). Aucune variable ni JS séparé.

Spec : [superpowers/specs/2026-05-12-anti-spam-contact-email-design.md](superpowers/specs/2026-05-12-anti-spam-contact-email-design.md).
Plan : [superpowers/plans/2026-05-12-anti-spam-contact-email.md](superpowers/plans/2026-05-12-anti-spam-contact-email.md).

Vérifications manuelles restant à effectuer côté navigateur (non automatisables) :

- ouvrir `/contact/` avec JS activé → vérifier le lien cliquable reconstruit ;
- désactiver JS → vérifier le fallback `<noscript>` lisible ;
- cliquer le CTA depuis `/faillis/checklist-premiere-semaine/` → vérifier la navigation vers `/contact/` ;
- (best-effort) tester avec un lecteur d'écran (NVDA / VoiceOver) que le lien reconstruit est annoncé comme une adresse e-mail normale.

## [2026-05-12] note | Alignement spec et plan sur l'implémentation effective

Mise à jour de [superpowers/specs/2026-05-12-anti-spam-contact-email-design.md](superpowers/specs/2026-05-12-anti-spam-contact-email-design.md) et [superpowers/plans/2026-05-12-anti-spam-contact-email.md](superpowers/plans/2026-05-12-anti-spam-contact-email.md) pour refléter ce qui a été effectivement construit : (1) le `try/catch` ajouté lors de la revue de Task 1 (le spec disait « pas de try/catch » avec un raisonnement incorrect) ; (2) la correction du CTA pilote (Task 1bis) qui n'apparaissait dans le plan que comme « hors scope ».

Reformulation de la section « Mémoire de travail » de [CLAUDE.md](CLAUDE.md) en « Historique récent » pour éviter qu'elle devienne périmée à la fin de la session.

## [2026-05-12] note | Corrections finales spec et log

Mise à jour de [superpowers/specs/2026-05-12-anti-spam-contact-email-design.md](superpowers/specs/2026-05-12-anti-spam-contact-email-design.md) pour synchroniser les deux blocs de code (`§3. Script inline de reconstruction` et `§Localisation dans contact.md`) avec la version effectivement déployée (try/catch, comment HTML, span et noscript sur deux lignes). Ajout d'une 4e étape à `§ Changement futur d'adresse` : mettre à jour la phrase de secours dans le `catch`, qui était hardcodée et non documentée.

Ajout du test lecteur d'écran à la liste des vérifications manuelles déférées (best-effort).
