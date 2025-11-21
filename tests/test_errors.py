from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_not_found_country():
    resp = client.get("/countries/ZZZ")
    assert resp.status_code == 404
    payload = resp.json()
    assert payload["status"] == "error"
    assert payload["code"] == 404


def test_bad_request_sort_field():
    resp = client.get("/countries?sort_by=invalid_field")
    assert resp.status_code == 400
    payload = resp.json()
    assert payload["status"] == "error"
    assert payload["code"] == 400


def test_validation_error_missing_param():
    resp = client.get("/capitals?order=invalid")
    assert resp.status_code == 422
    payload = resp.json()
    assert payload["status"] == "error"
    assert payload["code"] == 422
