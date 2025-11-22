from app.repositories import CountryRepository
from app.services import CountryService
from schemas import PaginationRequestSchema, SearchQuerySchema
from pathlib import Path


def test_service_search_and_pagination():
    service = CountryService(CountryRepository(Path("data/countries.json").resolve()))
    items, meta = service.list_countries(
        PaginationRequestSchema(page=1, size=2),
        SearchQuerySchema(region="Europe"),
    )
    assert meta.total_items == 2
    assert len(items) == 2

    # pagination boundary
    items_page2, meta_page2 = service.list_countries(
        PaginationRequestSchema(page=2, size=2),
        SearchQuerySchema(region="Europe"),
    )
    assert meta_page2.page == 2
    assert len(items_page2) == 0
