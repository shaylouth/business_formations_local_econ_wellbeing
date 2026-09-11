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
# DATA CLEANING

# Dropping unnecessary columns
laus = laus.drop(columns = [
    'area_type_code_x', 'area_type_code_y', 'display_level', 
    'selectable', '_merge', 'area_text', 'seasonal', 
    'footnote_codes_y', 'measure_code'
    ])

# Dropping annual average observations
laus = laus[laus['period'] != 'M13']

# Dropping Unnecessary Geographies (PR)
laus = laus[laus['state'] != 'PR']

# Adding 'DC' as the 'state' for District of Columbia to match other files
assert laus.loc[laus['state'].isna(), 'county'].unique().tolist() == ['District of Columbia']
laus = laus.fillna({'state':'DC'})


# Changing Alaska Borough/city labels to match FIPS
mask = laus['county'].str.endswith('Borough/city')
assert laus.loc[mask, 'county'].nunique() == 4 
    # Validates that this selects only the desired units

laus['county'] = laus['county'].str.replace(
    ' Borough/city',
    ' City and Borough',
    regex = False)


# Matching Anchorage, Alaska county name with FIPS
mask = laus['county'].str.endswith(' Borough/municipality')
assert laus.loc[mask, 'county'].nunique() == 1
    # Validating that this method selects only the desired unit
    
laus['county'] = laus['county'].str.replace(
   ' Borough/municipality',
   ' Municipality',
   regex = False 
)

# Changing City County Equivalents in California/Colorado/Pennsylvania/Hawaii to match FIPS
    # "x County/city" in LAUS vs "x County" in FIPS
mask = laus['county'].str.endswith(' County/city')
assert laus.loc[mask, 'county'].nunique() == 5
    # Validates that only the desired 5 county units are selected 

laus['county'] = laus['county'].str.replace(
    ' County/city',
    ' County',
    regex = False
)

# Changing "Nantucket County/town" to match "Nantucket County" in FIPS key
mask = laus['county'].str.endswith(' County/town')
assert laus.loc[mask, 'county'].nunique() == 1

laus ['county'] = laus['county'].str.replace(
    ' County/town',
    ' County',
    regex = False
)



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