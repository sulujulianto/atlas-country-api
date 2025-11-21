from fastapi import APIRouter

from app.routes.countries import router as countries_router
from app.routes.capitals import router as capitals_router

api_router = APIRouter()
api_router.include_router(countries_router, prefix="/countries", tags=["Countries"])
api_router.include_router(capitals_router, prefix="/capitals", tags=["Capitals"])

__all__ = ["api_router"]
