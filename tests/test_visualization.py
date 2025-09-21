import pandas as pd
import plotly.graph_objs as go
import pytest

from src.visualization import (
    VisualizationError,
    plot_expenses_by_category,
    plot_monthly_trend,
)

from src.visualization import _KALEIDO_AVAILABLE


def sample_df():
    return pd.DataFrame({
        "date": ["2025-01-01", "2025-01-15", "2025-02-01"],
        "amount": [-50, -20, -500],
        "category": ["Groceries", "Transport", "Housing"],
    })


def test_plot_expenses_by_category_returns_figure():
    df = sample_df()
    fig = plot_expenses_by_category(df)
    assert isinstance(fig, go.Figure)
    assert fig.data


@pytest.mark.skipif(not _KALEIDO_AVAILABLE, reason="kaleido is required for static export")
def test_plot_expenses_by_category_to_file(tmp_path):
    df = sample_df()
    output = plot_expenses_by_category(df, filename="test_category.png", to_file=True)
    assert output.exists()


def test_plot_monthly_trend_returns_figure():
    df = sample_df()
    fig = plot_monthly_trend(df)
    assert isinstance(fig, go.Figure)
    assert fig.data


@pytest.mark.skipif(not _KALEIDO_AVAILABLE, reason="kaleido is required for static export")
def test_plot_monthly_trend_to_file(tmp_path):
    df = sample_df()
    output = plot_monthly_trend(df, filename="test_monthly.png", to_file=True)
    assert output.exists()


def test_empty_dataframe():
    df = pd.DataFrame()
    with pytest.raises(VisualizationError):
        plot_expenses_by_category(df)
