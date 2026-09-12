"""
This file creates a standardized geographic index to use across files 
from different data sources. I take the BFS 'geo_idx' key and match it with
state FIPS codes, and then add both into a county FIPS codes file to create:
    1. state_geo_id.csv (geographic crosswalk for state-level datasets)
    2. county_geo_id.csv (geographic crosswalk for county-level datasets)
"""

import pandas as pd

################ BFS GEOGRAPHIC INDEX ###################
# Extracting geo_idx key from Census Business Formation Statistics (BFS) Complete Time Series Dataset
bfs = pd.read_csv('data_raw/BFS-mf/BFS-mf.csv', skiprows=43, nrows=57)
bfs = bfs.rename(columns={'geo_code': 'STATE'})
print(bfs.head())



################# State FIPS Codes ###################
# Reading in State FIPS Codes from Census.gov
state_fips = pd.read_csv(
    "https://www2.census.gov/geo/docs/reference/codes2020/national_state2020.txt",
    sep="|", 
        dtype={
        "STATEFP": str
    })
print(state_fips.head())

# Merging with bfs geo_idx key by State Abreviation ("STATE")
state_id = pd.merge(state_fips, bfs, on="STATE")

# Dropping extra columns and updating State FIPS variable name
state_id = state_id.drop(columns = ['geo_desc', 'STATENS'])
state_id = state_id.rename(columns = {'STATEFP': 'state_fips'})

# Saving resulting file to merge with intermediate files
print(state_id.head())
state_id.to_csv('data_intermediate/state_geo_id.csv', index=False)



################# County FIPS Codes ###################
# Reading in County FIPS Codes from Census.gov
county_fips = pd.read_csv(
    "https://www2.census.gov/geo/docs/reference/codes2020/national_county2020.txt",
    sep="|",
    dtype={
        "STATEFP": str,
        "COUNTYFP": str
    })


# Updating variable names and dropping unnecessary variables
county_fips = county_fips.rename(columns = {'STATEFP': 'state_fips', 'COUNTYFP': 'county_fips', 'COUNTYNAME': 'COUNTY_NAME'})
county_fips = county_fips.drop(columns = ['CLASSFP', 'FUNCSTAT', 'COUNTYNS'])
print(county_fips.head())

# Creating county-level geographic index file with County FIPS, State FIPS, and BFS State 'geo_idx'
county_id = pd.merge(county_fips, state_id, on='state_fips')

# Dropping unnecessary columns and standardizing variable names
county_id = county_id.drop(columns = ['STATE_y'])
county_id = county_id.rename(columns = {'STATE_x': 'STATE'})
print(county_id.head())



################# Creating Unique County 5-digit FIPS Codes ###################
# Adding combined 5 digit state+county fips for unique a county identifier
county_id['full_fips'] = county_id['state_fips'] + county_id['county_fips']
print(county_id.head())

################# Creating Simplified County Names ###################
# Creating a second county_names variable stripping diacritics/accents and capitalization for
# matching with other files without diacritics/accents

# NOTE: This version was written with a focus on practicing new pandas string cleaning skills, 
# will update with different method to address all diacritics/accents later

county_id['county_name_match'] = county_id['COUNTY_NAME'].str.lower()

mask = county_id['county_name_match'].str.contains('ñ')
print(county_id.loc[mask, 'county_name_match'].nunique())
print(county_id.loc[mask, 'county_name_match'].unique())

county_id['county_name_match'] = county_id['county_name_match'].str.replace(
    'ñ',
    'n',
    regex = False
)

assert not county_id['county_name_match'].str.contains('ñ').any()


################# Final Dataset Restriction ###################
# Dropping unnecessary geographic units that are excluded from the analysis at the present stage
excluded_states = ['CT', 'PR']

county_id = county_id[~county_id['STATE'].isin(excluded_states)]
state_id = state_id[~state_id['STATE'].isin(excluded_states)]

# Saving resulting file to merge with intermediate data
county_id.to_csv('data_intermediate/county_geo_id.csv', index=False)