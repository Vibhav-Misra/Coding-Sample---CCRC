# NYPD Anti-Asian Hate Crime Time-Series Forecasting

**Note to CCRC Review Committee regarding Stata:** 
*While this specific project was executed using Python (pandas, geopandas, statsmodels) and R, my deep foundation in statistical mechanics allows me to transition seamlessly to Stata. Furthermore, I actively leverage AI coding assistants (Claude, ChatGPT) in my workflow to rapidly translate logic between languages, ensuring immediate productivity in Stata for your research team's analysis plans.*

## Project Overview
This repository contains the data cleaning, geospatial merging, and time-series forecasting pipelines for analyzing Anti-Asian hate crime trends in New York City. The analysis leverages NYPD complaint data and precinct-level geospatial mapping to forecast incidents using ARIMA, SARIMA, and Prophet models.

## Repository Structure (Replicability)
To ensure replicability, this project is structured with relative file paths and isolated data environments.
- `data/raw/`: Contains the immutable raw administrative datasets.
- `data/processed/`: Contains the cleaned, merged, and analysis-ready datasets.
- `01_data_cleaning_nypd.py`: The primary script for handling missing values, standardizing administrative records, and merging spatial data.
- `02_time_series_forecasting.py`: The statistical modeling script.

## Instructions for Execution
1. Ensure all raw files (e.g., `nypd_hate_crimes_raw.csv`, `ny_precincts.geojson`) are placed in the `data/raw/` directory.
2. Run `python 01_data_cleaning_nypd.py` to generate the clean analytical dataset.
3. Run `python 02_time_series_forecasting.py` to fit the ARIMA and Prophet models.
