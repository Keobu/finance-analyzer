"""Data cleaning and normalization routines."""

from __future__ import annotations

import pandas as pd


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the data frame with normalized column names."""
    normalized = {col: col.strip().lower().replace(" ", "_") for col in df.columns}
    return df.rename(columns=normalized)


def filter_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Filter out non-expense transactions."""
    mask = df.get("amount", 0) < 0
    return df.loc[mask].copy()
