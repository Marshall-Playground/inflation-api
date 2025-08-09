"""Abstract base service pattern."""

from abc import ABC, abstractmethod
from decimal import Decimal

from inflation_api.models import (
    CurrentValueResponse,
    InflationRateResponse,
    ValueChangeResponse,
)


class BaseInflationService(ABC):
    """Abstract base class for inflation calculation services."""

    @abstractmethod
    async def get_inflation_rate_by_year(self, year: int) -> InflationRateResponse:
        """Get inflation rate for a specific year.
        
        Args:
            year: The year to get inflation rate for
            
        Returns:
            InflationRateResponse with the rate data
            
        Raises:
            DataNotFoundError: If no data exists for the year
            InvalidYearError: If the year is invalid
        """
        pass

    @abstractmethod
    async def calculate_value_change_between_years(
        self, start_year: int, end_year: int
    ) -> ValueChangeResponse:
        """Calculate change in USD value between two years.
        
        The result satisfies: valueOfUsdInStartYear = valueChangeFactor * valueOfUsdInEndYear
        
        Args:
            start_year: Starting year
            end_year: Ending year
            
        Returns:
            ValueChangeResponse with calculation results
            
        Raises:
            DataNotFoundError: If data is missing for either year
            InvalidYearError: If years are invalid
            CalculationError: If calculation cannot be performed
        """
        pass

    @abstractmethod
    async def calculate_current_value(
        self, original_year: int, amount: Decimal = Decimal("1.00")
    ) -> CurrentValueResponse:
        """Calculate current value of money from a past year.
        
        Args:
            original_year: The original year
            amount: Original amount (defaults to $1.00)
            
        Returns:
            CurrentValueResponse with calculation results
            
        Raises:
            DataNotFoundError: If data is missing
            InvalidYearError: If year is invalid
            CalculationError: If calculation cannot be performed
        """
        pass
