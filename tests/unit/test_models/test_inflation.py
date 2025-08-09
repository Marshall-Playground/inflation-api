"""Unit tests for inflation models."""

from decimal import Decimal

import pytest
from pydantic import ValidationError

from inflation_api.models import (
    CurrentValueRequest,
    InflationRate,
    ValueChangeRequest,
)


class TestInflationRate:
    """Test InflationRate model."""

    def test_valid_inflation_rate(self):
        """Test creating a valid inflation rate."""
        rate = InflationRate(year=2020, rate=1.4)
        assert rate.year == 2020
        assert rate.rate == Decimal("1.4")

    def test_rate_conversion_to_decimal(self):
        """Test that rates are converted to Decimal."""
        rate = InflationRate(year=2020, rate=1.4)
        assert isinstance(rate.rate, Decimal)
        assert rate.rate == Decimal("1.4")

        # Test string conversion
        rate = InflationRate(year=2020, rate="1.4")
        assert isinstance(rate.rate, Decimal)
        assert rate.rate == Decimal("1.4")

    def test_invalid_year_range(self):
        """Test validation of year range."""
        # Year too low
        with pytest.raises(ValidationError):
            InflationRate(year=1799, rate=1.4)

        # Year too high
        with pytest.raises(ValidationError):
            InflationRate(year=2101, rate=1.4)

    def test_invalid_rate_range(self):
        """Test validation of rate range."""
        # Rate too low
        with pytest.raises(ValidationError):
            InflationRate(year=2020, rate=-21)

        # Rate too high
        with pytest.raises(ValidationError):
            InflationRate(year=2020, rate=51)


class TestValueChangeRequest:
    """Test ValueChangeRequest model."""

    def test_valid_value_change_request(self):
        """Test creating a valid value change request."""
        request = ValueChangeRequest(start_year=2020, end_year=2022)
        assert request.start_year == 2020
        assert request.end_year == 2022

    def test_same_start_end_year_invalid(self):
        """Test that same start and end year is invalid."""
        with pytest.raises(ValidationError):
            ValueChangeRequest(start_year=2020, end_year=2020)

    def test_invalid_year_range(self):
        """Test validation of year ranges."""
        with pytest.raises(ValidationError):
            ValueChangeRequest(start_year=1799, end_year=2020)

        with pytest.raises(ValidationError):
            ValueChangeRequest(start_year=2020, end_year=2101)


class TestCurrentValueRequest:
    """Test CurrentValueRequest model."""

    def test_valid_current_value_request(self):
        """Test creating a valid current value request."""
        request = CurrentValueRequest(original_year=2020)
        assert request.original_year == 2020
        assert request.amount == Decimal("1.00")

    def test_custom_amount(self):
        """Test request with custom amount."""
        request = CurrentValueRequest(original_year=2020, amount=100.50)
        assert request.amount == Decimal("100.50")
        assert isinstance(request.amount, Decimal)

    def test_amount_conversion(self):
        """Test amount conversion to Decimal."""
        # Float conversion
        request = CurrentValueRequest(original_year=2020, amount=100.5)
        assert isinstance(request.amount, Decimal)

        # String conversion
        request = CurrentValueRequest(original_year=2020, amount="100.50")
        assert isinstance(request.amount, Decimal)

    def test_negative_amount_invalid(self):
        """Test that negative amounts are invalid."""
        with pytest.raises(ValidationError):
            CurrentValueRequest(original_year=2020, amount=-1)

    def test_zero_amount_invalid(self):
        """Test that zero amount is invalid."""
        with pytest.raises(ValidationError):
            CurrentValueRequest(original_year=2020, amount=0)
