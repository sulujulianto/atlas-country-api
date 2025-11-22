"""Business logic layer for capital operations."""

from typing import List, Tuple

from app.exceptions import BadRequestError, NotFoundError
from app.core.logging import get_logger
from app.models import CapitalModel, PaginationMetaModel, PaginationModel, SearchModel
from app.repositories import CapitalRepository
from app.utils import matches_query, paginate_items


class CapitalService:
    """Orchestrates capital search, sorting, and pagination."""

    def __init__(self, repository: CapitalRepository):
        """Inject repository to decouple I/O from business logic."""
        self.repository = repository
        self.logger = get_logger("atlas.service.capital")

    def list_capitals(
        self,
        pagination: PaginationModel,
        query: SearchModel,
    ) -> Tuple[List[CapitalModel], PaginationMetaModel]:
        """
        Return capitals matching search criteria with pagination.

        - Text search by name (case-insensitive partial).
        - Optional sorting by any valid CapitalModel field.
        """
        capitals = self.repository.get_all_capitals()
        capitals = matches_query(capitals, lambda c: c.name, query.name)

        if query.sort_by is not None:
            if query.sort_by not in CapitalModel.model_fields:
                self.logger.warning("Invalid capital sort field", extra={"extra": {"sort_by": query.sort_by}})
                raise BadRequestError(f"Invalid sort field: {query.sort_by}", {"sort_by": query.sort_by})
            descending = query.order == "desc"
            sort_field = query.sort_by
            capitals = sorted(capitals, key=lambda c: getattr(c, sort_field), reverse=descending)

        items, meta = paginate_items(capitals, pagination.page, pagination.size)
        return items, meta

    def get_by_name(self, name: str) -> CapitalModel:
        """Fetch a single capital by name, case-insensitive."""
        capital = self.repository.get_by_name(name)
        if not capital:
            self.logger.info("Capital not found", extra={"extra": {"name": name}})
            raise NotFoundError(f"Capital '{name}' not found", {"name": name})
        return capital
