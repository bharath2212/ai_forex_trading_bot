from strategy_library.strategy_runner import run_strategy
import pandas as pd

df = pd.read_csv("eurusd_hourly.csv", index_col=0, parse_dates=True)
signals = run_strategy(df, strategy_name="macd_rsi")

print(signals[["Close", "Signal"]].tail())
