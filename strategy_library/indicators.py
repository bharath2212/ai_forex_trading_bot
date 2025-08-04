### === indicators.py ===
import pandas as pd


def add_indicators(df):
    df = df.copy()
    
    # Moving Averages
    df["MA_short"] = df["Close"].rolling(window=3).mean()
    df["MA_long"] = df["Close"].rolling(window=6).mean()
    df["MA_5"] = df["Close"].rolling(window=5).mean()
    df["MA_200"] = df["Close"].rolling(window=200).mean()

    # RSI (14 & 2)
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain_14 = gain.rolling(window=14).mean()
    avg_loss_14 = loss.rolling(window=14).mean()
    rs_14 = avg_gain_14 / avg_loss_14
    df["RSI"] = 100 - (100 / (1 + rs_14))

    avg_gain_2 = gain.rolling(window=2).mean()
    avg_loss_2 = loss.rolling(window=2).mean()
    rs_2 = avg_gain_2 / avg_loss_2
    df["RSI_2"] = 100 - (100 / (1 + rs_2))

    # MACD
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # Breakout Highs and Lows
    df["Recent_High"] = df["Close"].rolling(window=20).max()
    df["Recent_Low"] = df["Close"].rolling(window=20).min()

    return df
