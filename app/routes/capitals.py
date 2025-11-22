from pathlib import Path
from typing import Literal, Optional, cast

from fastapi import APIRouter, Depends, Query

from app.models import PaginationModel, SearchModel
from app.repositories import CapitalRepository
from app.services import CapitalService
from schemas import ResponseSchema

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "capitals.json"

router = APIRouter()


def get_capital_service() -> CapitalService:
    repo = CapitalRepository(DATA_PATH)
    return CapitalService(repo)


def build_response(data, meta=None) -> ResponseSchema:
    return ResponseSchema(status="success", data=data, meta=meta.model_dump() if meta else None, error=None)


@router.get(
    "",
    response_model=ResponseSchema,
    summary="List capitals",
    description="List capitals with pagination, optional name search, and sorting.",
)
async def list_capitals(
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=10, ge=1, le=100, description="Page size"),
    name: Optional[str] = Query(default=None, description="Search term for capital name"),
    sort_by: Optional[str] = Query(default=None, description="Field to sort by (e.g., population)"),
    order: Literal["asc", "desc"] = Query(default="asc", description="Sort order"),
    service: CapitalService = Depends(get_capital_service),
) -> ResponseSchema:
    def _clean(value):
        return value.strip() if isinstance(value, str) else value

    query = SearchModel(
        name=_clean(name),
        sort_by=_clean(sort_by),
        order=cast(Literal["asc", "desc"], _clean(order) or "asc"),
        region=None,
        subregion=None,
        min_population=None,
        max_population=None,
        min_area=None,
        max_area=None,
        language=None,
        currency=None,
    )
    pagination = PaginationModel(page=int(page), size=int(size))
    items, meta = service.list_capitals(pagination, query)
    return build_response(data=[i.model_dump() for i in items], meta=meta)


@router.get(
    "/{name}",
    response_model=ResponseSchema,
    summary="Get capital by name",
    description="Retrieve a single capital by its name.",
)
async def get_capital_by_name(
    name: str,
    service: CapitalService = Depends(get_capital_service),
) -> ResponseSchema:
    capital = service.get_by_name(name.strip())
    return build_response(data=capital.model_dump())
