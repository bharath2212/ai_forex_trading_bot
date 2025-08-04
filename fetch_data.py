import yfinance as yf 
from datetime import datetime, timedelta
import pandas as pd

# === Configurable Parameters ===
symbol = "EURUSD=X"
interval = "5m"
filename = "eurusd_hourly.csv"

start_str = "2025-07-01"
end_str = "2025-07-03"

df = yf.download(symbol, start=start_str, end=end_str, interval=interval)

if df.empty:
    print("❌ No data returned.")
else:
    df.index.name = "Date"
    df.reset_index(inplace=True)
    df.to_csv(filename, index=False)
    print(f"✅ Saved to {filename}")
    print(f"📅 Date Range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"📊 Total rows: {len(df)}")
