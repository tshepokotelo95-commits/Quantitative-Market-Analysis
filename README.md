# Quantitative-Market-Analysis

[![Quantitative Market Analysis CI](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/tshepokotelo95-commits/Quantitative-Market-Analysis)
[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Market Data Analysis & Strategy: Applied Python (Pandas) and advanced time-series techniques to analyze market data and model ZAR/USD volatility. Developed a predictive model with strong out-of-sample accuracy, informing macro investment strategy.

---

## Systematic Backtesting Architecture & Signal Mechanics

This framework processes multi-asset historical price-action data to backtest alpha-generation parameters while strictly mitigating data-snooping and look-ahead biases.

### 1. Cross-Sectional Data Ingestion
The pipeline ingests raw OHLCV (Open, High, Low, Close, Volume) data arrays. Rather than executing simple moving average crossovers, the engine computes rolling statistical attributes:
* **Volatility-Adjusted Spreads:** Utilizes True Range parameters to dynamically adjust execution entry thresholds based on structural market regimes.
* **Volume Profiling:** Integrates price-at-volume distributions to isolate institutional liquidity nodes and dynamic support/resistance levels.

### 2. Signal Execution & Parameter Backtesting
Signals are systematically generated through cross-sectional parameter sweeps. The backtesting loop enforces strict institutional constraints:
* **Transaction Cost Adjustments:** Integrates variable slippage models and fixed basis-point execution drag to reflect true market friction.
* **Vectorized Backtesting Optimization:** Leverages vectorized arrays via NumPy and Pandas to simulate multi-year holding period returns over varying macroeconomic cycles, tracking Sharpe, Sortino, and Max Drawdown metrics.

---

## Mathematical Specifications

### 1. True Range & Volatility Scaling
$$\text{TR}_t = \max\left(H_t - L_t, \vert{}H_t - C_{t-1}\vert{}, \vert{}L_t - C_{t-1}\vert{}\right)$$
$$\sigma_{t,\text{rolling}} = \sqrt{\frac{1}{n} \sum_{i=0}^{n-1} (R_{t-i} - \bar{R})^2}$$

### 2. Sharpe Ratio Performance Metric
$$\text{Sharpe} = \frac{\mathbb{E}[R_p - R_f]}{\sigma_p}$$

---

## System Architecture & Data Flow

```text
+-----------------------------------------------------------------------------------+
|                         HISTORICAL OHLCV & ZAR/USD FEEDS                          |
|                 (High-Frequency Multi-Asset Price & Volume Data)                  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     QUANTITATIVE BACKTESTING & SIGNAL ENGINE                      |
|  * Rolling Volatility & ATR Normalization      * Cross-Sectional Parameter Sweeps |
|  * Transaction Cost & Slippage Adjustments     * Vectorized Performance Metrics   |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                      STRATEGY EVALUATION & PERFORMANCE DESK                       |
|           (Sharpe, Sortino, Max Drawdown, & Out-of-Sample Validation)             |
+-----------------------------------------------------------------------------------+
