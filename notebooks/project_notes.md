# PROJECT NOTES
*These are my working notes for this project. Feel free to check out where I'm at!

## Project Notes
### *To Do List*
- **First Stage Data Cleaning**

    - [x] State apps
        - [x] fix application values (concatenated, not added, by year aggregation loop right now)
        - [x] add fips via geo_id
    - [x] County apps
    - [ ] State formations
        - [x] add fips
        - [x] decide how to handle suppressed values
            - [x] *make graph to visualize the patterns better*
            - [x] Investigate if I can get business formation data from direct state sources for high-suppression states
                - *Yes, BUT this is now exploding the early analysis stage beyond my current timeline. I am going to take a faster, temporary route to produce a preliminary analysis and return to this fabulous data after that.*
            - [x] pro/con to different ways to handle the missingness
        - [ ] aggregate to year level
    - [ ] Unemployment
        - [ ] figure out how to read in flatfile from internet or locally correctly
    - [ ] Gini index
        - [ ] revisit structure
    - [ ] Poverty Rate
        - [ ] download data

- **Stage 1.5 Data Cleaning**
    * [ ] Construct full stage one panel
    * [ ] Construct county formations estimation

- **First Stage Analysis**
    - [ ] Learn fixed effects panel stuff in Python

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