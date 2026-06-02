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

# Dropping seasonally adjusted data
df = df[df['is_adj']==0]

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


##############################################################
# ADDING STANDARDIZED GEOGRAPHIC INDEX (state fips) AND YEAR

# Reading in geographic index standardization file (contains state indexes from all different sources)
geo_id = pd.read_csv('data_intermediate/state_geo_id.csv')

# Merging in state_geo_id.csv to add state_fips
df = pd.merge(df, geo_id, on="geo_idx")

# Sorting by location, time
df = df.sort_values(by=['geo_idx','per_idx'])

# Defining year variable
df['year'] = 2005 + (df['per_idx'] - 13) // 12


##########################################
# QUICK COLUMNS CLEANUP
df = df.drop(columns = ['geo_idx', 'dt_idx', 'cat_idx', 'is_adj'])


##########################################
# DEALING WITH SUPPRESSED DATA PART 1

# Dropping observations from 2014 and earlier
df = df.drop(df[df['year']<=2014].index)

# Defining number of missing observations per state-year group
df['year_state_missing_count'] = df['state_formations'].isna().groupby([df['year'], df['STATE']]).transform('sum')

# Coverting all state_formations observations to NaN for years with 3 or more suppressed months
df.loc[df['year_state_missing_count'] >= 3, 'state_formations'] = pd.NA


##########################################
# AGGREGATING OBSERVATIONS TO YEAR LEVEL - ANNUALIZATION METHOD

# Using new dataframe for annualization method
ann = df.copy() 

# Aggregating by state-year sums
ann = ann.groupby(['year', 'state_fips']).agg({
    'state_formations': lambda x: x.sum(min_count=1),
    'STATE':'first',
    'STATE_NAME':'first',
    'year_state_missing_count':'first'
    }).reset_index()

# Applying annualization rule (will not impact complete years or missing years!)
ann['ann_state_formations'] = ann['state_formations'] * (12/(12-ann['year_state_missing_count']))


##########################################
# APPENDING WITH COMPLETE PRE-2015 DATA

# Prepparing annualized dataset to append
ann = ann.drop(columns = ['state_formations'])
ann = ann.rename(columns={'ann_state_formations':'state_formations'})

# Loading in aggregated quarterly pre-2015 data
pre_2015 = pd.read_csv('data_intermediate/bfs_historic_annual_state_formations.csv')

# Combining data for complete state_formations file
final = pd.concat([pre_2015, ann], ignore_index=True)


##########################################
# CHECKING DATASET DETAILS

# Comparing pre-aggregation/annualization data with post-aggregation data
print(df.describe(include='all'))
print('###########################################')
print(ann.describe(include='all'))
print('###########################################')

# Inspecting missing values and data distribution by column
for col in ann.columns:
    print("====", col, "====")
    print("dtype:", ann[col].dtype)
    print("nunique:", ann[col].nunique())
    print("missing:", ann[col].isna().sum())
    print(ann[col].value_counts(dropna=False).head(10))
    print("\n")


##########################################
# SAVING DATASETS

df.to_csv('data_intermediate/state_formations_Q8_monthly.csv', index=False)
final.to_csv('data_clean/annualized_state_formations.csv', index = False)