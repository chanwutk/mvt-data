# Efficiently Preprocessing and Querying from MVT Data

## Setup
```sh
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

## Preprocessing MVT Data
```sh
python preprocess.py I-24MOTION_2022-11-17_08-10-00.json
```
This script will output `I-24MOTION_2022-11-17_08-10-00.json.pkl`,
a dataframe-formatted data for efficient query processing.

## Querying using Polar
Running example queries in Jupyter Lab / Notebook
```sh
jupyter lab process-data.ipynb
```