from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_not_found_country():
    resp = client.get("/countries/ZZZ")
    assert resp.status_code == 404
    payload = resp.json()
    assert payload["status"] == "error"
    assert payload["code"] == "ERR_NOT_FOUND"


def test_bad_request_sort_field():
    resp = client.get("/countries?sort_by=invalid_field")
    assert resp.status_code == 400
    payload = resp.json()
    assert payload["status"] == "error"
    assert payload["code"] == "ERR_BAD_REQUEST"


def test_validation_error_missing_param():
    resp = client.get("/capitals?order=invalid")
    assert resp.status_code == 422
    payload = resp.json()
    assert payload["status"] == "error"
    assert payload["code"] == "ERR_VALIDATION"


def test_statistics_limit_bad_request():
    resp = client.get("/statistics/top-population/largest?limit=0")
    assert resp.status_code == 422
    payload = resp.json()
    assert payload["code"] == "ERR_VALIDATION"


def test_validation_error_for_negative_page():
    resp = client.get("/countries?page=-1&size=10")
    assert resp.status_code == 422
    payload = resp.json()
    assert payload["status"] == "error"
    assert payload["code"] == "ERR_VALIDATION"
