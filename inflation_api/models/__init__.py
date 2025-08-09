"""Models package for inflation API."""

from .inflation import (
    CurrentValueRequest,
    CurrentValueResponse,
    InflationRate,
    InflationRateResponse,
    ValueChangeRequest,
    ValueChangeResponse,
)

__all__ = [
    "InflationRate",
    "InflationRateResponse",
    "ValueChangeRequest",
    "ValueChangeResponse",
    "CurrentValueRequest",
    "CurrentValueResponse",
]
