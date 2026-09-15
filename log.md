# Log — infofaillite

Journal chronologique, append-only. Chaque entrée commence par `## [YYYY-MM-DD] <type> | <titre>` pour rester parsable (`grep "^## \[" log.md | tail -5`).

**Types courants** : `ingest` (nouvelle source ajoutée), `edit` (révision éditoriale), `refonte` (réécriture profonde), `seo` (passe SEO/GEO), `lint` (corrections de forme), `build` (build/déploiement), `config` (changement de config), `note` (observation hors modification).

---

## [2026-08-31] edit | Réhabilitation, levée d'interdiction et actualité de la base légale

Deux points arbitrés par l'utilisateur en fin de session, puis vérification de l'actualité de la base légale.

**1. Interdiction de gérer : pas de levée anticipative.** Confirmation : aucune levée pour bonne conduite ni anticipative. [docs/comprendre/cloture.md](docs/comprendre/cloture.md) l'affirmait en deux endroits (« levée anticipativement sur requête », « levée anticipée prononcée par le tribunal »), en contradiction avec [docs/faillis/interdiction.md](docs/faillis/interdiction.md) — contradiction signalée lors de la passe précédente. **Correction factuelle** : les deux passages renvoient désormais aux deux seules causes d'extinction anticipée (rétractation du jugement déclaratif, réhabilitation XX.237).

**2. Réhabilitation (art. XX.237).** [docs/faillis/effacement.md](docs/faillis/effacement.md) traitait le refus d'effacement sans mentionner de voie de sortie — le lecteur repartait en croyant sa situation définitive. Nouvelle section **« Si l'effacement vous est refusé : la réhabilitation »** : ouverte au failli qui n'a pas obtenu l'effacement et qui a intégralement acquitté en principal, intérêts et frais toutes les sommes dues ; effet extinctif sur l'interdiction de gérer (XX.235). Nouvelle entrée **Réhabilitation** au [glossaire](docs/glossaire.md), et **correction factuelle** de l'entrée « Interdiction de gérer », qui présentait les trois ans comme un plafond d'interdiction pour aveu tardif alors qu'il s'agit de la durée maximale du sursis (XX.229 §1).

