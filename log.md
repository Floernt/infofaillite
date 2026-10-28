# Log — infofaillite

Journal chronologique, append-only. Chaque entrée commence par `## [YYYY-MM-DD] <type> | <titre>` pour rester parsable (`grep "^## \[" log.md | tail -5`).

**Types courants** : `ingest` (nouvelle source ajoutée), `edit` (révision éditoriale), `refonte` (réécriture profonde), `seo` (passe SEO/GEO), `lint` (corrections de forme), `build` (build/déploiement), `config` (changement de config), `note` (observation hors modification).

---

## [2026-10-28] refonte | Navigation et identité visuelle

Refonte de l'expérience de navigation, sur maquette validée par l'utilisateur (inspiration : noerr.com). Le menu latéral unique de plus de 50 entrées, trié par nom de fichier, est remplacé par une navigation par rubrique.

**Navigation.**
- Menu explicite dans [zensical.toml](zensical.toml) : quatre rubriques (Je suis en faillite, Je suis créancier, Comprendre la procédure, Actualités) intégrées à l'en-tête, libellés courts. Le menu de gauche est limité à la rubrique active.
- Délais, glossaire, ressources, à propos et contact passent dans le pied de page.
- Nouvelle page d'entrée [docs/comprendre/README.md](docs/comprendre/README.md), à relire.
- `SUMMARY.md`, hérité de GitBook et publié comme page, est supprimé.
- Garde-fou [tests/test_nav.py](tests/test_nav.py).

**Référencement.**
- Avec un menu explicite, le sitemap de Zensical ne listait plus que les pages du menu. Il est désormais généré en dur par [scripts/build_sitemap.py](scripts/build_sitemap.py) (44 URL, appelé par `inject_git_dates.py`).
- `site_url` passe en `https` : les URL canoniques et le sitemap pointaient en `http`.
- Le fil d'Ariane `BreadcrumbList` est produit côté serveur avec les libellés du menu, et retiré de `schema.js`.
- Chaque page garde un seul H1, celui du Markdown, affiché dans le bandeau.

**Identité visuelle.**
- Palette Yale Blue, Carrot Orange, Bondi Blue, Yellow Green et Graphite. Les couleurs claires sont assombries pour le petit texte.
- Police Albert Sans, en remplacement libre de la police ES Allianz N de Noerr, sous licence commerciale.
- Gabarits : [header.html](overrides/partials/header.html), [footer.html](overrides/partials/footer.html), [main.html](overrides/main.html) (bandeau de page), [home.html](overrides/home.html) (accueil).

**Contenu.**
- Accueil réécrit : ouverture, colonne « À la une » générée, tuiles de situation, bandeau « Information générale ». Les sections délais et déroulé de la procédure ont été écartées à la demande de l'utilisateur.
- Tuiles numérotées en tête des pages d'entrée des rubriques faillis et créanciers.
- Les actualités liées passent de la liste repliable aux cartes. Les cartes affichent la date du texte commenté, à défaut celle de publication.

**Correction au passage.** [docs/delais.md](docs/delais.md) : l'ancre `#déclaration-de-créance` était cassée (Zensical produit `#declaration-de-creance`).

**Contrôles.**
- 38 tests au vert ; build sans erreur.
- 3 332 liens internes vérifiés : aucun cassé, hors les liens absolus de `404.html`, corrects une fois en ligne.
- Captures d'écran sans navigateur sur ordinateur et à 520 px.

---

## [2026-10-28] edit | Cautions : alignement du guide sur la loi du 5 juin 2025

