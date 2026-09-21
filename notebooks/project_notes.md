# PROJECT NOTES
*These are my working notes for this project. Feel free to check out where I'm at!

## Project Notes
### *To Do List*
- **First Stage Data Cleaning**

    - [x] State apps
        - [x] fix application values (concatenated, not added, by year aggregation loop right now)
        - [x] add fips via geo_id
    - [x] County apps
    - [x] State formations
        - [x] add fips
        - [x] decide how to handle suppressed values
            - [x] *make graph to visualize the patterns better*
            - [x] Investigate if I can get business formation data from direct state sources for high-suppression states
                - *Yes, BUT this is now exploding the early analysis stage beyond my current timeline. I am going to take a faster, temporary route to produce a preliminary analysis and return to this fabulous data after that.*
            - [x] pro/con to different ways to handle the missingness
        - [x] aggregate to year level
    - [ ] Unemployment
        - [x] figure out lack of file extension

    - [ ] Gini index
        - [ ] revisit structure
    - [ ] Poverty Rate
        - [ ] download data

- **Stage 1.5 Data Cleaning**
    * [ ] Construct full stage one panel
        * [ ] Ensure all counties are matched across files
            * [ ] Connecticut
            * [ ] Kalawao
    * [x] Construct county formations estimation

- **First Stage Analysis**
    - [ ] Make maps!
        - [ ] 
    - [ ] Learn fixed effects panel stuff in Python
    - [ ] Run analysis on full dataset, pre-2015 dataset, and with all partially missing years dropped and compare

- **Stage Two Data Cleaning**
    * [ ] Find county demographics sources
        * race
        * maybe proportion immigrant?
        * population size? density? (big city counties vs rural counties?)

    * [ ] Make lagged poverty, inequality, and gini variables

- **Stage Two Analysis**
    * [ ] Look more into which dynamic estimator would work best here (use Prof Alem course notes, recommended textbooks in syllabus)

## Useful Code Snippets

#### Copy-paste diagnostic loop like Stata describe command
(*I did not write this snippet*)
```python

# Inspecting missing values and data distribution by column
for col in df.columns:
    print("====", col, "====")
    print("dtype:", df[col].dtype)
    print("nunique:", df[col].nunique())
    print("missing:", df[col].isna().sum())
    print(df[col].value_counts(dropna=False).head(10))
    print("\n")

```

## Project Structure

* Raw Data Inputs
    * State-level business formations and applications
    * Business applications (county-level)
    * Gini index
    * Unemployment rate
    * 
* 

## Progress Notes

* **5/21/26** 
    * Technical Progress: 
        * fixed kernel issues with .ipynb files, code runs smoothly through file now! 
        * learned about lambda functions
    * Project Progress:
        * added fips to state_formations file
        * converted formations to numeric, converted 'D' to missings
        * made .ipynb for state formations missingness exploration
    * Next Step: make graph of missingness, see notes in state formations cleaning notebook, handle the suppressed data accordingly

* **5/27/26**
    * Technical Progress:
        * Learned a lot about matplotlib
        * Expanded Python learning notes with heatmap/missingness visualization techniques
    * Project Progress:
        * Made state-year missingness heatmap for state formations!!
        * Started going over options to handle suppressed data, decision pending
        * Got very deep into measurement methodology and validation challenges
        * Looked into alternative data sources to potentially 1) patch suppression in data set where possible and 2) test validity of my estimate of county formations
            * Found SUPER promising Connecticut administrative business registry dataset to use in future measurement validation
            * Made difficult decision to set this aside for now due to endlessly exploding possibilities in this measurement construction phase. Exciting, but not aligned with the current preliminary analysis timeline. I will implement this in the next stage!
        * Update: upon further exploration of the methodology/cutoffs behind Census BFS data suppression, I am realizing that the spliced business formations within 8 quarters (SBF)
    * **Next Step**: Treat suppressed data as missing for now, and use this approach:
        1. Decide threshold for highly-suppressed states, what information is usable vs not usable
        2. Decide threshold for unreliable year aggregations (too many months for this year-state observation are missing, so this year-state observation is going to be missing)
        3. Eventually run analysis with and without high suppression states for comparison
        4. Explore if measurement quality differs systematically in ways that bias interpretation

* **5/28/26**
    * Technical Progress
    * Project Progress
        * Found historical quarterly BFS data, downloaded
        * Cleaned quarterly BFS formations time series
        * Realized I need to use non-seasonally adjusted data where possible because I'm aggregating to a year level (at the start I wanted to work on a monthly level); updated older BFS cleaning files accordingly to pull non-adjusted data instead

* **5/29/26**
    * Technical Progress
        * Practiced writing for loops
        * Learned about .sample (did not use in the end though)
        * Reviewed using f-strings in for loops
    * Project Progress
        * Created quarterly_state_formations_validation.ipynb
        * Validated annualization method to handle suppressed data years with at least 10 non-suppressed years
        * Decided how to handle data suppression in preliminary analysis. Ready to proceed now!
    * Next Steps
        * Finally complete state_formations dataset with new historic data and properly handled suppressed data
        * Merge state formations, state applications, and county applications into one dataframe
        * Estimate county formations

