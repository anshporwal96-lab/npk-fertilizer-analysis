# Analysis of NPK Fertilizer Consumption, Nutrient Imbalance and Agricultural Productivity across Indian States

Capstone Mini Project, Python Programming Laboratory (316U50L301)
S.Y. B.Tech Computer Science and Business Systems, K. J. Somaiya School of Engineering, Somaiya Vidyavihar University

## Problem Statement

To analyze NPK fertilizer consumption across Indian states, identify nutrient imbalances, and examine its relationship with agricultural productivity.

## Team

| Name | Roll No. | Part of the project |
| --- | --- | --- |
| Ansh Porwal | 16015025056 | Relationship with productivity, statistical and outlier analysis |
| Subhojit Paul | 16015025054 | Fertilizer consumption, state-wise comparison |
| Jainam Raka | 16015025058 | Nutrient imbalance, individual N, P, K comparison |

**Guide:** Prof. Jasraj Bherwani

## Dataset

Official government data from *Agricultural Statistics at a Glance* (2020, 2022 and 2024-25 editions), Ministry of Agriculture & Farmers Welfare, Government of India:
https://desagri.gov.in/document-report-category/agriculture-statistics-at-a-glance/

We put `npk_state_panel_2017-18_to_2024-25.csv` together from these tables. It has 288 rows and 15 columns with N, P and K use, gross cropped area, foodgrain yield and irrigation for 35 States/UTs and All-India, from 2017-18 to 2024-25.

## Files

| File | Description |
| --- | --- |
| `npk_main.py` | Main program; runs the whole analysis |
| `npk_module.py` | User-defined module with all functions (loading, cleaning, analysis, statistics, graphs) |
| `npk_state_panel_2017-18_to_2024-25.csv` | Input dataset |
| `npk_clean_data.csv` | Cleaned data created by the program |
| `requirements.txt` | Python libraries needed |
| `graphs/` | The four graphs produced by the program |
| `report/NPK_Project_Report.pdf` | Project report |

## How to Run

```
pip install -r requirements.txt
python npk_main.py
```

Make sure the CSV file is in the same folder as the Python files.

## What the Program Does

1. Loads the dataset and cleans it. It keeps only the state rows and removes duplicates and missing values.
2. Works out fertilizer use per hectare, the share of N, P and K, and an imbalance index that shows how far each state is from the ideal 4 : 2 : 1 ratio.
3. Lists the top states by fertilizer use and by imbalance, and compares N, P and K use across states.
4. Checks whether fertilizer use and foodgrain yield are related (Pearson correlation) and looks for outliers (IQR method).
5. Draws four graphs: fertilizer use per hectare, nutrient shares, fertilizer use vs yield, and the yearly trend.

## Key Results (2022-23)

- Among major farming states, Andhra Pradesh (262 kg/ha), Punjab (227 kg/ha) and Bihar (225 kg/ha) use the most fertilizer per hectare.
- The average nitrogen share is 69.3 %, against the ideal 57.1 %. Punjab and Haryana have potash shares below 2 %.
- States that use more fertilizer do get somewhat higher yields (r = 0.377, p < 0.001), but the link is weak, so fertilizer alone doesn't explain productivity.

## Libraries Used

Pandas, NumPy, Matplotlib, Seaborn, SciPy
