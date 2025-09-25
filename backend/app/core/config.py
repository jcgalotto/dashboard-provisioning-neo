"""Application configuration module."""
from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Runtime configuration values."""

    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    api_prefix: str = "/api"

    class Config:
        populate_by_name = True


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings instance."""

    return Settings()
