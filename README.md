# myvizlib

A personal Python visualization library with a consistent style.

## Install (dev)
pip install -e .

## Usage
from myvizlib import bar_chart, line_chart, scatter_plot, histogram, pie_chart

fig, ax = bar_chart(["North","South","East"], [100, 60, 80], title="Sales by region")

