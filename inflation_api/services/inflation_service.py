"""Business logic service for inflation calculations."""

import logging
from datetime import datetime
from decimal import Decimal

from inflation_api.core.exceptions import (
    CalculationError,
    DataNotFoundError,
    InvalidYearError,
)
from inflation_api.models import (
    CurrentValueResponse,
    InflationRateResponse,
    ValueChangeResponse,
)
from inflation_api.repositories.base import BaseInflationRepository
from inflation_api.services.base import BaseInflationService

logger = logging.getLogger(__name__)


class InflationService(BaseInflationService):
    """Service for inflation rate calculations."""

    def __init__(self, repository: BaseInflationRepository) -> None:
        """Initialize service with repository dependency.
        
        Args:
            repository: Repository for accessing inflation data
        """
        self.repository = repository

    def _validate_year(self, year: int) -> None:
        """Validate that a year is reasonable.
        
        Args:
            year: Year to validate
            
        Raises:
            InvalidYearError: If year is invalid
        """
        current_year = datetime.now().year
        if year < 1800 or year > current_year + 10:
            raise InvalidYearError(
                f"Year {year} is outside valid range (1800-{current_year + 10})",
                details="Year must be within reasonable historical bounds"
            )

    async def get_inflation_rate_by_year(self, year: int) -> InflationRateResponse:
        """Get inflation rate for a specific year."""
        self._validate_year(year)

        rate = await self.repository.get_inflation_rate(year)
        if rate is None:
            available_years = await self.repository.get_available_years()
            raise DataNotFoundError(
                f"No inflation data found for year {year}",
                details=f"Available years: {min(available_years)}-{max(available_years)}"
            )

        logger.info(f"Retrieved inflation rate for {year}: {rate}%")
        return InflationRateResponse(year=year, rate=rate)

    async def calculate_value_change_between_years(
        self, start_year: int, end_year: int
    ) -> ValueChangeResponse:
        """Calculate change in USD value between two years.
        
        Uses compound inflation calculation:
        value_change_factor = (1 + rate_i) from start_year+1 to end_year
        
        This satisfies: valueOfUsdInStartYear = valueChangeFactor * valueOfUsdInEndYear
        """
        self._validate_year(start_year)
        self._validate_year(end_year)

        if start_year == end_year:
            raise InvalidYearError(
                "Start year and end year must be different",
                details="Cannot calculate value change for the same year"
            )

        # Get all rates for calculation
        all_rates = await self.repository.get_all_rates()

        # Determine direction of calculation
        if start_year < end_year:
            # Forward calculation: start -> end
            years_to_check = list(range(start_year + 1, end_year + 1))
            multiplier = Decimal("1")

            for year in years_to_check:
                if year not in all_rates:
                    raise DataNotFoundError(
                        f"Missing inflation data for year {year}",
                        details="Cannot calculate value change with missing data"
                    )
                # Convert percentage to decimal and add 1
                rate_decimal = all_rates[year] / Decimal("100")
                multiplier *= (Decimal("1") + rate_decimal)

            description = (
                f"${1:.2f} in {start_year} is equivalent to "
                f"${multiplier:.2f} in {end_year}"
            )
        else:
            # Backward calculation: start -> end (start > end)
            years_to_check = list(range(end_year + 1, start_year + 1))
            multiplier = Decimal("1")

            for year in years_to_check:
                if year not in all_rates:
                    raise DataNotFoundError(
                        f"Missing inflation data for year {year}",
                        details="Cannot calculate value change with missing data"
                    )
                # Convert percentage to decimal and add 1
                rate_decimal = all_rates[year] / Decimal("100")
                multiplier *= (Decimal("1") + rate_decimal)

            # For backward calculation, we need the inverse
            try:
                multiplier = Decimal("1") / multiplier
            except (ArithmeticError, ZeroDivisionError):
                raise CalculationError(
                    "Cannot calculate backward value change",
                    details="Division by zero or arithmetic error in calculation"
                )

            description = (
                f"${1:.2f} in {start_year} is equivalent to "
                f"${multiplier:.2f} in {end_year}"
            )

        logger.info(f"Calculated value change from {start_year} to {end_year}: {multiplier}")

        return ValueChangeResponse(
            start_year=start_year,
            end_year=end_year,
            value_change_factor=multiplier,
            description=description
        )

    async def calculate_current_value(
        self, original_year: int, amount: Decimal = Decimal("1.00")
    ) -> CurrentValueResponse:
        """Calculate current value of money from a past year."""
        current_year = datetime.now().year
        self._validate_year(original_year)

        if original_year >= current_year:
            raise InvalidYearError(
                f"Original year {original_year} must be in the past",
                details=f"Current year is {current_year}"
            )

        # Use the value change calculation to get current value
        value_change_response = await self.calculate_value_change_between_years(
            original_year, current_year
        )

        current_value = amount * value_change_response.value_change_factor

        description = (
            f"${amount:.2f} in {original_year} is worth "
            f"${current_value:.2f} in {current_year}"
        )

        logger.info(
            f"Calculated current value: ${amount} from {original_year} = "
            f"${current_value} in {current_year}"
        )

        return CurrentValueResponse(
            original_year=original_year,
            current_year=current_year,
            original_amount=amount,
            current_value=current_value,
            description=description
        )
