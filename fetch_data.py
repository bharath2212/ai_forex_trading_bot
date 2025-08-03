import yfinance as yf

from datetime import datetime, timedelta
import pandas as pd
# === Configurable Parameters ===
symbol = "EURUSD=X"
interval = "1h"
filename = "eurusd_hourly.csv"

# Only 730 days (~2 years) supported for hourly
end_date = datetime.today()
start_date = end_date - timedelta(days=729)

# Format dates as strings
start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")

print(f"📥 Fetching {symbol} hourly data from {start_str} to {end_str} (interval={interval})...")
df = yf.download(symbol, start=start_str, end=end_str, interval=interval)

if df.empty:
    print("❌ No data returned. Try again later or check your internet connection.")
else:
    df.to_csv(filename)
    print(f"✅ Data saved to: {filename}")
    print(f"📅 Date Range: {start_str} to {end_str}")


df = pd.read_csv("eurusd_hourly.csv")
print(f"📊 Total rows (including header): {len(df)}")
if len(df) > 0:
    print(f"📅 Date Range in CSV: {df['Date'].min()} to {df['Date'].max()}")