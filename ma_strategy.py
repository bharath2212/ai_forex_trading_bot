import pandas as pd
import matplotlib.pyplot as plt

# === CONFIGURATION ===
ma_short_window = 3
ma_long_window = 6
stop_loss_pct = 0.05  # 0.5% stop-loss

data = pd.read_csv("eurusd_hourly.csv", index_col=0, parse_dates=True)
data = data[["Close"]].copy()
data["Close"] = pd.to_numeric(data["Close"], errors="coerce")
data.dropna(inplace=True)

# === Moving Averages ===
data["MA_short"] = data["Close"].rolling(window=ma_short_window).mean()
data["MA_long"] = data["Close"].rolling(window=ma_long_window).mean()

# === Signals ===
data["Signal"] = 0
data.loc[data["MA_short"] > data["MA_long"], "Signal"] = 1
data.loc[data["MA_short"] < data["MA_long"], "Signal"] = -1
data["Position"] = data["Signal"].diff()

# === Crossover Logging ===
crossovers = data[data["Position"].isin([1, -1])]
print("\n🔍 Sample Crossovers Detected:")
print(crossovers[["Close", "MA_short", "MA_long", "Position"]].head(10))
print(f"\n📊 Total crossover points: {len(crossovers)}")

# === Trade Simulation (with multiple trades and short selling) ===
trades = []
long_position = None
short_position = None

for date, row in data.iterrows():
    price = row["Close"]

    # === Check Stop-Loss ===
    if long_position:
        if price < long_position["entry"] * (1 - stop_loss_pct):
            trades.append({"Date": date, "Action": "SELL", "Price": price,
                           "Profit": round(price - long_position["entry"], 5), "Reason": "STOP-LOSS"})
            long_position = None
    if short_position:
        if price > short_position["entry"] * (1 + stop_loss_pct):
            trades.append({"Date": date, "Action": "COVER", "Price": price,
                           "Profit": round(short_position["entry"] - price, 5), "Reason": "STOP-LOSS"})
            short_position = None

    # === Entry and Exit Conditions ===
    if row["Position"] == 1:
        # Long Entry
        if not long_position:
            long_position = {"entry": price, "date": date}
            trades.append({"Date": date, "Action": "BUY", "Price": price})
        # Short Exit
        if short_position:
            trades.append({"Date": date, "Action": "COVER", "Price": price,
                           "Profit": round(short_position["entry"] - price, 5), "Reason": "CROSSOVER"})
            short_position = None

    elif row["Position"] == -1:
        # Short Entry
        if not short_position:
            short_position = {"entry": price, "date": date}
            trades.append({"Date": date, "Action": "SHORT", "Price": price})
        # Long Exit
        if long_position:
            trades.append({"Date": date, "Action": "SELL", "Price": price,
                           "Profit": round(price - long_position["entry"], 5), "Reason": "CROSSOVER"})
            long_position = None

# === Save and Report ===
trades_df = pd.DataFrame(trades)
trades_df.to_csv("trade_log.csv", index=False)

# === Plotting ===
# plt.figure(figsize=(20, 10))
# plt.plot(data["Close"], label="Price", color="gray", alpha=0.5)
# plt.plot(data["MA_short"], label=f"MA {ma_short_window}", color="blue")
# plt.plot(data["MA_long"], label=f"MA {ma_long_window}", color="orange")

buy_dates = trades_df[trades_df["Action"] == "BUY"]["Date"]
sell_dates = trades_df[trades_df["Action"] == "SELL"]["Date"]
short_dates = trades_df[trades_df["Action"] == "SHORT"]["Date"]
cover_dates = trades_df[trades_df["Action"] == "COVER"]["Date"]

# plt.plot(buy_dates, data.loc[buy_dates, "Close"], "^", color="green", markersize=10, label="BUY")
# plt.plot(sell_dates, data.loc[sell_dates, "Close"], "v", color="red", markersize=10, label="SELL")
# plt.plot(short_dates, data.loc[short_dates, "Close"], "<", color="purple", markersize=10, label="SHORT")
# plt.plot(cover_dates, data.loc[cover_dates, "Close"], ">", color="brown", markersize=10, label="COVER")

# plt.title("EUR/USD Strategy with MA Crossovers, Short Selling & Stop-Loss")
# plt.xlabel("Date")
# plt.ylabel("Price")
# plt.legend()
# plt.grid(True)
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# === Summary ===
total_profit = trades_df["Profit"].dropna().sum() if "Profit" in trades_df.columns else 0.0
num_trades = len(trades_df[trades_df["Action"].isin(["SELL", "COVER"])])

print(f"\n✅ Total Trades Executed: {num_trades}")
print(f"💰 Total Profit: {round(total_profit, 5)} USD")
print("📁 Trade log saved to trade_log.csv")
print("✅ Strategy executed successfully!")
