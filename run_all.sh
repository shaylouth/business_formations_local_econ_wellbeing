#!/usr/bin/env bash
set -e

python3 code/geo_id.py
python3 code/quarterly_bfs_cleaning.py
python3 code/county_applications_cleaning.py
python3 code/state_applications_cleaning.py
python3 code/state_formations_cleaning.py
python3 code/county_formations_estimation.py
python3 code/unemployment_cleaning.py
python3 code/final_panel_creation.py
