# README : Business Formation and Local Economic Wellbeing

## Project Introduction
Motivated by recent literature on the spatial dynamics of entrepreneurship and economic development, as well as the widespread adoption of entrepreneurship and small business development programming as a means of community economic development, this project seeks to analyze the impacts of startup activity on economic conditions across U.S. counties. By estimating new business formations and constructing a panel at the county-level, I analyze the relationship between new business formation and measures of local economic well-being, including poverty, inequality, and employment outcomes.

## Work-In-Progress
Please note this project is in the early stages of development, with the final dataset for analysis yet to be constructed.

## How To Run
A simple shell script (run_all.sh) is included to run the current data cleaning steps in order. In order for this to run successfully, the datasets mentioned below must be added to the `data_raw/` subdirectory, as the raw data files are not included in this repository. This pipeline will expand as the project develops.

## Data Sources

### *Business Formation Statistics (BFS)*
Two datasets are used from the U.S. Census Bureau's Business Formation Statistics (BFS). 

The first is the BFS time series dataset, which includes monthly state-level data on business applications and formations. This data is aggregated to find annual business formations and applications. This dataset can be found here ([BFS Time Series](https://www.census.gov/econ/currentdata/?programCode=BFS&startYear=2004&endYear=2025&categories[]=TOTAL&dataType=BA_BA&geoLevel=US&adjusted=1&notAdjusted=1&errorData=0))

The second BFS dataset is Business Applications by County, which can be found here ([BFS County Applications](https://www.census.gov/econ/bfs/data/county.html))

### *American Community Survey (ACS)*
The economic well-being data used in this project comes from the U.S. Census Bureau's American Community Survey data. Specific data sources will be updated soon.
