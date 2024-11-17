"""
Test Utilities for Insurance Tariff Calculation API

This module provides utility functions, fixtures, and setup for testing the API. 
It includes database preparation, test client creation, and helper functions for adding test data.

Modules:
    - `pytest`: Testing framework for managing test cases and fixtures.
    - `httpx`: Used for creating an asynchronous test client for the application.
    - `sqlalchemy`: Manages test database connections and sessions.
    - `app.config`, `app.database`, `app.main`: Application-specific configurations, database models, and the main FastAPI application.
"""

import json

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = settings.DATABASE_URL
test_engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)

async_session_maker = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession
)


async def override_get_db():
    """
    Override the default database dependency with a test session.

    Yields:
        AsyncSession: A database session for testing.
    """
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    """
    Fixture to prepare the test database by creating and dropping tables.

    Ensures tests are run only in TEST mode to avoid altering production data.
    """
    assert settings.MODE == "TEST", "Tests should only be run in TEST mode"

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    """
    Fixture to create an asynchronous test client for the application.

    Yields:
        AsyncClient: The test client.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_db_session():
    """
    Fixture to provide an asynchronous database session for tests.

    Yields:
        AsyncSession: A session connected to the test database.
    """
    async with async_session_maker() as session:
        yield session


async def add_test_data(client):
    """
    Add test tariff data to the database through an API endpoint.

    Args:
        client (AsyncClient): The asynchronous test client.

    Raises:
        AssertionError: If the API response status code or content is incorrect.
    """
    file_data = {
        "2020-06-01": [
            {"cargo_type": "Glass", "rate": 0.05},
            {"cargo_type": "Metal", "rate": 0.03},
        ]
    }
    file_content = json.dumps(file_data).encode("utf-8")

    response = await client.post(
        "/upload_tariffs/",
        files={"file": ("test_file.json", file_content, "application/json")},
    )

    assert response.status_code == 200
    assert response.json() == {"status": "success"}
