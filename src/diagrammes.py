""" Small building blocks for drawing schema diagrams with matplotlib."""
from matplotlib.patches import FancyArrowPatch, Rectangle

from src.style import ENCRE, STATUT

H_LIGNE = 0.34


def boite_table(ax, x, y, titre, lignes, largeur=3.0, entete="#2a78d6", texte_entete="white", pointille=False,
                sous_titre=None):
    """Draw a table (colorful header + one line per column) whose top-left corner is (x, y).

    lignes : list of (marker, label), where the marker is 'PK', 'FK', 'SK', or '' ...
    Returns the geometry of the box for linking.
    """
    h_entete = H_LIGNE * (1.9 if sous_titre else 1.3)
    hauteur = h_entete + H_LIGNE * (len(lignes) + 0.3)
    ax.add_patch(Rectangle((x, y - hauteur), largeur, hauteur, facecolor=ENCRE["fond"], edgecolor=ENCRE["axe"],
                           linewidth=1, linestyle=(0, (4, 3)) if pointille else "-", zorder=2))
    ax.add_patch(Rectangle((x, y - h_entete), largeur, h_entete, facecolor=entete, edgecolor="none", zorder=3))
    ax.text(x + 0.12, y - (H_LIGNE * 0.6 if sous_titre else h_entete / 2), titre, va="center", ha="left",
            fontsize=10, fontweight="bold", color=texte_entete, zorder=4)
    if sous_titre:
        ax.text(x + 0.12, y - H_LIGNE * 1.4, sous_titre, va="center", ha="left", fontsize=7.5,
                color=texte_entete, zorder=4)
    for i, (marqueur, libelle) in enumerate(lignes):
        yy = y - h_entete - H_LIGNE * (i + 0.65)
        if marqueur:
            ax.text(x + 0.12, yy, marqueur, fontsize=7, color=ENCRE["discrete"], va="center", fontweight="bold", zorder=4)
        ax.text(x + 0.55, yy, libelle, fontsize=8.3, color=ENCRE["principale"], va="center", zorder=4)
    return {"x": x, "y": y, "w": largeur, "h": hauteur}


def ancre(boite, cote, fraction=0.5):
    """Point d'accroche sur un côté de la boîte ; fraction = position le long du côté (0 = début)."""
    x, y, w, h = boite["x"], boite["y"], boite["w"], boite["h"]
    return {"gauche": (x, y - h * fraction), "droite": (x + w, y - h * fraction),
            "haut": (x + w * fraction, y), "bas": (x + w * fraction, y - h)}[cote]


def relier(ax, b1, cote1, b2, cote2, card1="", card2="", f1=0.5, f2=0.5, anomalie=None, pos_anomalie=0.5,
           decalage_anomalie=(0.1, 0.12), droit=False):
    """Lien entre deux tables (orthogonal, ou droit si droit=True), avec les cardinalités à chaque extrémité."""
    p1, p2 = ancre(b1, cote1, f1), ancre(b2, cote2, f2)
    horiz1, horiz2 = cote1 in ("gauche", "droite"), cote2 in ("gauche", "droite")
    if droit:
        chemin = [p1, p2]
    elif horiz1 and horiz2:
        xm = (p1[0] + p2[0]) / 2
        chemin = [p1, (xm, p1[1]), (xm, p2[1]), p2]
    elif not horiz1 and not horiz2:
        ym = (p1[1] + p2[1]) / 2
        chemin = [p1, (p1[0], ym), (p2[0], ym), p2]
    elif horiz1:
        chemin = [p1, (p2[0], p1[1]), p2]
    else:
        chemin = [p1, (p1[0], p2[1]), p2]
    xs, ys = zip(*chemin)
    ax.plot(xs, ys, color=ENCRE["secondaire"], linewidth=1.2, zorder=1, solid_joinstyle="miter")
    for p, cote, card in [(p1, cote1, card1), (p2, cote2, card2)]:
        if not card:
            continue
        dx, dy = {"gauche": (-0.12, 0.13), "droite": (0.12, 0.13), "haut": (0.1, 0.14), "bas": (0.1, -0.16)}[cote]
        ha = "right" if cote == "gauche" else "left"
        ax.text(p[0] + dx, p[1] + dy, card, fontsize=8.5, color=ENCRE["principale"], ha=ha, va="center",
                fontweight="bold", zorder=5)
    if anomalie:
        # position le long du segment central du chemin
        (xa, ya), (xb, yb) = chemin[len(chemin) // 2 - 1], chemin[len(chemin) // 2]
        xm, ym = xa + (xb - xa) * pos_anomalie, ya + (yb - ya) * pos_anomalie
        ax.scatter([xm], [ym], s=28, color=STATUT["critique"], zorder=6, edgecolor=ENCRE["fond"], linewidth=1.5)
        ax.text(xm + decalage_anomalie[0], ym + decalage_anomalie[1], anomalie, fontsize=7.5, color=ENCRE["secondaire"],
                ha="left", va="bottom", style="italic", zorder=6)


def boite_etape(ax, x, y, largeur, hauteur, titre, lignes, entete="#2a78d6", texte_entete="white", outils=None):
    """Bloc d'architecture : titre, contenu à puces, et outils en bas."""
    ax.add_patch(Rectangle((x, y - hauteur), largeur, hauteur, facecolor=ENCRE["fond"], edgecolor=ENCRE["axe"],
                           linewidth=1, zorder=2))
    ax.add_patch(Rectangle((x, y - 0.55), largeur, 0.55, facecolor=entete, edgecolor="none", zorder=3))
    ax.text(x + largeur / 2, y - 0.275, titre, ha="center", va="center", fontsize=10, fontweight="bold",
            color=texte_entete, zorder=4)
    for i, ligne in enumerate(lignes):
        ax.text(x + 0.12, y - 0.85 - i * 0.36, f"• {ligne}", fontsize=8, color=ENCRE["principale"], va="center", zorder=4)
    if outils:
        ax.plot([x + 0.1, x + largeur - 0.1], [y - hauteur + 0.75, y - hauteur + 0.75], color=ENCRE["grille"],
                linewidth=1, zorder=3)
        ax.text(x + largeur / 2, y - hauteur + 0.4, outils, ha="center", va="center", fontsize=7.8,
                color=ENCRE["secondaire"], style="italic", zorder=4, wrap=True)
    return {"x": x, "y": y, "w": largeur, "h": hauteur}


def fleche(ax, p1, p2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14, color=ENCRE["secondaire"],
                                 linewidth=1.4, zorder=1))
