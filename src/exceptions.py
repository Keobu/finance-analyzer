class DatasetNotFoundError(Exception):
    """Raise when a dataset cannot be found."""

class EmptyDatasetError(Exception):
    """Raise when an input is empty or invalid."""

class ModelNotFoundError(Exception):
    """Raise when a model file cannot be found."""