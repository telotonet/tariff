"""
Schemas for the Insurance Tariff Calculation API

This module defines Pydantic schemas used for validating request and response data in the API.
Schemas are used to define the structure of tariff data, insurance calculation requests, 
and responses, ensuring data integrity and validation.
"""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class TariffBase(BaseModel):
    """
    Base schema for Tariff data.

    Attributes:
        cargo_type (str): The type of cargo (e.g., "Glass", "Other").
        rate (float): The insurance rate for the given cargo type.
        effective_date (date): The date from which the tariff is effective.
    """

    cargo_type: str = Field(
        ..., description="The type of cargo (e.g., 'Glass', 'Other')"
    )
    rate: float = Field(..., description="The insurance rate for the given cargo type")
    effective_date: date = Field(
        ..., description="The date from which the tariff is effective"
    )

    model_config = ConfigDict(from_attributes=True)


class TariffCreate(TariffBase):
    """
    Schema for creating a new Tariff.

    Attributes:
        cargo_type (str): The type of cargo (e.g., "Glass", "Other").
        rate (float): The insurance rate for the given cargo type.
        effective_date (date): The date from which the tariff is effective.
    """

    pass


class Tariff(TariffBase):
    """
    Schema for retrieving a Tariff from the database.

    Attributes:
        id (int): The unique identifier for the tariff record.
        cargo_type (str): The type of cargo.
        rate (float): The insurance rate for the cargo.
        effective_date (date): The date the tariff is effective.
    """

    id: int = Field(..., description="The unique identifier for the tariff record")


class InsuranceCalculationRequest(BaseModel):
    """
    Schema for calculating insurance costs.

    Attributes:
        cargo_type (str): The type of cargo (e.g., "Glass", "Other").
        declared_value (float): The declared value of the cargo, used to calculate the insurance cost.
        date (str): The date for which the tariff should be applied.
    """

    cargo_type: str = Field(
        ..., description="The type of cargo (e.g., 'Glass', 'Other')"
    )
    declared_value: float = Field(..., description="The declared value of the cargo")
    date: str = Field(..., description="The date for applying the tariff")


class InsuranceCalculationResponse(BaseModel):
    """
    Schema for the insurance cost calculation response.

    Attributes:
        insurance_cost (float): The calculated insurance cost based on the cargo type and declared value.
        cargo_type (str): The type of cargo.
        rate (float): The rate applied for the calculation.
        date (str): The date used for applying the tariff rate.
    """

    insurance_cost: float = Field(..., description="The calculated insurance cost")
    cargo_type: str = Field(..., description="The type of cargo")
    rate: float = Field(..., description="The rate applied for the calculation")
    date: str = Field(..., description="The date the tariff is applied")
