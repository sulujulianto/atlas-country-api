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
