"""Expense analysis helpers."""

from __future__ import annotations

import pandas as pd


def summarize_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Compute total spending per month."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["month"] = df["date"].dt.to_period("M")
    return df.groupby("month")[["amount"]].sum().rename(columns={"amount": "total_spent"})


def summarize_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Compute total spending per category."""
    return df.groupby("category")[["amount"]].sum().rename(columns={"amount": "total_spent"})
