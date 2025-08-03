import pandas as pd
import matplotlib.pyplot as plt

# Load CSV (first column assumed to be Date)
try:
    data = pd.read_csv("eurusd_hourly.csv", index_col=0, parse_dates=True)
except Exception as e:
    print(f"❌ Failed to load CSV: {e}")
    exit()

# Drop completely empty rows
data.dropna(how="all", inplace=True)

# Clean 'Close' column
if "Close" not in data.columns:
    print("❌ ERROR: 'Close' column not found in the CSV.")
    print("📄 Available columns:", list(data.columns))
    exit()

data["Close"] = pd.to_numeric(data["Close"], errors="coerce")
data.dropna(subset=["Close"], inplace=True)

# Plot the closing prices
plt.figure(figsize=(14, 6))
plt.plot(data["Close"], label="EUR/USD Close", color="blue")
plt.title("EUR/USD Closing Prices (Last 5 Years)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

print("✅ Plot generated successfully!")
