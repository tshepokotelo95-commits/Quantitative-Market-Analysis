import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

def fetch_macro_data(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches USD/ZAR spot rates and relevant macroeconomic cross-assets.
    Assets include Gold (GC=F) and the US Dollar Index (DX-Y.NYB).
    """
    tickers = {
        'USD_ZAR': 'ZAR=X',
        'Gold': 'GC=F',
        'DXY': 'DX-Y.NYB'
    }
    
    print("Initializing secure institutional macro data pull...")
    data = yf.download(list(tickers.values()), start=start_date, end=end_date)['Adj Close']
    
    # Map back to intuitive column names
    inv_tickers = {v: k for k, v in tickers.items()}
    data = data.rename(columns=inv_tickers)
    
    # Handle time-zone alignments and forward-fill missing market days
    data = data.ffill().dropna()
    return data

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms raw asset prices into stationary statistical features
    suitable for time-series and ML forecasting algorithms.
    """
    feature_df = pd.DataFrame(index=df.index)
    
    # Calculate log returns to achieve stationarity
    feature_df['zar_log_return'] = np.log(df['USD_ZAR'] / df['USD_ZAR'].shift(1))
    feature_df['gold_log_return'] = np.log(df['Gold'] / df['Gold'].shift(1))
    feature_df['dxy_log_return'] = np.log(df['DXY'] / df['DXY'].shift(1))
    
    # Generate rolling statistical features (Historical Volatility)
    feature_df['zar_realized_vol_5d'] = feature_df['zar_log_return'].rolling(window=5).std()
    feature_df['zar_realized_vol_21d'] = feature_df['zar_log_return'].rolling(window=21).std()
    
    # Dropping rows with NaN values resulting from lags/rolling windows
    feature_df = feature_df.dropna()
    return feature_df

if __name__ == "__main__":
    # Define historical window (Lookback period for training/testing)
    end = datetime.today().strftime('%Y-%m-%d')
    start = (datetime.today() - timedelta(days=365 * 5)).strftime('%Y-%m-%d')
    
    # Run pipeline
    raw_macro_data = fetch_macro_data(start, end)
    processed_features = engineer_features(raw_macro_data)
    
    print(f"Data pipeline complete. Shape of feature matrix: {processed_features.shape}")
    # Ready to feed into model pipeline
