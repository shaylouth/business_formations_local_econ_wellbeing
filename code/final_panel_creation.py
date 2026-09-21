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

# #################################################################
# VALIDATING MERGE KEYS

assert not laus.duplicated(
    subset=['full_fips', 'year']
).any()

assert not estimation.duplicated(
    subset=['full_fips', 'year']
).any()

# #################################################################
# MERGING DATASETS

panel = pd.merge(estimation,
                 laus,
                 on=['full_fips', 'year'],
                 how='left',
                 indicator=True,
                 validate='one_to_one'
)

panel.to_csv('data_clean/panel.csv', index=False)