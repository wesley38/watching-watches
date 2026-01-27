import csv
import statistics

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

file_path = "5740_20250126.csv"
x_label = "Year of Production"
y_label = "Price"

palette = {
    "New / Perfect": "#0288D1",
    "Sealed in box": "#388E3C",
    "Minor Defects": "#FBC02D",
    "Used": "#D32F2F"
}

year_of_prods = []
prices = []
conditions = []

prices_by_year = dict()
with open(file_path, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    reader.__next__()

    # Year, Price, Condition
    for row in reader:
        price = int(row[0].replace(",", ""))
        year = int(row[3])
        condition = "Bad"
        if row[1] == "0":
            condition = "Sealed in box"
        elif row[1] == "1":
            condition = "New / Perfect"
        elif row[1] == "2":
            condition = "Minor Defects"
        elif row[1] == "3":
            condition = "Used"
        elif row[1] == "4":
            condition = "Poor"

        year_of_prods.append(year)
        conditions.append(condition)
        prices.append(price)

        if year not in prices_by_year:
            prices_by_year[year] = []

        prices_by_year[year].append(price)

sns.set(style="whitegrid")
df = pd.DataFrame({x_label: year_of_prods, y_label: prices, 'label': conditions})

prices_by_year = {key: value for key, value in sorted(prices_by_year.items())}
median_years = []
median_prices = []
for year in prices_by_year:
    median = statistics.median(prices_by_year[year])
    median_years.append(year)
    median_prices.append(median)

step = 10000
facet = sns.lmplot(df, x=x_label, y=y_label, hue='label', fit_reg=False, legend=False, palette=palette)
plt.plot(median_years, median_prices, marker='x', color='#E040FB', markersize=12, label='Median')
plt.legend(loc='upper left')
plt.xticks(np.arange(min(year_of_prods), max(year_of_prods) + 1, 1))
plt.yticks(np.arange(min(prices) // step * step, max(prices) // step * step + 1, step))
plt.title('Patek Phillipe 5740/1G-001')
#plt.show()
plt.savefig("scatter.png", dpi=300, bbox_inches='tight')

