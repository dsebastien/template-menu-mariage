# Agent Instructions

Ce projet utilise `bd` pour le suivi des tâches. Exécuter `bd onboard` au début
d'une session. À la fin : tests, mise à jour de la tâche, synchronisation,
commit et `git push`. Le travail n'est terminé que lorsque le dépôt distant est
à jour.

# Template de menu de mariage

L'utilisateur écrit en français : répondre en français. La cible n'est pas un
développeur ; les erreurs doivent expliquer quoi corriger et où.

Un utilisateur modifie `menu.yaml`, lance `./construire.sh` et obtient :

- une carte de menu de 120 × 180 mm ;
- une planche A4 paysage avec deux exemplaires à taille réelle et repères de coupe.

## Construire

```bash
pip install -r requirements.txt
./construire.sh
./construire.sh exemple
./regenerer-exemple.sh
```

Chrome ou Chromium sert au rendu. `CHROME=/chemin ./construire.sh` permet de
préciser l'exécutable.

## Chaîne

```text
menu.yaml → moteur/contenu.py → moteur/composer.py → build/menu.html
          → Chrome → build/menu-12x18.pdf
          → moteur/imposer.py → build/menu-a4-2-exemplaires.pdf
          → moteur/verifier.py
```

`build/` contient uniquement des intermédiaires régénérés.

## Invariants

1. Le menu individuel contient exactement une page au format configuré.
2. La planche contient deux exemplaires sans changement d'échelle sur A4.
3. Les polices du PDF sont Type0, jamais Type3.
4. Aucune encre du menu fini ne passe à moins de 8 mm du bord.
5. Tout texte visible passe par `fr()` dans `moteur/contenu.py`.
6. `menu.yaml` reste la seule interface nécessaire à l'utilisateur.

## Conventions

- Code, commentaires et messages en français.
- Champs YAML en français.
- Exceptions `ErreurContenu` formulées pour l'utilisateur final.
- Conserver les polices statiques ; les polices variables produisent souvent du Type3.
- Après une modification visuelle, exécuter `./regenerer-exemple.sh`.

Le contenu de `menu.yaml` est un exemple humoristique. Il peut être remplacé,
mais ne doit contenir aucune donnée personnelle réelle.