**3. Actualité de la base légale** (vérification sur sources officielles, à la demande de l'utilisateur). La **loi du 7 juin 2023** (M.B. 7 juillet 2023, transposition de la directive 2019/1023) reste la dernière réforme de fond du Livre XX, applicable aux procédures ouvertes depuis le 1er septembre 2023. Aucune loi postérieure ne le modifie sur le fond. La **directive (UE) 2026/799 du 1er avril 2026** (« Insolvabilité III ») imposera une réforme de fond mais son délai de transposition court jusqu'au **22 janvier 2029** : elle n'est pas applicable aujourd'hui. Mention ajoutée dans [docs/a-propos.md](docs/a-propos.md).

**4. Correction factuelle : borne d'articles du Livre XX.** Le site bornait le Livre XX à « XX.1 à XX.235 » en cinq endroits ([a-propos](docs/a-propos.md), [ressources](docs/ressources.md), [README](docs/README.md), [definition-faillite](docs/comprendre/definition-faillite.md), [glossaire](docs/glossaire.md)), alors qu'il va jusqu'à **XX.241** (Titre IX, interdictions et réhabilitations) — borne démentie par les articles XX.237 à XX.241 que le site citait lui-même. Corrigée partout.

**5. Dissolution judiciaire au lieu de la faillite.** [docs/comprendre/procedures-alternatives.md](docs/comprendre/procedures-alternatives.md) : nouvelle section sur la faculté du tribunal, saisi d'un aveu ou d'une demande de faillite, de prononcer la dissolution de la société plutôt que la faillite (**art. 2:74/1 CSA**, applicable depuis le 1er septembre 2023) — cas des sociétés sans activité, sans actif ni personnel. Le front matter de la page annonçait « dissolution judiciaire » sans que le corps la traite ; `description` corrigé au passage (« ASBL » → « au lieu de la faillite »).

**6. Correction de lien.** [docs/comprendre/deroulement-phase-4-5.md](docs/comprendre/deroulement-phase-4-5.md) : les deux renvois vers `contester-creance.md` pointaient vers `comprendre/` alors que la page vit dans `creanciers/` — lecteurs en 404. Détecté au contrôle systématique des 386 liens internes du site.

Contrôle final : build Zensical propre, **386 liens internes vérifiés, 0 cassé, 0 ancre introuvable**. Dates `updated:` rafraîchies via `python scripts/inject_git_dates.py`.

---

## [2026-08-31] edit | Dettes avant la faillite : intérêts, frais de recouvrement et saisies

Trois questions reçues par la page contact portaient sur une phase que le guide ne couvrait pas : celle du débiteur qui accumule des dettes **sans être en faillite**. Vérification faite, aucune des trois n'avait de réponse sur le site — les intérêts n'étaient traités que sous l'angle de leur *arrêt* par le jugement (deux lignes de FAQ créanciers, sans base légale), « saisie-arrêt » n'apparaissait nulle part, et « indépendant complémentaire » pas davantage. Le site n'offrait que deux portes d'entrée, « je suis en faillite » et « je suis créancier ».

- [docs/comprendre/dettes-avant-faillite.md](docs/comprendre/dettes-avant-faillite.md) : **nouvelle page**. Ce qui continue à s'ajouter à la dette (intérêt conventionnel et légal, loi du 2 août 2002 entre entreprises, clauses pénales et pouvoir de modération du juge, recouvrement amiable et loi du 4 mai 2023 pour les consommateurs, majorations fisc/TVA/ONSS/caisse sociale et plans d'apurement) ; effet d'une procédure sur le cours des intérêts (**article XX.113 CDE**, exception hypothécaire, moratoire PRJ publique vs absence de moratoire en PRJ privée) ; mécanique des saisies (titre exécutoire, conservatoire vs exécution, commandement de payer, saisie mobilière et articles 1408-1412 C. jud., **saisie-arrêt sur salaire et quotités de l'article 1409**, article 1411bis pour les sommes créditées en compte, saisie immobilière, fichier central des avis de saisie) ; exercice d'une activité indépendante malgré des dettes, avec le cas de l'**indépendant complémentaire** (aucun cloisonnement patrimonial : le salaire du poste principal est saisissable pour une dette professionnelle, et inversement) et les conséquences à terme (faillibilité de l'indépendant complémentaire au sens du Livre XX, patrimoine unique, activité déficitaire, cotisations sociales, délai d'un mois pour l'aveu). Choix éditorial : **expliquer les mécanismes sans citer de montants**, les barèmes de l'article 1409 étant indexés chaque année — renvoi au SPF Justice. Section de bornage du périmètre pour ne pas laisser croire que la faillite est la seule issue, sans étendre le guide hors Livre XX.
- [docs/SUMMARY.md](docs/SUMMARY.md) et [docs/README.md](docs/README.md) : entrée dans « Comprendre la procédure », avant les procédures alternatives (les dettes montent → les alternatives).
- [docs/comprendre/procedures-alternatives.md](docs/comprendre/procedures-alternatives.md) : renvoi depuis « Avant toute procédure judiciaire ». **Correction de deux coquilles** l. 31 (« être envisagées » → « envisagée », « eaussi » → « aussi »).
- [docs/comprendre/definition-faillite.md](docs/comprendre/definition-faillite.md) : renvoi depuis « L'ébranlement du crédit », qui évoquait saisies et huissier sans les expliquer. **Correction factuelle** : la réorganisation judiciaire relève du **Titre V** du Livre XX, la page indiquait Titre VI — en contradiction interne avec procedures-alternatives.md.
- [docs/comprendre/dessaisissement.md](docs/comprendre/dessaisissement.md) : FAQ « Mon salaire peut-il être saisi par le curateur ? » — les « limites légales » sont désormais rattachées à l'article 1409 C. jud. avec renvoi.
- [docs/creanciers/paiement-dividendes.md](docs/creanciers/paiement-dividendes.md) et [docs/creanciers/verification-contestation.md](docs/creanciers/verification-contestation.md) : **base légale ajoutée** (article XX.113 CDE) sur les deux FAQ qui affirmaient l'arrêt des intérêts sans la citer, + renvoi pour l'avant-faillite.
- [docs/faillis/faq.md](docs/faillis/faq.md) : nouvelle entrée **« Mes dettes continuent-elles à augmenter ? »** (figées après le jugement, inverse avant).
- [docs/glossaire.md](docs/glossaire.md) : six entrées — **huissier de justice**, **quotité insaisissable** (nouveau bloc `## Q`), **saisie-arrêt**, **saisie conservatoire**, **saisie-exécution**, **titre exécutoire** ; renvoi ajouté depuis « insaisissable ».
- [docs/ressources.md](docs/ressources.md) : article 1409 C. jud. et barèmes indexés du SPF Justice, lois du 4 mai 2023 et du 2 août 2002.

Build Zensical vérifié : ancres générées conformes, les 9 liens sortants de la nouvelle page et les 9 renvois entrants résolvent tous, trois admonitions rendues (`warning` intérêts, `danger` saisie sur salaire, `tip` fermeture des options), aucun montant chiffré dans la page. Dates `updated:` rafraîchies via `python scripts/inject_git_dates.py`.

**Reste à arbitrer** (non touché) : [docs/comprendre/cloture.md](docs/comprendre/cloture.md) affirme que l'interdiction de gérer peut être levée anticipativement sur requête, alors que [docs/faillis/interdiction.md](docs/faillis/interdiction.md) exclut explicitement toute levée pour bonne conduite. Les deux ne peuvent être exacts. Le glossaire mentionne par ailleurs une durée de « trois ans (aveu tardif) » sans contrepartie dans interdiction.md.

## [2026-05-15] edit | Contact & À propos : refonte autour de « information gratuite, conseil payant »

Reformulation des deux pages institutionnelles autour d'une même ligne assumée à la première personne.

- [docs/contact.md](docs/contact.md) : remplacement de la section négative « Ce que ce contact n'est pas » par **« L'information est gratuite, le conseil est payant »**. Distinction explicite entre échanges ponctuels (signalement, question générale — n'ouvrent pas de relation client) et demande d'accompagnement (consultation à organiser à la même adresse, rendez-vous au cabinet ou à distance, cadre d'honoraires défini en amont, relation avocat-client ouverte). Curateur / autre avocat / juge-commissaire repositionnés comme alternatives si la consultation à mes côtés n'est pas la bonne porte.
- [docs/a-propos.md](docs/a-propos.md) : « Ce guide » remplacé par **« Pourquoi ce site »**, conviction assumée (l'info juridique doit circuler librement, pas être verrouillée derrière une consultation). Nouvelle section **« Information gratuite, conseil payant »** alignée sur la page contact, avec renvoi vers [contact.md](docs/contact.md) pour organiser une consultation. Bloc Auteur : miniature à droite (photo depuis avroy.be) + reformulation (« à titre personnel, à partir de ma propre pratique »). Bloc Mise à jour épuré (suppression de la date figée « Avril 2026 », la date de pied de page sert déjà à ça).

---

## [2026-05-15] edit | Passe « faillis » : effacement, interdiction, reprise d'activité, FAQ, terminologie pénale

Deuxième session du 15 mai, sur les pages [docs/faillis/](docs/faillis/) principalement, avec quelques retombées dans [docs/comprendre/](docs/comprendre/) et [docs/glossaire.md](docs/glossaire.md). Six axes :

**1. Banqueroute → poursuites pénales.** La qualification autonome de banqueroute (simple/frauduleuse) est en pratique très peu utilisée ; les faits sont aujourd'hui poursuivis sous des qualifications de droit pénal commun (abus de biens sociaux, faux et usage, organisation frauduleuse d'insolvabilité, escroquerie). Reformulation cohérente sur [docs/faillis/obligations.md](docs/faillis/obligations.md) (titre de section, paragraphe transparence, keyword du front matter), [docs/comprendre/acteurs-secondaires.md](docs/comprendre/acteurs-secondaires.md) (admonition), [docs/faillis/effacement.md](docs/faillis/effacement.md) (causes de refus), [docs/faillis/reprendre-activite.md](docs/faillis/reprendre-activite.md) (condition du droit passerelle), [docs/faillis/checklist-premiere-semaine.md](docs/faillis/checklist-premiere-semaine.md), [docs/faillis/faq.md](docs/faillis/faq.md). L'entrée du [glossaire](docs/glossaire.md) est recadrée en « terme historique » et renvoie aux qualifications réelles.

**2. Effacement — trois corrections de fond sur [docs/faillis/effacement.md](docs/faillis/effacement.md).** Précisé que le tribunal statue sur l'effacement par **décision distincte** du jugement de clôture (même jour ou peu après). **Correction factuelle majeure** : le dirigeant d'une société faillie ne bénéficie *pas* de l'effacement — c'est la société qui est en faillite, ses engagements personnels (cautions, codébitions, prêts injectés) restent intégralement dus ; seule voie d'accès à l'effacement = faillite personnelle distincte. Clarification : les « cautions personnelles » effacées sont celles *souscrites par* le failli au profit de tiers, à ne pas confondre avec les cautions *données à* son profit par des proches (qui restent dues).

**3. Interdiction de gérer — [docs/faillis/interdiction.md](docs/faillis/interdiction.md).** **Correction factuelle** : le Livre XX ne prévoit *aucun mécanisme* de levée anticipée pour bonne conduite ; la section qui le décrivait est supprimée. Le seul mécanisme légal d'extinction anticipée est la **réhabilitation** de l'article XX.237 CDE, qui suppose le **désintéressement intégral** des créanciers (principal + intérêts + frais). Le failli qui a obtenu l'effacement est réputé réhabilité de plein droit ; XX.235 prévoit alors que l'interdiction prend fin. Procédure XX.238-241 documentée (requête, publication au Moniteur, opposition créancier dans le mois, délai d'un an avant nouvelle demande après rejet).

**4. Reprise de l'activité — [docs/faillis/reprendre-activite.md](docs/faillis/reprendre-activite.md).** Position ferme à la place de la « forte recommandation » précédente : reprendre l'activité faillie en réutilisant fonds de commerce, clientèle, enseigne, savoir-faire ou contrats en cours constitue un **détournement d'actifs** (poursuites pénales, refus d'effacement, réintégration dans la masse). Seule voie légale pour poursuivre : racheter le fonds auprès du curateur. FAQ alignée.

**5. Blocage automatique des comptes bancaires — [docs/faillis/checklist-premiere-semaine.md](docs/faillis/checklist-premiere-semaine.md).** Rappel que la publication du jugement au Moniteur belge entraîne automatiquement le blocage de *tous* les comptes (sans démarche du curateur), à l'endroit où l'on conseille au failli d'ouvrir un compte personnel — l'enjeu pratique étant qu'il se retrouve sinon sans accès à ses liquidités courantes du jour au lendemain.

**6. FAQ failli — [docs/faillis/faq.md](docs/faillis/faq.md).** Alignements de session : « Vais-je tout perdre » recalé sur [dessaisissement.md](docs/comprendre/dessaisissement.md) (un seul patrimoine, règle de la cause pour héritages/donations) ; « Refus de collaborer » : interdiction jusqu'à 10 ans (XX.229 §1) au lieu des « 3 ans » ; « Racheter des biens » : présenté comme la seule voie légale pour poursuivre l'activité ; nouvelle Q/R « Puis-je relancer la même activité juste après la faillite ? » ; « Faire appel » développée en trois voies (appel, opposition, tierce opposition) avec nécessité d'un avocat spécialisé.

**CTA contact** ajouté sur [docs/faillis/droits.md](docs/faillis/droits.md), [docs/faillis/effacement.md](docs/faillis/effacement.md), [docs/faillis/interdiction.md](docs/faillis/interdiction.md), [docs/faillis/faq.md](docs/faillis/faq.md), sur le modèle de la checklist.

Dates `updated:` rafraîchies via `python scripts/inject_git_dates.py`.

## [2026-05-15] edit | Caution : retirer la fausse « décharge automatique » + refonte PRJ post-réforme 2023

Deux corrections de fond menées dans la même session.

**1. Caution non déclarée — correction factuelle majeure.** L'ensemble du site affirmait qu'à défaut de déclaration de la sûreté personnelle dans les trois mois suivant le jugement, la caution était automatiquement déchargée. C'est faux : le droit du créancier contre la caution est indépendant de la procédure de faillite, il n'existe ni délai spécifique ni décharge automatique pour défaut de mention. L'affirmation a été retirée et remplacée par une formulation cohérente (mention utile mais non sanctionnée, seuls mécanismes réels conservés : cohabitation 6 mois pour le conjoint/cohabitant caution, décharge judiciaire pour cautionnement disproportionné) sur 12 fichiers : [docs/comprendre/cloture.md](docs/comprendre/cloture.md), [docs/creanciers/suretes-cautions.md](docs/creanciers/suretes-cautions.md), [docs/faillis/effacement.md](docs/faillis/effacement.md), [docs/delais.md](docs/delais.md), [docs/README.md](docs/README.md), [docs/glossaire.md](docs/glossaire.md), [docs/creanciers/README.md](docs/creanciers/README.md), [docs/creanciers/declarer-creance.md](docs/creanciers/declarer-creance.md), [docs/creanciers/droits-specifiques.md](docs/creanciers/droits-specifiques.md), [docs/creanciers/creanciers-categories.md](docs/creanciers/creanciers-categories.md), [docs/comprendre/deroulement-phase-1-3.md](docs/comprendre/deroulement-phase-1-3.md), [docs/faillis/checklist-premiere-semaine.md](docs/faillis/checklist-premiere-semaine.md).

**2. PRJ — refonte de [procedures-alternatives.md](docs/comprendre/procedures-alternatives.md) sur la base de la réforme du 7 juin 2023** (transposition de la directive 2019/1023, applicable depuis le 1er septembre 2023). Les « trois voies » de l'ancien régime sont remplacées par les quatre voies actuelles : **mesures amiables** (médiation, accord amiable extrajudiciaire, accord collectif extrajudiciaire — confidentielles), **PRJ privée** (confidentielle, sans moratoire général — nouveauté 2023), **PRJ publique** (moratoire de 4 mois prorogeable, strictement encadré), **régime spécial des grandes entreprises** (vote par classes, cram-down inter-classes, seuils 50 ETP / 4,5 M€ bilan / 9 M€ CA). Signalé : le **transfert sous autorité de justice n'est plus une modalité de la PRJ** mais une procédure de liquidation distincte. Sursis de la PRJ publique recalibré (4 mois au lieu des « 6 à 18 mois » de l'ancien régime). Liens externes ajoutés (SEO/GEO) vers [florianernotte.be/matieres/prj/](https://florianernotte.be/matieres/prj/) et ses sous-pages (mesures-amiables, prj-privee, prj-publique, grandes-entreprises) à plusieurs endroits opportuns (chaque voie, admonitions, paragraphe de conclusion, bloc dédié dans « Pour aller plus loin »).

Dates `updated:` rafraîchies via `python scripts/inject_git_dates.py`.

## [2026-05-14] edit | Relecture des pages « Comprendre » (déroulement, dessaisissement, période suspecte, liquidation)

Passe de relecture sur six pages du dossier [docs/comprendre/](docs/comprendre/), à partir de remarques et précisions dictées en session :

- [deroulement-chronologique.md](docs/comprendre/deroulement-chronologique.md) — tableau des délais clés allégé (mois pour l'aveu reformulé, déclaration de créance marquée « conseillé »).
- [deroulement-phase-1-3.md](docs/comprendre/deroulement-phase-1-3.md) — aveu déposé entièrement en ligne sur REGSOL ; citation par créancier ou Ministère public (échec des voies d'exécution, créanciers institutionnels SPF/ONSS/caisses sociales) ; blocage des comptes bancaires repositionné comme effet automatique de la publication au Moniteur belge, pas une démarche du curateur ; lien vers [definition-faillite.md](docs/comprendre/definition-faillite.md).
- [deroulement-phase-4-5.md](docs/comprendre/deroulement-phase-4-5.md) — section « actions en justice » enrichie : responsabilité des administrateurs pour manquements au CSA (comptabilité, dépôt des comptes annuels, sonnette d'alarme, poursuite déraisonnable), action contre les actionnaires n'ayant pas libéré leur capital souscrit ; encadré sur la voie ONSS autonome (faillites successives) avec lien externe vers l'article blog [avroy.be](https://avroy.be/demission-responsabilite-faillite-adminsitrateur/).
- [dessaisissement.md](docs/comprendre/dessaisissement.md) — admonition `warning` sur l'unicité du patrimoine pour les indépendants personnes physiques (privé + investissements + professionnel) ; règle de la cause pour les héritages et donations (le fait générateur, pas la date d'encaissement) ; admonition `danger` sur le délai de forclusion de l'action en revendication (avant le dépôt du premier PV de vérification).
- [periode-suspecte.md](docs/comprendre/periode-suspecte.md) — **correction factuelle importante** : suppression des sous-délais erronés (« 10 jours » pour les paiements anormaux, « 6 mois » pour les sûretés et les paiements de dettes non échues) ; les nullités de plein droit s'appliquent sur **toute la période suspecte**, dont la durée maximale est de 6 mois. Ajout en amont d'une section sur le préalable indispensable du report judiciaire de la date de cessation des paiements (sans report, pas de nullités), et d'une sous-section sur l'exception de l'**action paulienne** (Livre XX CDE, inopposabilité indépendamment de la date, charge probatoire de la fraude).
- [liquidation-actifs.md](docs/comprendre/liquidation-actifs.md) — alignement avec [periode-suspecte.md](docs/comprendre/periode-suspecte.md) (retrait des mêmes sous-délais 10j/6m), précision sur l'article XX.225, nettoyage rédactionnel.

Sources vérifiées : ancien article 17 de la loi du 8 août 1997 sur les faillites (repris au Livre XX CDE) — confirmation que les trois catégories de nullités de plein droit visent l'ensemble de la période suspecte, et non des fenêtres distinctes plus courtes.

Dates `updated:` du front-matter rafraîchies via `python scripts/inject_git_dates.py` après les commits éditoriaux.

## [2026-05-13] edit | Requête en refus d'effacement : page pilier

Enrichi [docs/faillis/effacement.md](docs/faillis/effacement.md) avec une sous-section dédiée à la **requête en refus d'effacement** déposée par le parquet (et les autres demandeurs : curateur, créancier impayé, tribunal d'office). Détaille la procédure : juridiction (tribunal de l'entreprise), audience contradictoire, défense, tierce opposition après clôture. Ajout d'un paragraphe correspondant dans [docs/comprendre/acteurs-secondaires.md](docs/comprendre/acteurs-secondaires.md) côté procureur du Roi, qui pointe vers la page pilier. Spec et plan dans [superpowers/](superpowers/).

## [2026-05-13] edit | Nuancer le délai de 30 jours (déclarations de créance)

Aligné toutes les mentions du délai de 30 jours pour la déclaration de créance sur une formulation type qui nomme explicitement le **3ᵉ procès-verbal de vérification** comme verrou de forclusion (≈ 12 mois après le jugement), au lieu de l'imprécis « passé un an ». Touche 8 fichiers : [docs/README.md](docs/README.md), [docs/creanciers/README.md](docs/creanciers/README.md), [docs/delais.md](docs/delais.md), [docs/creanciers/declarer-creance.md](docs/creanciers/declarer-creance.md), [docs/creanciers/faq.md](docs/creanciers/faq.md), [docs/comprendre/deroulement-phase-1-3.md](docs/comprendre/deroulement-phase-1-3.md), [docs/creanciers/verification-contestation.md](docs/creanciers/verification-contestation.md), [docs/glossaire.md](docs/glossaire.md). Spec et plan dans [superpowers/](superpowers/).

## [2026-05-13] edit | Format date français au pied de page

Suite directe du commit `lastmod automatique`. Le pied de page affichait la date au format ISO brut (`2026-05-13`) ; il l'affiche désormais en français — « Dernière mise à jour : 13 mai 2026 ». Géré dans [overrides/partials/source-file.html](overrides/partials/source-file.html) via une macro Jinja qui mappe les mois (compatible MiniJinja). Le sitemap garde le format ISO requis par sitemap.org.

## [2026-05-13] config | lastmod automatique dérivé de Git

Ajout d'une chaîne pré-build qui injecte la date du dernier commit Git dans le front matter de chaque page (`updated:`), avec deux templates Zensical overridés :

- [overrides/sitemap.xml](overrides/sitemap.xml) : `<lastmod>` par URL pour signaler la fraîcheur aux moteurs de recherche.
- [overrides/partials/source-file.html](overrides/partials/source-file.html) : pied de page « Dernière mise à jour » côté lecteur.

Script associé : [scripts/inject_git_dates.py](scripts/inject_git_dates.py), idempotent, mode `--check` pour CI. Spec et plan dans [superpowers/](superpowers/).

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

## 2026-08-31 08:52:13 - session 2a52abbe

**Demande :** continue

**Action :** Done. Four commits on `gh-pages`, working tree clean, not pushed (per the project workflow).  ## Réponse à la question posée  Le site ne répondait à **aucune des trois questions**. Il disait même l'inverse de ce qu'il fallait sur la première : les seules mentions d'intérêts expliquaient qu'ils *cessent* de courir au jugement de faillite — vrai, mais sans intérêt pour quelqu'un qui n'est pas en faillite. « Saisie-arrêt » et « indépendant complémentaire » n'apparaissaient nulle part dans le repo. ...

**Outils utilises :** aucun

---

## 2026-09-02 16:43:14 - session 2a52abbe

**Demande :** reprend et vérifie que tout est ok

**Action :** Tout est vérifié. Voici l'état réel.  ## Ce qui a été contrôlé  | Contrôle | Résultat | |---|---| | Build Zensical (from scratch, `site/` supprimé) | OK, 36 pages | | Liens internes de tout le site | **385 vérifiés, 0 cassé** | | Ancres internes | **0 introuvable** | | Page au sitemap avec `lastmod` | OK (`2026-08-31`) | | Les 3 admonitions | `warning` / `danger` / `tip` rendues | | Absence de montants chiffrés | conforme (décision « mécanisme sans montants ») | | Bases légales rendues | XX.113,...

**Outils utilises :** aucun

---
