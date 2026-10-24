import pytest

def test_sharpe_ratio_calculation():
    """Verify annualized Sharpe Ratio calculation given mean returns and volatility."""
    mean_daily_return = 0.0005  # 5 bps daily
    daily_volatility = 0.0100   # 100 bps daily
    risk_free_rate = 0.0
    
    annualized_sharpe = (mean_daily_return - risk_free_rate) / daily_volatility * (252 ** 0.5)
    
    assert pytest.approx(annualized_sharpe, 0.01) == 0.79

def test_transaction_cost_slippage_drag():
    """Verify return deduction after accounting for execution slippage friction."""
    gross_return = 0.0250      # 250 bps trade return
    execution_drag_bps = 0.0010 # 10 bps total drag (slippage + fee)
    
    net_return = gross_return - execution_drag_bps
    
    assert pytest.approx(net_return, 0.0001) == 0.0240
