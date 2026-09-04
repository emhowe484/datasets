#final4
#erin howe, jaasmine zhang, AI reviewed 9/1

import argparse
from pathlib import Path
from typing import Optional, Sequence, Tuple
import json
import pandas as pd
import numpy as np
from scipy.stats import iqr

def normalize_symbol(series: pd.Series) -> pd.Series:
    """Helper function to clean and standardize symbol strings."""
    return series.astype(str).str.upper().str.strip()

# --------------------------
# Data Loading & Cleaning
# --------------------------

def load_trades(csv_path: Path) -> pd.DataFrame:
    """Loads, cleans, deduplicates, and standardizes trade data from a CSV file."""
    trades = pd.read_csv(csv_path)
    trades['trade_date'] = pd.to_datetime(trades['trade_date'], errors='coerce')
    trades['settlement_date'] = pd.to_datetime(trades['settlement_date'], errors='coerce')

    # Convert numeric fields and force positive values in a single step
    trades["qty"] = pd.to_numeric(trades["qty"], errors="coerce").abs()
    trades["price"] = pd.to_numeric(trades["price"], errors="coerce").abs()
    trades["symbol"] = normalize_symbol(trades["symbol"])

    # Filter out rows missing critical numeric or string values
    valid_mask = (trades["price"].notna() & trades["venue"].notna() & trades["qty"].notna())
    trades = trades[valid_mask].copy()

    trades = trades.drop_duplicates(subset=["trade_date", "symbol", "qty", "price"])

    return trades


def check_outliers(trades: pd.DataFrame) -> pd.DataFrame:
    """separates data into subsets by symbol, finds 25th and 75th percentiles of price, uses IQR to remove outliers
    puts all the trades back together, recalculates derived columns (trade_ id, settlement_date, notional, signed_qty)"""

    stat1 = trades.groupby("symbol")["price"].agg(lambda x: x.quantile(0.25))
    stat2 = trades.groupby("symbol")["price"].agg(lambda x: x.quantile(0.75))
    my_iqr = trades.groupby("symbol")["price"].agg(lambda x: iqr(x))
    df1 = pd.concat([stat1-my_iqr, stat1, stat2, my_iqr, stat2+my_iqr], axis=1)
    df1.columns = ["lower_bound", "q1", "q3","iqr","upper_bound_1.5iqr"]
    return df1


def clean_trades(trades: pd.DataFrame) -> pd.DataFrame:
    """separates data into subsets by symbol, finds 25th and 75th percentiles of price, uses IQR to remove outliers
    puts all the trades back together, recalculates derived columns (trade_ id, settlement_date, notional, signed_qty)"""

    # Calculate 75th percentiles, and IQR 
    q3 = trades.groupby("symbol")["price"].transform(lambda x: x.quantile(0.75))
    iqr = q3 - trades.groupby("symbol")["price"].transform(lambda x: x.quantile(0.25))

    # Filter outliers
    upper_bound = q3 + 1.5 * iqr
    trades = trades[trades["price"] <= upper_bound].copy()
    print(trades.info())
    
    # sorts data by trade_date and symbol; reset index
    trades = trades.sort_values(by=['trade_date', 'symbol']).reset_index(drop=True)

    # reassign trade_id to ensure uniqueness of each row
    trades["trade_id"] = "T" + (trades.index + 100000).astype(str)

    # Fix settlement dates (Must be strictly after trade_date)
    invalid_settlement = trades['settlement_date'] <= trades['trade_date']
    trades.loc[invalid_settlement, 'settlement_date'] = (
        trades.loc[invalid_settlement, 'trade_date'] + pd.Timedelta(days=1)
    )

    # Recalculate derived columns 
    trades['notional'] = trades['qty'] * trades['price']
    trades['signed_qty'] = np.where(trades['side'] == 'SELL', trades['qty'] * -1, trades['qty'])
    return trades


def load_positions_and_trades( p_trades: Path,
    p_t0: Optional[Path] = None, p_t1: Optional[Path] = None,
    p_corp_actions: Optional[Path] = None, ) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Loads trade data and merges position files with optional corporate actions."""
    
    trades = load_trades(p_trades)
    valid_symbols = trades["symbol"].unique()

    if not (p_t0 and p_t1 and p_t0.exists() and p_t1.exists()):
        raise FileNotFoundError(
            "Both 'p_t0' and 'p_t1' file paths must be provided and exist." )

    t0 = pd.read_csv(p_t0)
    t1 = pd.read_csv(p_t1)
    t0["symbol"] = normalize_symbol(t0["symbol"])
    t1["symbol"] = normalize_symbol(t1["symbol"])

    merge_keys = [
        col
        for col in ["symbol", "account"]
        if col in t0.columns and col in t1.columns]

    positions = pd.merge(t0, t1, on=merge_keys, how="inner")
    positions = positions.rename(columns={"position_x": "position_t0", "position_y": "position_t1"})
    
    positions = positions[positions["symbol"].isin(valid_symbols)].copy()

    if p_corp_actions and p_corp_actions.exists():
        corp_actions = pd.read_csv(p_corp_actions)
        corp_actions["symbol"] = normalize_symbol(corp_actions["symbol"])

        ca_cols = [c for c in corp_actions.columns if c != "symbol"]
        positions = pd.merge(positions, corp_actions, on="symbol", how="left")
        positions[ca_cols] = positions[ca_cols].fillna(0)
    else:
        positions["corp_actions"] = 0

    return positions, trades