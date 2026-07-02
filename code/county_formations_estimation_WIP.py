"""
This file completes the estimation of county-year business formations to produce the base of the panel for analysis.
"""

# #################################
# SETUP

# Packages
import pandas as pd

# Loading Datasets
state_forms = pd.read_csv('data_clean/annualized_state_formations.csv',
                           dtype={'full_fips': str, 'state_fips': str, 'county_fips': str})
state_apps = pd.read_csv('data_clean/state_apps_annual.csv',
                         dtype={'full_fips': str, 'state_fips': str, 'county_fips': str})
county_apps = pd.read_csv('data_clean/annual_county_applications.csv',
                          dtype={'full_fips': str, 'state_fips': str, 'county_fips': str})


# #################################
# MERGING DATASETS

# Merging state formations and state applications
state = pd.merge(state_forms, state_apps, on=['year', 'state_fips', 'STATE', 'STATE_NAME'])
assert state.groupby(['state_fips', 'year']).size().eq(1).all()

# Merging state dataframe with county applications
est = pd.merge(county_apps, state, on=['year', 'state_fips', 'STATE'], validate='many_to_one')
assert est.groupby(['full_fips', 'year']).size().eq(1).all()

# Columns Cleanup
est = est.reindex(columns = ['STATE', 'year', 'COUNTY_NAME', 'full_fips', 'state_formations', 'state_apps', 'county_apps', 'county_forms_est', 'state_fips', 'county_fips', 'STATE_NAME'])


# #################################
# ESTIMATING COUNTY FORMATIONS

# Correcting variable types
est['county_apps'] = pd.to_numeric(est['county_apps'], errors='coerce')

# Calculating estimated county formations
est['county_forms_est'] = (est['state_formations']/est['state_apps']) * est['county_apps']


# #################################
# SAVING DATASET
est.to_csv('data_clean/county_formations_estimation.csv', index=False)