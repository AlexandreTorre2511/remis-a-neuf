# Origine des visuels

## Logo

`logo-mark.png`, `logo-mark-white.png`, `logo-full.png`, `logo-full-white.png`,
`favicon-32.png`, `favicon-180.png` sont dérivés des fichiers de logo fournis :
monogramme détouré, fond rendu transparent, version blanche générée pour les
fonds sombres. Aucun élément du logo n’a été redessiné.

## Photographies — statut

> **Toutes les photographies du site sont des visuels d’illustration temporaires.**
> Aucune ne représente un chantier réalisé par Remis à Neuf. Elles sont là pour
> valider la direction artistique et devront être remplacées par les
> photographies des projets réels.

Elles proviennent d’Unsplash (`images.unsplash.com`), dont la licence autorise
l’usage commercial sans attribution obligatoire. Avant la mise en production,
il est recommandé de vérifier la page de chaque photo sur unsplash.com, ou plus
simplement de les remplacer par les clichés de l’entreprise.

Les pastilles « Visuel d’illustration » / « Visuels de démonstration » affichées
sur la page devront être retirées en même temps que les images.

## Correspondance fichier → source

| Fichier | Contenu | Source |
|---|---|---|
| `hero-main.jpg` (+ `-600`) | Séjour ouvert, hero | `images.unsplash.com/photo-1750764515068-80d222d974bb` |
| `hero-sub.jpg` | Cuisine claire, vignette hero | `images.unsplash.com/photo-1643949915134-73a4c880f7c7` |
| `og-image.jpg` | Aperçu réseaux sociaux | même source que `hero-main.jpg` |
| `approche-01.jpg` | « Préparer » | `images.unsplash.com/photo-1692133220749-1c55bb918ad8` |
| `approche-02.jpg` | « Transformer » | `images.unsplash.com/photo-1689043528099-2ba014dd7c64` |
| `approche-03.jpg` | « Finaliser » | `images.unsplash.com/photo-1717416697589-d0881869fc46` |
| `real-01.jpg` (+ `-700`) | Appartement contemporain | `images.unsplash.com/photo-1745429523615-2a82c60bfc02` |
| `real-02.jpg` | Salon | `images.unsplash.com/photo-1745429523617-0d837856ca35` |
| `real-03.jpg` | Cuisine | `images.unsplash.com/photo-1758565811352-a439bd6f956e` |
| `real-04.jpg` (+ `-700`) | Salle de bains | `images.unsplash.com/photo-1744025098626-66c0b9cb1ba8` |
| `real-05.jpg` (+ `-700`) | Chambre | `images.unsplash.com/photo-1750764700420-4dc267342dbe` |
| `real-06.jpg` | Détail de finition | `images.unsplash.com/photo-1585128792020-803d29415281` |
| `avant.jpg` (+ `-800`) | Comparateur — avant | `images.unsplash.com/photo-1757742690834-aa581b9f53b2` |
| `apres.jpg` (+ `-800`) | Comparateur — après | `images.unsplash.com/photo-1750764611091-93ac9e7d4c92` |

## Format des remplacements

Pour conserver la mise en page sans retoucher le CSS, respecter les ratios :

| Emplacement | Ratio | Taille conseillée |
|---|---|---|
| `hero-main` | 4:5 | 1200 × 1500 |
| `hero-sub` | 3:2 | 760 × 507 |
| `approche-01 / 02 / 03` | 4:5 | 800 × 1000 |
| `real-01` | 4:3 | 1400 × 1050 |
| `real-02`, `real-03` | 3:4 | 900 × 1200 |
| `real-04`, `real-05` | 3:2 | 1400 × 933 |
| `real-06` | 1:1 | 900 × 900 |
| `avant`, `apres` | 16:10 | 1600 × 1000 |

Les variantes suffixées (`-600`, `-700`, `-800`) alimentent les attributs
`srcset` : les régénérer à la même échelle, ou retirer l’attribut `srcset` de la
balise concernée si une seule taille est fournie.

**Important** : pour le comparateur avant / après, les deux photographies
doivent montrer **la même pièce, depuis le même point de vue**, sous peine de
perdre tout l’intérêt de la comparaison.
