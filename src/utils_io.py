"""Input/output helpers for loading and saving expense data."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


def load_csv_files(paths: Iterable[Path]) -> list[pd.DataFrame]:
    """Load multiple CSV files into a list of data frames."""
    dataframes: list[pd.DataFrame] = []
    for path in paths:
        dataframes.append(pd.read_csv(path))
    return dataframes


def export_dataframe(df: pd.DataFrame, path: Path) -> None:
    """Persist a data frame to disk using UTF-8 encoding."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
