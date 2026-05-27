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
        - [ ] **decide how to handle suppressed values**
            - [x] *make graph to visualize the patterns better*
            - [ ] Investigate if I can get business formation data from direct state sources for high-suppression states
            - [ ] pro/con to different ways to handle the missingness
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
        * should this use the county/state app ratio by year or should I get averaged ratio overtime for each county?
            * Maybe graph to see if it changes drastically year to year 

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
    * **Next Step**: Decide between suppressed data handling options and move on with it!
        * maybe just treat them as missing for initial prelim analysis?
        * maybe search for suppressed data from other state-level sources, now or later