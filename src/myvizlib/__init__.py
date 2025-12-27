from .theme import DEFAULT_STYLE, apply_style
from .charts import (
    bar_chart,
    line_chart,
    scatter_plot,
    histogram,
    pie_chart,
    styled_line,
    styled_bar,
    styled_scatter,
    styled_hist,
    styled_pie,
)

# Partie cartes (optionnelle : nécessite `pip install myvizlib[maps]`)
try:
    from .bokeh_maps import styled_election_map_bokeh
except Exception:
    styled_election_map_bokeh = None


__all__ = [
    "DEFAULT_STYLE",
    "apply_style",
    "bar_chart",
    "line_chart",
    "scatter_plot",
    "histogram",
    "pie_chart",
    "styled_line",
    "styled_bar",
    "styled_scatter",
    "styled_hist",
    "styled_pie",
    "styled_election_map_bokeh",
]
