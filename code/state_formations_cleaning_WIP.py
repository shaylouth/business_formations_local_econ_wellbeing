"""
Note: This file is still a work in progress (WIP) pending suppressed data handling
This file cleans the complete Census Business Formation Statistics time series dataset to produce: 
    1. a state-year level dataset on business formations (Pending, WIP)
    2. a state-month level dataset on business formations as an intermediate file
"""

import pandas as pd
import numpy as np
import missingno as msno
import matplotlib.pyplot as plt

# Reading in Census Business Formation Statistics (BFS) complete time series dataset
df = pd.read_csv('data_raw/BFS-mf/BFS-mf.csv', skiprows=392)
    # Note: first 392 rows are useful data keys and notes
    # reproducibility note: adjust skiprows value accordingly depending on BFS time series download

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
# ADJUSTING VARNAMES, VARTYPES, AND CONVERTING MISSING VALUES

# Converting supressed ('D') observations to missing
df['val'] = df['val'].replace('D', np.nan)

# Renaming and converting state_formations to numeric type
df['val'] = df['val'].astype('float64')
df = df.rename(columns = {'val': 'state_formations'})

##########################################
# ADDING STANDARDIZED GEOGRAPHIC INDEX (state fips)

# Reading in geographic index standardization file (contains state indexes from all different sources)
geo_id = pd.read_csv('data_intermediate/state_geo_id.csv')

# Merging in state_geo_id.csv to add state_fips
df = pd.merge(df, geo_id, on="geo_idx")

##########################################
# AGGREGATING OBSERVATIONS TO YEAR LEVEL

# Sorting by location, time
df = df.sort_values(by=['geo_idx','per_idx'])

# Defining year variable to aggregate and later merge by
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




