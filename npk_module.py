#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# Load the dataset
def load_data():
    states = pd.read_csv("npk_state_panel_2017-18_to_2024-25.csv")
    return states

# Clean data and calculate values
def clean_data(data):
    data = data[data["Row_Type"] == "State/UT"].copy()
    data = data.drop_duplicates(["State_UT", "Year"])

    cols = ["N_000t", "P_000t", "K_000t", "Gross_Cropped_Area_000ha", "Foodgrain_Yield_kg_ha"]
    for col in cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(subset=["N_000t", "P_000t", "K_000t","Gross_Cropped_Area_000ha"])
    data["NPK_Total"] = (data["N_000t"] + data["P_000t"] + data["K_000t"])
    data["NPK_kg_ha"] = (data["NPK_Total"] /data["Gross_Cropped_Area_000ha"] * 1000)

    total = data["NPK_Total"].replace(0, np.nan)

    for nutrient in ["N", "P", "K"]:
        data[nutrient + "_share"] = (
            data[nutrient + "_000t"] / total * 100
        )

    # Compare nutrient shares with the 4:2:1 reference ratio
    data["Imbalance"] = (abs(data["N_share"] - 400 / 7) + abs(data["P_share"] - 200 / 7) + abs(data["K_share"] - 100 / 7)) / 2
    return data

# Analyze fertilizer consumption
def consumption_analysis(data):
    year = data["Year"].max()
    latest = data[data["Year"] == year]
    print("\nLatest usable year:", year)
    print("\nTop 5 states by NPK use per hectare:")
    print(latest.nlargest(5, "NPK_kg_ha")[["State_UT", "NPK_kg_ha"]].to_string(index=False))

# Analyze nutrient imbalance
def imbalance_analysis(data):
    latest = data[data["Year"] == data["Year"].max()]
    print("\nTop 5 states by nutrient imbalance:")

    print(
        latest.nlargest(5, "Imbalance")[
            ["State_UT", "N_share", "P_share", "K_share", "Imbalance"]
        ].round(2).to_string(index=False)
        )

# Analyze fertilizer use and crop yield
def productivity_analysis(data):
    valid = data.dropna(subset=["NPK_kg_ha", "Foodgrain_Yield_kg_ha"])
    correlation = valid["NPK_kg_ha"].corr(valid["Foodgrain_Yield_kg_ha"])

    print("\nCorrelation between fertilizer use and yield:",round(correlation, 3))
    print("Correlation shows a relationship, not proof of cause and effect.")

# Display graphs
def show_graphs(data):
    year = data["Year"].max()
    latest = data[data["Year"] == year].nlargest(10, "NPK_kg_ha")

    # Graph 1: State-wise fertilizer use
    sns.barplot(data=latest, x="NPK_kg_ha", y="State_UT")
    plt.title("Top States by NPK Use per Hectare")
    plt.xlabel("NPK Use (kg/ha)")
    plt.tight_layout()
    plt.show()

    # Graph 2: Nutrient shares
    latest[["N_share", "P_share", "K_share"]].set_index(
        latest["State_UT"]
    ).plot(kind="bar")
    plt.title("NPK Nutrient Shares by State")
    plt.ylabel("Share (%)")
    plt.tight_layout()
    plt.show()

    # Graph 3: Fertilizer use versus crop yield
    valid = data.dropna(subset=["NPK_kg_ha", "Foodgrain_Yield_kg_ha"])
    sns.scatterplot(
        data=valid,
        x="NPK_kg_ha",
        y="Foodgrain_Yield_kg_ha"
    )
    plt.title("Fertilizer Use vs Crop Yield")
    plt.xlabel("NPK Use (kg/ha)")
    plt.ylabel("Foodgrain Yield (kg/ha)")
    plt.tight_layout()
    plt.show()

    # Graph 4: Yearly fertilizer consumption trend
    yearly = data.groupby("Year")["NPK_kg_ha"].mean()
    yearly.plot(kind="line", marker="o")
    plt.title("Yearly Average NPK Use per Hectare")
    plt.xlabel("Year")
    plt.ylabel("Average NPK Use (kg/ha)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Compare fertilizer use across states
def state_comparison(data):
    year = data["Year"].max()
    latest = data[data["Year"] == year]

    highest = latest.loc[latest["NPK_kg_ha"].idxmax()]
    lowest = latest.loc[latest["NPK_kg_ha"].idxmin()]
    average = latest["NPK_kg_ha"].mean()

    print("\nSTATE-WISE COMPARISON")
    print("Highest fertilizer use:", highest["State_UT"])
    print("Value:", round(highest["NPK_kg_ha"], 2), "kg/ha")
    print("\nLowest fertilizer use:", lowest["State_UT"])
    print("Value:", round(lowest["NPK_kg_ha"], 2), "kg/ha")
    print("\nAverage fertilizer use:", round(average, 2), "kg/ha")

# Compare individual nutrient consumption across states
def individual_npk_comparison(data):
    year = data["Year"].max()
    latest = data[data["Year"] == year]
    nutrients = ["N_000t", "P_000t", "K_000t"]
    print("\nINDIVIDUAL NPK CONSUMPTION COMPARISON")
    print("Latest usable year:", year)

    for nutrient in nutrients:
        print("\nTop 5 states for", nutrient)

        result = latest.nlargest(5, nutrient)
        print(result[["State_UT", nutrient]].to_string(index=False))

# Perform statistical analysis
def statistical_analysis(data):
    valid = data.dropna(subset=["NPK_kg_ha", "Foodgrain_Yield_kg_ha"])

    if len(valid) < 2:
        print("\nNot enough data for statistical analysis.")
        return

    correlation, p_value = pearsonr(valid["NPK_kg_ha"],valid["Foodgrain_Yield_kg_ha"])
    print("\nSTATISTICAL ANALYSIS")
    print("Pearson Correlation:", round(correlation, 3))
    print("P-value:", round(p_value, 5))

    if p_value < 0.05:
        print("The relationship is statistically significant.")
    else:
        print("The relationship is not statistically significant.")

    print("Correlation does not prove causation.")

# Identify possible outliers using IQR
def outlier_analysis(data):
    print("\nOUTLIER ANALYSIS")
    columns = ["NPK_kg_ha", "Foodgrain_Yield_kg_ha"]

    for col in columns:
        values = data[col].dropna()

        if len(values) < 2:
            print("Not enough data for:", col)
            continue

        Q1 = values.quantile(0.25)
        Q3 = values.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = values[(values < lower) | (values > upper)]
        print("\nColumn:", col)
        print("Number of possible outliers:", len(outliers))

    print("\nOutliers are identified but not removed.")
