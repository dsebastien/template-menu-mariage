# Personnalisation

Tous les réglages se trouvent à la fin de `menu.yaml`.

## Format

```yaml
page:
  largeur_mm: 120
  hauteur_mm: 180
```

Le format 120 × 180 mm permet de placer deux cartes droites sur une A4 paysage.
Si vous l'agrandissez trop, la création de la planche A4 sera refusée plutôt
que de réduire silencieusement les cartes.

## Cadre

```yaml
cadre:
  retrait_mm: 9
  epaisseur_pt: 2
```

`retrait_mm` doit rester au moins égal à 8 mm pour préserver une zone de coupe
sûre. `epaisseur_pt` règle l'épaisseur du cadre.

## Polices

```yaml
polices:
  dossier: polices
  texte: EB Garamond
  titres: Cormorant Garamond
  taille_pt: 9
```

Les polices fournies sont des fichiers statiques correctement intégrés au PDF.
Si vous les remplacez, utilisez un fichier `.ttf` ou `.otf` par graisse ; les
polices variables peuvent produire un PDF Type3 mal géré en imprimerie.

## Couleurs

```yaml
couleurs:
  encre: "#4b413a"
  accent: "#A24F3D"       # terracotta
  decoration: "#A24F3D"   # cadre et petits motifs
```

`encre` colore le texte, `accent` les titres et `decoration` le cadre ainsi que
les petits motifs. Utilisez des couleurs assez foncées pour rester lisibles sur
papier.
