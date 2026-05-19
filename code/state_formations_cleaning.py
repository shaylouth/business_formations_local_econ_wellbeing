"""
File: state_formations_cleaning.py
Note: This file is still a work in progress (W-I-P) pending missing data handling
Purpose: cleans the complete Census Business Formation Statistics time series dataset and produces: 
    1. a state-year level dataset on business formations (Pending, W-I-P)
    2. a state-month level dataset on business formations as an intermediate file
"""

import pandas as pd

# Reading in Census Business Formation Statistics (BFS) complete time series dataset
df = pd.read_csv('data_raw/BFS-mf/BFS-mf.csv', skiprows=380)
    # Note: first 380 rows are useful data keys and notes

##########################################
# REMOVING UNNECESSARY DATA

# Dropping total U.S. observations and regional categories
df = df[~df['geo_idx'].isin([1,2,3,4,5])]

# Dropping non-seasonally adjusted data
df = df[df['is_adj']==1]

# Restricting to Business Formations data
df = df[df['dt_idx']==6]

# Restricting to period of interest
df = df[df['per_idx'] >= 13]

##########################################
# AGGREGATING OBSERVATIONS TO YEAR LEVEL

# Sorting by location, time
df = df.sort_values(by=['geo_idx','per_idx'])

# Defining year variable to aggregate by
df['year'] = 2005 + (df['per_idx'] - 13) // 12

# W-I-P note: 
# Deciding how to handle missing observations in the formations data before completing aggregation

##########################################
# CHECKING DATASET DETAILS

print(df.describe(include='all'))
print('###########################################')

# Inspecting missing values and data distribution by column
for col in df.columns:
    print("====", col, "====")
    print("dtype:", df[col].dtype)
    print("nunique:", df[col].nunique())
    print("missing:", df[col].isna().sum())
    print(df[col].value_counts(dropna=False).head(10))
    print("\n")

df.to_csv('data_intermediate/state_formations_Q8_monthly.csv', index=False)
