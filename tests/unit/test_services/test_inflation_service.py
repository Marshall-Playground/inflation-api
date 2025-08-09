"""Unit tests for inflation service."""

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from inflation_api.core.exceptions import (
    DataNotFoundError,
    InvalidYearError,
)
from inflation_api.models import (
    CurrentValueResponse,
    InflationRateResponse,
    ValueChangeResponse,
)
from inflation_api.services import InflationService


class TestInflationService:
    """Test inflation service."""

    @pytest.fixture
    def mock_repository(self):
        """Mock repository for testing."""
        repo = MagicMock()
        repo.get_inflation_rate = AsyncMock()
        repo.get_all_rates = AsyncMock()
        repo.get_available_years = AsyncMock()
        return repo

    @pytest.fixture
    def service(self, mock_repository):
        """Create service with mock repository."""
        return InflationService(mock_repository)

    def test_validate_year_valid(self, service: InflationService):
        """Test year validation with valid years."""
        # Should not raise
        service._validate_year(2000)
        service._validate_year(1800)

    def test_validate_year_invalid(self, service: InflationService):
        """Test year validation with invalid years."""
        with pytest.raises(InvalidYearError):
            service._validate_year(1799)  # Too old

        with pytest.raises(InvalidYearError):
            service._validate_year(2040)  # Too far in future

    @pytest.mark.asyncio
    async def test_get_inflation_rate_by_year_success(
        self, service: InflationService, mock_repository
    ):
        """Test successful inflation rate retrieval."""
        mock_repository.get_inflation_rate.return_value = Decimal("1.4")

        result = await service.get_inflation_rate_by_year(2020)

        assert isinstance(result, InflationRateResponse)
        assert result.year == 2020
        assert result.rate == Decimal("1.4")
        mock_repository.get_inflation_rate.assert_called_once_with(2020)

    @pytest.mark.asyncio
    async def test_get_inflation_rate_by_year_not_found(
        self, service: InflationService, mock_repository
    ):
        """Test inflation rate retrieval when data not found."""
        mock_repository.get_inflation_rate.return_value = None
        mock_repository.get_available_years.return_value = [2020, 2021, 2022]

        with pytest.raises(DataNotFoundError) as exc_info:
            await service.get_inflation_rate_by_year(1999)

        assert "No inflation data found for year 1999" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_inflation_rate_by_year_invalid_year(
        self, service: InflationService, mock_repository
    ):
        """Test inflation rate retrieval with invalid year."""
        with pytest.raises(InvalidYearError):
            await service.get_inflation_rate_by_year(1799)

    @pytest.mark.asyncio
    async def test_calculate_value_change_forward(
        self, service: InflationService, mock_repository
    ):
        """Test value change calculation going forward in time."""
        # Mock data: 2020->2021: 1.4%, 2021->2022: 5.39%
        mock_repository.get_all_rates.return_value = {
            2020: Decimal("1.4"),
            2021: Decimal("5.39"),
            2022: Decimal("6.5"),
        }

        result = await service.calculate_value_change_between_years(2020, 2022)

        assert isinstance(result, ValueChangeResponse)
        assert result.start_year == 2020
        assert result.end_year == 2022

        # Expected: (1 + 5.39/100) * (1 + 6.5/100) = 1.0539 * 1.065 ≈ 1.1224
        expected = Decimal("1.0539") * Decimal("1.065")
        assert abs(result.value_change_factor - expected) < Decimal("0.0001")

    @pytest.mark.asyncio
    async def test_calculate_value_change_backward(
        self, service: InflationService, mock_repository
    ):
        """Test value change calculation going backward in time."""
        mock_repository.get_all_rates.return_value = {
            2020: Decimal("1.4"),
            2021: Decimal("5.39"),
            2022: Decimal("6.5"),
        }

        result = await service.calculate_value_change_between_years(2022, 2020)

        assert isinstance(result, ValueChangeResponse)
        assert result.start_year == 2022
        assert result.end_year == 2020

        # Should be inverse of forward calculation
        forward_factor = Decimal("1.0539") * Decimal("1.065")
        expected = Decimal("1") / forward_factor
        assert abs(result.value_change_factor - expected) < Decimal("0.0001")

    @pytest.mark.asyncio
    async def test_calculate_value_change_same_year(
        self, service: InflationService, mock_repository
    ):
        """Test value change calculation with same start/end year."""
        with pytest.raises(InvalidYearError):
            await service.calculate_value_change_between_years(2020, 2020)

    @pytest.mark.asyncio
    async def test_calculate_value_change_missing_data(
        self, service: InflationService, mock_repository
    ):
        """Test value change calculation with missing data."""
        mock_repository.get_all_rates.return_value = {
            2020: Decimal("1.4"),
            # Missing 2021 data
            2022: Decimal("6.5"),
        }

        with pytest.raises(DataNotFoundError) as exc_info:
            await service.calculate_value_change_between_years(2020, 2022)

        assert "Missing inflation data for year 2021" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_calculate_current_value_success(
        self, service: InflationService, mock_repository
    ):
        """Test current value calculation."""
        # Mock the value change calculation by testing with known data
        from datetime import datetime
        current_year = datetime.now().year
        mock_data = {
            2020: Decimal("1.4"),
            2021: Decimal("5.39"),
            2022: Decimal("6.5"),
            2023: Decimal("3.2"),
            2024: Decimal("2.1"),
        }
        # Add current year if it's not already in the data
        if current_year not in mock_data:
            mock_data[current_year] = Decimal("2.5")
        mock_repository.get_all_rates.return_value = mock_data

        result = await service.calculate_current_value(2020, Decimal("100.00"))

        assert isinstance(result, CurrentValueResponse)
        assert result.original_year == 2020
        assert result.original_amount == Decimal("100.00")
        assert result.current_value > Decimal("100.00")  # Should be higher due to inflation

        # Check description format
        assert "2020" in result.description
        assert "100.00" in result.description

    @pytest.mark.asyncio
    async def test_calculate_current_value_future_year(
        self, service: InflationService, mock_repository
    ):
        """Test current value calculation with future year."""
        with pytest.raises(InvalidYearError):
            await service.calculate_current_value(2030)

    @pytest.mark.asyncio
    async def test_calculate_current_value_current_year(
        self, service: InflationService, mock_repository
    ):
        """Test current value calculation with current year."""
        from datetime import datetime
        current_year = datetime.now().year

        with pytest.raises(InvalidYearError):
            await service.calculate_current_value(current_year)

    @pytest.mark.asyncio
    async def test_calculate_current_value_default_amount(
        self, service: InflationService, mock_repository
    ):
        """Test current value calculation with default amount."""
        from datetime import datetime
        current_year = datetime.now().year
        mock_data = {
            2020: Decimal("1.4"),
            2021: Decimal("5.39"),
            2022: Decimal("6.5"),
            2023: Decimal("3.2"),
            2024: Decimal("2.1"),
        }
        # Add current year if it's not already in the data
        if current_year not in mock_data:
            mock_data[current_year] = Decimal("2.5")
        mock_repository.get_all_rates.return_value = mock_data

        result = await service.calculate_current_value(2020)

        assert result.original_amount == Decimal("1.00")
        assert result.current_value > Decimal("1.00")
