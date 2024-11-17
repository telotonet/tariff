"""
Tests for Insurance Tariff Calculation API

This module provides tests for the application's core endpoints, including:
- Health check verification
- Tariff upload functionality
- Insurance cost calculation

Each test ensures that the API behaves as expected under various scenarios.
"""

from datetime import datetime

import pytest
from fastapi import status
from sqlalchemy import text

from tests.conftest import add_test_data


async def test_health(client):
    """
    Verify the health check endpoint functionality.

    Ensures the `/healthcheck` endpoint returns a 200 OK status with the expected response body.

    Args:
        client (AsyncClient): The asynchronous test client.

    Asserts:
        - Status code is 200 (HTTP OK).
        - Response JSON is {"status": "ok"}.
    """
    response = await client.get("/healthcheck")
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Unexpected status code: {response.status_code}"
    assert response.json() == {
        "status": "ok"
    }, f"Unexpected response: {response.json()}"


@pytest.mark.asyncio
async def test_upload_tariffs(client, test_db_session):
    """
    Test the tariff upload functionality.

    This test validates that tariffs can be uploaded and correctly stored in the database.

    Args:
        client (AsyncClient): The asynchronous test client.
        test_db_session (AsyncSession): The database session for testing.

    Asserts:
        - Two tariffs are successfully added to the database.
        - Tariff data matches the expected values.
    """
    await add_test_data(client)

    # Fetch the tariffs from the database
    result = await test_db_session.execute(text("SELECT * FROM tariffs"))
    tariffs = result.fetchall()

    assert len(tariffs) == 2, f"Expected 2 tariffs, got {len(tariffs)}"
    assert (
        tariffs[0].cargo_type == "Glass"
    ), f"Unexpected cargo type: {tariffs[0].cargo_type}"
    assert (
        tariffs[1].cargo_type == "Metal"
    ), f"Unexpected cargo type: {tariffs[1].cargo_type}"
    assert tariffs[0].rate == 0.05, f"Unexpected rate: {tariffs[0].rate}"
    assert tariffs[1].rate == 0.03, f"Unexpected rate: {tariffs[1].rate}"
    assert (
        datetime.strptime(tariffs[0].effective_date, "%Y-%m-%d").date()
        == datetime(2020, 6, 1).date()
    ), f"Unexpected effective date: {tariffs[0].effective_date}"


@pytest.mark.asyncio
async def test_calculate_insurance(client):
    """
    Test the insurance cost calculation endpoint.

    Validates that the `/calculate_insurance/` endpoint calculates the insurance cost correctly
    for a given cargo type, declared value, and date.

    Args:
        client (AsyncClient): The asynchronous test client.

    Asserts:
        - Status code is 200 (HTTP OK).
        - Response JSON matches the expected insurance calculation results.
    """
    await add_test_data(client)

    request_data = {
        "cargo_type": "Glass",
        "declared_value": 10000.0,
        "date": "2020-06-01",
    }

    response = await client.post("/calculate_insurance/", json=request_data)

    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    assert response.json() == {
        "insurance_cost": 500.0,
        "cargo_type": "Glass",
        "rate": 0.05,
        "date": "2020-06-01",
    }, f"Unexpected response: {response.json()}"


@pytest.mark.asyncio
async def test_calculate_insurance_no_rate(client):
    """
    Test insurance cost calculation with a missing rate.

    Verifies that the `/calculate_insurance/` endpoint handles cases where no tariff is found
    for the provided cargo type and date.

    Args:
        client (AsyncClient): The asynchronous test client.

    Asserts:
        - Status code is 404 (Not Found).
        - Response JSON contains the expected error message.
    """
    request_data = {
        "cargo_type": "Wood",
        "declared_value": 10000.0,
        "date": "2020-06-01",
    }

    response = await client.post("/calculate_insurance/", json=request_data)

    assert (
        response.status_code == 404
    ), f"Unexpected status code: {response.status_code}"
    assert response.json() == {
        "detail": "Rate not found for this cargo type and date"
    }, f"Unexpected response: {response.json()}"
