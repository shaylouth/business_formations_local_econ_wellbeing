"""
This file cleans and reshapes the Census Business Formation Statistics county-level business 
application data and produces a county-year level business applications dataset, annual_county_applications.csv
"""

import pandas as pd

# Reading in raw BFS annual county-level business application data
df = pd.read_excel('data_raw/bfs_county_apps_annual.xlsx',
                   header = 2, 
                   dtype={'County Code': str, 'state_fips': str, 'county_fips': str})
                # dtype = str to preserve leading zeroes in FIPS codes

#######################################
# RESHAPING PANEL

# Reshaping data from wide to long form panel
df_long = pd.wide_to_long(
    df, 
    stubnames='BA', 
    i=['State', 'County', 'County Code', 'state_fips', 'county_fips'], 
    j='Year')

# Resetting index to keep location and time variables in the dataframe
df_long_complete = df_long.reset_index()   


#######################################
# CLEANUP & VALIDATION

# Renaming variables
df_long_complete = df_long_complete.rename(columns={'BA': 'county_apps', 'State': 'STATE', 'Year':'year', 'County':'COUNTY_NAME', 'County Code':'full_fips'})

# Final data validation
assert df_long_complete.groupby(['full_fips', 'year']).size().eq(1).all()
assert df_long_complete['full_fips'].str.len().eq(5).all()
assert df_long_complete['county_apps'].notna().all()

# Dropping geographic units excluded at this stage
excluded_geo_units = ['CT', 'PR']
df_long_complete = df_long_complete[~df_long_complete['STATE'].isin(excluded_geo_units)]

#######################################
# SAVING DATA
df_long_complete.to_csv('data_clean/annual_county_applications.csv', index=False)
