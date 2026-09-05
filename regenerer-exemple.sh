#!/usr/bin/env bash
# Régénère les PDF d'exemple et leurs aperçus dans la documentation.
set -euo pipefail

ICI="$(cd "$(dirname "$0")" && pwd)"
cd "$ICI"

./construire.sh exemple

echo "→ images de la documentation"
python3 - <<'PY'
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
PY

echo "✓ exemple/ et docs/images/ régénérés"
