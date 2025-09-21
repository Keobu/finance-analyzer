"""Data loading and preprocessing utilities for expense CSV files."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from .exceptions import DatasetNotFoundError, EmptyDatasetError
from .utils_logging import log_error, log_info


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


def _source_repr(source: Any) -> str:
    if _is_path_like(source):
        return str(Path(source))
    name = getattr(source, "name", None)
    if name:
        return f"<file-like {name}>"
    return f"<file-like {hex(id(source))}>"


def load_csv(source: Any) -> pd.DataFrame:
    """Load and sanitize a CSV file containing expenses.

    Args:
        source: Path-like string or a file-like object with a ``read`` method.

    Returns:
        A cleaned DataFrame with the expected columns.
    """

    descriptor = _source_repr(source)
    log_info(f"Loading CSV from {descriptor}")

    try:
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

    except Exception as exc:
        log_error(f"Failed to load CSV from {descriptor}: {exc}")
        raise

    df.columns = df.columns.str.lower().str.strip()
    required_cols = {"date", "description", "amount"}
    if not required_cols.issubset(df.columns):
        error_msg = f"CSV must contain columns: {required_cols}"
        log_error(error_msg)
        raise ValueError(error_msg)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["description"] = df["description"].astype(str)

    df = df.dropna(subset=["date", "amount"])
    if df.empty:
        error_msg = "CSV does not contain valid rows after cleaning."
        log_error(error_msg)
        raise EmptyDatasetError(error_msg)

    log_info(f"Loaded {len(df)} rows from {descriptor}")
    return df
