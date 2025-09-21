import pandas as pd
import pytest
from src.budget import check_budget, BudgetError

def sample_df():
    return pd.DataFrame({
        "category": ["Groceries", "Transport", "Housing"],
        "amount": [-350, -80, -500]
    })

def test_budget_exceeded():
    df = sample_df()
    budget = {"Groceries": 300, "Transport": 100}
    alerts = check_budget(df, budget)
    assert any("Groceries exceeded" in alert for alert in alerts)

def test_budget_within_limits():
    df = sample_df()
    budget = {"Transport": 200}
    alerts = check_budget(df, budget)
    assert any("within budget" in alert for alert in alerts)

def test_empty_dataframe():
    df = pd.DataFrame()
    with pytest.raises(BudgetError):
        check_budget(df, {"Groceries": 300})

def test_empty_budget_dict():
    df = sample_df()
    with pytest.raises(BudgetError):
        check_budget(df, {})