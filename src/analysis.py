import pandas as pd

class AnalysisError(Exception):
    """Raised when analysis cannot be performed."""

def monthly_totals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total expenses per month.
    Returns DataFrame with 'month' and 'total_amount'.
    """
    if df is None or df.empty:
        raise AnalysisError("Input DataFrame is empty or None.")

    if "date" not in df.columns or "amount" not in df.columns:
        raise AnalysisError("Missing required columns: date or amount")

    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    result = df.groupby("month")["amount"].sum().reset_index()
    result = result.rename(columns={"amount": "total_amount"})
    return result

def category_totals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total expenses per category.
    Returns DataFrame with 'category' and 'total_amount'.
    """
    if df is None or df.empty:
        raise AnalysisError("Input DataFrame is empty or None.")

    if "category" not in df.columns or "amount" not in df.columns:
        raise AnalysisError("Missing required columns: category or amount")

    result = df.groupby("category")["amount"].sum().reset_index()
    result = result.rename(columns={"amount": "total_amount"})
    return result

def net_balance(df: pd.DataFrame) -> float:
    """
    Calculate net balance (income - expenses).
    Assumes positive = income, negative = expense.
    """
    if df is None or df.empty:
        raise AnalysisError("Input DataFrame is empty or None.")

    if "amount" not in df.columns:
        raise AnalysisError("Missing required column: amount")

    return float(df["amount"].sum())
