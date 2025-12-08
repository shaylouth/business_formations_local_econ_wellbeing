#!/usr/bin/env bash
set -e

python3 code/county_applications_cleaning.py
python3 code/state_applications_cleaning.py
python3 code/state_formations_cleaning.py

