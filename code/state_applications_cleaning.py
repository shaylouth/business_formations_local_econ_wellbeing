"""
This file cleans the complete Census Business Formation Statistics time series dataset and produces: 
    1. a state-year level dataset on business applications
    2. a state-month level dataset on business applications as an intermediate file
"""

import pandas as pd

# Reading in Census Business Formation Statistics (BFS) complete time series dataset
df = pd.read_csv('data_raw/BFS-mf/BFS-mf.csv', skiprows=392)
    # reproducibility note: adjust skiprows value accordingly depending on BFS time series download


##########################################
# REMOVING UNNECESSARY DATA, CLEANING NECESSARY DATA

# Dropping total U.S. observations and regional categories
df = df[~df['geo_idx'].isin([1,2,3,4,5])]

# Dropping non-seasonally adjusted data
df = df[df['is_adj']==1]

# Restricting to Business Applications data
df_applications = df[df['dt_idx']==1]

# Restricting to period of interest
df_applications = df_applications[df_applications['per_idx'] <= 204]
df_applications = df_applications[df_applications['per_idx'] >= 13]

# Adjusting state_applications varname and vartype
df_applications = df_applications.rename(columns={'val': 'state_apps'})
df_applications['state_apps'] = df_applications['state_apps'].astype('float64')


##########################################
# ADDING STANDARDIZED GEOGRAPHIC INDEX (state fips)

# Reading in geographic index standardization file (contains state indexes from all different sources)
geo_id = pd.read_csv('data_intermediate/state_geo_id.csv')

# Merging in state_geo_id.csv to add state_fips
df_applications = pd.merge(df_applications, geo_id, on="geo_idx")
    # extra indexes are dropped in aggregation step below

##########################################
# AGGREGATING OBSERVATIONS TO YEAR LEVEL

# Sorting by location, time
df_applications = df_applications.sort_values(by=['state_fips','per_idx'])

# Defining year variable to aggregate by
df_applications['year'] = 2005 + (df_applications['per_idx'] - 13) // 12

# Aggregating by year and state
df_grouped = df_applications.groupby(['state_fips', 'year'])
df_agg = df_grouped.agg({
    'state_apps': 'sum',
    'STATE': 'first',
    'STATE_NAME': 'first'
})

df_agg = df_agg.reset_index()

# Manually validate year assignment and value aggregation before dropping extra variables
print(df_agg.head()) 


##########################################
# CHECKING DATASET DETAILS

print(df_agg.describe(include='all'))
print('###########################################')

# Inspecting missing values and data distribution by column
for col in df_agg.columns:
    print("====", col, "====")
    print("dtype:", df_agg[col].dtype)
    print("nunique:", df_agg[col].nunique())
    print("missing:", df_agg[col].isna().sum())
    print(df_agg[col].value_counts(dropna=False).head(10))
    print("\n")


##########################################
# SAVING DATASETS
df_applications.to_csv('data_intermediate/state_apps_monthly.csv', index=False)
df_agg.to_csv('data_clean/state_apps_annual.csv', index=False)