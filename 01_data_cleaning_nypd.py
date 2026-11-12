# Author: Vibhav Misra

import pandas as pd
import geopandas as gpd
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_and_clean_complaints(filepath):
    logging.info(f"Loading raw data from {filepath}...")
    try:
        df = pd.read_csv(filepath, low_memory=False)
    except FileNotFoundError:
        logging.warning("Mock mode: Raw data not found, generating sample administrative data.")
        
        # Mock data generation for sample purposes
        df = pd.DataFrame({
            'CMPLNT_NUM': range(1000, 1100),
            'RPT_DT': pd.date_range(start='2020-01-01', periods=100, freq='W'),
            'LAW_CAT_CD': ['FELONY', 'MISDEMEANOR', 'VIOLATION', 'UNKNOWN'] * 25,
            'BIAS_MOTIVE_DESC': ['ANTI-ASIAN'] * 60 + ['ANTI-BLACK'] * 20 + ['UNKNOWN'] * 20,
            'ADDR_PCT_CD': np.random.randint(1, 123, 100)
        })
        
    # Standardize column names (lowercase and strip spaces)
    df.columns = [c.lower().strip() for c in df.columns]
    
    # Filter for target demographic (Anti-Asian hate crimes)
    df_asian = df[df['bias_motive_desc'].str.contains("ANTI-ASIAN", na=False, case=False)].copy()
    
    # Handle missing values in precinct codes (drop invalid precincts)
    initial_len = len(df_asian)
    df_asian['addr_pct_cd'] = pd.to_numeric(df_asian['addr_pct_cd'], errors='coerce')
    df_asian = df_asian.dropna(subset=['addr_pct_cd'])
    df_asian['addr_pct_cd'] = df_asian['addr_pct_cd'].astype(int)
    logging.info(f"Dropped {initial_len - len(df_asian)} records due to missing precinct codes.")

    # Convert dates and set time index
    df_asian['rpt_dt'] = pd.to_datetime(df_asian['rpt_dt'], errors='coerce')
    df_asian = df_asian.dropna(subset=['rpt_dt'])
    
    return df_asian

def merge_geospatial_data(df_crimes, geo_filepath):
    logging.info("Merging with precinct shapefiles...")
    try:
        gdf_precincts = gpd.read_file(geo_filepath)
        gdf_precincts = gdf_precincts.rename(columns={'precinct': 'addr_pct_cd'})
        merged_gdf = gdf_precincts.merge(df_crimes, on='addr_pct_cd', how='left')
    except Exception as e:
        logging.warning("Mock mode: GeoJSON not found, skipping spatial merge for this sample.")
        merged_gdf = df_crimes 
        
    return merged_gdf

def main():
    # Define relative paths to ensure replicability across different machines
    RAW_DATA_PATH = os.path.join("data", "raw", "nypd_hate_crimes_raw.csv")
    GEO_DATA_PATH = os.path.join("data", "raw", "ny_precincts.geojson")
    OUTPUT_PATH = os.path.join("data", "processed", "nypd_clean_asian_hc.csv")
    
    df_clean = load_and_clean_complaints(RAW_DATA_PATH)
    df_final = merge_geospatial_data(df_clean, GEO_DATA_PATH)
    
    monthly_ts = df_final.set_index('rpt_dt').resample('ME').size().reset_index(name='incident_count')
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    monthly_ts.to_csv(OUTPUT_PATH, index=False)
    logging.info(f"Data cleaning complete. Clean analytical dataset saved to {OUTPUT_PATH}.")

if __name__ == "__main__":
    main()
