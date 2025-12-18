from .theme import apply_style, DEFAULT_STYLE

def _style(style):
    return DEFAULT_STYLE if style is None else style

def bar_chart(categories, values, title="", xlabel="", ylabel="", style=None, start_at_zero=True, max_bars=25):
    import matplotlib.pyplot as plt

    apply_style(style)
    s = _style(style)

    if len(categories) != len(values):
        raise ValueError("categories and values must have same length")

    if len(categories) > max_bars:
        raise ValueError("Too many bars; reduce categories (e.g., top-N) or use a table")

    fig, ax = plt.subplots()
    ax.bar(categories, values, color=s["palette"]["primary"])

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if start_at_zero:
        ax.set_ylim(bottom=0)

    return fig, ax

def line_chart(x, y, title="", xlabel="", ylabel="", style=None, max_series_points=None):
    import matplotlib.pyplot as plt

    apply_style(style)
    s = _style(style)

    if len(x) != len(y):
        raise ValueError("x and y must have same length")

    if max_series_points is not None and len(x) > max_series_points:
        raise ValueError("Too many points for a single line; consider aggregation or sampling")

    fig, ax = plt.subplots()
    ax.plot(x, y, color=s["palette"]["primary"], linewidth=s["lines"]["width"], alpha=s["lines"]["alpha"])

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    return fig, ax

def scatter_plot(x, y, title="", xlabel="", ylabel="", style=None, alpha=0.85):
    import matplotlib.pyplot as plt

    apply_style(style)
    s = _style(style)

    if len(x) != len(y):
        raise ValueError("x and y must have same length")

    fig, ax = plt.subplots()
    ax.scatter(x, y, color=s["palette"]["secondary"], alpha=alpha)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    return fig, ax

def histogram(data, bins=10, title="", xlabel="", ylabel="Frequency", style=None):
    import matplotlib.pyplot as plt

    apply_style(style)
    s = _style(style)

    fig, ax = plt.subplots()
    ax.hist(data, bins=bins, color=s["palette"]["primary"], alpha=0.85)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    return fig, ax

def pie_chart(labels, sizes, title="", style=None, max_categories=5, min_distinct_gap=0.03):
    import matplotlib.pyplot as plt
    import numpy as np

    apply_style(style)
    s = _style(style)

    if len(labels) != len(sizes):
        raise ValueError("labels and sizes must have same length")

    if len(labels) > max_categories:
        raise ValueError("Pie chart should have <= 5 categories; use bar/stacked bar instead")

    total = float(np.sum(sizes))
    if total <= 0:
        raise ValueError("sizes must sum to a positive value")

    shares = np.array(sizes, dtype=float) / total
    shares_sorted = np.sort(shares)
    if len(shares_sorted) >= 2 and np.min(np.diff(shares_sorted)) < min_distinct_gap:
        raise ValueError("Slices too similar; use bar chart for better comparison")

    colors = [
        s["palette"]["primary"],
        s["palette"]["secondary"],
        s["palette"]["neutral"],
        s["palette"]["alert"],
        "#9467bd"
    ]

    fig, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=labels,
        colors=colors[:len(labels)],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.set_title(title)

    return fig, ax
