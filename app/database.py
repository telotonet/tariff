"""
Database Module

This module sets up the database connection using SQLAlchemy's asynchronous capabilities.
It provides a session maker for creating database sessions and a base class for declarative models.
"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_async_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()


async def get_db():
    """
    Dependency that provides a database session.

    This function creates a new database session for each request, yielding the session and ensuring proper cleanup after use. It can be used as a dependency in FastAPI routes to access the database.

    Yields:
        AsyncSession: An asynchronous database session.
    """
    session = SessionLocal()
    try:
        yield session
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
    finally:
        await session.close()
