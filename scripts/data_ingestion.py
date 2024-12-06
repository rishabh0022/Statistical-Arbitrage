import yfinance as yf

def fetch_data(symbols, start_date='2010-01-01', end_date='2024-01-01'):
    for symbol in symbols:
        data = yf.download(symbol, start=start_date, end=end_date)
        data.to_csv(f"data/{symbol}_data.csv")
        print(f"Data for {symbol} saved to data/{symbol}_data.csv")

if __name__ == "__main__":
    symbols = ['AAPL', 'MSFT'] 
    fetch_data(symbols)
