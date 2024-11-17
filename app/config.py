"""
Application Settings

This module defines the application settings using Pydantic's BaseSettings.
It loads configuration values from an environment file (.env) for environment-specific settings, including database connection details.
"""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST"]

    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file="app/.env")


settings = Settings()
