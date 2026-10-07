from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import pandas as pd
import os

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

class Asset(BaseModel):
    asset_id: str = Field(..., regex='^[A-Z]{3}-\d{4}$')
    asset_type: str
    unit: str
    location: str
    install_year: int
    last_inspection: str
    operating_hours: int
    status: str
    criticality: str = Field(..., regex='^(High|Medium|Low)$')
    notes: Optional[str] = None
    
    @field_validator('asset_id')
    def validate_asset_id(cls, v):
        return v

assets_db = []

@app.on_event('startup')
async def load_data():
    global assets_db
    csv_path = os.path.join(os.path.dirname(__file__), 'maintenance_assets.csv')
    assets_db = pd.read_csv(csv_path).to_dict(orient='records')

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(content={'errors': [{'field': e['loc'][-1], 'reason': e['msg']} for e in exc.errors()]}, status_code=422)

@app.post('/assets', response_model=Asset)
async def create_asset(asset: Asset):
    assets_db.append(asset.model_dump())
    return asset

@app.get('/assets', response_model=List[Asset])
async def list_assets(status: Optional[str] = Query(None), unit: Optional[str] = Query(None), criticality: Optional[str] = Query(None)):
    filtered_assets = [asset for asset in assets_db if (status is None or asset['status'] == status) and (unit is None or asset['unit'] == unit) and (criticality is None or asset['criticality'] == criticality)]
    return filtered_assets

@app.get('/assets/{asset_id}', response_model=Asset)
async def get_asset(asset_id: str):
    for asset in assets_db:
        if asset['asset_id'] == asset_id:
            return asset
    raise HTTPException(status_code=404, detail='Asset not found')

@app.put('/assets/{asset_id}', response_model=Asset)
async def update_asset(asset_id: str, asset: Asset):
    for index, existing_asset in enumerate(assets_db):
        if existing_asset['asset_id'] == asset_id:
            assets_db[index] = asset.model_dump()
            return asset
    raise HTTPException(status_code=404, detail='Asset not found')

@app.delete('/assets/{asset_id}')
async def delete_asset(asset_id: str):
    for index, asset in enumerate(assets_db):
        if asset['asset_id'] == asset_id:
            assets_db[index]['status'] = 'Deleted'
            return {'detail': 'Asset soft-deleted'}
    raise HTTPException(status_code=404, detail='Asset not found')
