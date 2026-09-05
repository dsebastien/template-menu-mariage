# -*- coding: utf-8 -*-
"""Place deux exemplaires du menu, à taille réelle, sur une feuille A4."""
import os
import sys

try:
    import pymupdf
except ImportError:  # pragma: no cover
    sys.exit("PyMuPDF manquant. Installez-le avec : pip install -r requirements.txt")


MM = 72 / 25.4
A4_LARGEUR = 297 * MM
A4_HAUTEUR = 210 * MM


def _repere(page, x, y, horizontal, sens):
    """Trace un repère de coupe à l'extérieur d'une carte."""
    ecart = 1.5 * MM
    longueur = 4 * MM
    couleur = (0.35, 0.35, 0.35)
    if horizontal:
        debut = pymupdf.Point(x + sens * ecart, y)
        fin = pymupdf.Point(x + sens * (ecart + longueur), y)
    else:
        debut = pymupdf.Point(x, y + sens * ecart)
        fin = pymupdf.Point(x, y + sens * (ecart + longueur))
    page.draw_line(debut, fin, color=couleur, width=0.35)


def _reperes_coupe(page, rectangle):
    gauche, haut, droite, bas = rectangle
    for x, sens in ((gauche, -1), (droite, 1)):
        _repere(page, x, haut, True, sens)
        _repere(page, x, bas, True, sens)
    for y, sens in ((haut, -1), (bas, 1)):
        _repere(page, gauche, y, False, sens)
        _repere(page, droite, y, False, sens)


def imposer(source, sortie):
    document = pymupdf.open(source)
    if document.page_count != 1:
        raise ValueError(
            f"le menu produit contient {document.page_count} pages au lieu d'une. "
            "Réduisez le contenu ou la taille du texte dans menu.yaml.")

    largeur = document[0].rect.width
    hauteur = document[0].rect.height
    espace_horizontal = (A4_LARGEUR - 2 * largeur) / 3
    espace_vertical = (A4_HAUTEUR - hauteur) / 2
    if espace_horizontal < 7 * MM or espace_vertical < 7 * MM:
        raise ValueError(
            "deux menus de ce format ne tiennent pas à taille réelle sur une "
            "feuille A4 paysage. Utilisez au maximum 132 × 196 mm.")

    planche = pymupdf.open()
    page = planche.new_page(width=A4_LARGEUR, height=A4_HAUTEUR)
    rectangles = []
    for index in range(2):
        gauche = espace_horizontal + index * (largeur + espace_horizontal)
        rectangle = pymupdf.Rect(
            gauche, espace_vertical, gauche + largeur, espace_vertical + hauteur)
        page.show_pdf_page(rectangle, document, 0, keep_proportion=True)
        rectangles.append(rectangle)
        _reperes_coupe(page, rectangle)

    planche.set_metadata({
        "title": "Menu de mariage — deux exemplaires sur A4",
        "subject": "À imprimer à 100 %, sans ajustement à la page",
    })
    os.makedirs(os.path.dirname(os.path.abspath(sortie)), exist_ok=True)
    planche.save(sortie, garbage=4, deflate=True)
    return rectangles


if __name__ == "__main__":
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        racine, "build", "menu-12x18.pdf")
    sortie = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        racine, "build", "menu-a4-2-exemplaires.pdf")
    try:
        emplacements = imposer(source, sortie)
    except ValueError as erreur:
        sys.exit(f"\n  ✗ {erreur}\n")
    print(f"2 exemplaires à taille réelle sur A4 paysage — {sortie}")
