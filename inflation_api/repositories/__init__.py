"""Repositories package for data access layer."""

from .base import BaseInflationRepository
from .inflation_repository import CSVInflationRepository

__all__ = [
    "BaseInflationRepository",
    "CSVInflationRepository",
]
