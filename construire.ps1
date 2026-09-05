# Construit le menu individuel et une planche A4 de deux exemplaires (Windows).
# Équivalent PowerShell de construire.sh.
#
# Usage :  .\construire.ps1              -> PDF à la racine du projet
#          .\construire.ps1 exemple      -> PDF dans le dossier exemple\
#          $env:CHROME = "C:\chemin\chrome.exe" ; .\construire.ps1
param(
    [string]$Destination = ""
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"   # évite les erreurs d'affichage des caractères ✓ ✗ →

$Ici = $PSScriptRoot
if ($Destination -eq "") { $Destination = $Ici }
elseif (-not [System.IO.Path]::IsPathRooted($Destination)) {
    $Destination = Join-Path $Ici $Destination
}

$NomMenu = "Menu de mariage - 12x18 cm.pdf"
$NomPlanche = "Menu de mariage - A4 - 2 exemplaires.pdf"

function Echec($message, $conseil) {
    Write-Host "  ✗ $message" -ForegroundColor Red
    if ($conseil) { Write-Host "    $conseil" }
    exit 1
}

# --- Python ------------------------------------------------------------------
$Python = $null
foreach ($candidat in @("python", "python3", "py")) {
    $commande = Get-Command $candidat -ErrorAction SilentlyContinue
    if (-not $commande) { continue }
    & $commande.Source -c "import sys" 2>$null
    if ($LASTEXITCODE -eq 0) { $Python = $commande.Source; break }
}
if (-not $Python) {
    Echec "Python est introuvable." "Installez Python 3.9 ou plus depuis https://www.python.org/downloads/ en cochant « Add python.exe to PATH »."
}

$manque = @()
& $Python -c "import yaml" 2>$null
if ($LASTEXITCODE -ne 0) { $manque += "PyYAML" }
& $Python -c "import pymupdf" 2>$null
if ($LASTEXITCODE -ne 0) { $manque += "PyMuPDF" }
if ($manque.Count -gt 0) {
    Echec "Dépendances Python manquantes : $($manque -join ', ')" "Installez-les : pip install -r requirements.txt"
}

# --- Chrome ------------------------------------------------------------------
$Chrome = $env:CHROME
if (-not $Chrome) {
    $candidats = @()
    foreach ($cle in @(
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe",
        "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe")) {
        try { $candidats += (Get-ItemProperty $cle -ErrorAction Stop).'(default)' } catch {}
    }
    $candidats += @(
        "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
        "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
        "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
        "$env:LOCALAPPDATA\Chromium\Application\chrome.exe",
        "$env:ProgramFiles\Chromium\Application\chrome.exe",
        "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
        "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
    )
    foreach ($candidat in $candidats) {
        if ($candidat -and (Test-Path $candidat)) { $Chrome = $candidat; break }
    }
}
if (-not $Chrome -or -not (Test-Path $Chrome)) {
    Echec "Chrome, Chromium ou Edge est introuvable." "Installez Google Chrome, ou indiquez son chemin : `$env:CHROME = 'C:\chemin\vers\chrome.exe' ; .\construire.ps1"
}

# --- Construction ------------------------------------------------------------
Set-Location $Ici
New-Item -ItemType Directory -Force "build" | Out-Null
New-Item -ItemType Directory -Force $Destination | Out-Null

function Etape($nom, [scriptblock]$action) {
    Write-Host "→ $nom"
    & $action
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Etape "lecture de menu.yaml" { & $Python moteur\contenu.py }
Etape "composition du menu" { & $Python moteur\composer.py }

Write-Host "→ rendu du menu 12 × 18 cm"
$PdfMenu = Join-Path $Ici "build\menu-12x18.pdf"
$PdfPlanche = Join-Path $Ici "build\menu-a4-2-exemplaires.pdf"
Remove-Item $PdfMenu -Force -ErrorAction SilentlyContinue
$Html = (Join-Path $Ici "build\menu.html") -replace '\\', '/'
& $Chrome --headless=new --disable-gpu --no-sandbox --no-pdf-header-footer `
    --user-data-dir="$Ici\build\chrome-profile" `
    --run-all-compositor-stages-before-draw --virtual-time-budget=15000 `
    --print-to-pdf="$PdfMenu" "file:///$Html" 2>$null | Out-Null
if (-not (Test-Path $PdfMenu)) {
    Echec "Chrome n'a pas produit le PDF du menu." "Vérifiez que $Chrome se lance correctement."
}

Write-Host "→ placement de 2 exemplaires sur A4"
$sortie = & $Python moteur\imposer.py $PdfMenu $PdfPlanche
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
if ($sortie) { Write-Host ($sortie | Select-Object -First 1) }

Write-Host "→ copie vers $Destination"
Copy-Item $PdfMenu (Join-Path $Destination $NomMenu) -Force
Copy-Item $PdfPlanche (Join-Path $Destination $NomPlanche) -Force

Etape "vérification des fichiers produits" {
    & $Python moteur\verifier.py (Join-Path $Destination $NomMenu) (Join-Path $Destination $NomPlanche)
}

Write-Host "✓ fichiers prêts :"
Write-Host "   $(Join-Path $Destination $NomMenu)"
Write-Host "   $(Join-Path $Destination $NomPlanche)"
