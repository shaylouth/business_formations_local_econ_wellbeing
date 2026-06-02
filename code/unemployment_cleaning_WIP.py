"""
This file will read in and clean the unemployment data from BLS LAUS.
"""

import pandas as pd

laus = pd.read_csv(
    "data_raw/la.data.64.County",
    sep="\t"
)


print(laus.head())

# laus.to_csv('data_clean/unemployment_WIP.csv', index=False)