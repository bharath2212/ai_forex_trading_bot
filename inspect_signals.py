import pandas as pd

# Load and clean the data
data = pd.read_csv("eurusd_2023.csv", index_col=0, parse_dates=True)
data["Close"] = pd.to_numeric(data["Close"], errors="coerce")
data.dropna(subset=["Close"], inplace=True)

# Calculate short moving averages
data["MA3"] = data["Close"].rolling(window=3).mean()
data["MA7"] = data["Close"].rolling(window=7).mean()

# Generate buy/sell signals based on crossover
data["Signal"] = 0
data.loc[data["MA3"] > data["MA7"], "Signal"] = 1
data.loc[data["MA3"] < data["MA7"], "Signal"] = -1
data["Position"] = data["Signal"].diff()

# Extract only crossover points (Position == 1 or -1)
crossovers = data[data["Position"].isin([1, -1])]

# Print crossover examples
print("\n🔍 Sample Crossovers:")
print(crossovers[["Close", "MA3", "MA7", "Position"]].head(10))

# Print total number of crossovers found
print(f"\n📊 Total crossover points: {len(crossovers)}")
