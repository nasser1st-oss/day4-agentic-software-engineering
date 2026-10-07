import csv
import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator


CSV_PATH = os.path.join(os.path.dirname(__file__), "maintenance_assets.csv")


class Asset(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset_id: str
    asset_type: str
    unit: str
    location: str
    install_year: int
    last_inspection: str
    operating_hours: int
    status: str
    criticality: str
    notes: Optional[str] = None

    @field_validator("asset_id")
    @classmethod
    def validate_asset_id(cls, value: str) -> str:
        import re

        if not re.fullmatch(r"[A-Z]{3}-\d{4}", value):
            raise ValueError(
                "asset_id must match the format XXX-1234"
            )
        return value

    @field_validator("criticality")
    @classmethod
    def validate_criticality(cls, value: str) -> str:
        if value not in {"High", "Medium", "Low"}:
            raise ValueError(
                "criticality must be one of: High, Medium, Low"
            )
        return value


assets: list[dict] = []


def load_assets() -> None:
    assets.clear()

    with open(CSV_PATH, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            asset = Asset(
                asset_id=row["asset_id"],
                asset_type=row["asset_type"],
                unit=row["unit"],
                location=row["location"],
                install_year=int(row["install_year"]),
                last_inspection=row["last_inspection"],
                operating_hours=int(row["operating_hours"]),
                status=row["status"],
                criticality=row["criticality"],
                notes=row.get("notes") or None,
            )
            assets.append(asset.model_dump())


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_assets()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    errors = []

    for error in exc.errors():
        field = error["loc"][-1]
        reason = error["msg"]
        errors.append({"field": field, "reason": reason})

    return JSONResponse(
        status_code=422,
        content={"errors": errors},
    )


@app.post("/assets", response_model=Asset, status_code=200)
async def create_asset(asset: Asset):
    if any(existing["asset_id"] == asset.asset_id for existing in assets):
        raise HTTPException(
            status_code=409,
            detail="Asset already exists",
        )

    assets.append(asset.model_dump())
    return asset


@app.get("/assets", response_model=list[Asset])
async def list_assets(
    status: Optional[str] = None,
    unit: Optional[str] = None,
    criticality: Optional[str] = None,
):
    result = assets

    if status is not None:
        result = [a for a in result if a["status"] == status]

    if unit is not None:
        result = [a for a in result if a["unit"] == unit]

    if criticality is not None:
        result = [a for a in result if a["criticality"] == criticality]

    return result


@app.get("/assets/{asset_id}", response_model=Asset)
async def get_asset(asset_id: str):
    for asset in assets:
        if asset["asset_id"] == asset_id:
            return asset

    raise HTTPException(
        status_code=404,
        detail="Asset not found",
    )


@app.put("/assets/{asset_id}", response_model=Asset)
async def update_asset(asset_id: str, asset: Asset):
    for index, existing in enumerate(assets):
        if existing["asset_id"] == asset_id:
            if asset.asset_id != asset_id:
                raise HTTPException(
                    status_code=400,
                    detail="asset_id cannot be changed",
                )

            assets[index] = asset.model_dump()
            return assets[index]

    raise HTTPException(
        status_code=404,
        detail="Asset not found",
    )


@app.delete("/assets/{asset_id}")
async def delete_asset(asset_id: str):
    for asset in assets:
        if asset["asset_id"] == asset_id:
            asset["status"] = "Deleted"
            return {"detail": "Asset deleted"}

    raise HTTPException(
        status_code=404,
        detail="Asset not found",
    )
# Lab 4.1 PR review test change

# Lab 4.1 PR review test change
