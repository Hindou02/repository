DEFAULT_STYLE = {
    "palette": {
        "primary": "#1f77b4",
        "secondary": "#ff7f0e",
        "neutral": "#7f7f7f",
        "alert": "#d62728"
    },
    "font": {
        "family": "DejaVu Sans",
        "size": 11
    },
    "lines": {
        "width": 2.5,
        "alpha": 0.95
    },
    "axes": {
        "grid": True,
        "grid_alpha": 0.25,
        "spines": ("left", "bottom")
    }
}

def apply_style(style=None):
    import matplotlib as mpl

    s = DEFAULT_STYLE if style is None else style

    mpl.rcParams["font.family"] = s["font"]["family"]
    mpl.rcParams["font.size"] = s["font"]["size"]

    mpl.rcParams["axes.grid"] = s["axes"]["grid"]
    mpl.rcParams["grid.alpha"] = s["axes"]["grid_alpha"]

    mpl.rcParams["axes.spines.top"] = False
    mpl.rcParams["axes.spines.right"] = False
    mpl.rcParams["axes.spines.left"] = "left" in s["axes"]["spines"]
    mpl.rcParams["axes.spines.bottom"] = "bottom" in s["axes"]["spines"]
