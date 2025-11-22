"""Business logic layer for country operations."""

from typing import List, Tuple

from app.exceptions import BadRequestError, NotFoundError
from app.core.logging import get_logger
from app.models import CountryModel, PaginationMetaModel, PaginationModel, SearchModel
from app.repositories import CountryRepository
from app.utils import apply_numeric_filter, filter_by_list_field, matches_query, paginate_items


class CountryService:
    """Orchestrates country search, filtering, sorting, and pagination."""

    def __init__(self, repository: CountryRepository):
        """Inject repository to decouple I/O from business logic."""
        self.repository = repository
        self.logger = get_logger("atlas.service.country")

    def list_countries(
        self,
        pagination: PaginationModel,
        query: SearchModel,
    ) -> Tuple[List[CountryModel], PaginationMetaModel]:
        """
        Return countries matching search/filter criteria with pagination.

        - Text search across name, official_name, capital (case-insensitive, partial).
        - Region/subregion exact match (case-insensitive).
        - Numeric range filters for population and area.
        - Language/currency membership filters.
        - Sorting by any valid CountryModel field.
        """
        countries = self.repository.get_all_countries()

        # Text search: name
        countries = matches_query(countries, lambda c: c.name, query.name)
        if query.name:
            base = self.repository.get_all_countries()
            extras = [
                *matches_query(base, lambda c: c.official_name, query.name),
                *matches_query(base, lambda c: c.capital, query.name),
            ]
            dedup = {c.country_code: c for c in [*countries, *extras]}
            countries = list(dedup.values())

        # Region/subregion filters
        if query.region:
            countries = [c for c in countries if c.region.lower() == query.region.lower()]
        if query.subregion:
            countries = [c for c in countries if c.subregion.lower() == query.subregion.lower()]

        # Numeric filters
        countries = apply_numeric_filter(countries, lambda c: c.population, query.min_population, query.max_population)
        countries = apply_numeric_filter(countries, lambda c: c.area, query.min_area, query.max_area)

        # List membership filters
        countries = filter_by_list_field(countries, lambda c: c.languages, query.language)
        countries = filter_by_list_field(countries, lambda c: c.currencies, query.currency)

        # Sorting
        if query.sort_by:
            if query.sort_by not in CountryModel.model_fields:
                self.logger.warning("Invalid sort field", extra={"extra": {"sort_by": query.sort_by}})
                raise BadRequestError(f"Invalid sort field: {query.sort_by}", {"sort_by": query.sort_by})
            descending = query.order == "desc"
            countries = sorted(countries, key=lambda c: getattr(c, query.sort_by), reverse=descending)

        items, meta = paginate_items(countries, pagination.page, pagination.size)
        return items, meta

    def get_by_code(self, code: str) -> CountryModel:
        """Fetch a single country by ISO code, case-insensitive."""
        country = self.repository.get_country_by_code(code)
        if not country:
            self.logger.info("Country not found", extra={"extra": {"code": code}})
            raise NotFoundError(f"Country with code '{code}' not found", {"code": code})
        return country

    def get_by_region(self, region: str, pagination: PaginationModel) -> Tuple[List[CountryModel], PaginationMetaModel]:
        """List countries filtered by region with pagination."""
        countries = self.repository.get_by_region(region)
        return paginate_items(countries, pagination.page, pagination.size)

    def get_by_subregion(self, subregion: str, pagination: PaginationModel) -> Tuple[List[CountryModel], PaginationMetaModel]:
        """List countries filtered by subregion with pagination."""
        countries = self.repository.get_by_subregion(subregion)
        return paginate_items(countries, pagination.page, pagination.size)

    def get_by_language(self, language: str, pagination: PaginationModel) -> Tuple[List[CountryModel], PaginationMetaModel]:
        """List countries that speak the given language (case-insensitive) with pagination."""
        countries = filter_by_list_field(self.repository.get_all_countries(), lambda c: c.languages, language)
        return paginate_items(countries, pagination.page, pagination.size)

    def get_by_currency(self, currency: str, pagination: PaginationModel) -> Tuple[List[CountryModel], PaginationMetaModel]:
        """List countries that use the given currency (case-insensitive) with pagination."""
        countries = filter_by_list_field(self.repository.get_all_countries(), lambda c: c.currencies, currency)
        return paginate_items(countries, pagination.page, pagination.size)
