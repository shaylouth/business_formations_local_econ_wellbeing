"""
This file will read in and clean the unemployment data from the Bureau of Labor Statistics' Local Area Unemployment Statistics.
"""

# #################################################
# SETUP

# Packages
import pandas as pd

# Loading in data
laus = pd.read_csv(
    "data_raw/LAUS/la.data.64.County",
    sep="\t"
)

area = pd.read_csv(
    "data_raw/LAUS/la.area",
    sep="\t"
)

series = pd.read_csv(
    "data_raw/LAUS/la.series",
    sep="\t"
)

# #################################################
# SERIES METADATA PREPARATION AND MERGING

# Stripping extra spaces in file column names
laus.columns = laus.columns.str.strip()
series.columns = series.columns.str.strip()

# Merging in series metadata
laus = pd.merge(laus, series, on=('series_id'), indicator=True)

# Dropping unnecessary measures (unemployment rate = 03)
laus = laus[laus['measure_code'] == 3]

# Restricting to county/county-equivalents (counties and equivalents = F)
laus = laus[laus['area_type_code'] == 'F']

# #################################################
# AREA METADATA PREPARATION & MERGING

# Stripping column names
area.columns = area.columns.str.strip()

# Restricting to county/county-equivalents subset
area = area[area['area_type_code'] == 'F']

# Separating county and state names to later merge in geographic index on
area[['county', 'state']] = area['area_text'].str.split(', ', expand=True)

laus = pd.merge(laus, area, on=('area_code'))

# #################################################
# CLEANING FULL DATASET

# Dropping unnecessary columns
laus = laus.drop(columns = [
    'area_type_code_x', 'area_type_code_y', 'display_level', 
    'selectable', '_merge', 'area_text', 'seasonal', 
    'footnote_codes_y', 'measure_code'
    ])

# Dropping annual average observations
laus = laus[laus['period'] != 'M13']

# Adding 'DC' as the 'state' for District of Columbia to match other files
assert laus.loc[laus['state'].isna(), 'county'].unique().tolist() == ['District of Columbia']
laus = laus.fillna({'state':'DC'})

# #################################################
# MERGING IN FIPS

fips = pd.read_csv('data_intermediate/state_geo_id.csv')
# laus = pd.merge(laus, fips, left_on='county', right_on='COUNTY_NAME', how='outer', indicator=True)


# #################################################
# AGGREGATING TO YEAR LEVEL


# #################################################
# CHECKING & SAVING DATASET

print('Final Check #################################')
print(laus.head())

laus.to_csv('data_clean/unemployment_WIP.csv', index=False)