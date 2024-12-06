import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint

def load_data():
    asset1 = pd.read_csv('data/AAPL_data.csv', index_col='Date', parse_dates=True)['Adj Close']
    asset2 = pd.read_csv('data/MSFT_data.csv', index_col='Date', parse_dates=True)['Adj Close']
    return asset1, asset2


def check_cointegration(asset1, asset2):
    score, p_value, _ = coint(asset1, asset2)
    return p_value


def pair_trading_strategy(asset1, asset2, entry_threshold=1.5, exit_threshold=0):
   
    spread = asset1 - asset2
    mean_spread = spread.mean()
    std_spread = spread.std()

  
    long_entry = spread < mean_spread - entry_threshold * std_spread
    long_exit = spread > mean_spread

    short_entry = spread > mean_spread + entry_threshold * std_spread
    short_exit = spread < mean_spread

    return long_entry, long_exit, short_entry, short_exit

import pandas as pd

def backtest_strategy(asset1, asset2):
    long_entry, long_exit, short_entry, short_exit = pair_trading_strategy(asset1, asset2)

   
    capital = 10000
    position = 0  
    capital_history = []

    for i in range(1, len(asset1)):
        if long_entry.iloc[i]: 
            position = 1 
        elif short_entry.iloc[i]:  
            position = -1  
        elif long_exit.iloc[i] or short_exit.iloc[i]:
            position = 0  
        if position == 1:
            pnl = asset1.iloc[i] - asset1.iloc[i-1] - (asset2.iloc[i] - asset2.iloc[i-1])
        elif position == -1:
            pnl = -(asset1.iloc[i] - asset1.iloc[i-1]) + (asset2.iloc[i] - asset2.iloc[i-1])
        else:
            pnl = 0

        
        capital += pnl
        capital_history.append(capital)


    return pd.Series(capital_history, index=asset1.index[:len(capital_history)])



if __name__ == "__main__":
    asset1, asset2 = load_data()
    
    p_value = check_cointegration(asset1, asset2)
    print(f"Cointegration p-value: {p_value}")
    
    if p_value < 0.05:  
        capital_history = backtest_strategy(asset1, asset2)
        capital_history.plot(title="Strategy PnL")
        plt.show()
