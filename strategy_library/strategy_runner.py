
### === strategy_runner.py ===
from .indicators import add_indicators
from .strategies import (
    strategy_dual_ma_crossover,
    strategy_rsi_reversion,
    strategy_rsi2_connors,
    strategy_breakout,
    strategy_macd_rsi,
    strategy_carry_trade,
    strategy_pairs_spread,
)

def run_strategy(df, strategy_name):
    df = add_indicators(df)
    df["Signal"] = 0

    strategy_map = {
        "dual_ma": strategy_dual_ma_crossover,
        "rsi_reversion": strategy_rsi_reversion,
        "rsi2_connors": strategy_rsi2_connors,
        "breakout": strategy_breakout,
        "macd_rsi": strategy_macd_rsi,
        "carry_trade": strategy_carry_trade,
        "pairs_spread": strategy_pairs_spread
    }

    if strategy_name not in strategy_map:
        raise ValueError(f"Unknown strategy: {strategy_name}")

    strategy_func = strategy_map[strategy_name]

    for idx, row in df.iterrows():
        try:
            df.at[idx, "Signal"] = strategy_func(row)
        except Exception as e:
            df.at[idx, "Signal"] = 0

    return df
