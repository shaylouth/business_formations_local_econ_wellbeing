"""
File: county_applications_cleaning.py 
Purpose: cleans and reshapes the Census Business Formation Statistics county-level business 
application data and produces: 
    1. a county-year level business applications dataset
"""

import pandas as pd
import openpyxl

# Reading in raw BFS annual county-level business application data
df = pd.read_excel('data_raw/bfs_county_apps_annual.xlsx', header = 2)
print(df.head())

# Reshaping data from wide to long form panel
df_long = pd.wide_to_long(
    df, 
    stubnames='BA', 
    i=['State', 'County', 'County Code', 'state_fips', 'county_fips'], 
    j='Year')

# Resetting index to keep location and time variables in the dataframe
df_long_complete = df_long.reset_index()   

# Renaming variable
df_long_complete = df_long_complete.rename(columns={'BA': 'Applications'})
print(df_long_complete.head())


df_long_complete.to_csv('data_clean/annual_county_applications.csv', index=False)
