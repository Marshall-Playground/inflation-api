"""API v1 package."""

from fastapi import APIRouter

from . import inflation

api_router = APIRouter()
api_router.include_router(inflation.router, prefix="/inflation", tags=["inflation"])

__all__ = ["api_router"]
