from fastapi import APIRouter

from app.routes.countries import router as countries_router
from app.routes.capitals import router as capitals_router
from app.routes.statistics import router as statistics_router

api_router = APIRouter()
api_router.include_router(countries_router, prefix="/countries", tags=["Countries"])
api_router.include_router(capitals_router, prefix="/capitals", tags=["Capitals"])
api_router.include_router(statistics_router, prefix="/statistics", tags=["Statistics"])

__all__ = ["api_router"]
