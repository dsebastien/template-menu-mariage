# Dépannage

## Dépendances manquantes

```text
✗ Dépendances Python manquantes : PyYAML PyMuPDF
```

Installez-les avec `pip install -r requirements.txt`.

## Chrome introuvable

Installez Google Chrome ou Chromium, ou précisez son chemin :

```bash
CHROME=/chemin/vers/chrome ./construire.sh
```

## Le menu produit plusieurs pages

Le contenu dépasse la carte de 120 × 180 mm. Raccourcissez les descriptions ou
réduisez légèrement `reglages.polices.taille_pt` dans `menu.yaml`.

## Deux menus ne tiennent pas sur l'A4

Le format réglé dans `reglages.page` est trop grand. Pour obtenir deux cartes
droites sur une A4 paysage, la largeur ne peut pas dépasser 132 mm et la
hauteur 196 mm, marges de coupe comprises.

## Le format imprimé est faux

Dans la boîte de dialogue d'impression, sélectionnez « taille réelle » ou
100 % et désactivez « ajuster à la page ». Mesurez une feuille d'essai avant
de lancer toute la série.

## Erreur dans menu.yaml

Le message indique le champ à corriger. Les causes habituelles sont une
tabulation, une indentation irrégulière ou un `:` non protégé. Dans ce dernier
cas, mettez tout le texte entre guillemets :

```yaml
nom: "Le Cochon qui voulait être Roi :"
```

## Polices Type3

Une police variable a probablement été ajoutée. Remettez les fichiers fournis
dans `polices/` ou utilisez des instances statiques, un fichier par graisse.
