import numpy as np
import pandas as pd

def run_backtest(y_test: pd.Series, hybrid_predictions: np.ndarray, transaction_cost: float = 0.0005):
    """
    Simulates a long/short systematic trading strategy on USD/ZAR 
    based on directional hybrid model signals, adjusting for execution drag.
    """
    backtest_df = pd.DataFrame(index=y_test.index)
    backtest_df['actual_returns'] = y_test
    backtest_df['predicted_returns'] = hybrid_predictions
    
    # 1. Generate Trading Signals (Long +1 if positive return expected, Short -1 if negative)
    backtest_df['signal'] = np.sign(backtest_df['predicted_returns'])
    
    # Shift signal by 1 day to ensure we execute on the next day's open (prevents look-ahead)
    backtest_df['strategy_position'] = backtest_df['signal'].shift(1)
    
    # 2. Compute Raw Strategy Returns
    backtest_df['raw_strategy_returns'] = backtest_df['strategy_position'] * backtest_df['actual_returns']
    
    # 3. Apply Transaction Cost Penalty on Position Changes (Turnover Drag)
    backtest_df['trades'] = backtest_df['strategy_position'].diff().abs().fillna(0)
    backtest_df['transaction_costs'] = backtest_df['trades'] * transaction_cost
    backtest_df['net_strategy_returns'] = backtest_df['raw_strategy_returns'] - backtest_df['transaction_costs']
    
    # 4. Institutional Performance Metrics
    cumulative_returns = np.exp(backtest_df['net_strategy_returns'].cumsum()) - 1
    total_return = cumulative_returns.iloc[-1] if len(cumulative_returns) > 0 else 0
    
    # Annualized Sharpe Ratio (assuming 252 trading days)
    mean_ret = backtest_df['net_strategy_returns'].mean()
    std_ret = backtest_df['net_strategy_returns'].std()
    sharpe_ratio = (mean_ret / std_ret) * np.sqrt(252) if std_ret != 0 else 0
    
    # Peak-to-Trough Drawdown Calculation
    cum_wealth = np.exp(backtest_df['net_strategy_returns'].cumsum())
    running_max = cum_wealth.cummax()
    drawdowns = (cum_wealth - running_max) / running_max
    max_drawdown = drawdowns.min()
    
    print("================ BACKTEST ENGINE OUTPUT ================")
    print(f"Total Cumulative Strategy Return (Net): {total_return * 100:.2f}%")
    print(f"Annualized Net Sharpe Ratio:            {sharpe_ratio:.2f}")
    print(f"Maximum Performance Drawdown:           {max_drawdown * 100:.2f}%")
    print("========================================================")
    
    return backtest_df

if __name__ == "__main__":
    print("Initializing Backtest Performance Engine...")
    # Ready to ingest arrays from macro_forecasting_model.py
