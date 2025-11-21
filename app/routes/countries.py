from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.exceptions import BadRequestError, NotFoundError
from app.models import (
    CountryModel,
    PaginationMeta,
    PaginationRequest,
    ResponseModel,
    SearchQueryModel,
)
from app.repositories import CountryRepository
from app.services import CountryService

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "countries.json"

router = APIRouter()


def get_country_service() -> CountryService:
    repo = CountryRepository(DATA_PATH)
    return CountryService(repo)


def build_response(data, meta: PaginationMeta | None = None) -> ResponseModel:
    return ResponseModel(status="success", data=data, meta=meta.model_dump() if meta else None, error=None)


@router.get(
    "",
    response_model=ResponseModel,
    summary="List countries",
    description="List countries with pagination, sorting, filtering, and search across name, official_name, and capital.",
)
async def list_countries(
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=10, ge=1, le=100, description="Page size"),
    name: Optional[str] = Query(default=None, description="Search term for country name/official name/capital"),
    region: Optional[str] = Query(default=None, description="Filter by region"),
    subregion: Optional[str] = Query(default=None, description="Filter by subregion"),
    min_population: Optional[int] = Query(default=None, ge=0, description="Minimum population"),
    max_population: Optional[int] = Query(default=None, ge=0, description="Maximum population"),
    min_area: Optional[float] = Query(default=None, ge=0, description="Minimum area"),
    max_area: Optional[float] = Query(default=None, ge=0, description="Maximum area"),
    language: Optional[str] = Query(default=None, description="Filter by language"),
    currency: Optional[str] = Query(default=None, description="Filter by currency"),
    sort_by: Optional[str] = Query(default=None, description="Field to sort by"),
    order: str = Query(default="asc", pattern="^(asc|desc)$", description="Sort order"),
    service: CountryService = Depends(get_country_service),
) -> ResponseModel:
    def _unwrap(value):
        return value.default if isinstance(value, Query) else value

    page = _unwrap(page)
    size = _unwrap(size)
    name = _unwrap(name)
    region = _unwrap(region)
    subregion = _unwrap(subregion)
    min_population = _unwrap(min_population)
    max_population = _unwrap(max_population)
    min_area = _unwrap(min_area)
    max_area = _unwrap(max_area)
    language = _unwrap(language)
    currency = _unwrap(currency)
    sort_by = _unwrap(sort_by)
    order = _unwrap(order)

    query = SearchQueryModel(
        name=name,
        region=region,
        subregion=subregion,
        min_population=min_population,
        max_population=max_population,
        min_area=min_area,
        max_area=max_area,
        language=language,
        currency=currency,
        sort_by=sort_by,
        order=order,
    )
    pagination = PaginationRequest(page=page, size=size)
    items, meta = service.list_countries(pagination, query)
    return build_response(data=[item.model_dump() for item in items], meta=meta)


@router.get(
    "/{code}",
    response_model=ResponseModel,
    summary="Get country by code",
    description="Retrieve a single country by its ISO country code (2 or 3 letters).",
)
async def get_country_by_code(
    code: str,
    service: CountryService = Depends(get_country_service),
) -> ResponseModel:
    country = service.get_by_code(code)
    return build_response(data=country.model_dump())


