"""Files and directories paths."""
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
FICHIER_BRUT = RACINE / "data" / "raw" / "Data.xlsx"
DOSSIER_PROPRE = RACINE / "data" / "processed"
DOSSIER_FIGURES = RACINE / "figures"

# Date of data extraction from the application.

DATE_EXTRACTION = pd.Timestamp("2026-10-19")

# Date of data migration.

DATE_MIGRATION = pd.Timestamp("2025-06-03")

# Default dates for the signature

DATES_SIGNATURE_DEFAUT = pd.to_datetime(["2024-08-05", "2021-08-13"])
