"""Data loading and preprocessing utilities for expense CSV files."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from .exceptions import DatasetNotFoundError, EmptyDatasetError


def _is_path_like(obj: Any) -> bool:
    return isinstance(obj, (str, os.PathLike)) or hasattr(obj, "__fspath__")


def _read_csv(reader: Callable[[str], pd.DataFrame]) -> pd.DataFrame:
    last_error: Exception | None = None
    for encoding in ("utf-8", "latin1"):
        try:
            return reader(encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
            continue
    assert last_error is not None
    raise ValueError("Unable to decode CSV using utf-8 or latin1 encodings.") from last_error


def load_csv(source: Any) -> pd.DataFrame:
    """Load and sanitize a CSV file containing expenses.

    Args:
        source: Path-like string or a file-like object with a ``read`` method.

    Returns:
        A cleaned DataFrame with the expected columns.
    """

    if _is_path_like(source):
        file_path = Path(source)
        if not file_path.exists():
            raise DatasetNotFoundError(f"File not found: {source}")

        def reader(encoding: str) -> pd.DataFrame:
            return pd.read_csv(file_path, encoding=encoding)

        df = _read_csv(reader)

    elif hasattr(source, "read"):
        file_like = source

        def reader(encoding: str) -> pd.DataFrame:
            if hasattr(file_like, "seek"):
                file_like.seek(0)
            return pd.read_csv(file_like, encoding=encoding)

        try:
            df = _read_csv(reader)
        finally:
            if hasattr(file_like, "seek"):
                try:
                    file_like.seek(0)
                except Exception:
                    pass

    else:
        raise TypeError("CSV source must be a path or a file-like object with read().")

    df.columns = df.columns.str.lower().str.strip()
    required_cols = {"date", "description", "amount"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required_cols}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["description"] = df["description"].astype(str)

    df = df.dropna(subset=["date", "amount"])
    if df.empty:
        raise EmptyDatasetError("CSV does not contain valid rows after cleaning.")

    return df
