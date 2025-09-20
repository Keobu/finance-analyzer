"""Visualization utilities for expense data."""

from __future__ import annotations

import pandas as pd
import plotly.express as px


def spending_by_category_chart(df: pd.DataFrame):
    """Return a pie chart showing spend distribution by category."""
    totals = df.groupby("category", dropna=False)["amount"].sum().reset_index()
    return px.pie(totals, names="category", values="amount", title="Spending by Category")


def monthly_trend_chart(df: pd.DataFrame):
    """Return a line chart of monthly spending trends."""
    monthly = df.copy()
    monthly["date"] = pd.to_datetime(monthly["date"], errors="coerce")
    monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
    totals = monthly.groupby("month")["amount"].sum().reset_index()
    return px.line(totals, x="month", y="amount", title="Monthly Spending Trend")
