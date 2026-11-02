"""Chemins et constantes partagés par tous les notebooks."""
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
FICHIER_BRUT = RACINE / "data" / "raw" / "Data.xlsx"
DOSSIER_PROPRE = RACINE / "data" / "processed"
DOSSIER_FIGURES = RACINE / "figures"

# Date d'extraction des données de l'application.

DATE_EXTRACTION = pd.Timestamp("2026-10-19")

# Date de migration des données.

DATE_MIGRATION = pd.Timestamp("2025-06-03")

# Dates par défaut pour la signature

DATES_SIGNATURE_DEFAUT = pd.to_datetime(["2024-08-05", "2021-08-13"])