Résout l'incohérence relevée à l'entrée « Six premières notes d'actualité ». **Correction factuelle** : le guide décrivait encore l'ancien régime (décharge réservée à la caution à titre gratuit, disproportion appréciée « au moment de la signature », extension de l'effacement au conjoint rattachée à XX.173 et conditionnée à six mois de cohabitation). Réécrit sur la base des notes [caution consommateur](docs/actualites/2026-10-28-caution-consommateur-loi-5-juin-2025.md) et [effacement et décharge pour le conjoint](docs/actualites/2026-10-28-effacement-decharge-caution-conjoint-partenaire.md).

- [docs/creanciers/suretes-cautions.md](docs/creanciers/suretes-cautions.md) — page de référence : décharge de la caution consommateur (XX.176 : disproportion à l'ouverture de la procédure, garant sans influence substantielle sur la société, sûretés personnelles seulement, requête au registre avec pièces, suspension des voies d'exécution) ; effacement du conjoint ou cohabitant légal coobligé (XX.174 et ses trois limites, C. const. 25 janvier 2024 et 24 septembre 2014) ; nouveau régime du Code civil (art. 9.1.42 à 9.1.50) avec les points de contrôle pour le créancier ; avertissement sur les dossiers antérieurs au 1er janvier 2026. Ancres explicites `#decharge-caution-consommateur`, `#conjoint-cohabitant-cooblige`, `#surete-consommateur-code-civil`.
- [docs/comprendre/cloture.md](docs/comprendre/cloture.md), [docs/faillis/effacement.md](docs/faillis/effacement.md), [docs/faillis/faq.md](docs/faillis/faq.md), [docs/faillis/checklist-premiere-semaine.md](docs/faillis/checklist-premiere-semaine.md), [docs/glossaire.md](docs/glossaire.md) — résumés alignés, renvoi vers la page de référence.

**Retiré, à confirmer par l'utilisateur** : le délai de « six mois suivant le jugement de clôture définitif » pour demander la décharge (suretes-cautions et clôture). Il ne figure pas dans les notes sources et paraît difficilement conciliable avec une requête déposée en cours de procédure qui suspend les voies d'exécution.

---

## [2026-10-28] ingest | Six premières notes d'actualité

Notes fournies par l'utilisateur, reprises sans modification de fond (mise en forme Markdown, front matter, thèmes) :

- [Sûreté personnelle constituée par un consommateur, loi du 5 juin 2025](docs/actualites/2026-10-28-caution-consommateur-loi-5-juin-2025.md) — législation ; thèmes caution, réorganisation judiciaire.
- [Fraude intragroupe avant faillite, Entr. fr. Bruxelles, 10 septembre 2025](docs/actualites/2026-10-28-fraude-intragroupe-inopposabilite-dirigeant.md) — XX.114 ; thèmes période suspecte, responsabilité des dirigeants, compensation.
- [Effacement et décharge de caution pour le conjoint ou le partenaire](docs/actualites/2026-10-28-effacement-decharge-caution-conjoint-partenaire.md) — doctrine, XX.174 et XX.176 ; thèmes effacement, caution.
- [Interdiction professionnelle et non bis in idem, Entr. Hainaut (Mons), 28 juillet 2026](docs/actualites/2026-10-28-interdiction-non-bis-in-idem-condamnation-penale.md) — XX.229 ; thème interdiction de gérer.
- [Dirigeant démissionnaire et faillites successives, Cass., 6 mars 2025](docs/actualites/2026-10-28-cassation-dirigeant-demissionnaire-faillites-successives.md) — XX.226 ; thèmes responsabilité des dirigeants, fisc et ONSS.
- [Compte courant de l'administrateur, Bruxelles, 8 janvier 2026](docs/actualites/2026-10-28-compte-courant-administrateur-integralite-passif.md) — XX.144 et XX.170 ; thèmes réalisation des actifs, curateur.

Blocs « Actualités liées » générés sur 10 pages du guide, encart de l'accueil alimenté.

**Incohérence relevée, non corrigée (en attente d'arbitrage).** Les notes 1 et 3 décrivent la décharge de la caution depuis le 1er janvier 2026 (critère du consommateur et de la disproportion, gratuité abandonnée ; effacement du conjoint fondé sur XX.174). Le guide décrit encore l'ancien régime : [docs/creanciers/suretes-cautions.md](docs/creanciers/suretes-cautions.md) (l. 62-68 et 90, « à titre gratuit »), [docs/comprendre/cloture.md](docs/comprendre/cloture.md) (l. 54-60), [docs/faillis/effacement.md](docs/faillis/effacement.md) (l. 57 et 68, extension au conjoint rattachée à XX.173), [docs/faillis/faq.md](docs/faillis/faq.md) (l. 47).

---

## [2026-10-28] config | Rubrique Actualités et maillage avec le guide

Nouvelle rubrique `/actualites/` pour publier des notes de jurisprudence, de doctrine et de législation, avec des renvois automatiques dans les deux sens entre les notes et les pages du guide. Maquette validée au préalable (liste, gabarit de note, page théorique avec renvois, page par thème).

**Architecture.** Zensical 0.0.24 n'a ni plugin blog ni plugin tags opérationnel : un générateur Python pré-build écrit dans les sources Markdown, entre les marqueurs `<!-- actualites:auto:start/end -->`, et ne touche jamais au texte rédigé.

- [data/themes.yml](data/themes.yml) : taxonomie de 30 notions, chacune rattachée à 1 ou 2 pages du guide (hors `docs/`, non publiée).
- [scripts/build_actualites.py](scripts/build_actualites.py) : valide les notes, régénère la liste ([docs/actualites/README.md](docs/actualites/README.md)), la page par thème ([docs/actualites/themes.md](docs/actualites/themes.md)), l'encart « Dernières actualités » de l'accueil, les renvois en fin de note et le bloc repliable « Actualités liées » en fin de chaque page du guide concernée (retiré quand plus aucune note ne s'y rapporte). Idempotent, mode `--check`.
- [scripts/new_actualite.py](scripts/new_actualite.py) : squelette d'une note.
- [overrides/main.html](overrides/main.html) : cartouche de la note (source, référence, lien, articles du CDE) et JSON-LD `Article` dans le HTML statique.
- [docs/stylesheets/extra.css](docs/stylesheets/extra.css), [docs/javascripts/actualites.js](docs/javascripts/actualites.js) : badges de type, filtres par type et par thème.
- [overrides/llms.txt](overrides/llms.txt) et [CLAUDE.md](CLAUDE.md) : rubrique et workflow de publication documentés.

**Contrainte découverte.** Zensical échoue au build (« failed to extract field Markdown.meta », sans nom de fichier) sur toute valeur YAML vide et toute date non quotée dans un front matter. Le squelette quote les dates et n'émet aucune valeur nulle ; le générateur détecte les deux cas et nomme le fichier.

Contrôle : 32 tests au vert ; build Zensical vérifié avec deux notes de démonstration temporaires (liste, cartouche, JSON-LD, ancres `#slug`, bloc sur `faillis/effacement`, encart d'accueil, sitemap), puis notes retirées : les pages du guide reviennent à l'identique. Aucune note réelle publiée à ce stade.

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

## 2026-09-02 17:34:26 - session 2a52abbe

**Demande :** Je confirme que la levée de l'interdiction ne peut pas se faire pour bonne conduite ou levée anticipative. Par contre en matière d'effacement, le refus d'effacement peut être peut faire l'objet d'une réhabilitation conformément aux dispositions du code de droit économique lorsque Le failli qui n'a p...

**Action :** Tout est en ordre. Arbre propre, build clean, 386 liens vérifiés sans erreur, dates à jour.  ## Vos deux points  **Levée d'interdiction** — vous confirmez `interdiction.md`, c'était donc `cloture.md` qui était fautif, en deux endroits. Corrigé et rattaché aux deux seules causes d'extinction anticipée : rétractation du jugement déclaratif et réhabilitation XX.237.  **Réhabilitation** — c'était un vrai trou. [effacement.md](docs/faillis/effacement.md) expliquait longuement comment l'effacement peu...

**Outils utilises :** aucun

---

## 2026-09-15 12:26:26 - session 2a52abbe

**Demande :** on peut pousser les commits

**Action :** Poussé. `928ca68..ff77d61`, local et remote synchronisés sur `ff77d61`, aucun écart.  Les 11 commits sont en ligne — le déploiement GitHub Actions se déclenche sur `gh-pages`. Je n'ai pas pu vérifier son état, le CLI `gh` n'étant pas installé ici ; à contrôler dans l'onglet Actions du dépôt si vous voulez confirmer la mise en ligne effective.  Ce qui part en production : la nouvelle page sur les dettes avant faillite, les renvois et la base légale XX.113 sur les FAQ, les six entrées de glossaire...

**Outils utilises :** aucun

---

## 2026-10-28 10:52:15 - session 4a7bde3d

**Demande :** Je voudrais mettre en place une page spécifique sur le site qui concerne des actualités et des articles de Sur le sujet, l'objectif est d'avoir un espace qui permet de recenser des. Euh des matières liées au droit de la faillite et de publier des actualités jurisprudentielles ou doctrinales. Dans ce...

**Action :** La maquette est en ligne, en accès privé : https://claude.ai/artifact/Q5aVSWRd6eyxYcDa1aHoks  Elle simule quatre écrans dans l'apparence actuelle du site. Tu passes de l'un à l'autre avec la barre du haut. Les encadrés orange en pointillés expliquent ce qui est généré automatiquement ; tu peux les masquer.  1. **Liste des actualités** : notes groupées par année, chacune avec son type (jurisprudence, doctrine, législation), sa source, un résumé et ses étiquettes. Des filtres par type et par thème...

**Outils utilises :** aucun

---

## 2026-10-28 11:06:02 - session 4a7bde3d

**Demande :** parfait, on peut continuer

**Action :** La rubrique Actualités est en place sur `gh-pages`, en quatre commits locaux. Je n'ai rien poussé.  **Ce qui fonctionne :** - **Taxonomie** : les 30 notions de la maquette sont dans [data/themes.yml](data/themes.yml), fichier hors de `docs/`, donc jamais publié. - **Générateur** : [scripts/build_actualites.py](scripts/build_actualites.py) écrit dans tes pages, mais uniquement entre des marqueurs ; ton texte rédigé n'est jamais touché. Il produit :   - la liste des notes et la page « par thème » ...

**Outils utilises :** aucun

---

## 2026-10-28 11:52:44 - session 4a7bde3d

**Demande :** voila une première note d'actualité

**Action :** Tes six notes sont en ligne en local, en deux commits sur `gh-pages`. Je n'ai rien poussé.  J'ai repris ton texte tel quel : seulement la mise en Markdown (intertitres, listes, référence finale en italique), l'en-tête de chaque note et ses thèmes.  | Note | Type | Thèmes | |---|---|---| | Caution consommateur, loi du 5 juin 2025 | législation | caution, réorganisation judiciaire | | Fraude intragroupe, Entr. fr. Bruxelles, 10 septembre 2025 | jurisprudence | période suspecte, responsabilité des ...

**Outils utilises :** aucun

---

## 2026-10-28 12:06:53 - session 4a7bde3d

**Demande :** parfait; mets à jour les fiches pour être cohérént avec le régime de cautionnement en prenant en compte la mise à jour législative.

**Action :** J'ai mis le guide en cohérence avec le nouveau régime des cautions, en trois commits sur `gh-pages`, non poussés. Le build passe, les nouvelles ancres et les liens qui y mènent fonctionnent, et l'ancienne formulation n'apparaît plus dans le guide.  **Page de référence : [suretes-cautions.md](docs/creanciers/suretes-cautions.md).** Trois sections réécrites ou créées : - **Décharge de la caution consommateur (XX.176)** :   - la disproportion s'apprécie désormais à l'ouverture de la procédure, plus...

**Outils utilises :** aucun

---

## 2026-10-28 12:12:21 - session 4a7bde3d

**Demande :** <ide_opened_file>The user opened the file c:\Users\FlorianErnotteavroya\infofaillite\docs\actualites\2026-10-28-caution-consommateur-loi-5-juin-2025.md in the IDE. This may or may not be related to the current task.</ide_opened_file>

**Action :** Tout est sur GitHub : `ff77d61..0868727` poussé sur `gh-pages`, qui est maintenant à jour avec le dépôt distant. Avant le push, j'ai commité les entrées de session que le hook avait ajoutées à [log.md](log.md).  Ce qui est parti : - la rubrique Actualités et son générateur ; - tes six notes ; - les renvois dans les deux sens entre les notes et les pages du guide ; - la mise à jour du régime des cautions sur six pages.  Je n'ai pas pu vérifier que le site est réellement mis en ligne, car le CLI `...

**Outils utilises :** aucun

---

## 2026-10-28 12:41:34 - session 4a7bde3d

**Demande :** Je voudrais que tu réalises un gros travail sur L'expérience d'utilisateur et de navigation sur le site internet. Aujourd'hui, je suis tributaire du format proposé par Sensical. Et la navigation se fait au travers d'un menu Déroulant sur la gauche Mais qui est beaucoup trop chargé à mon goût. Il fau...

**Action :** La maquette est en ligne, en accès privé : https://claude.ai/artifact/99cqWfgoz5yn5ZDxNLz5aq  Elle montre quatre écrans, que tu ouvres depuis la barre du haut :  1. **Accueil** : sans menu latéral. Quatre cartes, une par onglet, chacune avec trois ou quatre questions formulées comme on les tape dans Google ou comme on les pose à une IA, et qui renvoient vers les pages qui y répondent. Puis l'encadré du délai de 30 jours et la mention « À propos ». 2. **Entrée de rubrique** (« Je suis en faillite...

**Outils utilises :** aucun

---

## 2026-10-28 13:36:06 - session 4a7bde3d

**Demande :** rends l'interface plus moderne avec quelques touches de couleurs pour faire donner un effet professionel et et liée à un cabinet d'avocats

**Action :** J'ai mis à jour la maquette, à la même adresse : https://claude.ai/artifact/99cqWfgoz5yn5ZDxNLz5aq. Je ne l'ai pas regardée moi-même une fois rendue.  Elle porte maintenant l'identité propre au site que tu as choisie : - **Couleurs** : bleu encre pour la structure (en-tête, onglets, pied de page) et bordeaux en touches (onglet actif, page active dans le menu, alerte de délai, flèches des cartes, liseré au-dessus du pied de page). Fond blanc légèrement chaud. - **Typographie** : titres à empattem...

**Outils utilises :** aucun

---

## 2026-10-28 13:43:15 - session 4a7bde3d

**Demande :** utilise cette pallette de couleur :  <pasted_content id="701a"> Colors ~Carrot Orange #f18f01 Lively burst of golden-orange, refreshing and bold, reminiscent of fresh harvests and playful creativity. ~Bondi Blue #048ba8 Luminous aquatic blue dances with refracted sunlight and tropical energy, offeri...

**Action :** J'ai appliqué ta palette à la maquette, à la même adresse : https://claude.ai/artifact/99cqWfgoz5yn5ZDxNLz5aq. Je ne l'ai pas regardée moi-même une fois rendue.  Voici à quoi sert chaque couleur :  | Couleur | Usage | |---|---| | **Yale Blue** `#2e4057` | Structure : en-tête, onglets, bandeau d'accueil, pied de page, titres | | **Carrot Orange** `#f18f01` | Accent : onglet actif, page active dans le menu, alerte de délai, liseré du pied de page, carte « Je suis en faillite » | | **Bondi Blue** `...

**Outils utilises :** aucun

---

## 2026-10-28 13:45:09 - session 4a7bde3d

**Demande :** modifie la police : utilise celle qui est présente sur : https://www.noerr.com/

**Action :** La maquette utilise maintenant la police **Albert Sans**, à la même adresse : https://claude.ai/artifact/99cqWfgoz5yn5ZDxNLz5aq. Je ne l'ai pas regardée moi-même une fois rendue.  Je n'ai pas pu reprendre la police exacte de Noerr. Leur site utilise **ES Allianz N**, une police commerciale sous licence, liée à la police d'entreprise Allianz et distribuée par la fonderie Elsner+Flake. On ne peut pas la charger depuis leur site sans enfreindre la licence, et aucun service de polices libres ne la p...

**Outils utilises :** aucun

---

## 2026-10-28 13:48:54 - session 4a7bde3d

**Demande :** repense la présentation en t'inspirant de noer afin une layout moderne et  plus dynamique

**Action :** J'ai refondu la maquette sur le modèle de Noerr, à la même adresse : https://claude.ai/artifact/99cqWfgoz5yn5ZDxNLz5aq. Je ne l'ai pas regardée moi-même une fois rendue.  **Ce qui change par rapport à la version précédente :** - **En-tête blanc** : le nom du site (« info·faillite », avec le point en orange), puis les quatre rubriques directement dans la barre, la rubrique active soulignée en orange, et la recherche. Il n'y a plus de barre d'onglets séparée. - **Accueil** :   - une grande accroch...

**Outils utilises :** aucun

---
