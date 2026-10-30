'''
This file is will execute the first stage analysis of this project,
including descriptive statistics and a baseline fixed-effects panel regression.
'''

# ##########################################
# SETUP 

import pandas as pd
import matplotlib
import numpy as np
from linearmodels import PanelOLS
import statsmodels.api as sm


panel = pd.read_csv('data_clean/panel.csv')
panel = panel.set_index(['full_fips', 'year'])


# ##########################################
# FIXED EFFECTS PANEL REGRESSION

model = PanelOLS.from_formula(
    'gini ~ county_forms_est + EntityEffects + TimeEffects',
    data=panel
)

results = model.fit(
    cov_type='clustered',
    cluster_entity=True
)

print(results.summary)