@router.get(
    "/search",
    response_model=ResponseModel,
    summary="Search countries",
    description="Advanced search for countries using name, region, subregion, population/area ranges, language, currency, and sorting.",
)
async def search_countries(
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=10, ge=1, le=100, description="Page size"),
    name: Optional[str] = Query(default=None, description="Search term"),
    region: Optional[str] = Query(default=None, description="Filter by region"),
    subregion: Optional[str] = Query(default=None, description="Filter by subregion"),
    min_population: Optional[int] = Query(default=None, ge=0, description="Minimum population"),
    max_population: Optional[int] = Query(default=None, ge=0, description="Maximum population"),
    min_area: Optional[float] = Query(default=None, ge=0, description="Minimum area"),
    max_area: Optional[float] = Query(default=None, ge=0, description="Maximum area"),
    language: Optional[str] = Query(default=None, description="Filter by language"),
    currency: Optional[str] = Query(default=None, description="Filter by currency"),
    sort_by: Optional[str] = Query(default=None, description="Field to sort by"),
    order: str = Query(default="asc", pattern="^(asc|desc)$", description="Sort order"),
    service: CountryService = Depends(get_country_service),
) -> ResponseModel:
    def _unwrap(value):
        return value.default if isinstance(value, Query) else value

    page = _unwrap(page)
    size = _unwrap(size)
    name = _unwrap(name)
    region = _unwrap(region)
    subregion = _unwrap(subregion)
    min_population = _unwrap(min_population)
    max_population = _unwrap(max_population)
    min_area = _unwrap(min_area)
    max_area = _unwrap(max_area)
    language = _unwrap(language)
    currency = _unwrap(currency)
    sort_by = _unwrap(sort_by)
    order = _unwrap(order)

    query = SearchQueryModel(
        name=name,
        region=region,
        subregion=subregion,
        min_population=min_population,
        max_population=max_population,
        min_area=min_area,
        max_area=max_area,
        language=language,
        currency=currency,
        sort_by=sort_by,
        order=order,
    )
    pagination = PaginationRequest(page=page, size=size)
    items, meta = service.list_countries(pagination, query)
    return build_response(data=[item.model_dump() for item in items], meta=meta)


@router.get(
    "/region/{region}",
    response_model=ResponseModel,
    summary="List countries by region",
    description="Filter countries by region with pagination.",
)
async def get_by_region(
    region: str,
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=10, ge=1, le=100, description="Page size"),
    service: CountryService = Depends(get_country_service),
) -> ResponseModel:
    def _unwrap(value):
        return value.default if isinstance(value, Query) else value

    pagination = PaginationRequest(page=_unwrap(page), size=_unwrap(size))
    items, meta = service.get_by_region(region, pagination)
    return build_response(data=[i.model_dump() for i in items], meta=meta)


@router.get(
    "/subregion/{subregion}",
    response_model=ResponseModel,
    summary="List countries by subregion",
    description="Filter countries by subregion with pagination.",
)
async def get_by_subregion(
    subregion: str,
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=10, ge=1, le=100, description="Page size"),
    service: CountryService = Depends(get_country_service),
) -> ResponseModel:
    def _unwrap(value):
        return value.default if isinstance(value, Query) else value

    pagination = PaginationRequest(page=_unwrap(page), size=_unwrap(size))
    items, meta = service.get_by_subregion(subregion, pagination)
    return build_response(data=[i.model_dump() for i in items], meta=meta)


@router.get(
    "/language/{language}",
    response_model=ResponseModel,
    summary="List countries by language",
    description="Filter countries by official language with pagination.",
)
async def get_by_language(
    language: str,
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=10, ge=1, le=100, description="Page size"),
    service: CountryService = Depends(get_country_service),
) -> ResponseModel:
    def _unwrap(value):
        return value.default if isinstance(value, Query) else value

    pagination = PaginationRequest(page=_unwrap(page), size=_unwrap(size))
    items, meta = service.get_by_language(language, pagination)
    return build_response(data=[i.model_dump() for i in items], meta=meta)


@router.get(
    "/currency/{currency}",
    response_model=ResponseModel,
    summary="List countries by currency",
    description="Filter countries by currency with pagination.",
)
async def get_by_currency(
    currency: str,
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=10, ge=1, le=100, description="Page size"),
    service: CountryService = Depends(get_country_service),
) -> ResponseModel:
    def _unwrap(value):
        return value.default if isinstance(value, Query) else value

    pagination = PaginationRequest(page=_unwrap(page), size=_unwrap(size))
    items, meta = service.get_by_currency(currency, pagination)
    return build_response(data=[i.model_dump() for i in items], meta=meta)
