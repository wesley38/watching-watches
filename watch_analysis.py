# TODO: Parameterise script. Create data folder with CSV and text file with inputs to generate plots again.
import csv
import statistics

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def condition_plot(file_path, step, watch_name):
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
    countries = []

    prices_by_year = dict()
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.__next__()

        # Year, Price, Condition
        for row in reader:
            price = int(row[0].replace(",", ""))
            year = int(row[3])
            country = row[2]

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
            countries.append(country)

            if year not in prices_by_year:
                prices_by_year[year] = []

            prices_by_year[year].append(price)

    sns.set(style="whitegrid")
    df = pd.DataFrame({x_label: year_of_prods, y_label: prices, 'label': conditions})
    df2 = pd.DataFrame({x_label: year_of_prods, y_label: prices, 'label': countries})

    prices_by_year = {key: value for key, value in sorted(prices_by_year.items())}
    median_years = []
    median_prices = []
    for year in prices_by_year:
        median = statistics.median(prices_by_year[year])
        median_years.append(year)
        median_prices.append(median)

    facet = sns.lmplot(df, x=x_label, y=y_label, hue='label', fit_reg=False, legend=False, palette=palette)
    plt.plot(median_years, median_prices, marker='x', color='#E040FB', markersize=12, label='Median', linestyle='dashed')
    plt.legend(loc='upper left')
    plt.xticks(np.arange(min(year_of_prods), max(year_of_prods) + 1, 1), rotation=45)
    plt.yticks(np.arange(min(prices) // step * step, max(prices) // step * step + 1, step))
    plt.title(f"{watch_name} Pricing and Condition")
    plt.savefig("scatter.png", dpi=300, bbox_inches='tight')
    plt.plot()

    facet = sns.lmplot(df2, x=x_label, y=y_label, hue='label', fit_reg=False, legend=False)
    plt.legend(loc='upper left')
    plt.xticks(np.arange(min(year_of_prods), max(year_of_prods) + 1, 1), rotation=45, ha='right')
    plt.yticks(np.arange(min(prices) // step * step, max(prices) // step * step + 1, step))
    plt.title(f"{watch_name} Lister Country of Origin")
    plt.savefig("countries.png", dpi=300, bbox_inches='tight')

def main():
    # condition_plot("5740_20250126.csv", 10000, 'Patek Phillipe 5740/1G-001')
    # condition_plot("5711-011_20250126.csv", 10000, 'Patek Phillipe 5711/1A-011')
    condition_plot("5712-001_20250202.csv", 10000, 'Patek Phillipe 5712/1A-001')


main()