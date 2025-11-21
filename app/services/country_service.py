from typing import List

from app.exceptions import BadRequestError, NotFoundError
from app.models import CountryModel, PaginationMeta, PaginationRequest, SearchQueryModel
from app.repositories import CountryRepository
from app.utils import apply_numeric_filter, filter_by_list_field, matches_query, paginate_items


class CountryService:
    def __init__(self, repository: CountryRepository):
        self.repository = repository

    def list_countries(self, pagination: PaginationRequest, query: SearchQueryModel | None = None) -> tuple[List[CountryModel], PaginationMeta]:
        query = query or SearchQueryModel()
        countries = self.repository.get_all_countries()

        # name search (name or official_name or capital)
        countries = matches_query(countries, lambda c: c.name, query.name)
        if query.name:
            # extend match on official_name and capital
            base = self.repository.get_all_countries()
            extras = [
                *matches_query(base, lambda c: c.official_name, query.name),
                *matches_query(base, lambda c: c.capital, query.name),
            ]
            countries = list({c.country_code: c for c in [*countries, *extras]}.values())
        if query.region:
            countries = [c for c in countries if c.region.lower() == query.region.lower()]
        if query.subregion:
            countries = [c for c in countries if c.subregion.lower() == query.subregion.lower()]
        countries = apply_numeric_filter(countries, lambda c: c.population, query.min_population, query.max_population)
        countries = apply_numeric_filter(countries, lambda c: c.area, query.min_area, query.max_area)
        countries = filter_by_list_field(countries, lambda c: c.languages, query.language)
        countries = filter_by_list_field(countries, lambda c: c.currencies, query.currency)

        if query.sort_by:
            if not hasattr(CountryModel, query.sort_by):
                raise BadRequestError(f"Invalid sort field: {query.sort_by}")
            descending = query.order == "desc"
            countries = self.repository.sort(countries, query.sort_by, descending)

        items, meta = paginate_items(countries, pagination.page, pagination.size)
        return items, meta

    def get_by_code(self, code: str) -> CountryModel:
        country = self.repository.get_country_by_code(code)
        if not country:
            raise NotFoundError(f"Country with code '{code}' not found")
        return country

    def get_by_region(self, region: str, pagination: PaginationRequest) -> tuple[List[CountryModel], PaginationMeta]:
        countries = self.repository.get_by_region(region)
        items, meta = paginate_items(countries, pagination.page, pagination.size)
        return items, meta

    def get_by_subregion(self, subregion: str, pagination: PaginationRequest) -> tuple[List[CountryModel], PaginationMeta]:
        countries = self.repository.get_by_subregion(subregion)
        items, meta = paginate_items(countries, pagination.page, pagination.size)
        return items, meta

    def get_by_language(self, language: str, pagination: PaginationRequest) -> tuple[List[CountryModel], PaginationMeta]:
        countries = filter_by_list_field(self.repository.get_all_countries(), lambda c: c.languages, language)
        items, meta = paginate_items(countries, pagination.page, pagination.size)
        return items, meta

    def get_by_currency(self, currency: str, pagination: PaginationRequest) -> tuple[List[CountryModel], PaginationMeta]:
        countries = filter_by_list_field(self.repository.get_all_countries(), lambda c: c.currencies, currency)
        items, meta = paginate_items(countries, pagination.page, pagination.size)
        return items, meta
