"""
Note: This file is currently a work in progress
This file completes the estimation of county-year business formations to produce the base of the panel for analysis.
"""

# #################################
# SETUP

# Packages
import pandas as pd

# Loading and inspecting datasets
state_forms = pd.read_csv('data_clean/annualized_state_formations.csv')
print('##########################')
print(state_forms.head())
state_apps = pd.read_csv('data_clean/state_apps_annual.csv')
print('##########################')
print(state_apps.head())
county_apps = pd.read_csv('data_clean/annual_county_applications.csv')
print('##########################')
print(county_apps.head())


# #################################
# MERGING DATASETS
 # one to many merge! put state-year in each county using state_fips and year

# #################################
# ESTIMATING COUNTY FORMATIONS