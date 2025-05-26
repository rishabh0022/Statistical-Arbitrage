# Statistical Arbitrage Strategy Backtester

This project provides a robust **Statistical Arbitrage Backtesting Framework** in Python. It identifies cointegrated ETF pairs and simulates a mean-reversion trading strategy using historical price data. The backtester tracks capital, positions, transaction costs, and performance metrics over time for in-depth strategy evaluation.

## Overview

The strategy focuses on trading pairs of ETFs that exhibit **cointegration**—a stable long-term relationship—by exploiting temporary price deviations from their mean. The framework includes:

- Kalman Filter and rolling OLS for dynamic hedge ratio estimation  
- Adaptive z-score thresholds for entry and exit signals  
- Volatility-targeted position sizing  
- Realistic transaction cost modeling, including spread and volume-based slippage


## Backtest Performance

- **Total Return**: 11.7%  
- **Annualized Sharpe Ratio**: 0.70  
- **Backtest Period**: 12.3 years (2013–2025)  
- **Number of Cointegrated Pairs Traded**: 3  
- **Pairs Selected**: ('DIA', 'XLK'), ('XLK', 'XLY'), ('IYR', 'XLRE')  
- **Max Capital Used per Pair**: 20%  
- **PnL After Costs**: Includes realistic modeling of spread (0.5 bps) and quadratic slippage per leg  



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
## Getting Started

Clone the repository and run the strategy:

```bash
git clone https://github.com/rishabh0022/Statistical-Arbitrage.git
cd Statistical-Arbitrage
Install dependencies using:

```bash
pip install pandas numpy statsmodels matplotlib yfinance pykalman
python backtester.py

