"""
This file cleans the historical quarterly Census Business Formation Statistics time series data
to produce the intermediate file:
    1. bfs_historic_annual_state_formations.csv
"""
# SETUP
#---------------------------------------------
import pandas as pd
df = pd.read_csv('data_raw/bfs_quarterly.csv')


# RESTRICTING FULL TIME SERIES TO DATA NEEDED
#---------------------------------------------
# Restricting to BF_BF8Q series (business formations within 8 quarters)
formations = df[df['series']=='BF_BF8Q']

# Restricting to non-seasonally adjusted data
formations = formations[formations['sa']=='U']

# Dropping aggregated country and region total observations
regions = 'US', 'NO', 'MW', 'SO', 'WE'
for region in regions:
    formations = formations[formations['geo']!=region]

# Dropping incomplete years
formations = formations[formations['year']!=2004]


# VERIFYING COMPLETENESS OF RESULTING DATASET
#---------------------------------------------
print(formations.isna().sum()) # NO MISSING VALUES! :D
print(formations['year'].max()) # Goes until 2014 as predicted by FRED data browser


# AGGREGATING TO YEAR LEVEL 
#---------------------------------------------
quarters = ['Q1', 'Q2', 'Q3', 'Q4']

# Updating variable type
formations[quarters] = formations[quarters].astype('int64')

# Creating aggregated yearly state_formations variable 
formations['state_formations'] = formations[quarters].sum(axis=1)


# STANDARDIZING GEOGRAPHIC INDEX
#---------------------------------------------
# Renaming geo variable to match key file variable name
formations = formations.rename(columns = {'geo': 'STATE'})

# Reading and merging in geographic index key file
geo_id = pd.read_csv('data_intermediate/state_geo_id.csv')
formations = pd.merge(geo_id, formations, on='STATE')


# DROPPING REMAINING EXTRA VARIABLES
#---------------------------------------------
# Saving full dataset for validtion of post-2014 suppressed data handling methods
formations.to_csv('data_intermediate/quarterly_state_formations.csv')

formations = formations.drop(columns = ['geo_idx', 'sa', 'series'] + quarters)


# SAVING DATASET
#---------------------------------------------
print(formations.head())
formations.to_csv('data_intermediate/bfs_historic_annual_state_formations.csv', index=False)

