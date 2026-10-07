# Maintenance Mini-App

## Description
This is a FastAPI application for managing maintenance records of assets.

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd maintenance_mini_app
   ```
2. Install dependencies:
   ```bash
   pip install fastapi[all] pandas pytest
   ```
3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```
4. Access the API at `http://127.0.0.1:8000/assets`

## Endpoints
- `POST /assets`: Create a new asset.
- `GET /assets`: List all assets with optional filters.
- `GET /assets/{asset_id}`: Retrieve a specific asset.
- `PUT /assets/{asset_id}`: Update an existing asset.
- `DELETE /assets/{asset_id}`: Soft-delete an asset.

## Testing
Run the tests using:
```bash
pytest -q
```