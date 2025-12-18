import myvizlib
import matplotlib.pyplot as plt

myvizlib.styled_bar(
    categories=["North", "South", "East"],
    values=[100, 60, 80],
    title="Sales by region"
)

myvizlib.styled_line(
    x=[1, 2, 3, 4, 5],
    y=[10, 12, 9, 15, 14],
    title="Temperature over time"
)

myvizlib.styled_scatter(
    x=[2, 4, 6, 8],
    y=[10, 14, 16, 18],
    title="Study hours vs grade"
)

myvizlib.styled_hist(
    data=[2000, 2200, 2500, 2600, 2700, 4000, 4100],
    bins=5,
    title="Salary distribution"
)

myvizlib.styled_pie(
    labels=["Rent", "Food", "Transport"],
    sizes=[60, 25, 15],
    title="Budget split"
)

plt.show()
