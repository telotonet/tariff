from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Tariff


async def get_rate_for_date_and_cargo(
    session: AsyncSession, cargo_type: str, date: str
):
    """
    Retrieves the most recent tariff rate for a given cargo type and date.

    Args:
        session (AsyncSession): The database session used to execute the query.
        cargo_type (str): The type of cargo (e.g., "Glass", "Other").
        date (str): The date (in "YYYY-MM-DD" format) for which the rate is requested.

    Returns:
        Tariff | None: The most recent `Tariff` object matching the cargo type and effective date, or `None` if not found.

    Raises:
        ValueError: If no rate is found for the given cargo type and date.
    """
    effective_date = datetime.strptime(date, "%Y-%m-%d").date()

    query = (
        select(Tariff)
        .filter(
            Tariff.cargo_type == cargo_type, Tariff.effective_date <= effective_date
        )
        .order_by(Tariff.effective_date.desc())
        .limit(1)
    )

    result = await session.execute(query)
    return result.scalars().first()


async def calculate_insurance_cost(
    session: AsyncSession, cargo_type: str, declared_value: float, date: str
):
    """
    Calculates the insurance cost based on the cargo type, declared value, and date.

    Args:
        session (AsyncSession): The database session used to execute the query.
        cargo_type (str): The type of cargo (e.g., "Glass", "Other").
        declared_value (float): The declared value of the cargo for insurance purposes.
        date (str): The date (in "YYYY-MM-DD" format) for which the insurance cost is being calculated.

    Returns:
        float: The calculated insurance cost based on the tariff rate and declared value.

    Raises:
        ValueError: If no tariff is found for the given cargo type and date, a ValueError is raised.
    """
    tariff = await get_rate_for_date_and_cargo(session, cargo_type, date)

    if not tariff:
        raise ValueError("Rate not found for this cargo type and date")

    return declared_value * tariff.rate
