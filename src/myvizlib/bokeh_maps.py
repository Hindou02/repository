# src/myvizlib/bokeh_maps.py

from __future__ import annotations
from typing import Optional, Sequence, Tuple, Dict

import pandas as pd
import geopandas as gpd

from bokeh.plotting import figure
from bokeh.models import (
    GeoJSONDataSource,
    LinearColorMapper,
    ColorBar,
    HoverTool,
    Select,
    CustomJS,
)
from bokeh.layouts import column
from bokeh.palettes import OrRd9


def styled_election_map_bokeh(
    gdf_moughataas: gpd.GeoDataFrame,
    df_agg_2024: pd.DataFrame,
    title_prefix: str = "Résultats",
    palette: Sequence[str] = OrRd9,
    reverse_palette: bool = True,
    width: int = 900,
    height: int = 600,
) -> column:
    """
    Crée une carte interactive Bokeh des résultats électoraux par moughataa.

    Attendus :
    - gdf_moughataas : GeoDataFrame avec colonnes ["moughataa", "geometry"]
    - df_agg_2024 : DataFrame avec colonnes ["moughataa", "candidate", "nb_votes"]

    Retour :
    - layout Bokeh (Select + carte), affichable avec show(layout)
    """

    # --- Vérifications minimales
    required_gdf = {"moughataa", "geometry"}
    required_df = {"moughataa", "candidate", "nb_votes"}
    if not required_gdf.issubset(set(gdf_moughataas.columns)):
        raise ValueError(f"gdf_moughataas doit contenir {required_gdf}")
    if not required_df.issubset(set(df_agg_2024.columns)):
        raise ValueError(f"df_agg_2024 doit contenir {required_df}")

    candidats_2024 = list(df_agg_2024["candidate"].unique())
    if len(candidats_2024) == 0:
        raise ValueError("Aucun candidat trouvé dans df_agg_2024.")

    # Palette inversée (foncé en haut, clair en bas)
    pal = list(palette)[::-1] if reverse_palette else list(palette)

    # --- Préparer GeoJSON pour chaque candidat (Solution 1 : colonnes utiles uniquement)
    geojson_dict: Dict[str, str] = {}

    for cand in candidats_2024:
        df_cand = df_agg_2024[df_agg_2024["candidate"] == cand].copy()

        gdf_tmp = gdf_moughataas.merge(df_cand, on="moughataa", how="left")
        gdf_tmp["nb_votes"] = gdf_tmp["nb_votes"].fillna(0)

        gdf_tmp = gdf_tmp[["moughataa", "nb_votes", "geometry"]].copy()
        geojson_dict[cand] = gdf_tmp.to_json()

    candidat_default = candidats_2024[0]
    geosource = GeoJSONDataSource(geojson=geojson_dict[candidat_default])

    # --- Échelle globale commune à tous les candidats
    global_min = float(df_agg_2024["nb_votes"].min())
    global_max = float(df_agg_2024["nb_votes"].max())
    if global_min == global_max:
        global_max = global_min + 1

    color_mapper = LinearColorMapper(palette=pal, low=global_min, high=global_max)

    # --- Figure
    p = figure(
        title=f"{title_prefix} {candidat_default} - Élection 2024",
        width=width,
        height=height,
        tools="pan,wheel_zoom,reset,save",
        active_scroll="wheel_zoom",
    )

    patches = p.patches(
        "xs",
        "ys",
        source=geosource,
        fill_color={"field": "nb_votes", "transform": color_mapper},
        line_color="black",
        line_width=0.5,
        fill_alpha=0.8,
    )

    hover = HoverTool(
        renderers=[patches],
        tooltips=[
            ("Moughataa", "@moughataa"),
            ("Voix", "@nb_votes{0,0}"),
        ],
    )
    p.add_tools(hover)

    color_bar = ColorBar(
        color_mapper=color_mapper,
        label_standoff=12,
        location=(0, 0),
        title="Nombre de voix",
    )
    p.add_layout(color_bar, "right")

    # --- Select + callback JS (Notebook friendly)
    select = Select(
        title="Choisir un candidat :",
        value=candidat_default,
        options=candidats_2024,
    )

    callback = CustomJS(
        args=dict(geosource=geosource, geojson_dict=geojson_dict, p=p, title_prefix=title_prefix),
        code="""
            const cand = cb_obj.value;
            geosource.geojson = geojson_dict[cand];
            p.title.text = `${title_prefix} ${cand} - Élection 2024`;
        """,
    )

    select.js_on_change("value", callback)

    return column(select, p)
