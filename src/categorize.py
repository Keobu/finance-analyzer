import pandas as pd

class CategorizationError(Exception):
    """Raised when categorization cannot be performed."""

# Category rules could be defined here or loaded from a config
CATEGORY_RULES = {
    "supermarket": "Groceries",
    "grocery": "Groceries",
    "market": "Groceries",
    "uber": "Transport",
    "taxi": "Transport",
    "fuel": "Transport",
    "gas": "Transport",
    "rent": "Housing",
    "bill": "Housing",
    "electricity": "Housing",
    "internet": "Housing",
    "netflix": "Entertainment",
    "spotify": "Entertainment",
    "cinema": "Entertainment",
}

def categorize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize transactions based on keywords in the description column.
    
    args:
        df (pd.DataFrame): must contain columns ["date", "description", "amount"]
        
    returns:
        pd.DataFrame: same dataframe with an extra "category column
    """
    if df is None or df.empty:
        raise CategorizationError("Input DataFrame is empty or None.")
    
    if "description" not in df.columns:
        raise CategorizationError("Missing required column: description")
    
    # Normalize description 
    df["description"] = df["description"].astype(str).str.lower()

    categories = []
    for desc in df["description"]:
        assigned = "Other"
        for keyword, cat in CATEGORY_RULES.items():
            if keyword in desc:
                assigned = cat
                break
        categories.append(assigned)

    df["category"] = categories
    return df