"""Pydantic models for inflation data."""

from decimal import Decimal
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field, field_validator


class InflationRate(BaseModel):
    """Model for inflation rate data."""

    year: int = Field(..., ge=1800, le=2100, description="Year for the inflation rate")
    rate: Decimal = Field(
        ...,
        ge=Decimal("-20"),
        le=Decimal("50"),
        description="Inflation rate as a percentage"
    )

    @field_validator("rate", mode="before")
    @classmethod
    def convert_rate_to_decimal(cls, v: Any) -> Decimal:
        """Convert rate to Decimal for precision."""
        return Decimal(str(v))


class InflationRateResponse(BaseModel):
    """Response model for getting inflation rate by year."""

    year: int
    rate: Decimal

    model_config = ConfigDict(
        json_encoders={Decimal: float}
    )


class ValueChangeRequest(BaseModel):
    """Request model for calculating value change between years."""

    start_year: int = Field(..., ge=1800, le=2100)
    end_year: int = Field(..., ge=1800, le=2100)

    @field_validator("end_year")
    @classmethod  
    def end_year_must_be_different(cls, v: int, info) -> int:
        """Ensure end year is different from start year."""
        if hasattr(info, 'data') and info.data and "start_year" in info.data and v == info.data["start_year"]:
            raise ValueError("End year must be different from start year")
        return v


class ValueChangeResponse(BaseModel):
    """Response model for value change calculation."""

    start_year: int
    end_year: int
    value_change_factor: Decimal
    description: str

    model_config = ConfigDict(
        json_encoders={Decimal: float}
    )


class CurrentValueRequest(BaseModel):
    """Request model for calculating current value of money from past year."""

    original_year: int = Field(..., ge=1800, le=2100)
    amount: Decimal = Field(default=Decimal("1.00"), gt=0)

    @field_validator("amount", mode="before")
    @classmethod
    def convert_amount_to_decimal(cls, v: Any) -> Decimal:
        """Convert amount to Decimal for precision."""
        return Decimal(str(v))


class CurrentValueResponse(BaseModel):
    """Response model for current value calculation."""

    original_year: int
    current_year: int
    original_amount: Decimal
    current_value: Decimal
    description: str

    model_config = ConfigDict(
        json_encoders={Decimal: float}
    )
