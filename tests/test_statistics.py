from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_statistics_totals_and_regions():
    resp = client.get("/statistics/totals")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["countries"] == 6
    assert data["capitals"] == 6

    regions = client.get("/statistics/regions")
    assert regions.status_code == 200
    region_data = regions.json()["data"]
    assert region_data["Asia"] == 2
    assert region_data["Europe"] == 2


def test_statistics_top_population():
    resp = client.get("/statistics/top-population/largest?limit=3")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) == 3
    assert data[0]["name"] == "United States"

    smallest = client.get("/statistics/top-population/smallest?limit=2")
    assert smallest.status_code == 200
    assert len(smallest.json()["data"]) == 2
