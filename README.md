# README : Business Formation and Local Economic Wellbeing

## Project Summary
Motivated by recent literature on the spatial dynamics of entrepreneurship and economic development, as well as the widespread adoption of entrepreneurship and small business development programs as a means of community economic development, this project seeks to explore the impacts of new business formations on economic conditions across U.S. counties. 

Specifically, this project explores how new business formations impact poverty, unemployment, and inequality at the county-year level, and if county characteristics like demographics and prior unemployment, poverty, and inequality are associated with heterogeneity in these relationships.

In order to achieve this, I first estimate new business formations at the county-year level using Census Business Formation Statistics data, 
then construct a panel at the county-level using ACS and U.S. Bureau of Labor Statistics data. I plan to analyze the relationship between new business formations and measures of local economic well-being, including poverty, inequality, and employment outcomes using basic fixed effects panel models. Then I will analyze if there is any heterogeneity in these associations by county characteristics like racial makeup, pre-existing poverty, gini index, and more. 

## Current Status
Please note this project is still in the early stages. Current work is focused on data cleaning, harmonization, and panel construction, as well as exploring empirical strategies for analysis. 

The next step in this project is to finish constructing the panel, including cleaning, standardizing, and merging the remaining datasets. Then, I will conduct a preliminary analysis to assess baseline impact. After this, I plan to incorporate additional county demographics data and conduct a more detailed analysis to assess impact heterogeneity. I have yet to choose specific estimators for this step, but I plan to use interaction terms for heterogeneity and I hope to explore dynamic models to further explore the impacts of poverty and unemployment over time.

## Data Sources

### *Business Formation Statistics (BFS)*
Two datasets are used from the U.S. Census Bureau's Business Formation Statistics (BFS). 

The first is the BFS time series dataset, which includes monthly state-level data on business applications and formations. This data is aggregated to find annual business formations and applications. This dataset can be found here ([BFS Time Series](https://www.census.gov/econ/currentdata/?programCode=BFS&startYear=2004&endYear=2025&categories[]=TOTAL&dataType=BA_BA&geoLevel=US&adjusted=1&notAdjusted=1&errorData=0)).

The second BFS dataset is Business Applications by County, which can be found here ([BFS County Applications](https://www.census.gov/econ/bfs/data/county.html)).

### *American Community Survey (ACS)*
Most of the economic well-being data used in this project comes from the U.S. Census Bureau's American Community Survey data. Specific data sources will be updated soon.

### *US Bureau of Labor Statistics (LAUS)*
The unemployment data for this project comes from the U.S. Bureau of Labor Statistics' Local Area Unemployment Statistics (LAUS) program. The specific raw file this repository uses is the flatfile *la.data.64.County*, which can be found here ([LAUS Flatfiles](https://download.bls.gov/pub/time.series/la/)).


## Reproducibility
A simple shell script (run_all.sh) is included to run the current data cleaning steps in order. In order for this to run successfully, the datasets mentioned above must be added to the `data_raw/` subdirectory, as the raw data files are not included in this repository. This pipeline will expand as the project develops.
