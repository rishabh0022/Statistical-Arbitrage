import matplotlib.pyplot as plt
import pandas as pd

def track_pnL(capital_history):
    plt.plot(capital_history)
    plt.title('Strategy PnL over time')
    plt.xlabel('Date')
    plt.ylabel('Capital')
    plt.show()
    
    final_capital = capital_history[-1]
    print(f"Final Capital: {final_capital}")

if __name__ == "__main__":
    
    capital_history = pd.read_csv('backtest_results.csv', index_col='Date', parse_dates=True)['Capital']
    track_pnL(capital_history)
