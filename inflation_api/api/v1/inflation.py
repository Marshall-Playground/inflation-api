"""Inflation API endpoints."""

import logging
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status

from inflation_api.api.dependencies import get_inflation_service
from inflation_api.core.exceptions import (
    CalculationError,
    DataNotFoundError,
    InflationAPIError,
    InvalidYearError,
)
from inflation_api.models import (
    CurrentValueRequest,
    CurrentValueResponse,
    InflationRateResponse,
    ValueChangeRequest,
    ValueChangeResponse,
)
from inflation_api.services import InflationService

logger = logging.getLogger(__name__)
router = APIRouter()


def handle_service_exceptions(e: InflationAPIError) -> HTTPException:
    """Convert service exceptions to HTTP exceptions."""
    if isinstance(e, DataNotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "details": e.details}
        )
    elif isinstance(e, InvalidYearError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )
    elif isinstance(e, CalculationError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": e.message, "details": e.details}
        )
    else:
        logger.error(f"Unexpected service error: {e}")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error", "details": None}
        )


@router.get(
    "/rate/{year}",
    response_model=InflationRateResponse,
    summary="Get inflation rate by year",
    description="Retrieve the inflation rate for a specific year"
)
async def get_inflation_rate(
    year: int,
    service: InflationService = Depends(get_inflation_service)
) -> InflationRateResponse:
    """Get inflation rate for a specific year."""
    try:
        return await service.get_inflation_rate_by_year(year)
    except InflationAPIError as e:
        raise handle_service_exceptions(e)


@router.post(
    "/value-change",
    response_model=ValueChangeResponse,
    summary="Calculate value change between years",
    description="Calculate how the value of USD changed between two years"
)
async def calculate_value_change(
    request: ValueChangeRequest,
    service: InflationService = Depends(get_inflation_service)
) -> ValueChangeResponse:
    """Calculate change in USD value between two years."""
    try:
        return await service.calculate_value_change_between_years(
            request.start_year, request.end_year
        )
    except InflationAPIError as e:
        raise handle_service_exceptions(e)


@router.get(
    "/value-change",
    response_model=ValueChangeResponse,
    summary="Calculate value change between years (GET)",
    description="Calculate how the value of USD changed between two years using query parameters"
)
async def calculate_value_change_get(
    start_year: int = Query(..., description="Starting year"),
    end_year: int = Query(..., description="Ending year"),
    service: InflationService = Depends(get_inflation_service)
) -> ValueChangeResponse:
    """Calculate change in USD value between two years (GET method)."""
    try:
        return await service.calculate_value_change_between_years(start_year, end_year)
    except InflationAPIError as e:
        raise handle_service_exceptions(e)


@router.post(
    "/current-value",
    response_model=CurrentValueResponse,
    summary="Calculate current value of historical amount",
    description="Calculate what an amount from a past year is worth today"
)
async def calculate_current_value(
    request: CurrentValueRequest,
    service: InflationService = Depends(get_inflation_service)
) -> CurrentValueResponse:
    """Calculate current value of money from a past year."""
    try:
        return await service.calculate_current_value(
            request.original_year, request.amount
        )
    except InflationAPIError as e:
        raise handle_service_exceptions(e)


@router.get(
    "/current-value",
    response_model=CurrentValueResponse,
    summary="Calculate current value of historical amount (GET)",
    description="Calculate what an amount from a past year is worth today using query parameters"
)
async def calculate_current_value_get(
    original_year: int = Query(..., description="Original year"),
    amount: Decimal = Query(Decimal("1.00"), description="Original amount"),
    service: InflationService = Depends(get_inflation_service)
) -> CurrentValueResponse:
    """Calculate current value of money from a past year (GET method)."""
    try:
        return await service.calculate_current_value(original_year, amount)
    except InflationAPIError as e:
        raise handle_service_exceptions(e)


@router.get(
    "/years",
    summary="Get available years",
    description="Get list of years with available inflation data"
)
async def get_available_years(
    service: InflationService = Depends(get_inflation_service)
) -> dict:
    """Get list of available years."""
    try:
        repository = service.repository
        years = await repository.get_available_years()
        year_range = await repository.get_year_range()

        return {
            "available_years": years,
            "year_range": {
                "min_year": year_range[0] if year_range else None,
                "max_year": year_range[1] if year_range else None
            },
            "total_years": len(years)
        }
    except InflationAPIError as e:
        raise handle_service_exceptions(e)
