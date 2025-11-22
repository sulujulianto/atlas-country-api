from pathlib import Path

from fastapi import APIRouter, Depends, Query

from app.repositories import CapitalRepository, CountryRepository
from app.services import StatisticsService
from schemas import ResponseSchema

COUNTRY_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "countries.json"
CAPITAL_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "capitals.json"

router = APIRouter()


def get_statistics_service() -> StatisticsService:
    country_repo = CountryRepository(COUNTRY_DATA_PATH)
    capital_repo = CapitalRepository(CAPITAL_DATA_PATH)
    return StatisticsService(country_repo, capital_repo)


def build_response(data) -> ResponseSchema:
    return ResponseSchema(status="success", data=data, meta=None, error=None)


@router.get(
    "/totals",
    response_model=ResponseSchema,
    summary="Totals",
    description="Return total counts for countries and capitals.",
)
async def totals(service: StatisticsService = Depends(get_statistics_service)) -> ResponseSchema:
    return build_response({"countries": service.total_countries(), "capitals": service.total_capitals()})


@router.get(
    "/top-population/largest",
    response_model=ResponseSchema,
    summary="Top largest populations",
    description="Top N countries by population (default 5).",
)
async def top_largest(
    service: StatisticsService = Depends(get_statistics_service),
    limit: int = Query(default=5, ge=1, le=100, description="Number of records to return"),
) -> ResponseSchema:
    return build_response(service.top_largest_populations(limit))


@router.get(
    "/top-population/smallest",
    response_model=ResponseSchema,
    summary="Top smallest populations",
    description="Top N smallest population countries (default 5).",
)
async def top_smallest(
    service: StatisticsService = Depends(get_statistics_service),
    limit: int = Query(default=5, ge=1, le=100, description="Number of records to return"),
) -> ResponseSchema:
    return build_response(service.top_smallest_populations(limit))


@router.get(
    "/regions",
    response_model=ResponseSchema,
    summary="Region distribution",
    description="Distribution of countries by region.",
)
async def region_distribution(service: StatisticsService = Depends(get_statistics_service)) -> ResponseSchema:
    return build_response(service.region_distribution())


@router.get(
    "/languages",
    response_model=ResponseSchema,
    summary="Language distribution",
    description="Distribution of languages across countries.",
)
async def language_distribution(service: StatisticsService = Depends(get_statistics_service)) -> ResponseSchema:
    return build_response(service.language_distribution())
