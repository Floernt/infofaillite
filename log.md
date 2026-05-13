# Log — infofaillite

Journal chronologique, append-only. Chaque entrée commence par `## [YYYY-MM-DD] <type> | <titre>` pour rester parsable (`grep "^## \[" log.md | tail -5`).

**Types courants** : `ingest` (nouvelle source ajoutée), `edit` (révision éditoriale), `refonte` (réécriture profonde), `seo` (passe SEO/GEO), `lint` (corrections de forme), `build` (build/déploiement), `config` (changement de config), `note` (observation hors modification).

---

## [2026-05-13] edit | Requête en refus d'effacement : page pilier

Enrichi [docs/faillis/effacement.md](docs/faillis/effacement.md) avec une sous-section dédiée à la **requête en refus d'effacement** déposée par le parquet (et les autres demandeurs : curateur, créancier impayé, tribunal d'office). Détaille la procédure : juridiction (tribunal de l'entreprise), audience contradictoire, défense, tierce opposition après clôture. Ajout d'un paragraphe correspondant dans [docs/comprendre/acteurs-secondaires.md](docs/comprendre/acteurs-secondaires.md) côté procureur du Roi, qui pointe vers la page pilier. Spec et plan dans [docs/superpowers/](docs/superpowers/).

## [2026-05-13] edit | Nuancer le délai de 30 jours (déclarations de créance)

Aligné toutes les mentions du délai de 30 jours pour la déclaration de créance sur une formulation type qui nomme explicitement le **3ᵉ procès-verbal de vérification** comme verrou de forclusion (≈ 12 mois après le jugement), au lieu de l'imprécis « passé un an ». Touche 8 fichiers : [docs/README.md](docs/README.md), [docs/creanciers/README.md](docs/creanciers/README.md), [docs/delais.md](docs/delais.md), [docs/creanciers/declarer-creance.md](docs/creanciers/declarer-creance.md), [docs/creanciers/faq.md](docs/creanciers/faq.md), [docs/comprendre/deroulement-phase-1-3.md](docs/comprendre/deroulement-phase-1-3.md), [docs/creanciers/verification-contestation.md](docs/creanciers/verification-contestation.md), [docs/glossaire.md](docs/glossaire.md). Spec et plan dans [docs/superpowers/](docs/superpowers/).

## [2026-05-13] edit | Format date français au pied de page

Suite directe du commit `lastmod automatique`. Le pied de page affichait la date au format ISO brut (`2026-05-13`) ; il l'affiche désormais en français — « Dernière mise à jour : 13 mai 2026 ». Géré dans [overrides/partials/source-file.html](overrides/partials/source-file.html) via une macro Jinja qui mappe les mois (compatible MiniJinja). Le sitemap garde le format ISO requis par sitemap.org.

## [2026-05-13] config | lastmod automatique dérivé de Git

Ajout d'une chaîne pré-build qui injecte la date du dernier commit Git dans le front matter de chaque page (`updated:`), avec deux templates Zensical overridés :

- [overrides/sitemap.xml](overrides/sitemap.xml) : `<lastmod>` par URL pour signaler la fraîcheur aux moteurs de recherche.
- [overrides/partials/source-file.html](overrides/partials/source-file.html) : pied de page « Dernière mise à jour » côté lecteur.

Script associé : [scripts/inject_git_dates.py](scripts/inject_git_dates.py), idempotent, mode `--check` pour CI. Spec et plan dans [docs/superpowers/](docs/superpowers/).

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
