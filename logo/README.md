# Logo info·faillite

Ce dossier rassemble le logo d'infofaillite.be dans toutes ses variantes. Il est à la racine du dépôt, hors de `docs/`, et n'est donc pas publié sur le site. Les quelques fichiers utilisés par le site (favicon, image de partage) sont copiés dans `docs/assets/`.

## Construction

Le logo est un logotype : « info·faillite » en **Albert Sans ExtraBold (800)**, avec un espacement de −0,03 em. Le point médian est la seule touche de couleur. Il reprend exactement le logo en texte de l'en-tête du site (`.ifa-brand` dans `docs/stylesheets/extra.css`).

Tous les SVG sont vectorisés : le texte est converti en tracés. Ils s'affichent donc correctement sans que la police soit installée.

| Couleur | Hex | Rôle |
|---|---|---|
| Yale Blue | `#2e4057` | texte du logo, fond du monogramme |
| Carrot Orange | `#f18f01` | point médian |
| Graphite | `#2f2d2e` | ligne de base de la signature (version couleur) |
| Blanc | `#ffffff` | texte sur fond sombre |

La police Albert Sans est sous licence SIL Open Font License : usage libre, y compris commercial.

## Variantes

**Logotype** (`svg/logotype-*.svg`) : la version de référence, à utiliser partout où la place le permet.

| Fichier | Usage |
|---|---|
| `logotype-couleur` | fonds blancs ou clairs (version principale) |
| `logotype-inverse` | fonds sombres, notamment Yale Blue |
| `logotype-yale` | une seule couleur, fonds clairs |
| `logotype-noir` | impression noir et blanc, tampon, fax |
| `logotype-blanc` | fonds photographiques ou colorés |

**Signature** (`svg/signature-*.svg`) : le logotype accompagné de la ligne « GUIDE DE LA FAILLITE EN BELGIQUE », justifiée sur la largeur du mot. Elle sert quand le logo apparaît sans contexte : présentation, document imprimé, en-tête de courrier. Variantes : `couleur`, `inverse`, `noir`, `blanc`.

**Monogramme** (`svg/monogramme-*.svg`) : « i·f », pour les petits formats carrés (icône, avatar). Variantes : fond `yale` (référence), fond `orange`, fond `blanc`, `transparent`, et `yale-rond` pour les profils de réseaux sociaux.

## Formats prêts à l'emploi

- `png/` : chaque variante en PNG transparent. Les logotypes et les signatures existent en 400, 800 et 1600 px de large, les monogrammes en 512 et 1024 px.
- `favicon/` :
  - `favicon.svg` et `favicon.ico` (16, 32 et 48 px) ;
  - `icon-16/32/48/192/512.png` ;
  - `apple-touch-icon.png` (180 px, fond plein, pour l'écran d'accueil iOS).
- `reseaux/` :
  - `og-image-1200x630.png`, la vignette affichée quand une page est partagée sur LinkedIn, Facebook, une messagerie, etc. Sa source est `og-image.svg`.
  - `avatar-400.png`, le monogramme rond pour une photo de profil.

## Règles d'usage

- Garder autour du logo un espace libre au moins égal à la hauteur du « f ».
- Ne pas déformer, incliner ni changer la couleur du point médian en dehors des variantes prévues.
- En dessous de 120 px de large, utiliser le monogramme plutôt que le logotype.

## Régénérer

Le script `make_logo.py` produit l'ensemble du dossier. Il a besoin de :

- `uharfbuzz`, `Pillow` ;
- la police variable Albert Sans, à télécharger depuis Google Fonts (`AlbertSans[wght].ttf`) ;
- Google Chrome, pour le rendu des PNG.

```
pip install uharfbuzz pillow
python logo/make_logo.py chemin/AlbertSans[wght].ttf logo chemin/dossier-temporaire
```

Le script recrée les sous-dossiers `svg/`, `png/`, `favicon/` et `reseaux/` ; le README et le script restent intacts. Après une régénération, recopier dans `docs/assets/` les fichiers `favicon.svg`, `favicon.ico`, `apple-touch-icon.png` et `icon-512.png`, ainsi que `reseaux/og-image-1200x630.png` sous le nom `og-image.png`.
