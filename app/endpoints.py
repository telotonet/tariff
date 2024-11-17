"""
This module contains the API routes for uploading tariff data and calculating insurance costs.

It includes the following endpoints:
- POST /upload_tariffs/: Uploads tariff data from a JSON file into the database.
- POST /calculate_insurance/: Calculates the insurance cost based on cargo type, declared value, and date.

It relies on SQLAlchemy for database interactions and FastAPI for creating the REST API endpoints.
"""

import json
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Tariff
from app.schemas import (InsuranceCalculationRequest,
                         InsuranceCalculationResponse, TariffCreate)
from app.services import calculate_insurance_cost

router = APIRouter()


@router.post("/upload_tariffs/")
async def upload_tariffs(
    file: UploadFile = File(...), session: AsyncSession = Depends(get_db)
):
    """
    Uploads tariff data from a JSON file into the database.

    Args:
        file (UploadFile): The JSON file containing tariff data.
        session (AsyncSession): The database session.

    Returns:
        dict: A status message indicating success.

    Raises:
        HTTPException: If there is an error during the file upload or processing.
    """
    contents = await file.read()
    data = json.loads(contents.decode("utf-8"))

    tariffs = []
    for date_str, rate_data in data.items():
        effective_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        for item in rate_data:
            tariffs.append(
                TariffCreate(
                    cargo_type=item["cargo_type"],
                    rate=float(item["rate"]),
                    effective_date=effective_date,
                )
            )

    for tariff in tariffs:
        db_tariff = Tariff(**tariff.model_dump())
        session.add(db_tariff)

    await session.commit()
    return {"status": "success"}


@router.post("/calculate_insurance/", response_model=InsuranceCalculationResponse)
async def calculate_insurance(
    request: InsuranceCalculationRequest, session: AsyncSession = Depends(get_db)
):
    """
    Calculates the insurance cost based on cargo type, declared value, and date.

    Args:
        request (InsuranceCalculationRequest): The request object containing cargo type, declared value, and date.
        session (AsyncSession): The database session.

    Returns:
        InsuranceCalculationResponse: A response object containing the calculated insurance cost, cargo type, rate, and date.

    Raises:
        HTTPException: If no rate is found for the provided cargo type and date.
    """
    try:
        insurance_cost = await calculate_insurance_cost(
            session, request.cargo_type, request.declared_value, request.date
        )
    except ValueError:
        raise HTTPException(
            status_code=404, detail="Rate not found for this cargo type and date"
        )

    return InsuranceCalculationResponse(
        insurance_cost=insurance_cost,
        cargo_type=request.cargo_type,
        rate=insurance_cost / request.declared_value,
        date=request.date,
    )
