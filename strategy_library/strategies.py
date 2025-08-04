
### === strategies.py ===
def strategy_dual_ma_crossover(row):
    if row["MA_short"] > row["MA_long"]:
        return 1
    elif row["MA_short"] < row["MA_long"]:
        return -1
    return 0

def strategy_rsi_reversion(row):
    if row["RSI"] < 30:
        return 1
    elif row["RSI"] > 70:
        return -1
    return 0

def strategy_rsi2_connors(row):
    if row["RSI_2"] < 5 and row["Close"] > row["MA_200"]:
        return 1
    elif row["RSI_2"] > 70 and row["Close"] > row["MA_5"]:
        return -1
    return 0

def strategy_breakout(row):
    if row["Close"] > row["Recent_High"]:
        return 1
    elif row["Close"] < row["Recent_Low"]:
        return -1
    return 0

def strategy_macd_rsi(row):
    if row["MACD"] > row["MACD_signal"] and row["RSI"] > 50:
        return 1
    elif row["MACD"] < row["MACD_signal"] and row["RSI"] < 50:
        return -1
    return 0

def strategy_carry_trade(row):
    if row.get("Interest_Diff", 0) > 0.5:
        return 1
    return 0

def strategy_pairs_spread(row):
    if row.get("zscore", 0) > 2:
        return -1
    elif row.get("zscore", 0) < -2:
        return 1
    elif abs(row.get("zscore", 0)) < 0.5:
        return 0
    return None

