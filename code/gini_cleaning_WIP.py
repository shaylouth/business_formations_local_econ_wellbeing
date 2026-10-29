"""
This file combines yearly gini index files into a panel, cleans and standardizes this panel,
and adds in the geographic crosswalk
"""

import pandas as pd
import glob
from pathlib import Path

################# COMBINING YEARLY FILES INTO ONE FILE #####################

# Collecting list of filenames of gini index files 
CSVs = glob.glob('data_raw/gini/*Data.csv')

# List to hold dataframes to be concatenated
df_list = []

# Looping over files
for file in CSVs:
    df = pd.read_csv(file, header = 1)
    
    # NOTE: ADD DATA VALIDATION CHECKS
        # maybe check row count for each file to ensure standardized
    
    # Dropping empty columns created in read_csv
    df = df.dropna(axis=1, how='all')

    # Slicing year out of filename to make year variable
    filename = Path(file).name
    file_year = filename[7:11] 
    assert 2006 <= int(file_year) <= 2026
    df['year'] = int(file_year)

    # Saving each dataframe in list
    df_list.append(df)

# Concatenating all years, sorting panel by year 
panel = pd.concat(df_list, ignore_index=True)
panel = panel.sort_values(by=['year','Geographic Area Name'])


################# GEOGRAPHIC STANDARDIZATION & CLEANING #####################
# Obtaining separated county and state names
panel[['COUNTY_NAME', 'STATE_NAME']] = panel['Geographic Area Name'].str.split(', ', expand=True)

# Removing excluded states from dataset
excluded_geo_units = ['Puerto Rico', 'Connecticut', 'Alaska']
panel = panel[~panel['STATE_NAME'].isin(excluded_geo_units)]

# Geographic Standardization for geographic crosswalk merge
#  ['Bedford city', 'Do?a Ana County', 'La Salle Parish', 'Shannon County']

# Dropping Bedford city
    # NOTE: need to recalculate gini for combined Bedford city/county to fit geographic standardization
    # dropping bedford city here in first stage of analysis
    # Dropping bedford county across all datasets in final panel construction stage for easy reversal
panel = panel[~((panel['COUNTY_NAME'] == 'Bedford city') & (panel['STATE_NAME'] == 'Virginia'))]

# Correcting Doña Ana County string error from 2010 ACS file
panel.loc[
    (panel['COUNTY_NAME'] == 'Do?a Ana County') &
    (panel['STATE_NAME'] == 'New Mexico'), 'COUNTY_NAME'
] = 'Doña Ana County'

# Correcting LaSalle Parish, LA string error from 2010 and 2011 gini files
panel.loc[
    (panel['COUNTY_NAME'] == 'La Salle Parish') &
    (panel['STATE_NAME'] == 'Louisiana'), 'COUNTY_NAME'
] = 'LaSalle Parish'

# Standardizing Shannon County/Oglala Lakota County name to Oglala Lakota County
panel.loc[
    (panel['COUNTY_NAME'] == 'Shannon County') &
    (panel['STATE_NAME'] == 'South Dakota'), 'COUNTY_NAME'
] = 'Oglala Lakota County'


################# MERGING GEOGRAPHIC CROSSWALK #####################

# Merging in geographic crosswalk
fips = pd.read_csv('data_intermediate/county_geo_id.csv',
                   dtype={'full_fips': str,
                        'state_fips': str,
                        'county_fips': str})

gini = pd.merge(panel,
                 fips,
                 on=['COUNTY_NAME', 'STATE_NAME'],
                 how='left',
                 indicator=True
)

# Validating merge
assert gini.loc[gini['_merge'] == 'left_only'].empty # no unmatched counties
assert gini[gini.duplicated(keep=False, subset=['year', 'full_fips'])].empty # no county-year duplicates


################# SAVING DATA #####################
gini.to_csv('data_intermediate/gini_panel.csv', index=False)