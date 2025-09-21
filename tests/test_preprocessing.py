import io

import pytest

from src.preprocessing import DatasetNotFoundError, load_csv

def test_load_csv_file_not_found():
    with pytest.raises(DatasetNotFoundError):
        load_csv("non_existent_file.csv")

def test_load_csv_valid(tmp_path):
    # Create a temporary CSV file
    file = tmp_path / "expenses.csv"
    file.write_text("date,description,amount\n2025-01-01,Supermarket,50\n")

    df = load_csv(file)
    assert not df.empty
    assert list(df.columns) == ["date", "description", "amount"]
    assert df.iloc[0]["amount"] == 50


def test_load_csv_from_file_like():
    buffer = io.StringIO("date,description,amount\n2025-01-01,Supermarket,50\n")

    df = load_csv(buffer)
    assert not df.empty
    assert list(df.columns) == ["date", "description", "amount"]
