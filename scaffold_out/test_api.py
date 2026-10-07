import pytest
from fastapi.testclient import TestClient

from main import app


valid_asset = {
    "asset_id": "ZZZ-9999",
    "asset_type": "Generator",
    "unit": "Unit A",
    "location": "Site 1",
    "install_year": 2020,
    "last_inspection": "2023-01-01",
    "operating_hours": 100,
    "status": "Active",
    "criticality": "High",
    "notes": "Routine maintenance done.",
}


def test_create_asset():
    with TestClient(app) as client:
        response = client.post("/assets", json=valid_asset)
        assert response.status_code == 200
        assert response.json() == valid_asset


def test_list_assets():
    with TestClient(app) as client:
        response = client.get("/assets")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 60


def test_get_asset():
    with TestClient(app) as client:
        response = client.get("/assets/TNK-1001")
        assert response.status_code == 200
        assert response.json()["asset_id"] == "TNK-1001"


def test_create_asset_invalid_id():
    invalid_asset = valid_asset.copy()
    invalid_asset["asset_id"] = "invalid-id"

    with TestClient(app) as client:
        response = client.post("/assets", json=invalid_asset)

        assert response.status_code == 422
        body = response.json()
        assert "errors" in body
        assert body["errors"][0]["field"] == "asset_id"
        assert "asset_id must match" in body["errors"][0]["reason"]


def test_get_nonexistent_asset():
    with TestClient(app) as client:
        response = client.get("/assets/ZZZ-0000")
        assert response.status_code == 404
        assert response.json() == {"detail": "Asset not found"}


def test_update_asset():
    with TestClient(app) as client:
        asset = client.get("/assets/TNK-1001").json()
        asset["status"] = "Inactive"

        response = client.put("/assets/TNK-1001", json=asset)

        assert response.status_code == 200
        assert response.json()["status"] == "Inactive"


def test_update_asset_invalid_id():
    updated_asset = valid_asset.copy()
    updated_asset["asset_id"] = "NEW-0001"

    with TestClient(app) as client:
        response = client.put("/assets/TNK-1001", json=updated_asset)

        assert response.status_code == 400
        assert response.json() == {
            "detail": "asset_id cannot be changed"
        }


def test_delete_asset():
    with TestClient(app) as client:
        response = client.delete("/assets/TNK-1001")

        assert response.status_code == 200
        assert response.json() == {"detail": "Asset deleted"}


def test_delete_nonexistent_asset():
    with TestClient(app) as client:
        response = client.delete("/assets/ZZZ-0000")

        assert response.status_code == 404
        assert response.json() == {"detail": "Asset not found"}