* **5/30/26**
    * Project Progress
        * Finished suppressed data handling in post-2014 state formations
        * Finished cleaning state formations dataset
        * Started county-year formations estimation file
        * Finished county-year formations estimations
    * Next Steps
        * Clean remaining 3 files
        * Prelim analysis (regressionson three different data subsets!)

* **6/1/26**
    * Project Progress
        * Started working on cleaning LAUS files
        * I don't know what was going on before but I was able to load the file despite its lack of an extension with the same code
        * Started exploration file

* **6/2/26**
    * Technical Progress
        * Reviewed modifiying, combining, slicing, etc strings
    * Project Progress
        * Parsed series_id in main file before realizing metadata files provide this parsing. Good practice though!
        * Merged LAUS metadata files with main data
        * Moved cleaning to actual .py file, will load in cleaned file directly to notebook for further exploration

* **6/3/26**
    * Technical Progress
        * Started learning about memory management best practices, will learn more later
            * Need to convert categorical variables to category dtype!
        * Investigated using more careful validation steps (assert keyword)
    * Project Progress
        * Moved forward with cleaning LAUS file

* **6/9/26**
    * Project Progress
        * To investigate bizzare number of counties, merging in county-level fips file to check unmatched data
    * Technical Progress
        * Took some notes on data structures vs data types vs data objects

* **6/15/26**
    * Project Progress
        * Finding issues with missing counties state-by-state
        * Considering handling of specific different format issues
            * --> Handle each format issue separately, id-ed by unique *name/name* endings
        * Need to get connecticut planning regions + FIPS codes into county_geo_id file
            * --> Make csv and add as only tracked file in raw data bc not easy to download
        * New problem unlocked: CONNECTICUT 
            * annual_county_applications and gini have counties only then switch to planning regions only starting in 2022
            * LAUS area file only has planning regions going back to 1990
            * --> need to coordiante rest of files to switch in 2022 or cut off pre-switch 
    * Next Steps
        * Decide how to handle Kalawao County, HI depending on dropped vs combined
        * Decide how to handle Connecticut
        * Clean up formatting issues in LAUS + FIPS merge (decisions for each issue in notebook)
        * Re-download raw gini data
        * Check for less complicated Connecticut data from the state data website

* **6/16/26**
    * Project Progress
        * CTData has county level employment numbers for 2011-2021, planning regions 2022-2023
            * need to find 2005-2010 unemployment numbers, maybe in ACS?

* **9/10/26**
    * Project Progress
        * Reoriented myself in the project
            * Verified no merge issues with state formations or state applications in county formations estimation dataset
            * Found 227 missing observations in county applications dataset, but they are ALL due to changes in geographic administrative units overtime
        * Need to solve 227 missing obs in county applications, so I plan to compare these counties with other county-level datasets (LAUS, ACS) before proceeding to decide how to handle each
        * Solved all LAUS-FIPS merge problems other than connecticut, Kalawao County, and the counties with tildas
    * Next steps:
        * Solve Kalawao County, tilda counties in LAUS-FIPS merge
        * Compare problem 227 in CA dataset with LAUS and ACS to decide how to handle the geographic changes consistently (use geo_hist_issues notebook that was setup today)
        * Just drop connecticut at this stage for time purposes and bring it back in the next stage

* **9/11/26**
    * Project Progress
        * Continued LAUS-FIPS merge harmonization
            * created simplified matching county name to match counties with tildes (laus)
        * Added state exclusions county-level cleaning files (CT and PR)
        * Started geographic history change comparison between FIPS, county apps, and LAUS (geo_hist notebook)
    * Decisions/Next Steps
        * Drop Alaska in first stage of analysis due to complicated historical county splits that must be handled carefully in the next stage
        * Shannon County → Oglala Lakota County: harmonize/recode because it's a rename/recode rather than a split
        * Bedford city/Bedford County: Aggregate where separated
        * Kalawao county: aggregate with Maui county in datasets where split

* **9/12/26**
    * Project Progress
        * Investigated the details of each of the above next step issues ^ 
        * Added AK to state exclusion list in all county-level dataset cleaning files
        * Implemented Oglala Lakota, Bedford, and Kalawao/Maui cleaning steps in the county applications cleaning file
        * Confirmed all remaining missing county_forms_est are from missing state formations, which were created intentionally! (verified in estimation_scratch.ipynb)
    * Next Steps
        * Finish aggregating LAUS
        * Merge LAUS with estimation file
        * See how long getting Gini would take

* **9/15/26**
    * Project Progress
        * Found 2025 missing data soure; the federal government just didn't collect the data in October 2025, so there is no data
        * 2005 and 2006 missing data are from Katrina -- flagged those years to test excluding for robustness
        * Found new issue in final data assertions -- there are still FIPS-county name duplicate matches that need to be addressed
    * Next step
        * sort out FIPS-county name duplicates in LAUS
        * Merge LAUS with county formations estimation data
        * ACS? Gini?

* **9/20/26**
    * Project Progress
        * Solved LAUS duplicates issue -- there were no duplicates in the post-aggregation data set, the assertion was just using the pre-aggregated data object
        * Updated LAUS file to specify how to read in variable types of fips file; consider updating other files to ensure fips are in string form with leading zeroes
        * Merged LAUS with county formations estimation dataset

    * Next steps
        * Inspect/validate merge
        * See how ACS clean is doing (estimate how long)
        * Cleanup final dataset

