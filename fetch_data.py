import yfinance as yf
import pandas as pd

symbol = "EURUSD=X"
start_str = "2025-06-01"
end_str = "2025-07-31"
interval = "1h"  # hourly data

filename = "eurusd_hourly.csv"

df = yf.download(symbol, start=start_str, end=end_str, interval=interval)

if df.empty:
    print("❌ No data returned.")
else:
    df = df[["Close"]].copy()
    df.index.name = "Date"
    df.to_csv(filename)
    print(f"✅ Saved {len(df)} rows to {filename}")
    print(f"📅 From {df.index.min()} to {df.index.max()}")
