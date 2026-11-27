# Dépôt : matière première des actualités

Ce dossier reçoit les documents qui serviront de base à une note d'actualité : décision, texte légal, statistique, courriel, article, présentation. Rien n'y est publié, et seul ce README est versionné (le reste est ignoré par Git : textes de tiers, correspondance).

## Déposer

- Placer le ou les fichiers à la racine de `depot/`.
- Facultatif : un fichier `.md` ou `.txt` du même nom avec des consignes (angle, public visé, date souhaitée, points à souligner).

## Traiter

Demander à Claude de « traiter le dépôt ». La procédure est décrite dans `CLAUDE.md` (section « Dépôt : matière première des actualités ») : lecture, croisement avec les notes et pages existantes, rédaction de la note, corrections éventuelles du site, puis rangement de la source.

## Après traitement

La source est rangée dans `traite/AAAA-MM-JJ-slug/`, sous le nom de la note qu'elle a produite. Un fichier présent à la racine de `depot/` n'a donc pas encore été traité.
