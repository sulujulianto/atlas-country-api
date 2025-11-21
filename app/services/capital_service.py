from typing import List

from app.exceptions import BadRequestError, NotFoundError
from app.models import CapitalModel, PaginationMeta, PaginationRequest, SearchQueryModel
from app.repositories import CapitalRepository
from app.utils import matches_query, paginate_items


class CapitalService:
    def __init__(self, repository: CapitalRepository):
        self.repository = repository

    def list_capitals(self, pagination: PaginationRequest, query: SearchQueryModel | None = None) -> tuple[List[CapitalModel], PaginationMeta]:
        query = query or SearchQueryModel()
        capitals = self.repository.get_all_capitals()
        capitals = matches_query(capitals, lambda c: c.name, query.name)
        if query.sort_by:
            if not hasattr(CapitalModel, query.sort_by):
                raise BadRequestError(f"Invalid sort field: {query.sort_by}")
            descending = query.order == "desc"
            capitals = self.repository.sort(capitals, query.sort_by, descending)
        items, meta = paginate_items(capitals, pagination.page, pagination.size)
        return items, meta

    def get_by_name(self, name: str) -> CapitalModel:
        capital = self.repository.get_by_name(name)
        if not capital:
            raise NotFoundError(f"Capital '{name}' not found")
        return capital
