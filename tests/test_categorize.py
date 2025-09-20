"""Tests for categorize module."""

from __future__ import annotations

import pandas as pd

from src import categorize


def test_apply_rules_assigns_category() -> None:
    df = pd.DataFrame({"description": ["Grocery Store"], "amount": [-50]})
    categorized = categorize.apply_rules(df)
    assert categorized.loc[0, "category"] == "groceries"
