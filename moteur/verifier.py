# -*- coding: utf-8 -*-
"""Contrôle le format, les marges et les polices des PDF produits."""
import collections
import os
import sys

try:
    import pymupdf
except ImportError:  # pragma: no cover
    sys.exit("PyMuPDF manquant. Installez-le avec : pip install -r requirements.txt")


ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

from contenu import charger  # noqa: E402


MM = 72 / 25.4
MARGE_MINI_MM = 8


def _dimensions_mm(page):
    return page.rect.width / MM, page.rect.height / MM


def _encre(page):
    boites = []
    for bloc in page.get_text("dict").get("blocks", []):
        if "bbox" in bloc:
            boites.append(bloc["bbox"])
    for dessin in page.get_drawings():
        rectangle = dessin.get("rect")
        if rectangle and not rectangle.is_empty:
            boites.append((rectangle.x0, rectangle.y0, rectangle.x1, rectangle.y1))
    return boites


def _marge_minimale(page):
    boites = _encre(page)
    if not boites:
        return 999.0
    return min(
        min(boite[0] for boite in boites),
        min(boite[1] for boite in boites),
        page.rect.width - max(boite[2] for boite in boites),
        page.rect.height - max(boite[3] for boite in boites),
    ) / MM


def verifier(chemin_menu, chemin_planche=None):
    erreurs = []
    avertissements = []
    reglages = charger()["reglages"]
    largeur_attendue = reglages["page"]["largeur_mm"]
    hauteur_attendue = reglages["page"]["hauteur_mm"]

    menu = pymupdf.open(chemin_menu)
    if menu.page_count != 1:
        erreurs.append(
            f"le menu contient {menu.page_count} pages au lieu d'une : "
            "réduisez le contenu ou la taille du texte dans menu.yaml")
    largeur, hauteur = _dimensions_mm(menu[0])
    if abs(largeur - largeur_attendue) > 0.3 or abs(hauteur - hauteur_attendue) > 0.3:
        erreurs.append(
            f"format obtenu {largeur:.1f} × {hauteur:.1f} mm, attendu "
            f"{largeur_attendue:g} × {hauteur_attendue:g} mm")

    types = collections.Counter()
    for page in menu:
        for police in page.get_fonts(full=True):
            types[police[2]] += 1
    if "Type3" in types:
        erreurs.append(
            f"polices Type3 détectées ({types['Type3']}) : utilisez des fichiers "
            "de police statiques, comme ceux fournis dans polices/")
    elif set(types) - {"Type0"}:
        avertissements.append(f"types de police inattendus : {dict(types)}")

    marge = min(_marge_minimale(page) for page in menu)
    if marge < MARGE_MINI_MM - 0.1:
        erreurs.append(
            f"de l'encre passe à {marge:.1f} mm du bord du menu "
            f"(minimum {MARGE_MINI_MM} mm)")

    resume = [
        f"menu : {largeur:.1f} × {hauteur:.1f} mm, 1 page, "
        f"polices {dict(types) or '—'}, marge mini {marge:.1f} mm"
    ]

    if chemin_planche and os.path.exists(chemin_planche):
        planche = pymupdf.open(chemin_planche)
        if planche.page_count != 1:
            erreurs.append(
                f"la planche A4 contient {planche.page_count} pages au lieu d'une")
        largeur_a4, hauteur_a4 = _dimensions_mm(planche[0])
        if abs(largeur_a4 - 297) > 0.3 or abs(hauteur_a4 - 210) > 0.3:
            erreurs.append(
                f"format de la planche {largeur_a4:.1f} × {hauteur_a4:.1f} mm, "
                "attendu 297 × 210 mm")
        resume.append("planche : A4 paysage, 2 exemplaires à taille réelle")

    return resume, avertissements, erreurs


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage : verifier.py <menu.pdf> [planche-a4.pdf]")
    resume, avertissements, erreurs = verifier(
        sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    for ligne in resume:
        print(f"   {ligne}")
    for avertissement in avertissements:
        print(f"   ! {avertissement}")
    for erreur in erreurs:
        print(f"   ✗ {erreur}")
    if erreurs:
        sys.exit(1)
    print("   ✓ conforme")
