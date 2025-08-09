"""Custom exceptions for the inflation API."""


class InflationAPIError(Exception):
    """Base exception for all inflation API errors."""

    def __init__(self, message: str, details: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class DataNotFoundError(InflationAPIError):
    """Raised when requested data is not found."""
    pass


class InvalidYearError(InflationAPIError):
    """Raised when an invalid year is provided."""
    pass


class DataLoadError(InflationAPIError):
    """Raised when data cannot be loaded from source."""
    pass


class CalculationError(InflationAPIError):
    """Raised when a calculation cannot be performed."""
    pass
