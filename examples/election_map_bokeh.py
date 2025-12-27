# examples/election_map_bokeh.py

import pandas as pd
import geopandas as gpd
from bokeh.io import show, output_file
from bokeh.palettes import Greens9  # ✅ Palette verte
from pathlib import Path

import myvizlib


# -------------------------
# Fonction utilitaire : trouver la racine du projet (celle qui contient pyproject.toml)
# -------------------------
def find_project_root(marker="pyproject.toml"):
    current = Path.cwd().resolve()
    for parent in [current] + list(current.parents):
        if (parent / marker).exists():
            return parent
    raise FileNotFoundError(
        f"Impossible de trouver {marker}. Lance ce script depuis le dépôt du projet."
    )


# -------------------------
# Trouver automatiquement le shapefile ADM2 (moughataas)
# -------------------------
ROOT = find_project_root()

# Chercher tous les fichiers .shp dans mrshape s'il existe, sinon partout
if (ROOT / "mrshape").exists():
    shp_files = list((ROOT / "mrshape").rglob("*.shp"))
else:
    shp_files = list(ROOT.rglob("*.shp"))

if not shp_files:
    raise FileNotFoundError(
        "Aucun fichier .shp trouvé dans le projet. Vérifie que le shapefile est bien extrait."
    )

# Filtrer ceux qui contiennent "adm2" (niveau moughataa)
adm2_files = [p for p in shp_files if "adm2" in p.name.lower()]

if not adm2_files:
    raise FileNotFoundError(
        "Aucun shapefile ADM2 trouvé. Vérifie que le fichier adm2 est bien présent dans mrshape."
    )

# Prendre le premier ADM2 trouvé
shapefile_path = adm2_files[0]
print("Shapefile ADM2 utilisé :", shapefile_path)


# -------------------------
# Charger shapefile
# -------------------------
gdf_moughataas = gpd.read_file(shapefile_path)

# Renommer la colonne ADM2_EN -> moughataa si elle existe
if "ADM2_EN" in gdf_moughataas.columns:
    gdf_moughataas = gdf_moughataas.rename(columns={"ADM2_EN": "moughataa"})
else:
    raise ValueError(
        "La colonne ADM2_EN n'existe pas dans ce shapefile. "
        "Vérifie que tu utilises bien le shapefile ADM2."
    )


# -------------------------
# Charger résultats CSV
# -------------------------
csv_url = "https://raw.githubusercontent.com/binorassocies/rimdata/refs/heads/main/data/results_elections_rim_2019-2024.csv"
df_elections = pd.read_csv(csv_url)

# Filtrer sur l'année 2024
df_elections_2024 = df_elections[df_elections["year"] == 2024]


# -------------------------
# Agrégation : somme des voix par moughataa et candidat
# -------------------------
df_agg_2024 = df_elections_2024.groupby(["moughataa", "candidate"], as_index=False)["nb_votes"].sum()


# -------------------------
# Carte interactive (palette verte)
# -------------------------
layout = myvizlib.styled_election_map_bokeh(
    gdf_moughataas,
    df_agg_2024,
    palette=Greens9,          # ✅ dégradé de verts
    reverse_palette=True      # ✅ foncé en haut, clair en bas
)

# Générer un fichier HTML (car c'est un script, pas un notebook)
output_file("election_map_bokeh.html", title="Election Map Bokeh - Mauritanie 2024")

# Afficher dans le navigateur
show(layout)
