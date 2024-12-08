# Statistical Arbitrage Strategy Backtester

This project implements a **Statistical Arbitrage** strategy backtester using Python. It analyzes the relationship between two assets, calculates their cointegration, and applies a mean-reversion trading strategy. The backtesting framework tracks capital changes, positions, and performance over time.

## Features

- **Cointegration Test**: Implements the Engle-Granger cointegration test to identify pairs of assets that move together.
- **Trading Strategy**: Trades based on statistical arbitrage principles using long and short positions.
- **Backtesting Framework**: Simulates real-world performance by executing trades, calculating daily PnL, and tracking capital growth over time.
- **Data Handling**: Uses historical price data for backtesting and performance evaluation.
- **Performance Evaluation**: Tracks portfolio performance over time, displaying capital changes during the backtest period.
## Results
Achieved a profit of 250 dollars. 
![image](https://github.com/user-attachments/assets/1a820396-6456-4f24-849a-1b6637ebabf8)

## Requirements

- Python 3.x
- Pandas
- NumPy
- Statsmodels
- Matplotlib (optional for visualizing results)

You can install the necessary dependencies using `pip`:
