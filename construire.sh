#!/usr/bin/env bash
# Construit le menu individuel et une planche A4 de deux exemplaires.
set -euo pipefail

ICI="$(cd "$(dirname "$0")" && pwd)"
DEST="${1:-$ICI}"
[ "${DEST#/}" = "$DEST" ] && DEST="$ICI/$DEST"

NOM_MENU="Menu de mariage - 12x18 cm.pdf"
NOM_PLANCHE="Menu de mariage - A4 - 2 exemplaires.pdf"

manque=""
python3 -c "import yaml" 2>/dev/null || manque="$manque PyYAML"
python3 -c "import pymupdf" 2>/dev/null || manque="$manque PyMuPDF"
if [ -n "$manque" ]; then
  echo "  ✗ Dépendances Python manquantes :$manque" >&2
  echo "    Installez-les : pip install -r requirements.txt" >&2
  exit 1
fi

CHROME="${CHROME:-}"
if [ -z "$CHROME" ]; then
  for navigateur in google-chrome google-chrome-stable chromium chromium-browser; do
    if command -v "$navigateur" >/dev/null 2>&1; then
      CHROME="$navigateur"
      break
    fi
  done
fi
if [ -z "$CHROME" ]; then
  echo "  ✗ Chrome ou Chromium est introuvable." >&2
  echo "    Installez-le, ou lancez : CHROME=/chemin/vers/chrome ./construire.sh" >&2
  exit 1
fi

cd "$ICI"
mkdir -p build "$DEST"

echo "→ lecture de menu.yaml"
python3 moteur/contenu.py

echo "→ composition du menu"
python3 moteur/composer.py

echo "→ rendu du menu 12 × 18 cm"
rm -f build/menu-12x18.pdf
"$CHROME" --headless=new --disable-gpu --no-sandbox --no-pdf-header-footer \
  --user-data-dir="$ICI/build/chrome-profile" \
  --run-all-compositor-stages-before-draw --virtual-time-budget=15000 \
  --print-to-pdf=build/menu-12x18.pdf "file://$ICI/build/menu.html" \
  >/dev/null 2>&1
if [ ! -f build/menu-12x18.pdf ]; then
  echo "  ✗ Chrome n'a pas produit le PDF du menu." >&2
  exit 1
fi

echo "→ placement de 2 exemplaires sur A4"
python3 moteur/imposer.py build/menu-12x18.pdf build/menu-a4-2-exemplaires.pdf | head -1

echo "→ copie vers ${DEST}"
cp build/menu-12x18.pdf "$DEST/$NOM_MENU"
cp build/menu-a4-2-exemplaires.pdf "$DEST/$NOM_PLANCHE"

echo "→ vérification des fichiers produits"
python3 moteur/verifier.py "$DEST/$NOM_MENU" "$DEST/$NOM_PLANCHE"

echo "✓ fichiers prêts :"
echo "   $DEST/$NOM_MENU"
echo "   $DEST/$NOM_PLANCHE"
