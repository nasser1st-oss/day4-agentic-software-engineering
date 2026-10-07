import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def sample_asset():
    return {
        'asset_id': 'TNK-1001',
        'asset_type': 'Generator',
        'unit': 'Unit A',
        'location': 'Site 1',
        'install_year': 2020,
        'last_inspection': '2023-01-01',
        'operating_hours': 100,
        'status': 'Active',
        'criticality': 'High',
        'notes': 'Routine maintenance'
    }

def test_create_asset(sample_asset):
    response = client.post('/assets', json=sample_asset)
    assert response.status_code == 200
    assert response.json() == sample_asset

def test_create_asset_invalid_id():
    response = client.post('/assets', json={**sample_asset, 'asset_id': 'invalid_id'})
    assert response.status_code == 422
    assert response.json() == {'errors': [{'field': 'asset_id', 'reason': 'string does not match regex '^[A-Z]{3}-\\d{4}$''}]}

def test_list_assets():
    response = client.get('/assets')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_asset(sample_asset):
    client.post('/assets', json=sample_asset)
    response = client.get('/assets/TNK-1001')
    assert response.status_code == 200
    assert response.json() == sample_asset

def test_get_asset_not_found():
    response = client.get('/assets/NOT-FOUND')
    assert response.status_code == 404

def test_update_asset(sample_asset):
    client.post('/assets', json=sample_asset)
    updated_asset = {**sample_asset, 'status': 'Inactive'}
    response = client.put('/assets/TNK-1001', json=updated_asset)
    assert response.status_code == 200
    assert response.json()['status'] == 'Inactive'

def test_update_asset_invalid_id():
    response = client.put('/assets/NOT-FOUND', json=sample_asset)
    assert response.status_code == 404

def test_delete_asset(sample_asset):
    client.post('/assets', json=sample_asset)
    response = client.delete('/assets/TNK-1001')
    assert response.status_code == 200
    assert response.json() == {'detail': 'Asset soft-deleted'}

def test_delete_asset_not_found():
    response = client.delete('/assets/NOT-FOUND')
    assert response.status_code == 404
