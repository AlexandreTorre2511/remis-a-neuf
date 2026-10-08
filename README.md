# Remis à Neuf — site web

Site vitrine de **Remis à Neuf**, entreprise de rénovation d’appartements tous corps d’état
à Nice et sur la Côte d’Azur.

HTML sémantique + CSS moderne + JavaScript natif, sans build ni dépendance.
Le site s’ouvre directement dans un navigateur et se déploie sur n’importe quel
hébergeur statique (Netlify, Vercel, OVH, o2switch, GitHub Pages…).

---

## 1. Arborescence

```
.
├── site/                           Racine publiée (publish directory Netlify)
│   ├── index.html                  Page d’accueil (toutes les sections)
│   ├── mentions-legales.html       Trame à compléter
│   ├── politique-confidentialite.html
│   └── assets/
│       ├── css/style.css           Design system complet, commenté par section
│       ├── js/main.js              Header, menu, accordéon, comparateur, formulaire
│       └── img/                    Logo, favicons, photographies
├── netlify.toml                    Configuration de déploiement et en-têtes HTTP
├── IMAGES.md                       Origine de chaque visuel
└── README.md
```

Seul le dossier `site/` est publié : la documentation reste à la racine du dépôt
et n’est pas servie par le site en ligne.

## 2. Lancer le site en local

```bash
python -m http.server 4321 --directory site
```

Puis ouvrir <http://localhost:4321>. (Un simple double-clic sur
`site/index.html` fonctionne également.)

## 2 bis. Déploiement

Hébergement prévu : **Netlify**, branche `main`, sans étape de build.

- `publish = "site"` et `command = ""` sont déjà définis dans `netlify.toml`
- chaque `git push` sur `main` déclenche une mise en ligne automatique
- les autres branches et les pull requests génèrent des aperçus (deploy previews)

Les en-têtes de sécurité et la politique de cache sont également décrits dans
`netlify.toml`. Les fichiers CSS et JS n’ayant pas de nom versionné, leur cache
est volontairement court (1 h) ; les images, elles, sont mises en cache un an et
doivent donc être remplacées par un **nouveau nom de fichier** plutôt que
modifiées en place.

---

## 3. Ce qu’il reste à renseigner

Tous les éléments manquants sont signalés dans la page par une pastille sable
« à renseigner ». Ils sont volontairement visibles pour ne rien laisser passer.

| Élément | Où | Remarque |
|---|---|---|
| Téléphone, email | `index.html` → section `#devis` et footer | Remplacer les `<span class="ph">…</span>` par les coordonnées |
| Prix au m² | `index.html` → section `#tarification` | Le bloc `.quote__val` affiche `—` tant qu’aucune fourchette n’est validée |
| Photos de chantiers | `assets/img/real-*.jpg`, `avant.jpg`, `apres.jpg` | Voir `IMAGES.md` ; supprimer ensuite les pastilles « Visuel d’illustration » |
| Références projets | `index.html` → `.gcard__m` | Remplacer « Projet à documenter » par « Rénovation complète — 78 m² », etc. |
| Mentions légales | `mentions-legales.html` | SIRET, assurances, hébergeur, directeur de publication |
| Politique de confidentialité | `politique-confidentialite.html` | Durées de conservation, sous-traitants |
| Fiche schema.org | `index.html` → `<script type="application/ld+json">` | Ajouter `telephone`, `address`, `openingHours` dès qu’ils sont connus |
| Domaine | balises `canonical`, `og:url`, `og:image` | Actuellement `https://www.remisaneuf.fr/` — à ajuster |

### Branchement du formulaire

Le formulaire est prêt à être connecté. Un seul point d’entrée :

```html
<form class="form" id="form-devis" data-endpoint="https://…">
```

- `data-endpoint` **vide** : mode recette — la soumission est journalisée dans la
  console du navigateur et le message de confirmation s’affiche. Rien n’est envoyé.
- `data-endpoint` **renseigné** : le formulaire envoie un `POST` en `FormData`
  (donc avec les photos). Compatible tel quel avec Formspree, Basin, Web3Forms,
  Brevo, HubSpot Forms ou une API interne.

Pour un envoi en JSON ou un passage par un CRM, la fonction `sendLead()` dans
`assets/js/main.js` (section 6) est le seul endroit à modifier.

---

## 4. Direction artistique

| Jeton | Valeur | Usage |
|---|---|---|
| `--ink` | `#171918` | Texte, fonds sombres, boutons principaux |
| `--sand` | `#C9B08A` | Accents, numéros, filets, soulignement du titre |
| `--sand-deep` | `#A88F69` | Accent sur fond clair (contraste AA) |
| `--paper` | `#FAF8F5` | Sections alternées |
| `--white` | `#FFFFFF` | Fond principal |

**Typographie** : `Avenir Next` si installée localement, sinon `Manrope`
(Google Fonts), sinon `Inter`. Les graisses utilisées sont 400 / 500 / 600 / 700.

**Logo** : extrait des fichiers fournis, détouré sur fond transparent.
- `logo-mark.png` — monogramme charbon + sable (fonds clairs)
- `logo-mark-white.png` — monogramme blanc (fonds sombres)
- `logo-full.png` / `logo-full-white.png` — monogramme + mot-symbole

Le nom s’écrit toujours **Remis à Neuf** — accent sur le `à`, majuscule au `N`,
sans baseline accolée au logo.

---

## 5. Composants réutilisables

Le CSS est découpé en blocs numérotés et commentés, chacun correspondant à un
composant autonome : `.btn`, `.eyebrow`, `.shead`, `.step`, `.trade`, `.quote`,
`.gcard`, `.mstep`, `.ba`, `.acc`, `.form`, `.ftr`, `.ph`.

La classe `.ph` matérialise un contenu à remplacer : elle rend l’élément
immédiatement repérable sur toutes les pages.

Les animations sont déclenchées par la classe `.rv` (apparition au scroll) et
les variantes de délai `.rv-d1` à `.rv-d4`. Elles sont neutralisées
automatiquement si le visiteur a activé « réduire les animations ».

---

## 6. Accessibilité et performance

- HTML sémantique, un seul `<h1>`, hiérarchie `h2` / `h3` respectée
- Lien d’évitement, navigation clavier complète (accordéon, comparateur, menu)
- `aria-expanded` / `aria-hidden` sur les composants interactifs
- Attributs `width` / `height` sur toutes les images (pas de décalage au chargement)
- `loading="lazy"` hors du premier écran, `srcset` sur les grands visuels
- `prefers-reduced-motion` et styles d’impression pris en charge
- Aucune bibliothèque externe : seules les polices Google sont chargées à distance
  (elles peuvent être auto-hébergées si une note RGPD stricte est souhaitée)

---

## 7. SEO local

Travaillé naturellement dans les contenus, sans sur-optimisation :
rénovation d’appartement Nice · rénovation appartement Côte d’Azur ·
entreprise de rénovation Nice · rénovation tous corps d’état Nice ·
rénovation appartement Alpes-Maritimes · rénovation complète appartement Nice.

Avant mise en ligne : ajouter `sitemap.xml` et `robots.txt`, créer la fiche
Google Business Profile, puis compléter le bloc `schema.org`.
