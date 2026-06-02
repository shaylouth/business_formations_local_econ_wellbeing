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

# Merging state formations and state applications
state = pd.merge(state_forms, state_apps, on=['year', 'state_fips'])
# print(state.head())

# Merging state dataframe with county applications
est = pd.merge(county_apps, state, on=['year', 'state_fips'], validate='many_to_one')
print(est.head())

# Columns Cleanup
est = est.drop(columns=['STATE_y', 'STATE_x', 'STATE_NAME_y', 'County Code'])
est = est.rename(columns={'STATE_NAME_x':'STATE_NAME', 'County': 'county'})
est = est.reindex(columns = ['STATE', 'year', 'county', 'state_formations', 'state_apps', 'county_apps', 'state_fips', 'county_fips', 'STATE_NAME'])


# #################################
# ESTIMATING COUNTY FORMATIONS

# # Correcting variable types
# est['county_apps'] = est['county_apps'].astype('float64')
print('#####################################################################')
est['county_apps'] = pd.to_numeric(est['county_apps'], errors='coerce')
print(est['county_apps'].isna().sum())
print('#####################################################################')
print(est['county_apps'].dtype)
print('#####################################################################')
print(type(est['county_apps'].iloc[0]))
print('#####################################################################')


# Calculating estimated county formations
est['county_forms_est'] = (est['state_formations']/est['state_apps']) * est['county_apps']

print(est.dtypes)

# #################################
# SAVING DATASET

ann = est.copy()
# Inspecting missing values and data distribution by column
for col in ann.columns:
    print("====", col, "====")
    print("dtype:", ann[col].dtype)
    print("nunique:", ann[col].nunique())
    print("missing:", ann[col].isna().sum())
    print(ann[col].value_counts(dropna=False).head(10))
    print("\n")

est.to_csv('data_clean/county_formations_estimation', index=False)