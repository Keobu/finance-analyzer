"""Transaction categorization tools."""

from __future__ import annotations

import pandas as pd

CATEGORY_RULES: dict[str, tuple[str, ...]] = {
    "groceries": ("market", "grocery"),
    "utilities": ("utility", "electric", "water"),
}


def apply_rules(df: pd.DataFrame) -> pd.DataFrame:
    """Assign categories using simple keyword matching rules."""
    df = df.copy()
    descriptions = df.get("description", pd.Series(dtype="object"))
    df["category"] = descriptions.apply(_match_category)
    return df


def _match_category(description: str | float) -> str:
    if not isinstance(description, str):
        return "uncategorized"
    lowered = description.lower()
    for category, keywords in CATEGORY_RULES.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return "uncategorized"
