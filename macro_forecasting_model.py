import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

def train_hybrid_model(df: pd.DataFrame):
    """
    Trains an ARIMA-XGBoost hybrid model on USD/ZAR returns
    using macro features to model statistical residuals.
    """
    # 1. Isolate target return and exogenous macro features
    y = df['zar_log_return']
    X = df[['gold_log_return', 'dxy_log_return', 'zar_realized_vol_5d', 'zar_realized_vol_21d']]
    
    # Chronological split to completely protect against look-ahead bias
    split_idx = int(len(df) * 0.8)
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    
    print("Fitting linear ARIMA baseline component...")
    # Fit ARIMA(1, 0, 1) on historical returns
    arima_model = ARIMA(y_train, order=(1, 0, 1))
    arima_fit = arima_model.fit()
    
    # Calculate residuals (errors) on training data
    train_predictions = arima_fit.fittedvalues
    residuals_train = y_train - train_predictions
    
    print("Training non-linear XGBoost residual engine...")
    # Train XGBoost to predict the errors using macro features
    xgb_model = XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.05, random_state=42)
    xgb_model.fit(X_train, residuals_train)
    
    # 2. Generate Out-of-Sample Hybrid Predictions
    arima_test_pred = arima_fit.forecast(steps=len(y_test))
    # Align index for accurate time-series mapping
    arima_test_pred.index = y_test.index 
    
    xgb_test_pred = xgb_model.predict(X_test)
    
    # Final Hybrid Prediction = Linear Drift + Non-Linear Macro Adjustment
    hybrid_test_pred = arima_test_pred + xgb_test_pred
    
    # Calculate directional accuracy
    correct_direction = np.sign(hybrid_test_pred) == np.sign(y_test)
    accuracy = np.mean(correct_direction) * 100
    print(f"Model Training Complete. Out-of-Sample Directional Accuracy: {accuracy:.2f}%")
    
    return arima_fit, xgb_model

if __name__ == "__main__":
    # In practice, this reads the exported data matrix from data_pipeline.py
    print("Initializing Hybrid Time-Series Model Pipeline...")
    # Placeholder for framework execution structure
