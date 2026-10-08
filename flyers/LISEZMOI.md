# Flyers Remis à Neuf — A5 recto/verso

## Fichiers

| Fichier | Usage |
|---|---|
| `flyer-A5-impression.pdf` | **À envoyer à l'imprimeur.** 154 × 216 mm, fonds perdus 3 mm, traits de coupe |
| `flyer-A5-apercu.pdf` | 148 × 210 mm net, sans repères. Pour relire ou faire valider |
| `apercu-recto.png` / `apercu-verso.png` | Rendus 150 dpi, pour un envoi rapide par message |
| `build_flyers.py` | Le générateur. Relancer après toute modification |

## Spécifications techniques

- **Format fini** : A5, 148 × 210 mm, portrait
- **Fonds perdus** : 3 mm sur les quatre côtés
- **Zone de sécurité** : 14 mm de marge, aucun texte n'en sort
- **Images** : 1850 px pour 154 mm, soit 305 dpi
- **Polices** : Manrope, incorporée au PDF en sous-ensemble (licence OFL, redistribution autorisée)
- **Texte** : vectoriel, pas de pixellisation à l'agrandissement
- **Espace colorimétrique** : RVB

Sur le dernier point : les imprimeurs en ligne acceptent les PDF RVB et font eux-mêmes la conversion. Si le vôtre exige du CMJN avec un profil précis, demandez-lui le profil et faites faire la conversion par ses soins, ou dites-le-moi.

## Avant d'imprimer

Trois éléments sont encore des réservations visibles dans le fichier :

1. `[ TÉLÉPHONE À RENSEIGNER ]` au verso
2. `[ EMAIL À RENSEIGNER ]` au verso
3. L'adresse du site, actuellement l'adresse technique provisoire `amazing-sable-e931e5.netlify.app`, qui apparaît en bas du recto **et dans le QR code**

Le QR code pointe vers le formulaire de devis du site. Scannez-le une fois avec un téléphone pour vérifier qu'il ouvre bien la bonne page avant de lancer le tirage.

## Mettre à jour les coordonnées

Ouvrir `build_flyers.py`, modifier le dictionnaire en haut du fichier :

```python
CONTACT = {
    "telephone": "04 00 00 00 00",
    "email": "contact@remisaneuf.fr",
    "site": "remisaneuf.fr",
}
```

Puis régénérer :

```bash
python flyers/build_flyers.py
```

Le QR code se régénère séparément si l'adresse du site change : il est produit dans `assets/qr.png` à partir de l'URL du formulaire de devis.

## Visuels

Les deux photographies sont des images d'illustration temporaires, de même provenance que celles du site (voir `IMAGES.md` à la racine du dépôt). Elles ne représentent pas de chantiers réalisés par Remis à Neuf et devront être remplacées par de vraies photographies de réalisations.
