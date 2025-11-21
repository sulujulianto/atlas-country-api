import pytest
from fastapi import HTTPException

from app.main import create_app
from app.routes import capitals, statistics
from app.services import country_service


def _get_health_payload():
    app = create_app()
    health_route = next(route for route in app.routes if getattr(route, "path", "") == "/health")
    return health_route.endpoint()


def test_health_payload():
    payload = _get_health_payload()
    assert payload["status"] == "ok"
    assert "Atlas Country API" in payload["message"]


def test_list_countries_defaults():
    response = capitals.list_countries()
    assert response.total == 8
    assert response.offset == 0
    assert response.limit == 10
    assert len(response.items) == 8


def test_list_countries_filters_and_search():
    europe = capitals.list_countries(region="Europe")
    names = {country.name for country in europe.items}
    assert europe.total == 2
    assert names == {"France", "Germany"}

    search = capitals.list_countries(search="indo")
    assert search.total == 1
    assert search.items[0].code == "ID"


def test_country_detail_endpoints():
    by_code = capitals.get_country_by_code("ID")
    assert by_code.name == "Indonesia"

    by_name = capitals.get_country_by_name("Japan")
    assert by_name.code == "JP"

    with pytest.raises(HTTPException) as exc:
        capitals.get_country_by_code("XX")
    assert exc.value.status_code == 404


def test_regions_and_random():
    regions = capitals.list_regions()
    as_dict = {entry.region: entry.country_count for entry in regions}
    assert as_dict == {"Africa": 1, "Americas": 2, "Asia": 2, "Europe": 2, "Oceania": 1}

    random_country = capitals.get_random_country()
    assert {"code", "name", "capital"} <= set(random_country.model_dump().keys())


def test_statistics():
    largest_population = statistics.largest_population()
    assert largest_population.name == "United States"

    longest_name = statistics.longest_name()
    assert longest_name.name == "United States"

    region_counts = statistics.region_counts()
    assert region_counts == {"Africa": 1, "Americas": 2, "Asia": 2, "Europe": 2, "Oceania": 1}
