"""Tests for analysis module."""

from __future__ import annotations

import pandas as pd

from src import analysis


def test_summarize_by_month_returns_totals() -> None:
    df = pd.DataFrame(
        {
            "date": ["2024-01-15", "2024-01-20", "2024-02-10"],
            "amount": [-100, -50, -200],
            "category": ["groceries", "utilities", "groceries"],
        }
    )
    summary = analysis.summarize_by_month(df)
    assert list(summary["total_spent"]) == [-150, -200]
