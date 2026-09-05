# -*- coding: utf-8 -*-
"""Compose le menu en HTML, prêt à être imprimé en PDF par Chrome."""
import html
import os
import re
import sys


ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
sys.path.insert(0, ICI)

from contenu import charger, ErreurContenu  # noqa: E402


def e(texte):
    return html.escape(str(texte), quote=False)


def _plat(plat):
    morceaux = [f'<h2>{e(plat["titre"])}</h2>']
    if plat["nom"]:
        morceaux.append(f'<p class="nom">{e(plat["nom"])}</p>')
    if plat["description"]:
        morceaux.append(f'<p class="description">{e(plat["description"])}</p>')
    if plat["note"]:
        morceaux.append(f'<p class="note">({e(plat["note"])})</p>')
    return '<section class="plat">' + "".join(morceaux) + "</section>"


def _motif(classe=""):
    return (f'<div class="motif {classe}" aria-hidden="true">'
            '<span class="trait"></span><span class="point"></span>'
            '<span class="trait"></span></div>')


def polices_css(reglages, depuis):
    """Déclare les instances statiques du dossier de polices."""
    polices = reglages.get("polices") or {}
    dossier = os.path.join(RACINE, polices.get("dossier", "polices"))
    if not os.path.isdir(dossier):
        raise ErreurContenu(
            f"dossier de polices introuvable : {dossier}\n"
            "    Corrigez « reglages.polices.dossier » dans menu.yaml.")

    faces = []
    for fichier in sorted(os.listdir(dossier)):
        if not fichier.endswith((".ttf", ".otf")):
            continue
        base = fichier.rsplit(".", 1)[0]
        nom, separateur, variante = base.rpartition("-")
        if not separateur:
            nom, variante = base, "400"
        famille = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", nom)
        famille = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", famille).strip()
        italique = "italic" in variante.lower()
        graisse = re.sub(r"[^0-9]", "", variante) or "400"
        chemin = os.path.relpath(os.path.join(dossier, fichier), depuis)
        chemin = chemin.replace(os.sep, "/")
        faces.append(
            f'@font-face{{font-family:"{famille}";'
            f'font-style:{"italic" if italique else "normal"};'
            f'font-weight:{graisse};font-display:block;'
            f'src:url("{chemin}") format("truetype");}}')
    if not faces:
        raise ErreurContenu(f"aucune police (.ttf/.otf) dans {dossier}")
    return "\n".join(faces)


