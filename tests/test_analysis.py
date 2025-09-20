import pandas as pd
import pytest
from src.analysis import monthly_totals, category_totals, net_balance, AnalysisError

def sample_df():
    return pd.DataFrame({
        "date": ["2025-01-01", "2025-01-15", "2025-02-01"],
        "description": ["Supermarket", "Uber Ride", "Rent"],
        "amount": [-50, -20, -500],
        "category": ["Groceries", "Transport", "Housing"]
    })

def test_monthly_totals():
    df = sample_df()
    result = monthly_totals(df)
    assert "month" in result.columns
    assert "total_amount" in result.columns
    assert result.shape[0] == 2  # two different months

def test_category_totals():
    df = sample_df()
    result = category_totals(df)
    assert "category" in result.columns
    assert "total_amount" in result.columns
    assert "Groceries" in result["category"].values

def test_net_balance():
    df = sample_df()
    balance = net_balance(df)
    assert isinstance(balance, (int, float))
    assert balance == -570  # -50 -20 -500

def test_empty_dataframe():
    df = pd.DataFrame()
    with pytest.raises(AnalysisError):
        monthly_totals(df)