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
# DATA CLEANING

# Renaming variables
df_long_complete = df_long_complete.rename(columns={'BA': 'county_apps', 'State': 'STATE', 'Year':'year', 'County':'COUNTY_NAME', 'County Code':'full_fips'})

# Dropping geographic units excluded at this stage
excluded_geo_units = ['CT', 'PR', 'AK']
df_long_complete = df_long_complete[~df_long_complete['STATE'].isin(excluded_geo_units)]

# Getting rid of blanks for missing data
df_long_complete['county_apps'] = df_long_complete['county_apps'].str.strip()
df_long_complete['county_apps'] = pd.to_numeric(df_long_complete['county_apps'], errors='raise')



#######################################
# GEOGRAPHIC HISTORY CLEANUP
# NOTE: see geo_hist_issues.ipynb for detailed explanations of the following cleaning steps

##### Shannon County/Oglala Lakota County ######
# Renaming/recoding historical Shannon County, SD to Oglala Lakota County
df_long_complete.loc[(df_long_complete['COUNTY_NAME'] == 'Shannon County') & (df_long_complete['STATE'] == 'SD'),
                      ['COUNTY_NAME', 'full_fips', 'state_fips', 'county_fips']] = ['Oglala Lakota County', '46102', '46', '102']

# Dropping remaining empty years
condition = ((df_long_complete['COUNTY_NAME'] == 'Oglala Lakota County') & 
             (df_long_complete['STATE'] == 'SD') & 
             (df_long_complete['county_apps'].isna()))
df_long_complete = df_long_complete.loc[~condition]


##### Bedford City / Bedford County, VA ######
# Separating out bedford city and county 
bedford_city = df_long_complete.loc[df_long_complete['COUNTY_NAME'] == 'Bedford city']
bedford_county = df_long_complete.loc[(df_long_complete['COUNTY_NAME'] == 'Bedford County') &
                                      (df_long_complete['STATE'] == 'VA')]

# Merging the two by year
bedford_combined = bedford_county[
    ['year', 'STATE', 'COUNTY_NAME', 'full_fips', 'county_apps']
    ].merge(bedford_city[['year', 'county_apps']],
            on='year',
            how='left',
            suffixes=('_county', '_city'))

# Calculating combined bedford city & bedford county applications
bedford_combined['bedford_combined_apps'] = (
    bedford_combined['county_apps_county'] + bedford_combined['county_apps_city'].fillna(0))

# Replacing Bedford City County Applications with the combined data in the main dataset
df_long_complete = df_long_complete.merge(bedford_combined[['full_fips', 'year', 'bedford_combined_apps']],
                                          on=['full_fips', 'year'],
                                          how='left')

df_long_complete.loc[
    (df_long_complete['COUNTY_NAME'] == 'Bedford County') & # Selecting county_apps
    (df_long_complete['STATE'] == 'VA'), 'county_apps'
    ] = df_long_complete.loc[
        (df_long_complete['COUNTY_NAME'] == 'Bedford County') &  # Replacing with combined apps 
        (df_long_complete['STATE'] == 'VA'), 'bedford_combined_apps']

# Dropping Bedford City & extra bedford_county_apps variable
df_long_complete = df_long_complete[~(df_long_complete['COUNTY_NAME'] == 'Bedford city')]
df_long_complete = df_long_complete.drop(columns=['bedford_combined_apps'])


##### Kalawao County & Maui County ######
# Kalawao County is accounted for within Maui county in the other datasets, so they will be combined here
# Selecting Kalawao County & Maui County
kalawao = df_long_complete.loc[
    (df_long_complete['COUNTY_NAME'] == 'Kalawao County') &
    (df_long_complete['STATE'] == 'HI')]

maui = df_long_complete.loc[
    (df_long_complete['COUNTY_NAME'] == 'Maui County') &
    (df_long_complete['STATE'] == 'HI')]

# Merging to combine their application data
maui_kalawao_combined = maui[['year', 'COUNTY_NAME', 'full_fips', 'county_apps']].merge(
    kalawao[['year', 'county_apps']], 
        on='year',
        how='left',
        suffixes=('_maui', '_kalawao'))

# Combining Application Data
maui_kalawao_combined['combined_county_apps'] = (
    maui_kalawao_combined['county_apps_maui'] + maui_kalawao_combined['county_apps_kalawao'])

# Merging combined application data back into main dataset
df_long_complete = df_long_complete.merge(
    maui_kalawao_combined[['full_fips', 'year', 'combined_county_apps']],
    on=['full_fips', 'year'],
    how='left'
)

# Replacing county_apps with combined totals
df_long_complete.loc[
    (df_long_complete['COUNTY_NAME'] == 'Maui County') & (df_long_complete['STATE'] == 'HI'),
    'county_apps'
    ] = df_long_complete.loc[
        (df_long_complete['COUNTY_NAME'] == 'Maui County') & (df_long_complete['STATE'] == 'HI'),
        'combined_county_apps'
        ]

# Dropping Kalawao County and combined_county_apps variable
df_long_complete = df_long_complete[~((df_long_complete['COUNTY_NAME'] == 'Kalawao County') & 
                                      (df_long_complete['STATE'] == 'HI'))]

df_long_complete = df_long_complete.drop(columns=('combined_county_apps'))



#######################################
# VALIDATION
# Final data validation
assert df_long_complete.groupby(['full_fips', 'year']).size().eq(1).all()
assert df_long_complete['full_fips'].str.len().eq(5).all()
assert df_long_complete['county_apps'].notna().all()

#######################################
# SAVING DATA
df_long_complete.to_csv('data_clean/annual_county_applications.csv', index=False)
