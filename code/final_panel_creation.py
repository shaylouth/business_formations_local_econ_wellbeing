"""
The purpose of this file is to merge together the cleaned datasets into 
the final panel dataset for analysis. This file will be updated as new datasets are cleaned
and ready to be incorporated.
"""

# #################################################################
# SETUP

import pandas as pd

# Files
estimation = pd.read_csv('data_clean/county_formations_estimation.csv',
                         dtype={'full_fips': str})

laus = pd.read_csv('data_clean/unemployment_WIP.csv',
                   dtype={'full_fips': str})

gini = pd.read_csv('data_intermediate/gini_panel.csv',
                   dtype={'full_fips': str})

# #################################################################
# VALIDATING MERGE KEYS

assert not laus.duplicated(
    subset=['full_fips', 'year']
).any()

assert not estimation.duplicated(
    subset=['full_fips', 'year']
).any()

assert not gini.duplicated(
    subset=['full_fips', 'year']
).any()

# #################################################################
# MERGING DATASETS

panel = pd.merge(estimation,
                 laus.drop(columns=['state', 'county']),
                 on=['full_fips', 'year'],
                 how='left',
                 indicator=False,
                 validate='one_to_one'
)

panel = pd.merge(panel.drop(columns='STATE_NAME'),
                 gini.drop(columns=['STATE_NAME', 'COUNTY_NAME', 'STATE']),
                 on=['full_fips', 'year'],
                 how='left',
                 indicator=True,
                 validate='one_to_one')

# #################################################################
# VALIDATING FINAL MERGED PANEL

assert not panel.duplicated(
    subset=['full_fips', 'year']).any()

# #################################################################
# FINAL CLEANUP & SAVING DATASET

# Dropping Bedford County (see project notes, 10/29/26)
panel = panel.loc[panel['full_fips'] != '51019']

# Reordering variables
panel = panel[['full_fips', 'year', 'COUNTY_NAME', 'STATE',
               'state_formations', 'state_apps', 'county_apps', 'county_forms_est',
               'unemployment_rate', 'months_observed_unemployment', 'katrina_incomplete',
               'gini', 'gini_margin_of_error']]

panel.to_csv('data_clean/panel.csv', index=False)