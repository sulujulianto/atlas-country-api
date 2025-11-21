from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.models import PaginationRequest, ResponseModel, SearchQueryModel
from app.repositories import CapitalRepository
from app.services import CapitalService

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "capitals.json"

router = APIRouter()


def get_capital_service() -> CapitalService:
    repo = CapitalRepository(DATA_PATH)
    return CapitalService(repo)


def build_response(data, meta=None) -> ResponseModel:
    return ResponseModel(status="success", data=data, meta=meta.model_dump() if meta else None, error=None)


@router.get(
    "",
    response_model=ResponseModel,
    summary="List capitals",
    description="List capitals with pagination, optional name search, and sorting.",
)
async def list_capitals(
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=10, ge=1, le=100, description="Page size"),
    name: Optional[str] = Query(default=None, description="Search term for capital name"),
    sort_by: Optional[str] = Query(default=None, description="Field to sort by (e.g., population)"),
    order: str = Query(default="asc", pattern="^(asc|desc)$", description="Sort order"),
    service: CapitalService = Depends(get_capital_service),
) -> ResponseModel:
    def _unwrap(value):
        return value.default if isinstance(value, Query) else value

    page = _unwrap(page)
    size = _unwrap(size)
    name = _unwrap(name)
    sort_by = _unwrap(sort_by)
    order = _unwrap(order)

    query = SearchQueryModel(name=name, sort_by=sort_by, order=order)
    pagination = PaginationRequest(page=page, size=size)
    items, meta = service.list_capitals(pagination, query)
    return build_response(data=[i.model_dump() for i in items], meta=meta)


@router.get(
    "/{name}",
    response_model=ResponseModel,
    summary="Get capital by name",
    description="Retrieve a single capital by its name.",
)
async def get_capital_by_name(
    name: str,
    service: CapitalService = Depends(get_capital_service),
) -> ResponseModel:
    capital = service.get_by_name(name)
    return build_response(data=capital.model_dump())
