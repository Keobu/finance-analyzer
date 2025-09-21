import pandas as pd

from .utils_logging import log_error, log_info


class BudgetError(Exception):
    """Raised when budget check cannot be performed."""

def check_budget(df: pd.DataFrame, budget_dict: dict) -> list[str]:
    """
    Check if expenses exceed category budgets.

    Args:
        df (pd.DataFrame): DataFrame with at least ["category", "amount"]
        budget_dict (dict): e.g. {"Groceries": 300, "Transport": 100}

    Returns:
        list of alert strings
    """
    if df is None or df.empty:
        raise BudgetError("Input DataFrame is empty or None.")
    if "category" not in df.columns or "amount" not in df.columns:
        raise BudgetError("Missing required columns: category or amount")
    if not budget_dict:
        raise BudgetError("Budget dictionary is empty or None.")

    invalid_entries: dict[str, object] = {}
    for category, budget in budget_dict.items():
        if not isinstance(budget, (int, float)):
            invalid_entries[category] = budget
            continue
        if budget < 0:
            invalid_entries[category] = budget

    if invalid_entries:
        message = (
            "Budget values must be non-negative numbers. Invalid entries: "
            f"{invalid_entries}"
        )
        log_error(message)
        raise BudgetError(message)

    categories = ", ".join(sorted(budget_dict.keys()))
    log_info(f"Checking budgets for categories: {categories}")

    alerts = []
    totals = df.groupby("category")["amount"].sum()

    for category, budget in budget_dict.items():
        spent = totals.get(category, 0)
        # spent is negative if expenses are stored as negatives → take abs()
        spent_abs = abs(spent)
        if spent_abs > budget:
            alerts.append(
                f"⚠️ {category} exceeded budget: {spent_abs:.2f}€ / {budget:.2f}€"
            )
        else:
            alerts.append(
                f"✅ {category}: {spent_abs:.2f}€ / {budget:.2f}€ (within budget)"
            )

    return alerts