def css(reglages):
    page = reglages["page"]
    largeur = page["largeur_mm"]
    hauteur = page["hauteur_mm"]
    cadre = reglages.get("cadre") or {}
    retrait = cadre.get("retrait_mm", 9)
    epaisseur = cadre.get("epaisseur_pt", 2)
    polices = reglages.get("polices") or {}
    texte = polices.get("texte", "EB Garamond")
    titres = polices.get("titres", "Cormorant Garamond")
    taille = polices.get("taille_pt", 9)
    couleurs = reglages.get("couleurs") or {}
    encre = couleurs.get("encre", "#4b413a")
    accent = couleurs.get("accent", "#A24F3D")
    decoration = couleurs.get("decoration", accent)

    return f"""
:root{{
  --encre:{encre}; --accent:{accent}; --decoration:{decoration};
  --texte:"{texte}", Palatino, Georgia, serif;
  --titres:"{titres}", "{texte}", Palatino, Georgia, serif;
}}
@page{{ size:{largeur}mm {hauteur}mm; margin:0; }}
*{{ box-sizing:border-box; }}
html,body{{ margin:0; padding:0; width:{largeur}mm; }}
html{{ font-size:{taille}pt; }}
body{{
  font-family:var(--texte); color:var(--encre); font-style:italic;
  font-kerning:normal; font-variant-ligatures:common-ligatures;
}}
.menu{{
  position:relative; width:{largeur}mm; height:{hauteur}mm;
  padding:11.5mm 13.5mm 11mm; display:flex; flex-direction:column;
  align-items:center; text-align:center;
}}
.cadre{{
  position:absolute; inset:{retrait}mm; border:{epaisseur}pt solid var(--decoration);
  pointer-events:none;
}}
.entete{{ flex:none; width:100%; }}
.motif{{
  width:24mm; height:3mm; margin:0 auto 3.2mm; display:flex;
  align-items:center; justify-content:center; gap:2.1mm; color:var(--decoration);
}}
.motif .trait{{ width:7mm; border-top:.65pt solid currentColor; }}
.motif .point{{ width:1.15mm; height:1.15mm; border-radius:50%;
               background:currentColor; }}
.motif-bas{{ width:7mm; margin:3mm auto 0; transform:rotate(45deg); }}
.motif-bas .trait{{ display:none; }}
.motif-bas .point{{ width:3.2mm; height:3.2mm; border-radius:0;
                   background:transparent; border:.7pt solid currentColor;
                   box-shadow:inset 0 0 0 .7mm white; }}
h1,h2{{
  font-family:var(--titres); font-style:normal; text-transform:uppercase;
  font-variant-numeric:lining-nums; font-feature-settings:"lnum" 1,"onum" 0;
}}
h1{{
  margin:0; color:var(--accent); font-size:24pt; line-height:1;
  font-weight:500; letter-spacing:.18em; text-indent:.18em;
}}
.sous-titre{{
  margin:2.2mm 0 0; font-size:8.7pt; color:var(--encre);
  letter-spacing:.08em;
}}
.losange{{
  width:3.3mm; height:3.3mm; margin:3.8mm auto 0; position:relative;
  transform:rotate(45deg); background:var(--decoration);
}}
.losange::before,.losange::after{{ content:""; position:absolute; background:white; }}
.losange::before{{ left:1.35mm; top:0; width:.55mm; height:100%; }}
.losange::after{{ top:1.35mm; left:0; height:.55mm; width:100%; }}
.plats{{
  width:100%; flex:1; display:flex; flex-direction:column;
  justify-content:center; gap:3.5mm; padding:2.5mm 0 1.5mm;
}}
.plat{{ break-inside:avoid; }}
.plat h2{{
  color:var(--accent); font-size:11.5pt; line-height:1.15; font-weight:600;
  letter-spacing:.15em; text-indent:.15em; margin:0 0 1.4mm;
}}
.plat p{{ margin:0; line-height:1.26; text-wrap:balance; }}
.nom{{
  font-family:var(--titres); font-weight:400; font-style:italic;
  font-size:10.8pt;
}}
.description{{ font-size:10.2pt; }}
.note{{ font-size:9.2pt; margin-top:1mm !important; }}
.conclusion{{ flex:none; width:100%; min-height:15mm; }}
.conclusion p{{ margin:0; line-height:1.3; text-wrap:balance; }}
.conclusion .message{{ font-size:10pt; margin-top:2.5mm; }}
.conclusion .note{{ font-size:9.2pt; margin-top:1.2mm !important; }}
"""


def composer(sortie=None):
    donnees = charger()
    menu = donnees["menu"]
    reglages = donnees["reglages"]
    sortie = sortie or os.path.join(RACINE, "build", "menu.html")
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    polices = polices_css(reglages, os.path.dirname(os.path.abspath(sortie)))

    sous_titre = ""
    if menu["sous_titre"]:
        sous_titre = f'<p class="sous-titre">{e(menu["sous_titre"])}</p>'
    plats = "\n".join(_plat(plat) for plat in menu["plats"])
    conclusion = menu["conclusion"]
    pied = ""
    if conclusion["message"] or conclusion["note"]:
        message = (f'<p class="message">{e(conclusion["message"])}</p>'
                   if conclusion["message"] else "")
        note = (f'<p class="note">{e(conclusion["note"])}</p>'
                if conclusion["note"] else "")
        pied = f'<footer class="conclusion">{_motif("motif-bas")}{message}{note}</footer>'

    titre_document = f'Menu de mariage — {menu["titre"]}'
    document = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>{e(titre_document)}</title>
<style>
{polices}
{css(reglages)}
</style>
</head>
<body>
<main class="menu">
  <div class="cadre" aria-hidden="true"></div>
  <header class="entete">
    {_motif()}
    <h1>{e(menu["titre"])}</h1>
    {sous_titre}
    <div class="losange" aria-hidden="true"></div>
  </header>
  <div class="plats">
    {plats}
  </div>
  {pied}
</main>
</body>
</html>"""

    with open(sortie, "w", encoding="utf8") as fichier:
        fichier.write(document)
    return sortie


if __name__ == "__main__":
    try:
        chemin = composer()
    except ErreurContenu as erreur:
        sys.exit(f"\n  ✗ {erreur}\n")
    print(f"HTML composé : {os.path.relpath(chemin, RACINE)}")
