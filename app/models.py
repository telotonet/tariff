from sqlalchemy import Column, Date, Float, Integer, String

from app.database import Base


class Tariff(Base):
    """
    Represents a tariff record for cargo insurance.

    Attributes:
        id (int): The unique identifier for the tariff.
        cargo_type (str): The type of cargo (e.g., "Glass", "Other").
        rate (float): The insurance rate for the given cargo type.
        effective_date (date): The date from which the tariff is effective.

    The model corresponds to the "tariffs" table in the database.
    """

    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True, index=True)
    cargo_type = Column(String, index=True)
    rate = Column(Float)
    effective_date = Column(Date, index=True)
