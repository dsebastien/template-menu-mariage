# Régénère les PDF d'exemple et leurs aperçus dans la documentation (Windows).
# Équivalent PowerShell de regenerer-exemple.sh.
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"

Set-Location $PSScriptRoot

& (Join-Path $PSScriptRoot "construire.ps1") exemple
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$Python = (Get-Command python, python3, py -ErrorAction SilentlyContinue | Select-Object -First 1).Source

Write-Host "→ images de la documentation"
$script = @'
import os
import pymupdf

os.makedirs("docs/images", exist_ok=True)

fichiers = (
    ("exemple/Menu de mariage - 12x18 cm.pdf", "docs/images/exemple-menu.png", 180),
    ("exemple/Menu de mariage - A4 - 2 exemplaires.pdf",
     "docs/images/exemple-planche-a4.png", 130),
)
for source, destination, resolution in fichiers:
    document = pymupdf.open(source)
    document[0].get_pixmap(dpi=resolution, alpha=False).save(destination)
    print(f"   {destination}")
'@
$script | & $Python -
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "✓ exemple\ et docs\images\ régénérés"
