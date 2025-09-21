"""Lightweight logging helpers for the Finance Expense Analyzer."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

_LOG_DIR = Path("logs")
_LOG_DIR.mkdir(parents=True, exist_ok=True)
_LOG_FILE = _LOG_DIR / "app.log"

_CONFIGURED = False


def _configure_logging() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(_LOG_FILE, mode="a", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    _CONFIGURED = True


def log_info(message: Any) -> None:
    """Log an informational message to the shared log file."""
    _configure_logging()
    logging.info(message)


def log_error(message: Any) -> None:
    """Log an error message to the shared log file."""
    _configure_logging()
    logging.error(message)
