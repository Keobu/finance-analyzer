"""Tests for preprocessing module."""

from __future__ import annotations

import pandas as pd

from src import preprocessing


def test_standardize_columns() -> None:
    df = pd.DataFrame({"Amount": [1], "Description": ["Test"]})
    normalized = preprocessing.standardize_columns(df)
    assert set(normalized.columns) == {"amount", "description"}
