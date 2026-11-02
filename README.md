# Test technique Data : NostrumCare

Analyse des données de contrats, de paiements (Stripe) et de remboursements de NostrumCare, en quatre parties : qualité des données, statistiques, segmentation des clients et data engineering.

**Auteur** : Gildas EDENAKPO
**Langages** : Python (pandas, scikit-learn, matplotlib) et SQL (SQLite)


## Structure du dossier

```
Test_Technique_NostrumCare/
├── data/
│   ├── raw/Data.xlsx              # Base de données brutes fournie par NostrumCare
│   ├── processed/                 # tables nettoyées (.pkl, .csv), registre des anomalies, segments
│   └── warehouse/                 # entrepôt prototype SQLite (régénéré par le notebook 04)
├── notebooks/
│   ├── 01_data_quality.ipynb      # Partie 1 (Data Quality)
│   ├── 02_statistiques.ipynb      # Partie 2 (Statistiques)
│   ├── 03_segmentation_clients.ipynb  # Partie 3 (Data Science)
│   └── 04_data_engineering.ipynb  # Partie 4 (Data Engineering)
├── rapport/
│   ├── Rapport_Test_Technique_NostrumCare.pdf
│   
│                   
├── figures/                       # tous les graphiques (PNG)
├── src/
│   ├── config.py                  # chemins, date d'extraction, dates par défaut repérées
│   ├── style.py                   # charte graphique commune
│   ├── diagrammes.py              # pour dessiner l'architecture de data warehouse 

|
├── requirements.txt
└── README.md
```

## Reproductibilité des résultats

```bash
python -m venv .venv
.venv\Scripts\activate          # sous macOS / Linux : source .venv/bin/activate
pip install -r requirements.txt
```

Exécuter ensuite les notebooks **dans l'ordre** : chacun lit les sorties du précédent (le 01 produit les tables nettoyées, le 03 produit les segments utilisés par le 04).

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_data_quality.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_statistiques.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_segmentation_clients.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/04_data_engineering.ipynb
```

Le rapport en PDF est réalisé avec Word


