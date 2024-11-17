"""
Insurance Tariff Calculation API

This FastAPI application provides endpoints for uploading tariff data and calculating 
insurance costs based on cargo type, declared value, and date. It allows for dynamic 
tariff updates and ensures accurate cost calculation.

Includes a health check endpoint to monitor application status.
"""

from fastapi import FastAPI

from app.endpoints import router as tariff_router

app = FastAPI(
    title="Insurance Tariff Calculation API",
    description="API for uploading and calculating insurance tariffs based on cargo type and declared value.",
)

app.include_router(tariff_router)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
