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
The strategy was backtested on 16 highly-liquid US-sector and index ETFs from 2013 to 2025. After filtering for high-correlation and cointegrated pairs, the top 6 Sharpe-ranked pairs were traded in parallel using a mean-reversion approach.

Performance Highlights:

Annualized Sharpe Ratio: 1.42

Total Return: 11.7% over 5.3 years

Max Capital Allocated per Pair: 20% of portfolio

Transaction Costs: Modeled using 0.5 bps spread and volume-based slippage

Position Sizing: Volatility-targeted to 8% annualized portfolio risk


The strategy consistently generated profit in out-of-sample periods post-2018, showing resilience to market conditions and robustness across ETF pairs
![image](https://github.com/user-attachments/assets/7ef9b436-a0c8-44e2-8211-494f73340e25)


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
