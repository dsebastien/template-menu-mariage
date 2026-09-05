# -*- coding: utf-8 -*-
"""Lit menu.yaml et prépare tout le texte destiné au menu imprimé."""
import os
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML manquant. Installez-le avec : pip install -r requirements.txt")


ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
NBSP = " "
LIGATURES = (
    ("coeur", "cœur"), ("Coeur", "Cœur"), ("soeur", "sœur"),
    ("Soeur", "Sœur"), ("oeuvre", "œuvre"), ("Oeuvre", "Œuvre"),
    ("voeu", "vœu"), ("Voeu", "Vœu"), ("noeud", "nœud"),
    ("oeil", "œil"),
)


class ErreurContenu(Exception):
    """Erreur de saisie dans menu.yaml, formulée pour l'utilisateur."""


def fr(texte):
    """Normalise la typographie française d'une chaîne."""
    if texte is None:
        return ""
    texte = re.sub(r"\s+", " ", str(texte).strip())
    texte = texte.replace("'", "’")
    for brut, ligature in LIGATURES:
        texte = texte.replace(brut, ligature)
    texte = re.sub(r"[  ]*([:;!?])", NBSP + r"\1", texte)
    texte = re.sub(r"(?<=\d)[  ]*([%€])", NBSP + r"\1", texte)
    texte = re.sub(r"«[  ]*", "«" + NBSP, texte)
    texte = re.sub(r"[  ]*»", NBSP + "»", texte)
    return texte.replace(" - ", " – ")


def _substituer(objet, valeurs):
    """Remplace les marqueurs {nom} partout dans le contenu."""
    if isinstance(objet, str):
        def remplacer(correspondance):
            cle = correspondance.group(1)
            if cle not in valeurs:
                disponibles = ", ".join(sorted(valeurs)) or "aucun"
                raise ErreurContenu(
                    f"marqueur inconnu « {{{cle}}} ». "
                    f"Marqueurs disponibles : {disponibles}.")
            return str(valeurs[cle])
        return re.sub(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", remplacer, objet)
    if isinstance(objet, list):
        return [_substituer(item, valeurs) for item in objet]
    if isinstance(objet, dict):
        return {cle: _substituer(valeur, valeurs)
                for cle, valeur in objet.items()}
    return objet


def _texte(valeur, ou, obligatoire=False):
    if valeur is None:
        valeur = ""
    if not isinstance(valeur, (str, int, float)):
        raise ErreurContenu(f"{ou} : attendu du texte.")
    resultat = fr(valeur)
    if obligatoire and not resultat:
        raise ErreurContenu(f"{ou} est obligatoire.")
    return resultat


def _nombre(valeur, ou, minimum=None):
    if isinstance(valeur, bool):
        raise ErreurContenu(f"{ou} : attendu un nombre, reçu {valeur!r}.")
    try:
        nombre = float(valeur)
    except (TypeError, ValueError):
        raise ErreurContenu(f"{ou} : attendu un nombre, reçu {valeur!r}.")
    if minimum is not None and nombre < minimum:
        raise ErreurContenu(f"{ou} doit être supérieur ou égal à {minimum}.")
    return nombre


def _reglages(brut):
    reglages = brut or {}
    if not isinstance(reglages, dict):
        raise ErreurContenu("reglages : attendu un groupe de réglages.")

    page = reglages.get("page") or {}
    if not isinstance(page, dict):
        raise ErreurContenu("reglages.page : attendu un groupe de réglages.")
    largeur = _nombre(page.get("largeur_mm", 120),
                      "reglages.page.largeur_mm", 50)
    hauteur = _nombre(page.get("hauteur_mm", 180),
                      "reglages.page.hauteur_mm", 50)

    cadre = reglages.get("cadre") or {}
    if not isinstance(cadre, dict):
        raise ErreurContenu("reglages.cadre : attendu un groupe de réglages.")
    retrait = _nombre(cadre.get("retrait_mm", 9),
                      "reglages.cadre.retrait_mm", 8)
    if retrait * 2 >= min(largeur, hauteur):
        raise ErreurContenu(
            "reglages.cadre.retrait_mm est trop grand pour le format choisi.")

    resultat = dict(reglages)
    resultat["page"] = {"largeur_mm": largeur, "hauteur_mm": hauteur}
    resultat["cadre"] = dict(cadre, retrait_mm=retrait)
    return resultat


def charger(chemin=None):
    chemin = chemin or os.path.join(RACINE, "menu.yaml")
    if not os.path.exists(chemin):
        raise ErreurContenu(f"fichier introuvable : {chemin}")

    with open(chemin, encoding="utf8") as fichier:
        try:
            brut = yaml.safe_load(fichier)
        except yaml.YAMLError as erreur:
            raise ErreurContenu(f"menu.yaml illisible :\n{erreur}")

    if not isinstance(brut, dict):
        raise ErreurContenu("menu.yaml est vide ou mal formé.")

    informations = brut.get("informations") or {}
    if not isinstance(informations, dict):
        raise ErreurContenu("informations : attendu une liste de valeurs nommées.")
    informations = {cle: _texte(valeur, f"informations.{cle}")
                    for cle, valeur in informations.items()}
    brut = _substituer(brut, informations)

    menu = brut.get("menu") or {}
    if not isinstance(menu, dict):
        raise ErreurContenu("menu : attendu un groupe contenant le titre et les plats.")
    titre = _texte(menu.get("titre"), "menu.titre", obligatoire=True)
    sous_titre = _texte(menu.get("sous_titre"), "menu.sous_titre")

    plats_bruts = menu.get("plats") or []
    if not isinstance(plats_bruts, list):
        raise ErreurContenu("menu.plats : attendu une liste commençant par « - ».")
    if not plats_bruts:
        raise ErreurContenu("menu.plats est vide : ajoutez au moins un plat.")

    plats = []
    for index, plat in enumerate(plats_bruts, 1):
        ou = f"menu.plats[{index}]"
        if not isinstance(plat, dict):
            raise ErreurContenu(f"{ou} : attendu un groupe avec « titre ».")
        normalise = {
            "titre": _texte(plat.get("titre"), f"{ou}.titre", obligatoire=True),
            "nom": _texte(plat.get("nom"), f"{ou}.nom"),
            "description": _texte(plat.get("description"), f"{ou}.description"),
            "note": _texte(plat.get("note"), f"{ou}.note"),
        }
        if not any(normalise[cle] for cle in ("nom", "description", "note")):
            raise ErreurContenu(
                f"{ou} : ajoutez au moins « nom », « description » ou « note ».")
        plats.append(normalise)

    conclusion = menu.get("conclusion") or {}
    if not isinstance(conclusion, dict):
        raise ErreurContenu("menu.conclusion : attendu un groupe de textes.")

    return {
        "informations": informations,
        "menu": {
            "titre": titre,
            "sous_titre": sous_titre,
            "plats": plats,
            "conclusion": {
                "message": _texte(conclusion.get("message"),
                                  "menu.conclusion.message"),
                "note": _texte(conclusion.get("note"),
                               "menu.conclusion.note"),
            },
        },
        "reglages": _reglages(brut.get("reglages")),
    }


if __name__ == "__main__":
    try:
        donnees = charger()
    except ErreurContenu as erreur:
        sys.exit(f"\n  ✗ {erreur}\n")
    print(f"menu.yaml : {len(donnees['menu']['plats'])} plats — OK")
