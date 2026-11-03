
# Main program for NPK Fertilizer Analysis

import npk_module as nm

try:
    states = nm.load_data()

    print("NPK FERTILIZER ANALYSIS")

    states = nm.clean_data(states)

    if states.empty:
        print("No valid state data found.")

    else:
        states.to_csv("npk_clean_data.csv", index=False)

        nm.consumption_analysis(states)
        nm.imbalance_analysis(states)
        nm.productivity_analysis(states)

        nm.state_comparison(states)
        nm.individual_npk_comparison(states)
        nm.statistical_analysis(states)
        nm.outlier_analysis(states)

        nm.show_graphs(states)

except FileNotFoundError as error:
    print("CSV file not found:", error.filename)
    print("Keep the state-wise CSV file in the same folder.")
