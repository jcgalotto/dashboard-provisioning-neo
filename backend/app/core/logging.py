"""Logging configuration utilities."""
from __future__ import annotations

import logging
from logging.config import dictConfig


def configure_logging() -> None:
    """Configure structured logging for the application."""

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": "INFO",
                }
            },
            "root": {"level": "INFO", "handlers": ["console"]},
        }
    )


logger = logging.getLogger("dashboard_provisioning")
