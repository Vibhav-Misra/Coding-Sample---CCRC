# Author: Vibhav Misra

import pandas as pd
import os
import warnings
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
import logging

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_analytical_data(filepath):
    logging.info(f"Loading cleaned dataset from {filepath}")
    df = pd.read_csv(filepath)
    df['rpt_dt'] = pd.to_datetime(df['rpt_dt'])
    df = df.set_index('rpt_dt')
    return df

def fit_arima_model(ts_data, p=1, d=1, q=1):
    logging.info(f"Fitting ARIMA({p},{d},{q}) model...")
    model = ARIMA(ts_data['incident_count'], order=(p, d, q))
    results = model.fit()
    logging.info(f"ARIMA AIC: {results.aic:.2f}")
    return results

def fit_prophet_model(df):
    logging.info("Fitting Prophet model...")
    df_prophet = df.reset_index().rename(columns={'rpt_dt': 'ds', 'incident_count': 'y'})
    model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    model.fit(df_prophet)
    
    # Forecast next 12 months
    future = model.make_future_dataframe(periods=12, freq='ME')
    forecast = model.predict(future)
    logging.info("Prophet forecasting complete.")
    return forecast

def main():
    PROCESSED_DATA_PATH = os.path.join("data", "processed", "nypd_clean_asian_hc.csv")
    
    if not os.path.exists(PROCESSED_DATA_PATH):
        logging.error(f"File not found: {PROCESSED_DATA_PATH}. Please run script 01 first.")
        return
        
    df = load_analytical_data(PROCESSED_DATA_PATH)
    
    arima_results = fit_arima_model(df)
    prophet_forecast = fit_prophet_model(df)
    
    logging.info("Pipeline execution finished successfully. Replicability ensured.")

if __name__ == "__main__":
    main()
