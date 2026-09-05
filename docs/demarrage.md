# Démarrage

## Prérequis

Installez Python 3.9 ou plus, puis les deux dépendances du projet :

```bash
pip install -r requirements.txt
```

Google Chrome ou Chromium doit aussi être installé. Le script le détecte
automatiquement. Si nécessaire, indiquez son chemin :

```bash
CHROME=/chemin/vers/chrome ./construire.sh
```

## Créer les PDF

À la racine du projet, lancez :

```bash
./construire.sh
```

Vous obtenez :

- `Menu de mariage - 12x18 cm.pdf`, une carte de 120 × 180 mm ;
- `Menu de mariage - A4 - 2 exemplaires.pdf`, deux cartes sur une A4 paysage.

Pour écrire les fichiers dans un autre dossier :

```bash
./construire.sh exemple
```

Modifiez ensuite uniquement `menu.yaml`. Le dossier `build/` contient des
intermédiaires qui seront écrasés à la prochaine construction.
