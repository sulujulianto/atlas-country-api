from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_capitals():
    resp = client.get("/capitals?sort_by=population&order=desc")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data[0]["name"] == "Tokyo"
    assert len(data) > 0
    assert resp.json()["meta"]["total_items"] >= len(data)


def test_get_capital_by_name():
    resp = client.get("/capitals/Tokyo")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["country"] == "Japan"


def test_get_capital_by_name_returns_404_for_unknown():
    resp = client.get("/capitals/UnknownCity")
    assert resp.status_code == 404
    payload = resp.json()
    assert payload["status"] == "error"
    assert payload["code"] == "ERR_NOT_FOUND"


def test_list_capitals_returns_422_for_invalid_pagination():
    resp_page = client.get("/capitals?page=0&size=5")
    assert resp_page.status_code == 422
    resp_size = client.get("/capitals?page=1&size=150")
    assert resp_size.status_code == 422


def test_capitals_invalid_sort_field_returns_400():
    resp = client.get("/capitals?sort_by=invalid_field")
    assert resp.status_code == 400
    payload = resp.json()
    assert payload["code"] == "ERR_BAD_REQUEST"
