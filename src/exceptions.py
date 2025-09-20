"""Custom exceptions for the Finance Expense Analyzer."""


class FinanceAnalyzerError(Exception):
    """Base exception for the Finance Expense Analyzer."""


class DataValidationError(FinanceAnalyzerError):
    """Raised when input data fails validation checks."""
