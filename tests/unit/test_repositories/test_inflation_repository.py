"""Unit tests for inflation repository."""

from decimal import Decimal
from pathlib import Path

import pytest

from inflation_api.core.exceptions import DataLoadError
from inflation_api.repositories import CSVInflationRepository


class TestCSVInflationRepository:
    """Test CSV inflation repository."""

    @pytest.mark.asyncio
    async def test_load_data_success(self, csv_repository: CSVInflationRepository):
        """Test successful data loading."""
        await csv_repository.load_data()

        # Check that data was loaded
        assert csv_repository._loaded is True
        assert len(csv_repository._data) > 0

        # Check specific values
        assert csv_repository._data[2020] == Decimal("1.4")
        assert csv_repository._data[2021] == Decimal("5.39")

    @pytest.mark.asyncio
    async def test_load_data_file_not_found(self):
        """Test loading data from non-existent file."""
        repo = CSVInflationRepository("non_existent_file.csv")

        with pytest.raises(DataLoadError) as exc_info:
            await repo.load_data()

        assert "CSV file not found" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_load_data_empty_file(self, empty_csv_file: Path):
        """Test loading data from empty file."""
        repo = CSVInflationRepository(empty_csv_file)

        with pytest.raises(DataLoadError) as exc_info:
            await repo.load_data()

        assert "empty" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_load_data_invalid_format(self, invalid_csv_file: Path):
        """Test loading data from file with invalid data."""
        repo = CSVInflationRepository(invalid_csv_file)

        # Should load successfully but skip invalid rows
        await repo.load_data()

        # Should only have one valid row
        assert len(repo._data) == 1
        assert 2022 in repo._data
        assert repo._data[2022] == Decimal("6.5")

    @pytest.mark.asyncio
    async def test_get_inflation_rate(self, csv_repository: CSVInflationRepository):
        """Test getting inflation rate by year."""
        rate = await csv_repository.get_inflation_rate(2020)
        assert rate == Decimal("1.4")

        # Test non-existent year
        rate = await csv_repository.get_inflation_rate(1999)
        assert rate is None

    @pytest.mark.asyncio
    async def test_get_inflation_rate_auto_loads(self, temp_csv_file: Path):
        """Test that get_inflation_rate auto-loads data if not loaded."""
        repo = CSVInflationRepository(temp_csv_file)
        assert repo._loaded is False

        rate = await repo.get_inflation_rate(2020)
        assert rate == Decimal("1.4")
        assert repo._loaded is True

    @pytest.mark.asyncio
    async def test_get_all_rates(self, csv_repository: CSVInflationRepository):
        """Test getting all rates."""
        rates = await csv_repository.get_all_rates()

        assert isinstance(rates, dict)
        assert len(rates) == 5  # Based on test data
        assert rates[2020] == Decimal("1.4")
        assert rates[2024] == Decimal("2.1")

    @pytest.mark.asyncio
    async def test_get_available_years(self, csv_repository: CSVInflationRepository):
        """Test getting available years."""
        years = await csv_repository.get_available_years()

        assert isinstance(years, list)
        assert years == [2020, 2021, 2022, 2023, 2024]
        assert all(isinstance(year, int) for year in years)

    @pytest.mark.asyncio
    async def test_get_year_range(self, csv_repository: CSVInflationRepository):
        """Test getting year range."""
        year_range = await csv_repository.get_year_range()

        assert year_range == (2020, 2024)

    @pytest.mark.asyncio
    async def test_get_year_range_empty_data(self, empty_csv_file: Path):
        """Test getting year range with no data."""
        repo = CSVInflationRepository(empty_csv_file)

        with pytest.raises(DataLoadError):
            await repo.get_year_range()

    @pytest.mark.asyncio
    async def test_data_persistence_after_load(self, csv_repository: CSVInflationRepository):
        """Test that data persists after initial load."""
        # Load data
        await csv_repository.load_data()
        initial_data = csv_repository._data.copy()

        # Call methods that trigger auto-load
        rate = await csv_repository.get_inflation_rate(2020)

        # Data should be the same
        assert csv_repository._data == initial_data
        assert rate == Decimal("1.4")
