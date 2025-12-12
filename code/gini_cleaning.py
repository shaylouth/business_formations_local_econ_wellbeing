"""
File: gini_cleaning.py 
STATUS: W-I-P 
Purpose: cleans yearly gini index files, merges into gini panel
"""

import pandas as pd
import glob

# Collecting list of filenames of gini index files 
CSVs = glob.glob('data_raw/gini/*Data.csv')

# List to hold dataframes to be concatenated
df_list = []

# Looping over files
for file in CSVs:
    df = pd.read_csv(file, header = 1)
    
    # Data validation


    # Rename variables 

    
    # Dropping empty columns created in read_csv
    df = df.dropna(axis=1, how='all')

    # Slicing year out of filename to make year variable
    file_year = file[21:25] 
    print(file_year)
    df['year']=file_year

    # Saving each dataframe in list
    df_list.append(df)

# Concatenating all years, sorting panel by year 
final_df = pd.concat(df_list, ignore_index=True)
final_df = final_df.sort_values(by=['year','Geographic Area Name'])

final_df.to_csv('data_intermediate/gini_panel.csv', index=False)