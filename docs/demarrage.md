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

Sous Windows, utilisez PowerShell et le script `construire.ps1`. Il trouve
Chrome, Chromium ou, à défaut, Microsoft Edge. Pour imposer un navigateur :

```powershell
$env:CHROME = "C:\chemin\vers\chrome.exe"
.\construire.ps1
```

Si PowerShell refuse de lancer le script, autorisez les scripts locaux une
fois pour toutes :

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Créer les PDF

À la racine du projet, lancez :

```bash
./construire.sh
```

ou, sous Windows :

```powershell
.\construire.ps1
```

Vous obtenez :

- `Menu de mariage - 12x18 cm.pdf`, une carte de 120 × 180 mm ;
- `Menu de mariage - A4 - 2 exemplaires.pdf`, deux cartes sur une A4 paysage.

Pour écrire les fichiers dans un autre dossier :

```bash
./construire.sh exemple
```

```powershell
.\construire.ps1 exemple
```

Modifiez ensuite uniquement `menu.yaml`. Le dossier `build/` contient des
intermédiaires qui seront écrasés à la prochaine construction.
