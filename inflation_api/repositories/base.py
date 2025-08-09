"""Abstract base repository pattern."""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, List


class BaseInflationRepository(ABC):
    """Abstract base class for inflation data repositories."""

    @abstractmethod
    async def load_data(self) -> None:
        """Load inflation data from source."""
        pass

    @abstractmethod
    async def get_inflation_rate(self, year: int) -> Decimal | None:
        """Get inflation rate for a specific year.
        
        Args:
            year: The year to get inflation rate for
            
        Returns:
            The inflation rate as a Decimal, or None if not found
        """
        pass

    @abstractmethod
    async def get_all_rates(self) -> Dict[int, Decimal]:
        """Get all available inflation rates.
        
        Returns:
            Dictionary mapping year to inflation rate
        """
        pass

    @abstractmethod
    async def get_available_years(self) -> List[int]:
        """Get list of years with available data.
        
        Returns:
            List of years that have inflation data
        """
        pass

    @abstractmethod
    async def get_year_range(self) -> tuple[int, int] | None:
        """Get the range of available years.
        
        Returns:
            Tuple of (min_year, max_year) or None if no data
        """
        pass
