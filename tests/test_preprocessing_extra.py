from io import StringIO

import pandas as pd
import pytest

from src.budget import BudgetError, check_budget
from src.preprocessing import EmptyDatasetError, load_csv


def test_load_csv_missing_columns_raises_value_error():
    csv_data = "date,description\n2024-01-01,Groceries"
    with pytest.raises(ValueError):
        load_csv(StringIO(csv_data))


def test_load_csv_invalid_rows_raise_empty_dataset():
    csv_data = """date,description,amount\ninvalid-date,Test,abc\n,Missing,-\n"""
    with pytest.raises(EmptyDatasetError):
        load_csv(StringIO(csv_data))


def test_load_csv_non_numeric_amounts_are_filtered():
    csv_data = """date,description,amount\n2024-01-01,Invalid,abc\n2024-01-02,Valid,-25\n"""
    df = load_csv(StringIO(csv_data))
    assert len(df) == 1
    assert df.iloc[0]["description"].lower() == "valid"
    assert df.iloc[0]["amount"] == -25


def test_check_budget_with_invalid_values():
    df = pd.DataFrame(
        {
            "category": ["Groceries", "Transport"],
            "amount": [-100, -50],
        }
    )
    with pytest.raises(BudgetError):
        check_budget(df, {"Groceries": "abc"})
    with pytest.raises(BudgetError):
        check_budget(df, {"Transport": -10})
