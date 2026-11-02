"""Charte graphique commune : palette validée daltonisme, encre de texte, grille discrète."""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from cycler import cycler

from src.config import DOSSIER_FIGURES

# Ordre fixe des couleurs catégorielles.

PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]

# Couleurs réservées aux statuts (gravité, conformité).

STATUT = {"conforme": "#0ca30c", "mineure": "#fab219", "majeure": "#ec835a", "critique": "#d03b3b"}

ENCRE = {
    "principale": "#0b0b0b",
    "secondaire": "#52514e",
    "discrete": "#898781",
    "grille": "#e1e0d9",
    "axe": "#c3c2b7",
    "fond": "#fcfcfb",
}


def appliquer_style():
    plt.rcParams.update({
        "figure.facecolor": ENCRE["fond"],
        "axes.facecolor": ENCRE["fond"],
        "savefig.facecolor": ENCRE["fond"],
        "font.family": ["Segoe UI", "DejaVu Sans"],
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 12,
        "axes.labelsize": 10,
        "axes.labelcolor": ENCRE["secondaire"],
        "axes.edgecolor": ENCRE["axe"],
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": ENCRE["grille"],
        "grid.linewidth": 0.8,
        "grid.linestyle": "-",
        "axes.prop_cycle": cycler(color=PALETTE),
        "text.color": ENCRE["principale"],
        "xtick.color": ENCRE["discrete"],
        "ytick.color": ENCRE["discrete"],
        "xtick.labelcolor": ENCRE["secondaire"],
        "ytick.labelcolor": ENCRE["secondaire"],
        "lines.linewidth": 2,
        "lines.solid_capstyle": "round",
        "legend.frameon": False,
        "legend.fontsize": 9,
        "figure.dpi": 110,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
    })


def sauver(fig, nom):
    DOSSIER_FIGURES.mkdir(exist_ok=True)
    fig.savefig(DOSSIER_FIGURES / f"{nom}.png")


def etiqueter_barres(ax, valeurs, fmt="{:,.0f}", horizontal=True, decalage=3):
    """Valeur au bout de chaque barre, en encre secondaire (jamais dans la couleur de la série)."""
    for patch, v in zip(ax.patches, valeurs):
        texte = fmt.format(v).replace(",", " ")
        if horizontal:
            ax.annotate(texte, (patch.get_width(), patch.get_y() + patch.get_height() / 2),
                        xytext=(decalage, 0), textcoords="offset points",
                        va="center", ha="left", fontsize=9, color=ENCRE["secondaire"])
        else:
            ax.annotate(texte, (patch.get_x() + patch.get_width() / 2, patch.get_height()),
                        xytext=(0, decalage), textcoords="offset points",
                        va="bottom", ha="center", fontsize=9, color=ENCRE["secondaire"])


def nb(x, decimales=0):
    """12345.6 -> '12 346' (espace comme séparateur de milliers)."""
    return f"{x:,.{decimales}f}".replace(",", " ")


MOIS_FR = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]


def axe_mensuel(ax, mois=(1, 4, 7, 10)):
    """Graduations trimestrielles en français sur un axe de dates : 'janv. 25', 'avr. 25'..."""
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=list(mois)))
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(
        lambda x, _: f"{MOIS_FR[mdates.num2date(x).month - 1]} {mdates.num2date(x):%y}"))


def rampe_bleue():
    """Rampe séquentielle à une seule teinte (clair -> foncé) pour les cartes de chaleur."""
    from matplotlib.colors import LinearSegmentedColormap
    pas = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
    return LinearSegmentedColormap.from_list("bleu", pas)


def rampe_divergente():
    """Bleu <-> rouge avec un gris neutre au centre (0 = 'comme la moyenne')."""
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list("div", ["#184f95", "#3987e5", "#f0efec", "#e66767", "#a52b2b"])


def format_milliers(ax, axe="y"):
    fmt = mtick.FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", " "))
    (ax.yaxis if axe == "y" else ax.xaxis).set_major_formatter(fmt)


def format_pct(ax, axe="x", decimales=0):
    (ax.xaxis if axe == "x" else ax.yaxis).set_major_formatter(mtick.PercentFormatter(1, decimales))
