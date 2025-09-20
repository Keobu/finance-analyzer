import pandas as pd
import pytest
from src.categorize import categorize_transactions, CategorizationError

def test_empty_dataframe():
    df = pd.DataFrame()
    with pytest.raises(CategorizationError):
        categorize_transactions(df)

def test_missing_description_column():
    df = pd.DataFrame({"date": ["2025-01-01"], "amount": [50]})
    with pytest.raises(CategorizationError):
        categorize_transactions(df)

def test_basic_categorization():
    df = pd.DataFrame({
        "date": ["2025-01-01", "2025-01-02", "2025-01-03"],
        "description": ["Supermarket Milano", "Uber Ride", "Cinema Tickets"],
        "amount": [50, 20, 15]
    })
    df = categorize_transactions(df)
    assert "category" in df.columns
    assert df.iloc[0]["category"] == "Groceries"
    assert df.iloc[1]["category"] == "Transport"
    assert df.iloc[2]["category"] == "Entertainment"

def test_uncategorized_goes_to_other():
    df = pd.DataFrame({
        "date": ["2025-01-04"],
        "description": ["Random Expense"],
        "amount": [10]
    })
    df = categorize_transactions(df)
    assert df.iloc[0]["category"] == "Other"