from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.params import Query as QueryParam

from app.core.security import verify_api_key
from app.models import Country, CountryListResponse, ErrorResponse, RegionSummary
from app.services import country_service
from app.services.country_service import DataSourceError


router = APIRouter(
    prefix="/api/v1/countries",
    tags=["Countries"],
    dependencies=[Depends(verify_api_key)],
)


@router.get(
    "/",
    response_model=CountryListResponse,
    summary="List countries",
    description=(
        "Return a paginated list of countries. "
        "You can filter by region and search by country or capital name."
    ),
)
def list_countries(
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip from the beginning"),
    search: Optional[str] = Query(
        None,
        description="Search by country or capital name (case-insensitive partial match)",
    ),
    region: Optional[str] = Query(
        None,
        description="Filter by region name (e.g. 'Asia', 'Europe')",
    ),
):
    def _unwrap(value):
        return value.default if isinstance(value, QueryParam) else value

    limit = _unwrap(limit)
    offset = _unwrap(offset)
    search = _unwrap(search)
    region = _unwrap(region)

    try:
        countries = country_service.filter_countries(region=region, search=search)
    except DataSourceError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    total = len(countries)
    items = countries[offset: offset + limit]

    return CountryListResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=items,
    )


@router.get(
    "/regions",
    response_model=List[RegionSummary],
    summary="List regions",
    description="Return available regions with the number of countries in each region.",
)
def list_regions():
    try:
        countries = country_service.get_countries()
    except DataSourceError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return country_service.get_region_summaries(countries)


@router.get(
    "/random",
    response_model=Country,
    summary="Get a random country",
    description="Return a single random country from the dataset.",
)
def get_random_country():
    try:
        country = country_service.random_country()
    except DataSourceError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    if not country:
        raise HTTPException(status_code=404, detail="No countries available")

    return country


@router.get(
    "/by-code/{country_code}",
    response_model=Country,
    responses={404: {"model": ErrorResponse}},
    summary="Get country by ISO code",
    description="Return country details for the given ISO code (e.g. 'ID', 'JP').",
)
def get_country_by_code(country_code: str):
    try:
        country = country_service.find_by_code(country_code)
    except DataSourceError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    if country:
        return country

    raise HTTPException(status_code=404, detail=f"Country with code '{country_code}' not found")


@router.get(
    "/by-name/{country_name}",
    response_model=Country,
    responses={404: {"model": ErrorResponse}},
    summary="Get country by name",
    description="Return country details for the given country name (e.g. 'Indonesia').",
)
def get_country_by_name(country_name: str):
    try:
        country = country_service.find_by_name(country_name)
    except DataSourceError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    if country:
        return country

    raise HTTPException(status_code=404, detail=f"Country named '{country_name}' not found")
