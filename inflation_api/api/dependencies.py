"""FastAPI dependencies for dependency injection."""

from functools import lru_cache
from pathlib import Path

from inflation_api.config import settings
from inflation_api.repositories import CSVInflationRepository
from inflation_api.services import InflationService


@lru_cache()
def get_inflation_repository() -> CSVInflationRepository:
    """Get inflation repository instance (cached)."""
    csv_path = Path(settings.inflation_data_path)
    return CSVInflationRepository(csv_path)


@lru_cache()
def get_inflation_service() -> InflationService:
    """Get inflation service instance (cached)."""
    repository = get_inflation_repository()
    return InflationService(repository)
