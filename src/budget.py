"""Budget monitoring helpers."""

from __future__ import annotations

import pandas as pd


def calculate_overages(df: pd.DataFrame, monthly_budget: float) -> pd.Series:
    """Return spending overages relative to a monthly budget."""
    monthly_totals = df.groupby("month")[["total_spent"]].sum()
    overages = monthly_totals["total_spent"] - monthly_budget
    return overages.clip(lower=0)
