from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_countries_pagination_and_filter():
    resp = client.get("/countries?region=Europe&page=1&size=2")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["status"] == "success"
    assert payload["meta"]["total_items"] == 2
    names = {item["name"] for item in payload["data"]}
    assert names == {"France", "Germany"}


def test_get_single_country():
    resp = client.get("/countries/ID")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["name"] == "Indonesia"
    assert data["country_code"] == "ID"


def test_search_sort_and_order():
    resp = client.get("/countries/search?name=a&page=1&size=5&sort_by=population&order=desc")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data[0]["name"] == "United States"
    meta = resp.json()["meta"]
    assert meta["page"] == 1


def test_language_and_currency_filters():
    resp = client.get("/countries/language/Portuguese?page=1&size=5")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data[0]["name"] == "Brazil"

    resp_currency = client.get("/countries/currency/EUR?page=1&size=5")
    assert resp_currency.status_code == 200
    names = {c["name"] for c in resp_currency.json()["data"]}
    assert names == {"France", "Germany"}


def test_get_country_by_code_returns_404_for_unknown_code():
    resp = client.get("/countries/ZZZ")
    assert resp.status_code == 404
    payload = resp.json()
    assert payload["status"] == "error"
    assert payload["code"] == "ERR_NOT_FOUND"


def test_list_countries_returns_422_for_invalid_pagination():
    # page cannot be 0, size cannot exceed 100
    resp_page = client.get("/countries?page=0&size=10")
    assert resp_page.status_code == 422
    resp_size = client.get("/countries?page=1&size=101")
    assert resp_size.status_code == 422


def test_search_returns_empty_for_no_matches():
    resp = client.get("/countries/search?name=nonexistentvalue")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["data"] == []
    assert payload["meta"]["total_items"] == 0
