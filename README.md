# Statistical Arbitrage Strategy Backtester

This project provides a robust **Statistical Arbitrage Backtesting Framework** in Python. It identifies cointegrated ETF pairs and simulates a mean-reversion trading strategy using historical price data. The backtester tracks capital, positions, transaction costs, and performance metrics over time for in-depth strategy evaluation.

## Overview

The strategy focuses on trading pairs of ETFs that exhibit **cointegration**—a stable long-term relationship—by exploiting temporary price deviations from their mean. The framework includes:

- Kalman Filter and rolling OLS for dynamic hedge ratio estimation  
- Adaptive z-score thresholds for entry and exit signals  
- Volatility-targeted position sizing  
- Realistic transaction cost modeling, including spread and volume-based slippage

## Features

- **Cointegration Screening**: Applies the Engle-Granger test and correlation filtering to identify tradable pairs
- **Trading Logic**: Executes long/short trades based on statistical divergence and mean-reversion signals
- **Position Sizing**: Allocates capital based on rolling volatility estimates to control risk
- **Backtesting Engine**: Simulates daily PnL, Sharpe ratio, and capital growth
- **Transaction Costs**: Models spread and slippage per leg for realistic PnL
- **Visualization**: Plots equity curves and portfolio performance metrics

## Results

The strategy achieved a **$250 profit** on a $10,000 capital base, yielding a **2.5% ROI** over the backtest period.

![Equity Curve](https://github.com/user-attachments/assets/1a820396-6456-4f24-849a-1b6637ebabf8)

## Requirements

- Python 3.x
- pandas
- numpy
- statsmodels
- matplotlib (optional, for plots)
- yfinance
- pykalman

Install dependencies using:

```bash
pip install pandas numpy statsmodels matplotlib yfinance pykalman
