"""
File: state_applications_cleaning.py 
Purpose: cleans the complete Census Business Formation Statistics time series dataset and produces: 
    1. a state-year level dataset on business applications
    2. a state-month level dataset on business applications as an intermediate file
"""

import pandas as pd

# Reading in Census Business Formation Statistics (BFS) complete time series dataset
df = pd.read_csv('data_raw/BFS-mf/BFS-mf.csv', skiprows=380)

##########################################
# REMOVING UNNECESSARY DATA

# Dropping total U.S. observations and regional categories
df = df[~df['geo_idx'].isin([1,2,3,4,5])]

# Dropping non-seasonally adjusted data
df = df[df['is_adj']==1]

# Restricting to Business Applications data
df_applications = df[df['dt_idx']==1]

# Restricting to period of interest
df_applications = df_applications[df_applications['per_idx'] <= 204]
df_applications = df_applications[df_applications['per_idx'] >= 13]

##########################################
# AGGREGATING OBSERVATIONS TO YEAR LEVEL

# Sorting by location, time
df_applications = df_applications.sort_values(by=['geo_idx','per_idx'])

# Defining year variable to aggregate by
df_applications['year'] = 2005 + (df_applications['per_idx'] - 13) // 12

# Aggregating by year and state
df_grouped = df_applications.groupby(['geo_idx', 'year'])
df_agg = df_grouped.sum()
df_agg = df_agg.reset_index()
print(df_agg.head())

# Dropping extra columns
df_agg = df_agg.drop(['per_idx', 'cat_idx', 'dt_idx', 'is_adj'], axis = 1)

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

df_applications.to_csv('data_intermediate/state_apps_monthly.csv', index=False)
df_agg.to_csv('data_clean/state_apps_annual.csv', index=False)
import sys
print(sys.executable)