"""Shared API dependencies."""
from __future__ import annotations

from provisioning_api.core.config import Settings, get_settings


def get_app_settings() -> Settings:
    """Provide application settings for dependency injection."""

    return get_settings()
