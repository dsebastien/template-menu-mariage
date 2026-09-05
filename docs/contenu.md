# Contenu du menu

Tout le contenu se trouve dans `menu.yaml`. L'indentation YAML se fait avec des
espaces, jamais avec des tabulations.

## Informations réutilisables

Le groupe `informations` est facultatif :

```yaml
informations:
  prenoms: Aurelia & Marcus
  date: 1er janvier 2030
```

Chaque valeur devient un marqueur utilisable ailleurs :

```yaml
menu:
  titre: Menu
  sous_titre: "{prenoms} · {date}"
```

`sous_titre` est facultatif. Supprimez-le ou laissez-le commenté pour ne rien
afficher sous « Menu ».

## Plats

`plats` est une liste. Chaque plat possède un `titre` obligatoire et peut
contenir un `nom`, une `description` et une `note` :

```yaml
plats:
  - titre: L'entrée
    nom: "Quand le Cochon rencontre le Volatile :"
    description: >
      Le Foie Gras accompagné de caille, de brioche et d'ananas vanillé.

  - titre: La pause glacée
    description: Sorbet citron givré
    note: Intermède glacé pour vous donner l'illusion d'être raisonnable
```

Le signe `>` permet d'écrire un long texte sur plusieurs lignes dans le
fichier sans créer de retours à la ligne dans le menu.

Pour ajouter, déplacer ou supprimer un service, manipulez un bloc complet
commençant par `- titre:`. Le moteur répartit automatiquement les espaces.

## Mot de fin

Les deux lignes sont facultatives :

```yaml
conclusion:
  message: Merci d'être à nos côtés !
  note: En cas de coma digestif, desserrez la ceinture d'un cran.
```

## Typographie automatique

Tous les textes sont normalisés : apostrophes courbes, ligatures comme `œ`,
espaces insécables avant `: ; ! ? % €` et tirets demi-cadratins. Vous pouvez
écrire naturellement ; le PDF reçoit la forme typographique correcte.
