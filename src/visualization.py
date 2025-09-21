"""Visualization utilities for expense data."""

from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.io import write_image

try:
    # Attempting to render static images requires the kaleido engine.
    import kaleido  # noqa: F401

    _KALEIDO_AVAILABLE = True
except ImportError:
    _KALEIDO_AVAILABLE = False

if _KALEIDO_AVAILABLE:
    try:
        _test_fig = px.scatter(x=[0], y=[0])
        _test_path = RESULTS_DIR / "__kaleido_probe__.png"
        write_image(_test_fig, _test_path)
        _test_path.unlink(missing_ok=True)
    except Exception:
        _KALEIDO_AVAILABLE = False

class VisualizationError(Exception):
    """Raised when visualization cannot be generated."""

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

ImageReturn = Union[go.Figure, Path]


def _validate_columns(df: pd.DataFrame, required: set[str]) -> None:
    missing = required.difference(df.columns)
    if missing:
        raise VisualizationError(f"Missing required columns: {missing}")


def _category_totals(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        raise VisualizationError("Input DataFrame is empty or None.")
    _validate_columns(df, {"category", "amount"})

    totals = df.groupby("category")["amount"].sum().abs()
    totals = totals[totals > 0]
    if totals.empty:
        raise VisualizationError("No expense values available for category plot.")

    return totals.reset_index().rename(columns={"amount": "total"})


def _monthly_totals(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        raise VisualizationError("Input DataFrame is empty or None.")
    _validate_columns(df, {"date", "amount"})

    data = df.copy()
    data["month"] = pd.to_datetime(data["date"]).dt.to_period("M").astype(str)
    totals = data.groupby("month")["amount"].sum().abs()
    totals = totals[totals > 0]
    if totals.empty:
        raise VisualizationError("No expense values available for monthly trend plot.")

    return totals.reset_index().rename(columns={"amount": "total"})


def plot_expenses_by_category(
    df: pd.DataFrame,
    *,
    filename: str = "expenses_by_category.png",
    to_file: bool = False,
) -> ImageReturn:
    data = _category_totals(df)
    fig = px.pie(
        data,
        names="category",
        values="total",
        title="Expenses by Category",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_traces(textinfo="percent+label")

    if to_file:
        if not _KALEIDO_AVAILABLE:
            raise VisualizationError(
                "Static image export requires the 'kaleido' package. Install it via 'pip install kaleido'."
            )
        output = RESULTS_DIR / filename
        write_image(fig, output, width=800, height=600, scale=2)
        return output

    return fig


def plot_monthly_trend(
    df: pd.DataFrame,
    *,
    filename: str = "monthly_trend.png",
    to_file: bool = False,
) -> ImageReturn:
    data = _monthly_totals(df)
    fig = px.bar(
        data,
        x="month",
        y="total",
        title="Monthly Expense Trend",
        labels={"month": "Month", "total": "Amount (€)"},
        color="total",
        color_continuous_scale="Blues",
    )
    fig.update_layout(coloraxis_showscale=False)

    if to_file:
        if not _KALEIDO_AVAILABLE:
            raise VisualizationError(
                "Static image export requires the 'kaleido' package. Install it via 'pip install kaleido'."
            )
        output = RESULTS_DIR / filename
        write_image(fig, output, width=900, height=600, scale=2)
        return output

    return fig
