from myvizlib import bar_chart, line_chart, scatter_plot, histogram, pie_chart
import matplotlib.pyplot as plt

bar_chart(["North", "South", "East"], [100, 60, 80], title="Sales by region")
line_chart([1, 2, 3, 4, 5], [10, 12, 9, 15, 14], title="Temperature over time")
scatter_plot([2, 4, 6, 8], [10, 14, 16, 18], title="Study hours vs grade")
histogram([2000, 2200, 2500, 2600, 2700, 4000, 4100], bins=5, title="Salary distribution")
pie_chart(["Rent", "Food", "Transport"], [60, 25, 15], title="Budget split")

plt.show()
